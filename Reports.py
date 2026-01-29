class ReportManager:
    def __init__(self, tracker):
        self.tracker = tracker

    def show_report_menu(self):
        print("\n--- REPORT MENU ---")
        print("1. Global Balance (Income vs Expenses)")
        print("2. Expenses by Category (Sorted)")
        print("3. View All Transactions (Merged)")
        print("4. Filter Expenses by Date")
        print("5. Visual Expense Chart (Pie)")
        print("6. Back to main menu")

    def generate_reports(self):
        while True:
            self.show_report_menu()
            choice = input("Selection: ")
          
            expenses = self.tracker.expenses
            incomes = self.tracker.income
            
            if choice == '1':
                total_inc = sum(float(i.amount) if isinstance(i.amount, (int, float, str)) else 0 for i in incomes)
                total_exp = sum(float(e.amount) if isinstance(e.amount, (int, float, str)) else 0 for e in expenses)
                balance = total_inc - total_exp
                
                print("\n=== GLOBAL FINANCIAL REPORT ===")
                print(f"Total Income:   +${total_inc:.2f}")
                print(f"Total Expenses: -${total_exp:.2f}")
                print("-" * 35)
                
                if balance >= 0:
                    print(f"CURRENT BALANCE: ${balance:.2f} (Positive)")
                else:
                    print(f"CURRENT BALANCE: ${balance:.2f} (Negative/Debt)")
                
                print("-" * 35)
                input("Press Enter to continue...")

            elif choice == '2':
                if not expenses:
                    print("No expenses recorded.")
                else:
                    sorted_exp = sorted(expenses, key=lambda x: x.category)
                    self.print_transaction_table(sorted_exp, "Expenses by Category")
                input("Press Enter...")

            elif choice == '3':
                all_transactions = []
                for e in expenses:
                    all_transactions.append({
                        "date": e.date,
                        "type": "EXPENSE",
                        "category": e.category,
                        "amount": -e.amount,
                        "desc": e.description
                    })
                for i in incomes:
                    all_transactions.append({
                        "date": i.date,
                        "type": "INCOME",
                        "category": i.category,
                        "amount": i.amount,
                        "desc": i.description
                    })
                
                all_transactions.sort(key=lambda x: x['date'], reverse=True)
                
                print("\n--- CHRONOLOGICAL TIMELINE ---")
                print(f"{'Date':<12} | {'Type':<8} | {'Category':<12} | {'Amount':<9} | {'Description'}")
                print("-" * 65)
                for t in all_transactions:
                    print(f"{t['date'][:10]:<12} | {t['type']:<8} | {t['category']:<12} | ${t['amount']:<9.2f} | {t['desc']}")
                input("Press Enter...")

            elif choice == '4':
                target = input("Enter date filter (YYYY or YYYY-MM): ").strip()
                filtered = [e for e in expenses if e.date.startswith(target)]
                
                if filtered:
                    self.print_transaction_table(filtered, f"Expenses for '{target}'")
                else:
                    print("No records found.")
                input("Press Enter...")

            elif choice == '5':
                self.visualize_expenses(expenses)

            elif choice == '6':
                break 
            else:
                print("Invalid selection.")

    def print_transaction_table(self, expense_list, title):
        print(f"\n--- {title} ---")
        for e in expense_list:
            print(f"{e.date[:10]:<12} | {e.category:<12} | ${e.amount:<9.2f} | {e.description}")

    def visualize_expenses(self, expenses):
        print("\n>> Generating Visualization...")
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("[ERROR] 'matplotlib' library is not installed.")
            input("Press Enter...")
            return

        cat_totals = {}
        for e in expenses:
            cat = e.category
            cat_totals[cat] = cat_totals.get(cat, 0) + e.amount
        
        if not cat_totals:
            print("No data to visualize yet.")
            return

        try:
            labels = list(cat_totals.keys())
            sizes = list(cat_totals.values())
            
            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Expense Distribution")
            plt.axis('equal') 
            plt.show()
        except Exception as e:
            print(f"Error generating chart: {e}")