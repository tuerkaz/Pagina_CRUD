# Librerías
from flask import Flask, render_template, request
import MySQLdb
import os

# Conexión a la base de datos
conn = MySQLdb.connect(
    host=os.getenv('DB_HOST', 'bzhahp9gear4wppnvuw8-mysql.services.clever-cloud.com'),
    user=os.getenv('DB_USER', 'uenogooku1xj27kq'),
    passwd=os.getenv('DB_PASSWORD', 'kJMRU7ehR4CWs81gsEBK'),
    db=os.getenv('DB_NAME', 'bzhahp9gear4wppnvuw8')
)
cursor = conn.cursor()

# Inicialización de Flask
app = Flask(__name__)

# Lista de enlaces
enlaces = [
    {"url": "/", "texto": "Home"},
    {"url": "/create", "texto": "Create"},
    {"url": "/read", "texto": "Read"},
    {"url": "/update", "texto": "Update"},
    {"url": "/delete", "texto": "Delete"}
]

# Función para obtener los nombres de las columnas de la tabla 'Employes'
def nombre_Columnas():
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Employes' ORDER BY ORDINAL_POSITION")
    columns_DB = [column[0] for column in cursor.fetchall()]
    return columns_DB

# Ruta de inicio
@app.route('/')
def init():
    enlaces_filtrados = [enlace for enlace in enlaces if enlace["url"] != "/"]
    return render_template('index.html', enlaces=enlaces_filtrados)

# Ruta de creación
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form['name']
        last_name = request.form['last-name']
        document = request.form['document']
        address = request.form['address']
        cell = request.form['cell-phone']
        
        # Insertar en la base de datos
        cursor.execute("""INSERT INTO Employes (Nombre, Apellido, Documento, Direccion, Telefono)
                          VALUES (%s, %s, %s, %s, %s)""", (name, last_name, document, address, cell))
        conn.commit()

        return "Registro creado con éxito"
    
    return render_template('create.html')

# Ruta de lectura
@app.route('/read')
def read():
    columns_DB = nombre_Columnas()
    cursor.execute("SELECT * FROM Employes")
    tabla = cursor.fetchall()
    return render_template('read.html', columns_DB=columns_DB, tabla=tabla)

# Ruta de actualización
@app.route('/update')
def update():
    return render_template('update.html')

# Ruta de eliminación
@app.route('/delete')
def delete():
    return render_template('delete.html')

# Cerrar la conexión a la base de datos al final de la solicitud
@app.teardown_appcontext
def close_connection(exception):
    if conn:
        conn.close()

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
