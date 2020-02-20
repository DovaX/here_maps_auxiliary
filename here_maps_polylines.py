from here_api_key import *
import requests
import json              
import functools
import operator


def request_address_details(address):
    request=requests.get("https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey="+API_KEY+"&searchtext="+address)
    output=json.loads(request.text) 
    return(output)

def request_coordinates(address):
    output=request_address_details(address)['Response']['View'][0]['Result'][0]
    coor1=output['Location']['DisplayPosition']['Latitude']
    coor2=output['Location']['DisplayPosition']['Longitude']
    return([coor1,coor2])

def request_distance(list_of_waypoints):
    #waypoint ~ list of two values - latitude, longitude
    waypoints=""
    for i,waypoint in enumerate(list_of_waypoints):
        waypoints+="waypoint"+str(i)+"="+str(waypoint[0])+"%2C"+str(waypoint[1])+"&"
    
    request=requests.get("https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey="+API_KEY+"&"+waypoints+"mode=fastest%3Bcar%3Btraffic%3Aenabled&departure=now")
    output=json.loads(request.text)['response']['route'][0]['summary']
    return(output)

def calculate_route(list_of_waypoints):
    waypoint_strings=["waypoint"+str(i)+"=geo!"+",".join(map(str,list_of_waypoints[i])) for i in range(len(list_of_waypoints))]
    request=requests.get("https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey="+API_KEY+"&routeAttributes=shape&"+"&".join(    )+"&jsonAttributes=41&mode=fastest;truck;traffic:disabled")
    route_details=json.loads(request.text)   
    return(route_details)
    
def render_and_save_map(route_details,file="image.png"):
    coordinates=route_details['response']['route'][0]['shape']
    step=round(len(coordinates)//200/2)*2 #return 200 points (always even number of coordinates - longitude, latitude)
    route_shape=list(map(list,zip(coordinates[0::step],coordinates[1::step])))
    start_point=route_shape[0]
    end_point=route_shape[-1]
    flags=start_point+end_point
    print(flags)
    flat_waypoints=functools.reduce(operator.iconcat, route_shape, [])
    waypoint_string = "%2C".join([str(x) for x in flat_waypoints])  #Example: 52.5338%2C13.2966%2C52.538361%2C13.325329                                                                     
    request=requests.get("https://image.maps.ls.hereapi.com/mia/1.6/route?r0="+waypoint_string+"&m0="+",".join(map(str,flags))+"&lc0=00ff00&sc0=000000&lw0=2&w=500&apiKey="+API_KEY)    
    f = open(file,"wb")
    f.write(request.content)
    f.close()

def get_route_info(route_details):    
    maneuvers=route_details['response']['route'][0]['leg'][0]['maneuver']
    waypoints=[[x['position']['latitude'],x['position']['longitude']] for x in maneuvers]
    length=route_details['response']['route'][0]['leg'][0]['length']
    travel_time=route_details['response']['route'][0]['leg'][0]['travelTime']
    return(waypoints,length,travel_time)
    

