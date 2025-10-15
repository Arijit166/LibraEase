import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class UserCartPage:
    def __init__(self, parent_frame, main_app):
        self.parent_frame = parent_frame
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
        
        self.show_cart()
    
    def show_cart(self):
        # Clear parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Header with title centered
        header_frame = tk.Frame(self.parent_frame, bg=self.APP_BG)
        header_frame.pack(fill="x", padx=40, pady=20)
        
        title_container = tk.Frame(header_frame, bg=self.APP_BG)
        title_container.pack(expand=True)
        
        tk.Label(
            title_container,
            text="My Cart",
            font=("Helvetica", 28, "bold"),
            fg=self.ACCENT_PURPLE,
            bg=self.APP_BG
        ).pack()
        
        # Cart Grid with Scrollbar
        canvas_frame = tk.Frame(self.parent_frame, bg=self.APP_BG)
        canvas_frame.pack(fill="both", expand=True, padx=(40, 20), pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=self.APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.cart_container = tk.Frame(canvas, bg=self.APP_BG)
        
        self.cart_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        self._cart_window_id = canvas.create_window((0, 0), window=self.cart_container, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfig(self._cart_window_id, width=event.width, height=event.height)

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
        
        # Load and display cart items
        self.display_cart_items()
    
    def display_cart_items(self):
        for widget in self.cart_container.winfo_children():
            widget.destroy()
        
        # Get user's cart items
        user_email = self.current_user['email']
        cart_items_df = self.db.get_user_cart(user_email)
        
        if len(cart_items_df) == 0:
            self.cart_container.grid_rowconfigure(0, weight=1)
            self.cart_container.grid_columnconfigure(0, weight=1)
            
            empty_frame = tk.Frame(self.cart_container, bg=self.APP_BG)
            empty_frame.grid(row=0, column=0, sticky="nsew")
            
            # Center content within the frame
            empty_content = tk.Frame(empty_frame, bg=self.APP_BG)
            empty_content.place(relx=0.5, rely=0.5, anchor="center")
            
            tk.Label(
                empty_content,
                text="🛒",
                font=("Helvetica", 60),
                fg="#64748b",
                bg=self.APP_BG
            ).pack()
            
            tk.Label(
                empty_content,
                text="Your cart is empty",
                font=("Helvetica", 20, "bold"),
                fg="#64748b",
                bg=self.APP_BG
            ).pack(pady=(10, 5))
            
            tk.Label(
                empty_content,
                text="Add books from the Books section to see them here!",
                font=("Helvetica", 12),
                fg="#94a3b8",
                bg=self.APP_BG
            ).pack()
            return
        
        books = cart_items_df.to_dict('records')
        
        # 4-column grid
        cols = 4
        for c in range(cols):
            self.cart_container.grid_columnconfigure(c, weight=1, uniform="cartcol")
        
        for idx, book in enumerate(books):
            r = idx // cols
            c = idx % cols
            cell = tk.Frame(self.cart_container, bg=self.APP_BG)
            cell.grid(row=r, column=c, padx=20, pady=20, sticky="nsew")
            self.create_cart_card(cell, book)
    
    def create_cart_card(self, parent, book):
        # Container with fixed height
        card_container = tk.Frame(parent, bg=self.APP_BG, height=450)
        card_container.pack(fill="both", expand=True)
        card_container.pack_propagate(False)
        
        # Canvas for rounded card
        card_canvas = tk.Canvas(card_container, bg=self.APP_BG, highlightthickness=0)
        card_canvas.pack(fill="both", expand=True)
        
        # Store references
        card_canvas.images = []
        
        def redraw_card(event=None):
            canvas = card_canvas
            width = canvas.winfo_width()
            height = 450
            canvas.delete("all")
            
            # Draw rounded card
            card_id = self.round_rectangle(canvas, 5, 5, width - 10, height - 5, radius=20, fill=self.CARD_BG, outline="#334155")
            
            # Hover effects
            def on_hover_enter(e):
                canvas.itemconfig(card_id, outline=self.ACCENT_GREEN, width=2)
            
            def on_hover_leave(e):
                canvas.itemconfig(card_id, outline="#334155", width=1)
            
            canvas.bind("<Enter>", on_hover_enter)
            canvas.bind("<Leave>", on_hover_leave)
            
            # Image
            img_y_pos = 135
            try:
                if book.get('image_path') and os.path.exists(book['image_path']):
                    img = Image.open(book['image_path'])
                    img = img.resize((220, 230), Image.Resampling.LANCZOS)
                    
                    photo = ImageTk.PhotoImage(img)
                    canvas.images.append(photo)
                    canvas.create_image(width / 2, img_y_pos, image=photo)
                else:
                    canvas.create_text(width / 2, img_y_pos, text="📚\nNo Image", font=("Helvetica", 16), fill="#64748b", justify="center")
            except Exception:
                canvas.create_text(width / 2, img_y_pos, text="📚\nNo Image", font=("Helvetica", 16), fill="#64748b", justify="center")
            
            # Book details
            title_text = book['name'][:20] + "..." if len(book['name']) > 20 else book['name']
            author_text = f"by {book['author'][:18]}..." if len(book['author']) > 18 else f"by {book['author']}"
            
            canvas.create_text(20, 280, text=title_text, anchor="nw", font=("Helvetica", 14, "bold"), fill=self.TEXT_FG)
            canvas.create_text(20, 305, text=author_text, anchor="nw", font=("Helvetica", 11), fill="#94a3b8")
            
            # Remove button (centered)
            btn_width = width - 40
            btn_height = 38
            btn_y = 360
            
            self.create_rounded_button(
                canvas, x=20, y=btn_y, width=btn_width, height=btn_height, radius=10,
                text="❌ Remove from Cart", text_color="white",
                bg_color="#ef4444", hover_color="#dc2626",
                command=lambda b=book: self.remove_from_cart(b)
            )
        
        card_canvas.bind("<Configure>", redraw_card)
        card_canvas.after(10, redraw_card)
    
    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
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
        button_shape = self.round_rectangle(canvas, x, y, x + width, y + height, radius=radius, fill=bg_color, outline="")
        button_text = canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color, font=("Helvetica", 10, "bold"))
        
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
    
    def remove_from_cart(self, book):
        result = messagebox.askyesno(
            "Remove from Cart",
            f"Remove '{book['name']}' from your cart?"
        )
        if result:
            user_email = self.current_user['email']
            self.db.remove_from_cart(user_email, book['id'])
            self.display_cart_items()
            messagebox.showinfo("Success", f"'{book['name']}' removed from cart!")