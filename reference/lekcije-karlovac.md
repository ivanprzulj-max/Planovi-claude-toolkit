# Lekcije iz izrade Plana G&H Karlovac

Sažetak pravila koja su nastala iz stvarnih nalaza kontrole (pet prolaza K3) i revizija kanona
(kolovoz–listopad 2026.). Izvori: `1_Karlovac/5_Plan_G&H/Radno/VERZIJA.md` i
`1_Karlovac/8_Radno/nalaz-kontrole-*.md` na SharePointu.

## Master tablica
1. **`openpyxl` nikad za spremanje Mastera.** Pri spremanju bez upozorenja briše grafikone,
   crteže, slike, pivot tablice i VML. Čitanje da (`read_only=True`), pisanje ne.
2. Upis: **Excel COM (pywin32)** u jednoj sesiji, `CalculateFullRebuild()` prije jedinog
   spremanja — ili izravna XML tehnika nad `.xlsx` arhivom. Prije i poslije: brojanje dijelova
   arhive (grafikoni moraju ostati isti) i 0 ćelija s `#NAME?/#VALUE!/#REF!`.
3. **Jedna oznaka verzije po seriji upisa** (`MS_<grad>_<datum>_v<n>`). Oznaka u Planu mora
   odgovarati stanju Mastera.
4. Sinkronizacija OneDrive/SharePoint mijenja bajtove bez promjene sadržaja — MD5 nije dokaz.
5. Dvojnici (`_fresh`, `_patch`, `_to_delete`, stare kopije) se ne otvaraju i ne citiraju.

## Plan (.docx)
6. **Radni dokument ≠ primjerak za isporuku.** Radni nosi praćene izmjene i komentare (trag);
   primjerak za isporuku je izvod (sve prihvaćeno, svi komentari obrisani) i ne uređuje se izravno.
7. Prije slanja provjeri **brojanjem** u XML-u: 0 komentara, 0 `w:ins`/`w:del`. Povučeni tekst u
   praćenim izmjenama otkriva povučene brojke.
8. **Najčešći razred greške: odlomak bez ijedne praćene izmjene** koji između dva ispravljena
   zadržava povučenu vrijednost. Nakon svake promjene pretraži cijeli dokument (proza, tablice,
   kartice mjera, registar pretpostavki, sažetak, zaključak, prilozi).
9. Ne miješaj **LCOH tehnologije** (referentni uvjeti) i **LCOH mjere** (kartica mjere);
   referentne vrijednosti uvijek s troškom CO₂.
10. Natpisi: jedno polje `STYLEREF` po natpisu (dvostruko daje *Slika 44.6* i ne popravlja se F9).
11. Ista zamjena primijenjena dvaput razara rečenicu — provjeri postoji li već umetnuti run.
12. Komentari ne smiju sadržavati interne putanje, nazive agenata ni opise pogrešaka ako dokument
    izlazi iz REGEA-e.

## GIS
13. Rasterski kartogrami prostornih planova su podloga za prikaz, ne analitički sloj.
14. Nepostojanje sloja je nalaz — zatražiti točno imenovani list plana u GeoPackageu, EPSG:3765.

## Proces
15. Kapije K1–K3 i odobrenje korisnika prije svakog upisa u Master — bez iznimke.
16. EN verzija, sažeta verzija i prezentacija usklađuju se **nakon svake** revizije glavnog plana.
