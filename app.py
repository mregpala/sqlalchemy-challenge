
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
Station = base.classes.station


#Create Session


#Setup Flastk
from flask import Flask, jsonify

#Datetime
import datetime as dt



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def welcome():
	return(
			f"/api/v1.0/stations<br/>"
			f"/api/v1.0/tobs<br/<><br/>"
			f"/api/v1.0/stats"
	) 

@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)
	v_stations = session.query(Station).all()
	v_station_list = []
	for station in v_stations:
		v_station_dict =  {"id": station.id,
		                   "station": station.station,
						   "name": station.name,
						   "latitude": station.latitude,
						   "longitude": station.longitude,
						   "elevation": station.elevation
						  }
		v_station_list.append(v_station_dict)
	return jsonify(v_station_list)

@app.route("/api/v1.0/tobs")	
def tobs():
	session = Session(engine)
	#Genereate anchor date for prior year.  365 days in past.
	max_date = session.query(func.max(Measurement.date)).first()
	v_prior_year_start = dt.datetime.strptime(max_date[0], "%Y-%m-%d") - dt.timedelta(days=365)

	#Genereate query to pull back busiest station  for past 365 days.  User v_prior_year variable set in prior step.
	v_meas = session.query(Measurement.station,func.count(Measurement.id)).\
             	     group_by(Measurement.station).\
                	 filter(Measurement.date >= v_prior_year_start).\
                	 order_by(func.count(Measurement.id).desc()).first()					 
	v_most_active_station = v_meas[0]
	v_most_active_count = v_meas[1]

	#Generate query to pull detail observations for most active station for past year
	v_tobs = session.query(Measurement.date, Measurement.tobs).\
                	 filter(Measurement.date >= v_prior_year_start,Measurement.station == v_most_active_station).\
                	 order_by(Measurement.date).all()	

	v_tob_list = []

	for obs in v_tobs:
		v_final_dict = {}
		v_final_dict = {"name": obs.date,
						"tob": obs.tobs}
		v_tob_list.append(v_final_dict)
	v_tob_list

	return jsonify(v_tob_list)

@app.route("/api/v1.0/stats/<start>")
def stats_by_day(start):
	session = Session(engine)
	v_statistics = session.query(func.max(Measurement.prcp).label("max"),
							     func.min(Measurement.prcp).label("min"),
								 func.avg(Measurement.prcp).label("avg"),
								 func.count(Measurement.prcp).label("observations")).\
						    filter(Measurement.date == start).first()
	v_station_list = []
	for statistic in v_statistics:
		v_dict = dict({"min": v_statistics.min,
		               "max": v_statistics.max,
				       "avg": v_statistics.avg,
				       "observations": v_statistics.observations,
				       "start_date": start}
					)
	return (f"Hello")

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