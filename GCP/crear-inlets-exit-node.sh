#!/usr/bin/env bash
PROJECT="inletsuv04"
echo -n "Creando proyecto [${PROJECT}]"
gcloud projects create ${PROJECT}
BILLING=$(gcloud beta billing accounts list --format="value(name)" | tail -n 1)
gcloud beta billing projects link ${PROJECT} --billing-account=${BILLING}
echo -n "Habilitando EC2 al proyecto... "
gcloud services enable compute.googleapis.com --project=${PROJECT}
echo "habilitado!"
INSTANCE="exit-node"
ZONE="us-west1-c"
DIGEST="sha256:e1ae8711fa5a7ee30bf577d665a7a91bfe35556f83264c06896765d75b84a990"
PORT="8090"
TOKEN=$(head --bytes=8192 /dev/urandom | sha256sum | head --bytes=64)
echo -n "Creando contenedor en GCP... "
gcloud beta compute instances create-with-container ${INSTANCE} \
--project=${PROJECT} \
--zone=${ZONE} \
--machine-type=f1-micro \
--image-family=cos-stable \
--image-project=cos-cloud \
--boot-disk-size=10GB \
--container-image=inlets/inlets@${DIGEST} \
--container-restart-policy=always \
--container-arg=server \
--container-arg="--port=${PORT}" \
--container-arg="--token=${TOKEN}" \
--labels=project=inlets,language=golang
echo "creado!"
#
# Obteniendo IP de la instancia recien creada
#
IP=$(\
  gcloud compute instances describe ${INSTANCE} \
  --project=${PROJECT} \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)" \
  --zone=${ZONE}) 
NAME="projects/${PROJECT}/serviceAccounts/[0-9]{12}-compute@developer.gserviceaccount.com"

ACCOUNT=$(\
  gcloud iam service-accounts list \
  --project=${PROJECT} \
  --filter="name ~\"${NAME}\"" \
  --format="value(email)")

echo -n "Creando regla en el firewall... "
RULE="inlets-allow-${PORT}"
gcloud compute firewall-rules create ${RULE} \
--project=${PROJECT} \
--direction=INGRESS \
--action=ALLOW \
--rules=tcp:${PORT} \
--source-ranges=0.0.0.0/0 \
--target-service-accounts=${ACCOUNT}
echo "creada!"

echo ""
echo "Proyecto [${PROJECT}]"
echo "Antes de ejecutar el script '/vagrant/correr-cliente-inlets.sh'" 
echo "modifique sus primeras lineas con la siguiente informacion"
echo ""
echo "REMOTE=\"${IP}:${PORT}\""
echo "TOKEN=\"${TOKEN}\""
echo "DIGEST=\"${DIGEST}\""
