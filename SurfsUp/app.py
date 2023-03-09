import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database Setup

engine= create_engine("sqlite:///hawaii.sqlite")

#reflect database into new model
Base= automap_base()

#reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement=Base.classes.measurement
Station= Base.classes.station

#Flask Setup

app= Flask(__name__)

#Flask Routes

@app.route("/")
def homepage():
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

#Precipitation route
@app.route("/api/v1.0/precipitation")
def precipition():
    session=Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= '2016-08-23').\
            order_by(Measurement.date).all()

    session.close()

#Create a dictionary with date:precipitation
    precip_results = []
    for date, prcp in results:
        precip_dict ={}
        precip_dict[date]= prcp
       
        precip_results.append(precip_dict)

    return jsonify(precip_results)    

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)

    #Query all stations
    results = session.query(Station.station,Station.name).all()
    session.close()

    station_names = list(np.ravel(results))
    
    return jsonify(station_names)

#Temperature route    
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    results = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station =='USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()
    session.close()
    temps = list(np.ravel(results))

    return jsonify(temps)

#Temperature min, max average from dynamic start date 
@app.route("/api/v1.0/<start>")
def start_Date(start):
    session=Session(engine) 
    start = dt.datetime.strptime(start, "%m-%d-%Y")
    results= session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close
    date_temp = list(np.ravel(results))
    return jsonify (date_temp)

#Temperature min, max average from dynamic start and end date 
@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    session=Session(engine)
    start = dt.datetime.strptime(start, "%m-%d-%Y") 
    end = dt.datetime.strptime(end, "%m-%d-%Y")
    results= session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date > start).\
        filter(Measurement.date < end).all()
    session.close
    date_range_temps = list(np.ravel(results))
    return jsonify (date_range_temps)

if __name__ == '__main__':
    app.run(debug=True)

