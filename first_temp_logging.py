import wifi, os, time, ssl, socketpool, adafruit_requests
import ipaddress
import digitalio
import board
import adafruit_datetime as datetime
import microcontroller

def blink(times:int, sec_gap:float=0.2) -> None:
    led.value = False
    for i in range(times):
        led.value = not led.value
        time.sleep(sec_gap/2)
        led.value = not led.value
        time.sleep(sec_gap/2)

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

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

with open('/temp_log.txt', 'a') as outfile:
    while True:
        try:
            response = requests.get(url).json()
        except:
            print('Request failed!')
        else:
            print('Request successful!')
            print('Writing date and temperature to file...')
            temp = microcontroller.cpu.temperature
            try:
                outfile.write(f'{response["datetime"]} - {round(temp, 1)}\n')
                blink(3)
            except OSError as e:  # Typically when the filesystem isn't writeable...
                delay = 0.5  # ...blink the LED every half second.
                if e.args[0] == 28:  # If the filesystem is full...
                    delay = 0.25  # ...blink the LED faster!
                while True:
                    led.value = not led.value
                    time.sleep(delay)
            outfile.flush()
            time.sleep(300)

# exec(open('main.py').read())