from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import 	SocketIO, send, emit, join_room, leave_room
# from passlib.hash import pbkdf2_sha256
import string
import random

from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)

# # Configure database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gpazyzbxlqeeof:dff845d894a7a9c5ba972a147f35255d36ecbe560092c90a15cc8f5174083088@ec2-35-169-184-61.compute-1.amazonaws.com:5432/d343dtd9u9opg0'
# db = SQLAlchemy(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'secret!'

# Configure flask login
login = LoginManager(app)
login.init_app(app)

ROOMS = {}
NUM_PLAYERS = {}
GAMES = {}

ROOM_CODE_LENGTH = 6
random.seed()

@login.user_loader
def load_user(user_id):
	username = user_id[:-ROOM_CODE_LENGTH]
	room_code = user_id[-ROOM_CODE_LENGTH:]
	if room_code in ROOMS and username in ROOMS[room_code]:
		return User(username=username, room=room_code)
	return None
	# user_object = User()
	# return user_object
	# return User.query.get(int(id))

@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def index():
	# reg_form = RegistrationForm()
	return render_template("index.html")
	# join_room_form = JoinRoomForm()
	# print(join_room_form.validate_on_submit())
	# print(join_room_form.room_code.data, join_room_form.username.data)
	# print(join_room_form.room_code.errors, join_room_form.username.errors)
	# if join_room_form.room_code.data in ROOMS and join_room_form.username.data not in ROOMS[join_room_form.room_code.data]:
	# 	# user_object = User()
	# 	# login_user(user_object
	# 	ROOMS[join_room_form.room_code.data].append(join_room_form.username.data)
	# 	flash("Yeeeee lets go!", 'success')
	# 	return redirect(url_for("play", room_code=join_room_form.room_code.data))
	# # if join_room_form.room_code.data not in ROOMS:
	# # 	print("Got here", join_room_form.room_code.data, ROOMS)
	# # 	join_room_form.room_code.errors = ("Room code not valid",)
	# # if join_room_form.room_code.data in ROOMS and join_room_form.username.data in ROOMS[join_room_form.room_code.data]:
	# # 	join_room_form.username.errors = ("This username is taken",)
	# return render_template("index.html", form=join_room_form)


	# 	return redirect(url_for('login'))
	# if reg_form.validate_on_submit():
	# 	username = reg_form.username.data
	# 	password = reg_form.password.data

	# 	hashed_pswd = pbkdf2_sha256.hash(password)
	# 	# pbkdf2_sha256.using(rounds=29000,salt_size=16).hash(password) 29000 iterations and 16 bytes are default to edit use commented code


	# 	# Check username exists
	# 	# user_object = User.query.filter_by(username=username).first() # could also use .all() but there should only be 1
	# 	# if user_object:
	# 	# 	return "Someone else has taken this username"

	# 	user = User(username=username, password=hashed_pswd)
	# 	db.session.add(user)
	# 	db.session.commit()
	# 	flash("Registered sucessfully. Please login.", 'success')


@app.route("/joinroom", methods=['GET', 'POST'])
def joinroom():
	join_room_form = JoinRoomForm()
	# print(join_room_form.validate_on_submit())
	# print(join_room_form.room_code.data, join_room_form.username.data)
	# print(join_room_form.room_code.errors, join_room_form.username.errors)
	if not join_room_form.validate_on_submit():
		# print("Got here")
		return render_template("joinroom.html", form=join_room_form)
	if join_room_form.room_code.data in ROOMS and join_room_form.username.data not in ROOMS[join_room_form.room_code.data]:
		# user_object = User()
		# login_user(user_object
		ROOMS[join_room_form.room_code.data].append(join_room_form.username.data)
		print(join_room_form.room_code.data)
		# flash("Yeeeee lets go!", 'success')
		user_object = User(username=join_room_form.username.data, room=join_room_form.room_code.data)
		login_user(user_object)
		return redirect(url_for("play", room_code=join_room_form.room_code.data))
	if join_room_form.room_code.data not in ROOMS:
		print(ROOMS)
		# print("Got here", join_room_form.room_code.data, ROOMS)
		join_room_form.room_code.errors = ("Room code not valid",)
	if join_room_form.room_code.data in ROOMS and join_room_form.username.data in ROOMS[join_room_form.room_code.data]:
		join_room_form.username.errors = ("This username is taken",)
	return render_template("joinroom.html", form=join_room_form)

@app.route("/createroom", methods=['GET', 'POST'])
def createroom():
	create_room = CreateRoomForm()
	validNum = True
	try:
		numplayers = int(create_room.numplayers.data)
	except:
		validNum = False
	if create_room.validate_on_submit() and validNum and 2 <= int(create_room.numplayers.data) <= 10:
		firstIter = True
		while firstIter or room_code in ROOMS:
			room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=ROOM_CODE_LENGTH))
			firstIter = False
		user_object = User(username=create_room.username.data, room=room_code)
		login_user(user_object)
		ROOMS[room_code] = [create_room.username.data]
		NUM_PLAYERS[room_code] = int(create_room.numplayers.data)
		return redirect(url_for("play", room_code=room_code))
	if create_room.numplayers.data and (not validNum or not (2 <= int(create_room.numplayers.data) <= 10)):
		create_room.numplayers.errors = ("The number of players must be between 2 and 10",)
	return render_template("createroom.html", form=create_room)


@app.route("/login", methods = ['GET', 'POST'])
def login():
	login_form = LoginForm()

	if login_form.validate_on_submit():
		user_object = User.query.filter_by(username=login_form.username.data).first()
		login_user(user_object)
		return redirect(url_for('play'))
		# if current_user.is_authenticated:
		# 	return "Logged in yay!!!"
		# return "Not logged in"

	return render_template("login.html", form=login_form)

@app.route("/play<room_code>", methods = ['GET', 'POST'])
# @login_required
def play(room_code):
	if room_code not in ROOMS:
		flash("Please use a valid room code")
		return redirect(url_for('joinroom', room_code=room_code))
	if not current_user.is_authenticated:
		# print("Something happened again")
		flash("Please create a username to enter this room.", 'danger')
		return redirect(url_for('createusername', room_code=room_code))

	# join_room(room_code, sid=request.sid, namespace="/")

	# print(f"\n\nYou have joined this {room_code} bitch \n\n")
	return render_template("play.html", username=current_user.username)
	# return f"Ready to play at room {room_code}?"

@app.route("/createusername<room_code>", methods = ['GET', 'POST'])
def createusername(room_code):
	create_user = CreateUsernameForm()
	# print(create_user.validate_on_submit())
	# print(create_user.username.data)
	if create_user.validate_on_submit() and create_user.username.data not in ROOMS[room_code]:
		user_object = User(username=create_user.username.data, room=room_code)
		login_user(user_object)
		ROOMS[room_code].append(create_user.username.data)
		print("Joined room")
		return redirect(url_for('play', room_code=room_code))
	if create_user.username.data and create_user.username.data in ROOMS[room_code]:
		# print("This username is taken ", current_user.username.data)
		create_user.username.errors = ("This username is taken",)
	# print(f"The errors are {create_user.username.errors}")
	return render_template("createusername.html", form=create_user, room_code=room_code)


@app.route("/logout", methods=['GET'])
def logout():
	print(current_user)
	ROOMS[current_user.room].remove(current_user.username)
	leave_room(current_user.room, sid=current_user.username + current_user.room, namespace="/")
	logout_user()
	flash("You have logged out successfully", 'success')
	return redirect(url_for('index'))



def find_value(card):
	if card >= 52:
		return 0
	elif card == 38 or card == 51:
		return -1
	else:
		return (card % 13) + 1


@socketio.on('message')
def message(data):
	print(f"\n\n{data}\n\n")
	send(data)

@socketio.on('start_game')
def start_game(data):
	room = current_user.room
	print(f"{current_user.username} in {current_user.room} {data}")
	join_room(room)
	if NUM_PLAYERS[room] == len(ROOMS[room]):
		if room not in GAMES:
			cards = [i for i in range(54)]
			random.shuffle(cards)
			board = []
			board = cards[:4 * NUM_PLAYERS[room]]
			cards = cards[4 * NUM_PLAYERS[room]:]
			index = 0
			player = ROOMS[room][0]
			GAMES[room] = [board, cards, index, 0, False]
			print(GAMES[room])
			# my_event(data)
			emit('make board drawcard', {'board': board, 'players': ROOMS[room]}, room=room)
			emit('load game drawcard', {'board': board, 'drawn card': cards[index], 'player': 0, 'players': ROOMS[room], 'firsttime': True}, room=room)
			# print("Emitted start_game data", data)
		else:
			board = GAMES[room][0]
			cards = GAMES[room][1]
			index = GAMES[room][2]
			player = GAMES[room][3]
			print(GAMES[room])
			emit('make board drawcard', {'board': board, 'players': ROOMS[room]}, room=room)
			emit('load game drawcard', {'board': board, 'drawn card': cards[index], 'player': player, 'players': ROOMS[room], 'firsttime': False}, room=room)

	else:
		print(f"{current_user.username} has joined the room but the game has not started")

@socketio.on('selected_card')
def selected_card(data):
	print(f"\n\n\n\nWe fuckin did it!!!\n\n\n\n")

	room = current_user.room
	player_index = ROOMS[room].index(current_user.username)
	cards = GAMES[room][1]
	player_board = GAMES[room][0][4 * player_index: 4 * player_index + 4]
	drawn_card = cards[GAMES[room][2]]
	if data < 4:
		played_card = player_board[data]
		player_board[data] = drawn_card
	else:
		played_card = drawn_card
	GAMES[room][0][4 * player_index: 4 * player_index + 4] = player_board
	GAMES[room][3] = player_index
	print(f"\n\n\n\nI have selected the card {GAMES[room][0]}, {played_card}\n\n\n\n")
	emit('create board playcard', {'board': GAMES[room][0], 'players': ROOMS[room], 'player': player_index, 'played card': played_card}, room=room)

@socketio.on('freeze_flip_cards')
def freeze_flip_cards(data):
	room = current_user.room
	GAMES[room][4] = data['player']

@socketio.on('flipped_card')
def flipped_card(data):
	room = current_user.room
	if GAMES[room][4] != False and GAMES[room][4] == data['player']:
		GAMES[room][0] = data['board']
		GAMES[room][4] = False
	if GAMES[room][4] == False:
		GAMES[room][0] = data['board']

	emit('create board playcard', {'board': GAMES[room][0], 'players': ROOMS[room], 'player': GAMES[room][3], 'played_card': played_card}, room=room)

@socketio.on('next_round')
def next_round(data):
	room = current_user.room
	GAMES[room][0] = data['board']
	GAMES[room][2] += 1
	if GAMES[room][2] >= len(GAMES[room][1]):
		cards = [i for i in range(54) if i not in GAMES[room][0]]
		random.shuffle(cards)
		GAMES[room][1] = cards
		GAMES[room][2] = 0
	GAMES[room][3] = (GAMES[room][3] + 1) % NUM_PLAYERS[room]
	board = GAMES[room][0]
	cards = GAMES[room][1]
	index = GAMES[room][2]
	player = GAMES[room][3]
	print(GAMES[room])
	emit('make board drawcard', {'board': board, 'players': ROOMS[room]}, room=room)
	emit('load game drawcard', {'board': board, 'drawn card': cards[index], 'player': player, 'players': ROOMS[room], 'firsttime': False}, room=room)




# @socketio.on('my event')
# def my_event(data):
# 	print("\n\nI got it yay!!!!!\n\n")
# 	name = current_user.username
# 	room = current_user.room
# 	print(f"\n\n\n\n\n\n {name} {room} \n\n\n\n\n\n{data}\n\n")
# 	send(f"Hello {current_user.username} playing in room {current_user.room}")

@socketio.on('connect')
def connect():
	send(current_user.username)

@app.route("/test", methods=['GET', 'POST'])
def test():
	return render_template('test.html')


if __name__ == '__main__':
	socketio.run(app, debug=True)
	app.run(debug=True)
