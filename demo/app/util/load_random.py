from websocket import create_connection
import random
import time

ws = create_connection("ws://localhost:8000/chat")

places = ['Midwest', 'Mountain', 'Northeast', 'Pacific', 'South', 'South Atlantic']

for x in range(1,200):
    v = random.randint(1,20)
    p = random.randint(0,5)

    msg = (", ".join([places[p], str(v)]))
    print msg

    ws.send(msg)
    time.sleep(.25)