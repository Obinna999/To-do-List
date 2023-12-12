from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import render_template , request ,redirect , url_for


app = Flask(__name__)
# connecting the DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tasks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120), nullable =False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    try:
        title = request.form['name']
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    except KeyError:
        print("Input 'name' not found in the form.")
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    del_task = Task.query.get (task_id)
    if del_task:
        db.session.delete(del_task)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:task_id>')
def update(task_id):
    up_task = Task.query.get(task_id)
    if up_task:
        up_task.completed = True
        db.session.commit()
        return redirect('/')



if __name__== '__main__':
    app.run(debug=True)