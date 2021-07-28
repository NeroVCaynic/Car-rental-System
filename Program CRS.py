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
            #creates the bill
            mycursor.execute("select number from serial where category='Bills';")
            BillID1=mycursor.fetchall()
            BillID2=BillID1[0]
            BillID=BillID2[0]
            mycursor.execute("update serial set number=number+1 where category='Bills';")
            BillStat='n'
            mycursor.execute('select insurance from booking_details where booking_id=%s;',(Book,))
            ins1=mycursor.fetchall()
            ins2=ins1[0]
            ins=ins2[0]
            if ins=='n':
                mycursor.execute("insert into bills values(%s,%s,%s,%s,%s);",(BillID,returnDate,BillStat,amount,Book,))
                db.commit()
                print('\n\t Operation completed successfully!\n')
                print('Billing ID is ',BillID)
            
            else:
                mycursor.execute('select cost_per_day_in_kwd from insurance where insurance_code=%s;',(ins,))
                insCost1=mycursor.fetchall()
                insCost2=insCost1[0]
                insCost=insCost2[0]
                AmountWithIns=amount+(insCost*TotDur)
                mycursor.execute("insert into bills values(%s,%s,%s,%s,%s);",(BillID,returnDate,BillStat,AmountWithIns,Book,))
                db.commit()
                print('\n\t Operation completed successfully!\n')
                print('Billing ID is ',BillID)
            
        else:
            print('\n\t Something went wrong!\n Please check the return date and try again.\n')
                            
    else:
        print("\n\t ERROR! \n\tCar doesn't exist!\n\n please try again.")

#Generate Billing
def BillGen():
    Book=input('Enter Booking ID: ')
    mycursor.execute("select * from bills where booking_id=%s;",(Book,))
    mycursor.fetchall()
    count = mycursor.rowcount
    if count == 1:
        #required info from bill table 
        mycursor.execute("select bill_id,bill_date,TOTAL_AMOUNT,bill_status from bills where booking_id=%s;",(Book,))
        BillInfo1=mycursor.fetchall()
        BillID2=BillInfo1[0]
        #BillID
        BillID=BillID2[0]
        BillDate2=BillInfo1[0]
        #Bill date
        BillDate=BillDate2[1]
        TotAm2=BillInfo1[0]
        #total amount
        TotAm=TotAm2[2]
        BillStat2=BillInfo1[0]
        #billing status
        BillStat=BillStat2[3]
        #required info from booking_details
        mycursor.execute('SELECT ACT_RET_DT-FROM_DT from booking_details WHERE BOOKING_ID= %s',(Book,))
        TotDur1=mycursor.fetchall()
        TotDur2=TotDur1[0]
        #Total Duration
        TotDur=TotDur2[0]
        mycursor.execute('Select reg_no from booking_details where booking_id= %s',(Book,))
        regno1=mycursor.fetchall()
        regno2=regno1[0]
        #Registration Number
        regno=regno2[0]
        mycursor.execute('SELECT ACT_RET_DT-RET_DT from booking_details WHERE BOOKING_ID= %s',(Book,))
        late1=mycursor.fetchall()
        #late days
        late2=late1[0]
        late=late2[0]
        mycursor.execute('select insurance from booking_details where booking_id=%s;',(Book,))
        ins1=mycursor.fetchall()
        ins2=ins1[0]
        #insurance
        ins=ins2[0]
        mycursor.execute('select model_name from car where reg_no=%s;',(regno,))
        car1=mycursor.fetchall()
        car2=car1[0]
        #car name
        car=car2[0]
        mycursor.execute('select DL from booking_details where booking_id=%s;',(Book,))
        DL1=mycursor.fetchall()
        DL2=DL1[0]
        #driving license 
        DL=DL2[0]
        #customer table info
        mycursor.execute('select FULL_NAME,PH_NO,MEM_ID from customer where DL=%s;',(DL,))
        CusInfo1=mycursor.fetchall()
        fname2=CusInfo1[0]
        #fullname
        fname=fname2[0]
        pnum2=CusInfo1[0]
        #phone number
        pnum=pnum2[1]
        '''mid2=CusInfo1[0]
        #mem_id
        mid=mid2[2]'''
        clear()
        print('+----------------------------------------------------+')
        logo()
        print('\n\n░░░░░░░░░░░░░░ BILLING INVOICE ░░░░░░░░░░░░░░ ')
        print('+----------------------------------------------------+')
        print('\nDate: ',BillDate,'\t\t Invoice no. : ',BillID,'\n\nBill To: ',fname,' ',DL,'\nPhone no.: ',pnum)
        print('\n Bill:\n+----------------------------------------------------+')
        print(car,'Reg no.',regno,'\nFor total duration of: ',TotDur,' days.\n',late,' days late.')
        print('\nInsurance: ',ins)
        print('+----------------------------------------------------+')
        print('\t\tTotal Amount:',TotAm)
        print('+----------------------------------------------------+')
        print('\n*Note:\n#Vehicle returned after due date will have 10%')
        print('charged from original cost as *late fees*.\n#Fees once paid cannot be refunded.')
        print('+----------------------------------------------------+')
        if BillStat=='n':
            con=input('\n Is the fees paid? (y/n): ')
            if con=='y':
                mycursor.execute("update bills set bill_status='y' where booking_id=%s;",(Book,))
                db.commit()
                print('Successfully recorded.')
                
    else:
        print('\n\t Bill not found.\n\t Try again.\n')
        
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

#book
def BookOrReserve():
    logoPrint()
    mycursor.execute("SELECT MAKE,MODEL_NAME,CAR_CATEGORY, COST_PER_DAY_IN_KWD FROM car WHERE AVAILABILITY LIKE 'y'")
    result = pd.DataFrame(mycursor.fetchall(), columns=["MAKE","MODEL","CATEGORY","COST_PER_DAY_IN_KWD"])
    print('\nAvailable cars:\n')
    print(result)
    loc = int(input('\nSelect a car (0,1,2,3): '))
    logoPrint()
    re = result.iloc[loc]
    print('\nYou have chosen: ')
    for x in re:
        print(x, end=' ')
    print(' \n')
    mycursor.execute("SELECT INSURANCE_NAME,COVERAGE_TYPE,COST_PER_DAY_IN_KWD FROM insurance;")
    result2 = pd.DataFrame(mycursor.fetchall(), columns=["INSURANCE", "COVERAGE_TYPE", "COST_PER_DAY_IN_KWD"])
    print(result2)
    loc2 = int(input('Add an insurance: '))
    logoPrint()
    re2 = result2.iloc[loc2]
    for x in re2:
        print(x, end=' ')
    print('\n\n')
    while True:
        DL = input("Enter your Driver's License: ")
        mycursor.execute("select DL from customer;")
        DLchck=mycursor.fetchall()
        DLcheck=list()
        for x in DLchck:
            temp=x[0]
            DLcheck.append(temp)
        if DL in DLcheck:
            mycursor.execute("select * from customer where DL=%s;",(DL,))
            info=mycursor.fetchall()
            ExistCus= pd.DataFrame(info,columns=["DL","FULL NAME","PHONE NO","ADDRESS","MEM_ID"])
            print(ExistCus)
            confirm=input('\n\n Is the above information correct? y/n : ')
            if confirm=='y':
                infoFin=info[0]
                mycursor.execute("select year(curdate());")
                CurYear1=mycursor.fetchall()
                CurYear2=CurYear1[0]
                CurYear=CurYear2[0]
                takeDD = input("enter pick up day(DD): ")
                takeMM = input("enter pick up month(MM): ")
                takeYYY = str(CurYear)
                takeinDT = takeYYY+"-"+takeMM+"-"+takeDD
                returnDD = input("enter return day(DD): ")
                returnMM = input("enter return month(MM): ")
                returnYYY = str(CurYear)
                returnDT = returnYYY + "-" + returnMM+ "-" + returnDD
        else:
            name = input("Enter your Full name: ")
            address = input("Enter your address: ")
            print("Enter your phone number with country code")
            phNo = input(": ")
            mycursor.execute("select year(curdate());")
            CurYear1=mycursor.fetchall()
            CurYear2=CurYear1[0]
            CurYear=CurYear2[0]
            takeDD = input("enter pick up day(DD): ")
            takeMM = input("enter pick up month(MM): ")
            takeYYY = str(CurYear)
            takeinDT = takeYYY+"-"+takeMM+"-"+takeDD
            returnDD = input("enter return day(DD): ")
            returnMM = input("enter return month(MM): ")
            returnYYY = str(CurYear)
            returnDT = returnYYY+"-"+returnMM+"-"+returnDD
            mycursor.execute("select number from serial where category='Mem_id';")
            MemID1=mycursor.fetchall()
            MemID2=MemID1[0]
            #membership id
            MemID=MemID2[0]
            mycursor.execute("update serial set number= number + 1 where category='Mem_id';")
            db.commit()
            if len(phNo) >= 11:
                if len(name) >= 1:
                    phNo = '+'+phNo
                    if len(takeDD) == 2 and len(takeMM) == 2:
                        if len(returnDD) == 2 and len(returnMM) == 2:
                            print("\nDriver's license: ",DL,"\nFull Name: ",name,"\nPhone Number: ",phNo,"\nAddress: ",address)
                            Endloop = input("Is the above information correct? y/n:  ")
                            if Endloop == 'y':
                                mycursor.execute("INSERT INTO customer (DL, FULL_NAME, PH_NO, ADDRESS, MEM_ID) VALUES (%s,%s,%s,%s,%s)",(DL,name,phNo,address,MemID,))
                                mycursor.execute("SELECT * FROM customer;")
                                print(mycursor.fetchall())
                                model = re.loc["MODEL"]
                                mycursor.execute("UPDATE car SET AVAILABILITY = 'n' WHERE MODEL = %s", (model,))
                                mycursor.execute("SELECT * FROM car;")
                                print(mycursor.fetchall())
                                db.commit()  
                            else:
                                continue 
                        else:
                            print("Invalid return date")
                    else:
                        print("Invalid take out date")
                else:
                    print('invalid Entry')
            else:
                print('invalid phone number')
        mycursor.execute("INSERT INTO customer (DL, FULL_NAME, PH_NO, ADDRESS, MEM_ID) VALUES (%s,%s,%s,%s,%s)",(DL,name,phNo,address,MemID,))
        mycursor.execute("SELECT * FROM customer;")
        print(mycursor.fetchall())
        model = re.loc["MODEL"]
        mycursor.execute("UPDATE car SET AVAILABILITY = 'n' WHERE MODEL = %s", (model,))
        mycursor.execute("SELECT * FROM car;")
        print(mycursor.fetchall())
        db.commit()

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
            BookOrReserve()
        elif Num == "2":
            pass
        else:
            print("\t ERROR! \n\tWRONG ENTRY\n\n press enter to try again")
            input()


#Main
Main()