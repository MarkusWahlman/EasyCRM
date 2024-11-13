# EasyCRM

EasyCRM on yrityksille suunnattu yksinkertainen asiakashallintajärjestelmä (CRM). Yrityskäyttäjä voi luoda yrityksiä, joilla voi olla useita kontakteja. Yrityskäyttäjä voi myös hallinnoida yritysten tietoja sekä luoda uusia käyttäjiä, joilla on oikeus joko muokata tai tarkastella yrityksiä.

### Sovelluksen tavoitteet

- **Yrityskäyttäjän luominen**  
  Kuka tahansa voi rekisteröityä sovellukseen yrityskäyttäjäksi.

- **Tietojen hakeminen**  
  Yrityskäyttäjä pystyy tarkastelemaan ja hakemaan luotuja yrityksiä.

- **Yritysten tietojen hallinnointi**  
  Mahdollisuus muokata ja poistaa yritysten perustietoja ja kontakteja.

- **Käyttäjien hallinnointi**  
  Yrityskäyttäjä voi luoda uusia käyttäjiä, joilla on joko oikeus katsella tai hallinnoida yrityksiä. Yrityskäyttäjä voi myös halutessaan poistaa nämä käyttäjät tai muokata niiden oikeuksia.

## Sovellus on saatavilla Vercelissä

Sovelluksen uusin versio on suoraan käytettävissä Vercel alustalla.  
Pääset käyttämään sovellusta Vercelissä [tästä](https://easy-crm-two.vercel.app)

## Kehittäjän asennusohjeet

### 1. Kloonaa projekti

Kloonaa projekti GitHubista ja siirry projektin hakemistoon:

```
$ git clone https://github.com/MarkusWahlman/EasyCRM.git
$ cd EasyCRM
```
### 2. Luo .env-tiedosto

Luo projektiisi .env-tiedosto ja lisää siihen seuraavat tiedot:

```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
### 3. Asenna riippuvuudet

Projektissa käytetään [poetry-riippuvuushallintatyökalua](https://python-poetry.org/docs/#installation). Varmista, että olet asentanut sen onnistuneesti. Asenna tarvittavat riippuvuudet komennolla:

```
$ poetry install
```
### 4. Määritä tietokannan skeema

Määritä tietokanta skeema komennolla:

```
$ psql < schema.sql
```
### 5. Käynnistä sovellus

Siirry poetry-virtuaaliympäristöön ja käynnistä sovellus:

```
$ poetry shell
$ cd src/
$ flask --debug run
```