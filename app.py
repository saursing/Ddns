import os
import re
import ipaddress
from datetime import datetime
from google.cloud import dns
from googleapiclient.discovery import build
from flask import Flask, request, make_response, jsonify
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

app = Flask(__name__)
PROJECT_ID="rb-munish-playground"
MANAGED_ZONE="my-zone-testing"

def is_valid_ipv4(ip_address):
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ValueError:
        return False

def is_valid_url(URL):
    # Check if the URL is in the format "test.domain.com."
    match_object = re.match("[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+\.", URL)
    if match_object:
        return True
    else:
        return False

def process_request(request, operation):
    match_object = re.match("URL=(.*)&IP=(.*)", request)
    URL = match_object.group(1)
    ip_address = match_object.group(2)
    if not is_valid_ipv4(ip_address):
        return jsonify({"error": "Invalid IP address"}), 400
    if not is_valid_url(URL):
        return "Error: The URL {} is not in the correct format (example.com.)".format(URL)
    client = dns.Client(project=PROJECT_ID)
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)

    record_set_data = {
        "kind": "dns#resourceRecordSet",
        "name": URL,
        "rrdatas": [ip_address],
        "ttl": 50,
        "type": "A",
    }
    try:
        if operation == "add":
            service.changes().create(
                project=PROJECT_ID,
                managedZone=MANAGED_ZONE,
                body={
                    "additions": [record_set_data]
                }
            ).execute()
        else:
            service.changes().create(
                project=PROJECT_ID,
                managedZone=MANAGED_ZONE,
                body={
                    "deletions": [record_set_data]
                }
            ).execute()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "DNS record {} successfully".format(operation)}), 200

@app.route("/addIP/<request>")
def add_dns(request):
    return process_request(request, "add")

@app.route("/deleteIP/<request>")
def delete_dns(request):
    return process_request(request, "delete")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
