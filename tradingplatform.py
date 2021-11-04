import mysql.connector
from datetime import datetime
from passlib.hash import sha256_crypt


#establishing connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bank_group2",
    database="bank_delivery2"
)
mycursor = db.cursor()



def show_Menu():
    print ("""               -MENU-
               Press 0 to see available crypto currencies
               Press 1 to see open positions.
               Press 2 to see trade history.
               Press 3 to add money from bank account
               Press 4 to see account balance
               Press 5 to transfer money back to your bank account
               Press Q to quit.
        """)
def show_Menu_open_positions():
    
    mycursor.execute("SELECT crypto_assets.crypto_name, crypto_trades.trade_open, crypto_trades.trade_units, crypto_trades.trade_open_date FROM crypto_assets INNER JOIN crypto_trades ON crypto_assets.cryptoID = crypto_trades.cryptoID WHERE crypto_trades.trade_close IS NULL AND crypto_trades.customerID=%s", (customerID_crypto,))
        
    print ("|Asset Name | Open Price | Units bought | Trade Open Date|")
    for x in mycursor:
        print(x)
    mycursor.fetchall()

    print("""               -MENU-
             Press 1 to close a trade
             Press B to go back
    """)
    check_input = 0
    while check_input == 0:
        userInput_close = (input("What do you want to do next? "))
        if userInput_close == "1": 
            print ("Open positions:")
            mycursor.execute("SELECT crypto_trades.tradeID, crypto_assets.crypto_name, crypto_trades.trade_open, crypto_trades.trade_units, crypto_trades.trade_open_date FROM crypto_assets INNER JOIN crypto_trades ON crypto_assets.cryptoID = crypto_trades.cryptoID WHERE crypto_trades.trade_close IS NULL AND crypto_trades.customerID=%s", (customerID_crypto,))
        
            print ("| Trade ID | Asset Name | Open Price | Units bought | Trade Open Date |")

            for x in mycursor:
                print(x)
            mycursor.fetchall()

            userInput_close_tradeID = (input("Which trade you want to close? (Enter the trade ID of the trade you want to close)" ))
            userInput_close_tradeID = int(userInput_close_tradeID)

            mycursor.execute ("SELECT cryptoID FROM crypto_trades WHERE tradeID=%s", (userInput_close_tradeID,))
            for x in mycursor:
                tradeclose_cryptoID = format_id(x)
            mycursor.fetchall()

            mycursor.execute("SELECT Crypto_current_price FROM crypto_assets WHERE cryptoID=%s", (tradeclose_cryptoID,))
            for x in mycursor:
                closetrade_currentprice = format_id(x)
                closetrade_currentprice = float(closetrade_currentprice)
            mycursor.fetchall()

            mycursor.execute("UPDATE crypto_trades SET trade_close =%s WHERE tradeID=%s", (closetrade_currentprice, userInput_close_tradeID))
            db.commit()

            mycursor.execute("SELECT trade_units FROM crypto_trades WHERE tradeID=%s", (tradeclose_cryptoID,))
            for x in mycursor:
                closetrade_units = format_id(x)
            mycursor.fetchall()

            closetrade_units = float(closetrade_units)
            closetrade_units = (round(closetrade_units, 2))
            trade_value = closetrade_units * closetrade_currentprice
            trade_value = (round(trade_value, 2))

            mycursor.execute("UPDATE crypto_trades SET trade_value=%s WHERE tradeID=%s", (trade_value, userInput_close_tradeID))
            db.commit()

            mycursor.execute("SELECT trade_open FROM crypto_trades WHERE tradeID=%s", (userInput_close_tradeID,))
            for x in mycursor:
                trade_open = format_id(x)
            mycursor.fetchall()

            mycursor.execute("UPDATE crypto_trades SET trade_close_date=%s",(datetime.now(),))
            db.commit()

            trade_open = float(trade_open)
            trade_open = (round(trade_open, 2))
            trade_profit = ((closetrade_currentprice - trade_open)/trade_open)*100
            print ("Trade closed at",closetrade_currentprice,"with a value of", trade_value, "with a profit of:",trade_profit,"%")

            goback = 0
            while goback == 0:
                
                print("Press B to go back")
                print("press Q to quit")
                usergoback = (input("What do you want to do? "))
                if usergoback == "B" or usergoback == "b":
                    show_Menu_open_positions()
                    goback = 1
                elif usergoback == "Q" or usergoback =="q":
                    exit
                    goback= 1
                else:
                    print("Not valid, try again by pressing B or Q")
        else:
            user_Input()

def user_Input():
    check_File = 0
    show_Menu()
    while check_File == 0:
        userInput = (input("What do you want to do "))
        if userInput == "0":
            show_crypto_currencies()
        elif userInput == "1":
            check_File = 1
            show_Menu_open_positions()
        elif userInput == "2":
            check_File = 1
            show_trade_history()
        elif userInput == "3":
            check_File = 1
            transfer_funds()
        elif userInput == "4":
            check_File = 1
            show_balance()
        elif userInput == "5":
            check_File = 1
            withdraw_money()
        elif userInput == "Q" or userInput == "q":
            check_File = 1                
        else:    
            print("Please try again using a valid option ")
            #show_Menu()


def format_names(x):
    x = str(x)
    x = x[2:]
    x = x[:-3]
    return x
def format_id(x):
    x = str(x)
    x = x[1:]
    x = x[:-2]
    return x

def  show_crypto_currencies():
    mycursor.execute("SELECT crypto_name, Crypto_abv, Crypto_current_price FROM crypto_assets;")
    print ("ALL PRICES ARE IN DKK ")
    print ("| Crypto Name | Abreviation | Price |")

    for x in mycursor:
        print(x)
    mycursor.fetchall()
    user_input_buy()


def user_input_buy():
    check_File1 = 0
    print ("""               -MENU-
               Press 1 to buy BTC.
               Press 2 to buy ETH.
               Press 3 to buy DOGE.
               Press B to go back.
               Press Q to quit.
        """)   
    while check_File1 == 0:
        userInput_buy = (input("What do you want to do? "))
        
        if userInput_buy == "1":
            crypto_buy_id = 1
            buy_crypto(crypto_buy_id)
        elif userInput_buy == "2":
            crypto_buy_id = 2
            buy_crypto(crypto_buy_id)
        elif userInput_buy == "3":
            crypto_buy_id = 3
            buy_crypto(crypto_buy_id)
        elif userInput_buy == "B" or userInput_buy == "b":
            user_Input()
            check_File1 = 1
        elif userInput_buy == "Q" or userInput_buy == "q":
            quit
            check_File1 = 1                
        else:    
            print("Please try again using a valid option ")

def buy_crypto(cryptobuyid):
    mycursor.execute("SELECT Crypto_current_price FROM crypto_assets WHERE cryptoID=%s", (cryptobuyid,))
    for x in mycursor:
        cryptotobuy = format_id(x)
        cryptotobuy = float(cryptotobuy)
    mycursor.fetchall()

    mycursor.execute("SELECT Crypto_abv FROM crypto_assets WHERE cryptoID=%s", (cryptobuyid,))
    for x in mycursor:
        cryptoabv = format_names(x)
    mycursor.fetchall()

    mycursor.execute("SELECT available_balance FROM customer_trading_account WHERE customerID =%s", (customerID_crypto,))
    for x in mycursor:
        funds_availabetobuy = format_id(x)
        funds_availabetobuy = float(funds_availabetobuy)
    mycursor.fetchall()

    print("1 ",cryptoabv," is ",cryptotobuy,"DKK")
    print("Funds available:",funds_availabetobuy)
    buy_amount = input("Please enter the amount of money you want to invest: ")
    buy_amount = float(buy_amount)

    mycursor.execute("SELECT available_balance FROM customer_trading_account WHERE customerID=%s", (customerID_crypto,))
    for x in mycursor:
        available_balance = format_id(x)
        available_balance = float(available_balance)
        available_balance = (round(available_balance, 2))
    mycursor.fetchall()

    if buy_amount > available_balance:
        print("Not enough funds, you need to deposit more or change the amount")
        user_input_buy()
    else:
        unitsbought = buy_amount / cryptotobuy
        mycursor.execute("INSERT INTO crypto_trades (customerID, cryptoID, trade_open, trade_units, trade_open_date) VALUES (%s,%s,%s,%s,%s)", (customerID_crypto, cryptobuyid, cryptotobuy, unitsbought, datetime.now()))
        db.commit()
        
        mycursor.execute ("UPDATE customer_trading_account SET available_balance = available_balance-%s WHERE customerID=%s", (buy_amount, customerID_crypto))
        db.commit()

        print("Transaction complete")
        print("You bought:",unitsbought,"at the rate of",cryptotobuy,"for",buy_amount)
        user_Input()

def show_trade_history():
    print ("these are your trades made")
    print ("| TradeID | COIN | OPEN | UNITS | CLOSE | VALUE | CLOSED AT |")
    mycursor.execute("SELECT crypto_trades.tradeID, crypto_assets.crypto_name, crypto_trades.trade_open, crypto_trades.trade_units, crypto_trades.trade_close, crypto_trades.trade_value, crypto_trades.trade_close_date FROM crypto_assets INNER JOIN crypto_trades ON crypto_assets.cryptoID = crypto_trades.cryptoID WHERE crypto_trades.trade_close IS NOT NULL AND customerID=%s", (customerID_crypto,))
    for x in mycursor:
        print (x)
    mycursor.fetchall()
    user_Input()

def transfer_funds():
    userinput_funds = (input("how much you want to transfer: "))
    userinput_funds = float(userinput_funds)
    mycursor.execute("SELECT Balance FROM accounts WHERE customerID=%s", (customerID_crypto,))
    for x in mycursor:
        available_balance = format_id(x)

    if userinput_funds <= float(available_balance):
        mycursor.execute("UPDATE accounts SET Balance = Balance - %s WHERE customerID = %s",
                                 (userinput_funds, customerID_crypto,))
        db.commit()
        mycursor.execute("UPDATE customer_trading_account SET available_balance = available_balance + %s WHERE customerID = %s",
                                 (userinput_funds, customerID_crypto,))
        db.commit()
        print("You've transfered",userinput_funds,"DKK")
        print("")
        user_Input()
    else:
        print("not enough funds")
        user_Input()
        
def show_balance():
    mycursor.execute("SELECT available_balance FROM customer_trading_account WHERE customerID=%s", (customerID_crypto,))
    for x in mycursor:
        balance= format_id(x)
    print("Funds=",balance)
    mycursor.fetchall()
    user_Input()

def withdraw_money():
    
    mycursor.execute("SELECT available_balance FROM customer_trading_account WHERE customerID =%s", (customerID_crypto,))
    for x in mycursor:
        check_Wamount = format_id(x)
    mycursor.fetchall()
    check_Wamount = float(check_Wamount)
    print("Balnce:",check_Wamount,"DKK")
    userinput_withdraw = (input("How much you want to withdraw? "))
    userinput_withdraw = float(userinput_withdraw)
    if userinput_withdraw <= check_Wamount:
        print("You just withdrawn",userinput_withdraw, "DKK")
        mycursor.execute("UPDATE accounts SET Balance = Balance + %s WHERE customerID=%s", (userinput_withdraw, customerID_crypto))
        db.commit()
        mycursor.execute("UPDATE customer_trading_account SET available_balance = available_balance - %s WHERE customerID=%s", (userinput_withdraw, customerID_crypto))
        db.commit()
        user_Input()
    else:
        print("Not enough funds! Please enter an amount smaller than",check_Wamount)


def log_in():
    global username
    print("LOG IN")
    userInput_username = (input("Username: "))
    userInput_password = (input("Paswword: "))
    mycursor.execute ("SELECT Username FROM logininformation WHERE Username=%s", (userInput_username,))
    username= "-1"
    for x in mycursor:
        username = format_names(x)
    mycursor.fetchall()

    if(userInput_username != username):
        print("user not fount please try again")
        log_in()
    else:
        mycursor.execute ("SELECT Passwd FROM logininformation WHERE Username=%s", (userInput_username,))
        for x in mycursor:
            password = format_names(x)
        mycursor.fetchall()
        text = sha256_crypt.verify(userInput_password, password)
        if text == 1:
            print("Log in succesfull.")
            print("Welcome")
            global customerID_crypto
            mycursor.execute("SELECT customerID FROM logininformation WHERE Username=%s", (username,))
            for x in mycursor:
                customerID_crypto = format_id(x)
            mycursor.fetchall()

            user_Input()

        else:
            print("wrong password please try again")
            log_in()


global cryptobuyID
global password
global userinput_buy


log_in()