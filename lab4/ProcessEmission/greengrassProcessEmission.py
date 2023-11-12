import json
import logging
import sys

import greengrasssdk
import pandas as pd

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

#store max_co2 for each of the vehicles
max_co2_emission = {"veh0": 0, "veh1": 0, "veh2": 0, "veh3": 0, "veh4": 0}

my_counter = 0
def lambda_handler(event, context):
    global my_counter
    #1. Get your data
    veh_id, cur_veh_co2 = event.get("vehicle_id"), event.get("vehicle_co2")

    #2. Calculate max CO2 emission
    if cur_veh_co2 > max_co2_emission[veh_id]:
        max_co2_emission[veh_id] = cur_veh_co2

    #3. Return the result
    client.publish(
        topic="emission/" + veh_id + "/max_co2",
        queueFullPolicy="AllOrException",
        payload=json.dumps(
            {veh_id: max_co2_emission[veh_id]},
             "Invocation Count: {}".format(my_counter)),
    )
    my_counter += 1
    return