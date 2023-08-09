import RPi.GPIO as GPIO
import datetime
import math
import requests
import time
import dht11
from twilio.rest import Client

from gpiozero import InputDevice, AnalogInputDevice
from time import sleep

GPIO.setmode(GPIO.BCM)
myDHT=dht11.DHT11(pin=17)

data_to_send={}
result=myDHT.read()

rain_pin = 12
rain_count=0.6475
rain=InputDevice(rain_pin)
# Set GPIO pin as input and enable pull-down resistor
GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
Rain_percentage=format((rain_count / 60.0)*100)
time.sleep(1)

a = 17.27
b = 237.7
def dew_point(temp, hum):
    alpha = ((a * temp) / (b + temp)) + math.log(hum/100.0)
    return (b * alpha) / (a - alpha)
def relative_humidity(temp, dp):
    alpha = ((a * temp) / (b + temp)) + math.log(dp/100.0)
    return math.exp(alpha) * 100.0
def pressure_estimate(temp, rh):
    # Convert temperature to Kelvin
    temp = result.temperature + 273.15

    # Calculate the saturation vapor pressure
    es = 6.112 * math.exp((17.67 * temp) / (temp + 243.5))

    # Calculate the actual vapor pressure
    e = (rh / 100.0) * es

    # Calculate the pressure estimate
    p = ((e / 0.378) / (result.temperature / 216.6) ** 5.212/10000000)
    return p
# Example usage
dp = dew_point(result.temperature, 50.0) # Dew point at 50% relative humidity
rh = relative_humidity(result.temperature, dp)
pressure = pressure_estimate(result.temperature, rh)
#print("Temperature: {:.1f} degrees Celsius".format(result.temperature))
#print("Dew point: {:.1f} degrees Celsius".format(dp))
#print("Relative humidity: {:.1f}%".format(rh))
#print("Pressure: {:.1f} hPa".format(pressure))
#print("Rain percentage: {:.1f}%".format((rain_count / 60.0) * 100.0))

data_to_send["Date"]= str(datetime.datetime.now())
data_to_send["Temperature"]=result.temperature
data_to_send["Humidity"]=result.humidity
data_to_send["Rain"]=rain.is_active
data_to_send["Pressure"]=pressure
if rain.is_active == False:
        data_to_send["Rain Percentage"]=Rain_percentage
else:
        data_to_send["Rain Percentage"]=0
print(data_to_send)
r=requests.post("https://hook.eu1.make.com/pwgt47l8l8ldy1uew1ocjsng2awbrs1q",json=data_to_send)
print(r.status_code)

account_id='YOUR ACCOUNT ID'
auth_token='YOUR AUTHORIZATION TOKEN'
client=Client(account_id,auth_token)
if (result.temperature>=20.00 and result.temperature<=32.00):
        print("Ideal Weather Conditions : Enjoy the pleasant day ")
        message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body='Ideal Weather Conditi>
 
elif (result.temperature>32.00 and result.temperature<=36.00):
        print("Hot Day!! Caution ")
        message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body='Caution: Chances of H>
else:
        print("Extremely Hot Day!! Caution  ")
        message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body='Caution : High Chance>
if (result.humidity>=60 and result.humidity<=70.00):
        print("Ideal Weather Conditions : Enjoy the pleasant day ")
        message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body="Ideal Weather Conditi>
 
elif (result.humidity>70.00 and result.humidity<=80.00):
        print("Humid Day!! Caution ")
        message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body="Caution: Chances of  >
else:
        print("Extremely Humid Day!! Caution  ")
         message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body="Caution : High  chanc>

if (rain.is_active == False):
        print("Drizzling !! ")
        message=client.api.account.messages.create(to='+919361795817',from_='+12765985345',body= 'Drizzling')
