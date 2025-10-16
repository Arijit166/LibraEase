import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from user.cart import UserCartPage
from user.borrowing import UserBorrowingPage
import os

class UserBooksPage:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.current_user = main_app.current_user
        self.db = main_app.db
        
        # Colors matching the admin UI
        self.APP_BG = "#0f172a"
        self.NAVBAR_BG = "#1e293b"
        self.CARD_BG = "#1e293b"
        self.INPUT_BG = "#334155"
        self.TEXT_FG = "#e5e7eb"
        self.ACCENT_GREEN = "#43e97b"
        self.ACCENT_PURPLE = "#667eea"
        
        # Track active nav button
        self.active_nav_button = None
        
        self.show_user_dashboard()
    
    def show_user_dashboard(self):
        self.main_app.clear_window()
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # Create background canvas
        bg_canvas = tk.Canvas(main_container, highlightthickness=0, bd=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        def update_bg(event=None):
            width = main_container.winfo_width()
            height = main_container.winfo_height()
            bg_canvas.delete("bg")
            bg_canvas.create_rectangle(0, 0, width, height, fill=self.APP_BG, outline=self.APP_BG, tags="bg")
        
        main_container.bind("<Configure>", update_bg)
        update_bg()
        
        # Content container
        content_container = tk.Frame(main_container, bg=self.APP_BG)
        content_container.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create navbar
        self.create_navbar(content_container)
        
        # Content area
        self.content_frame = tk.Frame(content_container, bg=self.APP_BG)
        self.content_frame.pack(fill="both", expand=True)
        
        # Show Books by default
        self.show_books()
    
    def create_navbar(self, parent):
        navbar = tk.Frame(parent, bg=self.NAVBAR_BG, height=80)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        left_frame.pack(side="left", padx=30, pady=15)
        
        title_container = tk.Frame(left_frame, bg=self.NAVBAR_BG)
        title_container.pack(side="left", pady=(5, 0))  

        # Title container
        title_inner = tk.Frame(title_container, bg=self.NAVBAR_BG)
        title_inner.pack(side="left", anchor="center")

        # Emoji logo — bigger and slightly raised
        tk.Label(
            title_inner,
            text="📚",
            font=("Helvetica", 32), 
            fg=self.ACCENT_GREEN,
            bg=self.NAVBAR_BG
        ).pack(side="left", padx=(0, 10), pady=(0, 4))  

        # LibraEase title — larger font
        tk.Label(
            title_inner,
            text="Libra",
            font=("Helvetica", 24, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.NAVBAR_BG
        ).pack(side="left")

        tk.Label(
            title_inner,
            text="Ease",
            font=("Helvetica", 24, "bold"),
            fg=self.ACCENT_GREEN,
            bg=self.NAVBAR_BG
        ).pack(side="left")
        
        # Center - Navigation buttons
        nav_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        nav_frame.pack(side="left", expand=True, padx=60)
        
        nav_items = [
            ("📙", "Books", self.show_books),
            ("🛒", "Cart", self.show_cart),
            ("📖", "Borrowed", self.show_borrowed)
        ]
        
        self.nav_buttons = []
        
        for icon, text, command in nav_items:
            btn_container = tk.Frame(
                nav_frame, 
                bg=self.NAVBAR_BG,
                highlightthickness=0
            )
            btn_container.pack(side="left", padx=3)
            
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
            
            text_label = tk.Label(
                btn_inner,
                text=text,
                font=("Segoe UI", 9, "bold"),
                bg=self.NAVBAR_BG,
                fg="#64748b"
            )
            text_label.pack(side="left", padx=(2, 8))
            
            btn.text_label = text_label
            btn.inner_frame = btn_inner
            btn.container = btn_container
            
            btn.config(command=lambda c=command, b=btn: self.set_active_nav(b, c))
            text_label.bind("<Button-1>", lambda e, c=command, b=btn: self.set_active_nav(b, c))
            
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
        
        # Set Books as default active
        self.set_active_nav(self.nav_buttons[0], self.show_books, initial=True)
        
        # Right side - User info and logout
        right_frame = tk.Frame(navbar, bg=self.NAVBAR_BG)
        right_frame.pack(side="right", padx=30)
        
        user_container = tk.Frame(right_frame, bg="#253145", highlightthickness=1, highlightbackground="#334155")
        user_container.pack(side="left", padx=(0, 15))
        
        user_name = self.current_user.get("first_name", "User")
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
        
        def logout_enter(e):
            logout_btn.config(bg="#dc2626")
        
        def logout_leave(e):
            logout_btn.config(bg="#ef4444")
        
        logout_btn.bind("<Enter>", logout_enter)
        logout_btn.bind("<Leave>", logout_leave)
    
    def set_active_nav(self, button, command, initial=False):
        if self.active_nav_button and self.active_nav_button != button:
            self.active_nav_button.config(fg="#64748b", relief="flat")
            self.active_nav_button.text_label.config(fg="#64748b")
            self.active_nav_button.inner_frame.config(bg=self.NAVBAR_BG)
            self.active_nav_button.container.config(highlightthickness=0)
        
        self.active_nav_button = button
        button.config(fg=self.ACCENT_GREEN, relief="flat")
        button.text_label.config(fg=self.ACCENT_GREEN)
        button.inner_frame.config(bg="#1a2332")
        button.container.config(
            highlightthickness=2,
            highlightbackground=self.ACCENT_GREEN,
            bg="#1a2332"
        )
        
        if not initial:
            command()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_cart(self):
        self.clear_content()
        UserCartPage(self.content_frame, self.main_app)
    
    def show_borrowed(self):
        self.clear_content()
        UserBorrowingPage(self.content_frame, self.main_app)
    
    def show_books(self):
        self.clear_content()
        
        # Header with title centered
        header_frame = tk.Frame(self.content_frame, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="📙 Available Books",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
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
            fg="#64748b",
            insertbackground=self.TEXT_FG
        )
        search_entry.insert(0, "Search by name or author...")
        
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
        
        # Books Grid with Scrollbar
        canvas_frame = tk.Frame(self.content_frame, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=(40, 20), pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.books_container = tk.Frame(canvas, bg=self.APP_BG)
        
        self.books_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        self._books_window_id = canvas.create_window((0, 0), window=self.books_container, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfigure(self._books_window_id, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Style scrollbar
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            background="#475569",
            troughcolor="#1e293b",
            bordercolor="#1e293b",
            arrowcolor="#cbd5e1",
            darkcolor="#334155",
            lightcolor="#64748b"
        )
        style.map(
            "Vertical.TScrollbar",
            background=[("active", "#64748b"), ("disabled", "#334155")]
        )
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Load and display books
        self.display_books()
    
    def display_books(self, search_query=""):
        for widget in self.books_container.winfo_children():
            widget.destroy()
        
        if search_query:
            books_df = self.db.search_books(search_query)
        else:
            books_df = self.db.get_all_books()
        
        if len(books_df) == 0:
            tk.Label(
                self.books_container,
                text=" No books available at the moment.",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG
            ).grid(pady=50)
            return
        
        books = books_df.to_dict('records')
        
        # 4-column grid
        cols = 4
        for c in range(cols):
            self.books_container.grid_columnconfigure(c, weight=1, uniform="bookcol")
        
        for idx, book in enumerate(books):
            r = idx // cols
            c = idx % cols
            cell = tk.Frame(self.books_container, bg=self.APP_BG)
            cell.grid(row=r, column=c, padx=20, pady=20, sticky="nsew")
            self.create_book_card(cell, book)
    
    def create_book_card(self, parent, book):
        # Container with fixed height
        card_container = tk.Frame(parent, bg=self.APP_BG, height=450)
        card_container.pack(fill="both", expand=True)
        card_container.pack_propagate(False)
        
        # Use a Canvas to draw a rounded rectangle for the card
        card_canvas = tk.Canvas(card_container, bg=self.APP_BG, highlightthickness=0)
        card_canvas.pack(fill="both", expand=True)

        # Store references to avoid garbage collection
        card_canvas.images = []
        
        def redraw_card(event=None):
            canvas = card_canvas
            width = canvas.winfo_width()
            height = 450  # Fixed height
            canvas.delete("all")

            # Draw the rounded card background
            card_id = self.round_rectangle(canvas, 5, 5, width - 10, height - 5, radius=20, fill=self.CARD_BG, outline="#334155")

            # Add hover effect
            def on_hover_enter(e):
                canvas.itemconfig(card_id, outline=self.ACCENT_PURPLE, width=2)
            
            def on_hover_leave(e):
                canvas.itemconfig(card_id, outline="#334155", width=1)
            
            canvas.bind("<Enter>", on_hover_enter)
            canvas.bind("<Leave>", on_hover_leave)

            # --- Image ---
            img_y_pos = 135
            try:
                if book.get('image_path') and os.path.exists(book['image_path']):
                    img = Image.open(book['image_path'])
                    # Fixed size for image
                    img = img.resize((220, 230), Image.Resampling.LANCZOS)
                    
                    photo = ImageTk.PhotoImage(img)
                    canvas.images.append(photo)  # Keep reference
                    canvas.create_image(width / 2, img_y_pos, image=photo)
                else:
                    canvas.create_text(width / 2, img_y_pos, text="📚\nNo Image", font=("Helvetica", 16), fill="#64748b", justify="center")
            except Exception:
                canvas.create_text(width / 2, img_y_pos, text="📚\nNo Image", font=("Helvetica", 16), fill="#64748b", justify="center")

            # --- Book Details ---
            title_text = book['name'][:20] + "..." if len(book['name']) > 20 else book['name']
            author_text = f"by {book['author'][:18]}..." if len(book['author']) > 18 else f"by {book['author']}"
            
            canvas.create_text(20, 280, text=title_text, anchor="nw", font=("Helvetica", 14, "bold"), fill=self.TEXT_FG)
            canvas.create_text(20, 305, text=author_text, anchor="nw", font=("Helvetica", 11), fill="#94a3b8")

            # --- Rounded Buttons ---
            btn_width = (width - 50) / 2
            btn_height = 38
            btn_y = 360

            # Check if book is in cart
            user_email = self.current_user['email']
            is_in_cart = self.db.is_in_cart(user_email, book['id'])
            
            # Modify button text and color based on cart status
            if is_in_cart:
                cart_btn_text = "✓ In Cart"
                cart_btn_color = "#64748b"  # Gray color
                cart_btn_hover = "#475569"
            else:
                cart_btn_text = "🛒 Add to Cart"
                cart_btn_color = self.ACCENT_PURPLE
                cart_btn_hover = "#5568d3"
            
            self.create_rounded_button(
                canvas, x=20, y=btn_y, width=btn_width, height=btn_height, radius=10,
                text=cart_btn_text, text_color="white", 
                bg_color=cart_btn_color, hover_color=cart_btn_hover,
                command=lambda b=book: self.add_to_cart(b) if not is_in_cart else None
            )

            is_borrowed = self.db.is_book_borrowed(book['id'])

            if is_borrowed:
                borrow_btn_text = "📕 Borrowed"
                borrow_btn_color = "#64748b"
                borrow_btn_hover = "#475569"
                borrow_enabled = False
            else:
                borrow_btn_text = "📖 Borrow"
                borrow_btn_color = self.ACCENT_GREEN
                borrow_btn_hover = "#38d46a"
                borrow_enabled = True

            self.create_rounded_button(
                canvas, x=30 + btn_width, y=btn_y, width=btn_width, height=btn_height, radius=10,
                text=borrow_btn_text, text_color="white", 
                bg_color=borrow_btn_color, hover_color=borrow_btn_hover,
                command=lambda b=book: self.borrow_book(b) if borrow_enabled else None
            )

        card_canvas.bind("<Configure>", redraw_card)
        # Initial draw
        card_canvas.after(10, redraw_card)

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Draw a rounded rectangle on a canvas."""
        points = [
            x1 + radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_rounded_button(self, canvas, x, y, width, height, radius, text, text_color, bg_color, hover_color, command):
        """Create a rounded button on a canvas with hover effects."""
        button_shape = self.round_rectangle(canvas, x, y, x + width, y + height, radius=radius, fill=bg_color, outline="")
        button_text = canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color, font=("Helvetica", 10, "bold"))
        
        # Tags for binding
        button_tag = f"button_{button_shape}"
        canvas.addtag_withtag(button_tag, button_shape)
        canvas.addtag_withtag(button_tag, button_text)

        canvas.tag_bind(button_tag, "<Button-1>", lambda event: command())
        
        def on_enter(event):
            canvas.itemconfig(button_shape, fill=hover_color)
        
        def on_leave(event):
            canvas.itemconfig(button_shape, fill=bg_color)
            
        canvas.tag_bind(button_tag, "<Enter>", on_enter)
        canvas.tag_bind(button_tag, "<Leave>", on_leave)
    
    def filter_books(self):
        search_query = self.search_var.get()
        if search_query == "Search by name or author...":
            search_query = ""
        self.display_books(search_query)
    
    def add_to_cart(self, book):
        user_email = self.current_user['email']
        
        # Check if already in cart
        if self.db.is_in_cart(user_email, book['id']):
            self.display_books()
            return
        
        # Add to cart
        success = self.db.add_to_cart(user_email, book['id'])
        
        if success:
            pass
        else:
            messagebox.showerror("Error", "Failed to add book to cart!")

    def borrow_book(self, book):
        user_email = self.current_user['email']
        
        # Check if user can borrow
        if not self.db.can_borrow_book(user_email):
            messagebox.showerror(
                "Borrowing Limit Reached",
                "You can only borrow maximum 2 books at a time!\n\n"
                "Please return your current books before borrowing new ones."
            )
            return
        
        # Check if book is already borrowed
        if self.db.is_book_borrowed(book['id']):
            messagebox.showwarning(
                "Book Already Borrowed",
                f"'{book['name']}' is currently borrowed by another user.\n\n"
                "Please check back later when it becomes available."
            )
            return
        
        # Confirm borrowing
        result = messagebox.askyesno(
            "Borrow Book",
            f"Do you want to borrow '{book['name']}'?\n\n"
            "Book Borrowing Terms:\n"
            "• Collect from library within 3 days\n"
            "• Return within 1.5 months (45 days)\n"
            "• Late return fine: ₹2 per day\n\n"
            "Do you accept these terms?"
        )
        
        if result:
            # Borrow the book
            borrow_result = self.db.borrow_book(user_email, book['id'])
            
            if borrow_result['success']:
                messagebox.showinfo(
                    "Book Borrowed Successfully!",
                    f"'{book['name']}' has been borrowed!\n\n"
                    f"📍 Collect from library by: {borrow_result['collection_deadline']}\n"
                    f"⏰ Return to library by: {borrow_result['return_deadline']}\n\n"
                    "⚠️ Failure to return on time will result in a fine of ₹2 per day.\n\n"
                    "Check 'Borrowed Books' section for details."
                )
                # Refresh the books display to update button states
                self.display_books()
            else:
                messagebox.showerror("Error", borrow_result['message'])
    
    def logout(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.main_app.current_user = None
            self.main_app.show_welcome_screen()