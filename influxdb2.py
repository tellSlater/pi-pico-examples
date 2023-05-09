import wifi, time, ssl, socketpool, adafruit_requests
import digitalio
import board
import adafruit_datetime as datetime
import microcontroller


class Resetter:
    def __init__(self, limit):
        self.count = 0
        self.limit = limit
        
    def increment(self):
            self.count += 1
            if self.count > self.limit:
                microcontroller.reset()

    def reset(self):
        self.count = 0


def wait(secs:int) -> None:
    time.sleep(secs)


def blink(times:int, sec_gap:float=0.2) -> None:
    led.value = False
    for i in range(times):
        led.value = not led.value
        time.sleep(sec_gap/2)
        led.value = not led.value
        time.sleep(sec_gap/2)


wifi.radio.connect('<SSID>', '<WPAKEY>')
print("Connected to wifi!")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

timeUrl = 'https://worldtimeapi.org/api/timezone/'
timezone = 'Europe/Vienna'
timeUrl = timeUrl + timezone

influxdbUrl = 'https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?org=<ORGANISATION_NAME>&bucket=<BUCKET_NAME>&precision=s'
influxdbToken = '<API_TOKEN>'

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

# Counter for successive errors
error_combo_counter = 0

# Resetter
r = Resetter(10)

while True:
    print("Getting time from worldtimeapi.org...")
    while True:
        try:
            response = requests.get(timeUrl).json()
        except:
            print('Request failed...')
            blink(1, 0.4)
            r.increment()
            time.sleep(1)
        else:
            print('Request successful! Time obtained.')
            blink(1)
            r.reset()
            break

    print("Reading tepmerature sensor...")
    temp = microcontroller.cpu.temperature
    print("Done!")

    print("Sending date and temperature to influxdb...")
    while True:
        try:
            inflresp = requests.request(
                method="POST",
                url=influxdbUrl,
                data=f"picoTemp, temperature={temp} {response['unixtime']}",
                headers={
                    "Authorization": "Token <API_TOKEN>",
                    "Content-Type": "text/plain; charset=utf-8",
                    "Accept": "application/json",
            }
            )
        except Exception as e:
            print("Post to influxdb failed!")
            with open('/error_log.txt', 'a') as erlog:
                erlog.write(f'{response["datetime"]}: {e}\n')
            blink(2, 0.4)
            r.increment()
            time.sleep(1)
        else:
            print("Successfully posted to influxdb!")
            blink(2)
            r.reset()
            break

    print('Writing date and temperature to flash...')
    
    with open('/temp_log.txt', 'a') as outfile:
        while True:
            try:
                outfile.write(f'{response["unixtime"]} {round(temp, 1)}\n')
            except OSError as e:  # Typically when the filesystem isn't writeable...
                blink(3, 0.4)  # ...blink the LED every half second.
                with open('/error_log.txt', 'a') as erlog:
                    erlog.write(f'{response["datetime"]}: {e}\n')
                    r.increment()
                time.sleep(1)
                if e.args[0] == 28:  # If the filesystem is full...
                    while True:
                        blink(3, 0.4)
                        time.sleep(1)
                break
            else:
                outfile.flush()
                print("Write to flash successful!")
                blink(3)
                r.reset()
                break
    time.sleep(600)

# """
# picoTemp,sensor_id=TLM0201 temperature=74.97038159354763,humidity=35.23103248356096,co=0.4544531056779365 1682350815
# picoTemp,sensor_id=TLM0202 temperature=76.30007505999716,humidity=35.65192991869171,co=0.5341876544505826 1682350844
# """,

# exec(open('main.py').read())