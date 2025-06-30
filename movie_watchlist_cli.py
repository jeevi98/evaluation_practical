import json
import os

WATCHLIST_FILE = "watchlist.json"

def load_watchlist():
    return json.load(open(WATCHLIST_FILE)) if os.path.exists(WATCHLIST_FILE) else []

def save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_movie():
    title = input("Title: ").strip()
    genre = input("Genre: ").strip()
    year = input("Release Year: ").strip()
    status = input("Status (watched/pending): ").strip().lower()
    if not title or not genre or not year or status not in ['watched', 'pending']:
        print(" Invalid input. All fields are required.")
        return
    try:
        int(year)
    except:
        print(" Year must be a number.")
        return
    data = load_watchlist()
    data.append({
        "title": title,
        "genre": genre,
        "year": year,
        "status": status,
        "rating": None,
        "review": None
    })
    save_watchlist(data)
    print(" Movie added.")

def list_movies(data=None):
    data = data or load_watchlist()
    if not data:
        print(" Watchlist is empty.")
        return
    for i, movie in enumerate(data, 1):
        print(f"\n[{i}] {movie['title']} ({movie['year']}) - {movie['genre']} - {movie['status'].capitalize()}")
        if movie['status'] == 'watched':
            print(f"    {movie['rating']} | Review: {movie['review']}")

def edit_movie():
    data = load_watchlist()
    list_movies(data)
    try:
        idx = int(input("\nEnter movie number to edit: ")) - 1
        if idx not in range(len(data)):
            raise IndexError
        m = data[idx]
        title = input(f"New title [{m['title']}]: ").strip()
        genre = input(f"New genre [{m['genre']}]: ").strip()
        year = input(f"New year [{m['year']}]: ").strip()
        status = input(f"New status (watched/pending) [{m['status']}]: ").strip().lower()

        if title: data[idx]['title'] = title
        if genre: data[idx]['genre'] = genre
        if year.isdigit(): data[idx]['year'] = year
        if status in ['watched', 'pending']: data[idx]['status'] = status

        save_watchlist(data)
        print(" Movie updated.")
    except (ValueError, IndexError):
        print(" Invalid selection.")

def delete_movie():
    data = load_watchlist()
    list_movies(data)
    try:
        idx = int(input("\nEnter movie number to delete: ")) - 1
        if idx not in range(len(data)):
            raise IndexError
        confirm = input(f"Delete '{data[idx]['title']}'? (y/n): ").strip().lower()
        if confirm == 'y':
            data.pop(idx)
            save_watchlist(data)
            print(" Movie deleted.")
    except (ValueError, IndexError):
        print(" Invalid selection.")

def search_or_filter():
    data = load_watchlist()
    choice = input("Search by (title/genre/status): ").strip().lower()
    keyword = input("Enter keyword: ").strip().lower()
    result = []
    for m in data:
        if choice == "title" and keyword in m["title"].lower():
            result.append(m)
        elif choice == "genre" and keyword in m["genre"].lower():
            result.append(m)
        elif choice == "status" and m["status"].lower() == keyword:
            result.append(m)
    list_movies(result)

def rate_review():
    data = load_watchlist()
    watched = [m for m in data if m["status"] == "watched"]
    if not watched:
        print(" No watched movies to rate.")
        return
    list_movies(watched)
    try:
        idx = int(input("\nEnter movie number to review: ")) - 1
        if idx not in range(len(watched)):
            raise IndexError
        movie = watched[idx]
        rating = float(input("Rating (0–5): ").strip())
        if not (0 <= rating <= 5):
            print(" Rating must be between 0 and 5.")
            return
        review = input("Write your review: ").strip()
        for m in data:
            if m["title"] == movie["title"]:
                m["rating"] = rating
                m["review"] = review
                break
        save_watchlist(data)
        print(" Review saved.")
    except (ValueError, IndexError):
        print(" Invalid input.")

def export_watchlist():
    data = load_watchlist()
    if not data:
        print(" Nothing to export.")
        return
    fmt = input("Export format (json/txt): ").strip().lower()
    if fmt == "json":
        with open("watchlist_export.json", "w") as f:
            json.dump(data, f, indent=4)
        print(" Exported to watchlist_export.json")
    elif fmt == "txt":
        with open("watchlist_export.txt", "w") as f:
            for m in data:
                f.write(f"{m['title']} ({m['year']}) - {m['genre']} - {m['status']}\n")
                if m["status"] == "watched":
                    f.write(f" {m['rating']} | Review: {m['review']}\n")
                f.write("\n")
        print(" Exported to watchlist_export.txt")
    else:
        print(" Invalid format.")

def menu():
    print("\n MOVIE WATCHLIST CLI")
    print("1. Add Movie")
    print("2. Edit Movie")
    print("3. Delete Movie")
    print("4. Search/Filter")
    print("5. Rate/Review")
    print("6. View All")
    print("7. Export")
    print("8. Exit")

def main():
    while True:
        menu()
        choice = input("Choose (1–8): ").strip()
        if choice == "1":
            add_movie()
        elif choice == "2":
            edit_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            search_or_filter()
        elif choice == "5":
            rate_review()
        elif choice == "6":
            list_movies()
        elif choice == "7":
            export_watchlist()
        elif choice == "8":
            print(" Happy watching!")
            break
        else:
            print(" Invalid option.")

if __name__ == "__main__":
    main()
