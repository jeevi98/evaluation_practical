import sqlite3
from datetime import datetime, timedelta
from tabulate import tabulate


conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    emp_id TEXT,
    date TEXT,
    check_in TEXT,
    check_out TEXT,
    working_hours REAL,
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
)
''')

conn.commit()


def valid_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False


def add_employee():
    emp_id = input("Enter Employee ID: ").strip()
    name = input("Enter Name: ").strip()
    dept = input("Enter Department: ").strip()
    if not (emp_id and name and dept):
        print(" All fields are required.")
        return
    try:
        cursor.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_id, name, dept))
        conn.commit()
        print(" Employee added.")
    except sqlite3.IntegrityError:
        print(" Employee ID already exists.")

def check_in():
    emp_id = input("Employee ID: ").strip()
    time = input("Check-in time (HH:MM): ").strip()
    if not valid_time(time):
        print(" Invalid time format.")
        return
    today = datetime.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM attendance WHERE emp_id=? AND date=?", (emp_id, today))
    if cursor.fetchone():
        print(" Already checked in today.")
    else:
        cursor.execute("INSERT INTO attendance(emp_id, date, check_in) VALUES (?, ?, ?)", (emp_id, today, time))
        conn.commit()
        print(" Check-in recorded.")

def check_out():
    emp_id = input("Employee ID: ").strip()
    time = input("Check-out time (HH:MM): ").strip()
    if not valid_time(time):
        print(" Invalid time format.")
        return
    today = datetime.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT check_in FROM attendance WHERE emp_id=? AND date=?", (emp_id, today))
    row = cursor.fetchone()
    if not row:
        print(" No check-in found for today.")
        return
    if row[0] is None:
        print(" Check-in time missing.")
        return

    check_in_time = datetime.strptime(row[0], "%H:%M")
    check_out_time = datetime.strptime(time, "%H:%M")
    if check_out_time < check_in_time:
        print(" Check-out can't be before check-in.")
        return
    hours = round((check_out_time - check_in_time).seconds / 3600, 2)

    cursor.execute("UPDATE attendance SET check_out=?, working_hours=? WHERE emp_id=? AND date=?",
                   (time, hours, emp_id, today))
    conn.commit()
    print(f" Checked out. Total hours: {hours} hrs")

def daily_report():
    date = input("Enter date (YYYY-MM-DD): ").strip()
    cursor.execute('''
        SELECT a.emp_id, e.name, e.department, a.check_in, a.check_out, IFNULL(a.working_hours, 0)
        FROM attendance a JOIN employees e ON a.emp_id = e.emp_id
        WHERE a.date=?
    ''', (date,))
    rows = cursor.fetchall()
    if rows:
        print("\n Daily Report:")
        print(tabulate(rows, headers=["ID", "Name", "Dept", "In", "Out", "Hours"], tablefmt="grid"))
    else:
        print(" No attendance records for that date.")

def monthly_report():
    emp_id = input("Enter Employee ID: ").strip()
    month = input("Enter month (YYYY-MM): ").strip()
    cursor.execute('''
        SELECT date, check_in, check_out, IFNULL(working_hours, 0)
        FROM attendance
        WHERE emp_id=? AND date LIKE ?
    ''', (emp_id, f"{month}-%"))
    rows = cursor.fetchall()
    if rows:
        total_hours = sum(row[3] for row in rows)
        print("\n Monthly Report:")
        print(tabulate(rows, headers=["Date", "Check-in", "Check-out", "Hours"], tablefmt="grid"))
        print(f" Total Working Hours in {month}: {round(total_hours, 2)} hrs")
    else:
        print(" No records for given employee and month.")

def menu():
    print("\n EMPLOYEE ATTENDANCE TRACKER")
    print("1. Add Employee")
    print("2. Check-In")
    print("3. Check-Out")
    print("4. Daily Report")
    print("5. Monthly Report")
    print("6. Exit")

def main():
    while True:
        menu()
        choice = input("Choose (1-6): ").strip()
        if choice == "1":
            add_employee()
        elif choice == "2":
            check_in()
        elif choice == "3":
            check_out()
        elif choice == "4":
            daily_report()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            print(" Exiting. Stay punctual!")
            break
        else:
            print(" Invalid option.")

if __name__ == "__main__":
    main()
