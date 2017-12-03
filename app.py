
import RPi.GPIO as GPIO
import time

import requests
import picamera
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture('test.jpg')
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
#GPIO.setup(24, GPIO.OUT)  #LED to GPIO24
i=0
url="http://4180413e.ngrok.io"
try:
    while True:
         button_state = GPIO.input(23)
         if button_state == False:
             #GPIO.output(24, True)
             
         pressed_time=time.time()
         while GPIO.input(23) == False:
            time.sleep(0.2)
             pressed_time=time.time()-pressed_time
         print(pressed_time)
            
             if pressed_time<=1:
        
            data=dict(time=1)
        print(data)
         elif pressed_time<=3:

        data=dict(time=3)

        print(data)
         else:
        data=dict(time=5)
            print(data)
        
         files = {'media': open('test.jpg', 'rb')}
         
         r=requests.post(url,data=data,files=files,allow_redirects=True)
             print(r.content)
         wget r.content -O example.mp3 --no-check-certificate
         omxplayer -o local example.mp3

                 
except:
    GPIO.cleanup()
