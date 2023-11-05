import customtkinter                          # agregado para la gui moderna "pip install customtkinter"
import tkinter as tk                          # agregado para gui
import sys                                    # agregado llamada al sistema
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
from tkinter.font import BOLD
import tkinter.messagebox                     # agregado para mensajes de confirmación 
from CTkMessagebox import CTkMessagebox       # agregado para el manejo de errores y caonfirmacion de acciones"pip install CTkMessagebox"

customtkinter.set_appearance_mode("Dark")           #aplica el color del tema a la ventana
customtkinter.set_default_color_theme("blue")       #aplica el color del tema a la ventana

#Funcion para el centrado universal de la ventan
def center_window(root, width, height):
    '''Funcion para el centrado universal de la ventan'''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.resizable(width=0, height=0)


class Login:
#funcion de la GUI 
    def __init__(self, root):
        ''' funcion de la GUI '''
        self.db_manager = DatabaseManager()
        self.root = root
        root.title('NetScanner')
        width, height = 350, 500
        self.root.geometry(f'{width}x{height}')
        center_window(self.root, width, height)


        self.frame = customtkinter.CTkFrame(master=root,width=320,height=500,corner_radius=10)
        self.frame.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.title = customtkinter.CTkLabel(master=self.frame,text="Inicio de Sesion",font=customtkinter.CTkFont(size=35))
        self.title.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.label_user = customtkinter.CTkLabel(master=self.frame,text="Usuario:",font=customtkinter.CTkFont(size=15))
        self.label_user.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)
        
        self.username_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10)
        self.username_entry.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    
        self.label_pass = customtkinter.CTkLabel(master=self.frame,text="Contraseña:",font=customtkinter.CTkFont(size=15))
        self.label_pass.place(relx=0.2, rely=0.7,anchor=tkinter.CENTER)

        self.password_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10,show="*")
        self.password_entry.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        self.login = customtkinter.CTkButton(master =self.frame, text="Iniciar sesion", command=self.authenticate_user)
        self.login.place(x=160, y=460, anchor=customtkinter.CENTER)


        self.cerrar = customtkinter.CTkButton(master =root, text="Cerrar",fg_color="#3D59AB", command=self.exit_program)
        self.cerrar.place(x=175, y=450, anchor=customtkinter.CENTER)

        self.root.bind("<Return>", lambda event: self.authenticate_user())

# funcion para validar usuario en la base de datos
    def authenticate_user(self):
        ''' funcion para validar usuario en la base de datos'''
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if self.db_manager.authenticate_user(username,password):
                self.authenticated_username = username
                if username == "admin":
                    self.open_dashboard()
                else:
                     self.open_dashboard_user()
            else:
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                CTkMessagebox(title="Error", message="El usuario o contraseña es incorrecto.",icon="cancel", option_1="Aceptar")
        else:
            CTkMessagebox(title="Error", message="No has ingresado nada en los campos.",icon="cancel", option_1="Aceptar")

    
# funcion para el boton de cerrar
    def exit_program(self):
        '''funcion para el boton de cerrar'''
        self.root.destroy()
        if hasattr(self, 'dash_window'):
            self.dash_window.destroy()
        sys.exit(0)


# funcion para crear la ventana del llamado dashboard de usuario
    def open_dashboard_user(self):
        '''funcion para crear la ventana del llamado dashboard de usuario'''
        import customtkinter  
        from DashboardUser import DashboardUser  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.exit_program)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash_user = DashboardUser(self.dash_window,self.authenticated_username)

# funcion para crear la ventana del llamado dashboard
    def open_dashboard(self):
        '''funcion para crear la ventana del llamado dashboard'''
        import customtkinter  
        from Dashboard import Dashboard  
        self.dash_window = customtkinter.CTkToplevel(self.root)  
        self.root.withdraw()
        self.dash_window.protocol("WM_DELETE_WINDOW", self.exit_program)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        dash = Dashboard(self.dash_window,self.authenticated_username)


    def set_username(self, username):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)

    def set_password(self, password):
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
# funcion para la ventana principal de login
def main():
    ''' funcion para la ventana principal de login'''
    root = customtkinter.CTk()
    login = Login(root)
    root.mainloop()

if __name__ == "__main__":
    main()




