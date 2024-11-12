from database.__init__ import database
import app_config as config
from models.task_model import Task
from bson.objectid import ObjectId
import bcrypt
import jwt
from flask import jsonify

def create_task(task):
    try:
        task.description = task.description.lower()
        task.assignedToUid = task.assignedToUid.lower()
        task.createdByUid = task.createdByUid.lower()
        task.done = "false"

        collection = database.database[config.CONST_TASK_COLLECTION]

        if collection.find_one({'description': task.description}):
            return "Duplicated Task"
        
        return collection.insert_one(task.__dict__)
    except:
        raise Exception("Error on creating task!")
    
def get_tasks_by_user(user_id):
    try:
        tasks = []
        collection = database[config.CONST_TASK_COLLECTION]

        user_tasks = collection.find({"createdByUid": user_id.lower()})

        for task in user_tasks:
            current_task = {
                "assignedToName": task["assignedToName"],
                "assignedToUid": task["assignedToUid"],
                "createdByName": task["createdByName"],
                "createdByUid": task["createdByUid"],
                "description": task["description"],
                "done": task["done"],
                "taskUid": str(task["_id"]) 
            }
            tasks.append(current_task)

        return tasks
    except:
        raise Exception("Error retrieving tasks for user")

def get_tasks_assigned_to_user(user_id):
    try:
        tasks = []
        collection = database[config.CONST_TASK_COLLECTION]

        assigned_tasks = collection.find({"assignedToUid": user_id.lower()})

        for task in assigned_tasks:
            current_task = {
                "assignedToName": task["assignedToName"],
                "assignedToUid": task["assignedToUid"],
                "createdByName": task["createdByName"],
                "createdByUid": task["createdByUid"],
                "description": task["description"],
                "done": task["done"],
                "taskUid": str(task["_id"]) 
            }
            tasks.append(current_task)

        return tasks
    except:
        raise Exception("Error retrieving tasks assigned to user")
    
def update_task_status(taskUid, user_id, done):
    try:
        collection = database[config.CONST_TASK_COLLECTION]

        task_to_update = collection.find_one({"_id": ObjectId(taskUid)})

        if not task_to_update:
            raise Exception('Task not found')

        if task_to_update["assignedToUid"] != user_id:
            raise Exception('Users can only change status when task is assigned to them.')

        collection.update_one({"_id": task_to_update["_id"]}, {"$set": {"done": done}})

        return task_to_update["_id"]
    except:
        raise Exception("Error updating task status")
    
def delete_task(taskUid, user_id):
    try:
        collection = database[config.CONST_TASK_COLLECTION]

        task_to_delete = collection.find_one({"_id": ObjectId(taskUid)})

        if not task_to_delete:
            raise Exception('Task not found')

        if task_to_delete["createdByUid"] != user_id:
            raise Exception('Users can only delete when task is created by them.')

        task_delete_attempt = collection.delete_one({"_id": task_to_delete["_id"]})

        return task_delete_attempt.deleted_count
    except:
        raise Exception("Error deleting task")
