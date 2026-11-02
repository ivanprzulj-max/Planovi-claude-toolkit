"""Izrađuje docs/UPUTE_ZA_KORISTENJE.docx iz .md izvornika (treba pandoc i python-docx).
Pokretanje iz korijena repozitorija:  python skripte/izradi_upute_docx.py"""
import pathlib, subprocess
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
repo = pathlib.Path(__file__).resolve().parent.parent
md, out = repo/"docs/UPUTE_ZA_KORISTENJE.md", repo/"docs/UPUTE_ZA_KORISTENJE.docx"
subprocess.run(["pandoc", str(md), "-o", str(out), "--toc", "--toc-depth=2"], check=True)
d = Document(str(out))
def setfont(st, f):
    st.font.name = f
    rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(a), f)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
for st in d.styles:
    if st.type == 1: setfont(st, "Consolas" if st.name == "Source Code" else "Calibri")
    elif st.type == 2 and st.name == "Verbatim Char": setfont(st, "Consolas")
d.styles["Normal"].font.size = Pt(10.5)
for st in d.styles:
    if st.name in ("Heading 1", "Title", "TOC Heading"): st.font.color.rgb = RGBColor.from_string("1F4E79")
    if st.name == "Heading 2": st.font.color.rgb = RGBColor.from_string("2E75B6")
for t in d.tables:
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{e}")
        for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:color", "A6A6A6")): el.set(qn(k), v)
        b.append(el)
    t._tbl.tblPr.append(b)
    for cell in t.rows[0].cells:
        sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), "DEEAF6")
        cell._tc.get_or_add_tcPr().append(sh)
d.save(str(out)); print(out.relative_to(repo))
