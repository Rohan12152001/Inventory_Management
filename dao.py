import mysql.connector
import datetime
from mysql.connector import Error
from configuration import DB

""" For database interactions only """

# Global functions (helpers)
def formatDateTime(givenTime):
    return datetime.datetime.fromtimestamp(
        int(givenTime)                    # Adding 19800 for IST time
    ).strftime('%d-%m-%Y || %H:%M:%S')

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

    def getName(self, ID):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_fetch_query = "select equipName from equipments WHERE equipID=%s"
            cursor.execute(sql_fetch_query, (ID,))
            records = cursor.fetchone()
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

    def approveEquipment(self, empID, empName, equipID, reqTime):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)

            sql_check_query = """UPDATE equipments 
                                 SET issued = %s, issueTime = %s, holderID = %s, holderName = %s 
                                 WHERE equipID = %s;"""

            cursor.execute(sql_check_query, (1, reqTime, empID, empName, equipID))
            connection.commit()
            print("Equipment approved !")
        except Error as e:
            print("Error updating data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def returnEquipment(self, empID, equipID):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)

            sql_check_query = """UPDATE equipments 
                                 SET issued = %s, issueTime = %s, holderID = %s, holderName = %s 
                                 WHERE equipID = %s;"""

            cursor.execute(sql_check_query, (0, None, None, None, equipID))
            connection.commit()
            print("Equipment returned !")
        except Error as e:
            print("Error updating data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


class Employee:
    def getAll(self):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_fetch_query = "select * from employee order by empID ASC"
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

    def getName(self, ID):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_fetch_query = "select empName from employee WHERE empID=%s"
            cursor.execute(sql_fetch_query, (ID,))
            records = cursor.fetchone()
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
            print("Successfully added new request !")
        except Error as e:
            print("Error inserting data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def getAll(self):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_fetch_query = "select * from requestQueue order by reqTime ASC"
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

    def getAllwithNames(self):
        empObject = Employee()
        equipObject = Equipment()
        buffer = self.getAll()
        records = buffer.copy()
        print(records)

        for record in records:
            empName = empObject.getName(record['empID'])['empName']
            equipName = equipObject.getName(record['equipID'])['equipName']
            record['equipName'] = equipName
            record['empName'] = empName
            record['reqTimeEpoch'] = record['reqTime']
            record['reqTime'] = formatDateTime(record['reqTime'])

        return records

    def removeDuplicates(self, equipID):
        try:
            connection = mysql.connector.connect(host=DB.host,
                                                 database=DB.database,
                                                 user=DB.user,
                                                 password=DB.password)
            cursor = connection.cursor(dictionary=True)
            sql_check_query = """DELETE FROM requestQueue
                                 WHERE equipID=%s"""
            cursor.execute(sql_check_query, (equipID,))
            connection.commit()
            print("Successfully deleted duplicates !")
        except Error as e:
            print("Error inserting data from MySQL table", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

