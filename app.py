from flask import Flask, config, flash, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a unique string
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Corrected typo
db = SQLAlchemy(app)


class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route("/")
def home():
    return "Welcome to Flask Learning"

@app.route("/home",methods = ['GET','POST'])
def home1():
    if request.method == 'POST':
        title = request.form['task']
        desc = request.form['desc']
        task = Task(title=title, desc=desc)
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully!", "success")
    alltask = Task.query.all()    
    return render_template("todo_template.html",tasks = alltask)

@app.route("/delete/<int:sno>")
def delete(sno):
    task = Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/home")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    task = Task.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        task.title = request.form['task']
        task.desc = request.form['desc']
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect('/home')
    return render_template("todo_update.html", task=task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables before running the app
    app.run(host='0.0.0.0', port=5000, debug=True)