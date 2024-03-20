from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        description = request.form['description']
        priority = request.form['priority']
        todos.insert_one({'description': description, 'priority': priority})
        return redirect(url_for('index'))
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

@app.route("/<id>/update/", methods=['GET', 'POST'])
def update(id):
    todo = todos.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        description = request.form['description']
        priority = request.form['priority']
        todos.update_one({"_id": ObjectId(id)}, {'$set': {'description': description, 'priority': priority}})
        return redirect(url_for('index'))
    return render_template('update.html', todo=todo)

@app.post("/<id>/delete/")
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

db = client['peterspik']
todos = db['todos']

if __name__ == "__main__":
    app.run(debug=True)
