import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from database import DatabaseManager
import os
from dotenv import load_dotenv
load_dotenv()

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1400x800")

        # Center the window
        self.center_window(1400, 800)

        # Admin passkey
        self.ADMIN_PASSKEY = os.getenv("ADMIN_PASSKEY")
        self.db = DatabaseManager()
        # Data files
        self.users_file = "users.json"

        # Initialize data files
        self.init_data_files()

        # Current user
        self.current_user = None

        # Single dark background color (attractive slate-like)
        self.APP_BG = "#0f172a"  # slate-900 tone
        self.root.configure(bg=self.APP_BG)

        # Show welcome screen
        self.show_welcome_screen()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def init_data_files(self):
        pass

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_background(self, parent):
        """Create a single-color dark background (replaces gradient)."""
        # Create a canvas that fills the entire window
        canvas = tk.Canvas(parent, highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        
        def update_bg(event=None):
            # Update rectangle size when window is resized
            width = parent.winfo_width()
            height = parent.winfo_height()
            canvas.delete("bg")  # Remove old background
            canvas.create_rectangle(0, 0, width, height, fill=self.APP_BG, outline=self.APP_BG, tags="bg")
        
        # Bind to resize events
        parent.bind("<Configure>", update_bg)
        # Initial draw
        update_bg()
        return canvas

    def show_welcome_screen(self):
        self.clear_window()

        # Single-color dark background
        self.create_background(self.root)

        # Glass-like card with dark theme matching background
        container = tk.Frame(self.root, bg="#1e293b", bd=0)
        container.place(relx=0.5, rely=0.5, anchor="center", width=500, height=650)  # Increased height from 600 to 650

        # Subtle shadow
        shadow = tk.Frame(self.root, bg="#0b1020")
        shadow.place(relx=0.5, rely=0.505, anchor="center", width=510, height=660)  # Increased height from 610 to 660
        shadow.lower()
        container.lift()

        icon_frame = tk.Frame(container, bg="#1e293b")
        icon_frame.pack(pady=25)  # Changed from 40

        icon_label = tk.Label(icon_frame, text="📚", font=("Arial", 80), bg="#1e293b")  # Changed from 90
        icon_label.pack()

        title = tk.Label(
            container,
            text="Library Management",
            font=("Helvetica", 32, "bold"),  # Changed from 36
            fg="#667eea",
            bg="#1e293b",
        )
        title.pack(pady=3)  # Changed from 5

        subtitle = tk.Label(
            container,
            text="System",
            font=("Helvetica", 32, "bold"),  # Changed from 36
            fg="#a78bfa",
            bg="#1e293b",
        )
        subtitle.pack()

        tagline = tk.Label(
            container,
            text="Your Gateway to Infinite Knowledge",
            font=("Helvetica", 12, "italic"),  # Changed from 13
            fg="#94a3b8",
            bg="#1e293b",
        )
        tagline.pack(pady=10)  # Changed from 15

        line_frame = tk.Frame(container, bg="#475569", height=2, width=300)
        line_frame.pack(pady=15)  # Changed from 20

        btn_container = tk.Frame(container, bg="#1e293b")
        btn_container.pack(pady=15)  # Changed from 20

        login_btn = tk.Button(
            btn_container,
            text="🔐 LOGIN",
            font=("Helvetica", 14, "bold"),
            bg="#43e97b",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#38d46a",
            command=self.show_login,
        )
        login_btn.pack(pady=8, ipadx=60, ipady=10)
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#38d46a"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#43e97b"))

        # CREATE ACCOUNT button
        signup_btn = tk.Button(
            btn_container,
            text="✨ CREATE ACCOUNT",
            font=("Helvetica", 14, "bold"),
            bg="#667eea",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#5568d3",
            command=self.show_signup,
        )
        signup_btn.pack(pady=8, ipadx=35, ipady=10)
        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg="#5568d3"))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg="#667eea"))

        footer = tk.Label(
            container,
            text="© 2025 LMS | Powered by Knowledge",
            font=("Helvetica", 10),
            fg="#64748b",
            bg="#1e293b",
        )
        footer.pack(side="bottom", pady=20)  # Changed from 25

    def show_signup(self):
        self.clear_window()

        # Single-color dark background
        self.create_background(self.root)

        card_bg = "#1e293b"     
        input_bg = "#334155"     
        text_fg = "#e5e7eb"     
        muted_fg = "#9ca3af"     
        accent_green = "#43e97b" 
        accent_green_hover = "#38d46a"

        # Main card (formerly white)
        main_frame = tk.Frame(self.root, bg=card_bg, bd=0)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=550, height=720)

        # Shadow
        shadow = tk.Frame(self.root, bg="#0b1020")
        shadow.place(relx=0.5, rely=0.505, anchor="center", width=560, height=730)
        shadow.lower()
        main_frame.lift()

        # Header (kept brand indigo)
        header_frame = tk.Frame(main_frame, bg="#667eea", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Helvetica", 12, "bold"),
            bg="#667eea",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#5568d3",
            command=self.show_welcome_screen,
        )
        back_btn.place(x=20, y=15)

        header_label = tk.Label(
            header_frame,
            text="Create Your Account",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg="#667eea",
        )
        header_label.place(relx=0.5, rely=0.6, anchor="center")

        # Create a canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_frame, bg=card_bg, highlightthickness=0)

        # Change from tk.Scrollbar to ttk.Scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=canvas.yview,
        )

        scrollable_frame = tk.Frame(canvas, bg=card_bg)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=450)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Style scrollbar to match UI (MOVE THIS BEFORE creating the scrollbar)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#334155",
            darkcolor="#1e293b",
            lightcolor="#1e293b",
            troughcolor="#1e293b",
            bordercolor="#1e293b",
            arrowcolor="#94a3b8",
        )

        canvas.pack(side="left", fill="both", expand=True, padx=(50, 0), pady=32)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=32)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Now use scrollable_frame instead of form_frame for all form elements
        form_frame = scrollable_frame

        # First Name
        tk.Label(
            form_frame,
            text="🪪 First Name",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
        ).pack(anchor="w", pady=(8, 6))

        first_frame = tk.Frame(form_frame, bg=input_bg, bd=0, highlightthickness=1, highlightbackground="#475569")
        first_frame.pack(fill="x", pady=(0, 16))
        first_entry = tk.Entry(first_frame, font=("Helvetica", 13), relief="flat", bd=0, bg=input_bg, fg=text_fg, insertbackground=text_fg)
        first_entry.pack(fill="x", padx=15, pady=12)

        # Last Name
        tk.Label(
            form_frame,
            text="🪪 Last Name",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
        ).pack(anchor="w", pady=(4, 6))

        last_frame = tk.Frame(form_frame, bg=input_bg, bd=0, highlightthickness=1, highlightbackground="#475569")
        last_frame.pack(fill="x", pady=(0, 16))
        last_entry = tk.Entry(last_frame, font=("Helvetica", 13), relief="flat", bd=0, bg=input_bg, fg=text_fg, insertbackground=text_fg)
        last_entry.pack(fill="x", padx=15, pady=12)

        # Email
        tk.Label(
            form_frame,
            text="📧 Email",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
        ).pack(anchor="w", pady=(4, 6))

        email_frame = tk.Frame(form_frame, bg=input_bg, bd=0, highlightthickness=1, highlightbackground="#475569")
        email_frame.pack(fill="x", pady=(0, 16))
        email_entry = tk.Entry(email_frame, font=("Helvetica", 13), relief="flat", bd=0, bg=input_bg, fg=text_fg, insertbackground=text_fg)
        email_entry.pack(fill="x", padx=15, pady=12)

        # Password
        tk.Label(
            form_frame,
            text="🔒 Password",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
        ).pack(anchor="w", pady=(4, 6))

        password_frame = tk.Frame(form_frame, bg=input_bg, bd=0, highlightthickness=1, highlightbackground="#475569")
        password_frame.pack(fill="x", pady=(0, 20))
        password_entry = tk.Entry(
            password_frame,
            font=("Helvetica", 13),
            show="●",
            relief="flat",
            bd=0,
            bg=input_bg,
            fg=text_fg,
            insertbackground=text_fg,
        )
        password_entry.pack(fill="x", padx=15, pady=12)

        # Role
        tk.Label(
            form_frame,
            text="👥 Select Your Role",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
        ).pack(anchor="w", pady=(6, 10))

        role_var = tk.StringVar(value="User")
        role_frame = tk.Frame(form_frame, bg=card_bg)
        role_frame.pack(anchor="w", pady=(0, 10))

        # Custom styled radio buttons
        user_radio = tk.Radiobutton(
            role_frame,
            text="User",
            variable=role_var,
            value="User",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
            activebackground=card_bg,
            activeforeground=accent_green,
            selectcolor=card_bg,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            indicatoron=1,
        )
        user_radio.pack(side="left", padx=(0, 30))

        admin_radio = tk.Radiobutton(
            role_frame,
            text="Admin (requires passkey)",
            variable=role_var,
            value="Admin",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg=text_fg,
            activebackground=card_bg,
            activeforeground=accent_green,
            selectcolor=card_bg,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            indicatoron=1,
        )
        admin_radio.pack(side="left")

        # Admin passkey container
        passkey_container = tk.Frame(form_frame, bg=card_bg)

        passkey_label = tk.Label(
            passkey_container,
            text="🔑 Admin Passkey",
            font=("Helvetica", 12, "bold"),
            bg=card_bg,
            fg="#fbbf24",
        )

        passkey_frame_inner = tk.Frame(
            passkey_container, 
            bg="#2c1e10", 
            bd=0, 
            highlightthickness=2, 
            highlightbackground="#f59e0b"
        )
        passkey_entry = tk.Entry(
            passkey_frame_inner,
            font=("Helvetica", 13),
            show="●",
            relief="flat",
            bd=0,
            bg="#2c1e10",
            fg="#fde68a",
            insertbackground="#fde68a",
        )

        def handle_signup():
            first_name = first_entry.get().strip()
            last_name = last_entry.get().strip()
            email = email_entry.get().strip().lower()
            password = password_entry.get().strip()
            role = role_var.get()

            if not first_name or not last_name or not email or not password:
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            if len(first_name) < 2 or len(last_name) < 2:
                messagebox.showerror("Error", "Names must be at least 2 characters!")
                return

            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "Please enter a valid email address!")
                return

            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters!")
                return

            if role == "Admin":
                admin_key = passkey_entry.get().strip()
                if admin_key != self.ADMIN_PASSKEY:
                    messagebox.showerror("Error", "Invalid admin passkey!")
                    return

            if self.db.user_exists(email):
                messagebox.showerror("Error", "Email already exists! Please log in.")
                return

            self.db.create_user(email, first_name, last_name, password, role)

            # Set current user
            self.current_user = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            }

            # Redirect based on role first
            if role == 'Admin':
                from admin.manage_book import AdminDashboard
                AdminDashboard(self.root, self)
            else:
                from user.book import UserBooksPage
                UserBooksPage(self.root, self)

            # Redirect based on role
            if role == 'Admin':
                from admin.manage_book import AdminDashboard
                AdminDashboard(self.root, self)
            else:
                from user.book import UserBooksPage
                UserBooksPage(self.root, self)

        signup_btn = tk.Button(
            form_frame,
            text="CREATE ACCOUNT",
            font=("Helvetica", 14, "bold"),
            bg=accent_green,
            fg="white",
            width=30,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground=accent_green_hover,
            command=handle_signup,
        )

        # Helper note
        helper_note = tk.Label(
            form_frame,
            text="By creating an account you agree to our Terms & Privacy.",
            font=("Helvetica", 10),
            bg=card_bg,
            fg=muted_fg,
        )

        def toggle_passkey(*args):
            passkey_container.pack_forget()
            signup_btn.pack_forget()
            helper_note.pack_forget()

            if role_var.get() == "Admin":
                passkey_container.pack(fill="x", pady=(8, 0))
                passkey_label.pack(anchor="w", pady=(0, 6))
                passkey_frame_inner.pack(fill="x")
                passkey_entry.pack(fill="x", padx=15, pady=12)
            
            signup_btn.pack(pady=(20, 0))
            helper_note.pack(pady=(16, 0))

        role_var.trace("w", toggle_passkey)

        # Initial placement
        signup_btn.pack(pady=(20, 0))
        helper_note.pack(pady=(16, 0))

        # Hover effects
        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg=accent_green_hover))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg=accent_green))

    def show_login(self):
        self.clear_window()

        # Single-color dark background
        self.create_background(self.root)

        # Main card with dark theme
        main_frame = tk.Frame(self.root, bg="#1e293b", bd=0)  # Changed from white
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=550, height=600)

        # Shadow
        shadow = tk.Frame(self.root, bg="#0b1020")
        shadow.place(relx=0.5, rely=0.505, anchor="center", width=560, height=610)
        shadow.lower()
        main_frame.lift()

        # Header
        header_frame = tk.Frame(main_frame, bg="#43e97b", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Helvetica", 12, "bold"),
            bg="#43e97b",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#38d46a",
            command=self.show_welcome_screen,
        )
        back_btn.place(x=20, y=15)

        header_label = tk.Label(
            header_frame,
            text="Welcome Back!",
            font=("Helvetica", 32, "bold"),
            fg="white",
            bg="#43e97b",
        )
        header_label.place(relx=0.5, rely=0.6, anchor="center")

        # Form
        form_frame = tk.Frame(main_frame, bg="#1e293b")  # Match main frame
        form_frame.pack(fill="both", expand=True, padx=50, pady=50)

        tk.Label(
            form_frame,
            text="📧 Email",
            font=("Helvetica", 12, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",  # Light text
        ).pack(anchor="w", pady=(20, 5))

        email_frame = tk.Frame(form_frame, bg="#334155", bd=0, highlightthickness=1, highlightbackground="#475569")
        email_frame.pack(fill="x", pady=(0, 25))

        email_entry = tk.Entry(
            email_frame, 
            font=("Helvetica", 13), 
            relief="flat", 
            bd=0, 
            bg="#334155",
            fg="#e5e7eb",
            insertbackground="#e5e7eb"
        )
        email_entry.pack(fill="x", padx=15, pady=12)

        tk.Label(
            form_frame,
            text="🔒 Password",
            font=("Helvetica", 12, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(anchor="w", pady=(10, 5))

        password_frame = tk.Frame(form_frame, bg="#334155", bd=0, highlightthickness=1, highlightbackground="#475569")
        password_frame.pack(fill="x", pady=(0, 35))

        password_entry = tk.Entry(
            password_frame,
            font=("Helvetica", 13),
            show="●",
            relief="flat",
            bd=0,
            bg="#334155",
            fg="#e5e7eb",
            insertbackground="#e5e7eb"
        )
        password_entry.pack(fill="x", padx=15, pady=12)

        # In handle_login function (inside show_login method):
        def handle_login():
            email = email_entry.get().strip().lower()
            password = password_entry.get().strip()

            if not email or not password:
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            # Use database manager
            user_data = self.db.validate_login(email, password)
            
            if user_data is None:
                messagebox.showerror("Error", "Invalid email or password!")
                return

            self.current_user = user_data
            display_name = self.current_user["first_name"] or email
            
            # Check role and redirect accordingly first
            if self.current_user['role'] == 'Admin':
                from admin.manage_book import AdminDashboard
                AdminDashboard(self.root, self)
            else:
                from user.book import UserBooksPage
                UserBooksPage(self.root, self)

            # Check role and redirect accordingly
            if self.current_user['role'] == 'Admin':
                from admin.manage_book import AdminDashboard
                AdminDashboard(self.root, self)
            else:
                from user.book import UserBooksPage
                UserBooksPage(self.root, self)
    

        login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            font=("Helvetica", 14, "bold"),
            bg="#667eea",
            fg="white",
            width=30,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground="#5568d3",
            command=handle_login,
        )
        login_btn.pack(pady=(10, 10))
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#5568d3"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#667eea"))

        account_frame = tk.Frame(form_frame, bg="#1e293b")
        account_frame.pack(pady=15)

        tk.Label(
            account_frame,
            text="Don't have an account?",
            font=("Helvetica", 10),
            bg="#1e293b",
            fg="#94a3b8",
        ).pack(side="left")

        signup_link = tk.Label(
            account_frame,
            text="Sign Up",
            font=("Helvetica", 10, "bold underline"),
            bg="#1e293b",
            fg="#667eea",
            cursor="hand2",
        )
        signup_link.pack(side="left", padx=5)
        signup_link.bind("<Button-1>", lambda e: self.show_signup())


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
