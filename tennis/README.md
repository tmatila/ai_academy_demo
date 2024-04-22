# Tennismailat 
Tommilla on tennismaila-fetissi. Tässä demossa Tommin ja muun maailman mailat pistetään tietokantaan. Slideshow pyörittää kuvia maailman ja Tommin mailoista.

## Käyttö
Tarvitset Tommilta mailojen kuvat, jos haluat käyttää oikesti. Kansiossa tennis/static kuuluu olla melkoinen nippu kuvia, jotka eivät ole osa tätä repoa.

Koodi löytyy:

git clone https://github.com/tmatila/ai_academy_demo

Käytän pythonia tietokannan käpistelyyn, mitä varteen pitää asennella pyodbc

pip install pyodbc
sudo apt-get update
sudo apt-get install unixodbc unixodbc-dev

Lisäksi piti asentaa Microsoftin työkaluja:

curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"

Jos tämän ajo onnistuu ilman virheitä on jo aika pitkällä:
/bin/python3 /home/ai2024lectures/repos/ai_academy_demo/tennis/python/test_dB.py

Tietokannan salasana kulkee systeemivariaabelina:

export SQL_SERVER_PASSWORD='YourGoodPasswdComesHere'
   
## Ongelmia
SQL-serveri lopettaa "joskus" toimintansa. Sen voi tarkistaa
sudo docker ps
sudo docker ps --all

Ja tarvittaessa uudelleenkäynnistää
sudo docker start sql-edge





