# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
#wlan.connect('Balaji pg 1', 'apple7@ball') # connect to an AP
wlan.connect('test', 'shubhu1234')
wlan.config('mac')      # get the interface's MAC adddress
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
while not wlan.active():
    print("Waiting for wifi")
import gc
import webrepl
webrepl.start()
gc.collect()
