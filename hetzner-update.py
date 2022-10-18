# Purpose: maintain firewall rules on Hetzner
#
# Author Predrag Vlajkovic, 2022

from __future__ import print_function
# from cgi import FieldStorage
from dataclasses import field
import sys, requests, configparser
from hcloud import Client
from hcloud.firewalls.domain import (
    FirewallRule,
    FirewallResource,
    FirewallResourceLabelSelector,
)
from uuid import uuid4

hetznerUrl = "https://api.hetzner.cloud/v1/"
ifconfigUrl = "http://ifconfig.me/ip"
configLocation = "./config.txt"

# global variables
headers = {}
firewallName = ""
hcloudToken = ""
externalIP = ""
resourceLabels = { "env":"production" }
firewallRules = []
firewallResources = []


def parseConfig (externalIP):
    global firewallName, headers, hcloudToken, firewallRules, firewallResources

    config = configparser.RawConfigParser()
    config.read(configLocation)
    firewallName = config.get('hetzner', 'firewall-name')
    hcloudToken = config.get('hetzner', 'hcloud-token')
    headers = {
        'Authorization': 'Bearer '+hcloudToken,
        'Content-Type': 'application/json'
    }
    firewallRules = [
        FirewallRule ( protocol="tcp", source_ips=[externalIP+"/32"], description="ssh", direction="in", port="22" ),
        FirewallRule ( protocol="tcp", source_ips=[externalIP+"/32"], description="kubernetes", direction="in", port="6443" )
    ]
    firewallResources = [
        FirewallResource ( type="label_selector", server=None, label_selector=FirewallResourceLabelSelector(selector="env=production") )
    ]

def getExternalIP ():
    response = requests.get (ifconfigUrl)
    if (response.status_code == 200):
        return response.text
    return None

def main(argv=None):

    externalIP = getExternalIP()
    if ( externalIP is None ):
        print ("Error trying to fetch public IP")
        sys.exit ()
    print ("External/public IP (via ifconfig.me service): {} .".format(externalIP))

    parseConfig(externalIP)

    client = Client(token=hcloudToken)
    firewall = client.firewalls.get_by_name (firewallName)
    if ( firewall is not None ):
        print ("Firewall exists.")
        client.firewalls.set_rules(firewall = firewall, rules = firewallRules)
    else:
        print ("Firewall not existing. Creating new one...")
        newFirewall = client.firewalls.create (firewallName, rules=firewallRules, labels=resourceLabels, resources=firewallResources)
        if ( newFirewall is not None ):
            print ("Firewall succesfully created.")
        else:
            print ("Error creating firewall.")

if __name__ == '__main__':
    main(sys.argv[1:])