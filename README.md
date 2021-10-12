# TP1 Taller3 2c-2021
Sitio institucional con contador de visitas. Desplegable en GCP como una o mas funciones, y haciendo uso de datastore y pub/sub.

Construido con:
* python
* gcloud
* locust.io
 
# Desarrollo Local

Installar gcloud y las librerias `requirements.txt` adicionalmente instalar 

```shell
pip install locust
pip install functions-framework
```

Para ejecutar la app  y los emuladores desde una terminal de ubuntu

```shell

gnome-terminal --tab -- gcloud beta emulators datastore start
gnome-terminal --tab -- gcloud beta emulators pubsub start
$(gcloud beta emulators pubsub env-init) && $(gcloud beta emulators datastore env-init)
export PROJECT_ID=test
gnome-terminal --tab -- bash -c 'python ./helper.py'
N_SHARD=10 functions-framework --debug --target site

```

# Release
Para armar el zip a desplegar en GCP correr el script release.sh, el mismo genera un zip con el número de versión y un tag de release en el repo.
