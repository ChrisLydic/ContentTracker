# ContentTracker
A todo list style website written in Python using the Django framework and MySQL. Features include normal todo items, items with website links, and items with custom css for books, movies, and tv shows. The primary use of Content Tracker is as an easy way to keep track of books, movies, tv shows, online articles, and other media that you plan to view and have viewed. For books, movies, and tv shows, Content Tracker provides search functions that will automatically populate list items from search results while also providing the ability to add custom items that can't be found in search.

## Dependencies & Frameworks
* [Python 3.3 or higher](https://www.python.org/download/releases/3.3.0/)
* [Django](https://www.djangoproject.com/)

## Cloning & Running
A Django secret key and database connection info must be provided in text files named key.txt and db.txt respectively. You have to add these files to the tracker/tracker directory in order for the server to run. These files are ignored by git and should never be committed.

Run the server using the following command:

    python3 manage.py runserver

