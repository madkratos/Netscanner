import customtkinter                          # agregado para la gui moderna
import tkinter as tk                          # agregado para gui
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
import tkinter.messagebox                     # agregado para el manejo de errores y caonfirmacion de acciones
from CTkMessagebox import CTkMessagebox       # agregado para el manejo de errores y caonfirmacion de acciones"pip install CTkMessagebox"

class Rols:
# funcion para la GUI
    def __init__(self, root,authenticated_username):
        self.db_manager = DatabaseManager()
        self.db_manager.create_user_tables()
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.resizable(width=0, height=0)


        self.title_label =customtkinter.CTkLabel(master=root, text="Gestor de rol de usuarios", font=customtkinter.CTkFont(size=30))
        self.title_label.place(x=10, y=4)

        self.user_label = customtkinter.CTkLabel(master=root,text="Usuario:",font=customtkinter.CTkFont(size=15))
        self.user_label.place(x=65, y=65)

        self.user_entry = customtkinter.CTkEntry(master=root,width=100,height=20,corner_radius=8)
        self.user_entry.place(x=130, y=70)

        self.add_button = customtkinter.CTkButton(master =root, text="Agregar",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.open_register)
        self.add_button.place(x=110, y=120)

        self.delete_button = customtkinter.CTkButton(master =root, text="Borrar",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.delete_user)
        self.delete_button.place(x=180, y=120)

        self.back_button = customtkinter.CTkButton(master =root, text="Atras",fg_color="#3D59AB",font=customtkinter.CTkFont(size=13),width=20,height=10,corner_radius=8, command=self.back_button_clicked)
        self.back_button.place(x=290, y=135)

        self.result_label = customtkinter.CTkLabel(master=root,text="",font=customtkinter.CTkFont(size=10), pady=5)
        self.result_label.place(x=120, y=150)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=root, width=310, height=300)
        self.scrollable_frame.place(x=10, y=180)

        self.text = tk.Text(master=self.scrollable_frame, height=19, width=41,bg="#3B3B3B",fg="white")
        self.text.pack()
        
        self.display_usernames()


#funcion para crear ventana de registro de usuario
    def open_register(self):
        from Register import Register
        self.register_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.register_window.protocol("WM_DELETE_WINDOW", self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        register = Register(self.register_window,self.authenticated_username)

# funcion para mostrar los usuarios
    def display_usernames(self):
        usernames = self.db_manager.get_usernames()
        if usernames:
            self.text.insert(tk.END, f"Users:\n")
            for username in usernames:
                self.text.insert(tk.END, f"{username}\n")


# funcion para actualizar los usuarios
    def refresh_button_clicked(self):
        self.result_label.configure(text="")
        self.text.delete("1.0", tk.END)
        self.display_usernames()


# funcion para restaurar la ventana 
    def restore_dashboard(self):
        self.dash_window.destroy()

# funcion para el boton de atras
    def back_button_clicked(self):
        if self.authenticated_username == "admin":
            self.open_dashboard()
        else:
            self.open_dashboard_user()


# funcion para crear la ventana del llamado dashboard de usuario
    def open_dashboard_user(self):
        import customtkinter  
        from DashboardUser import DashboardUser  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash_user = DashboardUser(self.dash_window,self.authenticated_username)

# funcion para crear la ventana del llamado dashboard
    def open_dashboard(self):
        import customtkinter  
        from Dashboard import Dashboard  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash = Dashboard(self.dash_window,self.authenticated_username)


# funcion para el boton de crear usuario
    def register_user(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if username and password:
            self.db_manager.insert_user(username, password)
            self.result_label.configure(text=f"Usuario {username} agregado con éxito")
            self.refresh_button_clicked()
        else:
            self.result_label.configure(text="Por favor, complete los campos")

# funcion para el boton de borrar usuario
    def delete_user(self):
        username_to_delete = self.user_entry.get()

        if username_to_delete:
            if self.db_manager.user_exists(username_to_delete):
                option= CTkMessagebox(title='Confirme la operacion', message='Esta seguro de querer eliminar este usuario?',icon="question",option_2="Si", option_1="No") 
                option = option.get()
                if option =="Si":
                    self.db_manager.delete_user(username_to_delete)
                    CTkMessagebox(message="Usuario borrado con éxito",icon="check", option_1="Aceptar")
                    self.result_label.configure(text=f"Usuario {username_to_delete} borrado con éxito")
                    self.refresh_button_clicked()
                    self.user_entry.delete(0, tk.END)
                    self.user_entry.focus()
                else:
                    CTkMessagebox(title="Operacion cancelada.", message="Usuario no eliminado.")
                    #tkinter.messagebox.showinfo(title="Operacion cancelada.", message="Usuario no eliminado.")
                    self.user_entry.delete(0, tk.END)
                    self.user_entry.focus()
            else:
                self.result_label.configure(text="El usuario no existe.")
                self.user_entry.delete(0, tk.END)
                self.user_entry.focus()
        else:
            self.result_label.configure(text="Por favor, ingrese un nombre de usuario.")


#funcion que da inicio al loop de la GUI 
def main():
    root = customtkinter.CTk()
    rol= Rols(root)
    root.mainloop()

if __name__ == "__main__":
    main()

