# MyLibrary - Library Management System

![MyLibrary](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)
![Tkinter](https://img.shields.io/badge/gui-tkinter-blue)
![License](https://img.shields.io/badge/license-mit-green)

## 📚 About

**MyLibrary** is a modern, user-friendly desktop application for managing your personal book collection.
With MyLibrary, you can easily add, edit, search, filter, and visualize your books.
The app supports importing/exporting data, statistics, and even fetching book info by ISBN!

![Logo](https://i.imgur.com/4EgGp0p.png)
    
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
## 🛠️ Build as EXE (Optional)

If you want to convert the application into a standalone Windows executable (.exe), you can use [PyInstaller](https://pyinstaller.org/):

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```
2. **Run the following command in your project directory:**
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon=ikon.ico MyLibrary.py
   ```
   - If you don't have an icon, you can remove the `--icon=ikon.ico` part.
3. **Find your .exe file in the `dist` folder:**
   - Example: `dist/MyLibrary.exe`
4. **Copy your database file (`mylibrary.db`) and any other required files to the same folder as the .exe if needed.**

> Now you can run your application on any Windows computer without needing Python installed!

---
