import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Home Page<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>start&end</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()
    
    precipitation_date = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        precipitation_date.append(prcp_dict)
    return jsonify(precipitation_date)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_data = session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    station_name = list(np.ravel(station_data))

    return jsonify(station_name)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temp_data = session.query(Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.date <= '2017-08-23').all()
    session.close()
    temp = list(np.ravel(temp_data))

    return jsonify(temp)



@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end='2017-08-23'):
    session = Session(engine)
    calc_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temp = list(np.ravel(calc_temp))
    
    return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)