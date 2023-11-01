################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string

#directory operations
import os
import shutil

################################################### Parameters for Thing
thingArn          = ''
thingId           = ''
thingName         = ''

#IoT device policy name
defaultPolicyName = 'permissions'

thing_dir = ""
certificate_dir = ""
certificates_dir = "./certificates"
public_key_dir = ""
private_key_dir = ""

cnt_of_things = 10

###################################################

def createThing():
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = thingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  for element in data: 
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
        createCertificate()


def createCertificate():
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
            setAsActive = True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data: 
            if element == 'certificateArn':
                    certificateArn = data['certificateArn']
            elif element == 'keyPair':
                    publicKey = data['keyPair']['PublicKey']
                    privateKey = data['keyPair']['PrivateKey']
            elif element == 'certificatePem':
                    certificatePem = data['certificatePem']
            elif element == 'certificateId':
                    certificateId = data['certificateId']

    if os.path.exists(thing_dir):
        shutil.rmtree(thing_dir)
    os.mkdir(thing_dir)

    with open(publicKeyPath, "w") as out:
        out.write(publicKey)
    with open(privateKeyPath, "w") as out:
        out.write(privateKey)
    with open(certificatePath, "w") as out:
        out.write(certificatePem)

    response = thingClient.attach_policy(
            policyName = defaultPolicyName,
            target     = certificateArn
    )
    response = thingClient.attach_thing_principal(
            thingName = thingName,
            principal = certificateArn
    )

thingClient = boto3.client('iot')
for i in range(1, cnt_of_things + 1):
    thingName = f'device_{str(i)}'

    thing_dir  = f"{certificates_dir}/{thingName}"
    
    certificatePath = f"{thing_dir}/{thingName}.certificate.pem"
    
    publicKeyPath = f"{thing_dir}/{thingName}.public.pem"
    
    privateKeyPath  = f"{thing_dir}/{thingName}.private.pem"

    createThing()