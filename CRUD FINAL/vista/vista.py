import tkinter as tk
from tkinter import ttk, messagebox
import modelo.consultas_dao as consulta

class Frame(tk.Frame):  
    def __init__(self, root=None):    
        super().__init__(root, width=480, height=380)
        self.root = root    
        self.pack()
        self.id_peli = None
        self.fondo = "#FBFCDD"   
        self.config(bg=self.fondo)

        self.label_form()
        self.input_form()
        self.botones_principales()
        self.mostrar_tabla()

    def label_form(self):    
        tk.Label(self, text="Nombre:", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Duración:", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="Género:", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="Actor Principal:", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text="Director:", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=4, column=0, padx=10, pady=10)

    def input_form(self):   
        self.nombre = tk.StringVar()
        self.duracion = tk.StringVar()
        self.actor_principal = tk.StringVar()
        self.director = tk.StringVar()

        self.entry_nombre = tk.Entry(self, textvariable=self.nombre, state='disabled', width=50)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.entry_duracion = tk.Entry(self, textvariable=self.duracion, state='disabled', width=50)
        self.entry_duracion.grid(row=1, column=1, padx=10, pady=10)

        x = consulta.listar_generos()
        y = [i[1] for i in x]
        self.generos = ['Seleccione Uno'] + y
        self.entry_genero = ttk.Combobox(self, values=self.generos, state='disabled', width=25)
        self.entry_genero.current(0)
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10)

        self.entry_actor_principal = tk.Entry(self, textvariable=self.actor_principal, state='disabled', width=50)
        self.entry_actor_principal.grid(row=3, column=1, padx=10, pady=10)

        self.entry_director = tk.Entry(self, textvariable=self.director, state='disabled', width=50)
        self.entry_director.grid(row=4, column=1, padx=10, pady=10)

    def botones_principales(self):    
        self.btn_alta = tk.Button(self, text='Nuevo', command=self.habilitar_campos,
                                  width=20, font=('Arial',12,'bold'), fg='white', bg='#1C500B',
                                  cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_alta.grid(row=5, column=0, padx=10, pady=10)   

        self.btn_modi = tk.Button(self, text='Guardar', command=self.guardar_campos,
                                  width=20, font=('Arial',12,'bold'), fg='white', bg='#0D2A83',
                                  cursor='hand2', activebackground='#7594F5', activeforeground='#000000', state='disabled')
        self.btn_modi.grid(row=5, column=1, padx=10, pady=10) 

        self.btn_cance = tk.Button(self, text='Cancelar', command=self.bloquear_campos,
                                  width=20, font=('Arial',12,'bold'), fg='white', bg='#A90A0A',
                                  cursor='hand2', activebackground='#F35B5B', activeforeground='#000000', state='disabled')
        self.btn_cance.grid(row=5, column=2, padx=10, pady=10)

    def mostrar_tabla(self):
        self.lista_p = consulta.listar_peli()
        self.lista_p.reverse()

        self.tabla = ttk.Treeview(self, columns=('Nombre','Duracion','Genero','Actor Principal','Director'), height=8)
        self.tabla.grid(row=6, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=6, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Nombre')
        self.tabla.heading('#2', text='Duración')
        self.tabla.heading('#3', text='Género')
        self.tabla.heading('#4', text='Actor Principal')
        self.tabla.heading('#5', text='Director')

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for p in self.lista_p:
            caracteristica = consulta.obtener_caracteristica_por_pelicula(p[0])
            actor = caracteristica.actor_principal if caracteristica else ''
            director = caracteristica.director if caracteristica else ''
            self.tabla.insert('', 0, text=p[0],
                              values=(p[1], p[2], p[3], actor, director))

        self.btn_editar = tk.Button(self, text='Editar', command=self.editar_registro,
                                   width=20, font=('Arial',12,'bold'), fg='white', bg='#1C500B',
                                   cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_editar.grid(row=7, column=0, padx=10, pady=10)    
        
        self.btn_delete = tk.Button(self, text='Eliminar', command=self.eliminar_registro,
                                    width=20, font=('Arial',12,'bold'), fg='white', bg='#A90A0A',
                                    cursor='hand2', activebackground='#F35B5B', activeforeground='#000000')
        self.btn_delete.grid(row=7, column=1, padx=10, pady=10)

    def editar_registro(self):
        try:
            self.id_peli = self.tabla.item(self.tabla.selection())['text']
            values = self.tabla.item(self.tabla.selection())['values']
            self.nombre.set(values[0])
            self.duracion.set(values[1])
            self.entry_genero.current(self.generos.index(values[2]))
            self.actor_principal.set(values[3])
            self.director.set(values[4])
            self.habilitar_campos()
        except:
            pass

    def eliminar_registro(self):
        self.id_peli = self.tabla.item(self.tabla.selection())['text']
        response = messagebox.askyesno("Confirmar", "¿Desea borrar el registro?")
        if response:
            consulta.borrar_caracteristica_por_pelicula(self.id_peli)
            consulta.borrar_peli(int(self.id_peli))
        else:
            messagebox.showinfo("Cuidado", "Cancelaste eliminar.")
        self.id_peli = None
        self.mostrar_tabla()

    def guardar_campos(self):
        nombre = self.nombre.get().strip()
        duracion = self.duracion.get().strip()
        genero_index = self.entry_genero.current()
        actor = self.actor_principal.get().strip()
        director = self.director.get().strip()

    
        if not nombre or not duracion or not actor or not director:
            messagebox.showerror("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if genero_index == 0:
            messagebox.showerror("Género inválido", "Debe seleccionar un género.")
            return

        pelicula = consulta.Peliculas(nombre, duracion, genero_index)

        if self.id_peli is None:
            consulta.guardar_peli(pelicula)
            lista = consulta.listar_peli()
            pelicula_id = lista[-1][0]
            caracteristica = consulta.Caracteristica(actor, director, pelicula_id)
            consulta.guardar_caracteristica(caracteristica)
        else:
            consulta.editar_peli(pelicula, int(self.id_peli))
            caracteristica = consulta.Caracteristica(actor, director, int(self.id_peli))
            consulta.editar_caracteristica(caracteristica, int(self.id_peli))

        self.mostrar_tabla()
        self.bloquear_campos()

    def habilitar_campos(self):    
        self.entry_nombre.config(state='normal')    
        self.entry_duracion.config(state='normal')    
        self.entry_genero.config(state='readonly')    
        self.entry_actor_principal.config(state='normal')
        self.entry_director.config(state='normal')
        self.btn_modi.config(state='normal')    
        self.btn_cance.config(state='normal')    
        self.btn_alta.config(state='disabled')

    def bloquear_campos(self):    
        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')    
        self.entry_genero.config(state='disabled')    
        self.entry_actor_principal.config(state='disabled')
        self.entry_director.config(state='disabled')
        self.btn_modi.config(state='disabled')    
        self.btn_cance.config(state='disabled')    
        self.btn_alta.config(state='normal')
        self.nombre.set('')
        self.duracion.set('')
        self.entry_genero.current(0)
        self.actor_principal.set('')
        self.director.set('')
        self.id_peli = None
