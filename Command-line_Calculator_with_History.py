import math
import json
import os

HISTORY_FILE = "calc_history.json"
history = []


def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)

def evaluate_expression(expr):
    try:
      
        allowed = {
            'sqrt': math.sqrt,
            'log': math.log10,
            'sin': lambda x: math.sin(math.radians(x)),
            'cos': lambda x: math.cos(math.radians(x)),
            'tan': lambda x: math.tan(math.radians(x)),
            '^': '**'
        }
        for key in allowed:
            if key in expr:
                expr = expr.replace(key, f'{key}')
        expr = expr.replace('^', '**')
        result = eval(expr, {"__builtins__": None}, allowed)
        return round(result, 5)
    except ZeroDivisionError:
        print(" Error: Division by zero.")
    except ValueError:
        print(" Error: Invalid math domain.")
    except Exception:
        print(" Error: Invalid expression.")
    return None


def calculate():
    expr = input(" Enter expression (e.g. 5+3, sqrt(25), sin(30)): ").strip().lower()
    result = evaluate_expression(expr)
    if result is not None:
        print(f" Result: {result}")
        history.append({"expression": expr, "result": result})

def show_history():
    if not history:
        print(" No history yet.")
        return
    for i, item in enumerate(history, 1):
        print(f"[{i}] {item['expression']} = {item['result']}")

def delete_entry():
    show_history()
    try:
        index = int(input("Enter entry number to delete: ").strip())
        if 1 <= index <= len(history):
            deleted = history.pop(index - 1)
            print(f" Deleted: {deleted['expression']} = {deleted['result']}")
        else:
            print(" Invalid entry number.")
    except ValueError:
        print(" Invalid input.")

def save_to_file():
    save_history()
    print(" History saved to file.")

def load_from_file():
    load_history()
    print(" History loaded from file.")


def menu():
    print("\n COMMAND-LINE CALCULATOR")
    print("1. Perform Calculation")
    print("2. View History")
    print("3. Delete History Entry")
    print("4. Save History to File")
    print("5. Load History from File")
    print("6. Exit")

def main():
    load_from_file()
    while True:
        menu()
        choice = input("Choose (1–6): ").strip()
        if choice == "1":
            calculate()
        elif choice == "2":
            show_history()
        elif choice == "3":
            delete_entry()
        elif choice == "4":
            save_to_file()
        elif choice == "5":
            load_from_file()
        elif choice == "6":
            print(" Goodbye, Mathematician!")
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    main()
