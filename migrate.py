import mysql.connector
from mysql.connector import Error
from configuration import DB

"""

Create a MySQL database first 
And configure the variables 
(host,database,user, password) in configurations.py accordingly
And then run this script...

"""

# Global connection object
connection = mysql.connector.connect(host=DB.host,
                                     database=DB.database,
                                     user=DB.user,
                                     password=DB.password)

# Triggered when server shut down
def close():
    if connection.is_connected():
        print("Closing connection !")
        connection.close()

def SET_SQL_UPDATE():
    try:
        cursor = connection.cursor()
        sql_query = """SET SQL_SAFE_UPDATES = 0;"""
        cursor.execute(sql_query)
        connection.commit()
        print("SET_SQL_UPDATE to 0 !")
    except Error as e:
        print("Error from MySQL ", e)

    finally:
        if (connection.is_connected()):
            cursor.close()

# Basically a table for keeping track of equipments
def forEquipments():
    try:
        cursor = connection.cursor()
        sql_query = """CREATE TABLE equipments(
                        equipID varchar(10) PRIMARY KEY,
                        equipName varchar(50),
                        issued boolean,
                        issueTime INT,
                        holderID varchar(10),
                        holderName varchar(50)
                        );"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into equipments values('P1', 'Motherboard',False, null, null, null);"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into equipments values('P2', 'Keyboard',False, null, null, null);"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into equipments values('P3', 'Mouse',False, null, null, null);"""
        cursor.execute(sql_query)
        connection.commit()
        print("Create & Insert for equipments !")
    except Error as e:
        print("Error from MySQL forEquipments()", e)

    finally:
        if (connection.is_connected()):
            cursor.close()

# Table for keeping records of employees
def forEmployee():
    try:
        cursor = connection.cursor()
        sql_query = """CREATE TABLE employee(
                        empID varchar(10) PRIMARY KEY,
                        empName varchar(50) not null,
                        currentHolding INT DEFAULT 0
                        );"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into employee values('E1', 'Rohan', 0);"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into employee values('E2', 'Akash', 0);"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into employee values('E3', 'Sagar', 0);"""
        cursor.execute(sql_query)
        connection.commit()
        print("Create & Insert for employees !")
    except Error as e:
        print("Error from MySQL forEmployee() ", e)

    finally:
        if (connection.is_connected()):
            cursor.close()

# This requestQueue table is used to maintain the
# access requests from the employees
def forRequestQueue():
    try:
        cursor = connection.cursor()
        sql_query = """CREATE TABLE requestQueue(
                        empID varchar(10),
                        equipID varchar(50) not null,
                        reqTime INT,							 
                        PRIMARY KEY (empID, equipID) 
                        );"""
        cursor.execute(sql_query)
        connection.commit()
        print("Create for requestQueue !")
    except Error as e:
        print("Error from MySQL forBuffer() ", e)

    finally:
        if (connection.is_connected()):
            cursor.close()

# Table for keeping records of employees
def forManager():
    try:
        cursor = connection.cursor()
        sql_query = """CREATE TABLE manager(
                        manID varchar(10) PRIMARY KEY,
                        manName varchar(50) not null
                        );"""
        cursor.execute(sql_query)
        connection.commit()
        sql_query = """insert into manager values('M1', 'Paresh');"""
        cursor.execute(sql_query)
        connection.commit()
        print("Create & Insert for manager !")
    except Error as e:
        print("Error from MySQL forManager() ", e)

    finally:
        if (connection.is_connected()):
            cursor.close()

if __name__ == '__main__':
    SET_SQL_UPDATE()
    forEquipments()
    forEmployee()
    forManager()
    forRequestQueue()
    # close connection
    close()







