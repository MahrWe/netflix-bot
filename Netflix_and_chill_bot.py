# -*- coding: utf-8 -*-
from Telegram_bot import *
from db import DBMS
from omdb import omdb
from entry import Entry

class Netflix_and_chill_bot(Telegram_bot):
	## Constructor using superclass
	def __init__(self, Token):
		super(Netflix_and_chill_bot, self).__init__(Token)
		self.name = "NetflixAndChillBot"
		self.version = "4.0"
		self.db = DBMS.DBMS()

	def add_movie_to_db(self, movie, update):
		row = movie.as_row(update.message.chat_id)
		return self.db.insert_film(row)

	def delete_movie_from_db(self, movie, update):
		row = (update.message.chat_id, movie.ident)
		return self.db.delete_film(row)

	def add_movie(self, bot, update, args):
		if not args:
			bot.sendMessage(chat_id=update.message.chat_id, text='Please enter a name for the movie after the command')
			return
		movie = Entry(args)
		correctly_added = self.add_movie_to_db(movie, update)

		if not correctly_added:
			text_answer = "<< " + movie.name + " >>" + " already in your watchlist (or maybe a database problem)!"
			bot.sendMessage(chat_id=update.message.chat_id, text=text_answer)
			return

		if not movie.movie_found:
			bot.sendMessage(chat_id=update.message.chat_id, text='Unable to find <<' + movie.name + '>> in Internet Movie database, but it has still been added to your list!')
			return

		if movie.category != "null":
			text_answer = "<< " + movie.name + " >>" + " added to your watchlist inside the category: " + movie.category + "!"
		else:
			text_answer = "<< " + movie.name + " >>" + " added to your watchlist without category!"

		bot.sendMessage(chat_id=update.message.chat_id, text=text_answer)

	def respond_with_movie(self, bot, update, movie):
		chat_id = update.message.chat_id
		if movie.film.get_response() == "True":
			text = 'For request ' + movie.name + ', found:'
			bot.sendMessage(chat_id=chat_id, text=text)
			bot.sendMessage(chat_id=chat_id, text=movie.film.get_text_message())
			bot.sendPhoto(chat_id=chat_id, photo=film.get_poster())
			return True
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text='Unable to find <<' + movie.name + '>> in Internet Movie database')
			return False

	def get_info(self, bot, update, args):
		if not args:
			reply_markup = self.movie_keyboard(update.message.chat_id, 'i')
			text_answer = 'You may get info about any movie or series with:\n/getinfo <movie_name>\nor select one from list below.'
			update.message.reply_text(text_answer, reply_markup=reply_markup)
		else:
			movie = Entry(args)
 			self.respond_with_movie(bot, update, movie)

	def handle_callback(self, bot, update):
		query = update.callback_query
		bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
		if query.data[0] == 'i':
			movie = Entry([query.data[1:]])
			self.respond_with_movie(bot, query, movie)
		if query.data[0] == 'd':
			movie = Entry([query.data[1:]])
			correctly_deleted = self.delete_movie_from_db(movie, query)
			if correctly_deleted:
				text_answer = "<< " + movie.name + " >>" + " removed from watchlist!"
			else:
				text_answer = "<< " + movie.name + " >>" + " not in watchlist!"
			bot.sendMessage(chat_id=query.message.chat_id, text=text_answer)

	def movie_keyboard(self, chat_id, mode):
		keyboard = [[]]
		for index, movie in enumerate(self.db.get_rows(chat_id, 10000, "")):
			if not index%2:
				keyboard.append([InlineKeyboardButton(movie, callback_data=mode+movie)])
			else:
				keyboard[-1].append(InlineKeyboardButton(movie, callback_data=mode+movie))
		return InlineKeyboardMarkup(keyboard)

	def delete_movie(self, bot, update, args):
		if not args:
			reply_markup = self.movie_keyboard(update.message.chat_id, 'd')
			text_answer = 'Please select the movie you want to delete from your database'
			update.message.reply_text(text_answer, reply_markup=reply_markup)
		else:
			movie = Entry(args)
			correctly_deleted = self.delete_movie_from_db(movie, update)
			if correctly_deleted:
				text_answer = "<< " + movie.name + " >>" + " removed from watchlist!"
			else:
				text_answer = "<< " + movie.name + " >>" + " not in watchlist!"
			bot.sendMessage(chat_id=update.message.chat_id, text=text_answer)

	def tell_bernardo_i_want(self, bot, update, args):
		text_answer = "Bernardo, Katelyn says she wants " + ' '.join(args) + " ;)"
		bot.sendMessage(chat_id=update.message.chat_id, text=text_answer)

	def tell_Katelyn_i_want(self, bot, update, args):
		text_answer = "Katelyn, Bernardo says he wants " + ' '.join(args) + " ;)"
		bot.sendMessage(chat_id=update.message.chat_id, text=text_answer)

	## Main function #2, displays some (one or more ? ) movies to the user.
	def get_all_movies(self, bot, update, args):
		bot_text = "Here are all your movies-to-watch! \n"
		for movie in self.db.get_rows(update.message.chat_id, 10000, ""):
			bot_text += "* " + movie + '\n'

		bot.sendMessage(chat_id=update.message.chat_id, text=bot_text)

	## Main function #2, displays some (one or more ? ) movies to the user.
	def get_movies(self, bot, update, args):
		message = ' '.join(args)
		try:
			if len(message) == 0:
				number_of_movies = 1
				pass
			else:
				number_of_movies = int(message[0])
		except ValueError:
			bot.sendMessage(chat_id=update.message.chat_id, text=" \
				You should add a number after the get command...")
			return
		if len(args) > 2:
			bot.sendMessage(chat_id=update.message.chat_id, text=" \
				This function accepts two arguments as maximum...")
			return
		elif len(args) == 2:
			category = args[1]
			bot_text = "Here they are! the next " + category + " " + str(number_of_movies) + \
				" movies to watch ! \n"
		else:
			category = ""
			bot_text = "Here they are! the next " + str(number_of_movies) + \
				" movies to watch ! \n"
		for movie in self.db.get_rows(update.message.chat_id, number_of_movies, category):
			bot_text += "* " + movie + '\n'

		bot.sendMessage(chat_id=update.message.chat_id, text=bot_text)

	## List of functions to add to the bot!
	def add_functions(self):
		## Receives as parameter the name of the function and the command
		self.add_function(self.add_movie, "add")
		self.add_function(self.delete_movie, "delete")
		self.add_function(self.get_info, "getinfo")
		self.add_function(self.get_movies, "get")
		self.add_function(self.get_all_movies, "getall")
		self.add_callback_query(self.handle_callback)
		self.add_function(self.tell_bernardo_i_want, "tellBernardoIWant")
		self.add_function(self.tell_Katelyn_i_want, "tellKatelynIWant")


# ------------------------------------------------------------#
## Initialize bot by http token given by Telegram
token = ## Add your own Bottoken here!
bot = Netflix_and_chill_bot(token)
# ------------------------------------------------------------#

## Set-up start message (using super-class function)
start_message = '''Hi there :P I'm a bot designed for NetflixAndChill's \
hardest task, choosing what to watch! Talk to me for help!'''
bot.define_start_message(start_message)
# ------------------------------------------------------------#
## Set-up of functions
bot.add_functions()
# ------------------------------------------------------------#
## Set-up error handling message (non-existing function called)
## ATENTION ! ERROR MESSAGE SHOULD ALWAYS BE AT LAST !
error_message = "Sorry, I didn't understand that command."
bot.define_error_message(error_message)
# ------------------------------------------------------------#

## START RUNNING
bot.run()

# ------------------------------------------------------------#
