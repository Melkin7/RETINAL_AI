import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3, datetime, webbrowser
from model import main as predict_retinal_image

# ---------------- THEME SETTINGS ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Updated color scheme matching the React sample
BG_GRADIENT = ("#f4f6f9", "#ffffff")
HERO_GRADIENT = ("#2b7cff", "#3fc1c9")  # Blue gradient from sample
ACCENT = "#ff4d67"  # Red button color from sample
HOVER = "#e73c56"
SIDEBAR_COLOR = "#101828"  # Dark sidebar from sample
TITLE_FONT = ("Segoe UI", 36, "bold")
SUBTITLE_FONT = ("Segoe UI", 18)
TEXT_FONT = ("Segoe UI", 14)
BTN_FONT = ("Segoe UI", 16, "bold")
NAV_FONT = ("Segoe UI", 14)
CARD_FONT = ("Segoe UI", 16, "bold")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("dr_users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    name TEXT,
    email TEXT,
    user_type TEXT,
    created_at TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    report_type TEXT,
    prediction TEXT,
    status TEXT,
    date TEXT,
    image_path TEXT
)
""")
conn.commit()

# ---------------- APP CLASS ----------------
class RetinalAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Retinal AI - E-Health Management System")
        self.geometry("1400x900")
        self.resizable(True, True)
        self.configure(fg_color=BG_GRADIENT[0])

        self.current_user = None
        self.user_type = None

        # Main container
        self.container = ctk.CTkFrame(self, fg_color=BG_GRADIENT[0])
        self.container.pack(fill="both", expand=True)

        # Initialize frames
        self.frames = {}
        for Page in (HomePage, LoginPage, DashboardPage, UploadPage, ReportsPage):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(HomePage)

    def show_frame(self, page):
        self.frames[page].tkraise()

# ---------------- NAVBAR COMPONENT ----------------
class Navbar(ctk.CTkFrame):
    def __init__(self, parent, controller, show_login_dropdown=True):
        super().__init__(parent, fg_color="white", height=70)
        self.controller = controller
        
        # Logo
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(side="left", padx=40, pady=15)
        
        ctk.CTkLabel(logo_frame, text="🧠 Retinal AI", 
                     font=("Segoe UI", 20, "bold"), text_color="#333333").pack()
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(side="right", padx=40, pady=15)
        
        # Main nav buttons
        nav_buttons = [
            ("Features", lambda: self.show_features()),
            ("About", lambda: self.show_about()),
            ("Team", lambda: self.show_team())
        ]
        
        for text, command in nav_buttons:
            ctk.CTkButton(nav_frame, text=text, font=NAV_FONT, fg_color="transparent", 
                         text_color="#666666", hover_color="#f0f0f0", width=80,
                         command=command).pack(side="right", padx=10)
        
        if show_login_dropdown:
            # Login dropdown
            login_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
            login_frame.pack(side="right", padx=10)
            
            self.login_menu = ctk.CTkOptionMenu(login_frame, 
                                              values=["Patient Login", "Doctor Login", "Hospital Login", "Insurance Login"],
                                              command=self.handle_login_selection,
                                              font=NAV_FONT, fg_color=ACCENT, text_color="white",
                                              dropdown_fg_color="white", dropdown_text_color="#333333")
            self.login_menu.set("Login ▾")
            self.login_menu.pack()
    
    def handle_login_selection(self, choice):
        user_type = choice.split()[0].lower()  # Extract user type
        self.controller.user_type = user_type
        self.controller.show_frame(LoginPage)
    
    def show_features(self):
        messagebox.showinfo("Features", "AI Diagnosis • Medical Reports • Doctor Review • Insurance Ready")
    
    def show_about(self):
        messagebox.showinfo("About", "Retinal AI uses deep learning for early Diabetic Retinopathy detection.")
    
    def show_team(self):
        messagebox.showinfo("Team", "Built by medical AI specialists for better eye care.")

# ---------------- HOME PAGE (Hero + Features) ----------------
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_GRADIENT[0])
        self.controller = controller
        
        # Navbar
        navbar = Navbar(self, controller)
        navbar.pack(fill="x", pady=(0, 0))
        
        # Hero Section
        hero_frame = ctk.CTkFrame(self, fg_color=HERO_GRADIENT, height=400)
        hero_frame.pack(fill="x", padx=0, pady=0)
        
        hero_content = ctk.CTkFrame(hero_frame, fg_color="transparent")
        hero_content.pack(expand=True, pady=80, padx=80)
        
        ctk.CTkLabel(hero_content, text="AI-Powered Retinal Disease Detection", 
                     font=TITLE_FONT, text_color="white").pack(anchor="w")
        
        ctk.CTkLabel(hero_content, text="Early detection of Diabetic Retinopathy using deep learning.\nUpload retinal scans and get instant insights.", 
                     font=SUBTITLE_FONT, text_color="white").pack(anchor="w", pady=(20, 30))
        
        ctk.CTkButton(hero_content, text="Upload Retinal Image", font=BTN_FONT, 
                     fg_color=ACCENT, hover_color=HOVER, text_color="white",
                     width=220, height=50, corner_radius=25,
                     command=lambda: controller.show_frame(LoginPage)).pack(anchor="w")
        
        # Features Section (Cards)
        features_frame = ctk.CTkFrame(self, fg_color=BG_GRADIENT[0])
        features_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(features_frame, text="Our Features", 
                     font=("Segoe UI", 28, "bold"), text_color="#333333").pack(pady=(0, 30))
        
        # Feature cards grid
        cards_container = ctk.CTkFrame(features_frame, fg_color="transparent")
        cards_container.pack(expand=True)
        
        features = [
            ("🧠 AI Diagnosis", "Deep learning model detects DR stages accurately."),
            ("📊 Medical Reports", "Automatically generated and stored securely."),
            ("👨‍⚕️ Doctor Review", "Doctors can validate AI predictions."),
            ("🛡️ Insurance Ready", "Reports usable for insurance claims.")
        ]
        
        # Create 2x2 grid
        for i, (title, desc) in enumerate(features):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(cards_container, fg_color="white", 
                               border_width=1, border_color="#e0e0e0", 
                               corner_radius=10, width=300, height=150)
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=CARD_FONT, text_color="#333333").pack(pady=(20, 10))
            ctk.CTkLabel(card, text=desc, font=TEXT_FONT, text_color="#666666", 
                        wraplength=250).pack(pady=(0, 20), padx=20)

# ---------------- LOGIN PAGE ----------------
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller
        
        # Center container
        center_frame = ctk.CTkFrame(self, fg_color="white")
        center_frame.pack(expand=True)
        
        # Login card
        login_card = ctk.CTkFrame(center_frame, fg_color="white", border_width=2, border_color="#e0e0e0")
        login_card.pack(padx=50, pady=100)
        
        ctk.CTkLabel(login_card, text="Login", font=("Segoe UI", 32, "bold"), 
                     text_color="#333333").pack(pady=(40, 10))
        
        # User type indicator
        self.user_type_label = ctk.CTkLabel(login_card, text="Patient Login", 
                                           font=TEXT_FONT, text_color=ACCENT)
        self.user_type_label.pack(pady=(0, 20))
        
        # Login fields
        self.username = ctk.CTkEntry(login_card, placeholder_text="Username", 
                                   width=320, height=45, font=TEXT_FONT)
        self.username.pack(pady=10, padx=40)
        
        self.password = ctk.CTkEntry(login_card, placeholder_text="Password", show="*", 
                                   width=320, height=45, font=TEXT_FONT)
        self.password.pack(pady=10, padx=40)
        
        ctk.CTkButton(login_card, text="Sign In", fg_color=ACCENT, hover_color=HOVER,
                      font=BTN_FONT, width=320, height=50, corner_radius=25,
                      command=self.login).pack(pady=30, padx=40)
        
        ctk.CTkButton(login_card, text="← Back to Home", fg_color="transparent", 
                      text_color="#666666", hover_color="#f0f0f0", font=TEXT_FONT,
                      command=lambda: controller.show_frame(HomePage)).pack(pady=(0, 40))

    def login(self):
        u, p = self.username.get(), self.password.get()
        if not u or not p:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        # Simple authentication (in real app, use proper hashing)
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if cursor.fetchone():
            messagebox.showinfo("Welcome", f"Hello {u}!")
            self.controller.current_user = u
            self.controller.show_frame(DashboardPage)
        else:
            messagebox.showerror("Error", "Invalid credentials")

# ---------------- SIDEBAR COMPONENT ----------------
class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SIDEBAR_COLOR, width=220)
        self.controller = controller
        
        # Logo
        ctk.CTkLabel(self, text="🧠 Retinal AI", font=("Segoe UI", 18, "bold"), 
                     text_color="white").pack(pady=30)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", lambda: controller.show_frame(DashboardPage)),
            ("📋 Reports", lambda: controller.show_frame(ReportsPage)),
            ("🔍 Upload & Predict", lambda: controller.show_frame(UploadPage)),
            ("📅 Appointments", self.show_appointments),
            ("⚙️ Settings", self.show_settings),
            ("🚪 Logout", lambda: controller.show_frame(HomePage))
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(self, text=text, font=TEXT_FONT, fg_color="transparent",
                               text_color="white", hover_color="#2a3441", anchor="w",
                               height=45, command=command)
            btn.pack(fill="x", padx=10, pady=5)
    
    def show_appointments(self):
        messagebox.showinfo("Appointments", "Appointments feature coming soon!")
    
    def show_settings(self):
        messagebox.showinfo("Settings", "Settings panel coming soon!")

# ---------------- DASHBOARD PAGE ----------------
class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_GRADIENT[0])
        self.controller = controller
        
        # Main layout
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        sidebar = Sidebar(main_frame, controller)
        sidebar.pack(side="left", fill="y")
        
        # Main content
        content_frame = ctk.CTkFrame(main_frame, fg_color=BG_GRADIENT[0])
        content_frame.pack(side="right", fill="both", expand=True)
        
        # Header
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(header_frame, text="Good Afternoon 👋", 
                     font=("Segoe UI", 28, "bold"), text_color="#333333").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Here are your retinal health reports", 
                     font=TEXT_FONT, text_color="#666666").pack(anchor="w", pady=(5, 0))
        
        # Quick stats
        stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        stats = [
            ("Total Scans", "12", "#4CAF50"),
            ("Normal", "8", "#2196F3"),
            ("Abnormal", "4", "#FF9800"),
            ("Pending", "2", "#9C27B0")
        ]
        
        for title, value, color in stats:
            stat_card = ctk.CTkFrame(stats_frame, fg_color="white", 
                                   border_width=1, border_color="#e0e0e0")
            stat_card.pack(side="left", padx=10, pady=10, fill="x", expand=True)
            
            ctk.CTkLabel(stat_card, text=value, font=("Segoe UI", 24, "bold"), 
                        text_color=color).pack(pady=10)
            ctk.CTkLabel(stat_card, text=title, font=TEXT_FONT, 
                        text_color="#666666").pack(pady=(0, 10))

# ---------------- UPLOAD PAGE ----------------
class UploadPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_GRADIENT[0])
        self.controller = controller
        
        # Main layout
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        sidebar = Sidebar(main_frame, controller)
        sidebar.pack(side="left", fill="y")
        
        # Upload content
        content_frame = ctk.CTkFrame(main_frame, fg_color=BG_GRADIENT[0])
        content_frame.pack(side="right", fill="both", expand=True)
        
        # Upload box
        upload_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        upload_container.pack(expand=True)
        
        upload_box = ctk.CTkFrame(upload_container, fg_color="white", 
                                 border_width=2, border_color="#e0e0e0", 
                                 corner_radius=15, width=500, height=400)
        upload_box.pack(pady=50)
        
        ctk.CTkLabel(upload_box, text="Upload Retinal Image", 
                     font=("Segoe UI", 24, "bold"), text_color="#333333").pack(pady=30)
        
        # Upload preview
        self.preview_label = ctk.CTkLabel(upload_box, text="📁\nDrag & drop or click to select", 
                                         font=TEXT_FONT, text_color="#666666")
        self.preview_label.pack(pady=20)
        
        ctk.CTkButton(upload_box, text="Choose File", font=BTN_FONT, 
                     fg_color="#6c757d", hover_color="#5a6268", text_color="white",
                     width=200, height=45, command=self.upload_image).pack(pady=20)
        
        ctk.CTkButton(upload_box, text="Predict", font=BTN_FONT, 
                     fg_color=ACCENT, hover_color=HOVER, text_color="white",
                     width=200, height=45, command=self.predict).pack(pady=10)
        
        # Results
        self.result_label = ctk.CTkLabel(upload_box, text="", font=TEXT_FONT)
        self.result_label.pack(pady=20)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                img.thumbnail((200, 200))
                self.photo = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=self.photo, text="")
                self.image_path = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    
    def predict(self):
        if not hasattr(self, "image_path"):
            messagebox.showerror("Error", "Please upload an image first!")
            return

        try:
            severity, prediction, confidence = predict_retinal_image(
                self.image_path
            )

            status = "Normal" if severity == 0 else "Abnormal"
            status_color = "#4CAF50" if severity == 0 else "#f44336"

            self.result_label.configure(
                text=(
                    f"Model Prediction: {prediction}\n"
                    f"Model Probability: {confidence:.1%}\n"
                    f"Status: {status}\n"
                    "Experimental result — not a medical diagnosis."
                ),
                text_color=status_color
            )

            cursor.execute(
                "INSERT INTO reports "
                "(username, report_type, prediction, status, date) "
                "VALUES (?,?,?,?,?)",
                (
                    self.controller.current_user or "guest",
                    "Fundus Scan",
                    prediction,
                    status,
                    datetime.datetime.now().strftime("%d/%m/%Y"),
                ),
            )
            conn.commit()

        except Exception as e:
            messagebox.showerror(
                "Prediction Error",
                f"Could not run the model:\n{e}"
            )

# ---------------- REPORTS PAGE ----------------
class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_GRADIENT[0])
        self.controller = controller
        
        # Main layout
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        sidebar = Sidebar(main_frame, controller)
        sidebar.pack(side="left", fill="y")
        
        # Reports content
        content_frame = ctk.CTkFrame(main_frame, fg_color=BG_GRADIENT[0])
        content_frame.pack(side="right", fill="both", expand=True)
        
        # Header
        ctk.CTkLabel(content_frame, text="Medical Reports", 
                     font=("Segoe UI", 28, "bold"), text_color="#333333").pack(pady=30)
        
        # Reports table
        table_frame = ctk.CTkFrame(content_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Table headers
        headers = ["Report", "Date", "Prediction", "Status"]
        header_frame = ctk.CTkFrame(table_frame, fg_color="#f8f9fa")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        for header in headers:
            ctk.CTkLabel(header_frame, text=header, font=("Segoe UI", 14, "bold"), 
                        text_color="#333333").pack(side="left", expand=True)
        
        # Sample data rows
        sample_reports = [
            ("Fundus Scan", "17/03/2025", "Moderate DR", "Abnormal", "#f44336"),
            ("Fundus Scan", "10/01/2025", "No DR", "Normal", "#4CAF50"),
            ("Fundus Scan", "05/12/2024", "Mild DR", "Abnormal", "#FF9800"),
        ]
        
        for report, date, prediction, status, color in sample_reports:
            row_frame = ctk.CTkFrame(table_frame, fg_color="white")
            row_frame.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(row_frame, text=report, font=TEXT_FONT, text_color="#333333").pack(side="left", expand=True)
            ctk.CTkLabel(row_frame, text=date, font=TEXT_FONT, text_color="#333333").pack(side="left", expand=True)
            ctk.CTkLabel(row_frame, text=prediction, font=TEXT_FONT, text_color="#333333").pack(side="left", expand=True)
            ctk.CTkLabel(row_frame, text=status, font=TEXT_FONT, text_color=color).pack(side="left", expand=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app = RetinalAI()
    app.mainloop()
