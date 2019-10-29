import requests
from tqdm import tqdm
from app.models import User, ProjectPost, BlogPost
from app import app

def placeholder():
	url = f"https://api.unsplash.com/photos/random/?client_id={app.config['UNSPLASH_ACCESS_KEY']}"
	raw_url = requests.get(url).json()["urls"]["raw"] + "fm=jpg&q=90"
	specs = {}
	for size, format in zip(app.config["IMAGE_SIZES"], app.config["IMAGE_SIZE_FORMAT"]):
		if type(size) == tuple:
			w, h = size 
			specs[format] = raw_url + f"&w={w}&h={h}"
		else:
			specs[format] = raw_url
	return specs

def truncate_all():
	truncate_admin_data()
	truncate_blog_posts()
	truncate_project_posts()
	print("Deleted all records")

def truncate_blog_posts():
	BlogPost.objects.delete()
	print("Deleted all blog post records")

def truncate_project_posts():
	ProjectPost.objects.delete()
	print("Deleted all project post records")

def truncate_admin_data():
	User.objects.delete()
	print("Deleted all user records")

def create_new_admin(username, password):
	user = User(username)
	user.set_pass(password)
	user.save()
	print("Created admin account.")