import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import sqlite3
import requests
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class KitaplikUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x800")

        # Temaları ayarla
        self.setup_themes()

        # Varsayılan tema (açık)
        self.current_theme = "cosmo"
        self.style = ttk.Style(theme=self.current_theme)

        # Tema değiştirme butonu
        self.theme_button = ttk.Button(
            root,
            text="🌙 Dark Theme",
            style='secondary.TButton',
            command=self.toggle_theme
        )
        self.theme_button.pack(anchor='ne', padx=10, pady=5)

        # Ana container
        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.pack(fill=BOTH, expand=YES)

        # Notebook
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        # Sekmeler
        self.ekle_frame = ttk.Frame(self.notebook, padding="10")
        self.liste_frame = ttk.Frame(self.notebook, padding="10")
        self.istatistik_frame = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.ekle_frame, text="Add Book")
        self.notebook.add(self.liste_frame, text="List Books")
        self.notebook.add(self.istatistik_frame, text="Statistics")

        self.setup_ekle_frame()
        self.setup_liste_frame()
        self.setup_istatistik_frame()

    def toggle_theme(self):
        if self.current_theme == "cosmo":
            self.current_theme = "darkly"
            self.style.theme_use("darkly")
            self.theme_button.configure(text="☀️ Light Theme")
        else:
            self.current_theme = "cosmo"
            self.style.theme_use("cosmo")
            self.theme_button.configure(text="🌙 Dark Theme")

    def setup_ekle_frame(self):
        # ISBN Girişi
        isbn_frame = ttk.Frame(self.ekle_frame)
        isbn_frame.pack(fill=X, pady=10)

        ttk.Label(isbn_frame, text="ISBN:").pack(side=LEFT, padx=5)
        self.isbn_entry = ttk.Entry(isbn_frame)
        self.isbn_entry.pack(side=LEFT, padx=5, fill=X, expand=YES)

        ttk.Button(
            isbn_frame,
            text="🔍 Get Book Information",
            command=self.fetch_book_info
        ).pack(side=LEFT, padx=5)

        # Kitap Bilgileri Frame
        api_frame = ttk.LabelFrame(self.ekle_frame, text="Book Information", padding="10")
        api_frame.pack(fill=X, pady=10)

        self.api_entries = {}
        api_labels = ["Book Title:", "Author:", "Publisher:", "Page Count:", "Cover URL:"]

        for i, label in enumerate(api_labels):
            ttk.Label(api_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(api_frame, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            self.api_entries[label] = entry

        # Ek Bilgiler Frame
        manual_frame = ttk.LabelFrame(self.ekle_frame, text="Additional Information", padding="10")
        manual_frame.pack(fill=X, pady=10)

        self.manual_entries = {}

        # Kategori için Combobox
        ttk.Label(manual_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Category:"] = ttk.Combobox(manual_frame, width=47, values=[
            "Roman", "Science Fiction", "Fantasy", "History", "Science",
            "Philosophy", "Psychology", "Personal Growth", "Biography",
            "Poetry", "Essay", "Research", "Comic Book", "Other"
        ])
        self.manual_entries["Category:"].grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Okuma Durumu için Combobox
        ttk.Label(manual_frame, text="Reading Status:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Reading Status:"] = ttk.Combobox(manual_frame, width=47, values=[
            "Read", "Unread", "Reading", "Half-Finished", "In Wishlist"
        ])
        self.manual_entries["Reading Status:"].grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Alım Tarihi için Entry
        ttk.Label(manual_frame, text="Purchase Date:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Purchase Date:"] = ttk.Entry(manual_frame, width=50)
        self.manual_entries["Purchase Date:"].grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.manual_entries["Purchase Date:"].insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Fiyat için Spinbox
        ttk.Label(manual_frame, text="Price (TL):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Price:"] = ttk.Spinbox(manual_frame, width=44, from_=0, to=99999, increment=1)
        self.manual_entries["Price:"].grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Puanlama için Spinbox
        ttk.Label(manual_frame, text="Rating:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Rating:"] = ttk.Spinbox(manual_frame, width=44, from_=1, to=10, increment=1)
        self.manual_entries["Rating:"].grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Favori için Combobox
        ttk.Label(manual_frame, text="Favorite:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Favorite:"] = ttk.Combobox(manual_frame, width=47, values=["Yes", "No"])
        self.manual_entries["Favorite:"].grid(row=5, column=1, padx=5, pady=5, sticky='w')

        # Etiketler için Entry
        ttk.Label(manual_frame, text="Tags:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        self.manual_entries["Tags:"] = ttk.Entry(manual_frame, width=50)
        self.manual_entries["Tags:"].grid(row=6, column=1, padx=5, pady=5, sticky='w')
        ttk.Label(manual_frame, text="(Separate tags with commas)").grid(row=7, column=1, padx=5, sticky='w')

        # Kaydet butonu
        ttk.Button(self.ekle_frame, text="Save",
                   style='success.TButton',
                   command=self.save_book).pack(pady=20)

    def setup_liste_frame(self):
        # Filtre paneli
        filter_frame = ttk.LabelFrame(self.liste_frame, text="Filters", padding="10")
        filter_frame.pack(fill=X, pady=10)

        # Filtreler
        filters_grid = ttk.Frame(filter_frame)
        filters_grid.pack(fill=X, pady=5)

        # Okuma Durumu
        ttk.Label(filters_grid, text="Reading Status:").grid(row=0, column=0, padx=5, pady=5)
        self.okuma_durumu_var = tk.StringVar()
        okuma_combo = ttk.Combobox(filters_grid, textvariable=self.okuma_durumu_var,
                                   values=["All", "Read", "Unread", "Reading"])
        okuma_combo.grid(row=0, column=1, padx=5, pady=5)
        okuma_combo.set("All")

        # Fiyat Aralığı
        ttk.Label(filters_grid, text="Price Range:").grid(row=0, column=2, padx=5, pady=5)
        self.min_fiyat = ttk.Entry(filters_grid, width=10)
        self.min_fiyat.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(filters_grid, text="-").grid(row=0, column=4)
        self.max_fiyat = ttk.Entry(filters_grid, width=10)
        self.max_fiyat.grid(row=0, column=5, padx=5, pady=5)

        # Tarih Aralığı
        ttk.Label(filters_grid, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.min_tarih = ttk.Entry(filters_grid, width=10)
        self.min_tarih.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(filters_grid, text="-").grid(row=1, column=2)
        self.max_tarih = ttk.Entry(filters_grid, width=10)
        self.max_tarih.grid(row=1, column=3, padx=5, pady=5)

        # Etiket
        ttk.Label(filters_grid, text="Tag:").grid(row=1, column=4, padx=5, pady=5)
        self.etiket_var = ttk.Entry(filters_grid, width=20)
        self.etiket_var.grid(row=1, column=5, padx=5, pady=5)

        # Filtrele butonu
        ttk.Button(filter_frame, text="Filter",
                   style='primary.TButton',
                   command=self.apply_filters).pack(pady=10)

        # Tablo oluşturma
        columns = [
            "id", "isbn", "title", "author", "publisher",
            "category", "reading_status", "purchase_date", "price"
        ]

        column_widths = {
            "id": 50,
            "isbn": 100,
            "title": 200,
            "author": 150,
            "publisher": 150,
            "category": 100,
            "reading_status": 100,
            "purchase_date": 100,
            "price": 100
        }

        # Tablo container frame
        table_frame = ttk.Frame(self.liste_frame)
        table_frame.pack(fill=BOTH, expand=YES, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview oluşturma
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode="browse",
            height=20
        )

        # Scrollbar bağlama
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.table.yview)

        # Sütun başlıkları ve genişlikleri
        column_names = {
            "id": "ID",
            "isbn": "ISBN",
            "title": "Book Title",
            "author": "Author",
            "publisher": "Publisher",
            "category": "Category",
            "reading_status": "Reading Status",
            "purchase_date": "Purchase Date",
            "price": "Price (TL)"
        }

        for col in columns:
            self.table.heading(col, text=column_names[col],
                               command=lambda c=col: self.sort_table(c))
            self.table.column(col, width=column_widths[col], minwidth=50)

        self.table.pack(side=LEFT, fill=BOTH, expand=YES)

        # Butonlar
        button_frame = ttk.Frame(self.liste_frame)
        button_frame.pack(fill=X, pady=5)

        self.edit_button = ttk.Button(
            button_frame,
            text="Edit",
            style='info.TButton',
            command=self.edit_book,
            state="disabled"
        )
        self.edit_button.pack(side=LEFT, padx=5)

        self.delete_button = ttk.Button(
            button_frame,
            text="Delete",
            style='danger.TButton',
            command=self.delete_book,
            state="disabled"
        )
        self.delete_button.pack(side=LEFT, padx=5)

        # Tablo seçim olayını bağlama
        self.table.bind("<<TreeviewSelect>>", self.on_select)
        self.table.bind("<Double-1>", self.show_book_details)

        # Arama kutusu
        search_frame = ttk.Frame(self.liste_frame)
        search_frame.pack(fill=X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_books)

        # Başlangıçta kitapları listele
        self.list_all_books()

    def on_select(self, event=None):
        # Seçili satırı kontrol et
        selected = self.table.selection()
        if selected:
            # Düzenle ve Sil butonlarını aktif et
            self.edit_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else:
            # Düzenle ve Sil butonlarını pasif et
            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def setup_istatistik_frame(self):
        # Ana container
        stats_container = ttk.Frame(self.istatistik_frame)
        stats_container.pack(fill=BOTH, expand=YES)

        # Sol Panel - İstatistik Kartları
        left_panel = ttk.Frame(stats_container)
        left_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)

        # Sağ Panel - Grafikler
        right_panel = ttk.Frame(stats_container)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10)

        # İstatistik kartları için stil
        card_style = {'font': ('Segoe UI', 12), 'padding': 15, 'relief': 'solid'}

        # İstatistik kartları
        stats = self.get_library_stats()
        self.create_stat_cards(left_panel, stats)

        # Grafikler
        self.create_category_pie_chart(right_panel)

    def create_stat_cards(self, parent, stats):
        # İstatistik kartlarını 2 sütunda göster
        left_stats = ttk.Frame(parent)
        left_stats.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        right_stats = ttk.Frame(parent)
        right_stats.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        # Sol sütun kartları
        self.create_stat_card(left_stats, "📚 Total Books", stats['toplam_kitap'])
        self.create_stat_card(left_stats, "✅ Read Books", stats['okunan_kitap'])
        self.create_stat_card(left_stats, "📖 Unread Books", stats['okunmayan_kitap'])
        self.create_stat_card(left_stats, "💰 Total Value", f"{stats['toplam_deger']:.2f} TL")

        # Sağ sütun kartları
        self.create_stat_card(right_stats, "📊 Average Rating", f"{stats['ortalama_puan']:.1f}/10")
        self.create_stat_card(right_stats, "📚 Most Read Category", stats['en_cok_kategori'])
        self.create_stat_card(right_stats, "💫 Favorite Books", stats['favori_sayisi'])

    def create_stat_card(self, parent, title, value):
        card = ttk.Frame(parent, padding="10")
        card.pack(pady=5, fill=X)

        # Kart içeriği için frame
        content = ttk.Frame(card)
        content.pack(fill=X, expand=YES)

        # Başlık
        ttk.Label(content, text=title,
                  font=('Segoe UI', 11),
                  wraplength=200).pack(anchor='w')

        # Değer
        ttk.Label(content, text=str(value),
                  font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 0))

        # Ayırıcı çizgi
        ttk.Separator(card, orient='horizontal').pack(fill=X, pady=(10, 0))

    def get_library_stats(self):
        conn = sqlite3.connect("mylibrary.db")
        cursor = conn.cursor()

        stats = {}

        # Toplam kitap sayısı
        cursor.execute("SELECT COUNT(*) FROM MyLibrary")
        stats['toplam_kitap'] = cursor.fetchone()[0]

        # Okunan/Okunmayan kitap sayısı
        cursor.execute("SELECT COUNT(*) FROM MyLibrary WHERE reading_status='Read'")
        stats['okunan_kitap'] = cursor.fetchone()[0]
        stats['okunmayan_kitap'] = stats['toplam_kitap'] - stats['okunan_kitap']

        # Toplam değer
        cursor.execute("SELECT SUM(price) FROM MyLibrary")
        stats['toplam_deger'] = cursor.fetchone()[0] or 0

        # Ortalama puan
        cursor.execute("SELECT AVG(rating) FROM MyLibrary")
        stats['ortalama_puan'] = cursor.fetchone()[0] or 0

        # En çok okunan kategori
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM MyLibrary 
            GROUP BY category 
            ORDER BY COUNT(*) DESC 
            LIMIT 1
        """)
        result = cursor.fetchone()
        stats['en_cok_kategori'] = result[0] if result else "-"

        # Favori kitap sayısı
        cursor.execute("SELECT COUNT(*) FROM MyLibrary WHERE favorite='Yes'")
        stats['favori_sayisi'] = cursor.fetchone()[0] or 0

        conn.close()
        return stats

    def create_category_pie_chart(self, parent):
        conn = sqlite3.connect("mylibrary.db")
        cursor = conn.cursor()

        cursor.execute("SELECT category, COUNT(*) FROM MyLibrary GROUP BY category")
        data = cursor.fetchall()

        conn.close()

        if data:
            # Grafik için frame
            chart_frame = ttk.LabelFrame(parent, text="Category Distribution", padding="10")
            chart_frame.pack(fill=BOTH, expand=YES)

            # Verileri hazırla
            labels = [row[0] for row in data]
            sizes = [row[1] for row in data]

            # Renk paleti
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC',
                      '#99CCFF', '#FFB366', '#FF99FF', '#99FF99', '#FFB366']

            # Grafik boyutunu küçült ve daha okunaklı hale getir
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

            # Pasta grafik
            wedges, texts, autotexts = ax1.pie(sizes,
                                               labels=labels,
                                               colors=colors,
                                               autopct='%1.1f%%',
                                               pctdistance=0.85,
                                               textprops={'fontsize': 8})

            # Pasta grafik özelleştirme
            plt.setp(autotexts, size=7, weight="bold")
            plt.setp(texts, size=7)
            ax1.set_title("Pie Chart", pad=10, fontsize=10)

            # Çubuk grafik
            bars = ax2.bar(range(len(labels)), sizes, color=colors)
            ax2.set_title("Bar Chart", pad=10, fontsize=10)

            # Çubuk grafik özelleştirme
            ax2.set_xticks(range(len(labels)))
            ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=7)
            ax2.tick_params(axis='y', labelsize=7)

            # Çubukların üzerine değerleri yaz
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{int(height)}',
                         ha='center', va='bottom', fontsize=7)

            # Grafik düzeni
            plt.tight_layout()

            # Canvas oluştur ve boyutunu ayarla
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.configure(height=300)  # Canvas yüksekliğini ayarla
            canvas_widget.pack(fill=BOTH, expand=YES)

            # Açıklama tablosu
            table_frame = ttk.Frame(parent)
            table_frame.pack(fill=X, pady=5)

            # Başlıklar
            headers = ["Category", "Book Count", "Percentage"]
            for col, header in enumerate(headers):
                ttk.Label(table_frame, text=header, font=('Segoe UI', 9, 'bold')).grid(
                    row=0, column=col, padx=5, pady=2, sticky='w')

            # Veriler
            total = sum(sizes)
            for i, (label, size) in enumerate(zip(labels, sizes)):
                ttk.Label(table_frame, text=label, font=('Segoe UI', 9)).grid(
                    row=i + 1, column=0, padx=5, pady=1, sticky='w')
                ttk.Label(table_frame, text=str(size), font=('Segoe UI', 9)).grid(
                    row=i + 1, column=1, padx=5, pady=1, sticky='w')
                ttk.Label(table_frame, text=f"%{(size / total) * 100:.1f}", font=('Segoe UI', 9)).grid(
                    row=i + 1, column=2, padx=5, pady=1, sticky='w')

    def fetch_book_info(self):
        isbn = self.isbn_entry.get().strip()
        if not isbn:
            messagebox.showwarning("Warning", "Please enter ISBN!")
            return

        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

        try:
            response = requests.get(url).json()
            key = f"ISBN:{isbn}"

            if key in response:
                book_info = response[key]

                self.api_entries["Book Title:"].delete(0, tk.END)
                self.api_entries["Book Title:"].insert(0, book_info.get("title", ""))

                authors = ", ".join([author['name'] for author in book_info.get("authors", [])])
                self.api_entries["Author:"].delete(0, tk.END)
                self.api_entries["Author:"].insert(0, authors)

                publisher = book_info.get("publishers", [{"name": ""}])[0]["name"]
                self.api_entries["Publisher:"].delete(0, tk.END)
                self.api_entries["Publisher:"].insert(0, publisher)

                pages = book_info.get("number_of_pages", "")
                self.api_entries["Page Count:"].delete(0, tk.END)
                self.api_entries["Page Count:"].insert(0, str(pages))

                cover_url = book_info.get("cover", {}).get("large", "")
                self.api_entries["Cover URL:"].delete(0, tk.END)
                self.api_entries["Cover URL:"].insert(0, cover_url)

                messagebox.showinfo("Success", "Book information retrieved!")
            else:
                messagebox.showwarning("Warning", "Book not found!")

        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving information: {str(e)}")

    def save_book(self):
        try:
            data = {
                "isbn": self.isbn_entry.get(),
                "title": self.api_entries["Book Title:"].get(),
                "author": self.api_entries["Author:"].get(),
                "publisher": self.api_entries["Publisher:"].get(),
                "page_count": self.api_entries["Page Count:"].get() or 0,
                "cover_url": self.api_entries["Cover URL:"].get(),
                "category": self.manual_entries["Category:"].get(),
                "reading_status": self.manual_entries["Reading Status:"].get(),
                "purchase_date": self.manual_entries["Purchase Date:"].get(),
                "price": self.manual_entries["Price:"].get() or 0,
                "rating": self.manual_entries["Rating:"].get() or 0,
                "favorite": self.manual_entries["Favorite:"].get(),
                "tags": self.manual_entries["Tags:"].get()
            }

            conn = sqlite3.connect("mylibrary.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO MyLibrary (
                    isbn, title, author, publisher, category,
                    reading_status, purchase_date, price, page_count,
                    rating, favorite, tags, cover_url, average_rating
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["isbn"], data["title"], data["author"], data["publisher"],
                data["category"], data["reading_status"], data["purchase_date"],
                float(data["price"]), int(data["page_count"]),
                int(data["rating"]), data["favorite"], data["tags"],
                data["cover_url"], 0.0
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Book saved successfully!")
            self.clear_entries()
            self.list_all_books()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This ISBN is already registered!")
        except Exception as e:
            messagebox.showerror("Error", f"Save error: {str(e)}")

    def list_all_books(self):
        # Mevcut satırları temizle
        for item in self.table.get_children():
            self.table.delete(item)

        conn = sqlite3.connect("mylibrary.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, isbn, title, author, publisher, 
                   category, reading_status, purchase_date, price 
            FROM MyLibrary
        """)

        for book in cursor.fetchall():
            self.table.insert("", "end", values=book)

        conn.close()

    def apply_filters(self):
        filters = []
        params = []

        if self.okuma_durumu_var.get() != "All":
            filters.append("reading_status = ?")
            params.append(self.okuma_durumu_var.get())

        if self.min_fiyat.get():
            filters.append("price >= ?")
            params.append(float(self.min_fiyat.get()))
        if self.max_fiyat.get():
            filters.append("price <= ?")
            params.append(float(self.max_fiyat.get()))

        if self.min_tarih.get():
            filters.append("purchase_date >= ?")
            params.append(self.min_tarih.get())
        if self.max_tarih.get():
            filters.append("purchase_date <= ?")
            params.append(self.max_tarih.get())

        if self.etiket_var.get():
            filters.append("tags LIKE ?")
            params.append(f"%{self.etiket_var.get()}%")

        query = "SELECT * FROM MyLibrary"
        if filters:
            query += " WHERE " + " AND ".join(filters)

        self.show_filtered_results(query, tuple(params))

    def show_filtered_results(self, query, params):
        # Mevcut satırları temizle
        for item in self.table.get_children():
            self.table.delete(item)

        conn = sqlite3.connect("mylibrary.db")
        cursor = conn.cursor()

        cursor.execute(query, params)
        for book in cursor.fetchall():
            self.table.insert("", "end", values=book[:9])  # İlk 9 sütunu göster

        conn.close()

    def show_book_details(self, event):
        try:
            selected = self.table.selection()
            if not selected:
                return

            book_id = self.table.item(selected)['values'][0]

            conn = sqlite3.connect("mylibrary.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MyLibrary WHERE id=?", (book_id,))
            book = cursor.fetchone()
            conn.close()

            if not book:
                return

            detail_window = ttk.Toplevel(self.root)
            detail_window.title("Book Details")
            detail_window.geometry("400x700")

            # Kapak resmi
            if book[13]:  # cover_url
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}  # User-Agent ekledik
                    response = requests.get(book[13], headers=headers)
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    img = img.resize((200, 300), Image.Resampling.LANCZOS)  # LANCZOS ekledik
                    photo = ImageTk.PhotoImage(img)

                    label = ttk.Label(detail_window, image=photo)
                    label.image = photo
                    label.pack(pady=10)
                except Exception as e:
                    ttk.Label(detail_window, text=f"Cover image not loaded: {str(e)}").pack(pady=10)

            # Kitap bilgileri
            details_frame = ttk.Frame(detail_window, padding="20")
            details_frame.pack(fill=BOTH, expand=YES)

            labels = [
                "ID:", "ISBN:", "Book Title:", "Author:", "Publisher:",
                "Category:", "Reading Status:", "Purchase Date:", "Price:",
                "Page Count:", "Rating:", "Favorite:", "Tags:"
            ]

            for i, label in enumerate(labels):
                ttk.Label(details_frame, text=label, font=('Segoe UI', 10, 'bold')).grid(
                    row=i, column=0, sticky='e', padx=5, pady=2)
                ttk.Label(details_frame, text=str(book[i])).grid(
                    row=i, column=1, sticky='w', padx=5, pady=2)

            # Düzenleme butonu ekle
            ttk.Button(detail_window, text="Edit",
                       style='info.TButton',
                       command=lambda: self.edit_book(book_id)).pack(pady=10)

            # Goodreads linki ekle
            if book[1]:  # ISBN varsa
                goodreads_url = f"https://www.goodreads.com/search?q={book[1]}"
                ttk.Button(detail_window, text="Search on Goodreads",
                           command=lambda: webbrowser.open(goodreads_url)).pack(pady=5)

        except IndexError:
            messagebox.showwarning("Warning", "Please select a book!")

    def edit_book(self, book_id=None):
        try:
            if book_id is None:
                selected = self.table.selection()
                if not selected:
                    return
                book_id = self.table.item(selected)['values'][0]

            conn = sqlite3.connect("mylibrary.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MyLibrary WHERE id=?", (book_id,))
            book = cursor.fetchone()
            conn.close()

            if not book:
                return

            edit_window = ttk.Toplevel(self.root)
            edit_window.title("Edit Book")
            edit_window.geometry("500x800")

            # Ana frame
            main_frame = ttk.Frame(edit_window, padding="20")
            main_frame.pack(fill=BOTH, expand=YES)

            # Başlık
            ttk.Label(main_frame, text="Edit Book", font=('Segoe UI', 16, 'bold')).pack(pady=10)

            # Düzenleme alanları için frame
            edit_frame = ttk.Frame(main_frame)
            edit_frame.pack(fill=BOTH, expand=YES, pady=10)

            # Alanları gruplandıralım
            fields = {
                "Basic Information": [
                    ("Book Title", book[2]),
                    ("Author", book[3]),
                    ("Publisher", book[4])
                ],
                "Category and Status": [
                    ("Category", book[5], ["Roman", "Science Fiction", "Fantasy", "History", "Science",
                                           "Philosophy", "Psychology", "Personal Growth", "Biography",
                                           "Poetry", "Essay", "Research", "Comic Book", "Other"]),
                    ("Reading Status", book[6], ["Read", "Unread", "Reading", "Half-Finished", "In Wishlist"])
                ],
                "Details": [
                    ("Purchase Date", book[7]),
                    ("Price", book[8], 0, 99999),  # Spinbox için min ve max değerler
                    ("Page Count", book[9], 1, 9999),
                    ("Rating", book[10], 1, 10),
                    ("Favorite", book[11], ["Yes", "No"]),
                    ("Tags", book[12])
                ]
            }

            entries = {}
            row = 0

            for group_title, group_fields in fields.items():
                # Grup başlığı
                ttk.Label(edit_frame, text=group_title, font=('Segoe UI', 12, 'bold')).grid(
                    row=row, column=0, columnspan=2, pady=(15, 5), sticky='w')
                row += 1

                for field_info in group_fields:
                    field_name = field_info[0]
                    field_value = field_info[1]

                    ttk.Label(edit_frame, text=field_name + ":", font=('Segoe UI', 10)).grid(
                        row=row, column=0, padx=5, pady=5, sticky='e')

                    # Alan tipine göre widget oluştur
                    if len(field_info) > 2 and isinstance(field_info[2], list):
                        # Combobox için
                        entry = ttk.Combobox(edit_frame, values=field_info[2], width=40)
                        entry.set(field_value)
                    elif len(field_info) > 3:
                        # Spinbox için
                        entry = ttk.Spinbox(edit_frame, from_=field_info[2], to=field_info[3], width=39)
                        entry.set(field_value)
                    else:
                        # Normal Entry için
                        entry = ttk.Entry(edit_frame, width=40)
                        entry.insert(0, field_value)

                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')
                    entries[field_name] = entry
                    row += 1

            # Butonlar için frame
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=X, pady=20)

            ttk.Button(button_frame, text="Cancel", style='secondary.TButton',
                       command=edit_window.destroy).pack(side=RIGHT, padx=5)

            ttk.Button(button_frame, text="Save", style='success.TButton',
                       command=lambda: self.save_edit(book_id, entries, edit_window)).pack(side=RIGHT, padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Error opening edit window: {str(e)}")

    def save_edit(self, book_id, entries, edit_window):
        try:
            conn = sqlite3.connect("mylibrary.db")
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE MyLibrary 
                SET title=?, author=?, publisher=?, category=?,
                    reading_status=?, purchase_date=?, price=?, page_count=?,
                    rating=?, favorite=?, tags=?
                WHERE id=?
            """, (
                entries["Book Title"].get(),
                entries["Author"].get(),
                entries["Publisher"].get(),
                entries["Category"].get(),
                entries["Reading Status"].get(),
                entries["Purchase Date"].get(),
                float(entries["Price"].get()),
                int(entries["Page Count"].get()),
                int(entries["Rating"].get()),
                entries["Favorite"].get(),
                entries["Tags"].get(),
                book_id
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Changes saved!")
            edit_window.destroy()
            self.list_all_books()

        except Exception as e:
            messagebox.showerror("Error", f"Edit error: {str(e)}")

    def delete_book(self):
        try:
            selected = self.table.selection()
            if not selected:
                return

            book_id = self.table.item(selected)['values'][0]

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
                conn = sqlite3.connect("mylibrary.db")
                cursor = conn.cursor()

                try:
                    cursor.execute("DELETE FROM MyLibrary WHERE id=?", (book_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Book deleted!")
                    self.list_all_books()

                except Exception as e:
                    messagebox.showerror("Error", f"Delete error: {str(e)}")

                finally:
                    conn.close()

        except IndexError:
            messagebox.showwarning("Warning", "Please select the book to delete!")

    def export_to_excel(self):
        conn = sqlite3.connect("mylibrary.db")
        df = pd.read_sql_query("SELECT * FROM MyLibrary", conn)
        conn.close()

        today = datetime.now().strftime("%Y%m%d")
        filename = f"kutuphane_veriler_{today}.xlsx"

        df.to_excel(filename, index=False)
        messagebox.showinfo("Success", f"Data exported to {filename}!")

    def clear_entries(self):
        self.isbn_entry.delete(0, tk.END)
        for entry in self.api_entries.values():
            entry.delete(0, tk.END)
        for entry in self.manual_entries.values():
            entry.delete(0, tk.END)

    def search_books(self, event):
        search_text = self.search_entry.get().lower()
        self.show_filtered_results(
            f"SELECT * FROM MyLibrary WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(publisher) LIKE ? OR LOWER(category) LIKE ? OR LOWER(tags) LIKE ?",
            (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))

    def sort_table(self, column):
        # Mevcut tabloyu sıralama
        self.table.sort(column, 'ascending')

    def generate_pdf_report(self):
        # PDF dosya adı
        filename = f"kutuphane_raporu_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Başlık
        elements.append(Paragraph("Library Report", styles['Title']))
        elements.append(Spacer(1, 20))

        # İstatistikler
        stats = self.get_library_stats()
        stats_data = [
            ["Statistic", "Value"],
            ["Total Books", str(stats['toplam_kitap'])],
            ["Read Books", str(stats['okunan_kitap'])],
            ["Unread Books", str(stats['okunmayan_kitap'])],
            ["Total Value", f"{stats['toplam_deger']:.2f} TL"],
            ["Average Rating", f"{stats['ortalama_puan']:.1f}/10"],
            ["Most Read Category", stats['en_cok_kategori']],
            ["Favorite Books", str(stats['favori_sayisi'])]
        ]

        # Tablo oluştur
        table = Table(stats_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

        # PDF oluştur
        doc.build(elements)
        messagebox.showinfo("Success", f"Report created: {filename}")

    def setup_themes(self):
        # Tema seçenekleri
        self.themes = {
            "Light": {
                "theme_name": "cosmo",
                "bg_color": "#ffffff",
                "fg_color": "#000000",
                "accent_color": "#007bff"
            },
            "Dark": {
                "theme_name": "darkly",
                "bg_color": "#222222",
                "fg_color": "#ffffff",
                "accent_color": "#375a7f"
            },
            "Blue": {
                "theme_name": "litera",
                "bg_color": "#e3f2fd",
                "fg_color": "#000000",
                "accent_color": "#2196f3"
            }
        }

        # Tema menüsü
        theme_menu = tk.Menu(self.root)
        self.root.config(menu=theme_menu)

        theme_submenu = tk.Menu(theme_menu, tearoff=0)
        theme_menu.add_cascade(label="Theme", menu=theme_submenu)

        for theme_name in self.themes.keys():
            theme_submenu.add_command(
                label=theme_name,
                command=lambda t=theme_name: self.change_theme(t)
            )

    def change_theme(self, theme_name):
        theme = self.themes[theme_name]
        self.style.theme_use(theme["theme_name"])

        # Özel widget renkleri
        self.style.configure("TFrame", background=theme["bg_color"])
        self.style.configure("TLabel", background=theme["bg_color"], foreground=theme["fg_color"])
        self.style.configure("TButton", background=theme["accent_color"])

    def bulk_import_books(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )

        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)

                for _, row in df.iterrows():
                    # Veritabanına ekle
                    self.save_book_from_data(row)

                messagebox.showinfo(
                    "Success",
                    f"{len(df)} books successfully imported!"
                )
                self.list_all_books()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Bulk book import error: {str(e)}"
                )

    def setup_menu(self):
        # Menü çubuğu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Generate PDF Report", command=self.generate_pdf_report)
        file_menu.add_command(label="Export to Excel", command=self.export_to_excel)
        file_menu.add_command(label="Bulk Book Import", command=self.bulk_import_books)
        file_menu.add_command(label="Reset IDs", command=self.reset_database_ids)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Görünüm menüsü
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)

        # Tema alt menüsü
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        for theme_name in self.themes.keys():
            theme_menu.add_command(
                label=theme_name,
                command=lambda t=theme_name: self.change_theme(t)
            )

    def reset_database_ids(self):
        try:
            conn = sqlite3.connect("mylibrary.db")
            cursor = conn.cursor()

            # Geçici tablo oluştur
            cursor.execute("""
                CREATE TABLE temp_mylibrary AS 
                SELECT * FROM MyLibrary ORDER BY id
            """)

            # Ana tabloyu sil
            cursor.execute("DROP TABLE MyLibrary")

            # Yeni tablo oluştur
            cursor.execute("""
                CREATE TABLE MyLibrary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT UNIQUE,
                    title TEXT,
                    author TEXT,
                    publisher TEXT,
                    category TEXT,
                    reading_status TEXT,
                    purchase_date TEXT,
                    price REAL,
                    page_count INTEGER,
                    rating INTEGER,
                    favorite TEXT,
                    tags TEXT,
                    cover_url TEXT,
                    average_rating REAL
                )
            """)

            # Verileri yeni tabloya aktar
            cursor.execute("""
                INSERT INTO MyLibrary (
                    isbn, title, author, publisher, category,
                    reading_status, purchase_date, price, page_count,
                    rating, favorite, tags, cover_url, average_rating
                )
                SELECT 
                    isbn, title, author, publisher, category,
                    reading_status, purchase_date, price, page_count,
                    rating, favorite, tags, cover_url, average_rating
                FROM temp_mylibrary
            """)

            # Geçici tabloyu sil
            cursor.execute("DROP TABLE temp_mylibrary")

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Database IDs reset!")
            self.list_all_books()  # Tabloyu güncelle

        except Exception as e:
            messagebox.showerror("Error", f"ID reset error: {str(e)}")


if __name__ == "__main__":
    root = ttk.Window("Library Management System", "cosmo")
    app = KitaplikUygulamasi(root)
    app.setup_menu()
    root.mainloop()