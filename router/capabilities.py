"""Provider-neutral capability catalog and least-privilege resolver.

This module plans bindings only. It never discovers credentials, installs a
provider, enables a tool, or executes a capability.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_CAPABILITY_CATALOG = REPOSITORY / "capabilities" / "catalog.yaml"
DEFAULT_SPECIALIST_CATALOG = REPOSITORY / "agents" / "catalog.yaml"
VALID_PROVIDER_KINDS = {"chatgpt_app", "mcp", "cli", "local"}


class CapabilityCatalogError(ValueError):
    """Raised when capability or specialist policy is invalid."""


def _unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _load_yaml(path: Path, *, label: str) -> dict[str, Any]:
    if yaml is None:
        raise CapabilityCatalogError("PyYAML is required for capability resolution")
    if not path.is_file() or path.is_symlink():
        raise CapabilityCatalogError(f"{label} not found or symlink rejected: {path}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CapabilityCatalogError(f"cannot load {label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CapabilityCatalogError(f"{label} root must be a mapping")
    return payload


def load_capability_catalog(path: Path | None = None) -> dict[str, Any]:
    payload = _load_yaml(path or DEFAULT_CAPABILITY_CATALOG, label="capability catalog")
    if payload.get("schema_version") != 1:
        raise CapabilityCatalogError("capability catalog requires schema_version: 1")
    policy = payload.get("policy")
    providers = payload.get("providers")
    capabilities = payload.get("capabilities")
    if not isinstance(policy, dict) or not policy.get("provider_neutral"):
        raise CapabilityCatalogError("capability catalog must declare provider-neutral policy")
    if not isinstance(providers, dict) or not providers:
        raise CapabilityCatalogError("capability catalog providers must be a non-empty mapping")
    if not isinstance(capabilities, dict) or not capabilities:
        raise CapabilityCatalogError("capability catalog capabilities must be a non-empty mapping")
    for provider_id, provider in providers.items():
        if not isinstance(provider_id, str) or not provider_id:
            raise CapabilityCatalogError("provider IDs must be non-empty strings")
        if not isinstance(provider, dict) or provider.get("kind") not in VALID_PROVIDER_KINDS:
            raise CapabilityCatalogError(f"invalid provider kind for {provider_id}")
        hosts = provider.get("hosts")
        if not isinstance(hosts, list) or not hosts or not all(isinstance(host, str) and host for host in hosts):
            raise CapabilityCatalogError(f"provider hosts must be a string list: {provider_id}")
    for capability_id, capability in capabilities.items():
        if not isinstance(capability_id, str) or "." not in capability_id:
            raise CapabilityCatalogError(f"invalid capability ID: {capability_id!r}")
        if not isinstance(capability, dict) or not capability.get("description"):
            raise CapabilityCatalogError(f"capability needs a description: {capability_id}")
        implementations = capability.get("implementations")
        if not isinstance(implementations, list) or not implementations:
            raise CapabilityCatalogError(f"capability needs implementations: {capability_id}")
        seen_providers: set[str] = set()
        for binding in implementations:
            if not isinstance(binding, dict):
                raise CapabilityCatalogError(f"invalid implementation for {capability_id}")
            provider_id = binding.get("provider")
            permissions = binding.get("permissions")
            if provider_id not in providers:
                raise CapabilityCatalogError(f"unknown provider binding for {capability_id}: {provider_id}")
            if provider_id in seen_providers:
                raise CapabilityCatalogError(f"duplicate provider binding for {capability_id}: {provider_id}")
            seen_providers.add(provider_id)
            if not isinstance(permissions, list) or not permissions or not all(isinstance(p, str) and p for p in permissions):
                raise CapabilityCatalogError(f"permissions must be a non-empty string list: {capability_id}/{provider_id}")
    return payload


def specialist_capability_requirements(
    specialist_ids: Sequence[str],
    *,
    specialist_catalog_path: Path | None = None,
    capability_catalog: dict[str, Any] | None = None,
) -> dict[str, list[str]]:
    catalog = capability_catalog or load_capability_catalog()
    payload = _load_yaml(specialist_catalog_path or DEFAULT_SPECIALIST_CATALOG, label="specialist catalog")
    specialists = payload.get("specialists")
    if not isinstance(specialists, list):
        raise CapabilityCatalogError("specialist catalog must define a specialists list")
    indexed = {item.get("id"): item for item in specialists if isinstance(item, dict) and isinstance(item.get("id"), str)}
    required: list[str] = []
    preferred: list[str] = []
    known = set(catalog["capabilities"])
    for specialist_id in _unique(specialist_ids):
        specialist = indexed.get(specialist_id)
        if specialist is None:
            raise CapabilityCatalogError(f"unknown specialist: {specialist_id}")
        declaration = specialist.get("capabilities")
        if not isinstance(declaration, dict):
            raise CapabilityCatalogError(f"specialist lacks capabilities: {specialist_id}")
        for field, target in (("required", required), ("preferred", preferred)):
            values = declaration.get(field, [])
            if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
                raise CapabilityCatalogError(f"specialist {specialist_id} {field} capabilities must be a string list")
            unknown = set(values) - known
            if unknown:
                raise CapabilityCatalogError(f"specialist {specialist_id} references unknown capabilities: {sorted(unknown)}")
            target.extend(values)
    required_unique = _unique(required)
    return {"required": required_unique, "preferred": [item for item in _unique(preferred) if item not in required_unique]}


def resolve_capabilities(
    *,
    required: Sequence[str],
    preferred: Sequence[str],
    available_providers: Sequence[str] | None,
    host: str,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = catalog or load_capability_catalog()
    known_capabilities = data["capabilities"]
    providers = data["providers"]
    known_hosts = {
        provider_host
        for provider in providers.values()
        for provider_host in provider["hosts"]
    }
    if host not in known_hosts:
        raise CapabilityCatalogError(
            f"unknown provider host '{host}'; known: {', '.join(sorted(known_hosts))}"
        )
    required_ids = _unique(required)
    preferred_ids = [item for item in _unique(preferred) if item not in required_ids]
    requested = required_ids + preferred_ids
    unknown = [item for item in requested if item not in known_capabilities]
    if unknown:
        raise CapabilityCatalogError(f"unknown requested capabilities: {unknown}")
    inventory_provided = available_providers is not None
    available = set(available_providers or ())
    if inventory_provided:
        unknown_providers = sorted(available - set(providers))
        if unknown_providers:
            raise CapabilityCatalogError(f"inventory contains unknown providers: {unknown_providers}")
    grants: list[dict[str, Any]] = []
    unresolved_required: list[str] = []
    unresolved_preferred: list[str] = []
    resolution: dict[str, Any] = {}
    for capability_id in requested:
        candidates: list[dict[str, Any]] = []
        selected: dict[str, Any] | None = None
        for binding in known_capabilities[capability_id]["implementations"]:
            provider_id = binding["provider"]
            compatible = host in providers[provider_id]["hosts"]
            candidate = {"provider": provider_id, "kind": providers[provider_id]["kind"], "selected": False, "reason": None}
            if not inventory_provided:
                candidate["reason"] = "inventory_not_provided"
            elif not compatible:
                candidate["reason"] = "host_incompatible"
            elif provider_id not in available:
                candidate["reason"] = "provider_unavailable"
            elif selected is None:
                candidate["selected"] = True
                candidate["reason"] = "selected"
                selected = binding
            else:
                candidate["reason"] = "higher_priority_selected"
            candidates.append(candidate)
        required_capability = capability_id in required_ids
        resolution[capability_id] = {"required": required_capability, "selected_provider": selected["provider"] if selected else None, "candidates": candidates}
        if selected:
            provider_id = selected["provider"]
            grants.append({"capability": capability_id, "required": required_capability, "provider": provider_id, "provider_kind": providers[provider_id]["kind"], "permissions": list(selected["permissions"])})
        elif inventory_provided:
            (unresolved_required if required_capability else unresolved_preferred).append(capability_id)
    if not requested:
        status = "not_required"
    elif not inventory_provided:
        status = "inventory_required"
    elif unresolved_required:
        status = "degraded"
    elif unresolved_preferred:
        status = "resolved_with_optional_gaps"
    else:
        status = "resolved"
    return {
        "schema_version": 1,
        "status": status,
        "host": host,
        "inventory_provided": inventory_provided,
        "least_privilege": True,
        "requested": {"required": required_ids, "preferred": preferred_ids},
        "grants": grants,
        "unresolved_required": unresolved_required,
        "unresolved_preferred": unresolved_preferred,
        "pending_inventory": requested if not inventory_provided else [],
        "resolution": resolution,
    }


def validate_capability_envelope(
    envelope: dict[str, Any],
    *,
    catalog: dict[str, Any] | None = None,
) -> None:
    """Fail closed when a projected grant diverges from catalog policy."""
    data = catalog or load_capability_catalog()
    if envelope.get("schema_version") != 1 or envelope.get("least_privilege") is not True:
        raise CapabilityCatalogError("invalid capability envelope policy")
    requested = envelope.get("requested")
    grants = envelope.get("grants")
    resolution = envelope.get("resolution")
    if not isinstance(requested, dict) or not isinstance(grants, list) or not isinstance(resolution, dict):
        raise CapabilityCatalogError("invalid capability envelope shape")
    required = requested.get("required")
    preferred = requested.get("preferred")
    if not isinstance(required, list) or not isinstance(preferred, list):
        raise CapabilityCatalogError("invalid capability request shape")
    requested_ids = set(required) | set(preferred)
    seen: set[str] = set()
    for grant in grants:
        if not isinstance(grant, dict):
            raise CapabilityCatalogError("capability grants must be mappings")
        capability_id = grant.get("capability")
        provider_id = grant.get("provider")
        if capability_id not in requested_ids or capability_id in seen:
            raise CapabilityCatalogError(f"unexpected or duplicate capability grant: {capability_id}")
        seen.add(capability_id)
        capability = data["capabilities"].get(capability_id)
        provider = data["providers"].get(provider_id)
        if not capability or not provider:
            raise CapabilityCatalogError(f"unknown capability/provider grant: {capability_id}/{provider_id}")
        binding = next(
            (
                item
                for item in capability["implementations"]
                if item["provider"] == provider_id
            ),
            None,
        )
        if binding is None:
            raise CapabilityCatalogError(f"provider is not bound to capability: {capability_id}/{provider_id}")
        if grant.get("permissions") != binding["permissions"]:
            raise CapabilityCatalogError(f"grant permissions diverge from catalog: {capability_id}/{provider_id}")
        if grant.get("provider_kind") != provider["kind"]:
            raise CapabilityCatalogError(f"grant provider kind diverges from catalog: {provider_id}")
        if envelope.get("host") not in provider["hosts"]:
            raise CapabilityCatalogError(f"grant provider is incompatible with host: {provider_id}")
        if grant.get("required") is not (capability_id in required):
            raise CapabilityCatalogError(f"grant required flag diverges from request: {capability_id}")
        capability_resolution = resolution.get(capability_id)
        if not isinstance(capability_resolution, dict) or capability_resolution.get("selected_provider") != provider_id:
            raise CapabilityCatalogError(f"grant diverges from selected provider: {capability_id}")
