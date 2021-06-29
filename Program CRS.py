import mysql.connector as sql
import pandas as pd

db=sql.connect(
    host="localhost",
    user="root",
    passwd='root',
    database='crs')
mycursor=db.cursor()

seq=1
while seq==1:
    print('         ╔═╗╔═╗╦═╗╦╔═  ╦  ╔═╗╔╗╔╔═╗  ')
    print('         ╠═╝╠═╣╠╦╝╠╩╗  ║  ╠═╣║║║║╣   ')
    print('         ╩  ╩ ╩╩╚═╩ ╩  ╩═╝╩ ╩╝╚╝╚═╝  ')
    print('             CAR RENTAL COMPANY               ')
    print('\n Welcome to Park Lane Car Rental Company!\n\nPlease choose your option below:')
    print('\n\t1. Book or Reserve a car\n\t2. Cancel a reservation\n\n\n0. Staff Login\n')
    sel=input('Select your option: ')
    
    if sel=='0':
        print('\n\n\n\n\n\n \tSTAFF LOGIN \n\n Enter staff credentials:')
        user=input('Username: ')
        if user=='staff':
            pas=input('Password: ')
            if pas=='park1':
                print('\n\n\t\tWelcome Staff\n')
                seq1=1
                while seq1==1:
                    print('Choose options below:\n1. View Customers\n2. View vehicles\n3. View billing\n4. View Booking Details')
                    print('\n5. Register returned car\n6. Generate Billing invoice' )
                    sele=input('\n Enter choice: ')
                    if sele=='1':
                        mycursor.execute("SELECT * FROM customer")
                        cus=mycursor.fetchall()
                        #cusdf=pd.DataFrame(cus)  NOT SURE BOUT THIS
                        print(cus)
                        con=input('\nPress y to return back to menu or press any key to log out:  ')
                        if con=='y':
                            continue
                        else:
                            break
                    
            else:
                print('\nIncorrect password.\n')
                seq-=1
        else:
            print('\nunknown credentials.\nPlease Try Again.\n')
            seq-=1
        