#!/usr/bin/env python
import ceilometerclient.client
import datetime
import json
from conf import CONF

""" 
This file works as a tool to get data from ceilometer and save it to a multi-objects JSON file.
Output: raw_data.json
"""

## CONSTANTS ##
TIMESTAMP_FORMAT_1 = "%Y-%m-%dT%H:%M:%S.%f"
TIMESTAMP_FORMAT_2 = "%Y-%m-%dT%H:%M:%S"
##
    
def dump_json(cclient, start_timestamp, end_timestamp, request_limit):
    timestamp_filter = "{\"and\": [{\">\": {\"timestamp\":\"" + start_timestamp + "\"}}, {\"<\": {\"timestamp\":\"" + end_timestamp + "\"}}]}"
    orderby = "[{\"timestamp\": \"ASC\"}]"
    query = "{ \"filter\": " + timestamp_filter + ", \"orderby\":" + orderby + ", limit: " + str(request_limit) + "}"
    samples = cclient.query_samples.query(filter=timestamp_filter, orderby=orderby, limit = request_limit)
    if not samples:
        return

    vis = []
    prev_sample = samples[0]
    print "Dumping data starting from: ", start_timestamp,
    with open('raw_data.json', 'a') as outfile:
        for sample in samples:
            start_timestamp = sample.timestamp
            d = sample.to_dict()
            json.dump(d, outfile)
            outfile.write("\n")
    print "to: ", start_timestamp
    dump_json(cclient, start_timestamp, end_timestamp, request_limit)

if __name__ == "__main__":
    conf = None
    try:
        conf = CONF(r'dump_ceilometer_data.conf')
    except Exception as e:
        print e
        sys.exit(1)

    #Connect to ceilometer, connection_pool = True for keeping the connection alive as long as the process go
    cclient = ceilometerclient.client.get_client(conf.c_version,
                                                 os_username=conf.username,
                                                 os_password=conf.password,
                                                 os_tenant_name=conf.project_name,
                                                 os_auth_url=conf.auth_url,
                                                 connection_pool=True)
    dump_json(cclient, conf.start_timestamp, conf.end_timestamp, conf.request_limit)
