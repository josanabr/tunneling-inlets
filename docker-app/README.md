# README.md

En este directorio se encuentran los archivos que permiten crear una imagen de Docker y en la cual se encuetra desplegada la aplicación que se usa como ejemplo en este tutorial.

* `Dockerfile` es el archivo usado por el comando `docker build ...` para crear la imagen de Docker.

> Para este tutorial la imagen se creó de la siguiente manera `docker build -t josanabr/gtd-flask-app . `.
> Posteriormente se subió a Docker Hub, `docker push josanabr/gtd-flask-app`.

* `flask-app.py` contiene la aplicación escrita en Python que se usará en este tutorial.
