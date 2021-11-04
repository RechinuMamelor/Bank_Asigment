import requests
from forex_python.converter import CurrencyRates 
import mysql.connector
import math
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bank_group2",
    database="bank_delivery2"
)
mycursor = db.cursor()


global Currency
c = CurrencyRates()



def main():
  
  last_price = -1
  
  while True:
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    Currency = float(c.get_rate('USD', 'DKK'))  #convert USD to DKK
    btcprice = data["bpi"]["USD"]["rate"]
    btcprice = btcprice.replace(",", "")
    btcprice = float(btcprice)
    btcpricedkk = Currency * btcprice
    btcpricedkk = (round(btcpricedkk, 2))
    if btcprice != last_price:
      mycursor.execute("UPDATE crypto_assets SET Crypto_current_price =%s WHERE CryptoID = 1", (btcpricedkk,))
      db.commit()                   
      print("1 BTC=",btcpricedkk, "DKK")
      print ("1 BTC=",btcprice, "USD")
      last_price = btcprice

main()