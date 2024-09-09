from flask import Blueprint,render_template,redirect,request
from flask_login import login_required, current_user
from . import db
from .models import User, Todo


views = Blueprint('views' , __name__)

@views.route('/',methods=['POST','GET'])
@login_required
def home():
    if request.method == 'POST':
        task_content=request.form['content']
        new_task = Todo(content=task_content,user_id=current_user.id)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            # Print the exception details to understand the issue
            print(f"Error: {e}")
            return 'ERROR'
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('home.html',tasks=tasks,user=current_user)
@views.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem in deleting'
@views.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    print(id)
    task_to_update = Todo.query.get_or_404(id)
    print(task_to_update)
    if request.method == 'POST':
        task_to_update.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There is an error updating'
    else:
        return render_template('update.html',task_to_update=task_to_update,user=current_user)
@views.route('/profile',methods=['GET'])
@login_required
def profile():
    return render_template('profile.html',user=current_user)


@views.route('/profile/update/<int:id>',methods=['GET','POST'])
@login_required
def pupdate(id):
    user = User.query.get_or_404(id) 

    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')

        
        try:
            db.session.commit()
            return redirect('/profile')
        except Exception as e:
            print(f"Error updating profile: {e}")
            return 'There was an error updating your profile'
    else:
        return render_template('profile.html', user=current_user)