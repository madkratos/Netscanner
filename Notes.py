import tkinter as tk            # agregado para gui
from tkinter import filedialog  # agregado para cargar/guardar texto
from register import Register   # agregado para centrar la ventana
class Notes:
# funcion para la GUI
    def __init__(self, root,authenticated_username):
        self.root = root
        self.authenticated_username=authenticated_username
        self.root.geometry('350x500+800+200')
        root.title('NetScanner')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(width=0, height=0)


        self.title_label = tk.Label(root, text="Gestor de notas", font=('Times', 30), fg="white", bg='#0D7FD8', padx=50)
        self.title_label.place(x=1, y=4)

        self.scan_button = tk.Button(root, text="Guardar",font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.save_button_clicked)
        self.scan_button.place(x=20, y=65)

        self.reset_button = tk.Button(root, text="Borrar",font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.reset_button_clicked)
        self.reset_button.place(x=100, y=65)

        self.scan_button = tk.Button(root, text="Leer/edit",font=('Times', 11, 'bold'), bg='#0D7FD8', bd=2, fg="#fff", command=self.read_button_clicked)
        self.scan_button.place(x=170, y=65)

        self.back_button = tk.Button(root, text="Atras", font=('Times', 11, 'bold'), bg='#D8300D', bd=2, fg="#fff", command=self.back_button_clicked)
        self.back_button.place(x=290, y=80)

        
        self.title_label = tk.Label(root, text="Ingrese el texto que dese guardar en la plantilla blanca", font=('Times', 11), fg="#0D7FD8", bg='white')
        self.title_label.place(x=15, y=120)

        self.result_label = tk.Label(root, text="", font=('Times', 10), fg="#0D7FD8", bg='#fff', pady=5)
        self.result_label.place(x=90, y=90) 

        self.text = tk.Text(root, height=20, width=41)
        self.text.place(x=1, y=150)

        scrollbar = tk.Scrollbar(root, command=self.text.yview)
        scrollbar.place(x=330, y=180, height=320) 
        self.text.config(yscrollcommand=scrollbar.set)

# funcion para el boton de leer
    def read_button_clicked(self):
        self.result_label.config(text="")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Elija un lista",
            filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    saved_scans = file.read()
                    self.text.delete("1.0", tk.END)  
                    self.text.insert(tk.END, saved_scans)
            except FileNotFoundError:
                self.result_label.config(text="Lista no encontrada.")
        else:
            self.result_label.config(text="No se eligio la lista")

# funcion para el boton de borrar
    def reset_button_clicked(self):
        self.result_label.config(text="")
        self.text.delete("1.0", tk.END)

# funcion para el boton de guardado
    def save_button_clicked(self):
        lines = self.text.get("1.0", tk.END).splitlines()

        if not lines:
            self.result_label.config(text="No hay resultados para guardar.")
            return

        initial_dir = "C:/Users/*/Downloads"  

        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")])
        
        if file_path:
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(line + '\n')
            self.result_label.config(text="    Guardado")
        else:
            self.result_label.config(text="Operación cancelada.")


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

# funcion que da inicio al loop de la GUI 
def main():
    root = tk.Tk()
    note = Notes(root)
    root.mainloop()

if __name__ == "__main__":
    main()


