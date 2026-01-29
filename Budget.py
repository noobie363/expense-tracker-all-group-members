class BudgetManager:
    def __init__(self, tracker):
        self.tracker = tracker

    def show_budget_menu(self):
        print("\n--- BUDGETING MENU ---")
        print("1. Set Monthly Budget Limit")
        print("2. Set Specific Category Budget")
        print("3. Check Budget Status (Alerts)")
        print("4. Back to main menu")

    def manage_budgets(self):
        while True:
            self.show_budget_menu()
            choice = input("Selection: ")

            budgets = self.tracker.user_data['budgets']

            if choice == '1':
                try:
                    current = budgets.get('monthly', 0)
                    print(f"Current Monthly Limit: ${current:.2f}")
                    amount = float(input("Enter new overall monthly limit: "))
                    budgets['monthly'] = amount
                    self.tracker.save()
                    print(f"[Success] Monthly budget set to ${amount:.2f}")
                except ValueError:
                    print("[!] Invalid amount. Please enter a number.")
            
            elif choice == '2':
                print("Available Categories:", ", ".join(self.tracker.categories))
                category = input("Enter Category: ").strip()
                
                try:
                    current_cat = budgets['categories'].get(category, 0)
                    print(f"Current limit for '{category}': ${current_cat:.2f}")
                    amount = float(input(f"Enter new limit for '{category}': "))
                    budgets['categories'][category] = amount
                    self.tracker.save()
                    print(f"[Success] Budget for '{category}' set to ${amount:.2f}")
                except ValueError:
                    print("[!] Invalid amount.")

            elif choice == '3':
                self.check_budget_status()

            elif choice == '4':
                break
            else:
                print("Invalid selection.")

    def check_budget_status(self):
        print("\n--- BUDGET STATUS REPORT ---")
        
        total_spent = 0
        category_spent = {}
        
        for expense in self.tracker.expenses:
            try:
                amount = float(expense.amount) if isinstance(expense.amount, (int, float, str)) else 0
            except (ValueError, TypeError):
                amount = 0
            cat = expense.category if expense.category else "Other"
            
            total_spent += amount
            category_spent[cat] = category_spent.get(cat, 0) + amount

        monthly_limit = self.tracker.user_data['budgets'].get('monthly', 0)
        print(f"Total Spent: ${total_spent:.2f} / Monthly Limit: ${monthly_limit:.2f}")
        
        if monthly_limit > 0 and total_spent > monthly_limit:
            diff = total_spent - monthly_limit
            print(f"  [!!!] WARNING: You are OVER your monthly budget by ${diff:.2f}!")
        else:
            left = monthly_limit - total_spent
            print(f" You are within your monthly budget. Remaining: ${left:.2f}")

        print("\n--- Category Breakdown ---")
        has_alerts = False
        
        cat_budgets = self.tracker.user_data['budgets'].get('categories', {})
        
        if not cat_budgets:
            print("(No specific category budgets set yet)")

        for cat, limit in cat_budgets.items():
            spent = category_spent.get(cat, 0)
            status = "OK"
            if spent > limit:
                status = f"OVER by ${spent - limit:.2f}"
                has_alerts = True
            elif spent > limit * 0.9:
                status = "Near Limit"
                
            print(f"{cat}: Spent ${spent:.2f} / Limit ${limit:.2f} -> {status}")
        
        if not has_alerts and cat_budgets:
            print("\n[OK] All category budgets are healthy.")
            
        input("Press Enter to continue...")