import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


#Flask Setup
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)
#Flask Routes
@app.route("/")
def home():
    print('Welcome to the Hawaii WeatherBank')
    return(f'''Directory:
    <div> /api/v1.0/precipitation </div>
    <div> /api/v1.0/stations </div> 
    <div> /api/v1.0/tobs </div>
    <div> /api/v1.0/'start_date'(yyyy-mm-dd) </div>
    <div> /api/v1.0/'start_date'(yyyy-mm-dd)/'end_date'(yyyy-mm-dd) </div>''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    rain = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > last_year).\
        order_by(measurement.date).all()

    rain_totals = []
    
    for x in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(station.station, station.name).group_by(station.station).all()
    
    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    temps = session.query(measurement.date, measurement.tobs).group_by(measurement.tobs).all()

    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)