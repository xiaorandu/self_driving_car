#### configurations
    https://docs.aws.amazon.com/greengrass/v1/developerguide/gg-gs.html
    follow the steps from module 1 to module 4
    
#### start greengrass:
    #run in ec2 instance
    cd /greengrass/ggc/core/
    sudo ./greengrassd start

#### install the AWS IoT Device SDK for Python
    #run in local machine
    https://docs.aws.amazon.com/greengrass/v1/developerguide/IoT-SDK.html

#### interacting with client devices in an AWS IoT Greengrass group:
    #run in local machine
    #publisher device -> AWS IoT core
    #read vehicle data from data2
    python basicDiscovery.py --endpoint AWS_IOT_ENDPOINT --rootCA path-to-certificates/AmazonRootCA1.pem --cert path-to-certificates/publisherCertId-certificate.pem.crt --key path-to-certificates/publisherCertId-private.pem.key --thingName publisher-name --topic 'topic' --mode publish --data path-to-datafile
    #publish the vehicle info from the dataset
    ![test](https://github.com/xiaorandu/self_driving_car/assets/100817018/7bdce398-9239-4f40-ba0c-43068102afe6)
    
    #subscriber device -> AWS IoT core
    python basicDiscovery.py --endpoint AWS_IOT_ENDPOINT --rootCA path-to-certificates/AmazonRootCA1.pem --cert path-to-certificates/subscriberCertId-certificate.pem.crt --key path-to-certificates/subscriberCertId-private.pem.key --thingName subscriber-name --topic 'topic' --mode subscribe --data path-to-datafile
