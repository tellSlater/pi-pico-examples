import wifi, os, time, ssl, socketpool, adafruit_requests
import ipaddress
import board
import adafruit_datetime as datetime
import storage

ssid = 'Matrix'
password = 'Rouki1234'

wifi.radio.connect('Matrix', 'Rouki1234')
# wifi.radio.connect("ilias", 'ggqq1234')
print("Connected to wifi!")

# time.sleep(1)

pool = socketpool.SocketPool(wifi.radio)
# time.sleep(1)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# time.sleep(1)

url = 'https://worldtimeapi.org/api/timezone/'
timezone = 'Europe/Athens'
url = url + timezone

with open('/times.txt', 'a') as outfile:
    while True:
        outfile.write('GG'.encode())
        time.sleep(2)
    #     try:
    #         response = requests.get(url).json()
    #     except:
    #         print('Request failed!')
    #     else:
    #         print('Request successful!')
    #         print('Writing date to file in unixtime...')
    #         outfile.write(str(response['datetime']))
    #         time.sleep(5)

# exec(open('main.py').read())