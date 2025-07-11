from .coneciondb import Conneccion

def crear_tabla():
    conn = Conneccion()

    sql_genero = '''
        CREATE TABLE IF NOT EXISTS Genero(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre VARCHAR(50)
        );
    '''

    sql_peliculas = '''
        CREATE TABLE IF NOT EXISTS Peliculas(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre VARCHAR(150),
            Duracion VARCHAR(4),
            Genero INTEGER,
            FOREIGN KEY (Genero) REFERENCES Genero(ID)
        );
    '''

    sql_caracteristica = '''
        CREATE TABLE IF NOT EXISTS Caracteristica(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ActorPrincipal VARCHAR(100),
            Director VARCHAR(100),
            PeliculaID INTEGER,
            FOREIGN KEY (PeliculaID) REFERENCES Peliculas(ID)
        );
    '''

    try:
        conn.cursor.execute(sql_genero)
        conn.cerrar_con()

        conn = Conneccion()
        conn.cursor.execute(sql_peliculas)
        conn.cerrar_con()

        conn = Conneccion()
        conn.cursor.execute(sql_caracteristica)
        conn.cerrar_con()
    except Exception as e:
        print("Error creando tablas:", e)


class Peliculas():
    def __init__(self, nombre, duracion, genero):
        self.nombre = nombre
        self.duracion = duracion
        self.genero = genero

    def __str__(self):
        return f'Pelicula[{self.nombre}, {self.duracion}, {self.genero}]'

class Caracteristica():
    def __init__(self, actor_principal, director, pelicula_id):
        self.actor_principal = actor_principal
        self.director = director
        self.pelicula_id = pelicula_id



def guardar_peli(pelicula):
    conn = Conneccion()
    sql = '''
        INSERT INTO Peliculas(Nombre, Duracion, Genero)
        VALUES (?, ?, ?);
    '''
    try:
        conn.cursor.execute(sql, (pelicula.nombre, pelicula.duracion, pelicula.genero))
        conn.cerrar_con()
    except Exception as e:
        print("Error guardando película:", e)

def listar_peli():
    conn = Conneccion()
    listar_peliculas = []
    sql = '''
        SELECT p.ID, p.Nombre, p.Duracion, g.Nombre 
        FROM Peliculas AS p
        INNER JOIN Genero AS g ON p.Genero = g.ID;
    '''
    try:
        conn.cursor.execute(sql)
        listar_peliculas = conn.cursor.fetchall()
        conn.cerrar_con()
        return listar_peliculas
    except Exception as e:
        print("Error listando películas:", e)
        return []

def editar_peli(pelicula, id):
    conn = Conneccion()
    sql = '''
        UPDATE Peliculas
        SET Nombre = ?, Duracion = ?, Genero = ?
        WHERE ID = ?;
    '''
    try:
        conn.cursor.execute(sql, (pelicula.nombre, pelicula.duracion, pelicula.genero, id))
        conn.cerrar_con()
    except Exception as e:
        print("Error editando película:", e)

def borrar_peli(id):
    conn = Conneccion()
    sql = 'DELETE FROM Peliculas WHERE ID = ?;'
    try:
        conn.cursor.execute(sql, (id,))
        conn.cerrar_con()
    except Exception as e:
        print("Error borrando película:", e)


def listar_generos():
    conn = Conneccion()
    sql = 'SELECT * FROM Genero;'
    try:
        conn.cursor.execute(sql)
        generos = conn.cursor.fetchall()
        conn.cerrar_con()
        return generos
    except Exception as e:
        print("Error listando géneros:", e)
        return []


def obtener_caracteristica_por_pelicula(pelicula_id):
    conn = Conneccion()
    caracteristica = None
    sql = '''
        SELECT ActorPrincipal, Director 
        FROM Caracteristica
        WHERE PeliculaID = ?;
    '''
    try:
        conn.cursor.execute(sql, (pelicula_id,))
        fila = conn.cursor.fetchone()
        if fila:
            caracteristica = Caracteristica(fila[0], fila[1], pelicula_id)
        conn.cerrar_con()
    except Exception as e:
        print("Error obteniendo característica:", e)
    return caracteristica

def guardar_caracteristica(caracteristica):
    conn = Conneccion()
    sql = '''
        INSERT INTO Caracteristica (ActorPrincipal, Director, PeliculaID)
        VALUES (?, ?, ?);
    '''
    try:
        conn.cursor.execute(sql, (caracteristica.actor_principal, caracteristica.director, caracteristica.pelicula_id))
        conn.cerrar_con()
    except Exception as e:
        print("Error guardando característica:", e)

def borrar_caracteristica_por_pelicula(pelicula_id):
    conn = Conneccion()
    sql = 'DELETE FROM Caracteristica WHERE PeliculaID = ?;'
    try:
        conn.cursor.execute(sql, (pelicula_id,))
        conn.cerrar_con()
    except Exception as e:
        print("Error borrando característica:", e)

def editar_caracteristica(caracteristica, pelicula_id):
    conn = Conneccion()
    sql = '''
        UPDATE Caracteristica
        SET ActorPrincipal = ?, Director = ?
        WHERE PeliculaID = ?;
    '''
    try:
        conn.cursor.execute(sql, (caracteristica.actor_principal, caracteristica.director, pelicula_id))
        conn.cerrar_con()
    except Exception as e:
        print("Error editando característica:", e)
