import RPi.GPIO as GPIO
from collections import Counter, defaultdict
from alertmanager import Alertmanager
import time, json

GPIO.setmode(GPIO.BCM)   # set board mode to Broadcom
GPIO.setwarnings(False)  # don't show warnings

al = Alertmanager("http://prometheus.lan.uctrl.net:9093")

colors = {
        'red': 1,
        'orange': 2,
        'green': 3,
        'blue': 4,
        'clear': 5
        }

types = {
        'alert': {
            'color': 'red',
            'prev': 0
            },
        'warn': {
            'color': 'orange',
            'prev': 0
            }
        }

boot_seq = ['clear', 'blue', 'green', 'orange', 'red']

for color, io in colors.items():
    GPIO.setup(io, GPIO.OUT)


def setColor(color, state):
    io = colors[color]

    if GPIO.input(io) is not int(state):
        print('Setting color', color.upper(), str(state))
        GPIO.output(io, state)


def bootSequence():
    for color in boot_seq:
        setColor(color, True)
        time.sleep(0.2)
        setColor(color, False)


bootSequence()

while True:
    d = defaultdict(list)
    start = time.time()

    for alert in al.alerts():
        if alert["labels"]["alertname"] == "DeadMansSwitch":
            continue

        for t in types:
            if alert["labels"]["severity"] == t:
                d[t].append(alert["status"]["state"])
        
    for t in types:
        print(t, json.dumps(Counter(d[t]), indent=4, sort_keys=True))

    for x in range(0, 10):
        for t, v in types.items():
            if Counter(d[t])['active'] > 0:
                setColor(v['color'], True)

        time.sleep(.5)

        for t, v in types.items():
            if v['prev'] < Counter(d[t])['active']:
                setColor(v['color'], False)

        time.sleep(.5)

    setColor('green', False)

    for t, v in types.items():
        if Counter(d[t])['active'] == 0:
            setColor(v['color'], False)
        if v['prev'] > Counter(d[t])['active']:
            setColor('green', True)

        v['prev'] = Counter(d[t])['active']

    print(time.time() - start)
    print('---')
