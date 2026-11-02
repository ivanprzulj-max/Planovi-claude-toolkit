"""Pakira svaki skill u zasebnu .zip datoteku (dist/) za upload u claude.ai / Claude Desktop (Cowork).
Pokretanje iz korijena repozitorija:  python skripte/zapakiraj_skillove.py
Svaki zip sadrži mapu skilla (npr. hc-plan-creator/SKILL.md ...)."""
import pathlib, zipfile
repo = pathlib.Path(__file__).resolve().parent.parent
dist = repo / "dist"; dist.mkdir(exist_ok=True)
for base in [repo / ".claude" / "skills", repo / "skills-opcionalno"]:
    for skill in sorted(p for p in base.iterdir() if p.is_dir()):
        out = dist / f"{skill.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in skill.rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts:
                    z.write(f, f.relative_to(skill.parent))
        print(f"{out.relative_to(repo)}")
