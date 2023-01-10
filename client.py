"""
The Client is a simple Python script that sends a request to the Server and
waits for a response. The Client is a REQ socket, which means it sends a
request and waits for a response. The Server is a REP socket, which means it
waits for a request and then sends a response.
"""
import json
import random
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# while True:
#     p1 = float(input("p1:"))
#     p2 = float(input("p2:"))
#     inp = {"p1": p1, "p2": p2}
#     socket.send(bytes(json.dumps(inp), "utf-8"))
#     message = socket.recv()
#     res = json.loads(message)
#     print(f"wtot: {res['wtot']}")
W_MIN = 100000
p1_min, p2_min = 0, 0
start = time.time()
for i in range(10000):
    p1 = random.random() * (5e6 - 100e3) + 100e3
    p2 = p1 + random.random() * (5e6 - p1)
    inp = {"p1": p1, "p2": p2}
    socket.send(bytes(json.dumps(inp), "utf-8"))
    message = socket.recv()
    res = json.loads(message)
    if W_MIN > res["wtot"]:
        W_MIN = res["wtot"]
        p1_min, p2_min = p1, p2
    # print(f"wtot: {res['wtot']}")
stop = time.time()
print(stop - start)
print(f"p1: {p1_min}, p2: {p2_min}, wtot: {W_MIN}")
