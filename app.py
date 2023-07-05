from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask (__name__)

conexion = MySQL(app)

@app.route('/productos',  methods=['GET'])
def listar_productos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, nombre, descripcion, categoria, precio, stock, pedidoId FROM productos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        productos = []
        for fila in datos:
            producto= {'id': fila[0], 'nombre': fila[1], 'descripcion': fila[2], 'categoria': fila[3], 'precio': fila[4], 'stock': fila[5], 'pedidoIdS': fila[6]              }
            productos.append(producto)
        return jsonify({'Productos': productos, 'mensaje': "Productos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/productos/<id>', methods=['GET'])
def leer_productos(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id, nombre, descripcion, categoria, precio, stock ,pedidoId FROM productos  WHERE id='{0}' ".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            productos = {'id':datos[0],'nombre':datos[1],'descripcion':datos[2],'categoria':datos[3],'precio':datos[4],'stock':datos[5],'pedidoId':datos[6] }
            return jsonify({'productos': productos, 'mensaje': "Inventario listados.", 'exito': True})
        else:
            return jsonify({'mensaje': "Error", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})



@app.route('/productos', methods=['POST'])
def registrar_productos():
   try:
      cursor = conexion.connection.cursor()
      sql="INSERT INTO productos (id, nombre, descripcion, categoria, precio , stock,pedidoId) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','{6}')".format(request.json['id'],request.json['nombre'],request.json['descripcion'],request.json['categoria'],request.json['precio'],request.json['stock'],request.json['pedidoId'])
      cursor.execute(sql)
      conexion.connection.commit()
      return jsonify({'mensaje': "registrado.", 'exito': True})
   except Exception as ex:
        return jsonify({'mensaje':"Error"})
   


@app.route('/productos/<id>', methods=['DELETE'])
def eliminar_productos(id):
    try:
        cursor = conexion.connection.cursor()
        sql="DELETE FROM productos WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Eliminado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    
@app.route('/productos/<id>', methods=['PUT'] )
def modificar_productos(id):
    try:
        producto = leer_productos(id)
        if producto != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE productos SET nombre = '{0}', descripcion = {1}, categoria = {2}, precio = {3}, stock = {4}, pedidoId = {5}  
            WHERE id = '{6}'""".format(request.json['nombre'], request.json['descripcion'], request.json['categoria'], request.json['precio'], request.json['stock'],request.json['pedidoId'], id)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de actualización.
            return jsonify({'mensaje': "Producto actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Producto no valido", 'Error': True})
    except:
      return jsonify({'mensaje': "error.", 'Error': True})


@app.route('/pedidos', methods=['POST'])
def registrar_pedido():
   try:
      cursor = conexion.connection.cursor()
      sql="INSERT INTO pedido (id, direccion, detalle, productoId) VALUES ('{0}', '{1}', '{2}', '{3}')".format(request.json['id'],request.json['direccion'],request.json['detalle'],request.json['productoId'])
      cursor.execute(sql)
      conexion.connection.commit()
      return jsonify({'mensaje': "registrado.", 'exito': True})
   except Exception as ex:
        return jsonify({'mensaje':"Error"})

@app.route('/pedidos',  methods=['GET'])
def listar_pedidos():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id, direccion,detalle, productoId FROM pedido"
        cursor.execute(sql)
        datos = cursor.fetchall()
        pedidos = []
        for fila in datos:
            pedido = {'id':fila[0],'direccion':fila[1],'detalle':fila[2],'productoId':fila[3]}
            pedidos.append(pedido)
            return jsonify({'pedidos': pedido, 'mensaje': "Pedidos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'pedidos': pedido, 'mensaje': "error", 'exito': True})





def pagina_no_encontrada(error):
    return "<h1>La página que buscas no existe</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)


