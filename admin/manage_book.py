import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import shutil

class AdminDashboard:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.current_user = main_app.current_user
        
        # Data files
        self.books_file = "admin/books.json"
        self.images_dir = "admin/book_images"
        
        # Initialize admin folder and files
        self.init_admin_data()
        
        # Colors matching the UI
        self.APP_BG = "#0f172a"
        self.NAVBAR_BG = "#1e293b"
        self.CARD_BG = "#1e293b"
        self.INPUT_BG = "#334155"
        self.TEXT_FG = "#e5e7eb"
        self.ACCENT_GREEN = "#43e97b"
        self.ACCENT_PURPLE = "#667eea"
        
        self.show_admin_dashboard()
    
    def init_admin_data(self):
        # Create admin folder if not exists
        os.makedirs("admin", exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Initialize books file
        if not os.path.exists(self.books_file):
            with open(self.books_file, 'w') as f:
                json.dump([], f)
    
    def show_admin_dashboard(self):
        self.main_app.clear_window()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.APP_BG)
        main_container.pack(fill="both", expand=True)
        
        # Create navbar
        self.create_navbar(main_container)
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=self.APP_BG)
        self.content_frame.pack(fill="both", expand=True)
        
        # Show Book Management by default
        self.show_book_management()
    
    def create_navbar(self, parent):
        navbar = tk.Frame(parent, bg=self.NAVBAR_BG, height=80)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        left_frame.pack(side="left", padx=30, pady=15)
        
        tk.Label(
            left_frame,
            text="📚 Admin Dashboard",
            font=("Helvetica", 20, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.NAVBAR_BG
        ).pack(side="left")
        
        # Center - Navigation buttons
        nav_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        nav_frame.pack(side="left", expand=True, padx=50)
        
        nav_items = [
            ("🏠 Home", self.show_home),
            ("📖 Books", self.show_book_management),
            ("👥 Members", self.show_member_management),
            ("🔄 Issue/Return", self.show_issue_return),
            ("📊 Reports", self.show_reports)
        ]
        
        for text, command in nav_items:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("Helvetica", 11, "bold"),
                bg=self.NAVBAR_BG,
                fg=self.TEXT_FG,
                relief="flat",
                bd=0,
                cursor="hand2",
                activebackground="#334155",
                command=command
            )
            btn.pack(side="left", padx=8)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#334155"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.NAVBAR_BG))
        
        # Right side - User info and logout
        right_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        right_frame.pack(side="right", padx=30)
        
        user_name = self.current_user.get("first_name", "Admin")
        tk.Label(
            right_frame,
            text=f"👤 {user_name}",
            font=("Helvetica", 11),
            fg="#94a3b8",
            bg=self.NAVBAR_BG
        ).pack(side="left", padx=10)
        
        logout_btn = tk.Button(
            right_frame,
            text="🚪 Logout",
            font=("Helvetica", 11, "bold"),
            bg="#ef4444",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#dc2626",
            command=self.logout
        )
        logout_btn.pack(side="left", padx=5)
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#dc2626"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#ef4444"))
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🏠 Home - Coming Soon",
            font=("Helvetica", 24, "bold"),
            fg=self.TEXT_FG,
            bg=self.APP_BG
        ).pack(expand=True)
    
    def show_member_management(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="👥 Member Management - Coming Soon",
            font=("Helvetica", 24, "bold"),
            fg=self.TEXT_FG,
            bg=self.APP_BG
        ).pack(expand=True)
    
    def show_issue_return(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🔄 Issue/Return Management - Coming Soon",
            font=("Helvetica", 24, "bold"),
            fg=self.TEXT_FG,
            bg=self.APP_BG
        ).pack(expand=True)
    
    def show_reports(self):
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="📊 Reports & Analysis - Coming Soon",
            font=("Helvetica", 24, "bold"),
            fg=self.TEXT_FG,
            bg=self.APP_BG
        ).pack(expand=True)
    
    def show_book_management(self):
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        tk.Label(
            header_frame,
            text="📖 Book Management",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack(side="left")
        
        # Add Book Button
        add_btn = tk.Button(
            header_frame,
            text="➕ Add New Book",
            font=("Helvetica", 12, "bold"),
            bg=self.ACCENT_GREEN,
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#38d46a",
            command=self.show_add_book_dialog
        )
        add_btn.pack(side="right", ipadx=15, ipady=8)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#38d46a"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=self.ACCENT_GREEN))
        
        # Search Bar
        search_frame = tk.Frame(self.content_frame, bg=self.APP_BG)
        search_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.APP_BG
        ).pack(side="left", padx=(0, 10))
        
        search_entry_frame = tk.Frame(search_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        search_entry_frame.pack(side="left", fill="x", expand=True)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_books())
        
        search_entry = tk.Entry(
            search_entry_frame,
            textvariable=self.search_var,
            font=("Helvetica", 12),
            relief="flat",
            bd=0,
            bg=self.INPUT_BG,
            fg=self.TEXT_FG,
            insertbackground=self.TEXT_FG
        )
        search_entry.pack(fill="x", padx=15, pady=10)
        
        # Books Grid Container with Scrollbar
        canvas_frame = tk.Frame(self.content_frame, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.books_container = tk.Frame(canvas, bg=self.APP_BG)
        
        self.books_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.books_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Style scrollbar
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            background="#334155",
            troughcolor="#1e293b",
            bordercolor="#1e293b",
            arrowcolor="#94a3b8"
        )
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Load and display books
        self.display_books()
    
    def display_books(self, search_query=""):
        # Clear existing books
        for widget in self.books_container.winfo_children():
            widget.destroy()
        
        # Load books
        try:
            with open(self.books_file, 'r') as f:
                books = json.load(f)
        except:
            books = []
        
        # Filter books based on search
        if search_query:
            query = search_query.lower()
            books = [b for b in books if query in b['name'].lower() or query in b['author'].lower()]
        
        if not books:
            tk.Label(
                self.books_container,
                text="📚 No books found. Add your first book!",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG
            ).pack(pady=50)
            return
        
        # Display books in grid (3 columns)
        row_frame = None
        for idx, book in enumerate(books):
            if idx % 3 == 0:
                row_frame = tk.Frame(self.books_container, bg=self.APP_BG)
                row_frame.pack(fill="x", pady=10)
            
            self.create_book_card(row_frame, book)
    
    def create_book_card(self, parent, book):
        # Card container
        card = tk.Frame(parent, bg=self.CARD_BG, bd=0)
        card.pack(side="left", padx=10, pady=10)
        
        # Shadow effect
        shadow = tk.Frame(parent, bg="#0b1020")
        shadow.place(in_=card, x=3, y=3, relwidth=1, relheight=1)
        shadow.lower()
        card.lift()
        
        # Image
        img_frame = tk.Frame(card, bg="#334155", width=200, height=250)
        img_frame.pack(padx=15, pady=15)
        img_frame.pack_propagate(False)
        
        try:
            if book.get('image_path') and os.path.exists(book['image_path']):
                img = Image.open(book['image_path'])
                img = img.resize((180, 230), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(img_frame, image=photo, bg="#334155")
                img_label.image = photo  # Keep reference
                img_label.pack(expand=True)
            else:
                tk.Label(
                    img_frame,
                    text="📚\nNo Image",
                    font=("Helvetica", 16),
                    fg="#64748b",
                    bg="#334155"
                ).pack(expand=True)
        except:
            tk.Label(
                img_frame,
                text="📚\nNo Image",
                font=("Helvetica", 16),
                fg="#64748b",
                bg="#334155"
            ).pack(expand=True)
        
        # Book details
        details_frame = tk.Frame(card, bg=self.CARD_BG)
        details_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Label(
            details_frame,
            text=book['name'][:20] + "..." if len(book['name']) > 20 else book['name'],
            font=("Helvetica", 14, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w")
        
        tk.Label(
            details_frame,
            text=f"by {book['author'][:18]}..." if len(book['author']) > 18 else f"by {book['author']}",
            font=("Helvetica", 11),
            fg="#94a3b8",
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(2, 0))
        
        # Action buttons
        btn_frame = tk.Frame(card, bg=self.CARD_BG)
        btn_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        edit_btn = tk.Button(
            btn_frame,
            text="✏️ Edit",
            font=("Helvetica", 10, "bold"),
            bg=self.ACCENT_PURPLE,
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#5568d3",
            command=lambda b=book: self.edit_book(b)
        )
        edit_btn.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)
        edit_btn.bind("<Enter>", lambda e, b=edit_btn: b.config(bg="#5568d3"))
        edit_btn.bind("<Leave>", lambda e, b=edit_btn: b.config(bg=self.ACCENT_PURPLE))
        
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Delete",
            font=("Helvetica", 10, "bold"),
            bg="#ef4444",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#dc2626",
            command=lambda b=book: self.delete_book(b)
        )
        delete_btn.pack(side="left", fill="x", expand=True, padx=(5, 0), ipady=5)
        delete_btn.bind("<Enter>", lambda e, b=delete_btn: b.config(bg="#dc2626"))
        delete_btn.bind("<Leave>", lambda e, b=delete_btn: b.config(bg="#ef4444"))
    
    def filter_books(self):
        search_query = self.search_var.get()
        self.display_books(search_query)
    
    def show_add_book_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("500x600")
        dialog.configure(bg=self.CARD_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Header
        tk.Label(
            dialog,
            text="➕ Add New Book",
            font=("Helvetica", 22, "bold"),
            fg=self.ACCENT_GREEN,
            bg=self.CARD_BG
        ).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg=self.CARD_BG)
        form_frame.pack(fill="both", expand=True, padx=40)
        
        # Book Name
        tk.Label(
            form_frame,
            text="📖 Book Name",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(10, 5))
        
        name_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        name_frame.pack(fill="x")
        name_entry = tk.Entry(name_frame, font=("Helvetica", 12), relief="flat", bd=0, bg=self.INPUT_BG, fg=self.TEXT_FG, insertbackground=self.TEXT_FG)
        name_entry.pack(fill="x", padx=15, pady=12)
        
        # Author
        tk.Label(
            form_frame,
            text="✍️ Author",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(15, 5))
        
        author_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        author_frame.pack(fill="x")
        author_entry = tk.Entry(author_frame, font=("Helvetica", 12), relief="flat", bd=0, bg=self.INPUT_BG, fg=self.TEXT_FG, insertbackground=self.TEXT_FG)
        author_entry.pack(fill="x", padx=15, pady=12)
        
        # Image
        tk.Label(
            form_frame,
            text="🖼️ Book Cover Image",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(15, 5))
        
        image_path = {"path": None}
        
        def select_image():
            filename = filedialog.askopenfilename(
                title="Select Book Cover",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if filename:
                image_path["path"] = filename
                img_label.config(text=f"✅ {os.path.basename(filename)}", fg=self.ACCENT_GREEN)
        
        img_btn_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        img_btn_frame.pack(fill="x")
        
        img_btn = tk.Button(
            img_btn_frame,
            text="📁 Choose Image",
            font=("Helvetica", 11, "bold"),
            bg="#475569",
            fg=self.TEXT_FG,
            relief="flat",
            cursor="hand2",
            command=select_image
        )
        img_btn.pack(pady=10, padx=15)
        
        img_label = tk.Label(
            form_frame,
            text="No image selected",
            font=("Helvetica", 10),
            fg="#64748b",
            bg=self.CARD_BG
        )
        img_label.pack(pady=5)
        
        # Add Button
        def add_book():
            name = name_entry.get().strip()
            author = author_entry.get().strip()
            
            if not name or not author:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            # Load existing books
            try:
                with open(self.books_file, 'r') as f:
                    books = json.load(f)
            except:
                books = []
            
            # Save image if provided
            saved_image_path = None
            if image_path["path"]:
                try:
                    ext = os.path.splitext(image_path["path"])[1]
                    new_filename = f"book_{len(books) + 1}{ext}"
                    saved_image_path = os.path.join(self.images_dir, new_filename)
                    shutil.copy2(image_path["path"], saved_image_path)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not save image: {e}")
            
            # Add new book
            books.append({
                "id": len(books) + 1,
                "name": name,
                "author": author,
                "image_path": saved_image_path
            })
            
            # Save to file
            with open(self.books_file, 'w') as f:
                json.dump(books, f, indent=4)
            
            messagebox.showinfo("Success", "Book added successfully!")
            dialog.destroy()
            self.show_book_management()
        
        add_book_btn = tk.Button(
            form_frame,
            text="➕ Add Book",
            font=("Helvetica", 14, "bold"),
            bg=self.ACCENT_GREEN,
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#38d46a",
            command=add_book
        )
        add_book_btn.pack(pady=30, ipadx=40, ipady=10)
        add_book_btn.bind("<Enter>", lambda e: add_book_btn.config(bg="#38d46a"))
        add_book_btn.bind("<Leave>", lambda e: add_book_btn.config(bg=self.ACCENT_GREEN))
    
    def edit_book(self, book):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Book")
        dialog.geometry("500x600")
        dialog.configure(bg=self.CARD_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Header
        tk.Label(
            dialog,
            text="✏️ Edit Book",
            font=("Helvetica", 22, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.CARD_BG
        ).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg=self.CARD_BG)
        form_frame.pack(fill="both", expand=True, padx=40)
        
        # Book Name
        tk.Label(
            form_frame,
            text="📖 Book Name",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(10, 5))
        
        name_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        name_frame.pack(fill="x")
        name_entry = tk.Entry(name_frame, font=("Helvetica", 12), relief="flat", bd=0, bg=self.INPUT_BG, fg=self.TEXT_FG, insertbackground=self.TEXT_FG)
        name_entry.insert(0, book['name'])
        name_entry.pack(fill="x", padx=15, pady=12)
        
        # Author
        tk.Label(
            form_frame,
            text="✍️ Author",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(15, 5))
        
        author_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        author_frame.pack(fill="x")
        author_entry = tk.Entry(author_frame, font=("Helvetica", 12), relief="flat", bd=0, bg=self.INPUT_BG, fg=self.TEXT_FG, insertbackground=self.TEXT_FG)
        author_entry.insert(0, book['author'])
        author_entry.pack(fill="x", padx=15, pady=12)
        
        # Image
        tk.Label(
            form_frame,
            text="🖼️ Book Cover Image",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(15, 5))
        
        image_path = {"path": book.get('image_path')}
        
        def select_image():
            filename = filedialog.askopenfilename(
                title="Select Book Cover",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            if filename:
                image_path["path"] = filename
                img_label.config(text=f"✅ {os.path.basename(filename)}", fg=self.ACCENT_GREEN)
        
        img_btn_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        img_btn_frame.pack(fill="x")
        
        img_btn = tk.Button(
            img_btn_frame,
            text="📁 Change Image",
            font=("Helvetica", 11, "bold"),
            bg="#475569",
            fg=self.TEXT_FG,
            relief="flat",
            cursor="hand2",
            command=select_image
        )
        img_btn.pack(pady=10, padx=15)
        
        current_img = os.path.basename(book.get('image_path', '')) if book.get('image_path') else "No image"
        img_label = tk.Label(
            form_frame,
            text=current_img,
            font=("Helvetica", 10),
            fg="#64748b",
            bg=self.CARD_BG
        )
        img_label.pack(pady=5)
        
        # Update Button
        update_btn = tk.Button(
            form_frame,
            text="✔️ Update Book",
            font=("Helvetica", 14, "bold"),
            bg=self.ACCENT_PURPLE,
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#5568d3",
            command=lambda: self.update_book(book, name_entry, author_entry, image_path, dialog)
        )
        update_btn.pack(pady=30, ipadx=40, ipady=10)
        update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#5568d3"))
        update_btn.bind("<Leave>", lambda e: update_btn.config(bg=self.ACCENT_PURPLE))
        
    def delete_book(self, book):
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{book['name']}'?\n\nThis action cannot be undone."
        )
        
        if result:
            # Load books
            try:
                with open(self.books_file, 'r') as f:
                    books = json.load(f)
            except:
                books = []
            
            # Remove book
            books = [b for b in books if b['id'] != book['id']]
            
            # Delete image if exists
            if book.get('image_path') and os.path.exists(book['image_path']):
                try:
                    os.remove(book['image_path'])
                except:
                    pass
            
            # Save to file
            with open(self.books_file, 'w') as f:
                json.dump(books, f, indent=4)
            
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.show_book_management()

    def update_book(self, book, name_entry, author_entry, image_path, dialog):
        name = name_entry.get().strip()
        author = author_entry.get().strip()
        
        if not name or not author:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Load books
        try:
            with open(self.books_file, 'r') as f:
                books = json.load(f)
        except:
            books = []
        
        # Find and update book
        for b in books:
            if b['id'] == book['id']:
                b['name'] = name
                b['author'] = author
                
                # Update image if changed
                if image_path["path"] != book.get('image_path'):
                    if image_path["path"]:
                        try:
                            ext = os.path.splitext(image_path["path"])[1]
                            new_filename = f"book_{book['id']}{ext}"
                            saved_image_path = os.path.join(self.images_dir, new_filename)
                            shutil.copy2(image_path["path"], saved_image_path)
                            b['image_path'] = saved_image_path
                        except Exception as e:
                            messagebox.showwarning("Warning", f"Could not save image: {e}")
                break
        
        # Save to file
        with open(self.books_file, 'w') as f:
            json.dump(books, f, indent=4)
        
        messagebox.showinfo("Success", "Book updated successfully!")
        dialog.destroy()
        self.show_book_management()
    
    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.main_app.current_user = None
            self.main_app.show_welcome_screen()