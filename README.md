# Bank_Asigment
Proof of concept banking system

HOW TO RUN THE APP

PROGRAMS NEEDED

MYSQL WORKBENCH
Python 3.7+
ZIP File

THINGS NEEDED TO INSTALL
run these comands on in cmd one by one

pip install mysql-connector-python

pip install flask

pip install mysql-connect

pip install flask-mysqldb

pip install flask_mysqldb

pip install passlib

pip install forex-python

Steps 
1.Unzip the arhive at your desired location.

2. initiate a Mysql database connection and remember the username and the password used.

3. Open the "db.yaml" file from the "bankapi_group2" folder and change the mysql_user:'xxxxx' and mysql_paswword: '*******'to match yours

4. Run the MYSQL_group2_DB_Create.sql inside your Mysql server.

5. Open the "app.py", "app1.py", "app3.py"   file ( If it opens with a text editor, try running it from the command promt (python app.py)
if you get an error, find the app.py path by right clicking on it and Proprieties. A new windows should pop out and
from there you can copy the path. In command prompt run this command "cd PATH" (and paste the path copied earlier)
try to run the app.py again.)

6. If it runs you should see this message  "Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)"
					   "Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)"
					   "Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)"

7. Copy the URL (Running on "http://127.0.0.1:5001/) and paste it in your browser.

8. From here you can create an account or chose to populate the db with dummy data.
 
9. Then you can add balance to the accounts (specify customerID ex. 1, 2, 3, 4..) to be able to transfer money between accounts.

10. Frome here you can transfer money/view account details/ allow internationals transfer etc.

Stepts for Trading Platform:

11 After you create the database and you've inserted dummy data and funds into accounts now you need to establish connection to the database.

12. Open the tradingplatform.py and with a text editor or and edit lines 9 and 10 with the username and the password you've changed in the file db.yaml
	user="root",
	passwd="Bank_group2",
    Change "root" and "Bank_group2" with the credentials you are using to log into mysql connection.

13. Open importcryptocurrencyprice.py with a text editor and do the same as in step 12. Change user and passwd to match your connection.
13.1 This file should be running in the background while the USER is performing trades in the tradingplatform app.

14. If the user and passwd match with your mysql connection you would need to introduce the name and the password to LOG IN:

15.From here a menu will show up everytime you perform and action and will guide you to be fake BTC Trader.
