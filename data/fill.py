import random
import csv

# Clear all automatically generated data
def reset(path, lines):
	with open(path, "r") as file:
		contents = file.readlines()
	with open(path, "w") as file:
		file.writelines(contents[:lines])
reset("card_in_category.tsv", 1)
reset("card_in_deck.tsv", 15)
reset("categories.tsv", 5)
reset("deck.tsv", 5)
reset("flashcards.tsv", 12)
reset("session_decks.tsv", 1)
reset("sides.tsv", 23)
reset("spacings.tsv", 1)
reset("u_session.tsv", 1)
reset("user_decks.tsv", 14)
reset("user.tsv", 6)


decks = [
	{
		"id": 1,
		"name": "Trivia",
		"desc": "Random trivia facts (dates and names) from various categories",
		"cards": [1,3,4,10]
	}, {
		"id": 2,
		"name": "History",
		"desc": "Historical events",
		"cards": [3,4]
	}, {
		"id": 3,
		"name": "Computer Science",
		"desc": "Computer/programming related questions",
		"cards": [2,5,6,7,8,9]
	}, {
		"id": 4,
		"name": "Traditional Science",
		"desc": "Questions about biology, physics, etc.",
		"cards": [1,11]
	}
]

def make_copies(path, n):
	new_copies = []
	with open(path, "r") as source:
		source_array = list(csv.reader(source, delimiter="\t"))[1:] # ignore header
		l = len(source_array)
		# Check that you're not grabbing an empty newline
		if(len(source_array[-1]) != 0):
			current_id = int(source_array[-1][0]) + 1
		else:
			current_id = int(source_array[-2][0]) + 1

		for i in range(n):
			rand_index = random.randrange(0, l)
			# for sides, makes sure fronts stay fronts and backs stay backs
			if(rand_index % 2 != i % 2):
				if(rand_index == 0):
					rand_index += 1
				else:
					rand_index -= 1
			new_copy = source_array[rand_index][1:] # ignore that ones id
			new_copies.append([current_id] + new_copy)
			current_id += 1
	return new_copies

def rand(start, stop):
	return random.randrange(start, stop)

num_copies = 100
# Make new sides
new_sides = make_copies("sides.tsv", int(num_copies * 2))
# print(new_sides)

# Make new decks and categories (nothing assigned yet)
new_decks = make_copies("deck.tsv", int(num_copies/5))
new_categories = make_copies("categories.tsv", int(num_copies / 5))

# Make arr for new category and deck links and spacings and cards
new_card_category_links = []
new_card_deck_links = []
new_spacings = []
new_cards = []
# Get the id for the first new card by using the other 
# copy method to do the same and only keep the id part
card_id = make_copies("flashcards.tsv", 1)[0][0] + 1

# For each front/back side made, generate a card
for front, back in zip(new_sides[::2], new_sides[1::2]):
	# make a new card with a unique id, and the id's of the front/back
	new_card = [card_id, front[0], back[0], rand(0, 50), rand(0, 50)]
	new_cards.append(new_card)
	# generate a random number of decks for it to be in
	deck_count = rand(1,3)
	for i in range(deck_count):
		new_card_deck_links.append([card_id, random.choice(new_decks)[0]])
	# same for categories
	category_count = rand(0,5)
	for i in range(category_count):
		new_card_category_links.append([card_id, random.choice(new_categories)[0]])

	# add spacings for the card 
	for i in range(5):
		spacing_id = len(new_spacings) + 1
		interval = rand(5, 10)
		# ef should range from 1.1 to 2.5
		ef = f"{random.random() * 1.4 + 1.1:.4}"
		new_spacings.append([spacing_id, card_id, interval, ef])

	card_id += 1

# make a bunch of new users
new_users = make_copies("user.tsv", int(num_copies))
new_user_decks = []
new_sessions = []
new_session_decks = []
for user in new_users:
	user_id = user[0]
	# assign decks to them
	deck_count = rand(1,5)
	for i in range(deck_count):
		new_user_decks.append([user_id,random.choice(new_decks)[0]])

	# Generates sessions for them
	for i in range(5):
		session_id = len(new_sessions) + 1
		date = f"{rand(2020, 2023)}-{rand(0,13)}-{rand(0,30)}"
		correct_ratio = f"{random.random():.3}"
		new_sessions.append([session_id, date, correct_ratio, user_id])
		# assign some decks to those sessions
		for j in range(rand(1,3)):
			new_session_decks.append([session_id, random.choice(new_decks)[0]])

# Function to turn the arrays into rows of strings and write them all
def write(path, arr):
	# with open(path, "r") as file:
	# 	has_newline = file.readlines()[-1] == '\n'
	with open(path, "a") as file:
		# if(not has_newline):
		# 	file.write("\n")
		for row in arr:
			# maps values to strings first, then joins them with tabs, and appends a newline
			file.write("\t".join(map(lambda x: str(x), row)) + "\n")
			# print("\t".join(map(lambda x: str(x), row)))


write("card_in_category.tsv", new_card_category_links)
write("card_in_deck.tsv", new_card_deck_links)
write("categories.tsv", new_categories)
write("deck.tsv", new_decks)
write("flashcards.tsv", new_cards)
write("session_decks.tsv", new_session_decks)
write("sides.tsv", new_sides)
write("spacings.tsv", new_spacings)
write("u_session.tsv", new_sessions)
write("user_decks.tsv", new_user_decks)
write("user.tsv", new_users)