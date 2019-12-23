from app import app,db
import os, uuid
from flask import render_template, request, redirect, url_for, flash, session
from app.models import User, Project, Blog, Logs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, fresh_login_required
from werkzeug.security import check_password_hash, generate_password_hash
import boto3
from app.conf import S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY



#flask-login initializing
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#boto - aws-s3 resource settings
def aws_s3_conn():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    return my_bucket



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

        #uploading to s3 bucket
        s3 = aws_s3_conn()
        s3.Object('upload/projects/{}'.format(filename)).put(Body = image, 
                        ContentType='image/jpeg', 
                        ACL='public-read')

        public_link = 'https://devjosh.s3.ap-south-1.amazonaws.com/upload/projects/{}'.format(filename)
        project = Project(title, link, description, public_link)
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

        #changing image in aws
        if image:
            s3 = aws_s3_conn()
            filename = project.image.split('/')[-1]
            s3.Object('upload/projects/{}'.format(filename)).put(Body = image, 
                        ContentType='image/jpeg', 
                        ACL='public-read')


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

    #delete file from aws s3
    s3 = boto3.resource("s3")
    key = 'upload/projects/' + project.image.split('/')[-1]
    s3.Object(S3_BUCKET, key).delete()

    #delete record from database
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

        #storing file to aws s3
        s3 = aws_s3_conn()
        s3.Object('upload/blogs/{}'.format(filename)).put(Body = image, 
                        ContentType='image/jpeg', 
                        ACL='public-read')

        #storing data in database
        public_link = 'https://devjosh.s3.ap-south-1.amazonaws.com/upload/blogs/{}'.format(filename)
        blog = Blog(title,category, content, public_link, tag, False)
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
            #rewriting file in aws s3
            s3 = aws_s3_conn()
            filename = blog.cover_img.split('/')[-1]
            s3.Object('upload/blogs/{}'.format(filename)).put(Body = image, 
                        ContentType='image/jpeg', 
                        ACL='public-read')
            
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

    #delete file from aws s3
    s3 = boto3.resource("s3")
    key = 'upload/blogs/' + blog.cover_img.split('/')[-1]
    s3.Object(S3_BUCKET, key).delete()

    #deleting record in database
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

        return redirect(url_for('notification'))
    return redirect(url_for('notification'))
#----------------------------------------------END----------------------------------------------------#



#ERROR Handling
@app.errorhandler(404)
def error_404(error):
    return render_template('error.html', error = '404' )

@app.errorhandler(403)
def error(error):
    return render_template('error.html', error = '403' )

@app.errorhandler(500)
def error(error):
    return render_template('error.html', error = '500' )