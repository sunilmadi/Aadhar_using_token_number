import sqlite3 as sq 
from pymongo import MongoClient
from Modules_Packages.aadhar_project import otpcheck as otpt,sms1 as sma,emaila as ema
def func():
    print("continue aadhar registration using token number function")   
    token1=int(input("ENTER YPUR TOKEN NUMBER: "))
    pancard1=input("enter your pancard number: ")
    t1=readtokendb(token1,pancard1)
    if t1==0:
        print("INVALID TOKEN/PANCARD COMBINATION")
        return
    else:
        t2=readpandb(pancard1)
        if t2==0:
            print("PANCARD NOT IN PAN DATABASE. REGISTER FOR PANCARD FIRST USING OPTION 1")
            return
        else:
            t3=readaadhardb(t1[1],t1[2],t2[1],t2[2],t2[3],t2[4],t2[5],t2[6],token1)
            return   

def readtokendb(token1,pancard1):
    conn=sq.connect("pancard.db")
    query1="SELECT * FROM TOKEN WHERE TOKEN={0} AND PANNUM='{1}' AND TOEKN_USED='N'"
    query=query1.format(token1,pancard1)
    cur=conn.execute(query)
    cursor=cur.fetchall()
    if len(cursor)==0:
        conn.close()
        return 0
    else:
        conn.close()
        for i in cursor:
            return i
def readpandb(pancard1):
    conn=sq.connect("pancard.db")
    query1="SELECT * FROM PANCARD WHERE PANNUM='{0}'"
    query=query1.format(pancard1)
    cur=conn.execute(query)
    cursor=cur.fetchall()
    if len(cursor)==0:
        conn.close()
        return 0
    else:
        conn.close()
        for i in cursor:
            return i
def readaadhardb(pancard1,aadhar1,name1,dob1,age1,city1,state1,phone1,token1):
    print(pancard1,aadhar1,name1,dob1,age1,city1,state1,phone1)
    client=MongoClient('localhost',27017)
    db=client['AADHAR']
    aadharinfo=db.AADHARINFO 
    cursor=aadharinfo.find_one({'AADHARNUM':aadhar1})
    rt=otpt.otpcheck()
    if rt==1:
        if cursor is None:
            cursor1=aadharinfo.insert_one({'PANNUM':pancard1,'NAME':name1,'DOB':dob1,'AGE':age1,'CITY':city1,'STATE':state1,'PHONENUM':phone1,'AADHARNUM':aadhar1})
            if cursor1.acknowledged:
                sma.sendsms(aadhar1,'N')
                email1=input("enter your email :")
                ema.emailfunc(email1,aadhar1,'N')
                updatetokendb(token1,pancard1,aadhar1)
                return
        else:
            print("AADHAR NUMBER AREADY EXISTS IN AADHAR DATABASE")
            sma.sendsms(aadhar1,'E')
            email1=input("enter your email :")
            ema.emailfunc(email1,aadhar1,'E')
            updatetokendb(token1,pancard1,aadhar1)
            return
    else:
        print("invalid OTP or time out")
        return
def updatetokendb(token1,pancard1,aadhar1):
    conn=sq.connect("pancard.db")
    query1="UPDATE TOKEN SET TOEKN_USED='Y' WHERE  TOKEN={0} AND PANNUM='{1}' AND AADHARNUM={2}"
    query=query1.format(token1,pancard1,aadhar1)
    cur=conn.execute(query)
    conn.commit()
    conn.close()
    return

 







