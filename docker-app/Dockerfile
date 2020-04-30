FROM python:rc-buster
RUN pip install flask
WORKDIR /app
EXPOSE 5000
COPY flask-app.py /app
ENTRYPOINT [ "python" ]
CMD [ "flask-app.py" ]
