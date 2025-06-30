import json
import os
from datetime import datetime

NOTES_FILE = "notes.json"

def load_notes():
    return json.load(open(NOTES_FILE)) if os.path.exists(NOTES_FILE) else []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

def add_note():
    title = input("Enter title: ").strip()
    if not title:
        print(" Title can't be empty.")
        return
    content = input("Enter note content: ").strip()
    if not content:
        print(" Note content can't be empty.")
        return
    note = {
        "title": title,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes = load_notes()
    notes.append(note)
    save_notes(notes)
    print(" Note added successfully.")

def list_notes(order="date"):
    notes = load_notes()
    if not notes:
        print(" No notes found.")
        return
    if order == "alpha":
        notes.sort(key=lambda x: x["title"].lower())
    else:
        notes.sort(key=lambda x: x["timestamp"], reverse=True)
    for idx, note in enumerate(notes, 1):
        print(f"\n[{idx}] {note['title']} ({note['timestamp']})\n{note['content']}")

def search_notes():
    keyword = input("Enter keyword to search: ").strip().lower()
    notes = load_notes()
    found = [note for note in notes if keyword in note["title"].lower() or keyword in note["content"].lower()]
    if found:
        for idx, note in enumerate(found, 1):
            print(f"\n[{idx}] {note['title']} ({note['timestamp']})\n{note['content']}")
    else:
        print(" No notes matched your keyword.")

def edit_note():
    notes = load_notes()
    list_notes()
    try:
        idx = int(input("\nEnter note number to edit: ")) - 1
        if idx not in range(len(notes)):
            raise IndexError
        title = input(f"New title [{notes[idx]['title']}]: ").strip()
        content = input("New content (leave blank to keep existing): ").strip()
        if title:
            notes[idx]["title"] = title
        if content:
            notes[idx]["content"] = content
        notes[idx]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_notes(notes)
        print(" Note updated.")
    except (ValueError, IndexError):
        print(" Invalid note number.")

def delete_note():
    notes = load_notes()
    list_notes()
    try:
        idx = int(input("\nEnter note number to delete: ")) - 1
        if idx not in range(len(notes)):
            raise IndexError
        confirm = input(f"Are you sure you want to delete '{notes[idx]['title']}'? (y/n): ").strip().lower()
        if confirm == "y":
            notes.pop(idx)
            save_notes(notes)
            print(" Note deleted.")
        else:
            print(" Deletion cancelled.")
    except (ValueError, IndexError):
        print(" Invalid note number.")

def menu():
    print("\n NOTES TAKING APP")
    print("1. Add Note")
    print("2. List Notes by Date")
    print("3. List Notes Alphabetically")
    print("4. Search Notes")
    print("5. Edit Note")
    print("6. Delete Note")
    print("7. Exit")

def main():
    while True:
        menu()
        choice = input("Choose an option (1–7): ").strip()
        if choice == "1":
            add_note()
        elif choice == "2":
            list_notes("date")
        elif choice == "3":
            list_notes("alpha")
        elif choice == "4":
            search_notes()
        elif choice == "5":
            edit_note()
        elif choice == "6":
            delete_note()
        elif choice == "7":
            print(" Goodbye! Keep writing your thoughts.")
            break
        else:
            print(" Invalid choice. Please enter 1–7.")

if __name__ == "__main__":
    main()
