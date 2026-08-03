import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependency is optional for minimal installs
    yaml = None

try:
    from .route import route_task
except ImportError:  # unittest discover with router as the start directory
    from route import route_task


class RegistryRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if yaml is None:
            raise unittest.SkipTest("PyYAML no está instalado; se omite validación YAML")
        registry_path = Path(__file__).parents[1] / "registry.yaml"
        with registry_path.open(encoding="utf-8") as handle:
            cls.registry_ids = {entry["id"] for entry in yaml.safe_load(handle)["entries"]}

    def test_representative_router_outputs_resolve_in_registry(self):
        prompts = (
            "Implementa el login y la expiración de sesiones",
            "Audita el CRO y el copy de la landing",
            "Rediseña visualmente la pantalla",
            "Corrige el bug y añade una prueba",
            "Cambia el color del botón en este CSS",
        )
        emitted = {
            skill
            for prompt in prompts
            for skill in route_task(prompt)["skills"]
        }
        self.assertTrue(emitted)
        self.assertTrue(emitted <= self.registry_ids, emitted - self.registry_ids)

    def test_active_registry_entries_have_at_least_one_observed_path(self):
        registry_path = Path(__file__).parents[1] / "registry.yaml"
        entries = yaml.safe_load(registry_path.read_text(encoding="utf-8"))["entries"]
        for entry in entries:
            if entry.get("state") != "ACTIVE_GLOBAL":
                continue
            observed = any(Path(path).exists() for path in entry.get("paths", []))
            self.assertTrue(observed, entry["id"])


if __name__ == "__main__":
    unittest.main()
