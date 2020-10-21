##############################
#### QR Code URL Hydrator ####
##############################
## Goes through all records in airtable & picks URL per template  ##
## Will expand as more services are added ## 
##############
## Ticket: https://www.notion.so/automedia/QR-Code-Hydration-Service-46e18bcb859f4a9d9a83393b634087d1 
#############

## Declarations 
import os
from airtable import Airtable

# Airtable settings 
base_key = os.environ.get("PRIVATE_BASE_KEY")
table_name_producer = os.environ.get("PRIVATE_TABLE_NAME_PRODUCER")
table_name_jasp = os.environ.get("PRIVATE_TABLE_NAME_JASP")
api_key = os.environ.get("PRIVATE_API_KEY")
airtable_producer = Airtable(base_key, table_name_producer, api_key) #For production env
airtable_jasp = Airtable(base_key, table_name_jasp, api_key) #For production env

#Airtable variables so if name changes will be easy to update here 
URLColumnSourceCard = "Sourcecard_URL"
URLColumnJasp = "jasp_info_url"


# Individual functions for each service type
def url_amEmbed(airtableRow):
	payload = airtableRow["fields"]["payload"]
	return payload

def url_amJasp(airtableRow):
	jaspRecID = airtableRow["fields"]["JASP_payload"][0]
	jaspPayload = airtable_jasp.get(jaspRecID)["fields"][URLColumnJasp]
	return jaspPayload

def url_amData(airtableRow):
	dataURL = 'https://www.worldometers.info/coronavirus/' #Hard coded for now
	return dataURL


# Main loop that runs through all records 
def updateLoop(colToUpdate = URLColumnSourceCard):
	allRecords = airtable_producer.get_all() #get all data
	
	for i in allRecords:
			if "Prod_Ready" in i["fields"]: #Only working on prod ready ie checkboxed
				service = i["fields"]["am_Service"][0].lower() #Gives first service ie data pull
				rec_ofAsked = i["id"]
				
				# Getting different URLs per template type
				if service == 'am_embed':
					urlToUpdate = url_amEmbed(i)
				
				elif service == 'am_jasp':
					urlToUpdate = url_amJasp(i)
				
				elif service == 'am_data':
					urlToUpdate = url_amData(i)

				# else:
				# 	urlToUpdate = '' #Need some error raising here later 

				# Preparing to upload 
				# print('URL to update', urlToUpdate)
				fields = {colToUpdate: urlToUpdate}
				airtable.update(rec_ofAsked, fields)

updateLoop()


