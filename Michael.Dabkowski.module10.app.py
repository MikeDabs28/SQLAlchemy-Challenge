# Import the dependencies.
import numpy as np

import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

#Create connection to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine,reflect=True)

# Save references to each table
Measurement = base.classes.measurement
station = base.classes.station


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create initial route
@app.route("/")
def welcome ():
    """List all available api routes."""""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

#Create route for precipitation levels

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session from Python to DB
    session = Session(engine)

    #return list of precipitation and date
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()
    
    session.close


    #create dictionary from raw data
    all_prcp = []
    for date,prcp in results:
        prcp_dic = {}
        prcp_dic["date"] = date
        prcp_dic["prcp"] = prcp

        all_prcp.append(prcp_dic)

    return jsonify(all_prcp)

#return list of stations

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station).\
                order_by(station.station).all()
    
    session.close()

    #convert to list

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


#return list of tobs
@app.route("/api/v1.0/tobs")
def tobs ():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station =='USC00519281').\
        order_by(Measurement.date).all()
    
    session.close()

    #convert to dictionary
    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dic = {}
        tobs_dic["prcp"] = prcp
        tobs_dic["date"] = date
        tobs_dic["tobs"] = tobs

        all_tobs.append(tobs_dic)
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):

    session = Session(engine)

    #query tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
    
    session.close()

    #create dictionary and append a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in results:
            start_date_tobs_dic = {}
            start_date_tobs_dic["min_temp"] = min
            start_date_tobs_dic["avg_temp"] = avg
            start_date_tobs_dic["max_temp"] = max
            start_date_tobs.append(start_date_tobs_dic)

    return jsonify(start_date_tobs)
    
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):

    session = Session(engine)

    #query tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    session.close()

    #create dictions,a ppend start/end date

    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dic = {}
        start_end_tobs_dic["min_temp"] = min
        start_end_tobs_dic["avg_temp"] = avg
        start_end_tobs_dic["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dic)

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)

    


