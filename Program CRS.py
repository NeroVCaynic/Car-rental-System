#packages imported

import mysql.connector as sql
import pandas as pd


#database connection initialized 

db = sql.connect(
    host="localhost",
    user="root",
    passwd="pass",
    database='crs'
    )

mycursor = db.cursor()


#function creations

#creates empty space
def clear():
  for _ in range(50):
     print()
    
#logo print function
def logo():
    print('         ╔═╗╔═╗╦═╗╦╔═  ╦  ╔═╗╔╗╔╔═╗  ')
    print('         ╠═╝╠═╣╠╦╝╠╩╗  ║  ╠═╣║║║║╣   ')
    print('         ╩  ╩ ╩╩╚═╩ ╩  ╩═╝╩ ╩╝╚╝╚═╝  ')
    print('             CAR RENTAL COMPANY               ')

#combining the above 2 functions
def logoPrint():
    clear()
    logo()

#dataframe function
def df(data, col):
    result = pd.DataFrame(data, columns=col)
    results = result.to_string(index=False)
    print(results)


#visual functions
#customers
def showCustomer():
    mycursor.execute("SELECT * FROM customer;")
    data = mycursor.fetchall()
    head = ["Diver's licence", "Full Name", "Phone Number", "Address", " MEM_ID"]
    df(data,head)

#Vehicles
def showVehicles():
    mycursor.execute("SELECT * FROM car;")
    data = mycursor.fetchall()
    head = ["REG_NO","MODEL NAME", "MAKE", "CAR CATEGORY", "AVAILABILITY", "COST PER DAY IN KWD"]
    df(data,head)

#Billing
def showBills():
    mycursor.execute("SELECT * FROM bills;")
    data = mycursor.fetchall()
    head = ["BILL ID","BILL DATE", "BILL STATUS", "TOTAL AMOUNT", "BOOKING ID"]
    df(data,head)

#booking details
def showBooking():
    mycursor.execute("SELECT * FROM booking_details;")
    data = mycursor.fetchall()
    head = ["BOOKING ID", "FROM DT", "RET_DT", "AMOUNT", "REG_NO", "Diver's licence", "MEM_ID", "ACT_RET_DT"]
    df(data,head)

#staff View input statements
def ViewStaff(value):
    if value == "1":
        clear()
        logo()
        showCustomer()
    elif value == "2":
        clear()
        logo()
        showVehicles()
    elif value == "3":
        clear()
        logo()
        showBills()
    elif value == "4":
        clear()
        logo()
        showBooking()
    elif value == "5":
        clear()
        logo()
        pass
    elif value == "6":
        clear()
        logo()
        pass
    else:
        print("Wrong Entry")

#Main Menu
def MainMenu():
    logoPrint()
    print("\n\n\n Choose the following: ")
    print("\t1.Staff\n\t2.Customers\n\t3.Close")

#staff 
def staff():
    logoPrint()
    print('\n\n\n\n\n      STAFF LOGIN\n\nEnter staff credentials:')
    user = input('\tUsername: ')
    if user == 'staff':
        passwd = input('\tPassword: ')
        if passwd == 'staff':
            while True:
                logoPrint()
                print('\n\n\t\tWelcome Staff\n')
                print("\nChoose options below:\n1. View Customers\n2. View vehicles\n3. View billing"
                    "\n4. View Booking Details\n5. Register returned car\n6. Generate Billing invoice" )
                value = input('\n Enter choice: ')
                ViewStaff(value)
                Continue = input('\nPress y to return back to menu or press any key to log out:  ')
                if Continue == 'y':
                    continue
                else:
                    break      
        else:
            print('\nIncorrect password.\n')
    else:
        print('\nunknown credentials.\nPlease Try Again.\n')      

#Main Loop
def Main():
    while True:
        MainMenu()
        Num = input(": ")
        if Num == "1":
            staff()
        elif Num == "2":
            pass
        elif Num == "3":
            break
        else:
            print("ERROR WRONG ENTRY")


#Main
Main()