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

def iter_replace(string, replace_list):
    for repl in replace_list:
        string = string.replace(*repl)
        
    return string
        
def iter_repl_bksl(string, replace_list):
    return iter_replace(string, [[repl, f"\\{repl}"] for repl in replace_list])

def preprocess_route_code(project_post_obj, route_code):
    for route in re.finditer(r"@app\.route\('(/\S*',*.*)\)", route_code):
        str_route = route.group()
        repl_str_route = iter_repl_bksl(str_route, "()[]")
        route_code = re.sub(repl_str_route, 
                            f"@app.route('/p/{project_post_obj.pk}/live{route.group(1)})", 
                            route_code)

    for def_group in re.finditer(r"def ([a-zA-Z_]+[\w]*\(([a-zA-Z_]+[\w]*[, [a-zA-Z_]+[\w]*]*)*\):)", route_code):
        str_def_group = def_group.group()
        repl_str_def_group = iter_repl_bksl(str_def_group, "()[]")
        route_code = re.sub(repl_str_def_group, 
                            f"def _{project_post_obj.pk}_{def_group.group(1)}", 
                            route_code)
    
    return route_code

def block_code(project_post_obj, landing=None, route_code=None):
    if route_code:
        code = f"""
### {project_post_obj.title} - {project_post_obj.pk} - BLOCK STARTS
""" + route_code + f"""
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
        if meta.HAS_ROUTES:
            route_code = open("routes.py", "r").read()
            zip_route = zip.read(f"{base_path}/{meta.ROUTE_PATH}")
            zip_route = preprocess_route_code(project_post_obj, zip_route)
            route_code += block_code(project_post_obj, route_code=zip_route)
            
            zip.write(fp)
        else:
            route_code = open("routes.py", "r").read()
            route_code += block_code(project_post_obj, meta.LANDING)
            
            zip.write(fp)
            
