
 cd Ddns
 docker build --tag gcr.io/rb-munish-playground/python-dns .
 docker push gcr.io/rb-munish-playground/python-dns
 gcloud run deploy --project=rb-munish-playground python-dns --image gcr.io/rb-munish-playground/python-dns --region us-west1
