import tkinter as tk
from tkinter import ttk

class StyledMessageBox:
    """Custom styled message boxes matching the admin dashboard UI"""
    
    # Color scheme
    APP_BG = "#0f172a"
    CARD_BG = "#1e293b"
    INPUT_BG = "#334155"
    TEXT_FG = "#e5e7eb"
    ACCENT_GREEN = "#43e97b"
    ACCENT_PURPLE = "#667eea"
    ERROR_RED = "#ef4444"
    WARNING_ORANGE = "#f59e0b"
    
    @staticmethod
    def show_error(parent, title, message):
        """Show error message dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x250")
        dialog.configure(bg=StyledMessageBox.CARD_BG)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"450x250+{x}+{y}")
        
        # Error icon and title
        header_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        header_frame.pack(pady=30)
        
        tk.Label(
            header_frame,
            text="⚠️",
            font=("Helvetica", 48),
            bg=StyledMessageBox.CARD_BG,
            fg=StyledMessageBox.ERROR_RED
        ).pack()
        
        tk.Label(
            header_frame,
            text=title,
            font=("Helvetica", 18, "bold"),
            fg=StyledMessageBox.ERROR_RED,
            bg=StyledMessageBox.CARD_BG
        ).pack(pady=(10, 0))
        
        # Message
        msg_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        msg_frame.pack(pady=10, padx=40)
        
        tk.Label(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            fg=StyledMessageBox.TEXT_FG,
            bg=StyledMessageBox.CARD_BG,
            wraplength=370,
            justify="center"
        ).pack()
        
        # OK Button
        btn_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        btn_frame.pack(pady=20)
        
        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            font=("Helvetica", 12, "bold"),
            bg=StyledMessageBox.ERROR_RED,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=10,
            command=dialog.destroy
        )
        ok_btn.pack()
        
        ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg="#dc2626"))
        ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=StyledMessageBox.ERROR_RED))
        
        dialog.wait_window()
    
    @staticmethod
    def show_success(parent, title, message):
        """Show success message dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x250")
        dialog.configure(bg=StyledMessageBox.CARD_BG)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"450x250+{x}+{y}")
        
        # Success icon and title
        header_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        header_frame.pack(pady=30)
        
        tk.Label(
            header_frame,
            text="✓",
            font=("Helvetica", 48, "bold"),
            bg=StyledMessageBox.CARD_BG,
            fg=StyledMessageBox.ACCENT_GREEN
        ).pack()
        
        tk.Label(
            header_frame,
            text=title,
            font=("Helvetica", 18, "bold"),
            fg=StyledMessageBox.ACCENT_GREEN,
            bg=StyledMessageBox.CARD_BG
        ).pack(pady=(10, 0))
        
        # Message
        msg_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        msg_frame.pack(pady=10, padx=40)
        
        tk.Label(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            fg=StyledMessageBox.TEXT_FG,
            bg=StyledMessageBox.CARD_BG,
            wraplength=370,
            justify="center"
        ).pack()
        
        # OK Button
        btn_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        btn_frame.pack(pady=20)
        
        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            font=("Helvetica", 12, "bold"),
            bg=StyledMessageBox.ACCENT_GREEN,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=10,
            command=dialog.destroy
        )
        ok_btn.pack()
        
        ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg="#38d46a"))
        ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=StyledMessageBox.ACCENT_GREEN))
        
        dialog.wait_window()
    
    @staticmethod
    def show_warning(parent, title, message):
        """Show warning message dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x250")
        dialog.configure(bg=StyledMessageBox.CARD_BG)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"450x250+{x}+{y}")
        
        # Warning icon and title
        header_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        header_frame.pack(pady=30)
        
        tk.Label(
            header_frame,
            text="⚡",
            font=("Helvetica", 48),
            bg=StyledMessageBox.CARD_BG,
            fg=StyledMessageBox.WARNING_ORANGE
        ).pack()
        
        tk.Label(
            header_frame,
            text=title,
            font=("Helvetica", 18, "bold"),
            fg=StyledMessageBox.WARNING_ORANGE,
            bg=StyledMessageBox.CARD_BG
        ).pack(pady=(10, 0))
        
        # Message
        msg_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        msg_frame.pack(pady=10, padx=40)
        
        tk.Label(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            fg=StyledMessageBox.TEXT_FG,
            bg=StyledMessageBox.CARD_BG,
            wraplength=370,
            justify="center"
        ).pack()
        
        # OK Button
        btn_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        btn_frame.pack(pady=20)
        
        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            font=("Helvetica", 12, "bold"),
            bg=StyledMessageBox.WARNING_ORANGE,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=10,
            command=dialog.destroy
        )
        ok_btn.pack()
        
        ok_btn.bind("<Enter>", lambda e: ok_btn.config(bg="#d97706"))
        ok_btn.bind("<Leave>", lambda e: ok_btn.config(bg=StyledMessageBox.WARNING_ORANGE))
        
        dialog.wait_window()
    
    @staticmethod
    def ask_yes_no(parent, title, message):
        """Show yes/no confirmation dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x350")  # Increased from 320 to 350
        dialog.configure(bg=StyledMessageBox.CARD_BG)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        result = {"value": False}
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)  # Changed from 320 to 350
        dialog.geometry(f"450x350+{x}+{y}")
        # Question icon and title
        header_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        header_frame.pack(pady=30)
        
        tk.Label(
            header_frame,
            text="❓",
            font=("Helvetica", 48),
            bg=StyledMessageBox.CARD_BG,
            fg=StyledMessageBox.ACCENT_PURPLE
        ).pack()
        
        tk.Label(
            header_frame,
            text=title,
            font=("Helvetica", 18, "bold"),
            fg=StyledMessageBox.TEXT_FG,
            bg=StyledMessageBox.CARD_BG
        ).pack(pady=(10, 0))
        
        # Message
        msg_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        msg_frame.pack(pady=10, padx=40)
        
        tk.Label(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            fg=StyledMessageBox.TEXT_FG,
            bg=StyledMessageBox.CARD_BG,
            wraplength=370,
            justify="center"
        ).pack()
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=StyledMessageBox.CARD_BG)
        btn_frame.pack(pady=30)  # Increased from 20 to 30
        
        def on_yes():
            result["value"] = True
            dialog.destroy()
        
        def on_no():
            result["value"] = False
            dialog.destroy()
        
        yes_btn = tk.Button(
            btn_frame,
            text="✓ Yes",
            font=("Helvetica", 12, "bold"),
            bg=StyledMessageBox.ACCENT_GREEN,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10,
            command=on_yes
        )
        yes_btn.pack(side="left", padx=10)
        
        no_btn = tk.Button(
            btn_frame,
            text="✕ No",
            font=("Helvetica", 12, "bold"),
            bg=StyledMessageBox.ERROR_RED,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10,
            command=on_no
        )
        no_btn.pack(side="left", padx=10)
        
        yes_btn.bind("<Enter>", lambda e: yes_btn.config(bg="#38d46a"))
        yes_btn.bind("<Leave>", lambda e: yes_btn.config(bg=StyledMessageBox.ACCENT_GREEN))
        no_btn.bind("<Enter>", lambda e: no_btn.config(bg="#dc2626"))
        no_btn.bind("<Leave>", lambda e: no_btn.config(bg=StyledMessageBox.ERROR_RED))
        
        dialog.focus_set()
        dialog.protocol("WM_DELETE_WINDOW", on_no)
        dialog.wait_window()
        return result["value"]