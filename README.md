# Aurinkokuntasimulaattori

## Esittely

Ohjelmoinnin peruskurssi Y2:n kurssiprojekti (kevät 2019).
Aurinkokuntasimulaattori simuloi aurinkokunnan kappaleiden liikkeitä. Simulaatioon voidaan lisätä omia satelliitteja,
ja simulaation keston sekä simulaatioaskeleen voi käyttäjä määrittää.

## Asennusohje

Ohjelma tarvitsee toimiakseen PyQt5-kirjaston käyttöliittymää varten.

## Käyttöohje

Ohjelma käynnistetään ajamalla main.py-tiedosto, jolloin graafinen käyttöliittymä käynnistyy.

Ikkunasssa vasemmalla voi lisätä satelliitteja aurinkokuntaan. Klikkaamalla oikealla olevaa ruutua, jossa
aurinkokunta on, voi valita helposti x- ja y-koordinaatit satelliitille.

Liukusäätimillä voi asettaa simulaation keston ja aika-askeleen. Kun simulaatio on käynnistetty, sen voi
halutessaan lopettaa ennenaikaisesti painamalla käynnistyspainiketta uudelleen. Simulaation loputtua
aurinkokunnan voi vielä palauttaa alkutilaansa samaista nappia painamalla.

Ohjelmalla on asetustiedosto "settings.csv", joka määrää aurinkokunnan alkutilanteen ja siinä olevat planeetat.
Asetustiedostoa voi halutessaan muokata: jokainen rivi tiedostossa on yksi planeetta (tai tähti).
Kukin rivi on muotoa: `Nimi,massa,säde,paikka,nopeus,väri`, jossa paikka, nopeus ja väri ovat muotoa `x:y:z`.
Massa on kilogrammoina, säde ja paikka metreinä ja nopeus m/s. Väri on RGB-arvo, mutta se ei ole pakollinen,
vaan voidaan halutessa jättää pois, jolloin kappaleelle arvotaan väri.

Esimerkiksi: `Aurinko,1.9885e30,696e6,0:0:0,0:0:0,255:255:0`
