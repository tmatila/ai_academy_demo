from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:' + os.environ.get('SQL_SERVER_PASSWORD') + '@localhost,1495/AI2024?driver=ODBC+Driver+17+for+SQL+Server'
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

def update_image_defaults():
    # Query for records where Image is None
    rackets_with_no_image = TennisRackets.query.filter(TennisRackets.Image == None).all()
    for racket in rackets_with_no_image:
        racket.Image = 'not_found.png'  # Update the Image field
    db.session.commit()  # Commit the changes to the database

# Call the function to update the records
if __name__ == '__main__':
    with app.app_context():
        update_image_defaults()
        print("Updated records with missing images.")


