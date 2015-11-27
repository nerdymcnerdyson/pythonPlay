


import re
import googlemaps
import json

from datetime import datetime

class OpenHouseListing:
    def __init__(self, address, price, sqft):
        self.address = address
        self.price = price
        self.sqft = sqft

    def __repr__(self):
        return "$:%s sqft:%s Address:'%s'"%(self.price, self.sqft, self.address)
    
    def __str__(self):
        return "$:%s sqft:%s Address:'%s'"%(self.price, self.sqft, self.address)
        

def main():
    homeList = processRedfinCSV('redfin.csv')

    for home in homeList:
        print home

    myhome = OpenHouseListing('1766 NW 59th St. Unit A Seattle, WA 98107', 0, 0)
    homeList.append(myhome)


   # addresses = [home.address for home in homeList]
    #googleMaps(addresses)

    inputJSON = open('output.json')
    googleDistMatrixReader(inputJSON.read())


def googleDistMatrixReader(inputString):
    print 'hi'
    thing = json.loads(inputString)

    #check status

    #grab rows
    allrows = thing["rows"]


    destinations = thing["destination_addresses"]
    origins = thing["origin_addresses"]


    

    for i in xrange(len(allrows)):
        elements = allrows[i]["elements"]

        for j in xrange(len(elements)):
            
            print elements[j]
            print 'for origin', origins[j]
            print 'and dest', destinations[i]
            print '\n\n\n'


    
def googleMaps(addresses):
    gmaps = googlemaps.Client(key='AIzaSyC5DW8SCcmg7YZN0sPrVUZa6izmz246K9Q')

    # # Geocoding and address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # print reverse_geocode_result,'\n\n\n'

    
    # # Request directions via public transit
    # now = datetime.now()
    # directions_result = gmaps.directions("Sydney Town Hall",
    #                                                                           "Parramatta, NSW",
    #                                                                           mode="transit",
    #                                                                           departure_time=now)

    # print directions_result,'\n\n\n'


    

    
    distance_matrix_result = gmaps.distance_matrix(addresses, addresses, mode='walking')
    print distance_matrix_result







    
    
def processRedfinCSV(filename):
    redfinCSV = open(filename,'r')

    columnNames = redfinCSV.readline().strip().split(',')

    addressIndex = columnNames.index("ADDRESS")
    cityIndex = columnNames.index("CITY")
    stateIndex = columnNames.index("STATE")
    zipIndex = columnNames.index("ZIP")
    priceIndex = columnNames.index("LIST PRICE")
    sqftIndex =  columnNames.index("SQFT")
    
    homes = []
    
    for line in redfinCSV:
        if len(line.strip()) <= 0:
            continue
        fields = line.strip().split(',')
        address = " ".join([fields[addressIndex], fields[cityIndex], ',', fields[stateIndex], fields[zipIndex]])
        price = fields[priceIndex]
        sqft = fields[sqftIndex]
        newHouse = OpenHouseListing(address, price, sqft)
        homes.append(newHouse)

    return homes



if __name__ == '__main__':
    main()
