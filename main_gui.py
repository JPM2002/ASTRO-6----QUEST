import customtkinter as ctk
import subprocess
import sys

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("800x350")
        self.resizable(False, False)

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=50, padx=100, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Astronomy", font=("Roboto Medium", 16))
        self.title_label.pack(pady=8)

        self.run_button = ctk.CTkButton(self.main_frame, text="Run", command=self.run_command, corner_radius=10, height=40)
        self.run_button.pack(pady=10, fill="x", padx=20)

        #self.settings_button = ctk.CTkButton(self.main_frame, text="Settings", command=self.settings_command, corner_radius=10, height=40)
        #self.settings_button.pack(pady=10, fill="x", padx=20)
        #the code was remove due to not having enough time to implement the GUI design from ligth mode to dark mode... dark mode is superior

        self.exit_button = ctk.CTkButton(self.main_frame, text="Exit", command=self.destroy, corner_radius=10, height=40)
        self.exit_button.pack(pady=10, fill="x", padx=20)

    def run_command(self):
        subprocess.Popen([sys.executable, 'pygame_simulation.py'])

    def settings_command(self):
        print("Open settings")

if __name__ == "__main__":
    app = App()
    app.mainloop()
