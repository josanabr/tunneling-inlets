#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)
#
# Definicion de una variable de tipo lista en Python que en cada elemento
# almacena un diccionario el cual describe una tarea en terminos de: 'id',
# 'description', 'title' y 'done'. Este ultimo campo indica si la tarea fue
# realizada o no.
#
tasks = [
 {
  'id': 1,
  'title': "Buy groceries",
  'description': "Milk, cheese, pizaa",
  'done': False
 },
 {
  'id': 2,
  'title': "Learn Python",
  'description': "Need a good tutorial on the web",
  'done': False
 }
]

#
# Este metodo es invocado cada vez que se accede a este servidor web sin
# una ruta especifica para acceder a un recurso.
#
# Ejemplo:
#
# curl http://localhost:5000
#
@app.route('/')
def index():
    return "Hello, World!"

#
# Este metodo se invoca cada vez que se ejecuta el siguiente comando:
#
# curl http://localhost:5000/todo/api/v1.0/tasks
#
# Devuelve todas las tareas que estan en la lista 'tasks'
#
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
 return jsonify({'tasks': tasks})

#
# Este metodo se invoca cada vez que se ejecuta el siguiente comando:
#
# curl http://localhost:5000/todo/api/v1.0/tasks/1
#
# Devuelve la tarea cuyo identificador es el 'id' es '1'
#
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
 task = [task for task in tasks if task['id'] == task_id]
 if len(task) == 0:
  abort(404)
 return jsonify({'task': task[0]})

#
# Este metodo se invoca cada vez que se genera un error como el '404' y 
# se invoca desde Python con la instruccion 'abort(404)'
#
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)

#
# Este metodo se invoca cada vez que se ejecuta el comando:
#
# curl -X POST -H "Content-type: application/json" -d '{ "title": "write a letter" }' http://localhost:5000/todo/api/v1.0/tasks
#
# Este metodo entonces crea una nueva tarea y la concatena a la lista 'tasks'
#
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
 if not request.json or not 'title' in request.json:
  abort(400)
 task = {
  'id': tasks[-1]['id'] + 1,
  'title': request.json['title'],
  'description': request.json.get('description', ""),
  'done': False
 }
 tasks.append(task)
 return jsonify({'task': task}), 201

#
# Este metodo se invoca cada vez que se ejecuta el comando:
#
# curl -X PUT -H "Content-type: application/json" -d '{ "title": "sing a song", "description": "about love" }' http://localhost:5000/todo/api/v1.0/tasks/2
#
# Este metodo entonces altera el 'title' y la 'description' de la tarea 
# numero '2'.
#
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

#
# Este metodo se invoca cada vez que se ejecuta el comando:
#
# curl -X DELETE http://localhost:5000/todo/api/v1.0/tasks/1
#
# Este metodo entonces elimina la tarea cuyo identificador es '1'
#
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

#
# Punto de 'inicio' del programa
#
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
