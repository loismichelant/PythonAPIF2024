from flask import Blueprint, jsonify, request
from helpers.token_validation import validate_token
from database.__init__ import database
from models.task_model import Task
import controllers.task_controller as task_controller

task = Blueprint("task", __name__)

@task.route('/v0/tasks', methods=['POST'])
def add_task():
    try:
        # Validation du token
        token = validate_token()
        print(token)
        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 401
        
        # Validation des données
        task_data = request.json
        if 'description' not in task_data or 'assignedToUid' not in task_data:
            raise Exception('Error validating form')

        new_task = Task(
            description=task_data['description'],
            assignedToUid=task_data['assignedToUid'],
            createdByUid=token['user_id'], 
            createdByName=token['username']
        )

        created_task = task_controller.create_task(new_task)
        
        if created_task == "Duplicated Task":
            return jsonify({'error': 'Task Description already exists!'}), 400
        
        if not created_task.inserted_id:
            return jsonify({'error': 'Something went wrong!'}), 500

        return jsonify({'id': str(created_task.inserted_id)})
    except:
        return jsonify({'error': 'Something went wrong!'}), 500
    
@task.route('/v0/tasks/createdby', methods=['GET'])
def get_user_tasks():
    try:
        # Validation du token
        token = validate_token()
        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Récupérer les tâches de l'utilisateur
        user_tasks = task_controller.get_tasks_by_user(token['user_id'])

        return jsonify(user_tasks)
    except:
        return jsonify({'error': 'Something went wrong!'}), 500
    
@task.route('/v0/tasks/assignedto', methods=['GET'])
def get_assigned_tasks():
    try:
        # Validation du token
        token = validate_token()
        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Récupérer les tâches assignées à un utilisateur
        assigned_tasks = task_controller.get_tasks_assigned_to_user(token['user_id'])

        return jsonify(assigned_tasks)
    except:
        return jsonify({'error': 'Something went wrong!'}), 500

@task.route('/v0/tasks/<taskUid>', methods=['PATCH'])
def update_task(taskUid):
    try:
        # Validation du token
        token = validate_token()
        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Validation des données
        task_data = request.json
        if 'done' not in task_data:
            return jsonify({"error": 'Status done not found in the request'}), 400

        # Récupération et mise à jour de la tâche
        updated_task = task_controller.update_task_status(taskUid, token['user_id'], task_data['done'])

        # Si la tâche est bien mise à jour :
        return jsonify({"taskUid": str(updated_task)})
    except:
        return jsonify({'error': 'Something went wrong!'}), 500
    
@task.route('/v0/tasks/<taskUid>', methods=['DELETE'])
def delete_task(taskUid):
    try:
        # Validation du token
        token = validate_token()
        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        # Suppression de la tâche
        tasks_affected = task_controller.delete_task(taskUid, token['user_id'])

        # Retourner le nombre de tâches affectées
        return jsonify({'tasksAffected': tasks_affected}), 200
    except:
        return jsonify({'error': 'Something went wrong!'}), 500