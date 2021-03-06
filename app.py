
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

#Get Class
Measurement = base.classes.measurement

#Create Session


#Setup Flastk
from flask import Flask, jsonify

#Setup Pandas
import pandas as pd



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def welcome():
	return(
			f"/api/v1.0/stations<br/>"
			f"/api/v1.0/tobs<br/<><br/>"
			f"/api/v1.0/stats"
	) 


@app.route("/api/v1.0/stats/<start>")
def stats_by_day(start):
	session = Session(engine)
	v_statistics = session.query(func.max(Measurement.prcp).label("max"),
							     func.min(Measurement.prcp).label("min"),
								 func.avg(Measurement.prcp).label("avg"),
								 func.count(Measurement.prcp).label("observations")).\
						    filter(Measurement.date == start).first()
	v_dict = {}
	for statistic in v_statistics:
		v_dict = { "min": v_statistics.min,
		           "max": v_statistics.max,
				   "avg": v_statistics.avg,
				   "observations": v_statistics.observations,
				   "start_date": start
			     }
	return jsonify(v_dict)

@app.route("/api/v1.0/stats/<start>/<end>")
def stats_range(start, end):
	session = Session(engine)
	v_statistics = session.query(func.max(Measurement.prcp).label("max"),
							     func.min(Measurement.prcp).label("min"),
								 func.avg(Measurement.prcp).label("avg"),
								 func.count(Measurement.prcp).label("observations")).\
						    filter(Measurement.date >= start, Measurement.date <= end).first()
	v_dict = {}
	for statistic in v_statistics:
		v_dict = { "min": v_statistics.min,
		           "max": v_statistics.max,
				   "avg": v_statistics.avg,
				   "observations": v_statistics.observations,
				   "start_date": start,
				   "end_date": end
			     }
	return jsonify(v_dict)


if __name__ == "__main__":
    app.run(debug=True)