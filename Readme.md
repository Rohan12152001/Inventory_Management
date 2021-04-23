**I have used the Flask framework & MySQL as the database**

**Assumptions:**

1) I have assumed that only a single manager is handling the access requests of equipments.

**How to configure the project on your Machine** 

1) Clone the project 

2) Install the dependencies from _requirements.txt_ 

3) Create a MySQL database on your machine 
   & edit the _configurations.py_ file 
   with the respective values of (host, database, user, password)
   
4) Also configure the secretKey for flask in _configuration.py_

5) Now, to create all the tables & insert some minimum data run the _migrate.py_ file.

6) What does the migrate.py file do ?
    > It will create four tables namely (equipments, employee, manager, requestQueue) & insert some data
    
    > Equipments has [Motherboard(P1), Keyboard(P2), Mouse(P3)]
            
    > Employee has [Rohan(E1), Akash(E2), Sagar(E3)] 

    > Manager has [Paresh(M1)]

    > requestQueue is Empty 
    [This table is used as a queue for keeping a track of the access requests from the employees]

    > To know know more about the tables you can check out the _migrate.py_ file.

7) Now we are ready to start the server
    > Run the command _python apis.py_ to run the server on port 5000




