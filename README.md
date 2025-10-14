# 📘 LibraryEase

LibraryEase is a Python-based Library Management System designed for small institutions and personal use. It offers an intuitive GUI for managing books and members, handling book issues and returns, calculating late fees, tracking usage statistics, and maintaining borrow history.

## 🚀 Features

GUI-based book issue and return system using Tkinter

Visual analytics of most issued books using Matplotlib

Late fee calculation using NumPy (excludes weekends)

Persistent data storage with pandas and CSV files

Borrow and return logging via file handling

Add, manage, and update books and members easily

## 🛠️ Tech Stack & Tools

Python – Core programming language

Tkinter – For building the graphical user interface

pandas – To manage and manipulate book/member data

NumPy – For calculating late return fees using business days

Matplotlib – For visualizing the most frequently issued books

CSV & File I/O – To store book/member info and transaction logs

## 📦 Installation
```
Clone the repository:

git clone https://github.com/yourusername/LibraryEase.git
cd LibraryEase
```

## Install dependencies:
```
pip install pandas numpy matplotlib
```

## Run the application:
```
python libraryease.py
```

## 🧠 Usage Guide

Add Book – Enter details and click Add Book

Add Member – Enter ID and name, then click Add Member

Issue Book – Enter valid book and member IDs → Click Issue Book

Return Book – Provide the same info → Click Return Book

Analytics – Click View Most Issued Books to see a chart

## 📈 Late Fee Calculation

Allowed return period: 7 business days

Late fee: ₹2 per additional business day (excludes weekends)

Calculated using numpy.busday_count()

## 📌 Future Enhancements

Admin/staff login system

Search and filter capabilities

Overdue email alerts

Switch from CSV to SQL or SQLite

UI themes (e.g., dark mode)


## 📄 License

This project is licensed under the MIT License – see the LICENSE
 file for details.
