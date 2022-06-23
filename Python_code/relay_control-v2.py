### Taken from https://github.com/fourstix/Sparkfun_CircuitPython_QwiicRelay/blob/master/examples/example1_basic_control.py
"""
 Qwiic Relay Example 1 - example1_basic_control.py
 Written by Gaston Williams, June 13th, 2019
 Based on Arduino code written by
 Kevin Kuwata @ SparkX, March 21, 2018
 The Qwiic Single Relay is an I2C controlled relay produced by sparkfun
 Example 1 - Basic Control:
 This program uses the Qwiic Relay CircuitPython Library to
 control the Qwiic Relay breakout over I2C and demonstrate
 basic functionality.
"""
from time import sleep
import board
import busio
import sparkfun_qwiicrelay

# Create bus object using our board's I2C port
i2c = busio.I2C(board.SCL, board.SDA)
print(i2c)
print(board.SCL)
print(board.SDA)

# Create relay object
#relay = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c)

### To change i2c address of relay
# relay = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c, address=24)
# relay = relay.set_i2c_address(26)


relay1 = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c, address=24)
# relay2 = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c, address=25)
# relay3 = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c, address=26)

relay1.relay_on()
sleep(2)
relay1.relay_off()

'''
try:
    while True:
        relay1.relay_on()
        sleep(1)
        # relay2.relay_on()
        # sleep(2)
        # relay3.relay_on()
        # sleep(0.5)
        relay1.relay_off()
        # relay2.relay_off()
        # relay3.relay_off()
        sleep(2)

except KeyboardInterrupt:
    relay1.relay_off()
    relay2.relay_off()
    relay3.relay_off()
    print("Cancelled from Keyboard")
    pass
'''
