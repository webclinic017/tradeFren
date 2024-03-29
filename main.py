from flask import Flask, request, Response
from pyngrok import ngrok
import json
import tradingview_adapter as tview
import bitmex_adapter as bmex
import argparse
from flask import Flask
from flask import render_template
from flask import request
import sys
import os


app = Flask(__name__)

percentageToTradeWith = 80
leverageToTradeWith = 10


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':

        if(data["action"] == "buy" or data["action"] == "strongbuy"):
            bmex.buySignal(percentageToTradeWith, leverageToTradeWith)

        if(data["action"] == "sell" or data["action"] == "strongsell"):
            bmex.sellSignal(data)

    else:
        bmex.sellSignal()
    return Response(status=200)


# WEB INTERFACE

@app.route("/", methods=['POST', 'GET'])
def index():
    '''
    index page for changing the settings
    '''

    if request.method == "POST":
        #print (request.form['text'])
        percentage = request.form['percentage']
        leverage = request.form['leverage']


        #funds, orderQtyBTC, askPrice = bmex.get_funds(percentage)
        percentageToTradeWith = percentage
        leverageToTradeWith = leverage

        bmex.buySignal(percentageToTradeWith, leverageToTradeWith)


        #print(float(askPrice) , float(orderQtyBTC) , float(leverage))
        #contractSize = (float(askPrice) * (float(orderQtyBTC) * float(leverage)))

        #bmex.buySignal(percentageToTradeWith, leverageToTradeWith)

        '''
        print("walletbalance" , funds["walletBalance"])
        
        walletBalance = funds["walletBalance"]
        orderQty = walletBalance*0.8/100000000

        print(orderQty, walletBalance/100000000)
        '''

        balance = bmex.get_balance()
        print (balance)
        #return render_template('index.html', mitirjunk=balance)


    return render_template('index.html', mitirjunk = 'test')



if __name__ == "__main__":

    if len(sys.argv) > 1:
        portNumber = sys.argv[1]
    else:
        portNumber = 4040


    app.run(port=portNumber, debug=True)


