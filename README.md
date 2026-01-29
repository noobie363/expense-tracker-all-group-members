# Personal Expense Tracker

A comprehensive Python-based personal finance management application for tracking expenses, income, budgets, and generating financial reports.

## Features

- **Expense Management**: Add, edit, and remove expenses with categorization
- **Income Management**: Track income sources and amounts
- **Category Management**: Organize transactions with custom categories
- **Financial Reports**: Generate detailed financial reports and analytics
- **Budget Management**: Set budgets and receive alerts when limits are exceeded
- **User Profiles**: Support for multiple user profiles with individual tracking
- **Authentication**: Optional authentication system for secure access

## Project Structure

```
├── Main.py                              # Application entry point
├── Menu.py                              # Menu interface
├── tracker.py                           # Core expense tracking logic
├── income.py                            # Income management
├── expense.py                           # Expense management
├── Budget.py                            # Budget management and alerts
├── Reports.py                           # Financial reporting
├── INCOME_EXPENSE_CATEGORIES_MODULE.py # Category management
├── authyann.py                          # Authentication module (optional)
├── users.json                           # User data storage
└── README.md                            # This file
```

## Requirements

- Python 3.x
- Virtual environment recommended

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "send to matias"
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies (if any):
```bash
pip install -r requirements.txt  # If applicable
```

## Usage

Run the application:
```bash
python Main.py
```

Follow the interactive menu to:
- Manage your expenses and income
- Organize categories
- View financial reports
- Set and monitor budgets

## Getting Started

1. Start the application
2. Create or confirm your user profile
3. Use the main menu to navigate through features
4. Select options to manage expenses, income, categories, or view reports

## Features in Detail

### Expense Management
Track all your expenses with details like amount, category, and date.

### Income Management
Log income sources and amounts for a complete financial picture.

### Budget Alerts
Set spending limits and receive alerts when approaching or exceeding them.

### Financial Reports
Generate comprehensive reports to analyze spending patterns and financial health.

### Multi-User Support
Support for multiple user profiles, each with their own financial data.

## Data Storage

User data is stored locally in `users.json` format for privacy and easy access.

## Contributing

Feel free to fork and submit pull requests for any improvements.

## License

This project is provided as-is for personal use.

---

**Author**: Matias  
**Last Updated**: January 2026
