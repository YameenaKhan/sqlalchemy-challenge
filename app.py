import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Setting up Homepage
################################
@app.route("/")
def Homepage():
    """HOMEPAGE"""
    """List all available api routes."""
    return (
        f"HOMEPAGE:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        
    )


#Setting up Precipitation Page
################################
@app.route("/api/v1.0/precipitation")
def Precipitation():
    """Precipation Data"""

# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dict for all the precipation data"""
    #Query to get the dates and precipation data per dates
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

# Convert list of tuples into dictionary
    prcp_dict = dict()
    
    for date,prcp in results:
        prcp_dict.setdefault(date, []).append(prcp)

    return jsonify(prcp_dict)

#Setting up Stations Page
################################
@app.route("/api/v1.0/stations")
def Stations():
    """Stations Data"""

# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    #Query to get the all stations
    results = session.query(Station.station).all()

    session.close()

 # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

#Setting up Tobs Page
################################
@app.route("/api/v1.0/tobs")
def Tobs():
    """Tobs Data"""

# Create our session (link) from Python to the DB
    session = Session(engine)
#Calculating the query date
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    query_date

    """Return a list of tempratures observations of the most active station for the previous year of data"""
    # Query to get temp observations for the most active station for the previous year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= query_date).all()


    session.close()

 # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

#Setting up Range stats page
################################
@app.route("/api/v1.0/<start>")

def start_date(start):
    
# Create our session (link) from Python to the DB  
    session = Session(engine)

#Query to get the average, max and min temprature for the time period from the start date entered to the end of dataset 
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close() 

#Converting data recieved into comprehensive dictionary
    key_list = ['Average_Temprature','Max_Temprature', 'Minimum_Temprature']  

    result_list = list(np.ravel(results))

    res = dict(zip(key_list, result_list))


    return jsonify(res)

#Setting up within range stats page
################################

@app.route("/api/v1.0/<start>/<end>")

def start_end_date(start, end):
    
 # Create our session (link) from Python to the DB    
    session = Session(engine)

 #Query to get the average, max and min temprature for the time period from the start date to the end date entered  
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close() 

#Converting data recieved into comprehensive dictionary
    key_list = ['Average_Temprature','Max_Temprature', 'Minimum_Temprature']  

    result_list = list(np.ravel(results))

    res = dict(zip(key_list, result_list))

    return jsonify(res)






if __name__ == '__main__':
    app.run(debug=True)