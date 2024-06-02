from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_login import LoginManager,  login_user, login_required, current_user
from models import db, User, Task
from flask import Blueprint
from .forms import TaskForm
from datetime import datetime
import json
from flask import Flask, request, Response
from auth.authController import role_required

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks', methods=["GET"])
@login_required
def allTasks():

    tasks = Task.query.filter_by(user_id = current_user.id)
    
    return render_template('tasks.html', tasks = tasks)

@tasks.route('/deleteTask/<task_id>', methods=["DELETE","GET"])
@login_required
def deleteTask(task_id):
    task = Task.query.filter_by(id = task_id).first()
    if (task.user_id != current_user.id) and (current_user.role != 'admin'):
       return abort(403)
    db.session.delete(task)
    db.session.commit()
    if current_user.role == 'admin':
                return redirect(url_for('tasks.everyTask'))
    return redirect(url_for('tasks.allTasks'))

@tasks.route('/add_task', methods=['GET', 'POST'])
@login_required
def addTask():
    form = TaskForm()
    if form.validate_on_submit():
        newTask = Task(title = form.title.data, description = form.description.data, deadline = form.deadline.data, user_id=current_user.id)
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for('tasks.allTasks'))
    return render_template('add_task.html', form=form)

@tasks.route('/editTask/<task_id>', methods=['GET', 'POST'])
@login_required
def editTask(task_id):
    
    task = Task.query.filter_by(id = task_id).first()
    if (task.user_id != current_user.id) and (current_user.role != 'admin'):
       return abort(403)
    form = TaskForm(obj = task)
    
    if form.validate_on_submit():
        print(form.title.data +" " +form.description.data + " " +str(form.deadline.data))
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        db.session.commit()
        if current_user.role == 'admin':
                return redirect(url_for('tasks.everyTask' ))
        return redirect(url_for('tasks.allTasks', ))
    return render_template('edit_task.html', form=form)


@tasks.route('/allTasks', methods=["GET"])
@login_required
@role_required(role ='admin')
def everyTask():
    tasks = Task.query.all()
    tasks_with_users = []
    
    for task in tasks:
        user = User.query.get(task.user_id)
        tasks_with_users.append({
            'task': task,
            'user_email': user.email if user else 'No email'
        })

    return render_template('tasks_admin.html', tasks=tasks_with_users)