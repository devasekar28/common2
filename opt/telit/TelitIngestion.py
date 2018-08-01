import csv  
import json 
import urllib
import requests
import time

# Open the CSV  
f = open( '/opt/telit/vineyard-1.csv', 'rU' )  
# Change each fieldname to the appropriate field name. I know, so difficult.  
reader = csv.DictReader( f, fieldnames = ( "timestamp","airtemperature","internaltemperature","soilmoisture","solarradiation","leafwetness","relativehumidity" ))  

userCredentials={"username" : "demo@orzota.com","password" : "B!gD2t2$$"}
#"{\"auth\": {\"command\":\"api.authenticate\", \"params\": {\"username\":\""+userName+"\", \"password\":\""+password+"\"}}}"
authenticate = {"auth" : {"command" : "api.authenticate","params":userCredentials}}
out = json.dumps(authenticate)
response=requests.get("https://api-dev.devicewise.com/api",data=out)
sessionKey = json.loads(response.text)
sessionId = sessionKey['auth']['params']['sessionId']
print ("SessionId is : "+sessionId)
print(response.status_code, response.reason) 
headers = {'Content-type':'application/json','Accept':'application/json'}
for row in reader:
		airtemperature=float(row['airtemperature'])
		internaltemperature=float(row['internaltemperature'])
		soilmoisture = float(row['soilmoisture'])
		solarradiation = float(row['solarradiation'])
		leafwetness=float(row['leafwetness'])
		relativehumidity=float(row['relativehumidity'])
		ingestionData = {"auth" : {"sessionId" : sessionId},"1" : {"command" : "property.batch","params": {"thingKey": "0002","key": "11","ts":"","corrId" : "mycorrid","aggregate" : "true","data" : [ {"key" : "11","value": airtemperature},{"key" : "12","value": internaltemperature},{"key" : "13","value": leafwetness},{"key" : "14","value":relativehumidity},{"key" : "15","value": soilmoisture},{"key" : "16","value": solarradiation}]}}}
		out = json.dumps(ingestionData)
#		print(out)
		response=requests.post("https://api-dev.devicewise.com/api",data=out,headers=headers)
		print(response.status_code, response.reason)
		time.sleep(5)
print ("Finished")

