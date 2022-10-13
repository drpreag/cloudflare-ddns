# Purpose: maintain DNS record on Cloudflare
#
# Author Predrag Vlajkovic, 2022

from __future__ import print_function
import sys, requests, json, configparser
from uuid import uuid4

cloudflareUrl = "https://api.cloudflare.com/client/v4/"
ifconfigUrl = "https://ifconfig.me/ip"
configLocation = "./config.txt"

dnsZone = ""
aRecord = ""
apiKey = ""
headers = {}

def parseConfig ():
    global dnsZone, aRecord, apiKey, headers
    config = configparser.RawConfigParser()
    config.read(configLocation)
    dnsZone = config.get('cloudflare', 'dns-zone')
    aRecord = config.get('cloudflare', 'a-record')
    apiKey = config.get('cloudflare', 'api-key')
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Key': apiKey,
        'X-Auth-Email': 'predrag.vlajkovic@gmail.com'
    }

def getExternalIP ():
    response = requests.get (ifconfigUrl)
    if response.status_code == 200:
        return response.text
    else:
        return ""

def getZoneId ():
    response = requests.get (cloudflareUrl+"/zones/", headers = headers)
    if (response.json()['success'] and response.json()['result']):
        for zones in response.json()['result']:
            if zones['name'] == dnsZone:
                return zones['id']
    return

def getZoneRecord (zoneId):
    record = dict()
    response = requests.get (cloudflareUrl+"/zones/"+zoneId+"/dns_records/", headers = headers)

    if response.json()['success'] and response.json()['result']:
        for zones in response.json()['result']:
            if (zones['name'] == aRecord):
                record['id'] = zones['id']
                record['content'] = zones['content']
                return record
    return None

def addZoneRecord (zoneId, externalIP):
    data = {
        'type': 'A',
        'name': aRecord,
        'content': externalIP,
        'ttl': 600
    }
    response = requests.post (cloudflareUrl+"/zones/"+zoneId+"/dns_records", headers = headers, json = data )
    return response.json()

def updateZoneRecord (zoneId, recordId, externalIP):
    data = {
        'type': 'A',
        'name': aRecord,
        'content': externalIP,
        'ttl': 600
    }
    response = requests.patch (cloudflareUrl+"/zones/"+zoneId+"/dns_records/"+recordId, headers = headers, json = data )
    return response.json()

def main(argv=None):

    parseConfig()
    externalIP = getExternalIP()
    print ("External IP (ifconfig.me/ip): {} .".format(externalIP))

    zoneId = getZoneId()
    if (zoneId):
        dnsRecord = getZoneRecord (zoneId)
        if (dnsRecord):
            print ("Record {} found in zone {}.".format(aRecord, dnsZone))
            if ( externalIP != dnsRecord['content']):
                print ("Updating record to: {}.".format(externalIP))
                updateResult = updateZoneRecord (zoneId, dnsRecord['id'], externalIP)
                if (updateResult['success']):
                    print ("Record {} succesfully updated to {}.".format(aRecord, externalIP))
                else:
                    print ("Error! DNS record cloud not be updated.")
            else:
                print ("Record is up tp date, doing nothing, exiting.")
        else:
            print ("Record {} not found in zone {} / {}.".format(aRecord, dnsZone, zoneId))
            addResult = addZoneRecord (zoneId, externalIP)
            if (addResult['success']):
                print ("Record {} succesfully added to zone {} / {}.".format(aRecord, dnsZone, zoneId))
            else:
                print ("Error! DNS record could not be added to zone.")
    else:
        print ("Error! Zone {} was not found".format(dnsZone))

if __name__ == '__main__':
    main(sys.argv[1:])