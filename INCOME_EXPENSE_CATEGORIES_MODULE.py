

from datetime import datetime


def parse_date(s: str):
    """Parse a date string in ISO 8601 or YYYY-MM-DD format.

    Returns a datetime on success or None if empty/invalid.
    """
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None


def expenses_menu(et, user):
    # View expenses table with ID and actions underneath
    def print_table(items):
        if not items:
            print("No expenses to show.")
            return
        print(f"{'ID':36}  {'Date':10}  {'Category':12}  {'Amount':8}  Description")
        print('-'*90)
        for e in items:
            date_str = e.date[:10] if (e.date and isinstance(e.date, str)) else "N/A"
            category_str = e.category if e.category else "N/A"
            try:
                amount = float(e.amount) if e.amount is not None else 0.0
            except (ValueError, TypeError):
                amount = 0.0
            desc = e.description if e.description else ""
            print(f"{e.id:36}  {date_str:10}  {category_str:12}  {amount:8.2f}  {desc}")

    while True:
        items = et.list_expenses()
        print_table(items)
        # show current month budget summary under table
        ms = et.monthly_summary()
        if ms.get('budget') is not None:
            print(f"\nCurrent month budget: {ms['budget']:.2f}  Total: {ms['total']:.2f}  Over budget: {ms['over_budget']}")
        else:
            print(f"\nNo budget set for {ms['year']}-{ms['month']}")

        print("\nActions: [A]dd expense  [E]dit expense by id  [D]elete expense by id  [S]earch  [B]ack")
        act = input("Choose action: ").strip().lower()
        if act == 'a':
            amt = input("Amount: ")
            try:
                amt_float = float(amt)
                if amt_float <= 0:
                    print("Amount must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            cat = input("Category: ")
            date_in = input("Date (YYYY-MM-DD) [leave empty for today]: ")
            desc = input("Description (optional): ")
            date_iso = None
            if date_in.strip():
                d = parse_date(date_in)
                if d is None:
                    print("Invalid date format. Use YYYY-MM-DD")
                    continue
                date_iso = d.isoformat()
            try:
                e = et.add_expense(amt_float, cat, date_iso, desc)
                print("Added:", e.id)
            except Exception as exc:
                print("Error adding expense:", exc)
        elif act == 'd':
            eid = input("Expense id to delete: ").strip()
            found = [x for x in et.expenses if x.id == eid]
            if not found:
                print("Expense id not found.")
                continue
            e = found[0]
            print(f"\nDelete: {e.date[:10]} | {e.category} | ${e.amount:.2f} | {e.description}")
            confirm = input("Confirm delete? (yes/no): ").strip().lower()
            if confirm == 'yes':
                et.delete_expense(eid)
                print("Expense deleted.")
            else:
                print("Cancelled.")
        elif act == 'e':
            eid = input("Expense id to edit: ").strip()
            found = [x for x in et.expenses if x.id == eid]
            if not found:
                print("Not found")
                continue
            e = found[0]
            print("Leave blank to keep current value.")
            amt = input(f"Amount [{e.amount}]: ")
            amt_float = None
            if amt.strip():
                try:
                    amt_float = float(amt)
                    if amt_float <= 0:
                        print("Amount must be greater than zero.")
                        continue
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
            cat = input(f"Category [{e.category}]: ")
            date_in = input(f"Date YYYY-MM-DD [{e.date[:10]}]: ")
            desc = input(f"Description [{e.description}]: ")
            date_iso = None
            if date_in.strip():
                d = parse_date(date_in)
                if d is None:
                    print("Invalid date format. Use YYYY-MM-DD")
                    continue
                date_iso = d.isoformat()
            ok = et.edit_expense(eid, amount=amt_float, category=cat if cat.strip() else None, date=date_iso if date_iso else None, description=desc if desc.strip() else None)
            print("Updated" if ok else "Failed")
        elif act == 's':
            term = input("Search term (description or category) [optional]: ")
            cat = input("Category [optional]: ")
            start = parse_date(input("Start date YYYY-MM-DD [optional]: "))
            end = parse_date(input("End date YYYY-MM-DD [optional]: "))
            min_a = input("Min amount [optional]: ")
            max_a = input("Max amount [optional]: ")
            min_a_v = float(min_a) if min_a.strip() else None
            max_a_v = float(max_a) if max_a.strip() else None
            results = et.search(term=term if term.strip() else None, category=cat if cat.strip() else None, start=start, end=end, min_amount=min_a_v, max_amount=max_a_v)
            if not results:
                print("No matching expenses.")
            else:
                print("Search results:")
                for r in results:
                    print(f"{r.id:36}  {r.date[:10]:10}  {r.category:12}  {r.amount:8.2f}  {r.description}")
                print("Use the expense id shown above with Edit/Delete actions.")
        elif act == 'b' or act == '':
            break
        else:
            print("Unknown action.")



def income_menu(et, user):
    # View income table with ID and actions underneath
    def print_income_table(items):
        if not items:
            print("No income to show.")
            return
        print(f"{'ID':36}  {'Date':10}  {'Category':12}  {'Amount':8}  Description")
        print('-'*90)
        for i in items:
            date_str = i.date[:10] if (i.date and isinstance(i.date, str)) else "N/A"
            category_str = i.category if i.category else "N/A"
            try:
                amount = float(i.amount) if i.amount is not None else 0.0
            except (ValueError, TypeError):
                amount = 0.0
            desc = i.description if i.description else ""
            print(f"{i.id:36}  {date_str:10}  {category_str:12}  {amount:8.2f}  {desc}")

    while True:
        items = et.list_income()
        print_income_table(items)

        print("\nActions: [A]dd income  [E]dit income by id  [D]elete income by id  [S]earch  [B]ack")
        act = input("Choose action: ").strip().lower()
        if act == 'a':
            amt = input("Amount: ")
            try:
                amt_float = float(amt)
                if amt_float <= 0:
                    print("Amount must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            cat = input("Category: ")
            date_in = input("Date (YYYY-MM-DD) [leave empty for today]: ")
            desc = input("Description (optional): ")
            date_iso = None
            if date_in.strip():
                d = parse_date(date_in)
                if d is None:
                    print("Invalid date format. Use YYYY-MM-DD")
                    continue
                date_iso = d.isoformat()
            try:
                i = et.add_income(amt_float, cat, date_iso, desc)
                print("Added:", i.id)
            except Exception as exc:
                print("Error adding income:", exc)
        elif act == 'd':
            iid = input("Income id to delete: ").strip()
            found = [x for x in et.income if x.id == iid]
            if not found:
                print("Income id not found.")
                continue
            i = found[0]
            print(f"\nDelete: {i.date[:10]} | {i.category} | ${i.amount:.2f} | {i.description}")
            confirm = input("Confirm delete? (yes/no): ").strip().lower()
            if confirm == 'yes':
                et.delete_income(iid)
                print("Income deleted.")
            else:
                print("Cancelled.")
        elif act == 'e':
            iid = input("Income id to edit: ").strip()
            found = [x for x in et.income if x.id == iid]
            if not found:
                print("Not found")
                continue
            i = found[0]
            print("Leave blank to keep current value.")
            amt = input(f"Amount [{i.amount}]: ")
            amt_float = None
            if amt.strip():
                try:
                    amt_float = float(amt)
                    if amt_float <= 0:
                        print("Amount must be greater than zero.")
                        continue
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
            cat = input(f"Category [{i.category}]: ")
            date_in = input(f"Date YYYY-MM-DD [{i.date[:10]}]: ")
            desc = input(f"Description [{i.description}]: ")
            date_iso = None
            if date_in.strip():
                d = parse_date(date_in)
                if d is None:
                    print("Invalid date format. Use YYYY-MM-DD")
                    continue
                date_iso = d.isoformat()
            ok = et.edit_income(iid, amount=amt_float, category=cat if cat.strip() else None, date=date_iso if date_iso else None, description=desc if desc.strip() else None)
            print("Updated" if ok else "Failed")
        elif act == 's':
            term = input("Search term (description or category) [optional]: ")
            cat = input("Category [optional]: ")
            start = parse_date(input("Start date YYYY-MM-DD [optional]: "))
            end = parse_date(input("End date YYYY-MM-DD [optional]: "))
            min_a = input("Min amount [optional]: ")
            max_a = input("Max amount [optional]: ")
            min_a_v = float(min_a) if min_a.strip() else None
            max_a_v = float(max_a) if max_a.strip() else None
            results = et.search_income(term=term if term.strip() else None, category=cat if cat.strip() else None, start=start, end=end, min_amount=min_a_v, max_amount=max_a_v)
            if not results:
                print("No matching income.")
            else:
                print("Search results:")
                for r in results:
                    print(f"{r.id:36}  {r.date[:10]:10}  {r.category:12}  {r.amount:8.2f}  {r.description}")
                print("Use the income id shown above with Edit/Delete actions.")
        elif act == 'b' or act == '':
            break
        else:
            print("Unknown action.")

def categories_menu(et, user):
    # View categories - choose between expense or income categories
    while True:
        print("Categories:\n1) Expense categories\n2) Income categories\n3) Back")
        cat_choice = input("Choose: ").strip()
        
        if cat_choice == "1":
            # Expense categories management
            while True:
                cats = et.get_categories()
                if not cats:
                    print("No expense categories available.")
                else:
                    print("Expense Categories:")
                    for i, c in enumerate(cats, 1):
                        print(f"{i}. {c}")
                
                print("\nActions: [A]dd category  [R]emove category by name  [B]ack")
                a = input("Choose action: ").strip().lower()
                
                if a == 'a':
                    name = input("Category name: ").strip()
                    if not name:
                        print("Empty name.")
                        continue
                    if any(name.lower() == c.lower() for c in et.categories):
                        print("Category exists (case-insensitive).")
                        continue
                    et.categories.append(name)
                    et.save()
                    print("Expense category added.")
                elif a == 'r':
                    name = input("Category name to remove: ").strip()
                    matching = [c for c in et.categories if c.lower() == name.lower()]
                    if matching:
                        et.categories.remove(matching[0])
                        et.save()
                        print("Expense category removed.")
                    else:
                        print("Category not found.")
                elif a == 'b' or a == '':
                    break
                else:
                    print("Unknown action.")
                    
        elif cat_choice == "2":
            # Income categories management
            while True:
                income_cats = et.get_income_categories()
                if not income_cats:
                    print("No income categories available.")
                else:
                    print("Income Categories:")
                    for i, c in enumerate(income_cats, 1):
                        print(f"{i}. {c}")
                
                print("\nActions: [A]dd category  [R]emove category by name  [B]ack")
                a = input("Choose action: ").strip().lower()
                
                if a == 'a':
                    name = input("Category name: ").strip()
                    if not name:
                        print("Empty name.")
                        continue
                    if any(name.lower() == c.lower() for c in et.income_categories):
                        print("Category exists (case-insensitive).")
                        continue
                    et.income_categories.append(name)
                    et.save()
                    print("Income category added.")
                elif a == 'r':
                    name = input("Category name to remove: ").strip()
                    matching = [c for c in et.income_categories if c.lower() == name.lower()]
                    if matching:
                        et.income_categories.remove(matching[0])
                        et.save()
                        print("Income category removed.")
                    else:
                        print("Category not found.")
                elif a == 'b' or a == '':
                    break
                else:
                    print("Unknown action.")
            
        elif cat_choice == "3" or cat_choice == '':
            break
        else:
            print("Unknown option.")
