from flask import Flask, render_template, request, jsonify
from pyduino import *
import time

app = Flask(__name__)

print('Establishing connection to Arduino...')
    
a = Arduino(serial_port="COM3")

# sleep to ensure ample time for computer to make serial connection 
time.sleep(3)
print('established!')

# initialize the output and analog pins
LED_PIN = 13
ANALOG_PIN = 0

a.set_pin_mode(LED_PIN,'O')
print("Arduino initialized!")

@app.route('/' , methods = ['POST','GET'])
def index():

    if request.method == 'POST':
        # if we press the turn on button
        if request.form['submit'] == 'Turn On': 
            a.digital_write(LED_PIN,1)
            print('TURN ON')
            
        # if we press the turn off button
        elif request.form['submit'] == 'Turn Off': 
            a.digital_write(LED_PIN,0)
            print('TURN OFF')
        else:
            pass

    try:
        toRet = 100 * a.analog_read(ANALOG_PIN)/1023.
    except:
        toRet = 0

    return render_template('index.html', value=toRet)

# API

@app.route('/api/', methods=['GET'])
def api_all():
    try:
        toRet = jsonify([{"value" :  100 * (a.analog_read(ANALOG_PIN)/1023.)}])
    except:
        toRet = jsonify([{"value" :  0}])
    return toRet