from flask import Blueprint,render_template,redirect,request,Response,url_for,flash
from flask_login import login_required, current_user
from . import db
from .models import User, Todo
from werkzeug.security import generate_password_hash, check_password_hash


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
        user.bio = request.form.get('bio')
        user.birthday = request.form.get('birthday')
        user.phone_no = request.form.get('phone')
        

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename != '':
                user.profile_image = file.read()

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        repeat_new_password = request.form.get('repeat_new_password')

        if not len(current_password):
            return render_template('profile.html', user=user)
        else:
            if not check_password_hash(user.password, current_password):
                flash('Current password is incorrect.', category='error')
                return redirect(url_for('views.profile'),id=id)

            if new_password != repeat_new_password:
                flash('New passwords do not match.', category='error')
                return redirect(url_for('views.profile'),id=id)

            if len(new_password)<=8:
                flash('password should be greater than 8 characters', category='error')
                return redirect(url_for('views.profile'),id=id)
            
            user.password = generate_password_hash(new_password)
            flash("Your\'e \"Password\" has been changed")
        
        try:
            db.session.commit()
            return redirect(url_for("views.profile"))
        except Exception as e:
            print(f"Error updating profile: {e}")
            flash('There was an error updating your profile', category='error')
    else:
        return render_template('profile.html', user=current_user)

@views.route('/profile_image/<int:id>')
def profile_image(id):
    user = User.query.get_or_404(id)
    print(user)
    print(user.profile_image)
    if not user.profile_image:
        return '', 404  # No image found

    return Response(user.profile_image, mimetype='image/png')

@views.route('/reset/<int:id>')
@login_required
def reset(id):
    user = User.query.get_or_404(id)

    user.profile_image = None

    try:
        db.session.commit()
        return redirect('/profile')
    except:
        return 'There was a problem in deleting'