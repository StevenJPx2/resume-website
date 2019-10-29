from app import app
from flask import render_template, url_for, redirect, request, abort, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.forms import ContactForm, LoginForm, BlogPostForm, ProjectPostForm
from app.models import BlogPost, ProjectPost, User, process_body, Image
from app.bucket import preprocess_img_and_upload
from app.utils import truncate_all, create_new_admin, placeholder, truncate_blog_posts

import os
import requests
import json
from tqdm import tqdm

PER_PAGE = app.config['POSTS_PER_PAGE']

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	posts = [project for project in ProjectPost.objects]
	blog_post = BlogPost.objects.first()
	form = ContactForm()
	if form.validate_on_submit():
		return redirect(url_for('index'))

	return render_template('index.html', form=form, posts=posts, blog_post=blog_post)

@app.route('/blog')
def blog():
	page = request.args.get("n") or 1
	paginated = BlogPost.objects.paginate(page=page, per_page=PER_PAGE)
	posts_n = BlogPost.objects.count()
	next_url = url_for('index', page=paginated.next_num) if paginated.has_next else None
	prev_url = url_for('index', page=paginated.prev_num) if paginated.has_prev else None

	return render_template('blog_main.html', posts=paginated.items, posts_n=posts_n,next=next_url, prev=prev_url)

@app.route('/b/<post_hash>')
def blog_post(post_hash):
	post = BlogPost.objects.get_or_404(pk=post_hash)
	return render_template("blog_post.html", post=post)

@app.route('/b/archive')
def blog_archive():
	posts = BlogPost.objects
	return render_template("blog_archive.html", posts=posts)

@app.route('/b/archive/<date>')
def blog_archive_date(date):
	posts = BlogPost.objects
	return render_template("blog_archive.html", posts=posts)

@app.route('/projects')
def project_main():
	posts = ProjectPost.objects.order_by("last_updated")
	return render_template("project_main.html", posts=posts)

@app.route('/p/<post_hash>')
def project_post(post_hash):
	post = BlogPost.objects.get_or_404(pk=post_hash)	
	return render_template('project_post.html', post=post)

@app.route('/admin')
@app.route('/admin/')
@login_required
def admin_main():
	b_c = BlogPost.objects.count()
	p_c = ProjectPost.objects.count()
	return render_template('admin_main.html', op='main', b_c=b_c, p_c=p_c, title="Main")

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.objects(username=form.username.data).first()
		if user is None or not user.check_pass(form.password.data):
			flash(f'Invalid: {user}')
			return redirect(url_for('admin_login'))

		login_user(user)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			return redirect(url_for('admin_main'))
		return redirect(next_page)

	return render_template('admin_login.html', form=form, op='login', title="Login")

@app.route('/admin/post', methods=['GET', 'POST'])
def admin_post():
	post_type = request.args.get("post_type") or abort(404)
	_type = request.args.get("type") or abort(404)
 
	if post_type == 'b':
		form = BlogPostForm()
		op = 'blog'
	elif post_type == 'p':
		form = ProjectPostForm()
		op = 'project'
	else:
		abort(404)

	if _type != 'c':
		post = BlogPost.objects.get_or_404(pk=_type) if post_type == 'b' else ProjectPost.objects.get_or_404(pk=_type)

	if form.validate_on_submit():
		if _type == 'c':
			if post_type == 'b':
				post = BlogPost(title=form.title.data)
			else:
				post = ProjectPost(title=form.title.data)
				post.github_url = form.github_url.data
			
			post.save()
			imgs = [Image(**preprocess_img_and_upload(img, post.pk)) for img in form.imgs.data]
			cover_img = Image(**preprocess_img_and_upload(form.cover_img.data, post.pk)) if form.cover_img.data else placeholder()


   
		else:
			if post_type == 'b':
				post = BlogPost.objects.get_or_404(pk=_type)
				post.update(title=form.title.data)
			else:
				post = ProjectPost.objects.get_or_404(pk=_type)
				post.update(
        				title=form.title.data,
						github_url=form.github_url.data
            	)
			post.save()
			imgs = post.imgs + [Image(**preprocess_img_and_upload(img, post.pk)) for img in form.imgs.data] if not form.imgs.data else post.imgs
			cover_img = Image(**preprocess_img_and_upload(form.cover_img.data, post.pk)) if form.cover_img.data else post.cover_img

   

		body = process_body(imgs, form.body.data)
		post.update(
			cover_img=cover_img,
			imgs=imgs,
			body=body
		)
		post.save()
  
		flash('Post uploaded successfully!')
		redirect(url_for('blog_post' if post_type == 'b' else 'project_post', post_hash=post.pk))

	if _type == 'c':
		post = None
	
	return render_template('admin_post.html', form=form, title="Post", op=op, 
                        type=_type, post=post)

@app.route('/admin/list', methods=['GET', 'POST'])
def admin_list():
	post_type = request.args.get("post_type") or abort(404)
	page = request.args.get("n") or 1

	if post_type == 'b':
		posts = BlogPost.objects.paginate(page=page, per_page=PER_PAGE)
		title = "Blog Posts"
		op = 'blog'
  
	elif post_type == 'p':
		posts = ProjectPost.objects.paginate(page=page, per_page=PER_PAGE)
		title = "Project Posts"
		op = 'project'
	
	else:
		abort(404)
  
	next_url = url_for('index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
 
 
	return render_template('admin_list_posts.html', posts=posts.items, title=title,
						next_url=next_url, prev_url=prev_url, op=op, post_type=post_type)

@app.route('/admin/view/<post_type>/<post_hash>', methods=['GET', 'POST'])
def admin_view(post_type, post_hash):
	if post_type == 'b':
		post = BlogPost.objects.get_or_404(pk=post_hash)
		op = 'blog'
	elif post_type == 'p':
		post = ProjectPost.objects.get_or_404(pk=post_hash)
		op = 'project'
	else:
		abort(404)
  
	return render_template('admin_view_post.html', post=post, op=op, title="View Post")
 
@app.template_filter('autoversion')
def autoversion_filter(filename):

	fullpath = os.path.join('app/', filename[1:])
	try:
		timestamp = str(os.path.getmtime(fullpath))
	except OSError:
		return filename
	newfilename = "{0}?v={1}".format(filename, timestamp)
	return newfilename
