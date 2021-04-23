import os, sys
import time, signal
from flask import Flask, request, \
    render_template, redirect, \
    url_for, flash
from dao import Equipment, BufferedRequests, Employee
from configuration import DB
from dao import close
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# app
app = Flask(__name__)

# signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    close()
    sys.exit(0)

# Employee Home page ##
@app.route('/')
def home_page():
    equipments = Equipment()
    records = equipments.getAll()
    return render_template('Home.html', records=records)

@app.route('/issue')
def issue_page():
    # we are sending hidden form data of equipID to this html page
    employee = Employee()
    records = employee.getAll()
    return render_template('IssueEquip.html', records=records)

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
        epochTime = int(time.time())
        object.addNewRequest(empID, equipID, epochTime)
        message = "Your request is now sent to the manager !"
        flash(message)
        return redirect(url_for('home_page'))

@app.route('/returnPost', methods=['POST'])
def return_post():
    empID = request.form.get('empID')
    equipID = request.form.get('equipID')

    # Update the status of equipment in DB
    equipments = Equipment()
    equipments.returnEquipment(empID, equipID)

    return redirect(url_for('home_page'))

# Manager Home page ##
@app.route('/manager')
def manager_home():
    equipments = Equipment()
    equipmentRecords = equipments.getAll()

    buffer = BufferedRequests()
    bufferRecords = buffer.getAllwithNames()

    return render_template('managerHome.html',
                           records=equipmentRecords,
                           bufferRecords=bufferRecords)

@app.route('/approve', methods=['POST'])
def approve_equipment():
    empID = request.form.get('empID')
    equipID = request.form.get('equipID')
    empName = request.form.get('empName')
    reqTime = request.form.get('issueTime')

    # 1. change in equipments table
    equipment = Equipment()
    equipment.approveEquipment(empID, empName, equipID, reqTime)

    # 2. change in buffer (remove the duplicate requests)
    buffer = BufferedRequests()
    buffer.removeDuplicates(equipID)

    return redirect(url_for('manager_home'))

if __name__ == '__main__':
    app.secret_key = DB.secretKey
    # signal to close the DB connection
    signal.signal(signal.SIGINT, signal_handler)
    app.run(port=5000, debug=False)

