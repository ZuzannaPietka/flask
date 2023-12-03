from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

with open('books.json', 'r') as file:
    books_data = json.load(file)

#curl http://localhost:8080/isbns

@app.route('/isbns', methods=['GET'])
def get_isbns():
    isbns = [book['isbn'] for book in books_data['books']]
    return jsonify(isbns)

#curl http://localhost:8080/isbns/9781593275846

@app.route('/isbns/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    book = next((b for b in books_data['books'] if b['isbn'] == isbn), None)
    if book:
        return jsonify(book)
    else:
        abort(404)

#curl http://localhost:8080/authors/javascript

@app.route('/authors/<expression>', methods=['GET'])
def get_authors_by_title(expression):
    authors = [book['author'] for book in books_data['books'] if expression.lower() in book['title'].lower()]
    return jsonify(authors)

#curl -X PUT "http://localhost:8080/isbns/9781593275846?publisher=NewPublisher"

@app.route('/isbns/<isbn>', methods=['PUT'])
def update_publisher(isbn):
    new_publisher = request.args.get('publisher')
    book = next((b for b in books_data['books'] if b['isbn'] == isbn), None)

    if book:
        book['publisher'] = new_publisher
        return f"Publisher for ISBN {isbn} updated to {new_publisher}.", 200
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
