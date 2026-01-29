import json
import os
import uuid
from expense import Expense
from income import Income
from datetime import datetime

class ExpenseTracker:
    def __init__(self, username):
        self.username = username
        self.filename = "users.json"
        self.user_data = self._load_user_data()
        
        raw_expenses = self.user_data.get('expenses', [])
        self.expenses = [Expense.from_dict(e) for e in raw_expenses]
        
        raw_income = self.user_data.get('income', [])
        self.income = [Income.from_dict(i) for i in raw_income]
        
        self.categories = self.user_data.get('categories', ["Food", "Transport", "Entertainment", "Utilities", "Other"])
        self.income_categories = self.user_data.get('income_categories', ["Salary", "Freelance", "Gift"])
        
        if 'budgets' not in self.user_data:
            self.user_data['budgets'] = {'monthly': 0, 'categories': {}}

    def _load_user_data(self):
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r') as f:
                users = json.load(f)
                for u in users:
                    if u['userName'] == self.username:
                        # Ensure budgets key exists
                        if 'budgets' not in u:
                            u['budgets'] = {'monthly': 0, 'categories': {}}
                        return u
        except (json.JSONDecodeError, KeyError):
            pass
        return {}

    def save(self):
        self.user_data['expenses'] = [e.to_dict() for e in self.expenses]
        self.user_data['income'] = [i.to_dict() for i in self.income]
        self.user_data['categories'] = self.categories
        self.user_data['income_categories'] = self.income_categories
        
        all_users = []
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    all_users = json.load(f)
            except json.JSONDecodeError:
                all_users = []
        
        user_found = False
        for i, u in enumerate(all_users):
            if u['userName'] == self.username:
                all_users[i] = self.user_data
                user_found = True
                break
        
        if not user_found:
            self.user_data['userName'] = self.username
            all_users.append(self.user_data)
            
        with open(self.filename, 'w') as f:
            json.dump(all_users, f, indent=4)

    def add_expense(self, amount, category, date, description):
        if date is None:
            date = datetime.now().isoformat()
        new_expense = Expense(id=str(uuid.uuid4()), amount=amount, category=category, date=date, description=description)
        self.expenses.append(new_expense)
        self.save()

        try:
            cat_limit = self.user_data['budgets']['categories'].get(category, 0)
            if cat_limit > 0:
                spent_cat = sum(float(e.amount) if isinstance(e.amount, (int, float, str)) else 0 for e in self.expenses if e.category == category)
                if spent_cat > cat_limit:
                    print(f"\n[!!!] ALERT: You have EXCEEDED your budget for '{category}'!")
                    print(f"      Limit: ${cat_limit:.2f} | Spent: ${spent_cat:.2f}")
                    input("Press Enter to acknowledge alert...")
        except Exception:
            pass
        return new_expense # Return object for menu compatibility

    def add_income(self, amount, category, date, description):
        if date is None:
            date = datetime.now().isoformat()
        new_income = Income(id=str(uuid.uuid4()), amount=amount, category=category, date=date, description=description)
        self.income.append(new_income)
        self.save()
        return new_income

    def delete_expense(self, expense_id):
        initial = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        if len(self.expenses) < initial:
            self.save()

    def edit_expense(self, expense_id, **kwargs):
        for e in self.expenses:
            if e.id == expense_id:
                for k, v in kwargs.items():
                    if v is not None: setattr(e, k, v)
                self.save()
                return True
        return False

    def get_categories(self):
        return self.categories

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            self.save()

    def delete_income(self, income_id):
        initial = len(self.income)
        self.income = [i for i in self.income if i.id != income_id]
        if len(self.income) < initial:
            self.save()

    def edit_income(self, income_id, **kwargs):
        for i in self.income:
            if i.id == income_id:
                for k, v in kwargs.items():
                    if v is not None: setattr(i, k, v)
                self.save()
                return True
        return False

    def get_income_categories(self):
        return self.income_categories
        
    def search(self, term=None, category=None, start=None, end=None, min_amount=None, max_amount=None):
        results = self.expenses
        if term: results = [x for x in results if term.lower() in x.description.lower()]
        if category: results = [x for x in results if x.category.lower() == category.lower()]
        return results

    def search_income(self, term=None, category=None, start=None, end=None, min_amount=None, max_amount=None):
        results = self.income
        if term: results = [x for x in results if term.lower() in x.description.lower()]
        return results

    # --- COMPATIBILITY FUNCTIONS FOR MENUS ---
    def list_expenses(self):
        return self.expenses

    def list_income(self):
        return self.income

    def monthly_summary(self):
        total_spent = sum(float(e.amount) if isinstance(e.amount, (int, float, str)) else 0 for e in self.expenses)
        monthly_limit = self.user_data['budgets'].get('monthly', 0)
        
        over = 0
        if monthly_limit > 0 and total_spent > monthly_limit:
            over = total_spent - monthly_limit

        return {
            'budget': monthly_limit,
            'total': total_spent,
            'over_budget': over,
            'year': datetime.now().year,
            'month': datetime.now().month
        }