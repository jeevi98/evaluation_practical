import json
import os

DATA_FILE = "books.json"


QUOTES = [
    "“Books are a uniquely portable magic.” – Stephen King",
    "“Once you learn to read, you will be forever free.” – Frederick Douglass",
    "“There is no friend as loyal as a book.” – Ernest Hemingway",
    "“Reading gives us someplace to go when we have to stay where we are.” – Mason Cooley",
    "“You can never get a cup of tea large enough or a book long enough to suit me.” – C.S. Lewis",
    "“The only thing that you absolutely have to know is the location of the library.” – Albert Einstein",
    "“I have always imagined that Paradise will be a kind of library.” – Jorge Luis Borges",
    "“Books are mirrors: you only see in them what you already have inside you.” – Carlos Ruiz Zafón",
    "“A book is a dream that you hold in your hand.” – Neil Gaiman",
]

import random

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_books(books):
    with open(DATA_FILE, "w") as f:
        json.dump(books, f, indent=4)

def add_book():
    title = input("Enter book title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    author = input("Enter author name: ").strip()
    genre = input("Enter genre: ").strip()
    status = input("Have you read this book? (yes/no): ").strip().lower()
    if status not in ['yes', 'no']:
        print("Status must be 'yes' or 'no'.")
        return

    books = load_books()
    books.append({
        "title": title,
        "author": author,
        "genre": genre,
        "status": "read" if status == 'yes' else "unread"
    })
    save_books(books)
    print("Book added successfully!")
    print(random.choice(QUOTES))

def update_book():
    books = load_books()
    title = input("Enter the title of the book to update: ").strip()
    for book in books:
        if book["title"].lower() == title.lower():
            print("Leave a field blank to keep it unchanged.")
            new_author = input(f"Enter new author name [{book['author']}]: ").strip()
            new_genre = input(f"Enter new genre [{book['genre']}]: ").strip()
            new_status = input(f"Enter new status (read/unread) [{book['status']}]: ").strip().lower()
            if new_author:
                book["author"] = new_author
            if new_genre:
                book["genre"] = new_genre
            if new_status in ['read', 'unread']:
                book["status"] = new_status
            save_books(books)
            print("Book updated successfully!")
            return
    print("Book not found.")

def delete_book():
    books = load_books()
    title = input("Enter the title of the book to delete: ").strip()
    new_books = [book for book in books if book["title"].lower() != title.lower()]
    if len(new_books) == len(books):
        print("Book not found.")
    else:
        save_books(new_books)
        print("Book deleted successfully.")

def list_books_by_genre():
    genre = input("Enter genre to list: ").strip().lower()
    books = load_books()
    filtered = [book for book in books if book["genre"].lower() == genre]
    if filtered:
        for book in filtered:
            print(f"{book['title']} by {book['author']} - {book['status'].capitalize()}")
    else:
        print("No books found in that genre.")

def list_books_by_status():
    status = input("Enter status (read/unread): ").strip().lower()
    if status not in ['read', 'unread']:
        print("Invalid status entered.")
        return
    books = load_books()
    filtered = [book for book in books if book["status"] == status]
    if filtered:
        for book in filtered:
            print(f"{book['title']} by {book['author']} - Genre: {book['genre']}")
    else:
        print("No books with that status found.")

def mark_book_as_read():
    title = input("Enter the title of the book to mark as read: ").strip()
    books = load_books()
    for book in books:
        if book["title"].lower() == title.lower():
            book["status"] = "read"
            save_books(books)
            print("Book marked as read.")
            return
    print("Book not found.")

def search_books():
    keyword = input("Enter book title or author name to search: ").strip().lower()
    books = load_books()
    filtered = [book for book in books if keyword in book["title"].lower() or keyword in book["author"].lower()]
    if filtered:
        for book in filtered:
            print(f"{book['title']} by {book['author']} - {book['status'].capitalize()} - Genre: {book['genre']}")
    else:
        print("No matching books found.")

def show_menu():
    print("\n BOOK LIBRARY CLI ")
    print("1. Add a new book")
    print("2. Update a book")
    print("3. Delete a book")
    print("4. List books by genre")
    print("5. List books by read/unread status")
    print("6. Mark a book as read")
    print("7. Search by title or author")
    print("8. Exit")

def main():
    print("Welcome to your personal Book Library!")
    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            list_books_by_genre()
        elif choice == "5":
            list_books_by_status()
        elif choice == "6":
            mark_book_as_read()
        elif choice == "7":
            search_books()
        elif choice == "8":
            print("Goodbye! Keep reading 📖.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
