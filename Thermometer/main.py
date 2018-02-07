#!/usr/bin/env python3
# encoding: utf-8

import sys, getopt
import time
import pyowm
from blinktExtras import reportRuntimeErrorPixel, setPartialPixelColor, setFullPixelColor
import blinkt
import math
from API_KEY import getMyKey
from random import randint

MAX_TEMP = 32.0
MIN_TEMP = 0.0
SLEEP_TIME = 20 * 60 #0 minutes between queries
SLEEP_TIMETEST = 2 #2 seconds between temp increase by 1degC
NO_ERROR = 0
TEMP_ERROR = 1
BLINKT_ERROR = 2
NR_PIXELS = 8
API_KEY = getMyKey()

def getTemperatureAt(city = None, country = None):
    owm = pyowm.OWM(API_KEY)  # You MUST provide a valid API key
    # Have a pro subscription? Then use:
    # owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
    # Search for current weather in London (Great Britain)
    try:
        if(city != None and country != None):
            query = city+","+country
            observation = owm.weather_at_place(query)
            w = observation.get_weather()

            return w.get_temperature('celsius').get('temp')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        else:
            raise ValueError('Invalid city or country has been passes to getTemperatureAt function')
        #  Search current weather observations in the surroundings of
        # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
        # observation_list = owm.weather_around_coords(-22.57, -43.12)
    except Exception as error:
        raise error

def getNrPixelsToLightOn(_temp):
    temp = math.ceil(_temp)
    resolution = 4 # now only considerintervals of 4 (MAX_TEMP - MIN_TEMP) / NR_PIXELS
    full_pixels = math.floor(temp / resolution)
    partial_pixel = temp - full_pixels * 4
    #print("_temp, temp, full_pixels, partial_pixel = {}, {}, {} ,{}".format(_temp, temp, full_pixels, partial_pixel))
    return full_pixels, partial_pixel

def main(argv):
    sleep = SLEEP_TIME
    test = False
    blinkt.clear()
    print("Starting Termometer App... \n")

    try:
        opts, args = getopt.getopt(argv,"h:t")
    except getopt.GetoptError:
        print("Error in options. only -h is valid option.")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ("main.py city country /n city: Any city with Capital leter e.g. Leiden. /n country: Any contry code. 2Letters. eg. NL=netherlands, ES = Spain. /n -t will cause a test to gradualy increase temp until maximum range.")
            sys.exit()
        if opt == '-t':
            sleep = SLEEP_TIMETEST #increase every 5 seconds
            test = True
            print ("Entering self test mode. Increase from {} degC to {} degC every {} seconds".format(MIN_TEMP, MAX_TEMP, sleep))

    count = 0
    try:
        city = args[0]
        country = args[1]
    except IndexError:
        print( 'Missing Arguments!! main.py arg1<city> arg2<Country code 2 letters>')
        sys.exit(2)

    while(True):
        count = count + 1
        blinkt.clear()
        error_code = NO_ERROR
        #First obtain temperature from internet
        try: 
            if(test):
                temp = count
                if (temp > MAX_TEMP): # End of Test
                    sys.exit(0)
            else:
                temp = getTemperatureAt(city, country)
            print("At {}, Temperature: {} degC".format(time.ctime(),temp))
        except Exception as error:
            print('Caught this error in getTemperatureAt: ' + repr(error))
            # setting error
            error_code = TEMP_ERROR
            reportRuntimeErrorPixel(TEMP_ERROR)
    
        #Second, define  temperature and set pixel colors
        if(error_code == NO_ERROR):
            if(temp < MIN_TEMP):
                temp_pct = 0
            elif(temp > MAX_TEMP):
                temp_pct = 100
            else:
                temp_pct = ((temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)) * 100
            print("percentage = {}".format(temp_pct))

            try:
                # Calculate nr  of full and partial pixels 8function)
                [full_px, partial_pix] = getNrPixelsToLightOn(temp)
                #print("full_px, partial_pix = {}, {}".format(full_px, partial_pix))
                for pixel in range(full_px):
                    setFullPixelColor(pixel, temp_pct)
                if(partial_pix != 0):
                    setPartialPixelColor(full_px, partial_pix)
                #Go to sleep not to query too much from the web API
                blinkt.show()
            except Exception as error:
                print('Caught this error in getTemperatureAt: ' + repr(error))
                # setting error
                error_code = BLINKT_ERROR
                reportRuntimeErrorPixel(BLINKT_ERROR)

        time.sleep(sleep)


if __name__ == "__main__":
   main(sys.argv[1:])
