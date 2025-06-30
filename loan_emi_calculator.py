import json, os
from datetime import datetime
from fpdf import FPDF

HISTORY_FILE = "emi_history.json"


def validate_input(prompt, type_=float, min_val=0):
    try:
        value = type_(input(prompt).strip())
        if value <= min_val:
            raise ValueError
        return value
    except:
        print(f" Invalid input. Must be > {min_val}")
        return None

def calculate_emi(P, R, N):
    monthly_rate = R / (12 * 100)
    emi = P * monthly_rate * (1 + monthly_rate)**N / ((1 + monthly_rate)**N - 1)
    total_payment = round(emi * N, 2)
    total_interest = round(total_payment - P, 2)
    return round(emi, 2), total_interest, total_payment

def save_to_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def retrieve_by_date():
    date = input("Enter date (YYYY-MM-DD): ").strip()
    if not os.path.exists(HISTORY_FILE):
        print(" No history found.")
        return
    with open(HISTORY_FILE) as f:
        history = json.load(f)
    matches = [h for h in history if h["date"] == date]
    if matches:
        for i, h in enumerate(matches, 1):
            print(f"\n[{i}] Principal: ₹{h['principal']}, Interest: {h['rate']}%, Tenure: {h['tenure']} months")
            print(f"    EMI: ₹{h['emi']}, Total Interest: ₹{h['interest']}, Total Payment: ₹{h['total']}")
    else:
        print(" No records found for this date.")

def export_to_txt(entry):
    filename = f"emi_{entry['date'].replace('-', '')}.txt"
    with open(filename, "w") as f:
        f.write(" Loan EMI Calculation\n")
        for key, value in entry.items():
            f.write(f"{key.capitalize()}: {value}\n")
    print(f" Exported to {filename}")

def export_to_pdf(entry):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Loan EMI Calculation", ln=True, align='C')
    for key, val in entry.items():
        pdf.cell(200, 10, f"{key.capitalize()}: {val}", ln=True)
    filename = f"emi_{entry['date'].replace('-', '')}.pdf"
    pdf.output(filename)
    print(f" Exported to {filename}")


def new_calculation():
    P = validate_input("Enter principal amount (₹): ")
    R = validate_input("Enter annual interest rate (%): ")
    N = validate_input("Enter loan tenure (months): ", int)
    if None in (P, R, N):
        return

    emi, interest, total = calculate_emi(P, R, N)
    today = datetime.today().strftime("%Y-%m-%d")
    result = {
        "date": today,
        "principal": P,
        "rate": R,
        "tenure": N,
        "emi": emi,
        "interest": interest,
        "total": total
    }

    print("\n EMI Calculation:")
    print(f"Monthly EMI     : ₹{emi}")
    print(f"Total Interest  : ₹{interest}")
    print(f"Total Payment   : ₹{total}")

    save_to_history(result)

    exp = input("Export? (txt/pdf/none): ").strip().lower()
    if exp == "txt":
        export_to_txt(result)
    elif exp == "pdf":
        export_to_pdf(result)

# ---------- CLI ----------
def menu():
    print("\n📊 LOAN EMI CALCULATOR")
    print("1. New Calculation")
    print("2. View History by Date")
    print("3. Exit")

def main():
    while True:
        menu()
        choice = input("Choose (1-3): ").strip()
        if choice == "1":
            new_calculation()
        elif choice == "2":
            retrieve_by_date()
        elif choice == "3":
            print(" Goodbye! Manage loans wisely.")
            break
        else:
            print(" Invalid option.")

if __name__ == "__main__":
    main()
