# emulators

```shell

gnome-terminal --tab -- gcloud beta emulators datastore start
gnome-terminal --tab -- gcloud beta emulators pubsub start
$(gcloud beta emulators pubsub env-init) && $(gcloud beta emulators datastore env-init)
export PROJECT_ID=test
gnome-terminal --tab -- bash -c 'python ./helper.py'
functions-framework --debug --target site


```
