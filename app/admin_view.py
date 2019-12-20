from app import app,db
import os, uuid
from flask import render_template, request, redirect, url_for, flash, session
from app.models import User, Project, Blog, Logs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, fresh_login_required
from werkzeug.security import check_password_hash, generate_password_hash



#flask-login initializing
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#----------------------------------------------END----------------------------------------------------#


#route for register
#-------------------------------------------------------------------------------------------------------#
@app.route('/add-user', methods = ['GET', 'POST'])
@login_required
def add_user():
    
    if request.method == 'POST':

        if request.form['password'] == request.form['confirm']:
            
            username = request.form['username']
            password = generate_password_hash(request.form['password'], method='sha256')


            user = User(username, password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('dashboard'))
        
        flash('Password mismatch', 'danger')
        return render_template('admin/add_user.html')


    return render_template('admin/add_user.html')

#----------------------------------------------END----------------------------------------------------#




#route for login
#-------------------------------------------------------------------------------------------------------#
@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(name = username).first()

        if user:
            if check_password_hash(user.password, request.form['password']):
                
                login_user(user)
                return redirect('/dashboard')
            
            flash('Password mismatch', 'danger')
            render_template('admin/login.html')

        flash('User Not found', 'danger' )
        render_template('admin/login.html')

    return render_template('admin/login.html')
    


#----------------------------------------------END----------------------------------------------------#




#route for logout
#-------------------------------------------------------------------------------------------------------#
@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('logout successfully', 'success')
    return redirect(url_for('login'))



#----------------------------------------------END----------------------------------------------------#






#route for dashboard
#-------------------------------------------------------------------------------------------------------#
@app.route('/dashboard')
@login_required
def dashboard():

    projects = Project.query.all()
    blogs = Blog.query.all()

    return render_template('dashboard.html', projects = projects, blogs = blogs)


#----------------------------------------------END----------------------------------------------------#



#route for adding new project
#-------------------------------------------------------------------------------------------------------#
@app.route('/add-project', methods = ['GET', 'POST'])
@login_required
def add_project():

    if request.method == 'POST':

        title = request.form['title']
        link = request.form['link']
        description = request.form['description']
        image = request.files['image']
        file_ext = image.filename.split('.')
        filename = str(uuid.uuid4()) + '.' + file_ext[-1]

        image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'project/'+ filename))

        project = Project(title, link, description, filename)
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('project/add_project.html')

#----------------------------------------------END----------------------------------------------------#



#route for editing the project
#-------------------------------------------------------------------------------------------------------#
@app.route('/edit-project/<string:id>', methods = ['GET', 'POST'])
@login_required
def edit_project(id):

    project = Project.query.get(id)

    if request.method == 'POST':

        project.title = request.form['title']
        project.link = request.form['link']
        project.description = request.form['description']
        image = request.files['image']

        if image:
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'project/'+ project.image))

        db.session.commit()

        return redirect(url_for('dashboard'))


    return render_template('project/edit_project.html', project = project)


#----------------------------------------------END----------------------------------------------------#



#route for deleting an article
#-------------------------------------------------------------------------------------------------------#
@app.route('/delete-article/<string:id>', methods = ['POST'])
@login_required
def delete_article(id):

    project = Project.query.get(id)

    if os.path.exists(os.path.join(app.config["IMAGE_UPLOADS"], 'project/'+ project.image)):
        os.remove(os.path.join(app.config["IMAGE_UPLOADS"], 'project/'+ project.image))

    db.session.delete(project)
    db.session.commit()



    return redirect(url_for('dashboard'))

#----------------------------------------------END----------------------------------------------------#



#route for adding new blog post
#-------------------------------------------------------------------------------------------------------#
@app.route('/add-blog', methods = ['GET', 'POST'])
@login_required
def add_blog():

    if request.method == 'POST':
        
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        tag = request.form['tag']
        image = request.files['image']
        file_ext = image.filename.split('.')
        filename = str(uuid.uuid4()) + '.' + file_ext[-1]

        image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'blog/'+ filename))

        blog = Blog(title,category, content, filename, tag, False)
        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('dashboard'))


    return render_template('blog/add_blog.html')

#----------------------------------------------END----------------------------------------------------#





#route for editing the project
#-------------------------------------------------------------------------------------------------------#
@app.route('/edit-blog/<string:id>', methods = ['GET', 'POST'])
@login_required
def edit_blog(id):

    blog = Blog.query.get(id)

    if request.method == 'POST':

        blog.title = request.form['title']
        blog.content = request.form['content']
        blog.edited = True
        image = request.files['image']

        if image:
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'project/'+ blog.cover_img))

        db.session.commit()

        return redirect(url_for('dashboard'))


    return render_template('blog/edit_blog.html', blog = blog)



#----------------------------------------------END----------------------------------------------------#






#route for deleting the blog
#-------------------------------------------------------------------------------------------------------#
@app.route('/delete-blog/<string:id>', methods = ['POST'])
@login_required
def delete_blog(id):

    blog = Blog.query.get(id)

    if os.path.exists(os.path.join(app.config["IMAGE_UPLOADS"], 'blog/'+ blog.cover_img)):
        os.remove(os.path.join(app.config["IMAGE_UPLOADS"], 'blog/'+ blog.cover_img))

    db.session.delete(blog)
    db.session.commit()



    return redirect(url_for('dashboard'))

#----------------------------------------------END----------------------------------------------------#



#route for notification
#-------------------------------------------------------------------------------------------------------#
@app.route('/notification')
def notification():
    
    logs = Logs.query.all()
    return render_template('admin/notification.html', logs = logs)



#----------------------------------------------END----------------------------------------------------#




#route for notification read indication
#-------------------------------------------------------------------------------------------------------#
@app.route('/mark-as-read/<int:id>')
def mark_us_read(id):

    log = Logs.query.get(id)
    if log:
        log.seen = True
        db.session.commit()
        chechUnreadLog()

        return redirect(url_for('notification'))
    return redirect(url_for('notification'))
#----------------------------------------------END----------------------------------------------------#



@app.route('/settings')
@login_required
@fresh_login_required
def settings():
    return render_template('admin/settings.html')