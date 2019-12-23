from app import app, db, mail
from flask import render_template, redirect, session, send_file, request, flash, url_for
from app.models import Project, Blog, Subscribe, Contact, Hire, Logs
from flask_mail import Message
from sqlalchemy import desc
import os


#mail sending functon
def send_mail(name, email, types):

    msg = Message('Josh! The Developer', sender = 'joshyjoy.dev@gmail.com', recipients = [email])
    
    if types == 'subscription':
        msg.html = render_template('email/subscribe.html', name = name)

    elif types == 'contact':
        msg.html = render_template('email/hire_mail.html', name = name)

    elif types == 'hire':
        msg.html = render_template('email/hire_mail.html', name = name)


    mail.send(msg)
    return 

#inform mail
def inform_mail(data, types):

    msg = Message(data.fname + ' ' + types + ' request', sender = 'joshyjoy.dev@gmail.com', recipients = ['joshyjoy999@gmail.com'])

    msg.html = render_template('email/inform.html', data = data, types = types)

    mail.send(msg)
    return


#log recording
def add_log(log_id, event, msg):

    log = Logs(log_id, event,msg, False)
    db.session.add(log)
    db.session.commit()

    return 


#home route
#-------------------------------------------------------------------------------------------------------#
@app.route('/', methods = ['GET', 'POST'])
def home():

    projects = Project.query.all()


    return render_template('index.html', projects = projects)

#----------------------------------------------END----------------------------------------------------#



#route for the contact form
#-------------------------------------------------------------------------------------------------------#
@app.route('/contact', methods = ['GET', 'POST'])
def contact():

    if request.method == 'POST':
        fname = request.form['first-name']
        lname = request.form['last-name']
        email = request.form['email']
        ccode = request.form['pcode']
        phone = request.form['phone']
        phone = ccode + '-' + phone
        msg = request.form['message']

        contact = Contact(fname, lname, email, phone, msg)
        db.session.add(contact)
        db.session.flush()
        add_log(contact.id,'contact', fname + " contacted you")
        db.session.commit()

        send_mail(fname, email, 'contact')
        inform_mail(contact, 'contact')
        
        flash('Your valuable message is succesfully recieved. Thank you', 'success')

        return redirect(url_for('contact'))


    return render_template('contact.html')


#----------------------------------------------END----------------------------------------------------#



#route for downloading the resume
#-------------------------------------------------------------------------------------------------------#
@app.route('/download-cv')
def download_cv():

    filedir = os.path.abspath(os.path.dirname(__file__)) + '/static/docs/cv.pdf'
    return send_file(filedir, attachment_filename = 'resume.pdf')

#----------------------------------------------END----------------------------------------------------#



#route for hiring form
#-------------------------------------------------------------------------------------------------------#
@app.route('/hire', methods = ['GET', 'POST'])
def hire():

    if request.method == 'POST':

        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        company = request.form['company']
        buz = request.form['business']
        ccode = request.form['code']
        phone = request.form['phone']
        phone = ccode + '-' + phone
        country = request.form['country']
        project_type = request.form['project_type']
        paytype = request.form['budget_type']
        budget = request.form['budget']
        duration = request.form['duration']

        hire = Hire(fname, lname, email, company, buz, phone, country, project_type, paytype, budget, duration)
        db.session.add(hire)
        db.session.flush()
        add_log(hire.id,'hire', fname + " send you a hiring request")
        db.session.commit()

        send_mail(fname, email, 'hire')
        inform_mail(hire, 'hire')
        flash('Your request is recieved', 'success')

        return redirect(url_for('hire'))

    return render_template('hire.html')



#----------------------------------------------END----------------------------------------------------#




#route for blog
#-------------------------------------------------------------------------------------------------------#
@app.route('/blogs/<int:page_num>', methods = ['GET','POST'])
def blogs(page_num):

    try:
        recent = Blog.query.order_by(desc(Blog.date)).limit(6).all()
        tags = Blog.query.with_entities(Blog.tags).distinct().all()
        cat = Blog.query.with_entities(Blog.category).distinct().all()

        if recent:
            active = recent.pop(0)

        i = 0
        carousel = []
        while recent:
            if i>=2 or len(recent)<0:
                break
            carousel.append(recent.pop(0))
            i+=1
        
        popular = Blog.query.paginate(per_page = 10, page = page_num, error_out = True)
        
        if request.method == 'POST':

            search = request.form['search']
            return redirect(url_for('search', keyword = search, page_num = 1))

        return render_template('blog/blogs.html', active = active, carousel = carousel, recent = recent, popular = popular, tags = tags, cat = cat, active_page_num = page_num)
    
    except Exception as e:
        return render_template('error.html', error = '404')

#----------------------------------------------END----------------------------------------------------#


#route for category
#-------------------------------------------------------------------------------------------------------#
@app.route('/blogs/cat/<string:cattype>/<int:page_num>', methods = ['GET', 'POST'])
def category(cattype, page_num):

    cat_type = 'Category : ' + cattype
    recent = Blog.query.order_by(desc(Blog.date)).limit(6).all()
    tags = Blog.query.with_entities(Blog.tags).distinct().all()
    cat = Blog.query.with_entities(Blog.category).distinct().all()
    results = Blog.query.filter_by(category = cattype).paginate(per_page = 10, page = page_num, error_out = True)

    if recent:
        active = recent.pop(0)

    i = 0
    carousel = []
    while recent:
        if i>=2 or len(recent)<0:
            break
        carousel.append(recent.pop(0))
        i+=1
    
    if request.method == 'POST':

        search = request.form['search']
        return redirect(url_for('search', keyword = search, page_num = 1))

    return render_template('blog/blog_search.html',search_type = cat_type, active = active, carousel = carousel, recent = recent, tags = tags, cat = cat, results = results, active_page_num = page_num)




#----------------------------------------------END----------------------------------------------------#





#route for category
#-------------------------------------------------------------------------------------------------------#
@app.route('/blogs/tags/<string:tagtype>/<int:page_num>', methods = ['GET', 'POST'])
def tags(tagtype, page_num):

    tag_type = 'Tag : ' + tagtype
    recent = Blog.query.order_by(desc(Blog.date)).limit(6).all()
    tags = Blog.query.with_entities(Blog.tags).distinct().all()
    cat = Blog.query.with_entities(Blog.category).distinct().all()
    results = Blog.query.filter_by(tags = tagtype).paginate(per_page = 10, page = page_num, error_out = True)

    if recent:
        active = recent.pop(0)

    i = 0
    carousel = []
    while recent:
        if i>=2 or len(recent)<0:
            break
        carousel.append(recent.pop(0))
        i+=1
    
    if request.method == 'POST':

        search = request.form['search']
        return redirect(url_for('search', keyword = search, page_num = 1))

    return render_template('blog/blog_search.html',search_type = tag_type, active = active, carousel = carousel, recent = recent, tags = tags, cat = cat, results = results, active_page_num = page_num)





#----------------------------------------------END----------------------------------------------------#





#route for category
#-------------------------------------------------------------------------------------------------------#
@app.route('/blogs/search/<string:keyword>/<int:page_num>', methods = ['GET', 'POST'])
def search(keyword, page_num):

    search_type = 'Search : ' + keyword
    recent = Blog.query.order_by(desc(Blog.date)).limit(6).all()
    tags = Blog.query.with_entities(Blog.tags).distinct().all()
    cat = Blog.query.with_entities(Blog.category).distinct().all()
    results = Blog.query.filter(Blog.content.like("%"+keyword+"%")).paginate(per_page = 10, page = page_num, error_out = True)

    if recent:
        active = recent.pop(0)

    i = 0
    carousel = []
    while recent:
        if i>=2 or len(recent)<0:
            break
        carousel.append(recent.pop(0))
        i+=1
    
    if request.method == 'POST':

        search = request.form['search']
        return redirect(url_for('search', keyword = search, page_num = 1))

    return render_template('blog/blog_search.html',search_type = search_type, active = active, carousel = carousel, recent = recent, tags = tags, cat = cat, results = results, num_result = len(results.items), active_page_num = page_num)




#----------------------------------------------END----------------------------------------------------#




#route for displaying the post
#-------------------------------------------------------------------------------------------------------#
@app.route('/blog-page/<int:id>', methods = ['GET', 'POST'])
def blog_page(id):

    blog = Blog.query.filter_by(id = id).first()
    results = Blog.query.filter_by(category = blog.category).limit(5).all()

    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('search', keyword = search, page_num = 1))

    return render_template('blog/blog_page.html', blog = blog, results = results)



#----------------------------------------------END----------------------------------------------------#

@app.route('/subscribe/<string:page>', methods = ['GET', 'POST'])
def subscription(page):

    if request.method == 'POST':
        email = request.form['email']

        subscribe = Subscribe(email)
        db.session.add(subscribe)
        db.session.commit()


        name = email.split('@')
        send_mail(name[0], email, 'subscription')

        if page == 'blogs':
            return redirect(url_for(page, page_num = 1))
        else:
            return redirect(url_for(page))





