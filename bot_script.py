import json
import random
from faker import Faker

with open("config.json", "r") as config_file:
    config = json.load(config_file)

number_of_users = config["number_of_users"]
max_posts_per_user = config["max_posts_per_user"]
max_likes_per_user = config["max_likes_per_user"]

fake = Faker()

# Create users
users = []
for i in range(number_of_users):
    user = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    users.append(user)

# Creating posts and likes
for user in users:
    num_posts = random.randint(1, max_posts_per_user)
    for _ in range(num_posts):
        post = {
            "user": user["username"],
            "content": fake.paragraph(),
        }
        # We receive a random number of likes per post
        num_likes = random.randint(1, max_likes_per_user)
        post["likes"] = num_likes

        print(f"A post has been created: {post}")
        for _ in range(num_likes):
            print(f"Like from {fake.user_name()}")
