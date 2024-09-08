from flask import Blueprint,render_template,redirect,request
from flask_login import login_required, current_user
from . import db
from .models import User, Todo


views = Blueprint('views' , __name__)
"""
@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user)"""

@views.route('/',methods=['POST','GET'])
@login_required
def home():
    if request.method == 'POST':
        print("HI")
        task_content=request.form['content']
        new_task = Todo(content=task_content,user_id=current_user.id)
        print(new_task)

        try:
            print("bye")
            db.session.add(new_task)
            print("hi")
            db.session.commit()
            print("commited")
            return redirect('/')
        except Exception as e:
            # Print the exception details to understand the issue
            print(f"Error: {e}")
            return 'ERROR'
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('home.html',tasks=tasks,user=current_user)
@views.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem in deleting'
@views.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There is an error updating'
    else:
        return render_template('update.html',task_to_update=task_to_update,user=current_user)