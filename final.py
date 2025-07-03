from flask import Flask, render_template, request,session ,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime


with open(r'Path to your config.json for detail read README.md', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER']=params['upload_location']

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD=  params['gmail_password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)



class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    if not post:  # Handle case where post is not found
        return "Post not found!", 404  # Return a valid HTTP response

    return render_template("post.html", params=params, post=post)



@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail_user']],
                          body = message + "\n" + phone
                          )
    return render_template('contact.html', params=params)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params,posts=posts)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get("pass")


        if username == params["admin_user"] and userpass == params["admin_password"]:
            session['user'] = username
            posts=Posts.query.all()
            return render_template("dashboard.html", params=params,posts=posts)
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", params=params)


@app.route("/edit/<string:sno>", methods=['POST', 'GET'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            # Get the form data
            title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == "0":
                # Create a new post
                post = Posts(title=title, slug=slug, content=content, date=date, tagline=tagline, img_file=img_file)
                db.session.add(post)
                db.session.commit()
                # Flash message (requires flash messages to be displayed in layout.html as discussed previously)
                flash("New post added successfully!", "success")
                # Redirect to the newly created post's edit page, or to the dashboard
                # Option A: Redirect to edit the newly created post (post.sno will now have the ID)
                return redirect(url_for('dashboard'))
                # Option B: Redirect to the dashboard
                # return redirect(url_for('dashboard'))
            else:
                # Update existing post
                post = Posts.query.filter_by(sno=sno).first()
                if post: # Ensure post exists before trying to update
                    post.title = title
                    post.slug = slug
                    post.content = content
                    post.img_file = img_file
                    post.date = date
                    db.session.commit()
                    flash("Post updated successfully!", "success")
                    return  redirect(url_for('dashboard')) # Stay on the edit page for the updated post
                else:
                    # If sno was provided but post not found (e.g., deleted by another admin)
                    flash("Post not found for editing!", "danger")
                    return redirect(url_for('dashboard'))

        else: # This block handles GET requests
            post = None # Default for new post or if not found
            if sno != "0":
                # If sno is not "0", try to fetch an existing post
                post = Posts.query.filter_by(sno=sno).first()
                if not post:
                    flash("Post not found.", "danger")
                    return redirect(url_for('dashboard')) # Redirect if trying to edit non-existent post

        return render_template("edit.html", params=params, sno=sno, post=post)

    # If user is not authorized, redirect them to dashboard/login
    flash("You must be logged in to access this page.", "warning")
    return redirect(url_for('dashboard')) # or url_for('dashboard') if that's your login page

@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            f = request.files['file1']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Upload successfully"
    return "Unauthorized"

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route("/delete/<string:sno>",methods=['GET','POST'] )
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')



app.run(debug=True)


