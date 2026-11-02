# -*- coding: utf-8 -*-
"""Pomoćne funkcije za izradu studija u REGEA predlošku (python-docx).

Upotreba:
    from studija_helpers import *
    doc = kopiraj_i_otvori_predlozak("moja_studija.docx")
    ...
    doc.save("moja_studija.docx")

Sva polja (STYLEREF, SEQ, TOC) prikazuju vrijednosti tek nakon
Update Fields u Wordu (Ctrl+A -> F9) — to napomeni korisniku.
"""
import os
import re
import shutil
import copy

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PREDLOZAK = os.path.join(os.path.dirname(__file__), "..", "assets", "Studija_predlozak.docx")

NBSP = "\u00A0"

# ---------------------------------------------------------------- predložak

def kopiraj_predlozak(odrediste):
    """Kopira predložak na odredište. UVIJEK početi ovako — stilovi i
    numeracija naslova postoje samo u predlošku."""
    shutil.copy(PREDLOZAK, odrediste)
    return odrediste


def kopiraj_i_otvori_predlozak(odrediste):
    kopiraj_predlozak(odrediste)
    return Document(odrediste)

# ---------------------------------------------------------------- brojevi

def hr_broj(x, decimale=None):
    """1586278.85 -> '1 586 278,85' (neprelomivi razmaci za tisućice).

    decimale=None: cijeli brojevi bez decimala, ostali s onoliko koliko imaju
    (max 2). decimale=n: fiksno n decimala."""
    if decimale is None:
        if float(x) == int(float(x)):
            s = f"{int(float(x)):,}"
            return s.replace(",", NBSP)
        decimale = 2
    s = f"{float(x):,.{decimale}f}"          # 1,586,278.85
    s = s.replace(",", "§").replace(".", ",").replace("§", NBSP)
    return s


RX_TOCKA_TISUCICE = re.compile(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b")

def popravi_brojeve_u_tekstu(tekst):
    """Zamjenjuje točku-tisućice razmakom: '1.586.278,85' -> '1 586 278,85'."""
    def _fix(m):
        return m.group(0).replace(".", NBSP)
    return RX_TOCKA_TISUCICE.sub(_fix, tekst)

# ---------------------------------------------------------------- polja (fields)

def _fld_char(tip):
    el = OxmlElement("w:fldChar")
    el.set(qn("w:fldCharType"), tip)
    return el


def _instr_text(instr):
    el = OxmlElement("w:instrText")
    el.set(qn("xml:space"), "preserve")
    el.text = instr
    return el


def _dodaj_polje(paragraph, instr, bold=True):
    """Umeće Word polje { instr } kao runove u odlomak."""
    for el, txt in ((_fld_char("begin"), None), (None, instr),
                    (_fld_char("end"), None)):
        run = paragraph.add_run()
        run.bold = bold
        if el is not None:
            run._r.append(el)
        else:
            run._r.append(_instr_text(txt))

# ---------------------------------------------------------------- captioni

def _dodaj_caption(paragraph_container, vrsta, naziv, doc):
    """vrsta: 'Slika' ili 'Tablica'. Vraća novi odlomak stila Caption:
    'Slika { STYLEREF 1 \\s }.{ SEQ Slika \\* ARABIC \\s 1 } Naziv' """
    p = doc.add_paragraph(style="Caption") if paragraph_container is None else paragraph_container
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(f"{vrsta} ")
    r.bold = True
    _dodaj_polje(p, r" STYLEREF 1 \s ", bold=True)
    r = p.add_run(".")
    r.bold = True
    _dodaj_polje(p, rf" SEQ {vrsta} \* ARABIC \s 1 ", bold=True)
    r = p.add_run(f" {naziv}")
    r.bold = False
    return p


def dodaj_caption_slike(doc, naziv):
    """Poziva se NAKON umetanja slike — caption ide ISPOD slike."""
    return _dodaj_caption(None, "Slika", naziv, doc)


def dodaj_caption_tablice(doc, naziv):
    """Poziva se PRIJE umetanja tablice — caption ide IZNAD tablice."""
    return _dodaj_caption(None, "Tablica", naziv, doc)


def dodaj_izvor(doc, tekst="Izvor: "):
    """Odlomak stila Small (Calibri 10) — ide ispod tablice/slike."""
    p = doc.add_paragraph(tekst, style="Small")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

# ---------------------------------------------------------------- tablice

RX_HR_BROJ = re.compile(r"^[\d\s\u00A0.,%€$]*\d[\d\s\u00A0.,%€$]*$")

def _je_broj(tekst):
    t = tekst.strip()
    return bool(t) and bool(RX_HR_BROJ.match(t))


def formatiraj_tablicu(table, font_pt=10, header_bold=True):
    """Calibri font_pt; brojevi centrirano, tekst lijevo; 1. red bold+centar."""
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            for p in cell.paragraphs:
                if i == 0 and header_bold:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = (WD_ALIGN_PARAGRAPH.CENTER
                                   if _je_broj(p.text) else WD_ALIGN_PARAGRAPH.LEFT)
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(font_pt)
                    if i == 0 and header_bold:
                        run.bold = True
    _ponovi_zaglavlje(table)


def _ponovi_zaglavlje(table):
    """Označi 1. red kao header koji se ponavlja na svakoj stranici."""
    tr = table.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    if trPr.find(qn("w:tblHeader")) is None:
        el = OxmlElement("w:tblHeader")
        el.set(qn("w:val"), "true")
        trPr.append(el)

# ---------------------------------------------------------------- naslovi / sekcije

def h1_na_neparnoj(doc):
    """Umeće section break tipa Odd Page prije svakog Heading 1 (osim prvog
    odlomka dokumenta) tako da svaki glavni naslov počinje na neparnoj str."""
    body_pars = doc.paragraphs
    for p in body_pars:
        if p.style.name == "Heading 1" and p.text.strip():
            prev = p._p.getprevious()
            # preskoči ako je već prethodni element sectPr paragraf
            if prev is not None and prev.find(qn("w:pPr")) is not None \
               and prev.find(qn("w:pPr")).find(qn("w:sectPr")) is not None:
                continue
            _umetni_odd_break_prije(p, doc)


def _umetni_odd_break_prije(paragraph, doc):
    """Umeće prazan odlomak sa sectPr (oddPage) neposredno prije danog odlomka.
    Kopira postavke stranice iz zadnjeg sectPr dokumenta."""
    zadnji_sectpr = doc.element.body.find(qn("w:sectPr"))
    novi_p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    sectPr = copy.deepcopy(zadnji_sectpr) if zadnji_sectpr is not None else OxmlElement("w:sectPr")
    # postavi tip oddPage
    t = sectPr.find(qn("w:type"))
    if t is None:
        t = OxmlElement("w:type")
        sectPr.insert(0, t)
    t.set(qn("w:val"), "oddPage")
    pPr.append(sectPr)
    novi_p.append(pPr)
    paragraph._p.addprevious(novi_p)

# ---------------------------------------------------------------- navodnici

RX_NAVODNICI = re.compile(r"[„“”\"»«]([^„“”\"»«]{1,120}?)[„“”\"»«]")

def italic_umjesto_navodnika(paragraph):
    """Zamjenjuje „tekst" / "tekst" kurzivom bez navodnika.
    Radi na razini cijelog odlomka (spaja runove) — koristiti na odlomcima
    bez posebnog formatiranja unutar teksta."""
    puni = paragraph.text
    if not RX_NAVODNICI.search(puni):
        return False
    dijelovi = RX_NAVODNICI.split(puni)
    for r in list(paragraph.runs):
        r._r.getparent().remove(r._r)
    # split vraća: [prije, citat, poslije, citat, ...] — neparni indeksi su citati
    for i, dio in enumerate(dijelovi):
        if not dio:
            continue
        run = paragraph.add_run(dio)
        run.italic = (i % 2 == 1)
    return True

# ---------------------------------------------------------------- popisi

def dodaj_popis(doc, vrsta):
    """Umeće TOC polje za Popis tablica/slika: vrsta='Tablica' ili 'Slika'."""
    naslov = "Popis tablica" if vrsta == "Tablica" else "Popis slika"
    p = doc.add_paragraph(naslov)
    for run in p.runs:
        run.bold = True
        run.font.size = Pt(14)
    p2 = doc.add_paragraph()
    _dodaj_polje(p2, rf' TOC \h \z \c "{vrsta}" ', bold=False)
    return p2
