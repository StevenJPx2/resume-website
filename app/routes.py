from app import app
from flask import render_template, url_for, redirect, request
from app.forms import ContactForm
from app.models import Post

import os
import requests
import json
from tqdm import tqdm

NO_OF_IMAGES = app.config['NO_OF_PLACEHOLDER_IMAGES']

def placeholder(count=1):
    url = f"https://api.unsplash.com/photos/random/?client_id={app.config['UNSPLASH_ACCESS_KEY']}&count={count}"
    photo_url = [photo["urls"] for photo in tqdm(requests.get(url).json())]
    return photo_url

if 'unsplash_img_urls.json' in os.listdir('app/static'):
    unsplash_img_urls = json.load(open('app/static/unsplash_img_urls.json', 'r'))
    diff = len(unsplash_img_urls) - NO_OF_IMAGES
    if diff < 0:
        unsplash_img_urls += placeholder(int(diff*-1))
    json.dump(unsplash_img_urls, open('app/static/unsplash_img_urls.json', 'w'), indent=4)
    
else: 
    unsplash_img_urls = placeholder(NO_OF_IMAGES)
    json.dump(unsplash_img_urls, open('app/static/unsplash_img_urls.json', 'w'), indent=4)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    img_urls = {
        "card_thumb" : [unsplash_img_urls[0]["small"],
                        unsplash_img_urls[1]["small"]]
    }
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('index.html', form=form, img_urls=img_urls)


@app.route('/blog')
def blog():
    img_urls = {
        "header" : unsplash_img_urls[2]["full"],
        "blog_post" : [unsplash_img_urls[i]["regular"] for i in range(3, NO_OF_IMAGES)]
    }
    blog_n = len(img_urls["blog_post"])
    return render_template('blog.html', img_urls=img_urls, blog_n=blog_n)

@app.route('/post/<post_hash>')
def blog_post(post_hash):
    post = Post()
    head_pic = unsplash_img_urls[int(request.args.get("n"))]["full"]
    return render_template("blog_post.html", post=post, head=head_pic)

@app.template_filter('autoversion')
def autoversion_filter(filename):
    # determining fullpath might be project specific
    fullpath = os.path.join('app/', filename[1:])
    try:
        timestamp = str(os.path.getmtime(fullpath))
    except OSError:
        return filename
    newfilename = "{0}?v={1}".format(filename, timestamp)
    return newfilename
