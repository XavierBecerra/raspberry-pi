import blinkt

def setFullPixelColor(_pixel_nr = 0, _temperature_pct = 0):
    #the pixel color will be as per temperature percentage.
    # if precentage 0.0 Blue (Cold) since it minimum temp or below
    # if precentage 100.0 Red (Warm) since it maximum temp or above
    blinkt.set_pixel(_pixel_nr, 255*(_temperature_pct/100), 0, 255*(1 - _temperature_pct/100), 0.2)
    if(_temperature_pct < 0.0 or _temperature_pct > 100.0):
        raise ValueError('Invalid Temperature percentage {} for pixel {}'.format(_pixel_nr, _temperature_pct))

def setPartialPixelColor(_pixel_nr = 0, _intensity = 0):
    if(_intensity == 1):#Pixel will be Blue
        blinkt.set_pixel(_pixel_nr, 0, 255, 255, 0.1)
    elif(_intensity == 2):#Pixel will be Green
        blinkt.set_pixel(_pixel_nr, 128, 255, 0, 0.1)
    #elif(_intensity == 3):#Pixel will be Yellow
    #    blinkt.set_pixel(_pixel_nr, 255, 255, 0, 0.1)
    elif(_intensity == 3):#Pixel will be Orange
        blinkt.set_pixel(_pixel_nr, 255, 128, 0, 0.1)
    else:
        raise ValueError('Invalid intensity {} for pixel {}'.format(_intensity, _pixel_nr))

def reportRuntimeErrorPixel(_error_code = 0):
    if(_error_code == 0):
        raise ValueError('error code provided is {}. No error should be reported'.fotmat(_error_code))
    elif (_error_code == 1):
        blinkt.set_all(255, 255, 0, 0.8) # using yellow to report erro nr 1
    elif (_error_code == 2):
        blinkt.set_all(255, 255, 255, 0.8) # using white to report erro nr 1
    else:
        raise ValueError('error code provided is {}. No error code should be linked to this number')