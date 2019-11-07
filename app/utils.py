import json
import os
import re
from zipfile import ZipFile

import requests
from tqdm import tqdm

from app import app
from app.models import BlogPost, DemoMeta, ProjectPost, User


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
 
def DemoMeta_from_config(config):
	config = json.loads(config)
	if config.get("HAS_ROUTES") is None:
		config["HAS_ROUTES"] = False
	
	return DemoMeta.from_json(config)

def preprocess_route_code(project_post_obj, route_code):
	all_routes = re.findall(r"@app\.route\('(/\S*',*.*)\)", route_code)
	for route in all_routes:
		print(route)
		print(f"@app.route('/p/{project_post_obj.pk}/live{route})")
		print(re.search(route, route_code))
		re.sub(route, f"@app.route('/p/{project_post_obj.pk}/live{route}')", route_code)
	
	all_defs = re.findall(r"def ([a-zA-Z_]+[\w]*\(([a-zA-Z_]+[\w]*[, [a-zA-Z_]+[\w]*]*)*\)):", route_code)
	for def_group in all_defs:
		print(def_group)
		print(f"_{project_post_obj.pk}_{def_group[0]}")
		print(re.search(def_group[0], route_code))
		re.sub(def_group[0], f"_{project_post_obj.pk}_{def_group[0]}", route_code)
	
	# print(route_code)
	return route_code

def block_code(project_post_obj, landing=None, route_code=None):
	if route_code:
		code = f"""
### {project_post_obj.title} - {project_post_obj.pk} - BLOCK STARTS""" + route_code + f"""
### {project_post_obj.pk} - BLOCK ENDS

"""
	else:
		code = f"""
### {project_post_obj.title} - {project_post_obj.pk} - BLOCK STARTS
@app.route(p/{project_post_obj.pk}/live/)
def _{project_post_obj.pk}_index():
	render_template('{landing}')
### {project_post_obj.pk} - BLOCK ENDS
"""
	return code
 
def plug_in_demo(file_zip, base_path, project_post_obj):
	with ZipFile(file_zip, 'r+') as zip:
		config = zip.read(f"{base_path}/live_config.json")
		meta = DemoMeta_from_config(config)
		project_post_obj.update(live_demo=meta)
		project_post_obj.save()
		if not meta.HAS_ROUTES:
			route_code = open("routes.py", "r").read()
			route_code += block_code(project_post_obj, meta.LANDING)
			
			zip.write(fp)
		else:
			route_code = open("routes.py", "r").read()
			route_code = preprocess_route_code(route_code)
			route_code += block_code(project_post_obj, zip.extract(meta.ROUTE_PATH))
			
			zip.write(fp)
