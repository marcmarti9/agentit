import unittest
from pathlib import Path

try:
    from .profiles import load_catalog as load_profile_catalog, resolve_profile
    from .mcp_catalog import get_server, recommend_stack
except ImportError:
    from profiles import load_catalog as load_profile_catalog, resolve_profile
    from mcp_catalog import get_server, recommend_stack


REPOSITORY = Path(__file__).resolve().parents[1]


class DesignStudioTests(unittest.TestCase):
    def test_design_profile_contains_full_craft_stack(self):
        catalog = load_profile_catalog()
        skills = resolve_profile("design", catalog, repo_root=REPOSITORY)

        required = {
            "design-taste-frontend",
            "impeccable-design",
            "emil-design-eng",
            "design-inspiration-research",
            "design-trend-researcher",
            "creative-web-experiences",
            "visual-storytelling-director",
            "creative-tool-scout",
            "delight-and-whimsy",
            "figma-design-workflow",
            "scrollytelling-web",
            "gsap-scrolltrigger",
            "gsap-performance",
            "threejs-spatial-experiences",
            "threejs-product-storytelling",
            "browser-testing-with-devtools",
            "frontend-ui-engineering",
        }
        self.assertTrue(required.issubset(set(skills)), required - set(skills))

    def test_heavy_design_specialists_do_not_expand_global_core(self):
        catalog = load_profile_catalog()
        core = resolve_profile("core", catalog, repo_root=REPOSITORY)
        self.assertEqual(
            {"using-agentit", "task-router", "using-agent-skills"}, set(core)
        )
        self.assertNotIn("reference-intelligence", core)
        self.assertNotIn("specialist-agent-routing", core)
        self.assertNotIn("impeccable-design", core)
        self.assertNotIn("scrollytelling-web", core)
        self.assertNotIn("threejs-product-storytelling", core)
        self.assertNotIn("creative-tool-scout", core)

    def test_design_studio_mcp_stack_includes_figma_and_browser_verification(self):
        stack = recommend_stack("design_studio")
        ids = [server["id"] for server in stack["servers"]]
        self.assertEqual(
            ["figma", "context7", "playwright", "chrome-devtools"], ids
        )

    def test_figma_uses_official_remote_oauth_shape(self):
        figma = get_server("figma")
        self.assertEqual("official_vendor", figma["trust"])
        self.assertEqual("https://mcp.figma.com/mcp", figma["mcp_json_remote"]["url"])
        self.assertFalse(figma["requires_secret"])
        self.assertNotIn("secret_env", figma)
        self.assertIn("OAuth", " ".join(figma.get("safety_notes", [])))


if __name__ == "__main__":
    unittest.main()
