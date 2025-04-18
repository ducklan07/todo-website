# to do list flask app
# to practice flask programming
import os
import flask
from flask import render_template, request, redirect, url_for
from datetime import date

app = flask.Flask(__name__)

datetoday = date.today().strftime("%m_%d_%y")
datetoday_alt = date.today().strftime("%d-%B-%Y")

if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt', 'w') as file:
        file.write('')

def get_task_list():
    uncompleted_tasks = []
    completed_tasks = []
    with open('tasks.txt', 'r') as file:
        for line in file:
            task, status = line.strip().split('|')
            if status == 'uncompleted':
                uncompleted_tasks.append(task)
            elif status == 'completed':
                completed_tasks.append(task)
    return uncompleted_tasks, completed_tasks

def create_new_task_list():
    os.remove('tasks.txt')
    with open('tasks.txt', 'r') as file:
        file.write('')
    
def update_task_list(uncompleted_tasks, completed_tasks):
    with open('tasks.txt', 'w') as file:
        for task in uncompleted_tasks:
            file.write(f"{task}|uncompleted\n")
        for task in completed_tasks:
            file.write(f"{task}|completed\n")

# app baseline templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        new_task = request.form.get('task')
        if new_task:
            with open('tasks.txt', 'a') as file:
                file.write(f"{new_task}|uncompleted\n")
            return redirect(url_for('tasks'))

    uncompleted_tasks, completed_tasks = get_task_list()
    return render_template('tasks.html', uncompleted_tasks=uncompleted_tasks, completed_tasks=completed_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    if new_task:
        with open('tasks.txt', 'a') as file:
            file.write(f"{new_task}|uncompleted\n")
    return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    uncompleted_tasks, completed_tasks = get_task_list()
    if 0 <= task_id < len(uncompleted_tasks):
        del uncompleted_tasks[task_id]
    elif len(uncompleted_tasks) <= task_id < (len(completed_tasks) + len(uncompleted_tasks)):
        completed_task_index = task_id - len(uncompleted_tasks)
        del completed_tasks[completed_task_index]
    update_task_list(uncompleted_tasks, completed_tasks)
    return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    uncompleted_tasks, completed_tasks = get_task_list()
    if 0 <= task_id < len(uncompleted_tasks):
        completed_tasks.append(uncompleted_tasks.pop(task_id))
        update_task_list(uncompleted_tasks, completed_tasks)
    return redirect(url_for('tasks'))

if __name__ == "__main__":
    app.run(debug=True)