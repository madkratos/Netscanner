import customtkinter                          # agregado para la gui moderna
import tkinter as tk                          #Libreria para crear los diseños y la interfaz
import tkinter.messagebox                     #libreria para mensajes de error y demas
import sqlite3 
from DatabaseManager import DatabaseManager   # agregado modificar valores de la base de datos
from CTkMessagebox import CTkMessagebox       # agregado para el manejo de errores y caonfirmacion de acciones"pip install CTkMessagebox"

#Funcion para el centrado universal de la ventan
def center_window(root, width, height):
    '''Funcion para el centrado universal de la ventan'''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.resizable(width=0, height=0)

class Register:
# Función para para contruir la ventana con diseños desde la ventana login
    def __init__(self, root,authenticated_username):
        '''Función para para contruir la ventana con diseños desde la ventana login'''
        self.db_manager = DatabaseManager()
        self.db_manager.create_user_tables()
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.title('Registrar Usuario')
        width, height = 350, 500
        self.root.geometry(f'{width}x{height}')
        center_window(self.root, width, height)
        
        self.frame = customtkinter.CTkFrame(master=root,width=320,height=530,corner_radius=10)
        self.frame.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.title = customtkinter.CTkLabel(master=self.frame,text="Registrar Usuario",font=customtkinter.CTkFont(size=35))
        self.title.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.label_user = customtkinter.CTkLabel(master=self.frame,text="Usuario:",font=customtkinter.CTkFont(size=15))
        self.label_user.place(relx=0.16, rely=0.4, anchor=tkinter.CENTER)
        
        self.user_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10)
        self.user_entry.place(relx=0.5, rely=0.47, anchor=tkinter.CENTER)
    
        self.label_pass = customtkinter.CTkLabel(master=self.frame,text="Contraseña:",font=customtkinter.CTkFont(size=15))
        self.label_pass.place(relx=0.2, rely=0.57,anchor=tkinter.CENTER)

        self.pass_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10,show="*")
        self.pass_entry.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)

        self.label_pass = customtkinter.CTkLabel(master=self.frame,text="Confirmar contraseña:",font=customtkinter.CTkFont(size=15))
        self.label_pass.place(relx=0.32, rely=0.74,anchor=tkinter.CENTER)

        self.passv_entry = customtkinter.CTkEntry(master=self.frame,width=200,height=30,corner_radius=10,show="*")
        self.passv_entry.place(relx=0.5, rely=0.81, anchor=tkinter.CENTER)

        self.login = customtkinter.CTkButton(master =self.frame, text="Registrar Usuario", command=self.register_user)
        self.login.place(x=160, y=490, anchor=customtkinter.CENTER)


        self.cerrar = customtkinter.CTkButton(master =root, text="Volver",fg_color="#3D59AB", command=self.back_button_clicked)
        self.cerrar.place(x=175, y=460, anchor=customtkinter.CENTER)

        self.root.bind("<Return>", lambda event: self.register_user())
        self.root.bind("<Escape>", lambda event: self.back_button_clicked())

#Funcion para eliminar la ventana registrarse al presionar el boton volver
    def restore_dashboard(self):
        '''Funcion para eliminar la ventana registrarse al presionar el boton volver'''
        self.login_window.destroy()
    
#Funcion para volver a inicio de sesion al presionar el botos volver 
    def back_button_clicked(self):
        '''Funcion para volver a inicio de sesion al presionar el botos volver '''
        from Rols import Rols  
        self.login_window = customtkinter.CTkToplevel(self.root)
        self.root.withdraw()
        self.login_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)
        customtkinter.set_appearance_mode("Dark") 
        customtkinter.set_default_color_theme("blue")
        rol = Rols(self.login_window,self.authenticated_username)

        
# funcion para el boton de crear usuario
    def register_user(self):
        '''funcion para el boton de crear usuario'''
        username = self.user_entry.get()
        password = self.pass_entry.get()
        passwordv = self.passv_entry.get()
        if username and passwordv and password:
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            usuario_existente = cursor.fetchone()
            if usuario_existente:
                conn.close()
                self.user_entry.delete(0, 'end')
                self.passv_entry.delete(0, 'end')
                self.pass_entry.delete(0, 'end')
                CTkMessagebox(title="Error", message="El usuario ingresado ya existe.",icon="cancel", option_1="Aceptar")
            elif password == passwordv:
                if username:
                        option= CTkMessagebox(title='Confirme la operacion', message='¿Esta seguro de querer agregar este usuario?',icon="question",option_2="Si", option_1="No") 
                        option = option.get()
                if option == "Si":
                    self.db_manager.insert_user(username, password)
                    self.user_entry.delete(0, 'end')
                    self.passv_entry.delete(0, 'end')
                    self.pass_entry.delete(0, 'end')
                    CTkMessagebox(title="Aprobado", message="Usuario registrado con exito.",icon="check", option_1="Aceptar")
                else:
                    CTkMessagebox(title="Operacion cancelada", message="Operacion cancelada.",icon="cancel", option_1="Aceptar")
            else:
                self.user_entry.delete(0, 'end')
                self.passv_entry.delete(0, 'end')
                self.pass_entry.delete(0, 'end')
                CTkMessagebox(title="Error", message="Las contraseñas no son iguales.",icon="cancel", option_1="Aceptar")
        else: 
            CTkMessagebox(title="Error", message="No has ingresado nada en los campos.",icon="cancel", option_1="Aceptar")

# funcion principal
def main():
    '''funcion principal'''
    root = customtkinter.CTk()
    register = Register(root)
    root.mainloop()

if __name__ == "__main__":
    main()
