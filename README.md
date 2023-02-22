## DNS Management API

This is a Flask-based REST API for managing DNS records in a Google Cloud DNS managed zone. The API allows adding and deleting DNS records for a specified URL and IP address. The API uses the Google Cloud DNS Python library and the Google Cloud DNS REST API.

## Prerequisites
* Google Cloud DNS project
* Google Cloud DNS managed zone
* Python 3.x
* Flask
* google-auth
* google-auth-oauthlib
* google-auth-httplib2
* google-api-python-client
* ipaddress

## Installation and Setup
1. Clone the repository:

```bash
git clone https://github.com/<your_username>/dns-management-api.git
```

2. Navigate to the project directory:


```bash
cd dns-management-api
```
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set the PROJECT_ID and MANAGED_ZONE variables in the app.py file to match your Google Cloud DNS project and managed zone.

## Usage
1. Start the Flask server:

```bash
python app.py
```

2. To add a DNS record, send a GET request to /addIP/URL=<URL>&IP=<IP_address>. Replace <URL> with the URL you want to add, and <IP_address> with the corresponding IP address.

3. To delete a DNS record, send a GET request to /deleteIP/URL=<URL>&IP=<IP_address>. Replace <URL> with the URL you want to delete, and <IP_address> with the corresponding IP address.

## Docker Commands
1. Build the Docker image:

```bash
docker build --tag gcr.io/<your_project_id>/python-dns .
```
Replace <your_project_id> with your Google Cloud project ID.

2. Push the Docker image to Google Container Registry:

```bash
docker push gcr.io/<your_project_id>/python-dns
```
Replace <your_project_id> with your Google Cloud project ID.

3. Deploy the Docker image to Cloud Run:

 ```bash
gcloud run deploy --project=<your_project_id> python-dns --image gcr.io/<your_project_id>/python-dns --region=<your_region>
```
Replace <your_project_id> with your Google Cloud project ID, and <your_region> with your preferred region for Cloud Run.

### Note: You will need to have the Cloud Run API enabled for your Google Cloud project before running this command.
