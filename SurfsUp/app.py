import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references
Measurement = Base.classes.measurement
Station = Base.classes.station



# Flask Setup
app = Flask(__name__)

# 1) Flask Routes
@app.route("/")
def home():
    return (
    f"<h2>Welcome to the Hawaii Climate App.</h2><br/>"
    f"Available routes are:<br/>"
    f"<ul><li>Precipitation (Last 12 months) - <code>/api/v1.0/precipitation</code></li></ul>"
    f"<ul><li>Stations - <code>/api/v1.0/stations</code></li></ul>"
    f"<ul><li>Temperature Observations - <code>/api/v1.0/tobs</code></li></ul>"
    f"<ul><li>Calculated Temperatures (From Date) - <code>/api/v1.0/start</code></li></ul>"
    f"<ul><li>Calculated Temperatures (Between Dates) - <code>/api/v1.0/start/end</code></li></ul>"
    f""
    f"The <b>Calculated Temperatures</b> route will return the minimum, average, and maximum temperatures of the date range given. "
    f"<br>If a single date is given, temperatures will be calculated for all dates equal to or greater than the date given. "
    f"<br>If two dates are given, temperatures will be calculated for all dates between the two given, inclusively. "
    f"<br>To use these routes, replace <code>start</code> and <code>end</code> with dates in YYYY-MM-DD format.")


# 2) Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query dates and precipitation
    session = Session(engine)
    dates = session.query(Measurement.date).all()

    # Extract and store the start and end dates of one year's data
    last_date = dates[-1][0]
    end_dt = dt.datetime.strptime(last_date, '%Y-%m-%d')
    end_dt = end_dt.date()
    start_dt = end_dt - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>=start_dt).\
        filter(Measurement.date<=end_dt).all()

    # Create a dictionary using 'date' as the key and 'prcp' as the value
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict) 

    session.close()

    # Return the list of dates and precipitation
    return jsonify(prcp_list)
    


# 3) Stations Route
@app.route("/api/v1.0/stations")
def stations():
    
    # Query all distinct stations
    session = Session(engine)
    results = session.query(Station.name).all()
    
    # Store results as a list
    stations_list = list(np.ravel(results))

    session.close()

    # Return a list of all distinct stations
    return jsonify(stations_list)



# 4) Temperature Observation Route
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query all dates
    session = Session(engine)
    dates = session.query(Measurement.date).all()
    
    # Extract and store the start and end dates of one year's data
    last_date = dates[-1][0]
    end_dt = dt.datetime.strptime(last_date, '%Y-%m-%d')
    end_dt = end_dt.date()
    start_dt = end_dt - dt.timedelta(days=365)
    
    # Find the most active stations
    stations = session.query(Measurement.station).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    most_active_station = stations[0][0]

    # Query one year's worth of temperature observations
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>=start_dt).\
        filter(Measurement.date<=end_dt).\
        filter(Measurement.station==most_active_station).all()
    
    # Create a dictionary using 'date' as the key and 'tobs' as the value
    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict) 

    session.close()

    # Return the list of dates and temperature observations
    return jsonify(tobs_list)



# 5.a) TMIN, TAVG, TMAX with only start date
@app.route("/api/v1.0/<start>")
def start(start):
    
    # Query dates and temperature observations
    session = Session(engine)

     # Select first and last dates of the data set
    date_start = session.query(func.min(Measurement.date)).first()[0]
    date_end = session.query(func.max(Measurement.date)).first()[0]

    # Calculate temperatures if the input date is in the data set
    if start >= date_start and start <= date_end:
        calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= date_end).all()[0]
    
        return (
            f"Min temp: {calc_temps[0]}</br>"
            f"Avg temp: {calc_temps[1]}</br>"
            f"Max temp: {calc_temps[2]}")
    
    else:
        return jsonify({"error": f"The date {start} was not found. Please select a date between 2010-01-01 and 2017-08-23."}), 404



# 5.b) TMIN, TAVG, TMAX with start and end dates
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    # Query dates and temperature observations
    session = Session(engine)

    # Select first and last dates of the data set
    date_start = session.query(func.min(Measurement.date)).first()[0]
    date_end = session.query(func.max(Measurement.date)).first()[0]

    # Calculate temperatures if the input dates are in the data set
    if start >= date_start and end <= date_end:
        calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]
    
        return (
            f"Min temp: {calc_temps[0]}</br>"
            f"Avg temp: {calc_temps[1]}</br>"
            f"Max temp: {calc_temps[2]}")
    
    else:
        return jsonify({"error": f"The dates {start} or {end} were not found. Please select dates between 2010-01-01 and 2017-08-23."}), 404
            

if __name__ == "__main__":
    app.run(debug=True)