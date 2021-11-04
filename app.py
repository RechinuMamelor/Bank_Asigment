from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from datetime import datetime
from passlib.hash import sha256_crypt
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

@app.route('/index', methods=['GET', 'POST'])
def users():
    userDetails = request.form
    userData = userDetails['cpr']
    return render_template('login1.html', userData=userData)

@app.route('/acc', methods=['GET', 'POST'])
def acc_create():
    return render_template('createacc.html')

@app.route('/pop', methods=['GET', 'POST'])
def pop():
    return render_template('pop.html')
@app.route('/pip', methods=['GET', 'POST'])
def pip():
    return render_template('pip.html')

@app.route('/loginx', methods=['GET', 'POST'])
def loginx():
    if request.method == 'POST':
        print(request.data)
        global status
        status = request.data
        status = str(status)
        status = status[2:]
        status = status[:-1]
        print (status)

        if int(status) == 1:
            print("oi")
            return (status)
        else:
            print("rrr")
            return render_template('pop.html')

    return render_template('createacc.html')



@app.route('/bal', methods=['GET', 'POST'])
def bal():
    if request.method == 'POST':
        userDetails = request.form
        userInputUsername = userDetails['customerID']
        print(userInputUsername)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE accounts SET Balance = Balance + 20000 WHERE customerID=%s", (userInputUsername,))

        mysql.connection.commit()
        cur.close()
        return render_template('index1.html')



@app.route('/acc1', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form

        userInputCPR = userDetails['cpr']

        userInputFirstName = userDetails['name']

        userInputLastName = userDetails['lastname']

        userInputAge = userDetails['age']

        userInputGender = userDetails['gen']

        userInputphone = userDetails['phone']

        userInputemail = userDetails['email']

        userInputCountry = userDetails['country']

        userInputCity = userDetails['city']

        userInputaddres = userDetails['adr']

        userInputpostcode = userDetails['postcode']



        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (first_name, last_name, age, CPR, addres, postcode, City, Country, Gender, phonenumber, email, datecreated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (userInputFirstName, userInputLastName, userInputAge, userInputCPR, userInputaddres, userInputpostcode, userInputCity, userInputCountry, userInputGender, userInputphone, userInputemail, datetime.now()) )
        mysql.connection.commit()
        cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer_trading_account (first_name, last_name) VALUES (%s,%s)", (userInputFirstName, userInputLastName))
        mysql.connection.commit()
        
        cur.close()
        CVC_number = random.randint(100, 999)

        accunt_number = random.randint(1000000000,9999999999)
        accunt_number = str(accunt_number)







        def cardnumbergen():
            a = random.randint(0, 10)
            b = random.randint(100000000000000,999999999999999)
            if (a % 2) == 0:
                a = 4
                Number = eval(f"{a}{b}")
            else:
                a = random.randint(51, 55)
                Number = eval(f"{a}{b}")
                Number = int(Number / 10)
            return (Number)

        CardNumber = cardnumbergen()
        if (int(CardNumber /  1000000000000000)) == 5:
            PaymentCardType = "MASTERCARD"
        else:
            PaymentCardType = "VISA"

        def expiredate():
            today = datetime.now()
            year = today.strftime("%y")
            year = int(year)
            year = year + 4
            year = str(year)
            month = today.strftime("%m")
            expire = month + '-' + year
            return expire

        ExpireDate = expiredate()

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO accounts (account_number, Balance, card_number, Expire_date, CVC, Currency, PaymentCardType, CardType, AccountType) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (accunt_number, 0, CardNumber, ExpireDate, CVC_number, 'DKK', PaymentCardType, "Debit", "Personal"))
        mysql.connection.commit()
        cur.close()

        
        userDetails = request.form

        userUsername = userDetails['cpr']
        print(userUsername)

        userPasswd = userDetails['passwd']
        userPasswd = sha256_crypt.encrypt(userPasswd)
        print(userPasswd)



        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO logininformation (Username, Passwd) VALUES (%s,%s)", (userUsername, userPasswd))
        mysql.connection.commit()
        cur.close()



        return render_template('index.html', userData=userUsername)
    return render_template('index.html', userData=userUsername)




if __name__ == '__main__':
    app.run(debug=True, port=5001)
