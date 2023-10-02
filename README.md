# Social Network

Social Network is a web application that simulates the functionalities of a social media system. It provides features for user registration, posting and liking posts. The project is built using Django REST framework.

## Features

- User Registration: Users can create accounts by providing a username, email, and password.

- User Authentication: Authentication is implemented using JSON Web Tokens (JWT). Registered users can obtain JWT tokens to access protected endpoints.

- Post Creation: Users can create posts with text content. Each post can include optional hashtags.

- Post Listing: Users can view a feed of posts. Posts can be filtered by hashtags.

- Post Likes: Users can like and unlike posts. The number of likes on each post is tracked.

- User Profiles: Each user has a profile with a profile picture, bio, and a list of followers.

- Follow/Unfollow Users: Users can follow and unfollow other users.


## Installation and Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/social-network.git
2. Navigate to the project directory:

   ```bash
   cd social-network
3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
4. Activate the virtual environment:

    ###### On Windows:
   ```
   venv\Scripts\activate
   ```
    ###### On macOS and Linux:
   ```
   source venv/bin/activate
   ```
5. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   
6. Apply migrations:

   ```bash
   python manage.py migrate

7. Create a superuser to access the admin panel (follow the prompts):

   ```bash
   python manage.py createsuperuser

8. Run the development server:

   ```bash
   python manage.py runserver

## Documentation
- Swagger UI: Access the interactive API documentation using Swagger UI at http://localhost:8000/api/doc/swagger/.
- ReDoc: Explore the API with ReDoc at http://localhost:8000/api/doc/redoc/.
