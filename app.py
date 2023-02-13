#imports
import os
import re
import ipaddress
from datetime import datetime
from google.cloud import dns
from googleapiclient.discovery import build
from flask import Flask, request, make_response
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

# initializing Flask app
app = Flask(__name__)
PROJECT_ID="rb-munish-playground"
MANAGED_ZONE="my-zone-testing"


def is_valid_ipv4(ip_address):
    try:
        # Check if the given IP address is a valid IPv4 address
        ipaddress.IPv4Address(ip_address)
        return True
    except ValueError:
        # If the given IP address is not a valid IPv4 address, return False
        return False


@app.route("/addIP/<request>")
def add_dns(request):
    match_object = re.match("URL=(.*)&IP=(.*)", request)
    URL = match_object.group(1)
    ip_address = match_object.group(2)
    if is_valid_ipv4(ip_address):
        print("The IP address {} is a valid IPv4 address.".format(ip_address))
    else:
        print("The IP address {} is not a valid IPv4 address.".format(ip_address))
    client = dns.Client(project=PROJECT_ID)
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)

    # Specify the zone and the new A record set
    record_set_data = {
        "kind": "dns#resourceRecordSet",
        "name": URL,
        "rrdatas": [ip_address],
        "ttl": 50,
        "type": "A",
    }

    # Create the new A record set
    service.changes().create(
        project=PROJECT_ID,
        managedZone=MANAGED_ZONE,
        body={
            "additions": [record_set_data]
        }
    ).execute()
    return "DNS record updated successfully"


@app.route("/deleteIP/<request>")
def delete_dns(request):
    match_object = re.match("URL=(.*)&IP=(.*)", request)
    URL = match_object.group(1)
    ip_address = match_object.group(2)
    if is_valid_ipv4(ip_address):
        print("The IP address {} is a valid IPv4 address.".format(ip_address))
    else:
        print("The IP address {} is not a valid IPv4 address.".format(ip_address))
    client = dns.Client(project=PROJECT_ID)
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)

    # Specify the zone and the new A record set
    record_set_data = {
        "kind": "dns#resourceRecordSet",
        "name": URL,
        "rrdatas": [ip_address],
        "ttl": 50,
        "type": "A",
    }

    # Create the new A record set
    service.changes().create(
        project=PROJECT_ID,
        managedZone=MANAGED_ZONE,
        body={
            "deletions": [record_set_data]
        }
    ).execute()
    return "DNS record deleted successfully"


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello " + clean_name + "! It's " + formatted_now
    return content

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
