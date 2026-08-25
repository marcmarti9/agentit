"""Mechanical access to Agentit's provenance-aware reference catalog.

The primary AI owns semantic selection of reference packs and sources. This module
only validates, filters, and returns explicitly selected catalog entries. It must
never infer a reference pack from natural-language task text.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = REPO_ROOT / "references" / "catalog.yaml"
VALID_EVIDENCE_LEVELS = {
    "canonical",
    "licensed_artifact",
    "corroborated",
    "creator_claim",
    "inspiration",
    "unverified",
}


class ReferenceCatalogError(ValueError):
    """Raised when reference catalog data or explicit selectors are invalid."""


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_CATALOG
    if not target.is_file() or target.is_symlink():
        raise ReferenceCatalogError(f"reference catalog not found or symlink rejected: {target}")
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReferenceCatalogError(f"cannot load reference catalog {target}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ReferenceCatalogError("reference catalog must use schema_version: 1")
    validate_catalog(data)
    return data


def validate_catalog(data: dict[str, Any]) -> None:
    if data.get("policy", {}).get("semantic_selection_owner") != "primary_ai":
        raise ReferenceCatalogError("reference policy must keep semantic selection with primary_ai")
    if data.get("policy", {}).get("software_role") != "mechanical_index_only":
        raise ReferenceCatalogError("reference software role must be mechanical_index_only")

    sources = data.get("sources")
    packs = data.get("packs")
    if not isinstance(sources, list):
        raise ReferenceCatalogError("reference catalog must define a sources list")
    if not isinstance(packs, dict):
        raise ReferenceCatalogError("reference catalog must define a packs mapping")

    by_id: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ReferenceCatalogError(f"source {index} must be a mapping")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise ReferenceCatalogError(f"source {index} has invalid id")
        if source_id in by_id:
            raise ReferenceCatalogError(f"duplicate reference source id: {source_id}")
        url = source.get("url")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            raise ReferenceCatalogError(f"reference source {source_id} must have an http(s) url")
        level = source.get("evidence_level")
        if level not in VALID_EVIDENCE_LEVELS:
            raise ReferenceCatalogError(
                f"reference source {source_id} has invalid evidence_level: {level!r}"
            )
        domains = source.get("domains")
        if not isinstance(domains, list) or not all(isinstance(item, str) for item in domains):
            raise ReferenceCatalogError(f"reference source {source_id} domains must be a string list")
        by_id[source_id] = source

    for pack_id, pack in packs.items():
        if not isinstance(pack_id, str) or not pack_id:
            raise ReferenceCatalogError("reference pack ids must be non-empty strings")
        if not isinstance(pack, dict):
            raise ReferenceCatalogError(f"reference pack {pack_id} must be a mapping")
        source_ids = pack.get("sources")
        if not isinstance(source_ids, list) or not all(isinstance(item, str) for item in source_ids):
            raise ReferenceCatalogError(f"reference pack {pack_id} sources must be a string list")
        unknown = [item for item in source_ids if item not in by_id]
        if unknown:
            raise ReferenceCatalogError(
                f"reference pack {pack_id} contains unknown sources: {', '.join(unknown)}"
            )


def _sources_by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in data["sources"]}


def list_sources(
    data: dict[str, Any] | None = None,
    *,
    domain: str | None = None,
    tag: str | None = None,
    evidence_level: str | None = None,
) -> list[dict[str, Any]]:
    catalog = data or load_catalog()
    rows: list[dict[str, Any]] = []
    for source in catalog["sources"]:
        if domain and domain not in source.get("domains", []):
            continue
        if tag and tag not in source.get("tags", []):
            continue
        if evidence_level and source.get("evidence_level") != evidence_level:
            continue
        rows.append(
            {
                "id": source.get("id"),
                "title": source.get("title"),
                "kind": source.get("kind"),
                "domains": source.get("domains"),
                "tags": source.get("tags"),
                "evidence_level": source.get("evidence_level"),
                "verification_status": source.get("verification_status"),
                "checked_at": source.get("checked_at"),
                "url": source.get("url"),
                "canonical_url": source.get("canonical_url"),
                "disposition": (source.get("integration") or {}).get("disposition"),
            }
        )
    return sorted(rows, key=lambda row: str(row["id"]))


def get_source(source_id: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = data or load_catalog()
    source = _sources_by_id(catalog).get(source_id)
    if source is None:
        known = ", ".join(sorted(_sources_by_id(catalog)))
        raise ReferenceCatalogError(f"unknown reference source '{source_id}'; known: {known}")
    return source


def list_packs(data: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = data or load_catalog()
    return dict(catalog["packs"])


def get_pack(pack_id: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = data or load_catalog()
    packs = catalog["packs"]
    if pack_id not in packs:
        known = ", ".join(sorted(packs))
        raise ReferenceCatalogError(f"unknown reference pack '{pack_id}'; known: {known}")
    pack = packs[pack_id]
    return {
        "id": pack_id,
        "description": pack.get("description"),
        "sources": [get_source(source_id, catalog) for source_id in pack.get("sources", [])],
        "policy": catalog.get("policy"),
    }


def catalog_summary(data: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = data or load_catalog()
    levels: dict[str, int] = {}
    for source in catalog["sources"]:
        level = str(source["evidence_level"])
        levels[level] = levels.get(level, 0) + 1
    return {
        "schema_version": catalog.get("schema_version"),
        "purpose": catalog.get("purpose"),
        "policy": catalog.get("policy"),
        "source_count": len(catalog["sources"]),
        "pack_count": len(catalog["packs"]),
        "evidence_levels": levels,
        "packs": {
            pack_id: {
                "description": pack.get("description"),
                "source_count": len(pack.get("sources", [])),
            }
            for pack_id, pack in catalog["packs"].items()
        },
    }


def _emit(payload: Any, *, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Mechanical Agentit reference-catalog access; the AI chooses explicit packs/sources."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List/filter catalog metadata mechanically")
    list_parser.add_argument("--domain")
    list_parser.add_argument("--tag")
    list_parser.add_argument("--evidence-level", choices=sorted(VALID_EVIDENCE_LEVELS))
    list_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    show_parser = sub.add_parser("show", help="Show one explicitly selected source")
    show_parser.add_argument("source_id")
    show_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    pack_parser = sub.add_parser("pack", help="Load one explicitly selected reference pack")
    pack_parser.add_argument("pack_id")
    pack_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    packs_parser = sub.add_parser("packs", help="List named packs; no semantic recommendation")
    packs_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    summary_parser = sub.add_parser("summary", help="Show catalog counts/policy")
    summary_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    validate_parser = sub.add_parser("validate", help="Validate catalog schema/references")
    validate_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        catalog = load_catalog(args.catalog)
        if args.command == "list":
            payload = list_sources(
                catalog,
                domain=args.domain,
                tag=args.tag,
                evidence_level=args.evidence_level,
            )
        elif args.command == "show":
            payload = get_source(args.source_id, catalog)
        elif args.command == "pack":
            payload = get_pack(args.pack_id, catalog)
        elif args.command == "packs":
            payload = list_packs(catalog)
        elif args.command == "summary":
            payload = catalog_summary(catalog)
        else:
            validate_catalog(catalog)
            payload = {"valid": True, "source_count": len(catalog["sources"]), "pack_count": len(catalog["packs"])}
    except ReferenceCatalogError as exc:
        parser.error(str(exc))
    _emit(payload, output_format=getattr(args, "format", "yaml"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
