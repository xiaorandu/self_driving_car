import json
import logging
import sys

import boto3
import csv

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
#client = greengrasssdk.client("iot-data")
iot_client = boto3.client("iot-data", region_name='us-east-2', aws_access_key_id="***", aws_secret_access_key="***")



# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath):
     
    # create a list to hold json objects for each row
    data = []
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary 
        # and add it to data
        for rows in csvReader:
            data.append(rows)
 
    return data
 
# Call the make_json function
data = make_json("vehicle4.csv")

for row in data:
    response = iot_client.publish(
        topic="emissions/publish", qos=0, payload=json.dumps(row))