import sys
import csv  
import json 
import urllib
import requests


      
# Open the CSV  
f = open( '/opt/telit/vine_data1.csv', 'rU' )  
# Change each fieldname to the appropriate field name. I know, so difficult.  
reader = csv.DictReader( f, fieldnames = ( "timestamp","airtemperature","internaltemperature","soilmoisture","solarradiation","leafwetness","relativehumidity" ))  

newDict = {"timestamp":"","metrics":""}
metrics = {}
my_final_json_output=[]
count=0
apiKey = sys.argv[1]
f=open( '/opt/telit/vine_data1.json', 'w')
headers = {'Content-type':'application/json','Accept':'application/json','X-API-Key':apiKey}
for row in reader:
		metrics['airtemperature']=row['airtemperature']
   	  	metrics['internaltemperature']=row['internaltemperature']
    		metrics['soilmoisture']=row['soilmoisture']
		metrics['solarradiation']=row['solarradiation']
		metrics['leafwetness']=row['leafwetness']
		metrics['relativehumidity']=row['relativehumidity']
		newDict['metrics'] = metrics
		timestamp=row['timestamp']  
		newDict['timestamp'] = timestamp
		my_final_json_output.append(newDict)
		cjson=my_final_json_output
		
		
		out = json.dumps(my_final_json_output[count])	
		print(out)
		response=requests.post("http://52.21.87.226/rest/things/0001/data",data=out,headers=headers)
		print(response.status_code, response.reason) 
		count+=1
		f.write(out+"\n")

print "Records Inserted!!!"  
 
# Save the JSON  
#json_text=json.dumps(my_final_json_output,indent=4)
#json_file.write("{}\n".format(json text))





