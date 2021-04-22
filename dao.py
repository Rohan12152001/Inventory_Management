import mysql.connector
import requests, os
import time
import datetime
from flask import Flask, jsonify, request, render_template
from mysql.connector import Error
from mysql.connector import errorcode
from configuration import DB

""" For database interactions only """

# For equipments

class Equipment:
    def getAll(self):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_fetch_query = "select * from equipments order by equipID ASC"
            cursor.execute(sql_fetch_query)
            records = cursor.fetchall()
            # print(records)
            # print(len(records))
        except Error as e:
            print("Error reading data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        return records


class BufferedRequests:
    def checkBuffer(self, empID, equipID):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_check_query = f"select empID from requestQueue " \
                              "WHERE empID = %s AND " \
                              "equipID = %s;"
            cursor.execute(sql_check_query, (empID, equipID))
            records = cursor.fetchall()
            # print(len(records))
        except Error as e:
            print("Error reading data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        if len(records) > 0:
            return 1
        else:
            return 0

    def addNewRequest(self, empID, equipID, reqTime):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_check_query = """INSERT INTO requestQueue 
                                (empID, equipID, reqTime) 
                                values (%s,%s,%s)"""
            cursor.execute(sql_check_query, (empID, equipID, reqTime))
            connection.commit()
            print("Success")
        except Error as e:
            print("Error inserting data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")




