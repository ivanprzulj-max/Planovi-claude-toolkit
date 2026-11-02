# -*- coding: utf-8 -*-
"""Provjera usklađenosti studije s REGEA pravilima formatiranja.

Upotreba:  python provjeri_studiju.py studija.docx

Ispisuje KRITIČNO / UPOZORENJE nalaze s lokacijom (redni broj odlomka i
isječak teksta). Izlazni kod 1 ako ima kritičnih nalaza.
"""
import re
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

DOZVOLJENI_STILOVI = {
    "Normal", "Heading 1", "Heading 2", "Heading 3", "Heading 4",
    "Caption", "Small", "List Paragraph", "Naslov studije", "TOC Heading",
    "toc 1", "toc 2", "toc 3", "No Spacing", "header", "footer",
}

RX_TOCKA_TISUCICE = re.compile(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b")
RX_NAVODNICI = re.compile(r"[„“”»«]|(?<!\w)\"|\"(?!\w)")
RX_RUCNI_BROJ_NASLOVA = re.compile(r"^\s*\d+(\.\d+)*[.)]?\s+\S")

kriticno, upozorenja = [], []


def K(msg): kriticno.append(msg)
def U(msg): upozorenja.append(msg)


def isjecak(t, n=60):
    t = t.strip().replace("\n", " ")
    return (t[:n] + "…") if len(t) > n else t


def provjeri(path):
    doc = Document(path)

    # --- section break (mora postojati > 1 sekcija, tj. sectPr unutar body-ja)
    if len(doc.sections) < 2:
        K("Nema Section breaka — numeracija stranica ne može početi od Uvoda.")

    ima_sadrzaj = False
    prethodni_element = {"tbl_pending_caption": None}

    body = doc.element.body
    par_idx = 0
    zadnji_caption = None      # (vrsta, par_idx)
    zadnja_slika_idx = None
    glavni_dio = False         # True nakon prvog Heading 1 — tablice naslovnice
                               # (Autori, Voditelj projekta) izuzete su od pravila

    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            par_idx += 1
            from docx.text.paragraph import Paragraph
            p = Paragraph(child, doc)
            txt = p.text
            stil = p.style.name if p.style is not None else "?"

            if "sadržaj" in txt.strip().lower()[:12]:
                ima_sadrzaj = True

            if stil == "Heading 1" and txt.strip():
                glavni_dio = True

            # stilovi
            if txt.strip() and stil not in DOZVOLJENI_STILOVI:
                U(f"[¶{par_idx}] Stil izvan predloška: '{stil}' — {isjecak(txt)}")

            # ručno numerirani naslovi
            if stil.startswith("Heading") and RX_RUCNI_BROJ_NASLOVA.match(txt):
                K(f"[¶{par_idx}] Ručno upisan broj u naslovu (numeracija je automatska): {isjecak(txt)}")

            # navodnici
            if txt.strip() and stil not in ("header", "footer") and RX_NAVODNICI.search(txt):
                K(f"[¶{par_idx}] Navodnici u tekstu — koristiti Italic: {isjecak(txt)}")

            # brojevi s točkom-tisućicama
            if RX_TOCKA_TISUCICE.search(txt):
                K(f"[¶{par_idx}] Broj s točkom za tisućice (treba razmak): {isjecak(txt)}")

            # captioni
            if stil == "Caption" or txt.strip().startswith(("Slika ", "Tablica ")):
                vrsta = "Slika" if txt.strip().startswith("Slika") else \
                        ("Tablica" if txt.strip().startswith("Tablica") else None)
                if vrsta:
                    zadnji_caption = (vrsta, par_idx)
                    # slika mora biti PRIJE captiona 'Slika'
                    if vrsta == "Slika" and zadnja_slika_idx is None:
                        U(f"[¶{par_idx}] Caption slike bez slike iznad — provjeriti poziciju (caption ide ISPOD slike).")
                    zadnja_slika_idx = None

            # sadrži li odlomak sliku
            if child.findall(".//" + qn("w:drawing")):
                zadnja_slika_idx = par_idx
                if zadnji_caption and zadnji_caption[0] == "Slika" and zadnji_caption[1] == par_idx - 1:
                    K(f"[¶{par_idx}] Slika je ISPOD svog captiona — caption slike mora biti ISPOD slike.")

            # font provjere u runovima (izvan tablica)
            for run in p.runs:
                if run.text.strip() and run.font.name not in (None, "Calibri") \
                   and stil != "Naslov studije":
                    U(f"[¶{par_idx}] Font '{run.font.name}' umjesto Calibri: {isjecak(run.text)}")

        elif child.tag == qn("w:tbl"):
            from docx.table import Table
            t = Table(child, doc)
            if not glavni_dio:
                continue   # administrativne tablice naslovnice — izuzete
            # caption tablice mora biti IZNAD (zadnji caption vrste Tablica neposredno prije)
            if not (zadnji_caption and zadnji_caption[0] == "Tablica"):
                U(f"[nakon ¶{par_idx}] Tablica bez captiona iznad (caption tablice ide IZNAD tablice).")
            zadnji_caption = None
            # font i poravnanje u tablici
            for ri, row in enumerate(t.rows):
                for cell in row.cells:
                    for cp in cell.paragraphs:
                        for run in cp.runs:
                            if run.font.size is not None and run.font.size > Pt(10):
                                K(f"[tablica nakon ¶{par_idx}] Font u tablici {run.font.size.pt:.0f} pt > 10 pt: {isjecak(run.text)}")
                                break

    if not ima_sadrzaj:
        U("Nije pronađen 'Sadržaj' — provjeriti strukturu dokumenta.")

    # --- H1 na neparnoj stranici: provjeri postoje li oddPage section breakovi
    odd_breaks = body.findall(".//" + qn("w:sectPr") + "/" + qn("w:type"))
    n_odd = sum(1 for tel in odd_breaks if tel.get(qn("w:val")) == "oddPage")
    n_h1 = sum(1 for p in doc.paragraphs if p.style.name == "Heading 1" and p.text.strip())
    if n_h1 > 1 and n_odd == 0:
        U(f"Dokument ima {n_h1} Heading 1 naslova, ali nijedan Odd Page section break — "
          "provjeriti počinju li glavni naslovi na neparnim stranicama.")

    # --- ispis
    print(f"Provjera: {path}")
    print(f"KRITIČNO: {len(kriticno)}   UPOZORENJA: {len(upozorenja)}\n")
    for m in kriticno:
        print("  [KRITIČNO]", m)
    for m in upozorenja:
        print("  [UPOZORENJE]", m)
    return 1 if kriticno else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(provjeri(sys.argv[1]))
