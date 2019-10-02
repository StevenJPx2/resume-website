from hashlib import md5
from datetime import datetime
from app import app

class Post:
	def __init__(self):
		self.title = "Finished my most anticipated project!"
		self.date = "Sep 9, 2019" #datetime.utcnow()
		self.body = '''Ut placet, inquam tum dicere exorsus est laborum et dolorum effugiendorum gratia  
		placet, inquam tum dicere exorsus est cur verear, ne ferae quidem se esse expetendam et 
		caritatem, quae ab eo delectu rerum, quem ad respondendum reddidisti quorum facta quem ad id 
		ne ad.
		Torquatos nostros? quos dolores suscipiantur maiorum dolorum fuga et quasi involuta aperiri, 
		altera prompta et aut contra sit, voluptatem accusantium doloremque laudantium, totam rem voluptas 
		expetenda, fugiendus dolor sit, a natura incorrupte atque insitam in culpa, qui studiose antiqua 
		persequeris, claris et quale sit sentiri.
		Torquatos nostros? quos tu tam inportuno tamque crudeli; sin, ut labore et accurate disserendum et 
		harum quidem exercitus quid ex ea voluptate velit esse, quam nihil est, qui officia deserunt mollitia 
		animi, id totum evertitur eo est cur verear, ne interiret at magnum periculum adiit. Ut placet, inquam
		tum dicere exorsus est laborum et dolorum effugiendorum gratia  placet, inquam tum dicere exorsus est
		cur verear, ne ferae quidem se esse expetendam et caritatem, quae ab eo delectu rerum, quem ad 
		respondendum reddidisti quorum facta quem ad id ne ad.
		Torquatos nostros? quos dolores suscipiantur maiorum dolorum fuga et quasi involuta aperiri, altera 
		prompta et aut contra sit, voluptatem accusantium doloremque laudantium, totam rem voluptas expetenda,
		fugiendus dolor sit, a natura incorrupte atque insitam in culpa, qui studiose antiqua persequeris,
		claris et quale sit sentiri.
		Torquatos nostros? quos tu tam inportuno tamque crudeli; sin, ut labore et accurate disserendum 
		et harum quidem exercitus quid ex ea voluptate velit esse, quam nihil est, qui officia deserunt 
		mollitia animi, id totum evertitur eo est cur verear, ne interiret at magnum periculum adiit. Ut 
		placet, inquam tum dicere exorsus est laborum et dolorum effugiendorum gratia  placet, inquam tum 
		dicere exorsus est cur verear, ne ferae quidem se esse expetendam et caritatem, quae ab eo delectu 
		rerum, quem ad respondendum reddidisti quorum facta quem ad id ne ad.'''
		self.body_preview = "".join(self.body.split()[:45]) + "..."
		self.img = []
		self.ttr = len(self.body.split()) // app.config["AVG_READING_SPEED"]
		self.hash = md5((self.title + self.date).encode())