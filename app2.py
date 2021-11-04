from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from datetime import datetime
import requests
import yaml
import random

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index1():
    return render_template('index1.html')

@app.route('/ATMt', methods=['GET', 'POST'])
def atmt():
    userDetails = request.form
    userData = userDetails['cpr']
    userInput = userDetails['input']
    global account_number_1
    global customerId_1
    global international_transfer_1
    global international_atm_withdrawals

    mycursor = mysql.connection.cursor()


    def format_id(x):
        x = str(x)
        x = x[1:]
        x = x[:-2]
        return x

    mycursor.execute("SELECT customerID FROM logininformation WHERE Username=%s", (userData,))
    for x in mycursor:
        customerId_1 = format_id(x)
    print(customerId_1)

    mycursor.execute("Select International_transfers FROM accounts WHERE customerID=%s", (customerId_1,))
    for x in mycursor:
        international_transfer_1 = format_id(x)

    mycursor.execute("Select International_atm_withdrawals FROM accounts WHERE customerID=%s", (customerId_1,))
    for x in mycursor:
        international_atm_withdrawals = format_id(x)

    mysql.connection.commit()
    mycursor.close()



    def allow_international_transfers():
        mycursor = mysql.connection.cursor()
        if international_transfer_1 == '0':
            mycursor.execute("UPDATE `bank_delivery2`.`accounts` SET `International_transfers` = 1 WHERE customerId =%s", (customerId_1,))
            print("now you can make international transfers/payments")
        else:
            print("now you can make international transfer/payments")
        mysql.connection.commit()
        mycursor.close()

    def allow_international_atm_withdrawals():
        mycursor = mysql.connection.cursor()
        if international_atm_withdrawals == '0':
            mycursor.execute("UPDATE accounts SET International_atm_withdrawals = 1 WHERE customerId =%s", (customerId_1,))
            print("now you can withdraw money from abroad ATMs")
        else:
            print("now you can withdraw money from aborad ATMSs")
        mysql.connection.commit()
        mycursor.close()

    def block_international_atm_withdrawals():
        mycursor = mysql.connection.cursor()
        if international_atm_withdrawals == '1':
            mycursor.execute("UPDATE accounts SET International_atm_withdrawals = 0 WHERE customerId =%s", (customerId_1,))
            print("now you can withdraw money from abroad ATMs")
        else:
            print("now you can withdraw money from aborad ATMSs")
        mysql.connection.commit()
        mycursor.close()

    def block_international_transfers():
        mycursor = mysql.connection.cursor()
        if international_transfer_1 == '1':
            mycursor.execute("UPDATE accounts SET International_transfers = 0 WHERE customerId =%s", (customerId_1,))
            print("now you cannot make international transfers/payments")
        else:
            print("now you cannot make international transfer/payments")
        mysql.connection.commit()
        mycursor.close()


    if userInput == "0":
        show_transfers_types()
    elif userInput == "1":
        print(userInput)
        allow_international_transfers()
    elif userInput == "2":
        allow_international_atm_withdrawals()
    elif userInput == "3":
        block_international_transfers()
    elif userInput == "4":
        block_international_atm_withdrawals()
    else:
        print("Please try again using a valid option ")
        # show_Menu()





    mysql.connection.commit()
    mycursor.close()

    return render_template('index.html', userData=userData)

@app.route('/index', methods=['GET', 'POST'])
def users():
    userDetails = request.form
    userData = userDetails['cpr']
    return render_template('login1.html', userData=userData)


@app.route('/login112', methods=['GET', 'POST'])
def cins():
    userDetails = request.form
    userData = userDetails['cpr']
    return render_template('transation.html', userData=userData)


@app.route('/login11', methods=['GET', 'POST'])
def transaction():

    if request.method == 'POST':
        userDetails = request.form
        userInputUsername = userDetails['cpr']


        mycursor = mysql.connection.cursor()
        global userinput_receiver_account
        global userinput_amount
        userinput_receiver_account = userDetails['receiver']
        userinput_amount = userDetails['amount']

        # gettung receiver location to check
        if float(userinput_amount) <= 0:
            print("insert valid amount >0")
            return render_template('index.html', userData=userInputUsername)

        mycursor.execute("SELECT customerID FROM accounts WHERE account_number=%s", (userinput_receiver_account,))
        row = mycursor.fetchone()
        if row == None:
            print("There are no account n. match")
            return render_template('index.html', userData=userInputUsername)
        for a in mycursor:
            a = str(a)
            a = a[1:]
            a = a[:-2]
            print(a)
            customerID_receiver_Location = a


        mycursor.execute("SELECT Country FROM customer WHERE customerID=%s", (customerID_receiver_Location,))
        for b in mycursor:

            b = str(b)
            b = b[2:]
            b = b[:-3]
            receiver_Location = b

        print(receiver_Location)


        # checking if there is enough money in the account to complete transaction



        # getting the account number of the sender/user
        mycursor.execute("SELECT customerID FROM customer WHERE CPR=%s", (userInputUsername,))
        for x in mycursor:
            x = str(x)
            x = x[1:]
            x = x[:-2]
            account_customerID = x
            print(account_customerID)



        # getting sender location to be able to compare
        mycursor.execute("SELECT Country FROM customer WHERE customerID=%s", (account_customerID,))
        for c in mycursor:
            print(c)
            c = str(c)
            c = c[2:]
            c = c[:-3]
            mylocation = c
            print(mylocation)

        # selecting customer account number to be able to check balance
        mycursor.execute("SELECT account_number FROM accounts WHERE customerID=%s", (account_customerID,))
        for y in mycursor:
            y = str(y)
            y = y[2:]
            y = y[:-3]
            account_number = y
            print(account_number)
        # getting the balance
        mycursor.execute("SELECT Balance FROM accounts WHERE account_number=%s", (account_number,))
        for z in mycursor:
            print(z)
            z = str(z)
            z = z[1:]
            z = z[:-2]
            available_funds = float(z)
            print(available_funds)



        # if there are enough funds transfer can be made
        userinput_amount = float(userinput_amount)
        if userinput_amount <= available_funds:
            print("uuu")
            print(receiver_Location)
            print(mylocation)


            mycursor.execute("SELECT International_transfers FROM accounts WHERE account_number=%s", (account_number,))
            for z in mycursor:
                print(z)
                z = str(z)
                z = z[1:]
                z = z[:-2]
                accountstat = int(z)


            if accountstat == 0:
                if mylocation == receiver_Location:
                    print("transaction made")
                    mycursor.execute("UPDATE accounts SET Balance = Balance + %s WHERE account_number = %s", (userinput_amount, userinput_receiver_account,))
                    mycursor.execute("UPDATE accounts SET Balance = Balance - %s WHERE account_number = %s", (userinput_amount, account_number,))
                    mycursor.execute(
                        "INSERT INTO transactions (customerID, Sender_ACC_NR, Receiver_ACC_NR, AMOUNT, Currency, DateTime) VALUES (%s,%s,%s,%s,%s,%s)", (account_customerID, account_number, userinput_receiver_account, userinput_amount, 'DKK', datetime.now()))
                    mysql.connection.commit()
                    mycursor.close()
                    print("transaction made succesfully")
                    return render_template('index.html', userData=userInputUsername)
                else:
                    print("transaction denied invalid settings")
                    return render_template('index.html', userData=userInputUsername)



            else:
                mycursor.execute("UPDATE accounts SET Balance = Balance + %s WHERE account_number = %s",
                                 (userinput_amount, userinput_receiver_account,))
                mycursor.execute("UPDATE accounts SET Balance = Balance - %s WHERE account_number = %s",
                                 (userinput_amount, account_number,))
                mycursor.execute(
                    "INSERT INTO transactions (customerID, Sender_ACC_NR, Receiver_ACC_NR, AMOUNT, Currency, DateTime) VALUES (%s,%s,%s,%s,%s,%s)",
                    (account_customerID, account_number, userinput_receiver_account, userinput_amount, 'DKK',
                     datetime.now()))
                mysql.connection.commit()
                mycursor.close()
                print("success allowed")
                return render_template('index.html', userData=userInputUsername)
        else:
            print("transaction not possible, not enough founds")
            return render_template('index.html', userData=userInputUsername)
        return render_template('index.html', userData=userInputUsername)

@app.route('/index1', methods=['GET', 'POST'])
def users1():
    userDetails = request.form
    userInputUsername = userDetails['cpr']

    cur = mysql.connection.cursor()
    cur.execute("SELECT Username FROM logininformation WHERE Username=%s",
                (userInputUsername,))  # chechink for the username in the db
    for x in cur:
        print(x)
        x = str(x)
        x = x[2:]
        x = x[:-3]  # formatting the result to match the input
        if (x != userInputUsername):  # in case the username doesn't exist
            print("user not fount please try again")
            return render_template('index.html', userData=userInputUsername)
        else:
            print("success")
            userDetails = request.form
            userInputCPR1 = userDetails['cpr']
            userInputCPR1 = str(userInputCPR1)
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT * FROM customer WHERE CPR=%s", (userInputCPR1,))
            curi = mysql.connection.cursor()
            resultValue = curi.execute("SELECT customerID FROM customer WHERE CPR=%s", (userInputCPR1,))
            userDetails = curi.fetchall()
            userDetails = str(userDetails)
            userDetails = userDetails[2:]
            userDetails = userDetails[:-4]
            print(str(userDetails))
            userID = userDetails
            curso = mysql.connection.cursor()
            resultValue = curso.execute("SELECT * FROM accounts WHERE customerID=%s", (userID,))
            curtra = mysql.connection.cursor()
            transaction = curtra.execute("SELECT * FROM transactions WHERE customerID=%s", (userID,))

            if resultValue > 0:
                userDetails = cur.fetchall()
                userDet = curso.fetchall()
                tran = curtra.fetchall()
                return render_template('users.html', userDetails=userDetails, userDet=userDet, userData=userInputCPR1, trans=tran)

    mysql.connection.commit()
    cur.close()


if __name__ == '__main__':
    app.run(debug=True, port=5003)
