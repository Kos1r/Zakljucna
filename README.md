# FitRise Slovenija - Fitnes obiskovalni števec
## Opis projekta

FitRise Slovenija je inovativna spletna stran, ki omogoča obiskovalcem fitnes centrov, da preverijo trenutno število obiskovalcev in razpoložljivost opreme v realnem času. Sistem uporablja tehnologijo ESP32 in NFC skenerje za sledenje obiskovalcem, kjer se številka povečuje ob prihodu obiskovalcev in zmanjšuje ob njihovem odhodu. Tako obiskovalci vedno vedo, kdaj je fitnes prost in kdaj je najboljši čas za obisk.

To je prva fitnes stran v Sloveniji, ki ponuja tovrstno funkcionalnost s števcem obiskovalcev, ki omogoča boljše načrtovanje obiskov in povečanje uporabniške izkušnje.
## Problem, ki ga rešujemo

Glavni problem, ki ga rešujemo, je težava pri iskanju primernega časa za obisk fitnesa. Pogosto je težko vedeti, kdaj je fitnes manj zaseden, kar vodi do neoptimalnega planiranja obiskov in dolgotrajnega čakanja na prosto opremo.
### Naša rešitev

FitRise Slovenija omogoča, da uporabniki v realnem času preverijo število obiskovalcev v fitnesu, kar jim pomaga bolje načrtovati obisk. Ko nekdo vstopi v fitnes, se številka poveča, ko pa izstopi, se zmanjša. Ta funkcionalnost omogoča uporabnikom, da se izognejo gneči in uživajo v optimalni izkušnji.

Dodatno, ko se uporabnik včlani v fitnes, prejme svojo unikatno NFC kartico za vstop v fitnes. Ob tem pa prejme na svoj e-mail uporabniško ime in geslo, s katerima se lahko prijavi na našo spletno stran, kjer lahko spremlja svoje obiske, povprečen čas bivanja v fitnesu, število mesečnih obiskov, napredek in druge statistike.
### Naša ciljna skupina

Naša ciljna skupina so fitnes člani v Sloveniji, ki si želijo boljšo uporabniško izkušnjo in večjo prilagodljivost pri načrtovanju svojih obiskov. To so ljudje, ki želijo imeti nadzor nad tem, kdaj je fitnes najbolj prost, in jim ni vseeno, da ne čakajo na prosto opremo.
## Analiza trga
### Velikost trga

Slovenski fitnes trg vključuje več tisoč aktivnih uporabnikov, ki vsakodnevno obiskujejo fitnes centre. Glede na različne fitnes verige, kot so CleverFit, Mega Center, FitInn, BODIFIT in drugi, ocenjujemo, da je v Sloveniji več kot 100.000 rednih uporabnikov fitnes centrov.
### Konkurenčna analiza
Ime fitnesa	Prednosti	Slabosti	Naša razlika
CleverFit	Široka mreža fitnes centrov	Pomanjkanje natančnega vpogleda v zasedenost fitnesa	Števec obiskovalcev v realnem času
Mega Center	Dobro razviti programi in storitve	Pomanjkanje funkcionalnosti za spremljanje zasedenosti	Delo z NFC tehnologijo za spremljanje obiskovalcev
FitInn	Ugodne cene in dostopnost	Ni podatkov o trenutnem številu obiskovalcev	Omogočanje natančnega vpogleda v zasedenost opreme
BODIFIT	Raznolike vadbe in storitve	Omejen vpogled v realno zasedenost	Prva fitnes stran v Sloveniji s števcem obiskovalcev
## USP (Unique Selling Proposition)

Naša stran je prva v Sloveniji z vključeno funkcionalnostjo za spremljanje števila obiskovalcev fitnesa in njihove zasedenosti v realnem času, kar omogoča boljše načrtovanje obiskov in povečuje uporabniško izkušnjo.
## SWOT analiza
### PREDNOSTI (S)

    Funkcionalnost za Slovenijo (števec obiskovalcev v realnem času)

    Tehnološka inovacija z uporabo ESP32 in NFC skenerjev

    Večja zadovoljstvo uporabnikov, saj lahko izberejo najbolj prosti čas za obisk fitnesa

    Enostavna integracija z obstoječimi fitnesi

    Prilagodljivost za spremljanje napredka uporabnikov (povprečen čas v fitnesu, število obiskov, napredek)

### SLABOSTI (W)

    Potrebujemo začetno kritično maso uporabnikov, da bi bila funkcionalnost učinkovita

    Možnost zavračanja uporabnikov, če je fitnes preveč zaseden

    Visoki stroški začetnega razvoja in implementacije

### PRILOŽNOSTI (O)

    Prvi v Sloveniji z to funkcionalnostjo, kar nas postavlja v prednost na trgu

    Možnost širjenja na druge fitnes centre v Sloveniji in širše

    Partnerstva z večjimi fitnes verigami, ki bodo želele vključiti to funkcionalnost

    Rast trga fitnesov, saj vse več ljudi skrbi za svoje zdravje

### GROŽNJE (T)

    Večje fitnes verige bi lahko kopirale našo funkcionalnost in jo uvedle v svoje sisteme

    Regulacija in zakonodaja o zbiranju in varovanju osebnih podatkov (še posebej, če bo vključeno spremljanje uporabnikov)

    Hitro spreminjajoči se trendi v fitnes industriji, ki bi lahko zmanjšali potrebo po naši storitvi

### Strategije iz SWOT:

    S-O strategija: Izkoristimo poznavanje ciljne skupine za hitro širjenje storitve in prilagoditev potrebam uporabnikov.

    W-O strategija: Povečajmo partnerstva s fitnesi, da pridobimo večjo kritično maso uporabnikov.

    S-T strategija: Poudarimo varnost in zaščito zasebnosti uporabnikov kot glavno prednost, da pomirimo morebitne skrbi.

    W-T strategija: Prilagodimo storitev z dodatnimi funkcionalnostmi, ki bodo težje kopirane s strani konkurence.

## Poslovni model in finančni plan
### Viri prihodkov:

    Brezplačna aplikacija za uporabnike, ki omogoča dostop do vse funkcionalnosti.

    Provizije od partnerskih fitnes centrov (2% za vključitev v naš sistem).

    Oglaševanje: promocija fitnes opreme in opreme za vadbo na naši spletni strani.

### Struktura stroškov:

    Začetni razvoj: 5.000€ (za razvoj aplikacije, integracijo NFC tehnologije in ESP32 sistemov)

    Mesečno vzdrževanje: 500€ (strežniki, podporna ekipa, posodobitve)

    Marketing: 300€ mesečno (spletno oglaševanje, promocijski dogodki)

### Strategija pridobivanja uporabnikov:

    Ciljamo na fitnes centre v večjih mestih Slovenije, kjer bo večje število uporabnikov.

    Povezovanje z influecerji v fitnes industriji.

    Partnerstva s fitnes verigami za širitev funkcionalnosti na večje število fitnes centrov.

## Navodila za zagon Python kode

### 1. Kloniraj repozitorij z GitHub-a

Najprej moraš klonirati repozitorij na svoj lokalni računalnik. To lahko storiš z naslednjim ukazom:

```
git clone https://github.com/Kos1r/Zakljucna.git
cd Zakljucna
```

### 2. Potrebne knjižnice

Za delovanje aplikacije so potrebne naslednje knjižnice:

- `tinydb`
- `flask`

Knjižnice lahko namestiš z ukazom:

```
pip install tinydb flask
```

### 3. Zaženi aplikacijo

Po tem, ko so vse knjižnice nameščene, lahko zaženeš aplikacijo z ukazom:

```
py main.py
```

### 4. Preveri aplikacijo v brskalniku

Aplikacija bo dostopna na naslovu:

```
http://127.0.0.1:8080
```

Preveri to v svojem brskalniku, da vidiš, ali aplikacija deluje.

### 5. Pogosti problemi

- **Napaka pri namestitvi knjižnic**: Prepričaj se, da imaš nameščen najnovejši `pip`. Lahko ga posodobiš z:

  ```
  pip install --upgrade pip
  ```

- **Napaka pri zagonu aplikacije**: Preveri, da imaš pravilno nastavljene poti in da je glavni Python skript pravilno poimenovan.

## Zaključek

FitRise Slovenija bo postal nepogrešljiv pripomoček za vsakogar, ki želi obiskovati fitnes in optimalno izkoristiti svoj čas. Naša rešitev ponuja inovativno spremljanje obiskovalcev in razpoložljivosti opreme ter omogoča boljše načrtovanje obiskov fitnesa, kar pomeni boljšo uporabniško izkušnjo. Smo pionirji na tem področju v Sloveniji, zato imamo odličen potencial za rast in širitev.
