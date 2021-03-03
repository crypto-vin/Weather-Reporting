import os
import time
import Adafruit_DHT
#import smbus
import drivers
from time import sleep
from datetime import datetime
from gpiozero import InputDevice

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
display = drivers.Lcd()
no_rain = InputDevice(18)

try:
    f = open('/home/pi/humtemp.csv', 'a+')
    if os.stat('/home/pi/humtemp.csv').st_size == 0:
            f.write('Date,Time,Temperature,Humidity, Rainfall\r\n')
except:
    pass

print("Welcome!")
display.lcd_display_string("Welcome!", 1) 
sleep(2)
display.lcd_display_string(str(datetime.now().strftime('TIME: %I:%M:%S %pm')), 1)
display.lcd_display_string(str(datetime.now().strftime('%a %b %d %Y')), 2)
sleep(3)
display.lcd_clear()
print("Loading data...")
display.lcd_display_string("Loading data...", 1)
sleep (3)
#display.lcd_clear()
#display.lcd_display_string(str(datetime.now().time()), 2) #display time
#sleep(1)

try:    
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        rainfall = no_rain
    
        if humidity is not None and temperature is not None:
            #f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity, rainfall))
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            display.lcd_display_string("T={0:0.1f}C  H={1:0.1f}%".format(temperature, humidity), 1)
 
            if not no_rain.is_active:
                rainfall = 3
                f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%,3.0mm/hr\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity, rainfall))
                print("Rainfall detected")
                display.lcd_display_string("Raining!", 2)
                
            else:
                rainfall = 0
                f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%,0.0mm/hr\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity, rainfall))
                print("No Rainfall detected")
                display.lcd_display_string("R=0mm/hr", 2)
   
        else:
            print('Failed! Please check your connection.')
            display.lcd_display_string("Error!", 2)
            sleep(3)

        time.sleep(10)
    
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt, exit the program and cleanup
    display.lcd_clear()
    print("Cleaning up")
    display.lcd_display_string("Cleaning up...", 1)
    display.lcd_display_string("Goodbye!", 2)
    sleep(2)
    display.lcd_clear()
    sys.exit(1)

