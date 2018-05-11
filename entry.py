import re
from omdb import omdb

# From https://www.wikidata.org/wiki/Property:P345
pattern = re.compile('ev\d{7}\/(19|20)\d{2}(-\d)?|(ch|co|ev|nm|tt)\d{7}|ni\d{8}')
class Entry:

    def __init__(self, args):
        movie = ' '.join(args)

        # users last word with caps means adding a category!
        self.category = "null"
        if len(args) > 1:
            if args[-1] == args[-1].upper():  # is written in caps?
                self.category = args[-1]
                movie = ' '.join(args[:-1])

        self.ident = "null"
        if self.is_movie_id(movie):
            self.ident = movie
            self.film = omdb.get_film_by_id(self.ident)
            if self.film.get_response() == "True":
                self.name = self.film.get_title()
        else:
            self.name = movie
            self.film = omdb.get_film_by_title(self.name)
            if self.film.get_response() == "True":
                self.ident = self.film.get_id()
        if not self.ident:
            self.ident = hash(self.name)

    def is_movie_id(self, movie):
        return pattern.match(movie)

    def movie_found(self):
        return pattern.match(self.ident)

    def as_row(self, chat_id):
        return (chat_id, self.ident, self.name, self.category)

    def get_priority(self, movie_name):
        return 1  # TODO Fix in a proper way...
