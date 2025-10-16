import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import pandas as pd
import os

class UserBorrowingPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.current_user = main_app.current_user
        self.db = main_app.db
        
        # Colors matching the UI
        self.APP_BG = "#0f172a"
        self.CARD_BG = "#1e293b"
        self.INPUT_BG = "#334155"
        self.TEXT_FG = "#e5e7eb"
        self.ACCENT_GREEN = "#43e97b"
        self.ACCENT_PURPLE = "#667eea"
        
        self.show_borrowed_books()
    
    def show_borrowed_books(self):
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.parent, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="📖 Borrowed Books",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
        # Get borrowed books
        user_email = self.current_user['email']
        borrowed_books = self.db.get_user_borrowed_books(user_email)
        
        if len(borrowed_books) == 0:
            tk.Label(
                self.parent,
                text="📚 No borrowed books yet.\n\nBorrow books from the Books section!",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG,
                justify="center"
            ).pack(expand=True, pady=50)
            return
        
        # Scrollable frame for borrowed books
        canvas = tk.Canvas(self.parent, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)

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

        books_frame = tk.Frame(canvas, bg=self.APP_BG)
        
        books_frame = tk.Frame(canvas, bg=self.APP_BG)
        books_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=books_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Make books_frame expand to canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(40, 20), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", pady=(0, 20), padx=(0, 40))
        
        # Display each borrowed book
        borrowed_list = borrowed_books.to_dict('records')
        for book_data in borrowed_list:
            self.create_borrowed_book_card(books_frame, book_data)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_borrowed_book_card(self, parent, book_data):
        # Card container
        card = tk.Frame(parent, bg=self.CARD_BG, highlightthickness=1, 
                       highlightbackground="#334155")
        card.pack(fill="both", expand=True, pady=15)
        
        # Main content frame
        content_frame = tk.Frame(card, bg=self.CARD_BG)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Book image
        left_frame = tk.Frame(content_frame, bg=self.CARD_BG)
        left_frame.pack(side="left", padx=(0, 20))
        
        try:
            if book_data.get('image_path') and os.path.exists(book_data['image_path']):
                img = Image.open(book_data['image_path'])
                img = img.resize((160, 220), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(left_frame, image=photo, bg=self.CARD_BG)
                img_label.image = photo
                img_label.pack()
            else:
                tk.Label(
                    left_frame,
                    text="📚\nNo Image",
                    font=("Helvetica", 12),
                    fg="#64748b",
                    bg=self.CARD_BG,
                    justify="center"
                ).pack()
        except Exception:
            tk.Label(
                left_frame,
                text="📚\nNo Image",
                font=("Helvetica", 12),
                fg="#64748b",
                bg=self.CARD_BG,
                justify="center"
            ).pack()
        
        # Right side - Book details
        right_frame = tk.Frame(content_frame, bg=self.CARD_BG)
        right_frame.pack(side="left", fill="both", expand=True)
        
        # Book title
        tk.Label(
            right_frame,
            text=book_data['name'],
            font=("Helvetica", 18, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Author
        tk.Label(
            right_frame,
            text=f"by {book_data['author']}",
            font=("Helvetica", 12),
            fg="#94a3b8",
            bg=self.CARD_BG,
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        # Status indicator
        status = book_data['status']
        if status == 'returned':
            status_color = self.ACCENT_GREEN
            status_text = "✓ RETURNED"
        else:
            status_color = self.ACCENT_PURPLE
            status_text = "📖 BORROWED"
        
        status_frame = tk.Frame(right_frame, bg=status_color, highlightthickness=0)
        status_frame.pack(anchor="w", pady=(0, 15))
        
        tk.Label(
            status_frame,
            text=status_text,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg=status_color,
            padx=12,
            pady=4
        ).pack()

        # Dates information
        info_frame = tk.Frame(right_frame, bg=self.CARD_BG)
        info_frame.pack(fill="x")

        if status == 'returned':
            tk.Label(
                info_frame,
                text="✅ This book has been returned to the library.",
                font=("Helvetica", 11),
                fg=self.ACCENT_GREEN,
                bg=self.CARD_BG,
                anchor="w"
            ).pack(fill="x")
            
            # Show return date if available
            if pd.notna(book_data.get('return_date')) and book_data.get('return_date'):
                return_date = datetime.fromisoformat(book_data['return_date'])
                tk.Label(
                    info_frame,
                    text=f"📅 Returned on: {return_date.strftime('%d %B %Y, %I:%M %p')}",
                    font=("Helvetica", 10),
                    fg="#94a3b8",
                    bg=self.CARD_BG,
                    anchor="w"
                ).pack(fill="x", pady=(5, 0))
        else:
            # Issue date
            issue_date = datetime.fromisoformat(book_data['issue_date'])
            tk.Label(
                info_frame,
                text=f"📅 Issue Date: {issue_date.strftime('%d %B %Y, %I:%M %p')}",
                font=("Helvetica", 11),
                fg=self.TEXT_FG,
                bg=self.CARD_BG,
                anchor="w"
            ).pack(fill="x", pady=2)
            
            # Check if collected
            is_collected = book_data.get('collected', False)
            
            if is_collected:
                # Show collected status
                collection_date = book_data.get('collection_date')
                if pd.notna(collection_date) and collection_date:
                    col_date = datetime.fromisoformat(collection_date)
                    tk.Label(
                        info_frame,
                        text=f"✅ Collected on: {col_date.strftime('%d %B %Y, %I:%M %p')}",
                        font=("Helvetica", 11),
                        fg=self.ACCENT_GREEN,
                        bg=self.CARD_BG,
                        anchor="w"
                    ).pack(fill="x", pady=2)
                else:
                    tk.Label(
                        info_frame,
                        text="✅ Collected from library",
                        font=("Helvetica", 11),
                        fg=self.ACCENT_GREEN,
                        bg=self.CARD_BG,
                        anchor="w"
                    ).pack(fill="x", pady=2)
            else:
                # Collection deadline
                collection_deadline = datetime.fromisoformat(book_data['collection_deadline'])
                tk.Label(
                    info_frame,
                    text=f"📍 Collect by: {collection_deadline.strftime('%d %B %Y')}",
                    font=("Helvetica", 11),
                    fg="#fbbf24",
                    bg=self.CARD_BG,
                    anchor="w"
                ).pack(fill="x", pady=2)
            
            # Return deadline
            return_deadline = datetime.fromisoformat(book_data['return_deadline'])
            days_left = (return_deadline - datetime.now()).days
            
            deadline_color = "#ef4444" if days_left < 7 else self.ACCENT_GREEN
            
            tk.Label(
                info_frame,
                text=f"⏰ Return by: {return_deadline.strftime('%d %B %Y')} ({days_left} days left)",
                font=("Helvetica", 11),
                fg=deadline_color,
                bg=self.CARD_BG,
                anchor="w"
            ).pack(fill="x", pady=2)
            
            # Fine warning (only if collected)
            if is_collected:
                tk.Label(
                    info_frame,
                    text="⚠️ Late return fine: ₹2 per day after deadline",
                    font=("Helvetica", 10, "italic"),
                    fg="#f59e0b",
                    bg=self.CARD_BG,
                    anchor="w"
                ).pack(fill="x", pady=(8, 0))