
#Import sqlalchemy libraries
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect, distinct

#Setup engine and reflect database.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

#Setup Flastk
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
	return(
			f"/api/v1.0/stations<br/>"
			f"/api/v1.0/tobs<br/>"
			f"/api/v1.0/start_date<br/>"
			f"/api/v1.0/start_date/end_date"
	) 


if __name__ == "__main__":
    app.run(debug=True)