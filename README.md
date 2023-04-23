# Intellivision

Running the Django Project with Docker Compose
This project is set up to run using Docker Compose, which makes it easy to set up and run the project in a consistent environment. To get started, follow these steps:

Install Docker Compose on your machine if you haven't already. You can download it from the official Docker website.

Clone the repository and cd into the project directory.

Create a .env file in the root directory of the project, and set the required environment variables for your Django project. Here is an example of what your .env file could look like:


OPENAI_API_KEY=sk-iATU8KkSH0HrUcUyds3RT3BlbkFJ



Build the Docker images and start the services by running the following command:

docker-compose up --build


This will start the Django development server and PostgreSQL database in separate containers. You should be able to access the Django project at http://localhost:8000.

To stop the services, run the following command:

docker-compose down


Using Django Custom Command
This project includes a custom Django command to seed the database with initial data. You can run the command by running the following command:


docker-compose run web python manage.py seed_data


This will seed the database with some initial data, making it easier to test the APIs.
