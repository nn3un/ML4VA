import csv
from urllib import request
import json

START_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
END_URL = '&key=AIzaSyAmNzOItr55rMHXeWaUEKKdecreyidYS_g'
addresses = []
with open('school_info_with_lat_and_long.csv', mode='a') as write_file:
    with open('school_info2.csv', newline='') as read_file:
        filereader = csv.DictReader(read_file)
        fieldnames = filereader.fieldnames + ['longitude', 'latitude']
        filewriter = csv.DictWriter(write_file, fieldnames=fieldnames)
        filewriter.writeheader()
        for row in filereader:
            address = row['Street Address'] + ',%20' + row['City'] + ',%20' + row['State'] + '%20' + row['ZIP']
            url = START_URL + address.replace(' ', '%20') + END_URL
            req = request.Request(url)
            try: request.urlopen(req)
            except request.HTTPError as e:
                print(row['School Name'])
                print(url)
                print(address)
            json_object = json.loads(request.urlopen(url).read())
            if json_object['status']=='OK':
                location = json_object['results'][0]['geometry']['location']
                print(location)
                row['latitude'] = location['lat']
                row['longitude'] = location['lng']
            filewriter.writerow(row)






