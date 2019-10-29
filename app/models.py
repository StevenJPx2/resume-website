from hashlib import md5
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import app, db, login
from tqdm import tqdm
import re, requests

class Image(db.EmbeddedDocument):
    full = db.StringField(db_field="Full")
    post = db.StringField(db_field="Post")
    small_post = db.StringField(db_field="Small Post")
    small_thumb = db.StringField(db_field="Small Thumb")
    big_thumb = db.StringField(db_field="Big Thumb")
    
class Post(db.Document):
	title = db.StringField(db_field='Title', max_length=120, required=True)
	date = db.DateTimeField(db_field='Date', default=datetime.utcnow(), required=True)
	body = db.StringField(db_field='Body')
	cover_img = db.EmbeddedDocumentField(Image, db_field='Cover Image')
	imgs = db.ListField(db.EmbeddedDocumentField(Image, db_field='Images'))
 
	meta = {'allow_inheritance': True}
  
	def body_preview(self, n=45):
		return " ".join(self.body.split(" ")[:n]) + "..." if self.body else '...'
  
	def return_date(self):
		return (self.date.strftime("%a"), self.date.strftime("%b %d, %Y"))

	
class ProjectPost(Post):
	github_url = db.URLField(db_field='GitHub URL')
	last_updated = db.DateTimeField(db_field='Last Updated', default=datetime.utcnow())
 
	meta = {'ordering': ['-last_updated']}
	
 
class BlogPost(Post):
	meta = {'ordering': ['-date']}
	
	def return_ttr(self):
		return len(self.body.split()) // app.config["AVG_READING_SPEED"]
  
class User(UserMixin, db.Document):
	username = db.StringField(db_field='Username', required=True, unique=True)
	password = db.StringField(db_field='Password', unique=True)
	
	def set_pass(self, password):
		self.password = generate_password_hash(password)

	def check_pass(self, password):
		return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
	return User.objects(pk=id).first()

def process_body(imgs, body):
	pattern = r"!\[.*\]\(\d\)"
	for i in re.findall(pattern, body):
		number = int(i[-2])
		body = body.replace(i, f"{i[:-2]}{imgs[number].post})")

	return body