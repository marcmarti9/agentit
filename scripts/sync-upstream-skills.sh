#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

clone_repo() {
  local slug="$1"
  local dest="$2"
  git clone --quiet --depth 1 "https://github.com/${slug}.git" "$dest"
}

copy_package() {
  local src="$1"
  local dest="$2"
  test -f "$src/SKILL.md" || {
    echo "missing expected upstream skill: $src/SKILL.md" >&2
    exit 1
  }
  rm -rf "$dest"
  mkdir -p "$dest"
  cp -a "$src/." "$dest/"
}

# Canonical sources. Keep Agentit-specific routing/composition outside these packages.
clone_repo addyosmani/agent-skills "$TMP/addy"
clone_repo Leonxlnx/taste-skill "$TMP/taste"
clone_repo pbakaus/impeccable "$TMP/impeccable"
clone_repo emilkowalski/skills "$TMP/emil"
clone_repo greensock/gsap-skills "$TMP/gsap"
clone_repo supabase/agent-skills "$TMP/supabase"
clone_repo Nutlope/hallmark "$TMP/hallmark"
clone_repo nextlevelbuilder/ui-ux-pro-max-skill "$TMP/uiux"
clone_repo Appllama/appllama-skills "$TMP/appllama"
clone_repo blader/humanizer "$TMP/humanizer"
clone_repo hardikpandya/stop-slop "$TMP/stopslop"
clone_repo cathrynlavery/diagram-design "$TMP/diagram"
clone_repo vercel-labs/skills "$TMP/vercel-skills"
clone_repo obra/superpowers "$TMP/superpowers"

ADDY_SKILLS=(
  api-and-interface-design
  browser-testing-with-devtools
  ci-cd-and-automation
  code-review-and-quality
  code-simplification
  context-engineering
  debugging-and-error-recovery
  deprecation-and-migration
  documentation-and-adrs
  doubt-driven-development
  frontend-ui-engineering
  git-workflow-and-versioning
  idea-refine
  incremental-implementation
  interview-me
  observability-and-instrumentation
  performance-optimization
  planning-and-task-breakdown
  security-and-hardening
  shipping-and-launch
  source-driven-development
  spec-driven-development
  test-driven-development
  using-agent-skills
)

for skill in "${ADDY_SKILLS[@]}"; do
  copy_package "$TMP/addy/skills/$skill" "$ROOT/skills/$skill"
done

copy_package "$TMP/taste/skills/taste-skill" "$ROOT/skills/design-taste-frontend"
copy_package "$TMP/impeccable/.agents/skills/impeccable" "$ROOT/skills/impeccable"
copy_package "$TMP/emil/skills/emil-design-eng" "$ROOT/skills/emil-design-eng"
copy_package "$TMP/gsap/skills/gsap-performance" "$ROOT/skills/gsap-performance"
copy_package "$TMP/gsap/skills/gsap-scrolltrigger" "$ROOT/skills/gsap-scrolltrigger"
copy_package "$TMP/supabase/skills/supabase-postgres-best-practices" "$ROOT/skills/supabase-postgres-best-practices"
copy_package "$TMP/hallmark/skills/hallmark" "$ROOT/skills/hallmark"
copy_package "$TMP/uiux/.claude/skills/ui-ux-pro-max" "$ROOT/skills/ui-ux-pro-max"
copy_package "$TMP/appllama/skills/appllama-app-design-skill" "$ROOT/skills/appllama-app-design-skill"
copy_package "$TMP/appllama/skills/appllama-usage" "$ROOT/skills/appllama-usage"

# Humanizer and Stop Slop are repo-root skill packages rather than skills/<id>.
rm -rf "$ROOT/skills/humanizer" "$ROOT/skills/stop-slop"
mkdir -p "$ROOT/skills/humanizer" "$ROOT/skills/stop-slop"
cp "$TMP/humanizer/SKILL.md" "$ROOT/skills/humanizer/SKILL.md"
for child in agents scripts; do
  if [ -e "$TMP/humanizer/$child" ]; then
    cp -a "$TMP/humanizer/$child" "$ROOT/skills/humanizer/$child"
  fi
done
cp "$TMP/stopslop/SKILL.md" "$ROOT/skills/stop-slop/SKILL.md"
if [ -d "$TMP/stopslop/references" ]; then
  cp -a "$TMP/stopslop/references" "$ROOT/skills/stop-slop/references"
fi

copy_package "$TMP/diagram/skills/diagram-design" "$ROOT/skills/diagram-design"
copy_package "$TMP/vercel-skills/skills/find-skills" "$ROOT/skills/find-skills"
copy_package "$TMP/superpowers/skills/verification-before-completion" "$ROOT/skills/verification-before-completion"

# Retire local compact/adaptor IDs where a canonical package now replaces them.
rm -rf \
  "$ROOT/skills/anti-ai-slop-design" \
  "$ROOT/skills/anti-ai-slop-writing" \
  "$ROOT/skills/ui-ux-pro-max-intelligence" \
  "$ROOT/skills/mobile-native-app-design" \
  "$ROOT/skills/diagram-and-architecture-visuals"

# Addy's skills intentionally use ../../references/<file>.md for shared checklists.
# Preserve those upstream files at Agentit's repository root without overwriting
# Agentit-owned reference files. A manifest makes later refreshes remove stale
# upstream-managed files safely.
ADDY_REF_MANIFEST="$ROOT/references/.addy-agent-skills-files"
if [ -f "$ADDY_REF_MANIFEST" ]; then
  while IFS= read -r rel; do
    [ -n "$rel" ] || continue
    rm -f "$ROOT/references/$rel"
  done < "$ADDY_REF_MANIFEST"
fi
mkdir -p "$ROOT/references"
: > "$ADDY_REF_MANIFEST"
if [ -d "$TMP/addy/references" ]; then
  while IFS= read -r -d '' file; do
    rel="${file#"$TMP/addy/references/"}"
    dest="$ROOT/references/$rel"
    if [ -e "$dest" ]; then
      echo "refusing to overwrite Agentit-owned shared reference: $dest" >&2
      exit 1
    fi
    mkdir -p "$(dirname "$dest")"
    cp -a "$file" "$dest"
    printf '%s\n' "$rel" >> "$ADDY_REF_MANIFEST"
  done < <(find "$TMP/addy/references" -type f -print0 | sort -z)
fi

# Persist exact source commits and mappings. This is generated, not hand-edited.
python3 - "$ROOT" "$TMP" <<'PY'
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
tmp = Path(sys.argv[2])

repos = {
    "addyosmani/agent-skills": tmp / "addy",
    "Leonxlnx/taste-skill": tmp / "taste",
    "pbakaus/impeccable": tmp / "impeccable",
    "emilkowalski/skills": tmp / "emil",
    "greensock/gsap-skills": tmp / "gsap",
    "supabase/agent-skills": tmp / "supabase",
    "Nutlope/hallmark": tmp / "hallmark",
    "nextlevelbuilder/ui-ux-pro-max-skill": tmp / "uiux",
    "Appllama/appllama-skills": tmp / "appllama",
    "blader/humanizer": tmp / "humanizer",
    "hardikpandya/stop-slop": tmp / "stopslop",
    "cathrynlavery/diagram-design": tmp / "diagram",
    "vercel-labs/skills": tmp / "vercel-skills",
    "obra/superpowers": tmp / "superpowers",
}
heads = {
    slug: subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    for slug, path in repos.items()
}

addy = [
    "api-and-interface-design", "browser-testing-with-devtools", "ci-cd-and-automation",
    "code-review-and-quality", "code-simplification", "context-engineering",
    "debugging-and-error-recovery", "deprecation-and-migration", "documentation-and-adrs",
    "doubt-driven-development", "frontend-ui-engineering", "git-workflow-and-versioning",
    "idea-refine", "incremental-implementation", "interview-me",
    "observability-and-instrumentation", "performance-optimization", "planning-and-task-breakdown",
    "security-and-hardening", "shipping-and-launch", "source-driven-development",
    "spec-driven-development", "test-driven-development", "using-agent-skills",
]

mappings = [
    *[
        {"skill": skill, "repo": "addyosmani/agent-skills", "path": f"skills/{skill}"}
        for skill in addy
    ],
    {"skill": "design-taste-frontend", "repo": "Leonxlnx/taste-skill", "path": "skills/taste-skill"},
    {"skill": "impeccable", "repo": "pbakaus/impeccable", "path": ".agents/skills/impeccable"},
    {"skill": "emil-design-eng", "repo": "emilkowalski/skills", "path": "skills/emil-design-eng"},
    {"skill": "gsap-performance", "repo": "greensock/gsap-skills", "path": "skills/gsap-performance"},
    {"skill": "gsap-scrolltrigger", "repo": "greensock/gsap-skills", "path": "skills/gsap-scrolltrigger"},
    {"skill": "supabase-postgres-best-practices", "repo": "supabase/agent-skills", "path": "skills/supabase-postgres-best-practices"},
    {"skill": "hallmark", "repo": "Nutlope/hallmark", "path": "skills/hallmark", "replaces": ["anti-ai-slop-design"]},
    {"skill": "ui-ux-pro-max", "repo": "nextlevelbuilder/ui-ux-pro-max-skill", "path": ".claude/skills/ui-ux-pro-max", "replaces": ["ui-ux-pro-max-intelligence"]},
    {"skill": "appllama-app-design-skill", "repo": "Appllama/appllama-skills", "path": "skills/appllama-app-design-skill", "replaces": ["mobile-native-app-design"]},
    {"skill": "appllama-usage", "repo": "Appllama/appllama-skills", "path": "skills/appllama-usage"},
    {"skill": "humanizer", "repo": "blader/humanizer", "path": ".", "replaces": ["anti-ai-slop-writing"]},
    {"skill": "stop-slop", "repo": "hardikpandya/stop-slop", "path": "."},
    {"skill": "diagram-design", "repo": "cathrynlavery/diagram-design", "path": "skills/diagram-design", "replaces": ["diagram-and-architecture-visuals"]},
    {"skill": "find-skills", "repo": "vercel-labs/skills", "path": "skills/find-skills"},
    {"skill": "verification-before-completion", "repo": "obra/superpowers", "path": "skills/verification-before-completion"},
]
for item in mappings:
    item["snapshot"] = heads[item["repo"]]

lock = {
    "schema_version": 1,
    "generated_by": "scripts/sync-upstream-skills.sh",
    "mappings": sorted(mappings, key=lambda x: x["skill"]),
    "shared": [
        {
            "repo": "addyosmani/agent-skills",
            "path": "references",
            "destination": "references",
            "snapshot": heads["addyosmani/agent-skills"],
            "manifest": "references/.addy-agent-skills-files",
        }
    ],
}
(root / "skills" / "UPSTREAM_LOCK.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

canonical_ids = {m["skill"] for m in mappings}
repo_skill_ids = sorted(
    p.parent.name for p in (root / "skills").glob("*/SKILL.md") if p.is_file()
)
owned = [skill for skill in repo_skill_ids if skill not in canonical_ids]

lines = [
    "# Skill provenance registry",
    "",
    "Canonical packages below are copied from their upstream repositories without compressing or rewriting `SKILL.md`. Agentit-specific routing, composition, policy, and runtime behavior live outside vendored packages.",
    "",
    "## Canonical vendored skills",
    "",
    "| Agentit skill | Upstream | Upstream path | Snapshot |",
    "| --- | --- | --- | --- |",
]
for item in sorted(mappings, key=lambda x: x["skill"]):
    lines.append(f"| `{item['skill']}` | `{item['repo']}` | `{item['path']}` | `{item['snapshot']}` |")
lines += [
    "",
    "## Agentit-owned skills",
    "",
    "These have no single canonical upstream skill package to sync 1:1. They remain Agentit-owned because they implement Agentit runtime/orchestration or compose multiple sources. Source-backed composites are documented in `THIRD_PARTY_NOTICES.md`.",
    "",
]
lines.extend(f"- `{skill}`" for skill in owned)
lines += [
    "",
    "## Refresh",
    "",
    "```bash",
    "./scripts/sync-upstream-skills.sh",
    "```",
    "",
    "The exact machine-readable mapping and snapshots live in `skills/UPSTREAM_LOCK.json`.",
]
(root / "skills" / "UPSTREAM_SOURCES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Canonical upstream snapshots:")
for slug, sha in sorted(heads.items()):
    print(f"  {slug:<42} {sha}")
print(f"Canonical skill packages: {len(mappings)}")
print(f"Agentit-owned skill packages: {len(owned)}")
PY
