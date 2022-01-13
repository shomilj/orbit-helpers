deploy:
	gcloud config configurations activate shomil
	gcloud config set project orbit-000
	gcloud functions deploy orbit_api --runtime python38 --trigger-http --allow-unauthenticated
