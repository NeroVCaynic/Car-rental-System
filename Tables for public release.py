import mysql.connector
import pandas as pd

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="sheikkhokon1435",
  database='crs'
   )

mycursor = db.cursor()
'''
mycursor.execute('create database if not exists crs;')
db.commit()

mycursor.execute('use crs;')

#customer table
mycursor.execute('create table if not exists CUSTOMER(DL char(15) primary key,FULL_NAME varchar(25) not null,PH_NO char(18) not null,ADDRESS varchar(25) not null,MEM_ID char(5) not null);')
db.commit()

#car 
mycursor.execute('create table if not exists CAR(REG_NO char(8) not null primary key,MODEL_NAME varchar(25) not null,MAKE varchar(15),CAR_CATEGORY varchar(15) not null,AVAILABILITY char(1) not null,COST_PER_DAY_IN_KWD int(3));')
db.commit()

#Booking_Details
mycursor.execute('create table if not exists BOOKING_DETAILS(BOOKING_ID int(5) primary key,FROM_DT date NOT NULL,RET_DT date NOT NULL,AMOUNT double(7,2) NOT NULL,REG_NO char(8) NOT NULL,DL char(15) NOT NULL,MEM_ID int(5) NOT NULL,ACT_RET_DT date NOT NULL,Insurance char(4) not null);')
db.commit()

#billing_details
mycursor.execute('create table if not exists BILLS(BILL_ID int(6) primary key,BILL_DATE DATE NOT NULL,BILL_STATUS CHAR(1) NOT NULL,TOTAL_AMOUNT double(7,2) NOT NULL,BOOKING_ID int(5) NOT NULL);')
db.commit()

#car rental insurance
mycursor.execute('CREATE TABLE if not exists INSURANCE(INSURANCE_CODE CHAR(4) PRIMARY KEY,INSURANCE_NAME VARCHAR(30),COVERAGE_TYPE VARCHAR(50) NOT NULL,COST_PER_DAY_IN_KWD int(4) NOT NULL);')
db.commit()

#inserts
ins='Insert into CUSTOMER values(%s,%s,%s,%s,%s);'
val = [
  ('260021005123','M. Abdul Rahman','+965 55944213','Kuwait City,KW','05123'),
  ('2388704','Abdullah Abdul Hashim','+971 77261822','Ras Al Khaimah,UAE','88704'),
  ('F100W21C35812','Thomas John Ellis','+44 078 0558 3105','Barnes Avenue,London','35812'),
  ('361907456','Gabriel Iglesias','+1 214 558 3039','Mas Drive Dallas,TX','07456'),
  ('238018471907','Trevor Noah','+27 083 918 8657','Nelson Mandela Drive,SA','71907'),
  ('303071500331','M. Ali Al-Helal','+965 60070573','Yarmouk 56th st.,KW','00331' ),
  ('260021004572','Ahmad Farhat','+965 55321475','Hawally Tunis St.,KW','04572')
  ]

mycursor.executemany(ins,val)
db.commit()



ins2='Insert into CAR values(%s,%s,%s,%s,%s,%s);'
val2 = [
  ('15/23402','Escalade SE 2020','Cadillac','SUV','n',45),
  ('19/61623','Autobiography 2019','Land Rover','SUV','n',61),
  ('3/12402','Mustang 2020','Ford','Sport','n',70),
  ('8/9823','Corvette Stingray 2021','GMC','Sport','n',75),
  ('30/69422','ES250 2019','Lexus','Sedan','n',50),
  ('93/14042','XF 260 2021','Jaguar','Sedan','n',60),
  ('2/6918','Model 3 2021','Tesla','Sedan','n',83),
  ('1/20021','Huracan STO 2018','Lamborghini','Sports','y',95),
  ('23/21003','Patrol LTZ 2020','Nissan','SUV','y',41),
  ('22/10030','Phantom 2017','Rolls Royce','Sedan','y',85),
  ('50/50501','Defender V8 2016','Land Rover','SUV','y',40),
  ('12/20013','Challenger 2019','Dodge','Sport','y',74),
  ('22/10203','California 2017','Ferrari','Sport','y',90),
  ('3/1024','AMG G63 2021','Mercedes','SUV','y',85),
  ('70/2102','S-Class 2020','Mercedes','Sedan','y',80),
  ('2/1024','240 Turbo 1994','Volvo','Sedan','y',17)]

mycursor.executemany(ins2,val2)
db.commit()

ins3='Insert into INSURANCE values(%s,%s,%s,%s);'
val3 = [
  ('T001','COLLISION DAMAGE WAIVER','Covers theft and damage to the rental car',5),
  ('T002','LIABILITY PROTECTION', 'Covers damage done to others',8),
  ('T003','PERSONAL ACCIDENT INSURANCE', 'Covers medical costs for driver and passengers',10),
  ('T004','PERSONAL EFFECTS COVERAGE', 'Covers theft of personal belongings',9),
  ('NONE','NO INSURANCE', 'Does not cover any loss or damages.',0)]
mycursor.executemany(ins3,val3)
db.commit()

#Serial
mycursor.execute('create table if not exists Serial(Category varchar(15) primary key,number int(5) not null);')
vals = [('Booking_details',1302),('Bills',1102),('Mem_id',3021)]
vals2='Insert into serial values(%s,%s);'
mycursor.executemany(vals2,vals)
db.commit()
'''
mycursor.execute("select number from serial where category='booking_details';")
BookID1=pd.DataFrame(mycursor.fetchall(), columns=["MEM_ID"])
print(BookID1.loc[0,"MEM_ID"])
#ExistCus.loc["MEM_ID"]

