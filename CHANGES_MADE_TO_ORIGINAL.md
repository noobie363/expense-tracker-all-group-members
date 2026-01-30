# CHANGES MADE TO ORIGINAL FILES

This document outlines every modification made to the original files to successfully merge the work from all 3 team members and fix integration issues.

---

## 1. authyann.py
**File Purpose:** User authentication (login/registration)

### Changes Made:

#### Change 1.1: Added consistent filename reference
**Lines affected:** `load_users()` and `save_users()` functions

**Original Code:**
```python
def load_users():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump([], f)
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
```

**Modified Code:**
```python
def load_users():
    filename = "users.json"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
    with open(filename, "r") as f:
        return json.load(f)

def save_users(users):
    filename = "users.json"
    with open(filename, "w") as f:
        json.dump(users, f, indent=2)
```

**Reason:** Ensures consistent file path references and makes it easier to modify the storage location in the future if needed.

---

## 2. tracker.py
**File Purpose:** Core expense tracking logic

### Changes Made:

#### Change 2.1: Added uuid import
**Line affected:** Top of file (imports section)

**Original Code:**
```python
import json
import os
from expense import Expense
from income import Income
from datetime import datetime
```

**Modified Code:**
```python
import json
import os
import uuid
from expense import Expense
from income import Income
from datetime import datetime
```

**Reason:** Required for generating unique IDs when creating new expenses and income records.

---

#### Change 2.2: Enhanced `_load_user_data()` to initialize budgets
**Line affected:** `_load_user_data()` method

**Original Code:**
```python
def _load_user_data(self):
    if not os.path.exists(self.filename):
        return {}
    try:
        with open(self.filename, 'r') as f:
            users = json.load(f)
            for u in users:
                if u['userName'] == self.username:
                    return u
    except (json.JSONDecodeError, KeyError):
        pass
    return {}
```

**Modified Code:**
```python
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
```

**Reason:** Prevents KeyError when accessing budget data for users with no prior budget configuration.

---

#### Change 2.3: Fixed `add_expense()` to handle None dates and generate UUIDs
**Line affected:** `add_expense()` method

**Original Code:**
```python
def add_expense(self, amount, category, date, description):
    new_expense = Expense(amount, category, date, description)
    self.expenses.append(new_expense)
    self.save()
    # ... rest of method
```

**Modified Code:**
```python
def add_expense(self, amount, category, date, description):
    if date is None:
        date = datetime.now().isoformat()
    new_expense = Expense(id=str(uuid.uuid4()), amount=amount, category=category, date=date, description=description)
    self.expenses.append(new_expense)
    self.save()
    # ... rest of method
```

**Reason:** 
- Prevents NoneType formatting errors when date is not provided
- Generates proper UUIDs for tracking records
- Ensures date always has a value

---

#### Change 2.4: Fixed budget alert formatting in `add_expense()`
**Line affected:** Budget alert message in `add_expense()` method

**Original Code:**
```python
print(f"      Limit: ${cat_limit} | Spent: ${spent_cat}")
```

**Modified Code:**
```python
print(f"      Limit: ${cat_limit:.2f} | Spent: ${spent_cat:.2f}")
```

**Reason:** Ensures consistent currency formatting with 2 decimal places.

---

#### Change 2.5: Fixed `add_income()` to handle None dates and generate UUIDs
**Line affected:** `add_income()` method

**Original Code:**
```python
def add_income(self, amount, category, date, description):
    new_income = Income(amount, category, date, description)
    self.income.append(new_income)
    self.save()
    return new_income
```

**Modified Code:**
```python
def add_income(self, amount, category, date, description):
    if date is None:
        date = datetime.now().isoformat()
    new_income = Income(id=str(uuid.uuid4()), amount=amount, category=category, date=date, description=description)
    self.income.append(new_income)
    self.save()
    return new_income
```

**Reason:** Same as `add_expense()` - prevents NoneType errors and ensures proper UUID generation.

---

#### Change 2.6: Fixed `monthly_summary()` to safely convert amounts
**Line affected:** `monthly_summary()` method

**Original Code:**
```python
def monthly_summary(self):
    total_spent = sum(e.amount for e in self.expenses)
    # ... rest of method
```

**Modified Code:**
```python
def monthly_summary(self):
    total_spent = sum(float(e.amount) if isinstance(e.amount, (int, float, str)) else 0 for e in self.expenses)
    # ... rest of method
```

**Reason:** Handles cases where amounts are stored as strings in the database, preventing TypeError when adding values.

---

#### Change 2.7: Enhanced category budget check in `add_expense()`
**Line affected:** Category budget check in `add_expense()` method

**Original Code:**
```python
spent_cat = sum(e.amount for e in self.expenses if e.category == category)
```

**Modified Code:**
```python
spent_cat = sum(float(e.amount) if isinstance(e.amount, (int, float, str)) else 0 for e in self.expenses if e.category == category)
```

**Reason:** Safely converts string amounts to floats before summing to prevent TypeError.

---

## 3. Main.py
**File Purpose:** Application entry point and main menu orchestration

### Changes Made:

#### Change 3.1: Fixed exception handling
**Line affected:** Authentication error handling

**Original Code:**
```python
except Exception:
    print(f"[Auth Error] {e}")
```

**Modified Code:**
```python
except Exception as e:
    print(f"[Auth Error] {e}")
```

**Reason:** Fixes NameError where variable `e` was not defined in the exception handler.

---

#### Change 3.2: Removed non-existent authentication functions
**Line affected:** Authentication check block

**Original Code:**
```python
if auth_ready:
    try:
        if hasattr(authyann, 'login_menu'):
            current_username = authyann.login_menu()
        elif hasattr(authyann, 'main'):
            current_username = authyann.main()
        elif hasattr(authyann, 'login'):
            current_username = authyann.login()
    except Exception as e:
        print(f"[Auth Error] {e}")
```

**Modified Code:**
```python
if auth_ready:
    try:
        if hasattr(authyann, 'login_menu'):
            current_username = authyann.login_menu()
    except Exception as e:
        print(f"[Auth Error] {e}")
```

**Reason:** `authyann.main()` and `authyann.login()` functions don't exist in authyann.py. Only `login_menu()` exists.

---

#### Change 3.3: Added `.strip()` to user input
**Line affected:** User choice input

**Original Code:**
```python
choice = input("Selection: ")
```

**Modified Code:**
```python
choice = input("Selection: ").strip()
```

**Reason:** Removes leading/trailing whitespace from user input, preventing selection matching issues.

---

#### Change 3.4: Added explicit save before exit
**Line affected:** Exit menu option (choice '6')

**Original Code:**
```python
elif choice == '6':
    print("Saving session...")
    break
```

**Modified Code:**
```python
elif choice == '6':
    print("Saving session...")
    et.save()
    print("Goodbye!")
    break
```

**Reason:** 
- Ensures all data is explicitly saved before exiting
- Provides user feedback with exit message

---

## 4. Reports.py
**File Purpose:** Financial reports and analytics

### Changes Made:

#### Change 4.1: Removed top-level matplotlib import
**Line affected:** Import section

**Original Code:**
```python
import matplotlib.pyplot as plt

class ReportManager:
    # ...
```

**Modified Code:**
```python
class ReportManager:
    # ...
```

**Reason:** matplotlib is optional. Top-level import causes ModuleNotFoundError if not installed. Import is now done conditionally inside the visualization method.

---

#### Change 4.2: Fixed amount conversion in global balance report
**Line affected:** `generate_reports()` method, choice '1' section

**Original Code:**
```python
total_inc = sum(i.amount for i in incomes)
total_exp = sum(e.amount for e in expenses)
balance = total_inc - total_exp
```

**Modified Code:**
```python
total_inc = sum(float(i.amount) if isinstance(i.amount, (int, float, str)) else 0 for i in incomes)
total_exp = sum(float(e.amount) if isinstance(e.amount, (int, float, str)) else 0 for e in expenses)
balance = total_inc - total_exp
```

**Reason:** Safely converts string amounts to floats before arithmetic operations to prevent TypeError.

---

## 5. INCOME_EXPENSE_CATEGORIES_MODULE.py
**File Purpose:** Menu system for managing expenses and income

### Changes Made:

#### Change 5.1: Fixed method call
**Line affected:** `expenses_menu()` function

**Original Code:**
```python
items = et.list.expenses()
```

**Modified Code:**
```python
items = et.list_expenses()
```

**Reason:** `et.list.expenses()` attempts to access a non-existent attribute. The correct method is `et.list_expenses()`.

---

#### Change 5.2: Enhanced print_table to handle None values
**Line affected:** `print_table()` function inside `expenses_menu()`

**Original Code:**
```python
def print_table(items):
    if not items:
        print("No expenses to show.")
        return
    print(f"{'ID':36}  {'Date':10}  {'Category':12}  {'Amount':8}  Description")
    print('-'*90)
    for e in items:
        print(f"{e.id:36}  {e.date[:10]:10}  {e.category:12}  {e.amount:8.2f}  {e.description}")
```

**Modified Code:**
```python
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
```

**Reason:** 
- Prevents NoneType formatting errors from corrupted database records
- Safely converts string amounts to floats
- Displays "N/A" for missing data instead of crashing

---

#### Change 5.3: Enhanced print_income_table similarly
**Line affected:** `print_income_table()` function inside `income_menu()`

**Original Code:**
```python
def print_income_table(items):
    if not items:
        print("No income to show.")
        return
    print(f"{'ID':36}  {'Date':10}  {'Category':12}  {'Amount':8}  Description")
    print('-'*90)
    for i in items:
        print(f"{i.id:36}  {i.date[:10]:10}  {i.category:12}  {i.amount:8.2f}  {i.description}")
```

**Modified Code:**
```python
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
```

**Reason:** Same as print_table - handles corrupted data gracefully.

---

## 6. expense.py
**File Purpose:** Expense data model

### Changes Made:

#### Change 6.1: Enhanced `from_dict()` with data validation
**Line affected:** `from_dict()` class method

**Original Code:**
```python
@classmethod
def from_dict(cls, data: dict):
    return cls(**data)
```

**Modified Code:**
```python
@classmethod
def from_dict(cls, data: dict):
    try:
        # Ensure amount is a float
        amount = float(data.get('amount', 0))
        # Ensure date is a string
        date = str(data.get('date', datetime.now().isoformat()))
        # Ensure category is a string
        category = str(data.get('category', 'Other'))
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            amount=amount,
            category=category,
            date=date,
            description=str(data.get('description', ''))
        )
    except (ValueError, KeyError, TypeError):
        # Return a safe default if data is corrupted
        return cls(
            id=str(uuid.uuid4()),
            amount=0.0,
            category='Other',
            date=datetime.now().isoformat(),
            description='[Corrupted]'
        )
```

**Reason:** 
- Handles corrupted database records that have misaligned fields
- Safely converts types (e.g., string amounts to float)
- Returns safe defaults instead of crashing
- Prevents ValueError when converting non-numeric strings to float

---

## 7. income.py
**File Purpose:** Income data model

### Changes Made:

#### Change 7.1: Enhanced `from_dict()` with data validation
**Line affected:** `from_dict()` class method

**Original Code:**
```python
@classmethod
def from_dict(cls, data: dict):
    return cls(**data)
```

**Modified Code:**
```python
@classmethod
def from_dict(cls, data: dict):
    try:
        # Ensure amount is a float
        amount = float(data.get('amount', 0))
        # Ensure date is a string
        date = str(data.get('date', datetime.now().isoformat()))
        # Ensure category is a string
        category = str(data.get('category', 'Other'))
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            amount=amount,
            category=category,
            date=date,
            description=str(data.get('description', ''))
        )
    except (ValueError, KeyError, TypeError):
        # Return a safe default if data is corrupted
        return cls(
            id=str(uuid.uuid4()),
            amount=0.0,
            category='Other',
            date=datetime.now().isoformat(),
            description='[Corrupted]'
        )
```

**Reason:** Same as expense.py - handles corrupted data gracefully.

---

## 8. Budget.py
**File Purpose:** Budget management and alerts

### Changes Made:

#### Change 8.1: Enhanced `check_budget_status()` with safe type conversion
**Line affected:** `check_budget_status()` method

**Original Code:**
```python
def check_budget_status(self):
    print("\n--- BUDGET STATUS REPORT ---")
    
    total_spent = 0
    category_spent = {}
    
    for expense in self.tracker.expenses:
        amount = expense.amount
        cat = expense.category
        
        total_spent += amount
        category_spent[cat] = category_spent.get(cat, 0) + amount
```

**Modified Code:**
```python
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
```

**Reason:** 
- Safely converts string amounts to floats before arithmetic
- Handles TypeError when adding mixed types
- Provides default category for None values

---

## Summary of Change Categories

### 1. **Type Safety Fixes** (8 changes)
   - Converting string amounts to floats
   - Handling None values in calculations
   - Safe type casting with try-except blocks

### 2. **Data Integrity Fixes** (2 changes)
   - Enhanced `from_dict()` methods to validate and sanitize corrupted data
   - Ensures consistent data format on load

### 3. **Import and Module Fixes** (2 changes)
   - Added missing `uuid` import
   - Made `matplotlib` import optional

### 4. **Method Call Fixes** (1 change)
   - Fixed `et.list.expenses()` to `et.list_expenses()`

### 5. **Error Handling Fixes** (2 changes)
   - Fixed exception variable reference
   - Removed calls to non-existent functions

### 6. **User Experience Improvements** (2 changes)
   - Added input `.strip()` for cleaner input handling
   - Added explicit save and goodbye message on exit

**Total Changes: 19 modifications across 8 files**

