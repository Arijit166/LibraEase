# 📘 LibraEase

LibraEase is a Python-based Library Management System designed for small institutions and personal use. It offers a fully-featured GUI for managing books, members, borrow/return workflows, and analytics, with separate panels for admin and users.

## 🚀 Features
### Admin Panel

- Secure login using an Admin Passkey stored in .env (ADMIN_PASSKEY)

- Add, edit, delete, and search books

- Manage members and track borrowing history

- Issue and return books on behalf of users

- Automatic updates to user records when books are collected or returned

- Analytics: View most to least borrowed books using charts

### User Panel

- Signup and login for regular users

- Browse available books and add to cart

- Borrow and return books

- View personal borrowing history

### Shared Functionality

- GUI-based interface built with Tkinter

- Data handling with pandas (books, members, borrow records)

- Visual analytics with Matplotlib

- Persistent storage using CSV and file I/O

## 🛠️ Tech Stack & Tools

- Python – Core programming language

- Tkinter – Graphical user interface

- pandas – Data management and manipulation

- NumPy – For calculations and data handling

- Matplotlib – Charts for analytics

- CSV & File I/O – Persistent storage

## 📁 Project Structure
```
LibraEase/
│
├─ main.py                     # Entry point
├─ database.py                 # Handles CSV and data operations
│
├─ admin/
│   ├─ admin_issue_return.py   # Book issue and return for admin
│   ├─ members/                # Member management
│   ├─ manage_book/            # Add, edit, delete, search books
│   └─ analytics/              # Borrowing analytics
│
├─ user/
│   ├─ cart/                   # Add books to cart
│   ├─ borrowing/              # Borrow/return workflow
│   └─ book.py                 # Book browsing and details
│
├─ data/                       # CSV files for books, members, borrow records
└─ .env                        # Stores admin passkey (ADMIN_PASSKEY)
```

## 📦 Installation

### Clone the repository:
```
git clone https://github.com/yourusername/LibraEase.git
cd LibraEase
```

### Install dependencies:
```
pip install pandas numpy matplotlib
```

### Run the application: 
```
python main.py
```

## 📌 Future Enhancements

- Overdue email notifications

- Switch to SQL/SQLite for more robust storage

- Advanced search and filter options

- UI themes (e.g., dark mode)

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.
