#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from werkzeug.security import generate_password_hash

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()

    print("Creating users...")

    # make sure users have unique usernames
    users = []
    usernames = []

    for i in range(20):
        
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        # Hash the password before saving
        password_hash = generate_password_hash(username + 'password')

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.url(),
            password_hash=password_hash,  # Use hashed password
        )

        users.append(user)

    db.session.add_all(users)

    print("Creating recipes...")
    recipes = []
    for i in range(100):
        instructions = fake.paragraph(nb_sentences=8)
        
        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15,90),
        )

        # Randomly assign a user to the recipe
        recipe.user = rc(users)

        recipes.append(recipe)

    db.session.add_all(recipes)
    
    db.session.commit()
    print("Complete.")
