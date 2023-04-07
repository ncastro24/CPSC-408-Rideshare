import mysql.connector
import random
from helper import helper
conn = mysql.connector.connect(host="localhost", user="root", password="cpsc408!", auth_plugin='mysql_native_password', database="RideShare")

#create cursor Object
cur_obj = conn.cursor()

######################

###UNCOMMMENT IF DB / TABLES ARE MISSING###

# create db
# mycursor.execute("CREATE SCHEMA RideShare;")

# create tables
# DRIVER
#cur_obj.execute("CREATE TABLE Driver (driverID VARCHAR(22) NOT NULL UNIQUE PRIMARY KEY, name VARCHAR(22), licensePlate VARCHAR(7), driverMode BOOLEAN NOT NULL, driverRating FLOAT)")
# RIDER
#cur_obj.execute("CREATE TABLE Rider (riderID VARCHAR(22) NOT NULL UNIQUE PRIMARY KEY, name VARCHAR(22))")
# RIDE
#cur_obj.execute("CREATE TABLE Ride (rideID INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT, driverID VARCHAR(22), riderID VARCHAR(22), pickUp VARCHAR(22), dropOff VARCHAR(22), rideRating FLOAT)")

# create foreign keys
#cur_obj.execute("ALTER TABLE Ride ADD FOREIGN KEY (driverID) REFERENCES Driver(driverID)")
#cur_obj.execute("ALTER TABLE Ride ADD FOREIGN KEY (riderID) REFERENCES Rider(riderID)")

#confirms execution worked by printing result
#cur_obj.execute("SHOW DATABASES;")
#for row in cur_obj:
    #print(row)

# putting in test values
#query = "INSERT INTO Driver (driverID, name, licensePlate, driverMode, driverRating) VALUES (%s, %s, %s, %s, %s)"
#values = [('jdoe12', 'Jane Doe', '3D42LWX', '0', '0.0'),
#('apple34', 'John Appleseed', '4HW12LK', '1', '5.0'),
#('ilikered', 'Tom Baker', '9WO3BM2', '1', '3.5'),
#('0new2', 'Edward Laguna', 'Y3TB2PL', '0', '4.5')]

#cur_obj.executemany(query, values)
#conn.commit()
#print(cur_obj.rowcount, "rows were inserted")

#query = "INSERT INTO Rider (riderID, name) VALUES (%s, %s)"
#values = [('123alpha', 'Alex Cook'),
#('roxyrocks', 'Roxanne Rivers'),
#('100bc', 'Joe Smith'),
#('cats300', 'Ruth Lee')]

#cur_obj.executemany(query, values)
#conn.commit()
#print(cur_obj.rowcount, "rows were inserted")

#testing
#cur_obj.execute("SELECT * FROM Driver;")
#cur_obj.execute("SELECT driverMode FROM Driver WHERE name LIKE 'Tom Baker';")
#cur_obj.execute("SELECT * FROM Driver WHERE driverMode = 1 ORDER BY name;")
#cur_obj.execute("SELECT * FROM Rider;")
#cur_obj.execute("SELECT name FROM Rider WHERE riderID LIKE '100bc';")
#result = cur_obj.fetchall()
#helper.pretty_print(result)

######################

# tuple to string
def tupToStr(tup):
    s = ''
    for item in tup:
        s = s + str(item)
    return s

#start screen of application
def startScreen():
    print("~~~Welcome to RideShare!~~~\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n~ Returning User: Press 1\n~ New User: Press 2\n~ Exit: 0\n")
    input = helper.get_choice([0,1,2])

    if input == 1:
        returningUser()
    if input == 2:
        newUser()
    if input == 0:
        print("Goodbye!")
        #break

# used to check both driver and rider tables for an existing user id
def checkIfUserExists(id):
    isUser = 0;
    query = "SELECT * FROM Driver WHERE driverID LIKE '" + id + "';"
    cur_obj.execute(query)
    driverCheck = cur_obj.fetchall()
    #helper.pretty_print(driverCheck)
    if driverCheck:
        isUser = 1
    query = "SELECT * FROM Rider WHERE riderID LIKE '" + id + "';"
    cur_obj.execute(query)
    riderCheck = cur_obj.fetchall()
    #helper.pretty_print(riderCheck)
    if riderCheck:
        isUser = 2
    return isUser


def returningUser():
    uid = input("Enter User ID [Enter 0 to go back]:\n ")

    if uid == "0":
        print("\n")
        startScreen()
    else:
        if checkIfUserExists(uid) == 0:
            print("User ID not found! Please try again\n")
            returningUser()
        if checkIfUserExists(uid) == 1:
            print("\n")
            driverUser(uid)
        if checkIfUserExists(uid) == 2:
            print("\n")
            riderUser(uid)

#create a new user
def newUser():
    print("Create a New User Account\n")
    print("Are you a Driver [1] or Rider [2]? [Enter 0 to go back]\n")
    choice = helper.get_choice([0,1,2])

    if choice == 0:
        startScreen()
    if choice == 1:
        nuid = input("Create your user id:\n ")
        if nuid == 0:
            #username cannot be a singular 0 as that is what is used to exit
            print("User ID cannot be 0!\n")
            newUser()
        elif checkIfUserExists(nuid) == 1 or 2:
            #check if the new id created is already in database
            print("User ID already in use! Please enter a different one.\n")
            newUser()
        else:
            name = input("Enter your name: ")
            lp = input("Enter your vehicle's license plate: ")
            print("Are you currently an active driver? 0 for no, 1 for yes: ")
            dm = helper.get_choice([0,1])

            query = "INSERT INTO Driver (driverID, name, licensePlate, driverMode, driverRating) VALUES (%s, %s, %s, %s, %s)"
            values = [(nuid, name, lp, dm, 0.0)]

            cur_obj.executemany(query, values)
            conn.commit()

            driverCheck = cur_obj.fetchall()
            helper.pretty_print(driverCheck)

            print("Successfully created driver account!\n")
            driverUser(nuid)
    if choice == 2:
        nuid = input("Create your user id:\n ")
        if nuid == 0:
            #username cannot be a singular 0 as that is what is used to exit
            print("User ID cannot be 0!\n")
            newUser()
        elif checkIfUserExists(nuid) == 1 or 2:
            #check if the new id created is already in database
            print("User ID already in use! Please enter a different one.\n")
            newUser()
        else:
            name = input("Enter your name: ")

            query = "INSERT INTO Rider (riderID, name) VALUES (%s, %s)"
            values = [(nuid, name)]

            cur_obj.executemany(query, values)
            conn.commit()

            riderCheck = cur_obj.fetchall()
            helper.pretty_print(riderCheck)

            print("Successfully created rider account!\n")
            riderUser(nuid)

# driver user portal
def driverUser(id):
    print(id + "'s DRIVER PORTAL\n")
    print("OPTIONS\n~View Rating: 1\n~View Rides: 2\n~Activate/Deactivate Driver Mode: 3\n~Log Out: 0\n")
    input = helper.get_choice([0,1,2,3])

    if input == 0:
        print("Goodbye!\n")
        #break
    if input == 1:
        driverViewRatings(id)
    if input == 2:
        viewRides(id)
        driverUser(id)
    if input == 3:
        driverMode(id)

#rider user portal
def riderUser(id):
    print(id + " RIDER PORTAL\n")
    print("OPTIONS\n~View Rides: 1\n~Find a Driver: 2\n~Rate My Driver: 3\n~Log Out: 0\n")
    input = helper.get_choice([0,1,2,3])

    if input == 0:
        print("Goodbye!\n")
        #break
    if input == 1:
        viewRides(id)
        riderUser(id)
    if input == 2:
        findADriver(id)
    if input == 3:
        rateDriver(id)
        riderUser(id)

def driverViewRatings(id):
    print("Viewing ratings for " + id + "\n")
    query = "SELECT driverRating FROM Driver WHERE driverID LIKE '" + id + "';"
    cur_obj.execute(query)
    result = cur_obj.fetchall()[0]
    driverRating = tupToStr(result)
    print("Your current rating: " + driverRating + " stars.\n")
    driverUser(id)

def viewRides(id):
    print("Viewing rides for " + id + "\n")
    query = "SELECT * FROM Ride WHERE driverID OR riderID LIKE '" + id + "';"
    rides = cur_obj.execute(query)
    hasRides = cur_obj.fetchall()
    if hasRides:
        helper.pretty_print(hasRides)
    else:
        print("No rides in database!\n")
    #driverUser(id)

def driverMode(id): #has issues
    print("Editing driver mode for " + id + "\n")
    print("Are you sure you want to change your driver mode? [1: Yes, 2: No]\n")
    input = helper.get_choice([0,1,2])
    msg = " "

    if input == 1:
        query = "SELECT driverMode FROM Driver WHERE driverID LIKE '" + id + "';"
        cur_obj.execute(query)
        dmode = cur_obj.fetchall()[0]

        print(str(dmode))

        nmode = str(not dmode) #flips 1 to 0 and 0 to 1

        query = "UPDATE Driver SET driverMode = " + nmode + " WHERE driverID LIKE '" + id + "';"
        cur_obj.execute(query)
        conn.commit()
        print("Driver mode has been changed to: " + nmode + "\n")
        driverUser(id)
    if input == 2:
        print("\n")
        driverUser(id)

def findADriver(id):
    print("Finding a driver for " + id + "\n")
    query = "SELECT driverID FROM Driver WHERE driverMode = 1 ORDER BY Rand() LIMIT 1;"
    cur_obj.execute(query)
    result = cur_obj.fetchall()[0]
    dID = tupToStr(result)

    query = "SELECT * FROM Driver WHERE driverID = '" + dID + "';"
    driverInfo = cur_obj.execute(query)
    dInfo = cur_obj.fetchall()
    print("Your assigned driver: \n")
    helper.pretty_print(dInfo)

    pUp = input("Insert where you want to be picked up from: ")
    dOff = input("Insert where you want to be dropped off to: ")

    rID = random.randrange(1, 999)

    query = "INSERT INTO Ride (rideID, driverID, riderID, pickUp, dropOff, rideRating) VALUES (%s, %s, %s, %s, %s, %s)"
    values = [(rID, dID, id, pUp, dOff, 0.0)]

    cur_obj.executemany(query, values)
    conn.commit()

    result = cur_obj.fetchall()
    print("Your ride info: ")
    helper.pretty_print(result)
    riderUser(id)


def rateDriver(id):
    print("Rating the driver for " + id + "\n")
    query = "SELECT * FROM Ride WHERE riderID = '" + id + "' LIMIT 1;"
    rides = cur_obj.execute(query)
    hasRides = cur_obj.fetchall()
    if hasRides:
        helper.pretty_print(hasRides)
        print("Is this the ride you want to rate? Y: 1 N: 2")
        userChoice = helper.get_choice([1,2])
        if userChoice == 1:
            query = "SELECT rideID FROM Ride WHERE riderID = '" + id + "' LIMIT 1;"
            cur_obj.execute(query)
            rideID =  cur_obj.fetchall()[0]
            strRideID = tupToStr(rideID)
            rating(id,strRideID)
        if userChoice == 2:
            rideID = input("Insert ride ID you want to rate for: ")
            rating(id,rideID)
    else:
        print("No rides in database!\n")

def rating(id, rID):
    query = "SELECT driverID FROM Ride WHERE rideID = '" + rID + "';"
    cur_obj.execute(query)
    hasDriver = cur_obj.fetchall()[0]
    driver = tupToStr(hasDriver)
    ratingNum = 0.0
    if hasDriver:
        print('''How will you rate your driver?
        1: 1.0 stars
        2: 1.5 stars
        3: 2.0 stars
        4: 2.5 stars
        5: 3.0 stars
        6: 3.5 stars
        7: 4.0 stars
        8: 4.5 stars
        9: 5.0 stars''')
        userChoice = helper.get_choice([1,2,3,4,5,6,7,8,9])
        if userChoice == 1:
            ratingNum = 1.0
        if userChoice == 2:
            ratingNum = 1.5
        if userChoice == 3:
            ratingNum = 2.0
        if userChoice == 4:
            ratingNum = 2.5
        if userChoice == 5:
            ratingNum = 3.0
        if userChoice == 6:
            ratingNum = 3.5
        if userChoice == 7:
            ratingNum = 4.0
        if userChoice == 8:
            ratingNum = 4.5
        if userChoice == 9:
            ratingNum = 5.0

        query = "SELECT driverRating FROM Driver WHERE driverID LIKE '" + driver + "';"
        cur_obj.execute(query)
        result = cur_obj.fetchall()[0]
        dRating = tupToStr(result)
        dRatingAsFloat = float(dRating)

        updatedRating = str((dRatingAsFloat + ratingNum)/2)

        query = "UPDATE Driver SET driverRating = " + updatedRating + " WHERE driverID LIKE '" + driver + "';"
        cur_obj.execute(query)
        conn.commit()
        print("You have rated the driver: " + driver + "\n")
    else:
        print("Driver with that id was not found!\n")



startScreen()

#print(conn)
conn.close
