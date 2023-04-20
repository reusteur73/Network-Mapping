import os, threading, socket

def getOwnIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local_ip_address = s.getsockname()[0]
    s.close()
    print('Local IP address:', local_ip_address)
    return local_ip_address

LocalIp = getOwnIp()

baseIp = ".".join(str(LocalIp).split(".")[:3])

alive = []

def ping(ip):
    response = os.popen(f"ping -n 5 {ip}").read()
    if "Impossible" in response or "unreachable" in response:
        pass
    else:
        alive.append(ip)

threads = []
print("Scanning network...")
for i in range(1, 255):
    ip = baseIp + "." + str(i)
    t = threading.Thread(target=ping, args=(ip,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Network IPs:", alive)
print("Network size:", len(alive))
