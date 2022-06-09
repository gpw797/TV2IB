import redis, json
from ib_insync import *
import asyncio, time, random

# connect to Interactive Brokers
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=8)

# connect to Redis and subscribe to tradingview messages
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('tradingview')

#contract = Contract(conId=477837011)
#ib.qualifyContractsAsync(contract)
#order = MarketOrder('BUY',1)
#trade = ib.placeOrder(contract, order)

async def check_messages():
    print(f"{time.time()} - checking for tradingview webhook messages")
    message = p.get_message()
    if message is not None and message['type'] == 'message':
        print(message)

        message_data = json.loads(message['data'])

        contract = Contract(conId=477837011)
        print(message_data['strategy']['order_action'])

        if message_data['strategy']['order_action'] == "BUY":
            print(message_data['strategy']['order_action'])
            #contract = Contract(conId=477837011)
            #ib.qualifyContracts(contract)
            order = MarketOrder('BUY', 1)
            trade = ib.placeOrder(contract, order)
            print(message)
        else:
            #contract = Contract(conId=477837011)
            #ib.qualifyContracts(contract)
            order = MarketOrder('SELL', 1)
            trade = ib.placeOrder(contract, order)

async def run_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(asyncio.sleep(interval), periodic_function())

asyncio.run(run_periodically(1, check_messages))

ib.run()