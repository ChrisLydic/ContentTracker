# # API calls
# import requests

# def getBook( olid ):
#     url = 'https://openlibrary.org/api/books'
#     params = { 'bibkeys': 'OLID:' + olid, 'jscmd': data, 'format': json }
#     r = requests.get( url, params=params )
#     book = r.json()

# def searchBooks( query ):
#     url = 'https://openlibrary.org/search.json'
#     params = { 'q': query }
#     r = requests.get( url, params=params )
#     books = r.json()
#     books_list = {'books':books['results']}