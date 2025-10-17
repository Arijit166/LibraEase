import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pandas as pd

class AdminMembers:
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
        
        self.show_members_page()
    
    def show_members_page(self):
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.parent, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        # Title
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="👤 Member Management",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
        # Search Bar
        search_frame = tk.Frame(self.parent, bg=self.APP_BG)
        search_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Helvetica", 12, "bold"),
            fg=self.TEXT_FG,
            bg=self.APP_BG
        ).pack(side="left", padx=(0, 10))
        
        search_entry_frame = tk.Frame(search_frame, bg=self.INPUT_BG, 
                                     highlightthickness=1, highlightbackground="#475569")
        search_entry_frame.pack(side="left", fill="x", expand=True)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_members())
        
        search_entry = tk.Entry(
            search_entry_frame,
            textvariable=self.search_var,
            font=("Helvetica", 12),
            relief="flat",
            bd=0,
            bg=self.INPUT_BG,
            fg=self.TEXT_FG,  # Changed from "#64748b" to TEXT_FG
            insertbackground=self.TEXT_FG
        )

        # Placeholder setup
        placeholder = "Search by member name, book name, author or ID..."
        search_entry.insert(0, placeholder)
        search_entry.config(fg="#64748b")

        def on_focus_in(event):
            if search_entry.get() == placeholder:
                search_entry.delete(0, tk.END)
                search_entry.config(fg=self.TEXT_FG)

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, placeholder)
                search_entry.config(fg="#64748b")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        search_entry.pack(fill="x", padx=15, pady=10)
        
        # Members Grid Container with Scrollbar
        canvas_frame = tk.Frame(self.parent, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=(40, 20), pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.members_container = tk.Frame(canvas, bg=self.APP_BG)
        
        self.members_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.members_container, anchor="nw")
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
        
        # Load and display members
        self.display_members()
    
    def filter_members(self):
        search_query = self.search_var.get()
        placeholder = "Search by member name, book name, author or ID..."
        if search_query == placeholder or not search_query:
            search_query = ""
        self.display_members(search_query)
    
    def display_members(self, search_query=""):
        # Clear existing
        for widget in self.members_container.winfo_children():
            widget.destroy()
        
        # Get all users (excluding admins)
        users_df = self.db.get_all_users()
        users_df = users_df[users_df['role'] == 'User']
        
        if len(users_df) == 0:
            tk.Label(
                self.members_container,
                text="👥 No members found.",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG
            ).grid(pady=50)
            return
        
        # Get all borrowed books for filtering
        borrowed_df = self.db.get_all_borrowed_books()
        
        # Apply search filter
        if search_query:
            query_lower = search_query.lower()
            
            # Get all borrowed books once for efficiency
            all_borrows = self.db.get_all_borrowed_books()
            
            # Filter users based on name or if they have a borrowed book matching the query
            def user_matches(user):
                # Check user name
                user_name = f"{user['first_name']} {user['last_name']}".lower()
                if query_lower in user_name:
                    return True
                
                # Check user email (as ID)
                if query_lower in user['email'].lower():
                    return True
                
                # Check user's borrowed books
                user_borrows = all_borrows[all_borrows['user_email'] == user['email']]
                if not user_borrows.empty:
                    # Check book name, author, or ID (as string)
                    book_match = (
                        user_borrows['name'].str.lower().str.contains(query_lower, na=False) |
                        user_borrows['author'].str.lower().str.contains(query_lower, na=False) |
                        user_borrows['book_id'].astype(str).str.contains(query_lower, na=False)
                    )
                    if book_match.any():
                        return True
                
                return False

            # Apply the filter function
            matching_users_mask = users_df.apply(user_matches, axis=1)
            users_df = users_df[matching_users_mask]
        
        if len(users_df) == 0:
            tk.Label(
                self.members_container,
                text="🔍 No members found matching your search.",
                font=("Helvetica", 16),
                fg="#64748b",
                bg=self.APP_BG
            ).grid(pady=50)
            return
        
        # Display members in 3-column grid
        cols = 3
        for c in range(cols):
            self.members_container.grid_columnconfigure(c, weight=1, uniform="membercol")
        
        # Configure rows to not expand
        for idx, (_, user) in enumerate(users_df.iterrows()):
            r = idx // cols
            c = idx % cols
            self.members_container.grid_rowconfigure(r, weight=0)
            cell = tk.Frame(self.members_container, bg=self.APP_BG)
            cell.grid(row=r, column=c, padx=15, pady=15, sticky="new")
            self.create_member_card(cell, user)
    
    def create_member_card(self, parent, user):
        # Card container
        card = tk.Frame(parent, bg=self.CARD_BG, highlightthickness=1, 
                       highlightbackground="#334155")
        card.pack(fill="both", expand=True)
        
        # Content
        content = tk.Frame(card, bg=self.CARD_BG, cursor="hand2")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bind click only to specific elements
        def on_click(e):
            self.show_member_details(user)
        
        # Hover effects
        def on_enter(e):
            card.config(highlightbackground=self.ACCENT_PURPLE, highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground="#334155", highlightthickness=1)
        
        content.bind("<Enter>", on_enter)
        content.bind("<Leave>", on_leave)
        
        # User icon
        icon_label = tk.Label(
            content,
            text="👤",
            font=("Helvetica", 36),
            fg=self.ACCENT_GREEN,
            bg=self.CARD_BG,
            cursor="hand2"
        )
        icon_label.pack(pady=(0, 10))
        icon_label.bind("<Button-1>", on_click)
        
        # User name
        user_name = f"{user['first_name']} {user['last_name']}"
        name_label = tk.Label(
            content,
            text=user_name,
            font=("Helvetica", 16, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG,
            cursor="hand2"
        )
        name_label.pack()
        name_label.bind("<Button-1>", on_click)
        
        # Email
        email_label = tk.Label(
            content,
            text=user['email'],
            font=("Helvetica", 10),
            fg="#94a3b8",
            bg=self.CARD_BG,
            cursor="hand2"
        )
        email_label.pack(pady=(5, 15))
        email_label.bind("<Button-1>", on_click)
        
        # Get borrow statistics
        borrowed_df = self.db.get_all_borrowed_books()
        user_borrows = borrowed_df[borrowed_df['user_email'] == user['email']]
        
        active_count = len(user_borrows[user_borrows['status'] == 'borrowed'])
        total_count = len(user_borrows)
        
        # Stats
        stats_frame = tk.Frame(content, bg=self.CARD_BG, cursor="hand2")
        stats_frame.pack(fill="x")
        stats_frame.bind("<Button-1>", on_click)
        
        active_label = tk.Label(
            stats_frame,
            text=f"📚 Active: {active_count}",
            font=("Helvetica", 11),
            fg=self.ACCENT_PURPLE,
            bg=self.CARD_BG,
            cursor="hand2"
        )
        active_label.pack(side="left", expand=True)
        active_label.bind("<Button-1>", on_click)
        
        total_label = tk.Label(
            stats_frame,
            text=f"📊 Total: {total_count}",
            font=("Helvetica", 11),
            fg="#64748b",
            bg=self.CARD_BG,
            cursor="hand2"
        )
        total_label.pack(side="left", expand=True)
        total_label.bind("<Button-1>", on_click)
        
        # Click to view details
        details_label = tk.Label(
            content,
            text="Click to view details →",
            font=("Helvetica", 9, "italic"),
            fg="#475569",
            bg=self.CARD_BG,
            cursor="hand2"
        )
        details_label.pack(pady=(10, 0))
        details_label.bind("<Button-1>", on_click)
    
    def show_member_details(self, user):
        # Create detailed view dialog
        dialog = tk.Toplevel(self.admin_dashboard.root)
        dialog.title("Member Details")
        dialog.geometry("900x700")
        dialog.configure(bg=self.APP_BG)
        dialog.transient(self.admin_dashboard.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450)
        y = (dialog.winfo_screenheight() // 2) - (350)
        dialog.geometry(f"900x700+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.CARD_BG)
        header_frame.pack(fill="x", pady=(0, 20))
        
        content = tk.Frame(header_frame, bg=self.CARD_BG)
        content.pack(padx=30, pady=20)
        
        tk.Label(
            content,
            text="👤",
            font=("Helvetica", 32),
            fg=self.ACCENT_GREEN,
            bg=self.CARD_BG
        ).pack(side="left", padx=(0, 15))
        
        info_frame = tk.Frame(content, bg=self.CARD_BG)
        info_frame.pack(side="left")
        
        user_name = f"{user['first_name']} {user['last_name']}"
        tk.Label(
            info_frame,
            text=user_name,
            font=("Helvetica", 24, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=user['email'],
            font=("Helvetica", 12),
            fg="#94a3b8",
            bg=self.CARD_BG
        ).pack(anchor="w")
        
        # Borrowing records
        tk.Label(
            dialog,
            text="📚 Borrowing Records",
            font=("Helvetica", 18, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack(padx=30, pady=(0, 15), anchor="center")
        
        # Scrollable records
        canvas_frame = tk.Frame(dialog, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        records_frame = tk.Frame(canvas, bg=self.APP_BG)
        
        records_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=records_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling for dialog - bind only when mouse is over this canvas
        def _on_dialog_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_dialog_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_dialog_mousewheel)

        def _unbind_dialog_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_dialog_mousewheel)
        canvas.bind("<Leave>", _unbind_dialog_mousewheel)

        # Ensure mousewheel is unbound when dialog closes and rebind for main window
        def on_dialog_close():
            canvas.unbind_all("<MouseWheel>")
            dialog.destroy()

        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        
        # Get user's borrowing records
        borrowed_df = self.db.get_all_borrowed_books()
        user_records = borrowed_df[borrowed_df['user_email'] == user['email']]
        user_records = user_records.sort_values('issue_date', ascending=False)
        
        if len(user_records) == 0:
            tk.Label(
                records_frame,
                text="No borrowing history yet.",
                font=("Helvetica", 14),
                fg="#64748b",
                bg=self.APP_BG
            ).pack(pady=50)
        else:
            for _, record in user_records.iterrows():
                self.create_record_card(records_frame, record)
    
    def create_record_card(self, parent, record):
        # Card
        card = tk.Frame(parent, bg=self.CARD_BG, highlightthickness=1, 
                       highlightbackground="#334155")
        card.pack(fill="x", pady=10)
        
        content = tk.Frame(card, bg=self.CARD_BG)
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Top row - Book info and status
        top_frame = tk.Frame(content, bg=self.CARD_BG)
        top_frame.pack(fill="x")
        
        # Book info
        info_frame = tk.Frame(top_frame, bg=self.CARD_BG)
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            info_frame,
            text=record['name'],
            font=("Helvetica", 14, "bold"),
            fg=self.TEXT_FG,
            bg=self.CARD_BG,
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"by {record['author']}",
            font=("Helvetica", 11),
            fg="#94a3b8",
            bg=self.CARD_BG,
            anchor="w"
        ).pack(fill="x", pady=(2, 0))
        
        # Status badge
        status_frame = tk.Frame(top_frame, bg=self.CARD_BG)
        status_frame.pack(side="right")
        
        status = record['status']
        is_collected = record.get('collected', False)
        
        if status == 'returned':
            status_text = "✅ RETURNED"
            status_color = self.ACCENT_GREEN
        elif is_collected:
            status_text = "📖 COLLECTED"
            status_color = self.ACCENT_PURPLE
        else:
            status_text = "⏳ PENDING"
            status_color = "#fbbf24"
        
        status_label = tk.Label(
            status_frame,
            text=status_text,
            font=("Helvetica", 10, "bold"),
            fg=status_color,
            bg=self.CARD_BG
        )
        status_label.pack()
        
        # Dates
        dates_frame = tk.Frame(content, bg=self.CARD_BG)
        dates_frame.pack(fill="x", pady=(10, 0))
        
        issue_date = datetime.fromisoformat(record['issue_date'])
        tk.Label(
            dates_frame,
            text=f"📅 Issued: {issue_date.strftime('%d %b %Y, %I:%M %p')}",
            font=("Helvetica", 9),
            fg="#cbd5e1",
            bg=self.CARD_BG
        ).pack(side="left", padx=(0, 20))
        
        if status == 'returned' and pd.notna(record.get('return_date')) and record.get('return_date'):
            return_date = datetime.fromisoformat(record['return_date'])
            tk.Label(
                dates_frame,
                text=f"📥 Returned: {return_date.strftime('%d %b %Y, %I:%M %p')}",
                font=("Helvetica", 9),
                fg="#cbd5e1",
                bg=self.CARD_BG
            ).pack(side="left")
        elif status == 'borrowed':
            return_deadline = datetime.fromisoformat(record['return_deadline'])
            days_left = (return_deadline - datetime.now()).days
            deadline_color = "#ef4444" if days_left < 7 else self.ACCENT_GREEN
            
            tk.Label(
                dates_frame,
                text=f"⏰ Return by: {return_deadline.strftime('%d %b %Y')} ({days_left} days left)",
                font=("Helvetica", 9),
                fg=deadline_color,
                bg=self.CARD_BG
            ).pack(side="left")