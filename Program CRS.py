#packages imported

import mysql.connector as sql
import pandas as pd


#database connection initialized 

db = sql.connect(
    host="localhost",
    user="root",
    passwd="root",
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
    print('             CAR RENTAL COMPANY               \n')
    print('      "Synonymous with style and luxury"   \n')

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
    print()
    mycursor.execute("SELECT * FROM customer;")
    data = mycursor.fetchall()
    head = ["Driver's licence", "Full Name", "Phone Number", "Address", " MEM_ID"]
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
    head = ["BOOKING ID", "FROM DT", "RET. DT", "AMOUNT", "REG. NO", "Driver's license", "MEM_ID", "ACT_RET_DT"]
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
        print("\nWrong Entry")

#Main Menu
def MainMenu():
    logoPrint()
    print('\n Welcome to Park Lane Car Rental Company!\n\nPlease choose your option below:')
    print('\n\t1. Book or Reserve a car\n\t2. Cancel a reservation\n\n\n0. Staff Login\n')

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
                    "\n4. View Booking Details\n\n5. Register returned car\n6. Generate Billing invoice" )
                value = input('\n Enter choice: ')
                ViewStaff(value)
                Continue = input('\nPress y to return back to menu or press any key to log out:  ')
                if Continue == 'y':
                    continue
                else:
                    break      
        else:
            print('\nIncorrect password.\nPress any key to try again.\n')
            er=input()
    else:
        print('\nUnknown credentials.\nPress any key to try again.\n')
        er=input()

#Main Loop
def Main():
    while True:
        MainMenu()
        Num = input(": ")
        if Num == "0":
            staff()
        elif Num == "1":
            pass
        elif Num == "2":
            pass
        else:
            print("\t ERROR! \n\tWRONG ENTRY\n\n press any key to try again")
            er=input()


#Main
Main()