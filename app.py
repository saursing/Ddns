# Import necessary modules
import os
import re
import ipaddress
import json
from datetime import datetime
from google.cloud import dns
from googleapiclient.discovery import build
from flask import Flask, request, make_response, jsonify
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

# Initialize Flask app and set project ID and managed zone
app = Flask(__name__)
PROJECT_ID="rb-munish-playground"
MANAGED_ZONE="my-zone-testing"

# Function to check if an IP address is valid
def is_valid_ipv4(ip_address):
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ValueError:
        return False

# Function to check if a URL is in the correct format
def is_valid_url(URL):
    # Check if the URL is in the format "test.domain.com."
    match_object = re.match("[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+\.", URL)
    if match_object:
        return True
    else:
        return False

# Function to process the HTTP request
def process_request(request, operation):
    # Extract the URL and IP address from the request string
    match_object = re.match("URL=(.*)&IP=(.*)", request)
    URL = match_object.group(1)
    ip_address = match_object.group(2)
    # Check if the IP address is valid
    if not is_valid_ipv4(ip_address):
        return jsonify({"error": "Invalid IP address"}), 400
    # Check if the URL is in the correct format
    if not is_valid_url(URL):
        return "Error: The URL {} is not in the correct format (example.com.)".format(URL)
    # Create a DNS client and get the Google credentials
    client = dns.Client(project=PROJECT_ID)
    credentials = GoogleCredentials.get_application_default()
    # Build the DNS API service
    service = discovery.build('dns', 'v1', credentials=credentials)
    # Create a DNS record set data object with the URL and IP address
    record_set_data = {
        "kind": "dns#resourceRecordSet",
        "name": URL,
        "rrdatas": [ip_address],
        "ttl": 50,
        "type": "A",
    }
    try:
        # If the operation is "add", create a new DNS record
        if operation == "add":
            service.changes().create(
                project=PROJECT_ID,
                managedZone=MANAGED_ZONE,
                body={
                    "additions": [record_set_data]
                }
            ).execute()
        # If the operation is "delete", delete the DNS record
        elif operation == "delete":
            service.changes().create(
                project=PROJECT_ID,
                managedZone=MANAGED_ZONE,
                body={
                    "deletions": [record_set_data]
                }
            ).execute()
        else:
            # Return a 400 Bad Request error code with an error message if invalid operation is specified
            error_message = f"Invalid operation '{operation}' specified."
            error_body = {
                "error": {
                    "code": 400,
                    "message": error_message
                }
            }
            return (json.dumps(error_body), 400, {'Content-Type': 'application/json'})            
    except Exception as e:
        # Return a 500 Internal Server Error code with an error message if an exception occurs
        return jsonify({"error": str(e)}), 500
    # Return a success message if the operation was successful
    return jsonify({"message": "DNS record {} successfully".format(operation)}), 200

#Define endpoint for adding DNS record
@app.route("/addIP/<request>")
def add_dns(request):
    return process_request(request, "add")

#Define endpoint for deleting DNS record
@app.route("/deleteIP/<request>")
def delete_dns(request):
    return process_request(request, "delete")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
