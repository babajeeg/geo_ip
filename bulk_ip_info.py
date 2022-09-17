import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import requests
from datetime import date, timedelta
try:
   conn = mysql.connector.connect(host='xx.xx.xx.xx',
                             database='xxdbnamexx',
                             user='username',
                             password='toor')
   cursor = conn.cursor()
   #Writing Query to insert data
   query = ("INSERT INTO table_name "
                "(IP,Date,Continent,Country,Timezone,Latitude,Longitude,Subdivision) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
   file = "2022-09-06"
   with open(file+'.txt','r') as f:
      data = f.readlines()
#Change every item in the sub list into the correct data type and store it in a directory
   for i in (data):
      try:
         d = i.split(' ')
         print(d[0])
         ip = d[0]
         def get_location(ipa):
             ip_address = ipa
             response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
             location = {
                     "continent": response.get("continent_code"),
                     "country": response.get("country_name"),
                     "timezone": response.get("timezone"),
                     "latitude": response.get("latitude"),
                     "longitude": response.get("longitude"),
                     "subdivision": response.get("region_code")
                     }
             return location
         location = get_location(ip)
             #response = requests.get('https://api64.ipify.org?format=json').json()
         #print(type(d[0].encode('utf-8')))
         #location = get_location(d[0])
         edge = (d[0],d[2].rstrip('\n'), location['continent'], location['country'], location['timezone'], location['latitude'], location['longitude'],location['subdivision'])
         #edge = (i.rstrip('\n'),"")
         print(edge)
         try:
            cursor.execute(query, edge) #Execute the Query
            #Commit your changes
            conn.commit()
         except Exception as e:
            print('pass',e)
            conn.rollback()
            pass
      except Exception as e:
         print(e)
         pass


except mysql.connector.Error as error :
    print("Failed to update record to database rollback: {}".format(error))
    #reverting changes because of exception
    conn.rollback()
