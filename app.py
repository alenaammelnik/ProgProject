from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Инициализация in-memory хранилища задач
tasks = {
    1: {"title": "Learn Flask", "description": "Read Flask documentation", "author": "Alena", "done": False},
}

current_id = len(tasks) + 1

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Получение всех задач"""
    return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Получение одной задачи по ID"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Создание новой задачи"""
    global current_id
    data = request.json
    if not data or 'title' not in data or 'description' not in data or 'author' not in data:
        return jsonify({"error": "Invalid request: 'title', 'description' and 'author' are required"}), 400
    new_task = {
        "title": data['title'],
        "description": data['description'],
        "author": data['author'],
        "done": False
    }
    tasks[current_id] = new_task
    response = {"id": current_id, "task": new_task}
    current_id += 1
    return jsonify(response), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Обновление существующей задачи"""
    data = request.json
    if not data or 'title' not in data or 'description' not in data or 'author' not in data:
        return jsonify({"error": "Invalid request: 'title', 'description' and 'author' are required"}), 400
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task['title'] = data['title']
    task['description'] = data['description']
    task['author'] = data['author']
    task['done'] = data.get('done', task['done'])
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удаление задачи"""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    del tasks[task_id]
    return '', 204

@app.route('/api/tasks/<int:task_id>/done', methods=['POST'])
def mark_task_done(task_id):
    """Отметка задачи как выполненной"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task['done'] = True
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True)

