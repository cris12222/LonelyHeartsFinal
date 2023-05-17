from flask import Flask, render_template, request
from cs50 import SQL

data = SQL("sqlite:///inven.db")
app = Flask(__name__)

#iniciamos la pagina
@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/catalogo/')
def catalogo():
    producto = data.execute("SELECT * FROM Productos ORDER BY id ASC")
    productolen =len(producto)
    return render_template("catalogo.html", productolen=productolen, producto=producto)

#registramos el los datos del producto
@app.route('/insertar/', methods=['GET', 'POST'])
def insertar():
    return render_template("alta.html")

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    nombre = request.form["producto"]
    cantidad = int(request.form["cantidad"])
    precio = float(request.form["precio"])
    total = cantidad * precio
    if nombre == "" or cantidad == "" or precio == "":
        return render_template("alta.html", msg="Espacio(S) vacio(S)")
    data.execute("INSERT INTO Productos( nombre, precio, cantidad, total)VALUES( :nombre, :precio, :cantidad, :total)",
                 nombre=nombre, precio=precio, cantidad=cantidad, total=total)
    producto = data.execute("SELECT * FROM Productos ORDER BY id ASC")
    productolen = len(producto)
    return render_template("catalogo.html", productolen=productolen, producto=producto)

@app.route('/editar/')
def editar():
    id = int(request.args.get('id'))
    producto = data.execute("SELECT * FROM Productos Where id=:id",id=id)
    return render_template("editar.html", producto=producto)

@app.route('/vender/')
def vender():
    id = int(request.args.get('id'))
    cantidad = int(request.args.get('cantidad'))
    cantidad = cantidad-1
    data.execute("UPDATE Productos SET cantidad=:cantidad WHERE id=:id ", id=id, cantidad=cantidad)
    producto = data.execute("SELECT * FROM Productos ORDER BY id ASC")
    productolen = len(producto)
    return render_template("catalogo.html", productolen=productolen, producto=producto)

@app.route('/editado/')
def editado():
    id = int(request.args.get('id'))
    print(id)
    cantidad = int(request.args.get('cantidad'))
    precio = float(request.args.get('precio'))
    nombre = (request.args.get('nombre')) 
    total = cantidad * precio
    data.execute("DELETE FROM Productos WHERE id = :id", id=id)
    data.execute("INSERT INTO Productos (id, nombre, precio, cantidad, total) VALUES (:id, :nombre, :precio, :cantidad, :total)",
        id=id, nombre =nombre, precio=precio, cantidad=cantidad, total=total)
    producto = data.execute("SELECT * FROM Productos ORDER BY id ASC")
    productolen = len(producto)
    return render_template("catalogo.html", productolen=productolen, producto=producto)

@app.route('/eliminar/', methods=["GET"])
def eliminar():
    id = int(request.args.get('id'))
    data.execute("DELETE FROM Productos WHERE id=:id", id=id)
    producto = data.execute("SELECT * FROM Productos ORDER BY id ASC")
    productolen = len(producto)
    return render_template("catalogo.html", productolen=productolen, producto=producto)

if __name__ == '__main__':
    app.run()
