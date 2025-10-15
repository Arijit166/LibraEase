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
        self.db = main_app.db
        
        # Data files and directories
        self.books_file = os.path.join("admin", "books.json")
        self.images_dir = os.path.join("admin", "book_images")
        
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
        
        # Track active nav button
        self.active_nav_button = None
        
        self.show_admin_dashboard()
    
    def init_admin_data(self):
        pass
    
    def show_admin_dashboard(self):
        self.main_app.clear_window()
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # Create background canvas
        bg_canvas = tk.Canvas(main_container, highlightthickness=0, bd=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        def update_bg(event=None):
            # Update rectangle size when window is resized
            width = main_container.winfo_width()
            height = main_container.winfo_height()
            bg_canvas.delete("bg")  # Remove old background
            bg_canvas.create_rectangle(0, 0, width, height, fill=self.APP_BG, outline=self.APP_BG, tags="bg")
        
        # Bind to resize events
        main_container.bind("<Configure>", update_bg)
        # Initial draw
        update_bg()
        
        # Content container that will hold all the UI elements
        content_container = tk.Frame(main_container, bg=self.APP_BG)
        content_container.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create navbar
        self.create_navbar(content_container)
        
        # Content area
        self.content_frame = tk.Frame(content_container, bg=self.APP_BG)
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
        
        # Gradient-style title with icon
        title_container = tk.Frame(left_frame, bg=self.NAVBAR_BG)
        title_container.pack(side="left")
        
        tk.Label(
            title_container,
            text="◆",
            font=("Helvetica", 24, "bold"),
            fg=self.ACCENT_GREEN,
            bg=self.NAVBAR_BG
        ).pack(side="left", padx=(0, 8))
        
        tk.Label(
            title_container,
            text="Admin",
            font=("Helvetica", 18, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.NAVBAR_BG
        ).pack(side="left")
        
        tk.Label(
            title_container,
            text="Portal",
            font=("Helvetica", 18),
            fg=self.TEXT_FG,
            bg=self.NAVBAR_BG
        ).pack(side="left", padx=(5, 0))
        
        # Center - Navigation buttons with modern design
        nav_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        nav_frame.pack(side="left", expand=True, padx=60)
        
        nav_items = [
            ("▦", "Library", self.show_book_management),
            ("◉", "Members", self.show_member_management),
            ("⇄", "Issue/Return", self.show_issue_return),
            ("▣", "Analytics", self.show_reports)
        ]
        
        self.nav_buttons = []
        
        for icon, text, command in nav_items:
            # Modern button container with subtle border
            btn_container = tk.Frame(
                nav_frame, 
                bg=self.NAVBAR_BG,
                highlightthickness=0
            )
            btn_container.pack(side="left", padx=3)
            
            # Inner frame for gradient-like effect
            btn_inner = tk.Frame(btn_container, bg=self.NAVBAR_BG)
            btn_inner.pack(padx=1, pady=1)
            
            btn = tk.Button(
                btn_inner,
                text=f" {icon} ",
                font=("Segoe UI", 16),
                bg=self.NAVBAR_BG,
                fg="#64748b",
                relief="flat",
                bd=0,
                padx=8,
                pady=6,
                cursor="hand2",
                activebackground="#334155",
                activeforeground="white"
            )
            btn.pack(side="left")
            
            # Text label below icon
            text_label = tk.Label(
                btn_inner,
                text=text,
                font=("Segoe UI", 9, "bold"),
                bg=self.NAVBAR_BG,
                fg="#64748b"
            )
            text_label.pack(side="left", padx=(2, 8))
            
            # Store both button and label for styling
            btn.text_label = text_label
            btn.inner_frame = btn_inner
            btn.container = btn_container
            
            # Update command to include button reference
            btn.config(command=lambda c=command, b=btn: self.set_active_nav(b, c))
            text_label.bind("<Button-1>", lambda e, c=command, b=btn: self.set_active_nav(b, c))
            
            # Modern hover effects
            def on_enter(e, button=btn):
                if button != self.active_nav_button:
                    button.config(fg="#94a3b8")
                    button.text_label.config(fg="#94a3b8")
                    button.inner_frame.config(bg="#253145")
            
            def on_leave(e, button=btn):
                if button != self.active_nav_button:
                    button.config(fg="#64748b")
                    button.text_label.config(fg="#64748b")
                    button.inner_frame.config(bg=self.NAVBAR_BG)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)
            
            self.nav_buttons.append(btn)
        
        # Set Library (Books) as default active
        self.set_active_nav(self.nav_buttons[0], self.show_book_management, initial=True)
        
        # Right side - User info and logout with modern styling
        right_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        right_frame.pack(side="right", padx=30)
        
        # User profile section
        user_container = tk.Frame(right_frame, bg="#253145", highlightthickness=1, highlightbackground="#334155")
        user_container.pack(side="left", padx=(0, 15))
        
        user_name = self.current_user.get("first_name", "Admin")
        tk.Label(
            user_container,
            text="●",
            font=("Helvetica", 10),
            fg=self.ACCENT_GREEN,
            bg="#253145"
        ).pack(side="left", padx=(12, 5))
        
        tk.Label(
            user_container,
            text=user_name,
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_FG,
            bg="#253145"
        ).pack(side="left", padx=(0, 12), pady=8)
        
        # Modern logout button
        logout_container = tk.Frame(right_frame, bg=self.NAVBAR_BG)
        logout_container.pack(side="left")
        
        logout_btn = tk.Button(
            logout_container,
            text="⏻  Logout",
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=8,
            activebackground="#dc2626",
            command=self.logout
        )
        logout_btn.pack()
        
        # Logout hover effects
        def logout_enter(e):
            logout_btn.config(bg="#dc2626")
            logout_container.config(bg="#dc2626")
        
        def logout_leave(e):
            logout_btn.config(bg="#ef4444")
            logout_container.config(bg=self.NAVBAR_BG)
        
        logout_btn.bind("<Enter>", logout_enter)
        logout_btn.bind("<Leave>", logout_leave)

    def set_active_nav(self, button, command, initial=False):
        # Reset previous active button
        if self.active_nav_button and self.active_nav_button != button:
            self.active_nav_button.config(
                fg="#64748b",
                relief="flat"
            )
            self.active_nav_button.text_label.config(fg="#64748b")
            self.active_nav_button.inner_frame.config(bg=self.NAVBAR_BG)
            self.active_nav_button.container.config(highlightthickness=0)
        
        # Set new active button with gradient-like effect
        self.active_nav_button = button
        button.config(
            fg=self.ACCENT_GREEN,
            relief="flat"
        )
        button.text_label.config(fg=self.ACCENT_GREEN)
        button.inner_frame.config(bg="#1a2332")
        button.container.config(
            highlightthickness=2,
            highlightbackground=self.ACCENT_GREEN,
            bg="#1a2332"
        )
        
        # Execute command only if not initial setup
        if not initial:
            command()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
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
        
        # Center the title
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="📖 Book Management",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
        # Add Book Button - positioned absolutely on the right
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
        add_btn.place(relx=1.0, rely=0.5, anchor="e")
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
            fg="#64748b",  # lighter color for placeholder
            insertbackground=self.TEXT_FG
        )
        search_entry.insert(0, "Search by name or author...")

        # Remove placeholder on focus
        def on_focus_in(event):
            if search_entry.get() == "Search by name or author...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=self.TEXT_FG)

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Search by name or author...")
                search_entry.config(fg="#64748b")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        search_entry.pack(fill="x", padx=15, pady=10)

        
        # Books Grid Container with Scrollbar
        canvas_frame = tk.Frame(self.content_frame, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=(40, 20), pady=(0, 20))
        
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
        
       # Before the mousewheel binding
        self.main_canvas = canvas  # Store reference

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
        
        # Load books using database manager
        if search_query:
            books_df = self.db.search_books(search_query)
        else:
            books_df = self.db.get_all_books()
        
        if len(books_df) == 0:
            tk.Label(
                self.books_container,
                text="📚 No books found. Add your first book!",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG
            ).pack(pady=50)
            return
        
        # Convert DataFrame to list of dicts for compatibility
        books = books_df.to_dict('records')
        
        # Display books in grid (3 columns)
        row_frame = None
        for idx, book in enumerate(books):
            if idx % 3 == 0:
                row_frame = tk.Frame(self.books_container, bg=self.APP_BG)
                row_frame.pack(fill="x", pady=10, padx=10)  # Added padx
            
            self.create_book_card(row_frame, book)

    def create_book_card(self, parent, book):
        card = tk.Frame(parent, bg=self.CARD_BG, bd=0, width=230, height=450)
        card.pack(side="left", padx=10, pady=10)
        card.pack_propagate(False)
        
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
        if search_query == "Search by name or author...":
            search_query = ""
        self.display_books(search_query)
    
    def show_add_book_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("500x700")  # Changed from 600 to 700
        dialog.configure(bg=self.CARD_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)  # Changed from 600 to 700
        dialog.geometry(f"500x700+{x}+{y}")
        
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
        # Book ID 
        tk.Label(
            form_frame,
            text="🔢 Book ID (Unique)",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w", pady=(15, 5))

        id_frame = tk.Frame(form_frame, bg=self.INPUT_BG, highlightthickness=1, highlightbackground="#475569")
        id_frame.pack(fill="x")
        id_entry = tk.Entry(id_frame, font=("Helvetica", 12), relief="flat", bd=0, bg=self.INPUT_BG, fg=self.TEXT_FG, insertbackground=self.TEXT_FG)
        id_entry.pack(fill="x", padx=15, pady=12)
                
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
            book_id = id_entry.get().strip()
            
            if not name or not author or not book_id:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            # Validate ID is numeric
            try:
                book_id = int(book_id)
            except ValueError:
                messagebox.showerror("Error", "Book ID must be a number!")
                return
            
            # Check if ID already exists
            if self.db.get_book_by_id(book_id) is not None:
                messagebox.showerror("Error", f"Book ID {book_id} already exists! Please use a unique ID.")
                return
            
            # Save image if provided
            saved_image_path = None
            if image_path["path"]:
                try:
                    ext = os.path.splitext(image_path["path"])[1]
                    new_filename = f"book_{book_id}{ext}"
                    saved_image_path = os.path.join(str(self.images_dir), new_filename)
                    shutil.copy2(image_path["path"], saved_image_path)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not save image: {e}")
            
            # Create book with specific ID
            # You'll need to modify create_book to accept an id parameter
            self.db.create_book_with_id(book_id, name, author, saved_image_path)
            
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
            # Delete book and get image path
            image_path = self.db.delete_book(book['id'])
            
            # Delete image file if exists
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass
            
            # Refresh the book display without showing messagebox first
            self.show_book_management()
            
            # Show success message after refresh
            self.root.after(100, lambda: messagebox.showinfo("Success", "Book deleted successfully!"))

    def update_book(self, book, name_entry, author_entry, image_path, dialog):
        name = name_entry.get().strip()
        author = author_entry.get().strip()
        
        if not name or not author:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Handle image update
        saved_image_path = None
        if image_path["path"] != book.get('image_path'):
            if image_path["path"]:
                try:
                    ext = os.path.splitext(image_path["path"])[1]
                    new_filename = f"book_{book['id']}{ext}"
                    saved_image_path = os.path.join(str(self.images_dir), new_filename)
                    shutil.copy2(image_path["path"], saved_image_path)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not save image: {e}")
                    saved_image_path = book.get('image_path')
        
        # Update book using database manager
        self.db.update_book(
            book['id'],
            name=name,
            author=author,
            image_path=saved_image_path if saved_image_path else book.get('image_path')
        )
        
        messagebox.showinfo("Success", "Book updated successfully!")
        dialog.destroy()
        self.show_book_management()
    
    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.main_app.current_user = None
            self.main_app.show_welcome_screen()