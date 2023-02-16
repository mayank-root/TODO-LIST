from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize the Flask application
app = Flask(__name__)

# Set up the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define the Task class
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

# Define the Task schema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'completed')

# Initialize the schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Create a new task
@app.route('/task', methods=['POST'])
def add_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'The title field is required.'}), 400
    title = request.json['title']
    completed = request.json.get('completed', False)
    new_task = Task(title, completed)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Get a single task
@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    return task_schema.jsonify(task)

# Update a task
@app.route('/task/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    title = request.json.get('title', task.title)
    completed = request.json.get('completed', task.completed)
    task.title = title
    task.completed = completed
    db.session.commit()
    return task_schema.jsonify(task)

# Delete a task
@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

# Mark a task as completed
@app.route('/task/complete/<id>', methods=['PUT'])
def complete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    task.completed = True
    db.session.commit()
    return task_schema.jsonify(task)

# Mark a task as incomplete
@app.route('/task/incomplete/<id>', methods=['PUT'])
def incomplete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    task.completed = False
    db.session.commit()
    return task_schema.jsonify(task)

@app.before_request
def before_request():
    g.db = db
# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    
