# ContentTracker
A todo list and media library website written in Python using the Django framework and MySQL. Users can create lists of normal todo items, items with urls, and items with custom css for books, movies, and tv shows.

The primary use of Content Tracker is as an easy way to keep track of books, movies, tv shows, online articles, and other media that users plan to view and have already viewed. For books, movies, and tv shows, Content Tracker provides search functions that will automatically populate list items from search results while also providing the ability to add custom items that can't be found through search.

## Dependencies & Frameworks
* [Python 3.3 or higher](https://www.python.org/download/releases/3.3.0/)
* [Django 1.10](https://www.djangoproject.com/)

## Running
A Django secret key and database connection info must be provided in text files named secret_key.txt and db.txt respectively. You have to add these files to the tracker/tracker directory in order for the server to run. These files are in the .gitignore and should never be committed.

Content Tracker uses a MySQL database. It will need one to connect to and an appropriate database driver that works with Django. [See Django's documentation for more information.](https://docs.djangoproject.com/en/1.10/ref/databases/#mysql-notes)

Appropriate migrations will need to be done:

    python3 manage.py makemigrations
    python3 manage.py migrate

Run the server using the following command:

    python3 manage.py runserver

