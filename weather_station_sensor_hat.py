import time
import httplib, urllib
import psutil
from time import localtime, strftime
from sense_hat import SenseHat

sense = SenseHat()
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
none = (0, 0, 0)

sense.show_message("Starting", text_colour=blue, scroll_speed=0.05)
sense.show_message("Anderson69s", text_colour=red, back_colour=green, scroll_speed=0.1)


while 1 :
    for i in range (0, 15) :
        humidity = sense.get_humidity()
        #print("Humidity: %s %%H" % humidity)
        sense_pressure = sense.get_pressure()
        #print("Pressure: %s Millibars" % sense_pressure)
        convert_pressure = sense_pressure*100
        #print("Pressure: %s Pascal" % convert_pressure)
        temp1 = sense.get_temperature_from_humidity()
        #print("Temperature1: %sC" % temp1)
        temp2 = sense.get_temperature_from_pressure()
        #print("Temperature2: %sC" % temp2)
        temp3 = ((temp1 + temp2)/2)
        #print("Temperature3: %sC" % temp3)
        cpu_pc = psutil.cpu_percent()
        #print cpu_pc
        mem_avail_mb = psutil.avail_phymem()/1000000
        #print mem_avail_mb
        cpu_temp = round(int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3,1)
        #print cpu_temp
        
        if sense_pressure < 99200 :
               sense.low_light = True
        elif sense_pressure >= 99200 :
               sense.low_light = False
               
        if temp3 < 0 :
               #print "cas 1"
               color = white
        elif temp3 >= 0 and temp3 < 14 :
               #print "cas 2"
               color = blue
        elif temp3 >= 14 and temp3 < 25 :
               #print "cas 3"
               color = green
        elif temp3 >= 25 and temp3 < 35 :
               #print "cas 4"
               color = yellow
        elif temp3 >= 35 :
               #print "cas 5"
               color = red
               
        sense.show_message("T: %d" % temp3, text_colour=color, scroll_speed=0.08)
        sense.show_message("P: %d" % convert_pressure, text_colour=color, scroll_speed=0.08)
        sense.show_message("H: %d" % humidity, text_colour=color, scroll_speed=0.08)
        #sense.show_message("CPU Load %s" % cpu_pc, text_colour=color, scroll_speed=0.08)
        #sense.show_message("CPU Temp %sC" % cpu_temp, text_colour=color, scroll_speed=0.08)
        #sense.show_message("Free Ram %s" % mem_avail_mb, text_colour=color, scroll_speed=0.08)
        time.sleep(1)
        
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    params = urllib.urlencode({'field1': convert_pressure,'field2': temp3,'field3': humidity,'field4': cpu_pc,'field5':cpu_temp,'field6': mem_avail_mb,'key':'AAAAAAAAAAAAAAAA'})
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        #print strftime("%a, %d %b %Y %H:%M:%S", localtime())
        #print response.status, response.reason
        data = response.read()
        conn.close()
        sense.show_message("ThingSpeak OK", text_colour=green, scroll_speed=0.05)
        #print "connection ok"
    except:
        sense.show_message("ThingSpeak Error", text_colour=red, scroll_speed=0.05)
        print "connection error"