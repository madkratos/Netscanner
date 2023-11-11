import tkinter as tk
import customtkinter
import threading


class Dashboard:
    def __init__(self, root, authenticated_username):
        self.root = root
        self.authenticated_username = authenticated_username
        self.root.title('Dashboard')
        self.root.geometry('350x500+800+200')
        self.root.resizable(width=0, height=0)

        self.frame = customtkinter.CTkFrame(master=root, width=330, height=70, corner_radius=10)
        self.frame.place(x=10, y=10)

        self.title = customtkinter.CTkLabel(master=self.frame, text=f"Acerca de NetScanner", font=customtkinter.CTkFont(size=25))
        self.title.place(x=10, y=10)

        self.atras = customtkinter.CTkButton(master=self.frame, text="Atras", command=self.back_button_clicked,
                                             width=10, height=30, corner_radius=8, fg_color="#3D59AB")
        self.atras.place(x=275, y=10)

        self.net_text = tk.Text(root, height=20, width=42, bg="black", fg="#16FF00")
        self.net_text.place(x=4, y=90)

    def back_button_clicked(self):
        '''Función para el botón de atrás'''
        self.message("NetScanner: ",
                     "Compatible con Windows y detecta interfaces de red inalámbricas y cableadas. ",
                     "Identifica dispositivos que responden a paquetes ICMP \n\nSoporta todos los rangos CIDR \n\nEs capaz de guardar los "
                     "datos de las direcciones escaneadas y de leerlos \n\nCuenta con un gestor de tareas para poder realizar los escaneos."
                     "\n\nVersión del programa 3.1.")

    def message(self, title, message, description):
        self.net_text.delete(1.0, tk.END)
        self.net_text.insert(tk.END, title + "\n\n" + message + "\n\n" + description)

def main():
    root = customtkinter.CTk()
    dash = Dashboard(root, "admin")  # Reemplaza "admin" con el nombre de usuario autenticado
    root.mainloop()

if __name__ == "__main__":
    main()
