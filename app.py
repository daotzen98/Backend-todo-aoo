from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['peterspik']
todos = db['todos']

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        description = request.form.get('description')
        priority = request.form.get('priority')

        if not description or not priority:
            raise BadRequest("Description and priority are required")

        todos.insert_one({'description': description, 'priority': priority})
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

@app.route("/<id>/update/", methods=['GET', 'POST'])
def update(id):
    oid = ObjectId(id)
    todo = todos.find_one({"_id": oid})

    if todo is None:
        raise NotFound("Todo not found")

    if request.method == "POST":
        description = request.form.get('description')
        priority = request.form.get('priority')

        if not description or not priority:
            raise BadRequest("Description and priority are required")

        todos.update_one({"_id": oid}, {'$set': {'description': description, 'priority': priority}})
        return redirect(url_for('index'))

    return render_template('update.html', todo=todo)

@app.route("/<id>/delete/", methods=['POST'])
def delete(id):
    oid = ObjectId(id)
    result = todos.delete_one({"_id": oid})

    if result.deleted_count == 0:
        raise NotFound("Todo not found")

    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)