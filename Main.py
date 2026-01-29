import sys
from tracker import ExpenseTracker
from Budget import BudgetManager
from Reports import ReportManager
from Menu import show_main_menu
from INCOME_EXPENSE_CATEGORIES_MODULE import expenses_menu, income_menu, categories_menu

auth_ready = False
try:
    import authyann
    auth_ready = True
except ImportError:
    pass

def main():
    current_username = None

    if auth_ready:
        try:
            if hasattr(authyann, 'login_menu'):
                current_username = authyann.login_menu()
        except Exception as e:
            print(f"[Auth Error] {e}")

    if not current_username:
        print("\n" + "-"*30)
        print("[System] Initializing Workspace...")
        current_username = input("Please confirm user to load profile: ").strip()
        
        if not current_username:
            sys.exit()

    print(f"\n[System] Profile Loaded: {current_username}")
    
    try:
        et = ExpenseTracker(username = current_username)
        budget_mgr = BudgetManager(et)
        report_mgr = ReportManager(et)
    except Exception as e:
        print(f"[Error] Failed to initialize ExpenseTracker: {e}")
        sys.exit()

    while True:
        try:
            show_main_menu(current_username)
            choice = input("Selection: ").strip()
            if choice == '1':
                expenses_menu(et, current_username)
            elif choice == '2':
                income_menu(et, current_username)
            elif choice == '3':
                categories_menu(et, current_username)
            elif choice == '4':
                report_mgr.generate_reports()
            elif choice == '5':
                budget_mgr.manage_budgets()
            elif choice == '6':
                print("Saving session...")
                et.save()
                print("Goodbye!")
                break 
            else:
                print("Invalid selection.")
        
        except Exception as e:
            print(f"[Error] {e}")
            import traceback
            traceback.print_exc()
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()