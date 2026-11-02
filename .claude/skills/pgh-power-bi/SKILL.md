---
name: pgh-power-bi
description: Izrada i održavanje Power BI izvještaja (projekt .pbip — semantički model u TMDL-u + izvješće u JSON-u) za Plan grijanja i hlađenja, s podacima koji se Power Queryjem vuku izravno iz Master tablice grada. Koristi kad korisnik traži "Power BI", "PBI", "dashboard u Power BI-ju", "izvještaj iz Master tablice", "vizualizacija plana", "prilagodi Power BI za [grad]", ili kad se Power BI izvještaj ne otvara / javlja grešku. Predložak je Power BI projekt Plana G&H Karlovac (mapa power-bi/karlovac u repozitoriju).
---

# Power BI izvještaj Plana G&H (format .pbip)

Predložak: `power-bi/karlovac/` u ovom repozitoriju (izvornik na SharePointu:
`2_Planovi/1_Karlovac/4_Power_BI/`). Izrađen 11. 8. 2026. nad `MasterSheet_Karlovac.xlsx`;
upute izvornika su u `power-bi/karlovac/UPUTE.txt` — pročitaj ih prije rada.

## Zašto .pbip, a ne .pbix
`.pbip` je tekstualni format (TMDL za model, JSON za izvješće): može se pregledavati, mijenjati i
verzionirati u Gitu, a Claude ga može generirati i ispravljati. `.pbix` je binaran — iz Power BI
Desktopa se po želji sprema *File → Save As → .pbix* za distribuciju.

## Struktura projekta
```
Plan_GH_<Grad>.pbip                      # ulazna datoteka — otvara se u Power BI Desktopu
Plan_GH_<Grad>.SemanticModel/
  definition/
    model.tmdl, database.tmdl
    expressions.tmdl                     # parametar MasterSheetPath (putanja do Mastera)
    tables/<Tablica>.tmdl                # po jedna tablica: stupci + Power Query (M) particija
  .pbi/                                  # LOKALNA predmemorija — ne ide u Git
Plan_GH_<Grad>.Report/
  definition/report.json, version.json, pages/...   # stranice i vizuali
Test_minimalni.pbip / .Report            # dijagnostika: isti model, jedan vizual
```

## Pravila (iz izrade za Karlovac)
1. **Master je jedini izvor podataka.** Upiti čitaju Master izravno (Power Query → Excel);
   nikakve brojke se ne upisuju ručno u model. Iznimka mora biti zapisana u `UPUTE.txt`
   (na Karlovcu: decentralizirana ulaganja postoje u Masteru samo kao tekstna bilješka pa su
   unesena kao fiksne vrijednosti — to je dug koji treba zatvoriti, ne obrazac).
2. **Putanja je parametar** `MasterSheetPath` (u `expressions.tmdl`). Svaki korisnik ga mijenja u
   *Transform data → Manage parameters* na svoju OneDrive putanju. Nikad ne ugrađuj osobnu putanju
   u upite.
3. **Pozicijska ovisnost.** Ako upit čita točno određene retke lista, umetanje/brisanje redaka u
   Masteru ruši upit. Kad je moguće, čitaj **imenovane raspone** ili tablice Excela, ili
   pronalazi retke po oznaci u stupcu A, a ne po broju retka. Popis listova o kojima izvješće
   ovisi zapiši u `UPUTE.txt`.
4. **Definicija izvješća mora imati blok `themeCollection`.** Bez njega Power BI Desktop pri
   otvaranju javlja *Došlo je do pogreške prilikom prikaza izvješća* (`Cannot read properties of
   undefined (reading 'customTheme')`). Model pri tome može biti ispravan.
5. **Dijagnostika:** uz glavno izvješće isporuči `Test_minimalni` (isti model, jedna stranica,
   jedan vizual tablice). Otvara se test, a glavno ne → greška je u vizualu; ne otvara se ni test
   → greška je u formatu izvješća ili modelu.
6. **Verifikacija prije isporuke:** svaku KPI karticu i ključnu vrijednost usporedi s Masterom
   (na Karlovcu 48/48 kontrolnih provjera) i broj provjera zapiši u `UPUTE.txt`.
7. Ne zbrajaj nizove koji su replicirani radi grafikona (npr. hlađenje kopirano po scenarijima) —
   to se izrijekom napiše u `UPUTE.txt`.
8. Raspakiravanje/kopiranje uvijek u **novu, praznu mapu** (stari `.pbi/` cache zbunjuje Desktop).
9. Oznake mjera, scenarija i nazivi u izvješću moraju pratiti **aktualnu** verziju Plana i
   Mastera (npr. preimenovanje scenarija ili mjera povlači izmjenu izvješća).

## Postupak za novi grad
1. Kopiraj `power-bi/karlovac/` u novu mapu i preimenuj `Plan_GH_Karlovac.*` u `Plan_GH_<Grad>.*`
   (i reference u `.pbip` i `definition.pbir`).
2. Usporedi strukturu Mastera novog grada s Karlovčevim (nazivi listova, raspored redaka) — za svaki
   upis u `tables/*.tmdl` provjeri da list i raspon postoje. Razlike riješi u M-upitima.
3. Postavi zadanu vrijednost `MasterSheetPath`.
4. Prilagodi tekstove stranica (naziv grada, scenariji, mjere). **Ne prenosi brojke Karlovca** —
   KPI kartice moraju čitati Master novog grada.
5. Otvori u Power BI Desktopu (verzija 2024.+), *Refresh*, provjeri svaku stranicu.
6. Napravi kontrolne provjere prema Masteru (pravilo 6) i ažuriraj `UPUTE.txt`.

## Ograničenja
- Claude ne može pokrenuti Power BI Desktop: može generirati i provjeriti datoteke (JSON
  valjanost, reference na listove Mastera), ali otvaranje i *Refresh* radi korisnik.
- Format PBIP/PBIR Microsoft razvija; ako Desktop javi grešku sheme, provjeri aktualnu
  dokumentaciju Microsofta (*Power BI Desktop projects*) — ne nagađaj nazive svojstava.
