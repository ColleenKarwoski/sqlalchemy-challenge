import numpy as np

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
Hawaii=Base.measurements.stations

#Flask Setup

app= Flask(__name__)

#Flask Routes

@app.route("/")
def homepage():
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        )

