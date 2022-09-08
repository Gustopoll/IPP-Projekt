# IPP-Interpret
### Vypracoval: Dominik Švač
### Rok: 2019

## Spustenie

### parse.php
Načíta zo štandardného vstupu kód vo formáte IPPcode19
Na výstupe je XML reprezentácia daného kódu

Príklad spustenia
```
php ./parse.php < <file>
php ./parse.php --help
```

### interpret.py
Načíta XML súbor, ktorý bol vygenerovaný scriptom parse.php a tento program z využitím štandardného vstupu interpretuje

```
python3 ./interpret.py --source=<file1> --input=<file2>

--source=<file1> -> subor vo formáte XML
-input=<file2> -> subor vstupov
```

aspoň jeden z agrugmentov source/input musí byť vložený, ak sa nenastaví jeden, druhý sa vyberá zo štandardného vstupu

### test.php
Testuje predáchádzajúce 2 scripty
dajú sa zvoliť nasledujúce argumety:
- --help - nápoveda
- --directory=path - testy hľadá v zadaném adresáři (ak chýba tento parametr, tak skript prechádza aktuálny adresár)
- --recursive - testy hladá aj rekurzivne vo všetkých jeho podadresároch
- --parse-script=file - súbor zo skriptom v PHP pre analýzu zdrojového kódu v IPPcode19 (ak chýba tento parameter, tak implicitnou hodnotou je parse.php uložený v aktuálnom adresáry)
- --int-script=file - súbor zo skriptom v Python 3.6 pre interpret XML kód v IPPcode19 (ak chýba tento parameter, tak implicitnou hodnotou je interpret.py uložený v aktuálnom adresáry)
- --parse-only - testovaný iba skript pre analýzu zdrojového kódu v IPPcode19
- --int-only - testovaný iba skript pre interpret XML kód v IPPcode19

Príklady testy sú uložené v zložke ./tests a rozdelené do 3 adresárov
- both - testujú sa oba scripty
- int-only - testuje sa iba interpret
- parse-only- testuje sa iba parser

Výsledkom testov je html stránka 




