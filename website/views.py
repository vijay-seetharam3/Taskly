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
        is_updated = False

        bio = request.form.get('bio')
        birthday = request.form.get('birthday')
        phone_no = request.form.get('phone')

        if bio or birthday or phone_no != "":
            user.bio = request.form.get('bio')
            user.birthday = request.form.get('birthday')
            user.phone_no = request.form.get('phone')
            is_updated=True

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        if len(email) < 4:
            flash('Email must be greater than 3 characters',category='danger')
        elif len(first_name) < 2:
            flash('FirstName must be greater than3 characters',category='danger')
        else:
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            is_updated = True


        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                try:
                    user.profile_image = file.read() 
                    print(f"Image data saved for user {id}") 
                    is_updated = True
                except Exception as e:
                    print(f"Error reading file: {e}")
                    flash('There was an error uploading your image.', category='danger')

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        repeat_new_password = request.form.get('repeat_new_password')

        if current_password and new_password and repeat_new_password:
            if not check_password_hash(user.password, current_password):
                flash('Current password is incorrect.', category='danger')
            elif new_password != repeat_new_password:
                flash('New passwords do not match.', category='danger')
            elif len(new_password) <= 8:
                flash('Password should be greater than 8 characters.', category='danger')
            else:
                user.password = generate_password_hash(new_password)
                print(f"Password updated for user {id}")  
                flash("Your password has been changed.", category='success')
                is_updated = True  

        if is_updated:
            try:
                db.session.commit()
                print("Profile updated successfully")
                return redirect(url_for("views.profile"))
            except Exception as e:
                print(f"Error updating profile: {e}")
                flash('There was an error updating your profile.', category='danger')

    return render_template('profile.html', user=user)
        

@views.route('/profile_image/<int:id>')
def profile_image(id):
    user = User.query.get_or_404(id)
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