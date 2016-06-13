from sense_hat import SenseHat
from random import randint
import time
import httplib, urllib
import psutil
from time import localtime, strftime

sense = SenseHat()
#sense.set_rotation(180)

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
none = (0, 0, 0)

sense.show_message("Starting", text_colour=blue, scroll_speed=0.05)
sense.show_message("Anderson69s", text_colour=blue, back_colour=none, scroll_speed=0.05)
sense.show_message("Raspberry", text_colour=green, back_colour=none, scroll_speed=0.05)
sense.show_message("Sense Hat", text_colour=red, back_colour=none, scroll_speed=0.05)

while True :

    for i in range (0, 1):
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
        temp3 = (((temp1 + temp2)/2)-11)
        #print("Temperature3: %sC" % temp3)
        cpu_pc = psutil.cpu_percent()
        #print cpu_pc
        mem_avail_mb = psutil.avail_phymem()/1000000
        #print mem_avail_mb
        cpu_temp = round(int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3,1)
        #print cpu_temp
            
        if temp3 < 10 :
               #print "cas 1"
               color = white
        elif temp3 >= 10 and temp3 < 16 :
               #print "cas 2"
               color = blue
        elif temp3 >= 16 and temp3 < 29 :
               #print "cas 3"
               color = green
        elif temp3 >= 29 and temp3 < 35 :
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
    params = urllib.urlencode({'field1': convert_pressure,'field2': temp3,'field3': humidity,'field4': cpu_pc,'field5':cpu_temp,'field6': mem_avail_mb,'key':'WIR86RDKQQ6A4HWA'})
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
     
    pixels = [
        [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
        [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
        [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
        [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
        [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
        [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
        [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
        [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
        ]
    msleep = lambda x: time.sleep(x / 1000.0)


    def next_colour(pix): 
        r = pix[0]
        g = pix[1]
        b = pix[2]

        if (r == 255 and g < 255 and b == 0):
            g += 1

        if (g == 255 and r > 0 and b == 0):
            r -= 1

        if (g == 255 and b < 255 and r == 0):
            b += 1

        if (b == 255 and g > 0 and r == 0):
            g -= 1

        if (b == 255 and r < 255 and g == 0):
            r += 1

        if (r == 255 and b > 0 and g == 0):
            b -= 1

        pix[0] = r
        pix[1] = g
        pix[2] = b
    
    for i in range (0,2500):    
        for pix in pixels:
            next_colour(pix)

        sense.set_pixels(pixels)
        msleep(1)
