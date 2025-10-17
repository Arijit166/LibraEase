import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class AdminAnalytics:
    def __init__(self, parent, admin_dashboard):
        self.parent = parent
        self.admin_dashboard = admin_dashboard
        self.db = admin_dashboard.db
        
        # Colors matching the UI
        self.APP_BG = admin_dashboard.APP_BG
        self.CARD_BG = admin_dashboard.CARD_BG
        self.INPUT_BG = admin_dashboard.INPUT_BG
        self.TEXT_FG = admin_dashboard.TEXT_FG
        self.ACCENT_GREEN = admin_dashboard.ACCENT_GREEN
        self.ACCENT_PURPLE = admin_dashboard.ACCENT_PURPLE
        
        self.show_analytics_page()
    
    def show_analytics_page(self):
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.parent, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        # Title centered
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="📊 Library Analytics",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
        # Stats cards container
        stats_frame = tk.Frame(self.parent, bg=self.APP_BG)
        stats_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Get statistics
        total_books = len(self.db.get_all_books())
        total_users = len(self.db.get_all_users()[self.db.get_all_users()['role'] == 'User'])
        borrowed_stats = self.db.get_borrowed_stats()
        
        stats_data = [
            ("📚", "Total Books", total_books, self.ACCENT_PURPLE),
            ("👥", "Total Members", total_users, self.ACCENT_GREEN),
            ("📖", "Active Borrows", borrowed_stats['active_borrowed'], "#fbbf24"),
            ("✅", "Total Returns", borrowed_stats['returned'], "#64748b")
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
        
        # Scrollable container for charts
        canvas_frame = tk.Frame(self.parent, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
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
        
        charts_container = tk.Frame(canvas, bg=self.APP_BG)
        
        charts_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=charts_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling - bind only when mouse is over canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Create charts
        self.create_borrowing_chart(charts_container)
        self.create_user_activity_chart(charts_container)
    
    def create_borrowing_chart(self, parent):
        """Create a bar chart showing books borrowed from most to least"""
        # Card for chart
        chart_card = tk.Frame(parent, bg=self.CARD_BG, highlightthickness=1, 
                            highlightbackground="#334155")
        chart_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Chart title
        tk.Label(
            chart_card,
            text="📚 Most Borrowed Books",
            font=("Helvetica", 18, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.CARD_BG
        ).pack(pady=(20, 10))
        
        # Get borrowing data
        borrowed_df = self.db.get_all_borrowed_books()
        books_df = self.db.get_all_books()
        
        if len(borrowed_df) == 0 or len(books_df) == 0:
            tk.Label(
                chart_card,
                text="No borrowing data available yet.",
                font=("Helvetica", 14),
                fg="#64748b",
                bg=self.CARD_BG
            ).pack(pady=50)
            return
        
        # Count borrows per book using numpy
        borrow_counts = borrowed_df.groupby('book_id').size()
        
        # Get all books and merge with counts
        book_stats = books_df.copy()
        book_stats['borrow_count'] = book_stats['id'].map(borrow_counts).fillna(0).astype(int)
        
        # Sort by borrow count (most to least)
        book_stats = book_stats.sort_values('borrow_count', ascending=False)
        
        # Take top 10 books
        top_books = book_stats.head(10)
        
        if len(top_books) == 0:
            tk.Label(
                chart_card,
                text="No books have been borrowed yet.",
                font=("Helvetica", 14),
                fg="#64748b",
                bg=self.CARD_BG
            ).pack(pady=50)
            return
        
        # Prepare data
        book_names = [name[:15] + "..." if len(name) > 15 else name 
                     for name in top_books['name'].values]
        borrow_counts = top_books['borrow_count'].values
        
        # Create matplotlib figure with dark theme
        fig = Figure(figsize=(12, 6), facecolor=self.CARD_BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.CARD_BG)
        
        # Create vibrant gradient colors from electric purple to neon green
        n_bars = len(book_names)
        colors = []
        for i in range(n_bars):
            # Interpolate between bright purple and bright green
            ratio = i / max(n_bars - 1, 1)
            # Bright purple (138, 43, 226) to Neon green (57, 255, 20)
            r = int(138 * (1 - ratio) + 57 * ratio)
            g = int(43 * (1 - ratio) + 255 * ratio)
            b = int(226 * (1 - ratio) + 20 * ratio)
            colors.append(f'#{r:02x}{g:02x}{b:02x}')
        
        # Create bars with glow effect
        bars = ax.bar(np.arange(len(book_names)), borrow_counts, 
                     color=colors, edgecolor='#00ffff', linewidth=2, alpha=0.9)
        
        # Add value labels on bars with bright color
        for i, (bar, count) in enumerate(zip(bars, borrow_counts)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                   f'{int(count)}',
                   ha='center', va='bottom', 
                   fontsize=11, fontweight='bold',
                   color='#00ffff')
        
        # Customize chart with bright accents
        ax.set_xlabel('Books', fontsize=13, color='#00ffff', fontweight='bold')
        ax.set_ylabel('Number of Borrows', fontsize=13, color='#00ffff', fontweight='bold')
        ax.set_xticks(np.arange(len(book_names)))
        ax.set_xticklabels(book_names, rotation=45, ha='right', fontsize=10, color='#e0e0e0')
        ax.tick_params(axis='y', labelcolor='#e0e0e0', colors='#00ffff')
        ax.tick_params(axis='x', colors='#00ffff')
        
        # Grid with bright cyan color
        ax.grid(axis='y', alpha=0.3, linestyle='--', color='#00ffff')
        ax.set_axisbelow(True)
        
        # Remove top and right spines, make others bright
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#00ffff')
        ax.spines['bottom'].set_color('#00ffff')
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
        
        # Adjust layout
        fig.tight_layout()
        
        # Embed chart in tkinter
        chart_canvas = FigureCanvasTkAgg(fig, chart_card)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_user_activity_chart(self, parent):
        """Create a pie chart showing borrowing status distribution"""
        # Card for chart
        chart_card = tk.Frame(parent, bg=self.CARD_BG, highlightthickness=1, 
                            highlightbackground="#334155")
        chart_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Chart title
        tk.Label(
            chart_card,
            text="📊 Borrowing Status Distribution",
            font=("Helvetica", 18, "bold"),
            fg=self.ACCENT_GREEN,
            bg=self.CARD_BG
        ).pack(pady=(20, 10))
        
        # Get statistics
        stats = self.db.get_borrowed_stats()
        
        if stats['total_borrowed'] == 0:
            tk.Label(
                chart_card,
                text="No borrowing activity yet.",
                font=("Helvetica", 14),
                fg="#64748b",
                bg=self.CARD_BG
            ).pack(pady=50)
            return
        
        # Prepare data
        labels = ['Pending Collection', 'Collected', 'Returned']
        sizes = np.array([
            stats['pending_collection'],
            stats['collected'],
            stats['returned']
        ])
        
        # Filter out zero values
        non_zero_mask = sizes > 0
        labels = np.array(labels)[non_zero_mask].tolist()
        sizes = sizes[non_zero_mask]
        
        if len(sizes) == 0:
            tk.Label(
                chart_card,
                text="No data to display.",
                font=("Helvetica", 14),
                fg="#64748b",
                bg=self.CARD_BG
            ).pack(pady=50)
            return
        
        # Vibrant colors matching the UI - bright and eye-catching
        colors = ['#ffcc00', '#ff00ff', '#00ff00']  # Bright yellow, magenta, neon green
        colors = [colors[i] for i, mask in enumerate(non_zero_mask) if mask]
        
        # Create matplotlib figure with dark theme
        fig = Figure(figsize=(10, 6), facecolor=self.CARD_BG)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.CARD_BG)
        
        # Create pie chart with vibrant styling
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.08] * len(sizes),
            shadow=True,
            textprops={'color': '#ffffff', 'fontsize': 12, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': '#00ffff', 'linewidth': 2.5, 'alpha': 0.95}
        )
        
        # Style percentage text with bright color
        for autotext in autotexts:
            autotext.set_color('#f5f5f5')  
            autotext.set_fontweight('bold')
        
        # Add a circle at the center to make it a donut chart
        centre_circle = plt.Circle((0, 0), 0.70, fc=self.CARD_BG, linewidth=0)
        ax.add_artist(centre_circle)
        
        # Add total in center with bright color
        ax.text(0, 0, f"{stats['total_borrowed']}\nTotal\nBorrows", 
               ha='center', va='center',
               fontsize=18, fontweight='bold', color='#00ffff')
        
        ax.axis('equal')
        
        # Add legend with bright styling
        legend = ax.legend(
            wedges,
            [f"{label}: {size}" for label, size in zip(labels, sizes)],
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            facecolor=self.INPUT_BG,
            edgecolor='#00ffff',
            labelcolor='#ffffff',
            fontsize=11,
            title="Status",
            title_fontsize=12
        )

        # ✅ Change "Status" title color safely
        legend.get_title().set_color("#bf00ff")  # Electric purple
        legend.get_title().set_fontweight("bold")

        
        # Adjust layout
        fig.tight_layout()
        
        # Embed chart in tkinter
        chart_canvas = FigureCanvasTkAgg(fig, chart_card)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))