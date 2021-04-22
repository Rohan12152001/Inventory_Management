import mysql.connector
import requests, os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import time
import datetime
from flask import Flask, jsonify, request, render_template
from mysql.connector import Error
from mysql.connector import errorcode
from dao import Equipment

# app
app = Flask(__name__)

# Home page
@app.route('/')
def home_page():
    equipments = Equipment()
    records = equipments.getAll()
    return render_template('Home.html', records=records)


if __name__ == '__main__':
    # Run app on localhost
    app.run(port=5000, debug=True)

