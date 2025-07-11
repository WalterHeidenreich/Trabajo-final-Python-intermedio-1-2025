import tkinter as tk
from vista.vista import Frame
from include.menu import barrita_menu

def  main():  
    ventana = tk.Tk()
    ventana.title('Listado Peliculas')  
    ventana.iconbitmap('img/Cine_32x32.ico')
    ventana.resizable(0,0)

    barrita_menu(ventana)
    app = Frame(root= ventana)

    ventana.mainloop()

if __name__ == '__main__':
    main()