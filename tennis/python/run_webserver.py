# I have now populated my database table TennisRackets successfully. 

# Now I want to create a web page that presents database items as web-page. Use python to access database. There will be three pages, each showing slideshow for database items. These pages are:
# 1) "Whole database"
# 2) " Tommi's racket collection" that only shows rackets for which "Owned_by_Tommi" is greater than 0 
# 3) "Tommi's shopping list" that only shows rackets for which "Tommi_wants_this" is greater than zero. 

# In the top of the page, there are push button to choose from these three pages. 

#  For each slide the strucure is the same. Items from top to down:
# 1) Text: Manufacturer + Name + "from year" + Year
# 2) Showing image read from directory listed in "Image"
# 3) Text: DescriptionTommi

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#            static_folder='/home/ai2024lectures/repos/ai_academy_demo/tennis/static/',
#            template_folder='/home/ai2024lectures/repos/ai_academy_demo/tennis/template/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:'+os.environ.get('SQL_SERVER_PASSWORD')+'@localhost,1495/AI2024?driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app)

class TennisRackets(db.Model):
    __tablename__ = 'TennisRackets'
    ID = db.Column(db.String, primary_key=True)
    Manufacturer = db.Column(db.String)
    Name = db.Column(db.String)
    Year = db.Column(db.Integer)
    Image = db.Column(db.String)
    DescriptionTommi = db.Column(db.Text)
    Owned_by_Tommi = db.Column(db.Integer)
    Tommi_wants_this = db.Column(db.Integer)

@app.route('/')
def whole_database():
    rackets = TennisRackets.query.all()
    #print("===================================")
    #for racket in rackets:
    #    print(racket.Image)  # Debugging line to inspect image filenames
    return render_template('slideshow.html', rackets=rackets, title="Whole Database")

@app.route('/owned_by_tommi')
def owned_by_tommi():
    rackets = TennisRackets.query.filter(TennisRackets.Owned_by_Tommi > 0).all()
    return render_template('slideshow.html', rackets=rackets, title="Tommi's Racket Collection")

@app.route('/tommi_wants')
def tommi_wants():
    rackets = TennisRackets.query.filter(TennisRackets.Tommi_wants_this > 0).all()
    return render_template('slideshow.html', rackets=rackets, title="Tommi's Shopping List")

if __name__ == '__main__':
    app.run(debug=True)

    