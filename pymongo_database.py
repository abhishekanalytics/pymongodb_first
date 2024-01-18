from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import json

app = Flask(__name__)

# This is Configure MongoDB
app.config['MONGO_URI'] ="mongodb://localhost:27017/monodatabase"
mongo = PyMongo(app)

@app.route('/tasks', methods=['GET', 'POST'])
def list_and_create_tasks():
    try:
        tasks_collection = mongo.db.tasks

        if request.method == 'GET':
            # This is for List all tasks
            tasks = list(tasks_collection.find())
            # Here,I am Converting ObjectId to string for JSON serialization
            for task in tasks:
                task['_id'] = str(task['_id'])
            return jsonify(tasks)

        elif request.method == 'POST':
            # Here I am Creating a new task
            new_task = request.get_json()
            new_task['_id'] = ObjectId()
            tasks_collection.insert_one(new_task)

            # Here I am Converting  ObjectId to string for JSON serialization
            new_task['_id'] = str(new_task['_id'])
            return jsonify(new_task)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_individual_task(task_id):
    try:
        tasks_collection = mongo.db.tasks

        if request.method == 'GET':
            # This is for Geting  a single task through  ID
            task = tasks_collection.find_one({'_id': ObjectId(task_id)})
            if task:
                # Here I am  Converting  ObjectId to string for JSON serialization
                task['_id'] = str(task['_id'])
                return jsonify(task)
            else:
                return jsonify({"error": "Task not found"})

        elif request.method == 'PUT':
            # ----------> Update a task
            update_data = request.get_json()
            result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': update_data})

            if result.modified_count > 0:
                updated_task = tasks_collection.find_one({'_id': ObjectId(task_id)})

                # Here I am Converting  ObjectId to string for JSON serialization
                updated_task['_id'] = str(updated_task['_id'])
                return jsonify(updated_task)
            else:
                return jsonify({"error": "Task not found"})

        elif request.method == 'DELETE':
            # --------->Delete a task
            result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
            if result.deleted_count > 0:
                return jsonify({"message": "Task deleted successfully"})
            else:
                return jsonify({"error": "Task not found"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)