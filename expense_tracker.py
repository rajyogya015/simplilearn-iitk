import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.expenses = []  # List of dictionaries: {'date', 'category', 'amount', 'description'}
        self.budgets = {}   # category: monthly_budget

    def add_expense(self):
        try:
            date = input("Enter date (YYYY-MM-DD): ")
            datetime.strptime(date, "%Y-%m-%d")  # validate date
            category = input("Enter category (e.g., Food, Transport): ")
            amount = float(input("Enter amount: "))
            description = input("Enter description (optional): ")
            self.expenses.append({
                "date": date,
                "category": category,
                "amount": amount,
                "description": description
            })
            print("✅ Expense added successfully.\n")
        except ValueError:
            print("❌ Invalid input. Please try again.\n")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.\n")
            return
        print("\n📋 All Expenses:")
        for exp in self.expenses:
            print(f"{exp['date']} - {exp['category']} - ₹{exp['amount']} - {exp['description']}")
        print()

    def set_budget(self):
        category = input("Enter category to set budget: ")
        try:
            amount = float(input("Enter monthly budget amount: "))
            self.budgets[category] = amount
            print(f"✅ Budget set for {category}: ₹{amount}\n")
        except ValueError:
            print("❌ Invalid amount.\n")

    def view_budget_status(self):
        if not self.budgets:
            print("No budgets set yet.\n")
            return
        print("\n📊 Budget Usage:")
        for category, budget in self.budgets.items():
            spent = sum(exp["amount"] for exp in self.expenses if exp["category"] == category)
            print(f"{category}: Spent ₹{spent} / Budget ₹{budget} ({(spent/budget)*100:.1f}%)")
        print()

    def save_to_file(self, filename="expenses.json"):
        data = {
            "expenses": self.expenses,
            "budgets": self.budgets
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data saved to {filename}\n")

    def load_from_file(self, filename="expenses.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.expenses = data.get("expenses", [])
                self.budgets = data.get("budgets", {})
            print(f"✅ Data loaded from {filename}\n")
        except FileNotFoundError:
            print("❌ File not found.\n")

    def run(self):
        while True:
            print("====== Personal Expense Tracker ======")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Set Monthly Budget")
            print("4. View Budget Status")
            print("5. Save to File")
            print("6. Load from File")
            print("0. Exit")
            choice = input("Select an option: ")
            print()

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.set_budget()
            elif choice == '4':
                self.view_budget_status()
            elif choice == '5':
                self.save_to_file()
            elif choice == '6':
                self.load_from_file()
            elif choice == '0':
                print("👋 Exiting the Expense Tracker. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Try again.\n")

# Run the app
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
