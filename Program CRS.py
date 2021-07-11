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

#Add/Delete a car
def CarModify():
    print('1. Add a car\n2. Delete a car\n')
    UserInput = input('\n Enter choice: ')
    if UserInput == '1':
        reg = input('Enter registration number: ')
        mdl = input('Enter model name: ')
        mke = input('Enter make: ')
        cc = input('Enter car category: ')
        av = input('Enter car availability: ')
        cpd = int(input('Enter cost per day in KWD: '))
        list1 = [reg,mdl,mke,cc,av,cpd]
        lis = [reg]
        comm = 'select * from car where reg_no=%s'
        coIns = 'insert into car values(%s,%s,%s,%s,%s,%s)'
        mycursor.execute(comm,lis)
        mycursor.fetchall()
        count = mycursor.rowcount
        if count >= 1:
            print('\nCar already exists!\n')
        else:
            mycursor.execute(coIns,list1)
            db.commit()
            print('\nCar has been added successfully\n') 
            
        
    elif UserInput=='2':
        reg=input('Enter Registration number of the car to be deleted: ')
        lis=[reg]
        comm='select * from car where reg_no=%s'
        mycursor.execute(comm,lis)
        mycursor.fetchall()
        count=mycursor.rowcount
        if count==1:
            Del='Delete from car where reg_no=%s'
            mycursor.execute(Del,lis)
            db.commit()
            print('\nCar deleted successfully\n')
        else:
            print('\nCar does not exist!\n') 
    
    else:
        print('\nWrong input please try again.\n')

#booking return function
def BookingReturn():
    Book = input("Enter Booking ID: ")
    mycursor.execute("SELECT * FROM booking_details WHERE BOOKING_ID = %s;",(Book,))
    result = mycursor.fetchall()
    row = mycursor.rowcount
    if row == 1:
        returnDate = input("Enter return date (YYYY-MM-DD): ")
        mycursor.execute('Select reg_no from booking_details where booking_id= %s',(Book,))
        regno1=mycursor.fetchall()
        regno2=regno1[0]
        regno=regno2[0]
        mycursor.execute("UPDATE booking_details SET ACT_RET_DT = %s WHERE BOOKING_ID = %s ",(returnDate, Book,))
        mycursor.execute("UPDATE car SET AVAILABILITY = 'y' WHERE reg_no = %s ",(regno,))
        mycursor.execute('SELECT COST_PER_DAY_IN_KWD FROM car WHERE reg_no = %s',(regno,))
        rate1=mycursor.fetchall()
        #bringing out the value from the list
        rate2=rate1[0]
        rate=rate2[0]
        mycursor.execute('SELECT ACT_RET_DT-FROM_DT from booking_details WHERE BOOKING_ID= %s',(Book,))
        TotDur1=mycursor.fetchall()
        TotDur2=TotDur1[0]
        TotDur=TotDur2[0]
        if TotDur>=1:
            mycursor.execute('SELECT ACT_RET_DT-RET_DT from booking_details WHERE BOOKING_ID= %s',(Book,))
            late1=mycursor.fetchall()
            late2=late1[0]
            late=late2[0]
            #final amount with late fees which is 10% of rate
            amount=rate*TotDur+(10/100*rate*late)
            mycursor.execute("UPDATE booking_details SET AMOUNT = %s where BOOKING_ID= %s ",(amount, Book,))
            db.commit()
            print('\n\t Operation completed successfully!\n')
        else:
            print('\n\t Something went wrong!\n Please check the return date and try again.\n')
                            
    else:
        print("\n\t ERROR! \n\tCar doesn't exist!\n\n please try again.")

#Generate Billing
def BillGen():
    print('d')
        
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
        CarModify()
        
    elif value == "6":
        clear()
        logo()
        BookingReturn()
    
    elif value == "7":
        clear()
        logo()
        BillGen()
    
    else:
        print("\nWrong Entry")

#Main Menu
def MainMenu():
    logoPrint()
    print('\n Welcome to Park Lane Car Rental Company!\n\nPlease choose your option below:')
    print('\n\t1. Book or Reserve a car\n\t2. Cancel a reservation\n\n\n0. Staff Login\n')

#CustomerSearch
    
    #---------->Are you fucking retarded searching a customer by their full name??? use DL instead. <----------
    
def CustomerSearch():
    name = input("Type your name: ")
    mycursor.execute("SELECT * FROM customer WHERE FULL_NAME LIKE CONCAT('%', %s, '%')",(name,))
    result = mycursor.fetchall()
    count = mycursor.rowcount
    if count == 1:
        print(result,"\n")
    elif count > 1:
        print("there are more than one Record avaliable")
    else:
        print("No Records avaliable")
    input("press enter to try again")

        
        
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
                    "\n4. View Booking Details\n5. Add/Delete a vehicle to/from the fleet \n\n6. Register returned car\n7. Generate Billing invoice" )
                value = input('\n Enter choice: ')
                ViewStaff(value)
                Continue = input('\nPress y to return back to menu or press any key to log out:  ')
                if Continue == 'y':
                    continue
                else:
                    break      
        else:
            print('\nIncorrect password.\nPress enter to try again.\n')
            input()
    else:
        print('\nUnknown credentials.\nPress enter to try again.\n')
        input()

#Main Loop
def Main():
    while True:
        MainMenu()
        Num = input(": ")
        if Num == "0":
            staff()
        elif Num == "1":
            #CustomerSearch()
            pass
        elif Num == "2":
            pass
        else:
            print("\t ERROR! \n\tWRONG ENTRY\n\n press enter to try again")
            input()


#Main
Main()