import tkinter as tk                          # agregado para gui
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
class Rols:
# funcion para la GUI
    def __init__(self, root,authenticated_username):

        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)
        

        self.title_label = tk.Label(root, text="Gestor de rol de usuarios", font=('Times', 20), fg="white", bg='#0D7FD8', padx=50)
        self.title_label.place(x=1, y=4)

        user_label = tk.Label(root, text="Usuario:", font=('Times', 15), fg="black", bg='#fcfcfc')
        user_label.place(x=50, y=50)

        self.user_entry = tk.Entry(root)
        self.user_entry.place(x=130, y=50)

        password_label = tk.Label(root, text="Password:", font=('Times', 15), fg="black", bg='#fcfcfc')
        password_label.place(x=30, y=80)

        self.pass_entry = tk.Entry(root)
        self.pass_entry.place(x=130, y=80)

        self.scan_button = tk.Button(root, text="Agregar", font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.register_user)
        self.scan_button.place(x=100, y=110)

        self.reset_button = tk.Button(root, text="Borrar", font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.delete_user)
        self.reset_button.place(x=200, y=110)


        self.back_button = tk.Button(root, text="Atras", font=('Times', 11, 'bold'), bg='#D8300D', bd=2, fg="#fff", command=self.back_button_clicked)
        self.back_button.place(x=290, y=135)


        self.result_label = tk.Label(root, text="", font=('Times', 10), fg="#0D7FD8", bg='#fff', pady=5)
        self.result_label.place(x=120, y=150)  

        self.text = tk.Text(root, height=20, width=41)
        self.text.place(x=1, y=180)
        self.display_usernames()
        scrollbar = tk.Scrollbar(root, command=self.text.yview)
        scrollbar.place(x=330, y=180, height=320) 
        self.text.config(yscrollcommand=scrollbar.set)


# funcion para mostrar los usuarios
    def display_usernames(self):
        usernames = self.db_manager.get_usernames()
        if usernames:
            self.text.insert(tk.END, f"Users:\n")
            for username in usernames:
                self.text.insert(tk.END, f"{username}\n")


# funcion para actualizar los usuarios
    def refresh_button_clicked(self):
        self.result_label.config(text="")
        self.text.delete("1.0", tk.END)
        self.display_usernames()


# funcion para restaurar la ventana 
    def restore_dashboard(self):
        self.dash_window.destroy()

# funcion para el boton de atras
    def back_button_clicked(self):
        from Dashboard import Dashboard  
        self.dash_window = tk.Toplevel(self.root)  
        self.root.withdraw()
        dash = Dashboard(self.dash_window,self.authenticated_username)
        self.dash_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

# funcion para el boton de crear usuario
    def register_user(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if username and password:
            self.db_manager.insert_user(username, password)
            self.result_label.config(text=f"Usuario {username} agregado con éxito")
            self.refresh_button_clicked()
        else:
            self.result_label.config(text="Por favor, complete los campos")

# funcion para el boton de borrar usuario
    def delete_user(self):
        username_to_delete = self.user_entry.get()

        if username_to_delete:
            if self.db_manager.user_exists(username_to_delete):
                self.db_manager.delete_user(username_to_delete)
                self.result_label.config(text=f"Usuario {username_to_delete} borrado con éxito")
                self.refresh_button_clicked()
            else:
                self.result_label.config(text="El usuario no existe.")
        else:
            self.result_label.config(text="Por favor, ingrese un nombre de usuario.")


#funcion que da inicio al loop de la GUI 
def main():
    root = tk.Tk()
    rol= Rols(root)
    root.mainloop()

if __name__ == "__main__":
    main()

