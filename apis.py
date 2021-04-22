import mysql.connector
import requests, os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import time
import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from mysql.connector import Error
from mysql.connector import errorcode
from dao import Equipment, BufferedRequests
from configuration import DB

# app
app = Flask(__name__)

# Home page
@app.route('/')
def home_page():
    equipments = Equipment()
    records = equipments.getAll()
    return render_template('Home.html', records=records)

@app.route('/issue')
def issue_page():
    # we are sending hidden form data of equipID to this html page
    return render_template('IssueEquip.html')

@app.route('/issuePost', methods=['POST'])
def issue_post():
    empID = request.form.get('empID')
    equipID = request.form.get('equipID')
    # send request to manager (if not in bufferedRequests)
    object = BufferedRequests()
    if(object.checkBuffer(empID, equipID)):
        # Dont add new request
        message = "Your request is already sent to the manager !"
        flash(message)
        return redirect(url_for('home_page'))
    else:
        # add new request
        object.addNewRequest(empID, equipID, int(time.time()))
        message = "Your request is now sent to the manager !"
        flash(message)
        return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.secret_key = DB.secretKey
    app.run(port=5000, debug=True)

