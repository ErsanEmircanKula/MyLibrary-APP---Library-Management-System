# MyLibrary - Library Management System

![MyLibrary](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)
![Tkinter](https://img.shields.io/badge/gui-tkinter-blue)
![License](https://img.shields.io/badge/license-mit-green)

## 📚 About

**MyLibrary** is a modern, user-friendly desktop application for managing your personal book collection.
With MyLibrary, you can easily add, edit, search, filter, and visualize your books.
The app supports importing/exporting data, statistics, and even fetching book info by ISBN!
![Logo](https://i.hizliresim.com/94nlcqf.png)
    
## ✨ Features

- **Add/Edit/Delete Books**  
- **Search & Filter** by title, author, publisher, category, tags, etc.
- **Statistics Dashboard** with charts and summary cards
- **Theme Support** (Light, Dark, Blue)
- **Export to Excel** and **Generate PDF Reports**
- **Bulk Import** from Excel/CSV
- **Book Details** with cover image and Goodreads link
- **ISBN Lookup** (fetch book info automatically)
- **Customizable Categories, Reading Status, and Tags**
- **Favorite Books** marking
- **Reset Database IDs**
## 🌐 API Usage

- **Fetching Book Information by ISBN:**
  - The application uses the [OpenLibrary Books API](https://openlibrary.org/dev/docs/api/books) service to automatically retrieve book details such as title, author, publisher, page count, and cover image when you enter an ISBN number.
  - This feature requires an internet connection.
  - You can use the "Get Book Information" button after entering the ISBN to auto-fill the book details.

---
