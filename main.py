from PIL import Image
from PIL.ExifTags import TAGS
import pyfiglet
from colorama import Fore
import sys

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data is not None:
            exif = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                exif[tag_name] = value
            return exif
        else:
            return None
    except Exception:
        return 'Error'

def convert_gps_info_to_decimal(gps_info):
    latitude_dms = gps_info[2]
    latitude_direction = gps_info[1]
    longitude_dms = gps_info[4]
    longitude_direction = gps_info[3]

    def dms_to_decimal(degrees, minutes, seconds, direction):
        decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees  # For South and West directions, make the coordinate negative
        return decimal_degrees

    # Convert latitude from DMS to decimal degrees
    latitude_decimal = dms_to_decimal(*latitude_dms, latitude_direction)

    # Convert longitude from DMS to decimal degrees
    longitude_decimal = dms_to_decimal(*longitude_dms, longitude_direction)

    return latitude_decimal, longitude_decimal


Banner = pyfiglet.figlet_format('GeoD8Detect', font='standard')
print(Fore.MAGENTA + Banner)

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    print("""
    Flags:
          -h: show all commands
          -a: show all information about image
          -g: show only geolocation

""")
else:
    if len(sys.argv) == 3:
        image_path = sys.argv[2]
        exif_data = get_exif_data(image_path)
        if exif_data == 'Error':
            print(f'No such file or directory: {image_path}')
        elif exif_data == None:
            print('Image has no exif data')
        else:
            if sys.argv[1] =='-a':
                for key, value in exif_data.items():
                    print(f'{key} - {value}')
            elif sys.argv[1] == '-g':
                try:
                    gps_info = convert_gps_info_to_decimal(exif_data['GPSInfo'])
                    print(f'Google maps: https://www.google.com/maps/@{gps_info[0]},{gps_info[1]},20z?entry=ttu')
                except:
                    print('No exif data about geolocation')
    else:
        print('Invalid options')


