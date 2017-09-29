from mqtt import MQTTClient 
import machine 
from network import WLAN, STA_IF
import time

ssid="<your wifi ssid>"
password="<your wifi password>"
username="<your username>"
secrete_key="<active key>"
read_obj_name="<led block name>"
write_obj_name="<text block name>"
wlan=WLAN(STA_IF)
wlan.active(True)

def sub_cb(topic, msg):
   print("Msg from server:%s"%msg)
   if str(msg) =="b'OFF'":
      led.value(1)
      print("off")
      file=open('data.txt','w')
      file.write(str(msg))
      file.close()
   elif str(msg) =="b'ON'":
      led.value(0)
      print("on")
      file=open('data.txt','w')
      file.write(str(msg))
      file.close()

while(not wlan.active()):
   wlan.scan()
   if not wlan.isconnect():
      wlan.connect(ssid,password)
      wlan.ifconfig()

led=machine.Pin(2, machine.Pin.OUT)
button=machine.Pin(12, machine.Pin.IN)

file=open('data.txt')
data=file.read()
print(data)
if str(data)=="b'ON'":
   led.value(0)
   print("on")
elif str(data)=="b'OFF'":
   led.value(1)
   print("off")
file.close()


      
while(wlan.active()):
   client = MQTTClient("my device","io.adafruit.com",0,username,secrete_key) 
   client.set_callback(sub_cb) 
   client.connect()
   client.subscribe(topic=username+"/feeds/"+read_obj_name)
   i="No Obstracle Detected"
   print("Sending %s"%str(i)) 
   client.publish(topic=username+"/feeds/"+write_obj_name, msg=str(i))
   while True:
      try:
         val=button.value()
         if val == 0:
            i="Obstracle Detected"
            print("Sending %s"%str(i)) 
            client.publish(topic=username+"/feeds/"+write_obj_name, msg=str(i))
         time.sleep(1)
         print(client.check_msg())
         print(str(val))
      except KeyboardInterrupt:
         break

   print("Leaving main")
   client.disconnect()
   break

