from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
from passlib.hash import sha256_crypt

app1 = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app1.config['MYSQL_HOST'] = db['mysql_host']
app1.config['MYSQL_USER'] = db['mysql_user']
app1.config['MYSQL_PASSWORD'] = db['mysql_password']
app1.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app1)

@app1.route('/quit', methods=['GET', 'POST'])
def quit():
    userDetails = request.form
    userData = userDetails['cpr']
    return render_template('index.html', userData=userData)
@app1.route('/ind', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app1.route('/', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        userDetails = request.form

        userInputUsername = userDetails['cpr']
        userInputPassword = userDetails['pass']


        #userInputPassword = sha256_crypt.encrypt(userInputPassword)
        # test = sha256_crypt.verify(password, password2))
        print(userInputUsername)
        print(userInputPassword)



        cur = mysql.connection.cursor()
        cur.execute("SELECT Username FROM logininformation WHERE Username=%s", (userInputUsername,))
        print("ok")# chechink for the username in the db
        row = cur.fetchone()
        if row == None:
            print("usernaME ERROR List is empty")
            resp = "1"
            return render_template('login.html')


        for x in cur:
            print("okkei",x)
            x = str(x)
            x = x[2:]
            x = x[:-3] #formatting the result to match the input


        mysql.connection.commit()
        cur.close()


        cur = mysql.connection.cursor()
        cur.execute("SELECT Passwd FROM logininformation WHERE Username=%s", (userInputUsername,))
        for y in cur:
            print(y)
            y = str(y)
            y = y[2:]
            y = y[:-3]
            print(y)
            test = sha256_crypt.verify(userInputPassword, y)
            if (test == 0):
                print ("wrong password, please try again")
                return render_template('login.html') 
            else:
                print ("login succesfull")
                userDetails = request.form
                userData = userDetails['cpr']
                return render_template('index.html', userData=userData)
        mysql.connection.commit()
        cur.close()
    return userInputUsername


if __name__ == '__main__':
    app1.run(debug=True, port=5002)
