import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinter.font import Font

from file_operations import (
    list_files,
    open_file,
    delete_file,
    create_file
)
from utils import build_full_path


class FileManagerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📁 Simple File Manager")
        self.root.geometry("800x600")
        
        # Configure theme colors
        self.bg_color = "#f0f0f0"
        self.btn_color = "#4a6fa5"
        self.btn_hover = "#3a5a8c"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Set minimum window size
        self.root.minsize(600, 400)
        
        self.current_folder = ""
        
        # Create custom fonts
        self.title_font = Font(family="Arial", size=16, weight="bold")
        self.label_font = Font(family="Arial", size=10)
        self.btn_font = Font(family="Arial", size=10, weight="bold")
        
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.root.bind('<Delete>', lambda e: self.delete_selected_file())
        self.root.bind('<Control-o>', lambda e: self.open_folder())
        self.root.bind('<Control-n>', lambda e: self.create_new_file())
        self.root.bind('<Double-Button-1>', lambda e: self.open_selected_file())
        self.root.bind('<F5>', lambda e: self.refresh_file_list())

    def create_widgets(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with current folder display
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="📁 Simple File Manager", 
                font=self.title_font, bg=self.bg_color, fg=self.text_color).pack(anchor=tk.W)
        
        # Current folder display
        self.folder_label = tk.Label(header_frame, text="No folder selected", 
                                     font=self.label_font, bg=self.bg_color, 
                                     fg="#666666", anchor=tk.W)
        self.folder_label.pack(fill=tk.X, pady=(5, 0))
        
        # Button toolbar with modern styling
        toolbar_frame = tk.Frame(main_container, bg=self.bg_color)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons = [
            ("📂 Open Folder", self.open_folder, "Ctrl+O"),
            ("📄 Open File", self.open_selected_file, "Double-click"),
            ("🗑️ Delete File", self.delete_selected_file, "Del"),
            ("➕ Create File", self.create_new_file, "Ctrl+N"),
            ("🔄 Refresh", self.refresh_file_list, "F5")
        ]
        
        for i, (text, command, shortcut) in enumerate(buttons):
            btn_frame = tk.Frame(toolbar_frame, bg=self.bg_color)
            btn_frame.pack(side=tk.LEFT, padx=2)
            
            btn = tk.Button(btn_frame, text=text, command=command,
                           font=self.btn_font, bg=self.btn_color, fg="white",
                           relief=tk.RAISED, borderwidth=1, padx=15, pady=8,
                           cursor="hand2")
            btn.pack()
            
            # Add shortcut hint
            tk.Label(btn_frame, text=shortcut, font=("Arial", 7), 
                    bg=self.bg_color, fg="#666666").pack()
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
        
        # File list with scrollbar
        list_frame = tk.Frame(main_container, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create Listbox with better styling
        self.file_list = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg="white",
            fg=self.text_color,
            selectbackground="#e0e0e0",
            selectforeground=self.text_color,
            font=("Courier New", 10),
            relief=tk.SUNKEN,
            borderwidth=2,
            height=20
        )
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.file_list.yview)
        
        # Status bar
        self.status_bar = tk.Label(main_container, text="Ready", 
                                  bg="#e0e0e0", fg="#666666", 
                                  anchor=tk.W, relief=tk.SUNKEN, borderwidth=1)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Footer info
        footer_frame = tk.Frame(main_container, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(footer_frame, text=f"Name: ADITYA BHARDWAJ | Section: D2 | Roll No: 07", 
                font=("Arial", 9), bg=self.bg_color, fg="#888888").pack(anchor=tk.W)
        tk.Label(footer_frame, text="Course: B.TECH | Branch: CSE", 
                font=("Arial", 9), bg=self.bg_color, fg="#888888").pack(anchor=tk.W)

    def on_enter(self, event, button):
        button.config(bg=self.btn_hover)

    def on_leave(self, event, button):
        button.config(bg=self.btn_color)

    def open_folder(self):
        folder = filedialog.askdirectory(title="Select a folder")
        if folder:
            self.current_folder = folder
            self.folder_label.config(text=f"📂 {folder}")
            self.refresh_file_list()
            self.update_status(f"Opened folder: {folder}")

    def refresh_file_list(self):
        if not self.current_folder:
            self.update_status("No folder selected")
            return
            
        self.file_list.delete(0, tk.END)
        try:
            files = list_files(self.current_folder)
            if not files:
                self.file_list.insert(tk.END, "📁 (Empty folder)")
            else:
                for file in files:
                    # Add icon based on file type
                    icon = "📄" if "." in file else "📁"
                    self.file_list.insert(tk.END, f"{icon} {file}")
            
            count = len(files)
            self.update_status(f"Found {count} item(s)")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read folder: {str(e)}")
            self.update_status("Error reading folder")

    def open_selected_file(self):
        selected = self.file_list.curselection()
        if selected:
            file_name = self.file_list.get(selected)
            # Remove icon from filename
            if " " in file_name:
                file_name = file_name.split(" ", 1)[1]
            
            full_path = build_full_path(self.current_folder, file_name)
            try:
                open_file(full_path)
                self.update_status(f"Opened: {file_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
                self.update_status(f"Failed to open: {file_name}")

    def delete_selected_file(self):
        selected = self.file_list.curselection()
        if selected:
            file_name = self.file_list.get(selected)
            # Remove icon from filename
            if " " in file_name:
                file_name = file_name.split(" ", 1)[1]
            
            full_path = build_full_path(self.current_folder, file_name)

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{file_name}'?\n\nThis action cannot be undone.",
                icon=messagebox.WARNING
            )

            if confirm:
                try:
                    delete_file(full_path)
                    self.refresh_file_list()
                    self.update_status(f"Deleted: {file_name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file: {str(e)}")
                    self.update_status(f"Failed to delete: {file_name}")

    def create_new_file(self):
        if not self.current_folder:
            messagebox.showwarning("No Folder", "Please open a folder first")
            return

        file_name = simpledialog.askstring(
            "Create File",
            "Enter file name:",
            parent=self.root
        )

        if file_name:
            if not file_name.strip():
                messagebox.showwarning("Invalid Name", "File name cannot be empty")
                return
                
            full_path = build_full_path(self.current_folder, file_name)

            if os.path.exists(full_path):
                messagebox.showerror("Error", f"'{file_name}' already exists")
            else:
                try:
                    create_file(full_path)
                    self.refresh_file_list()
                    self.update_status(f"Created: {file_name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create file: {str(e)}")
                    self.update_status(f"Failed to create: {file_name}")

    def update_status(self, message):
        self.status_bar.config(text=message)

    def run(self):
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()


# Alternative modern version using ttk for native OS look
class ModernFileManagerUI(FileManagerUI):
    def __init__(self):
        super().__init__()
        
    def create_widgets(self):
        # Use ttk for modern OS-native look
        style = ttk.Style()
        style.theme_use('clam')  # You can try 'vista', 'xpnative', 'clam'
        
        # Main container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header_frame, text="📁 Simple File Manager", 
                 font=self.title_font).pack(anchor=tk.W)
        
        # Current folder display
        self.folder_label = ttk.Label(header_frame, text="No folder selected", 
                                     font=self.label_font, foreground="gray")
        self.folder_label.pack(fill=tk.X, pady=(5, 0))
        
        # Button toolbar
        toolbar_frame = ttk.Frame(main_container)
        toolbar_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons = [
            ("📂 Open Folder", self.open_folder),
            ("📄 Open File", self.open_selected_file),
            ("🗑️ Delete File", self.delete_selected_file),
            ("➕ Create File", self.create_new_file),
            ("🔄 Refresh", self.refresh_file_list)
        ]
        
        for text, command in buttons:
            ttk.Button(toolbar_frame, text=text, command=command).pack(side=tk.LEFT, padx=2)
        
        # File list with treeview (alternative to listbox)
        list_frame = ttk.Frame(main_container)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for files
        columns = ('name', 'type', 'size')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        # Define headings
        self.tree.heading('#0', text='Icon')
        self.tree.heading('name', text='Name')
        self.tree.heading('type', text='Type')
        self.tree.heading('size', text='Size')
        
        # Configure column widths
        self.tree.column('#0', width=50)
        self.tree.column('name', width=300)
        self.tree.column('type', width=100)
        self.tree.column('size', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_bar = ttk.Label(main_container, text="Ready", 
                                   relief=tk.SUNKEN, padding=(5, 2))
        self.status_bar.pack(fill=tk.X, pady=(15, 0))
        
        # Override refresh method for treeview
        self.refresh_file_list = self.refresh_treeview

    def refresh_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.current_folder:
            self.update_status("No folder selected")
            return
            
        try:
            files = list_files(self.current_folder)
            for file in files:
                # Determine file type icon
                icon = "📄" if "." in file else "📁"
                file_type = "File" if "." in file else "Folder"
                size = os.path.getsize(build_full_path(self.current_folder, file)) if "." in file else "-"
                
                self.tree.insert('', 'end', text=icon, values=(file, file_type, size))
            
            count = len(files)
            self.update_status(f"Found {count} item(s)")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read folder: {str(e)}")
            self.update_status("Error reading folder")


# Run the application
if __name__ == "__main__":
    app = FileManagerUI()  # Use ModernFileManagerUI() for treeview version
    app.run()