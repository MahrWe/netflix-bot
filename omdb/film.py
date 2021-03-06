class Film:
	def __init__(self, data):
		self.data = data

	def get_title(self): return self.data['Title']
	def get_genre(self): return self.data['Genre']
	def get_imdb_rating(self): return self.data['imdbRating']
	def get_id(self): return self.data['imdbID']
	def get_poster(self): return self.data['Poster']
	def get_description(self): return self.data['Plot']
	def get_director(self): return self.data['Director']
	def get_text_message(self): return 'Title: ' + self.data['Title'] + '\nGenre: ' + self.data['Genre'] + '\nIMDB Rating: ' + self.data['imdbRating'] + '\nDescription: ' + self.data['Plot']
	def get_response(self): return self.data['Response']