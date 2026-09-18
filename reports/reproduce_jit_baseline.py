import sys,json,tempfile,argparse
from pathlib import Path
parser=argparse.ArgumentParser(description='Read-only JIT probes against a supplied repository checkout')
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args=parser.parse_args()
root=args.repo.resolve(); args.output.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(root))
from router.worker_context import WorkerTaskSpec,build_and_validate,render_worker_prompt,discover_project_instructions,resolve_skills_projected
from router.skill_loader import load_skill_bodies
from router.loop_runtime import new_loop,record_attempt,loop_receipt,validate_loop_receipt
from router.skills_cli import list_packs,pack_candidates
r={}
with tempfile.TemporaryDirectory() as d:
 p=Path(d); (p/'AGENTS.md').write_text('Root rule')
 skill='debugging-and-error-recovery'
 w=build_and_validate(WorkerTaskSpec(objective='Investigate a regression',skills=[skill]),project_root=p)
 body=load_skill_bodies([skill],project_root=p)[0]['content']
 r['worker_selected_body_present']=body in render_worker_prompt(w)
 r['worker_claims_active_by_name_only']='## Active skills for this task' in render_worker_prompt(w) and not r['worker_selected_body_present']
 (p/'packages/web').mkdir(parents=True);(p/'packages/AGENTS.md').write_text('Do not publish or use the production database')
 r['intermediate_instructions_preserved']='packages/AGENTS.md' in [i.path for i in discover_project_instructions(p,work_subdir='packages/web')]
 symlink=p/'link';symlink.symlink_to(p,target_is_directory=True)
 try:load_skill_bodies([skill],project_root=symlink);r['loader_rejects_symlink_project']=False
 except Exception:r['loader_rejects_symlink_project']=True
 private=p/'.agentit/profile-skills'/skill;private.mkdir(parents=True);(private/'SKILL.md').write_text('Stale or modified private instructions')
 try:r['untracked_private_cache_overrides_harness']=load_skill_bodies([skill],project_root=p)[0]['source']=='project-agentit-profile'
 except Exception as exc:r['untracked_private_cache_overrides_harness']=False;r['cache_rejection']=str(exc)
 r['manifest_auto_projects']=resolve_skills_projected(task_skills=[],manifest_skills=['unselected-a','unselected-b'],include_manifest_skills=True)
 loop=new_loop(goal='Fix runtime',verifier='execute tests',stop_condition='fresh tests pass',max_attempts=2)
 receipt=loop_receipt(record_attempt(loop,passed=True,strategy='assert',evidence='I think tests pass'))
 validate_loop_receipt(receipt)
 r['self_report_without_command_accepted_as_pass']=receipt['status']=='passed'
 r['receipt_has_provenance']='evidence_source' in receipt
# All scratch mutations above occur in a temporary fixture, never the supplied checkout.
import yaml,hashlib,re
profiles=yaml.safe_load((root/'profiles.yaml').read_text())
packs=list_packs();cands=pack_candidates([p['id'] for p in packs]);covered={p['id'] for p in cands}
inv=[]
for p in sorted((root/'skills').glob('*/SKILL.md')):
 text=p.read_text();parts=text.split('---',2);name=p.parent.name;errs=[]
 try:meta=yaml.safe_load(parts[1]) if text.startswith('---\n') else {}
 except yaml.YAMLError:
  meta={};errs.append('invalid-yaml-frontmatter')
 if meta.get('name')!=name:errs.append('frontmatter-name-mismatch:'+str(meta.get('name')))
 desc=meta.get('description','')
 if not isinstance(desc,str) or not 1<=len(desc)<=1024:errs.append('invalid-description')
 if name not in profiles['profiles']['all']['skills']:errs.append('not-in-all-profile')
 if name not in covered and name not in profiles['profiles']['core']['skills']:errs.append('not-in-pack-discovery')
 if len(text.splitlines())>500:errs.append('body-over-500-lines')
 if len(text.encode())>20000:errs.append('large-body-over-20k-bytes')
 refs=re.findall(r'\[[^\]]+\]\(([^)]+)\)',text)
 broken=[x for x in refs if not (':' in x or x.startswith('#') or '{' in x or '<' in x or ' ' in x) and not (p.parent/x.split('#')[0]).exists()]
 inv.append({'id':name,'name':meta.get('name'),'sha256':hashlib.sha256(text.encode()).hexdigest(),'bytes':len(text.encode()),'lines':len(text.splitlines()),'description':desc,'issues':errs,'broken_markdown_links':broken,'headings':[s for s in text.splitlines() if s.startswith('## ')]})
r['skill_count']=len(inv);r['total_skill_bytes']=sum(x['bytes'] for x in inv);r['core_body_bytes']=sum(x['bytes'] for x in inv if x['id'] in profiles['profiles']['core']['skills'])
(args.output/'probes.json').write_text(json.dumps(r,indent=2))
(args.output/'skills-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False))
print(json.dumps(r,indent=2))
for x in inv:print(x['id'],x['bytes'],','.join(x['issues']),x['broken_markdown_links'])
