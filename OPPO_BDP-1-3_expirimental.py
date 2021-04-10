import socket, sys, threading, time

## ========= CUSTOM SEND ============
def send(sock, msg):
    try:
        sock.send(b'REMOTE ' + msg)
    except Exception as error:
        print("Send Exception: ", error)
        sys.exit()

    sock.settimeout(10)
    response = b''
    try:
        print("... waiting (max 10s)")
        response = sock.recv(24)
    except Exception as error:
        print("Recv Exception: ", error)
    sock.settimeout(0)
    if len(response):
        print("Response: {}".format(response))


## ========= GET UDP BROADCAST ============
oppo_data = b''
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    print("... Waiting for udp message")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 7624))
    response = sock.recv(1024)
    if len(response):
        oppo_data = response
    print("Response: {}".format(response))

## ========= PROCESS UDP RECEIVED DATA ============
if not len(oppo_data):
    print("No data to parse")
    sys.exit()

data_as_str = oppo_data.decode('utf-8')
data_split = data_as_str.split("\n")
host_chunk = data_split[1]
port_chunk = data_split[2]

host = host_chunk.split(":")[1]
port = int(port_chunk.split(":")[1])
print("Host: ", host, "Port: ", port)


## ========= ANOTHER CONNECTION RUN IN THREAD FOR RECEIVING USOLICITED "UPDATE" RESPONSE ============
locked = False
def recver():
    global locked
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        command = ''
        while True:
            time.sleep(5)
            if not locked:
                locked = True
                response = b''
                try:
                    response = sock.recv(1024)
                except Exception as error:
                    print("Exception: ", error)

                if len(response):
                    print("Response: ", response)
                locked = False
recver_thread = threading.Thread(target=recver)
recver_thread.daemon = True
# recver_thread.start()
print("# Unsolited receive thread disabled")

## ========= OPEN TCP CONNECTION FOR SENDING COMMANDS ============
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    print("#")
    print("# Send commands in all caps - see protocol for types")
    print("# https://drive.google.com/file/d/1DTB7EDHV9UHFX7biYdfWC_5PFvB-XtI6/view")
    sock.connect((host, port))

    command = ''
    while True:
        command = input("\nOPPO > ")
        locked = True
        if command == "exit":
            break
        else:
            send(sock, command.encode('utf-8'))
