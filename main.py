#debug symbol
debug = 0

#importing the libraries
from mqtt import MQTTClient 
import machine
from network import WLAN, STA_IF
import time

#configure your data here.
ssid="<your wifi ssid>"
password="<your wifi password>"
username="<your username>"
secrete_key="<active key>"
read_obj_name="<led block title>"
write_obj_name="<text block title>"

#function to establish the connection with WiFi router.
def make_connection():
	if not wlan.isconnected():
		wlan.scan()
        wlan.connect(ssid,password)
        while not wlan.isconnected():
			try:
				print("ssid {s} is not found".format(s=ssid))
			except KeyboardInterrupt:
				break
			time.sleep(1)
	if debug:
		print('network config:', wlan.ifconfig())
	print("Successfully connected to {}".format(ssid))
	return wlan.isconnected()

#function to read the data from server.
def sub_cb(topic, msg):
	msg=msg.decode("utf-8") 
	if debug:
		print("Msg from server: {}".format(msg))		
	if msg is "OFF":
		led.value(1)
		print("off")
	elif msg =="ON":
		led.value(0)
		print("on")	
	file=open('data.txt','w')
	file.write(str(msg))
	file.close()

led=machine.Pin(16, machine.Pin.OUT)
button=machine.Pin(12, machine.Pin.IN)

file=open('data.txt')
data=file.read()
file.close()
if data is "ON":
	led.value(0)
	print("on")
elif data is "OFF":
	led.value(1)
	print("off")

#turn on WiFi
wlan = WLAN(STA_IF)
wlan.active(True)
make_connection()
      
#infinite loop
while True:
	if wlan.isconnected():
		client = MQTTClient("my device","io.adafruit.com",0,username,secrete_key) 
		client.set_callback(sub_cb) 
		client.connect()
		client.subscribe(topic=username+"/feeds/"+read_obj_name)
		i="No Obstracle Detected"
		print("Sending %s"%str(i)) 
		client.publish(topic=username+"/feeds/"+write_obj_name, msg=str(i))
	while wlan.isconnected():
		try:
			val=button.value()
			if val == 0:
				i="Obstracle Detected"
				print("Sending %s"%str(i)) 
				client.publish(topic=username+"/feeds/"+write_obj_name, msg=str(i))
			time.sleep(0.5)
			resp=client.check_msg()
			if debug:
				print(resp)
				print(str(val))
		except KeyboardInterrupt:
			break
	while not make_connection():
		pass
	print("Leaving main")
	client.disconnect()
	break



