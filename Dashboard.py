import tkinter as tk  # agregado para gui

class Dashboard:
    def __init__(self, root,authenticated_username):
        self.root = root
        self.authenticated_username = authenticated_username
        self.root.title('Dashboard.')
        self.root.geometry('350x500+800+200')
        self.root.config(bg='#0D7FD8')
        self.root.resizable(width=0, height=0)

        self.title_label = tk.Label(root, text=f"Hola {self.authenticated_username}!", font=('Times', 20), fg="white", bg='#0D7FD8', pady=20)
        self.title_label.place(x=10, y=10)

        self.logout_button = tk.Button(root, text="Logout", font=('Times', 13, 'bold'), bg='#D8300D', bd=2, fg="#fff", command=self.logout_button_clicked)
        self.logout_button.place(x=260, y=10)

        self.scan_button = tk.Button(root, text="Realizar Scan", font=('Times', 13, 'bold'), bg='#fff', bd=2, fg="#0D7FD8", command=self.scan_button_clicked)
        self.scan_button.place(x=6, y=90)

        self.pause_button = tk.Button(root, text="Rol de Usuarios", font=('Times', 13, 'bold'),bg='#fff', bd=2, fg="#0D7FD8", command=self.usuario_button_clicked)
        self.pause_button.place(x=127, y=90)

        self.reset_button = tk.Button(root, text="Notas", font=('Times', 13, 'bold'), bg='#fff', bd=2, fg="#0D7FD8", command=self.notas_button_clicked)
        self.reset_button.place(x=270, y=90)

        self.net_text = tk.Text(root, height=20, width=42)
        self.net_text.place(x=4, y=160)

        self.message("Bienvenido a ",
                      """  _   _          _   
 | \ | |        | |  
 |  \| |   ___  | |_ 
 | . ` |  / _ \ | __|
 | |\  | |  __/ | |_ 
 |_| \_|  \___|  \__|
 _____                                 
/ ____|                                
| (___   ___ __ _ _ __  _ __   ___ _ __ 
 \___ \ / __/ _` | '_ \| '_ \ / _ | '__|
 ____) | (_| (_| | | | | | | |  __| |   
|_____/ \___\__,_|_| |_|_| |_|\___|_|   ""","\nNetScanner es un programa para el escaneo de una red por medio de paquetes de ping, es capaz de manejar rangos de ip en  formato CIDR (classless inter-domain routing) y cubre todos los rangos posibles")
        

# funcion para el boton de escaneo abre al funcion de escaneo principal
    def scan_button_clicked(self):
        from NetScanner import NetScanner  
        self.scanner_window = tk.Toplevel(self.root)
        scanner = NetScanner(self.scanner_window,self.authenticated_username)
        self.root.withdraw()
        self.scanner_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

# funcion para restaurar la ventana 
    def restore_dashboard(self):
        self.scanner_window.destroy()
        self.login_window.destroy()


# funcion para el boton de logout
    def logout_button_clicked(self):
        from Login import Login  
        self.login_window = tk.Toplevel(self.root)
        login = Login(self.login_window)
        self.root.withdraw()
        self.login_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

# funcion para el mensaje sobre el programa
    def message(self,*lines):
            for line in lines:
                self.net_text.insert(tk.END, line + "\n")

# funcion para el boton de escan guardados
    def scans_hechos_button_clicked(self):
            from History import History  
            self.history_window = tk.Toplevel(self.root)
            history = History(self.history_window,self.authenticated_username)
            self.root.withdraw()
            self.history_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

# funcion para el boton de rol de usuarios
    def usuario_button_clicked(self):
            from Rols import Rols  
            self.rol_window = tk.Toplevel(self.root)
            rol = Rols(self.rol_window,self.authenticated_username)
            self.root.withdraw()
            self.rol_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

# funcion para el boton de notas
    def notas_button_clicked(self):
        from Notes import Notes  
        self.note_window = tk.Toplevel(self.root)
        note = Notes(self.note_window,self.authenticated_username)
        self.root.withdraw()
        self.note_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

# funcion para la ventana principal de dashboard
def main():
    root = tk.Tk()
    dash= Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()







