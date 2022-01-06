from flask import Flask, render_template,redirect,url_for,request,flash
from flask_mysqldb import MySQL #pip instal flask-mysqldb

app = Flask(__name__)

#clave secreta para mostrar mensajes flask
app.secret_key = 'clave_secreta_flask'


#Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'proyecto_flask'

mysql = MySQL(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/')
def index():
    return render_template('index.html')

#Crear
@app.route('/insertar-programador', methods=['GET', 'POST'])
def insertar_programador():

    
    if request.method == 'POST':

        #Valores obtenidos de los name de cada input
        lenguaje = request.form['lenguaje']
        experiencia = request.form['experiencia']
        sueldo = request.form['sueldo']
        ciudad = request.form['ciudad']

        #return f"{lenguaje},{experiencia},{sueldo},{ciudad}" comprobar si llegan los datos del formulario

        
        #cursor.execute("INSERT INTO programador VALUES (null, %s,%s,%s,%s)",(lenguaje,experiencia,sueldo,ciudad))

        #insertar datos
        sql = "INSERT INTO programador (lenguaje,annos_experiencia,sueldo,ciudad) values (%s,%s,%s,%s)"
        valores = (lenguaje,experiencia,sueldo,ciudad)
        
        cursor = mysql.connection.cursor()

        cursor.execute(sql, valores)
        if cursor.rowcount == 1:
            cursor.connection.commit()
            flash('Has creado al programador correctamente')
            return redirect(url_for('index'))
        else:
            flash('Error al ingresar programador, faltan datos!')
    
    return render_template('crear_programador.html')


#Mostrar
@app.route('/mostrar-programador')
def mostrar_programador():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM programador')
    programadores = cursor.fetchall() #mostrar todos los resultados
    cursor.close()

    return render_template('listado_programadores.html', programadores=programadores)
    

#Actualizar
@app.route('/actualizar-programador', methods=['GET', 'POST'])
def actualizar_programador():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM programador')
    programadores = cursor.fetchall() #mostrar todos los resultados
    #cursor.close()

    if request.method == 'POST':

        #Valores obtenidos de los name de cada input
        id = request.form['id']
        lenguaje = request.form['lenguaje']
        experiencia = request.form['experiencia']
        sueldo = request.form['sueldo']
        ciudad = request.form['ciudad']

        
        #si el campo no se ingresa asignar un valor como 'no indicado'
        if ciudad == '':
            ciudad = 'No indicado'
        
        sql = "update programador set lenguaje = %s, annos_experiencia = %s, sueldo = %s, ciudad = %s where id = %s"
        values = (lenguaje,experiencia,sueldo,ciudad,id)

        cursor.execute(sql, values)

        if cursor.rowcount == 1:
            cursor.connection.commit()
            flash("Cambios realizados exitosamente!")
            return redirect(url_for('index'))
        else:
            flash("Error al registrar los datos")


    return render_template('actualizar_programador.html',programadores=programadores)


#Eliminar


#Buscar
@app.route('/buscar-programador', methods=['GET', 'POST'])
def buscar_programador():
    cursor = mysql.connection.cursor()
    if request.method == "POST":
        buscar = request.form['buscar']

        sql = """select * from programador where lenguaje =%s"""
        values=(buscar, )

       
        cursor.execute(sql, values)

        registro = cursor.fetchall()
        result = cursor.rowcount

        if  len(registro) >=1:
            flash("Registro encontrado")
            return render_template('buscar_programador.html',registro=registro)
        else:
            flash("Registro no encontrado")
            return render_template("buscar_programador.html")
  



if __name__ == '__main__':
    app.run(debug=True)