import RPi.GPIO as GPIO
from collections import Counter, defaultdict
from alertmanager import Alertmanager
import time, json

GPIO.setmode(GPIO.BCM)   # set board mode to Broadcom
GPIO.setwarnings(False)  # don't show warnings

al = Alertmanager("http://prometheus.lan.uctrl.net:9093")

colors = {
        'red': {
            'io': 1,
            'steady': True,
            'prev': 0
            },
        'orange': {
            'io': 2,
            'steady': True,
            'prev': 0
            },
        'green': {
            'io': 3,
            'steady': False,
            'prev': 0
            },
        'blue': {
            'io': 4,
            'steady': True,
            'prev': 0
            },
        'clear': {
            'io': 5,
            'steady': False,
            'prev': 0
            }
        }

severities = {
        'alert': 'red',
        'warn': 'orange',
        'info': 'white'
        }

boot_seq = ['clear', 'blue', 'green', 'orange', 'red']

for c, v in colors.items():
    GPIO.setup(v['io'], GPIO.OUT)


def setColor(color, state):
    io = colors[color]['io']

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
        if 'color' in alert["labels"]:
            c = alert["labels"]["color"]
        elif 'severity' in alert["labels"]:
            c = severities[alert["labels"]["severity"]]
        else:
            continue

        d[c].append(alert["status"]["state"])
        
    for c in colors:
        print(c, json.dumps(Counter(d[c]), indent=4, sort_keys=True))

    for x in range(0, 10):
        for c, v in colors.items():
            if (Counter(d[c])['active'] > 0 and v['steady']) \
            or (Counter(d[c])['active'] > v['prev'] and not v['steady']):
                setColor(c, True)

        time.sleep(.5)

        # Turn color off if active alerts have increased, causing color to flash
        for c, v in colors.items():
            if Counter(d[c])['active'] > v['prev']:
                setColor(c, False)

        time.sleep(.5)

    # Turn green off, if on. It should only be on for one cycle
    setColor('green', False)

    for c, v in colors.items():
        if c == 'green':
            continue

        if Counter(d[c])['active'] == 0:
            setColor(c, False)

        # Use green to indicate decrease in active alerts
        if v['prev'] > Counter(d[c])['active'] and v['steady']:
            setColor('green', True)

        colors[c]['prev'] = Counter(d[c])['active']

    print(time.time() - start)
    print('---')
