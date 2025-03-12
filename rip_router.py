import socket
import select
import time

from rip_config import INPUTS, OUTPUTS

UPDATE_INTERVAL = 30 

sockets = {}
for port in INPUTS:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))
    sockets[port] = sock

print(f"Router listening on ports: {INPUTS}")

def send_routing_update():
    message = "RIP update from router"
    for port in OUTPUTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), ("127.0.0.1", port))
        print(f"Sent update to port {port}")

last_update_time = time.time()

while True:
    time_remaining = max(0, last_update_time + UPDATE_INTERVAL - time.time())

    readable, _, _ = select.select(sockets.values(), [], [], time_remaining)

    for sock in readable:
        data, addr = sock.recvfrom(1024)
        print(f"Received message from {addr}: {data.decode()}")

    if time.time() - last_update_time >= UPDATE_INTERVAL:
        send_routing_update()
        last_update_time = time.time()
