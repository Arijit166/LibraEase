import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
from admin.styled_message_box import StyledMessageBox
import os
import pandas as pd

class AdminIssueReturn:
    def __init__(self, parent, admin_dashboard):
        self.parent = parent
        self.admin_dashboard = admin_dashboard
        self.db = admin_dashboard.db
        
        # Colors
        self.APP_BG = admin_dashboard.APP_BG
        self.CARD_BG = admin_dashboard.CARD_BG
        self.INPUT_BG = admin_dashboard.INPUT_BG
        self.TEXT_FG = admin_dashboard.TEXT_FG
        self.ACCENT_GREEN = admin_dashboard.ACCENT_GREEN
        self.ACCENT_PURPLE = admin_dashboard.ACCENT_PURPLE
        
        self.show_issue_return_page()
    
    def show_issue_return_page(self):
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header with stats
        header_frame = tk.Frame(self.parent, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        # Title
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="⇄ Issue & Return Management",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
        # Stats cards
        stats_frame = tk.Frame(self.parent, bg=self.APP_BG)
        stats_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        stats = self.db.get_borrowed_stats()
        
        stats_data = [
            ("📚", "Active Borrowed", stats['active_borrowed'], self.ACCENT_PURPLE),
            ("⏳", "Pending Collection", stats['pending_collection'], "#fbbf24"),
            ("✅", "Collected", stats['collected'], self.ACCENT_GREEN),
            ("📥", "Returned", stats['returned'], "#64748b")
        ]
        
        for icon, label, value, color in stats_data:
            stat_card = tk.Frame(stats_frame, bg=self.CARD_BG, 
                               highlightthickness=1, highlightbackground="#334155")
            stat_card.pack(side="left", expand=True, fill="both", padx=10)
            
            tk.Label(
                stat_card,
                text=icon,
                font=("Helvetica", 24),
                fg=color,
                bg=self.CARD_BG
            ).pack(pady=(15, 5))
            
            tk.Label(
                stat_card,
                text=str(value),
                font=("Helvetica", 22, "bold"),
                fg=self.TEXT_FG,
                bg=self.CARD_BG
            ).pack()
            
            tk.Label(
                stat_card,
                text=label,
                font=("Helvetica", 10),
                fg="#94a3b8",
                bg=self.CARD_BG
            ).pack(pady=(0, 15))
        
        # Filter tabs
        filter_frame = tk.Frame(self.parent, bg=self.APP_BG)
        filter_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        self.filter_var = tk.StringVar(value="all")
        
        filters = [
            ("All", "all"),
            ("Pending Collection", "pending"),
            ("Collected", "collected"),
            ("Returned", "returned")
        ]
        
        for text, value in filters:
            rb = tk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.filter_var,
                value=value,
                font=("Helvetica", 11, "bold"),
                bg=self.APP_BG,
                fg=self.TEXT_FG,
                selectcolor=self.CARD_BG,
                activebackground=self.APP_BG,
                activeforeground=self.ACCENT_PURPLE,
                command=self.apply_filter,
                cursor="hand2"
            )
            rb.pack(side="left", padx=10)
        
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
        
        self.books_frame = tk.Frame(canvas, bg=self.APP_BG)
        
        self.books_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.books_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(40, 20), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", pady=(0, 20), padx=(0, 40))
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Load borrowed books
        self.display_borrowed_books()
    
    def apply_filter(self):
        self.display_borrowed_books()
    
    def display_borrowed_books(self):
        # Clear existing
        for widget in self.books_frame.winfo_children():
            widget.destroy()
        
        # Get all borrowed books
        borrowed_books = self.db.get_all_borrowed_books()
        
        # Apply filter
        filter_value = self.filter_var.get()
        
        if filter_value == "pending":
            borrowed_books = borrowed_books[
                (borrowed_books['status'] == 'borrowed') & 
                (borrowed_books['collected'] == False)
            ]
        elif filter_value == "collected":
            borrowed_books = borrowed_books[
                (borrowed_books['status'] == 'borrowed') & 
                (borrowed_books['collected'] == True)
            ]
        elif filter_value == "returned":
            borrowed_books = borrowed_books[borrowed_books['status'] == 'returned']
        # 'all' shows everything
        
        if len(borrowed_books) == 0:
            tk.Label(
                self.books_frame,
                text="📚 No books found in this category.",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG,
                justify="center"
            ).pack(expand=True, pady=50)
            return
        
        # Display books
        for _, book_data in borrowed_books.iterrows():
            self.create_book_card(self.books_frame, book_data)
    
    def create_book_card(self, parent, book_data):
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
            if pd.notna(book_data.get('image_path')) and os.path.exists(book_data['image_path']):
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
        ).pack(fill="x", pady=(0, 5))
        
        # User info
        tk.Label(
            right_frame,
            text=f"👤 Borrowed by: {book_data['user_name']} ({book_data['user_email']})",
            font=("Helvetica", 11),
            fg="#cbd5e1",
            bg=self.CARD_BG,
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        # Status and dates
        info_frame = tk.Frame(right_frame, bg=self.CARD_BG)
        info_frame.pack(fill="x")
        
        status = book_data['status']
        is_collected = book_data.get('collected', False)
        
        # Issue date
        issue_date = datetime.fromisoformat(book_data['issue_date'])
        tk.Label(
            info_frame,
            text=f"📅 Issued: {issue_date.strftime('%d %B %Y, %I:%M %p')}",
            font=("Helvetica", 10),
            fg=self.TEXT_FG,
            bg=self.CARD_BG,
            anchor="w"
        ).pack(fill="x", pady=2)
        
        if status == 'returned':
            # Show returned status
            tk.Label(
                info_frame,
                text="✅ RETURNED",
                font=("Helvetica", 12, "bold"),
                fg=self.ACCENT_GREEN,
                bg=self.CARD_BG,
                anchor="w"
            ).pack(fill="x", pady=(10, 2))
            
            if pd.notna(book_data.get('return_date')) and book_data.get('return_date'):
                return_date = datetime.fromisoformat(book_data['return_date'])
                tk.Label(
                    info_frame,
                    text=f"📥 Returned on: {return_date.strftime('%d %B %Y, %I:%M %p')}",
                    font=("Helvetica", 10),
                    fg="#94a3b8",
                    bg=self.CARD_BG,
                    anchor="w"
                ).pack(fill="x", pady=2)
        else:
            # Collection status
            if is_collected:
                tk.Label(
                    info_frame,
                    text="✅ Collected",
                    font=("Helvetica", 11, "bold"),
                    fg=self.ACCENT_GREEN,
                    bg=self.CARD_BG,
                    anchor="w"
                ).pack(fill="x", pady=(5, 2))
                
                if pd.notna(book_data.get('collection_date')) and book_data.get('collection_date'):
                    col_date = datetime.fromisoformat(book_data['collection_date'])
                    tk.Label(
                        info_frame,
                        text=f"📍 Collected on: {col_date.strftime('%d %B %Y, %I:%M %p')}",
                        font=("Helvetica", 10),
                        fg="#94a3b8",
                        bg=self.CARD_BG,
                        anchor="w"
                    ).pack(fill="x", pady=2)
            else:
                collection_deadline = datetime.fromisoformat(book_data['collection_deadline'])
                tk.Label(
                    info_frame,
                    text=f"⏳ Collect by: {collection_deadline.strftime('%d %B %Y')}",
                    font=("Helvetica", 11),
                    fg="#fbbf24",
                    bg=self.CARD_BG,
                    anchor="w"
                ).pack(fill="x", pady=(5, 2))
            
            # Return deadline
            return_deadline = datetime.fromisoformat(book_data['return_deadline'])
            days_left = (return_deadline - datetime.now()).days
            deadline_color = "#ef4444" if days_left < 7 else self.ACCENT_GREEN
            
            tk.Label(
                info_frame,
                text=f"⏰ Return by: {return_deadline.strftime('%d %B %Y')} ({days_left} days left)",
                font=("Helvetica", 10),
                fg=deadline_color,
                bg=self.CARD_BG,
                anchor="w"
            ).pack(fill="x", pady=2)
        
        # Action buttons
        if status == 'borrowed':
            btn_frame = tk.Frame(right_frame, bg=self.CARD_BG)
            btn_frame.pack(fill="x", pady=(15, 0))
            
            if not is_collected:
                # Show "Mark as Collected" button
                collect_btn = tk.Button(
                    btn_frame,
                    text="✅ Mark as Collected",
                    font=("Helvetica", 11, "bold"),
                    bg=self.ACCENT_GREEN,
                    fg="white",
                    relief="flat",
                    cursor="hand2",
                    activebackground="#38d46a",
                    command=lambda: self.mark_collected(book_data)
                )
                collect_btn.pack(side="left", padx=(0, 10), ipadx=15, ipady=8)
                collect_btn.bind("<Enter>", lambda e: collect_btn.config(bg="#38d46a"))
                collect_btn.bind("<Leave>", lambda e: collect_btn.config(bg=self.ACCENT_GREEN))
            else:
                # Show "Mark as Returned" button
                return_btn = tk.Button(
                    btn_frame,
                    text="📥 Mark as Returned",
                    font=("Helvetica", 11, "bold"),
                    bg=self.ACCENT_PURPLE,
                    fg="white",
                    relief="flat",
                    cursor="hand2",
                    activebackground="#5568d3",
                    command=lambda: self.mark_returned(book_data)
                )
                return_btn.pack(side="left", ipadx=15, ipady=8)
                return_btn.bind("<Enter>", lambda e: return_btn.config(bg="#5568d3"))
                return_btn.bind("<Leave>", lambda e: return_btn.config(bg=self.ACCENT_PURPLE))
    
    def mark_collected(self, book_data):
        result = StyledMessageBox.ask_yes_no(
            self.parent,
            "Confirm Collection",
            f"Mark '{book_data['name']}' as collected by {book_data['user_name']}?"
        )
        
        if result:
            success = self.db.mark_book_collected(
                book_data['user_email'], 
                book_data['book_id']
            )
            
            if success:
                # Refresh the page first
                self.show_issue_return_page()
                # Show success message after refresh
                self.admin_dashboard.root.after(100, lambda: StyledMessageBox.show_success(
                    self.parent,
                    "Success", 
                    f"✅ '{book_data['name']}' marked as collected!\n\nUser: {book_data['user_name']}"
                ))
            else:
                StyledMessageBox.show_error(self.parent, "Error", "Failed to update collection status!")
    
    def mark_returned(self, book_data):
        result = StyledMessageBox.ask_yes_no(
            self.parent,
            "Confirm Return",
            f"Mark '{book_data['name']}' as returned by {book_data['user_name']}?"
        )
        
        if result:
            success = self.db.mark_book_returned(
                book_data['user_email'], 
                book_data['book_id']
            )
            
            if success:
                # Refresh the page first
                self.show_issue_return_page()
                # Show success message after refresh
                self.admin_dashboard.root.after(100, lambda: StyledMessageBox.show_success(
                    self.parent,
                    "Success", 
                    f"✅ '{book_data['name']}' has been returned!\n\nUser: {book_data['user_name']}\n\nThe book is now available in the library."
                ))
            else:
                StyledMessageBox.show_error(self.parent, "Error", "Failed to update return status!")