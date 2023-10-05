import tkinter as tk                 #Libreria para crear los diseños y la interfaz
import sqlite3                       #libreria para manejar base de dato
import tkinter.messagebox            #libreria para mensajes de error y demas
from DatabaseManager import DatabaseManager #Libreria para usar para poder manipular la base de datos
from tkinter.font import BOLD        #libreria para poner en negrita la fuente de la interfaz

class Register:
# Función para para contruir la ventana con diseños desde la ventana login
    def __init__(self, root):
        self.db_manager = DatabaseManager()
        self.root = root
        self.root.title('Registrar Usuario.')
        self.root.geometry('350x500+800+200')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)

        #frame_form
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form
        
        #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Registrar Usuario",font=('Times', 30), fg="white",bg='#0D7FD8',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill 
        frame_form_fill = tk.Frame(frame_form,height = 30,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        user_label = tk.Label(frame_form_fill, text="Usuario:", font=('Times', 14) ,fg="black",bg='#fcfcfc', anchor="w")
        user_label.pack(fill=tk.X, padx=20,pady=5)
        self.user_entry = tk.Entry(frame_form_fill, font=('Times', 16))
        self.user_entry.pack(fill=tk.X, padx=20,pady=5)

        correo_label = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 14) ,fg="black",bg='#fcfcfc', anchor="w")
        correo_label.pack(fill=tk.X, padx=20,pady=5)
        self.pass_entry = tk.Entry(frame_form_fill, font=('Times', 16))
        self.pass_entry.pack(fill=tk.X, padx=20,pady=5)
        self.pass_entry.config(show="*")

        password_label = tk.Label(frame_form_fill, text="Confirmar contraseña:", font=('Times', 16),fg="black",bg='#fcfcfc' , anchor="w")
        password_label.pack(fill=tk.X, padx=20,pady=5)
        self.password_entry = tk.Entry(frame_form_fill, font=('Times', 14))
        self.password_entry.pack(fill=tk.X, padx=20,pady=5)
        self.password_entry.config(show="*")

        register = tk.Button(frame_form_fill,text="Registrase",font=('Times', 15,BOLD),bg='#0D7FD8', bd=2,fg="#fff", command=self.register_user)
        register.pack(fill=tk.X, padx=20,pady=5)

        volver = tk.Button(frame_form_fill,text="volver",font=('Times', 15,BOLD),bg='#fff', bd=2,fg="black",command=self.logout_button_clicked)
        volver.pack(fill=tk.X, padx=20,pady=5)    
       
        self.root.bind("<Return>", lambda event: self.register_user())
        self.root.bind("<Escape>", lambda event: self.logout_button_clicked())

#Funcion para eliminar la ventana registrarse al presionar el boton volver
    def restore_dashboard(self):
        self.dash_window.destroy()
    
#Funcion para volver a inicio de sesion al presionar el botos volver 
    def logout_button_clicked(self):
        from Login import Login  
        self.login_window = tk.Toplevel(self.root)
        login = Login(self.login_window)
        self.root.withdraw()
        self.login_window.protocol("WM_DELETE_WINDOW",self.restore_dashboard)

#Funcion para agregar el usuario a la base de datos
    def register_user(self): 
        username = self.user_entry.get()
        password = self.password_entry.get()
        passwordv = self.pass_entry.get()
        if username and passwordv and password:
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            usuario_existente = cursor.fetchone()
            if usuario_existente:
                conn.close()
                tkinter.messagebox.showerror(title="error", message="El usuario ingresado ya existe.")
            elif password == passwordv:
                if username:
                    self.db_manager.insert_user(username, password)
                    tkinter.messagebox.showinfo(title="Registro exitoso.", message="Usuario registrado con exito.")
            else:
                tkinter.messagebox.showerror(title="error", message="Las contraseñas no son iguales.")
        else: 
            tkinter.messagebox.showerror(title="error", message="No has ingresado todos los campos.")

    

def main():
    root = tk.Tk()
    register = Register(root)
    root.mainloop()

if __name__ == "__main__":
    main()
