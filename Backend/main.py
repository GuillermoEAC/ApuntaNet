# from flask import Flask,jsonify,request
# import mysql.connector
# from flask_cors import CORS
# import random
# import string
# import jwt #<-- Instalar Pip install PyJWT
# #Se genera la Api
# SECRET_KEY = 'UnaDeCasaParaElGaelPlis'
# Api = Flask(__name__)
# CORS(Api, resources={r"/*": {"origins": "http://localhost:4200"}}, 
#      supports_credentials=True)

# conexion = mysql.connector.connect(user='root',
#                                    password='hola12',
#                                    host='localhost',
#                                    database='apuntanet_db')

# #esta ruta sirve para iniciar sesion
# @Api.route("/login", methods=['POST'])
# def login():
#     data = request.get_json()
#     usuario = data.get('usuario')
#     password = data.get('password')
    
#     cursor = conexion.cursor()
#     cursor.execute("""SELECT id,usuario, password 
#                    FROM usuarios 
#                    WHERE usuario = %s AND password = AES_ENCRYPT(%s, %s)"""
#                    , (usuario, password, SECRET_KEY))
#     resultado = cursor.fetchone()
#     cursor.close()

#     if resultado:
#         token = jwt.encode({
#             'usuario': usuario,
#             'id_usuario': resultado[0]
#         },
#         SECRET_KEY, algorithm='HS256')

#         return jsonify({"status": "Correcto", "message": "Inicio de sesión exitoso", "token": token}), 200
#     else:
#         return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401

# #esta ruta sirve para registrar un nuevo usuario en la base de datos
# #se le pasa el nombre de usuario, la contraseña, el correo y el telefono. la fecha de creacion se le asigna automaticamente la fecha actual 
# @Api.route("/registro", methods=['POST'])
# def registro ():
#     data = request.get_json()
#     usuario = data.get('usuario')
#     password = data.get('password')
#     correo = data.get('correo')
#     telefono = data.get('telefono')

#     try:
#         cursor = conexion.cursor()
#         cursor.execute("""
#              INSERT INTO usuarios (usuario, password, correo, telefono)
#             VALUES (%s, 
#                     aes_encrypt(%s, %s), 
#                     aes_encrypt (%s, %s),
#                     aes_encrypt(%s, %s));
#         """, 
#             (usuario,
#              password, SECRET_KEY,
#              correo, SECRET_KEY,
#              telefono, SECRET_KEY))
#         conexion.commit()  # Confirma los cambios en la base de datos
#         return jsonify({"status": "Correcto", "message": "Usuario registrado exitosamente"}), 201
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al registrar usuario: {err}"}), 500
#     finally:
#         cursor.close()

# @Api.route("/bienvenida", methods=['POST'])
# def bienvenida():
#     data = request.get_json()
#     accion = data.get('accion')

#     if accion == 'crear':
#         return crear_hogar(data)
#     elif accion == 'unirse':
#         return unirse_hogar(data)
#     else:
#         return jsonify({"status": "error", "message": "Acción no válida"}), 400

# def crear_hogar(data):
#     nombre_hogar = data.get('nombre_hogar')
#     descripcion = data.get('descripcion_hogar')
#     id_usuario = data.get('id_usuario')
#     codigo = crearcodigo()

#     try:
#         cursor = conexion.cursor()
#         cursor.execute("SELECT estado FROM usuarios WHERE Id = %s", (id_usuario,))
#         estado = cursor.fetchone()
#         if estado and estado[0] == 'A':
#             return jsonify({"status": "error", "message": "No puedes crear un hogar porque ya perteneces a uno"}), 400

#         cursor.execute("""
#             INSERT INTO hogar (nombre, descripcion, id_usuario, fecha_creacion, codigo)
#             VALUES (%s, %s, %s, NOW(), %s)
#         """, (nombre_hogar, descripcion, id_usuario, codigo))
#         cursor.execute("UPDATE usuarios SET estado = 'A' WHERE Id = %s", (id_usuario,))
#         conexion.commit()
#         return jsonify({"status": "Correcto", "message": "Hogar creado exitosamente"}), 201
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al crear hogar: {err}"}), 500
#     finally:
#         cursor.close()

# def unirse_hogar(data):
#     raw_token = data.get('token')
#     if not raw_token or not raw_token.startswith("Bearer "):
#         return jsonify({"status": "error", "message": "Token no proporcionado o malformado"}), 401

#     token = raw_token.split(" ")[1]
#     codigo = data.get('codigo')
#     cursor = conexion.cursor()
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         id_usuario = decoded_token['id_usuario']

#         cursor.execute("SELECT estado FROM usuarios WHERE Id = %s", (id_usuario,))
#         estado = cursor.fetchone()
#         if estado and estado[0] == 'A':
#             return jsonify({"status": "error", "message": "No puedes pertenecer a dos hogares al mismo tiempo"}), 400

#         cursor.execute("""
#             INSERT INTO casas_usuarios (id_usuario, id_hogar, fecha_ingreso)
#             VALUES (%s, (SELECT id FROM hogar WHERE codigo = %s), NOW())
#         """, (id_usuario, codigo))
#         cursor.execute("UPDATE usuarios SET estado = 'A' WHERE Id = %s", (id_usuario,))
#         conexion.commit()
#         return jsonify({"status": "Correcto", "message": "Ingreso exitoso"}), 201
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al ingresar al hogar: {err}"}), 500
#     except jwt.ExpiredSignatureError:
#         return jsonify({"status": "error", "message": "Token expirado"}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({"status": "error", "message": "Token inválido"}), 401
#     finally:
#         cursor.close()

# #esta ruta sirve para consultar los usuarios de un hogar
# #se le pasa el id del hogar, el cual se utiliza para obtener los usuarios de ese hogar
# @Api.route("/salirHogar", methods=['POST'])
# def salirse_hogar():
#     data = request.get_json()

#     raw_token = data.get('token')
#     if not raw_token or not raw_token.startswith("Bearer "):
#         return jsonify({"status": "error", "message": "Token no proporcionado o malformado"}), 401

#     token = raw_token.split(" ")[1]
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         id_usuario = decoded_token['id_usuario']
        
#         cursor = conexion.cursor() 

#         cursor.execute("SELECT id FROM hogar WHERE id_usuario = %s", (id_usuario,))
#         creador_hogar = cursor.fetchone()

#         if creador_hogar:
#             id_hogar = creador_hogar[0]
#             cursor.execute("UPDATE usuarios SET estado = '' WHERE Id IN (SELECT id_usuario FROM casas_usuarios WHERE id_hogar = %s)", (id_hogar,))
#             cursor.execute("DELETE FROM casas_usuarios WHERE id_hogar = %s", (id_hogar,))
#             cursor.execute("DELETE FROM hogar WHERE id = %s", (id_hogar,))
#             cursor.execute("UPDATE usuarios SET estado = '' WHERE Id = %s", (id_usuario,))
#             conexion.commit()
#             return jsonify({"status": "Correcto", "message": "Hogar disuelto exitosamente"}), 200

#         cursor.execute("SELECT id_hogar FROM casas_usuarios WHERE id_usuario = %s", (id_usuario,))
#         miembro_hogar = cursor.fetchone()

#         if miembro_hogar:
#             id_hogar = miembro_hogar[0]
#             cursor.execute("DELETE FROM casas_usuarios WHERE id_usuario = %s AND id_hogar = %s", (id_usuario, id_hogar))
#             cursor.execute("UPDATE usuarios SET estado = '' WHERE Id = %s", (id_usuario,))
#             conexion.commit()
#             return jsonify({"status": "Correcto", "message": "Has salido del hogar"}), 200

#         return jsonify({"status": "error", "message": "No perteneces a ningún hogar"}), 400

#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error: {err}"}), 500
#     except jwt.ExpiredSignatureError:
#         return jsonify({"status": "error", "message": "Token expirado"}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({"status": "error", "message": "Token inválido"}), 401
#     finally:
#         cursor.close()



# #esta ruta sirve para consultar los hogares a los que pertenece el usuario
# #se le pasa el token del usuario, el cual se utiliza para obtener el id del usuario.
# @Api.route("/consultarHogar", methods=['POST'])
# def consultar_hogar():
#     data = request.get_json()
#     token = data.get('token')

#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         id_usuario = decoded_token['id_usuario']
#         cursor = conexion.cursor()

#         hogares = []

#         # CREADOR
#         cursor.execute("""
#             SELECT hogar.id, hogar.nombre, hogar.descripcion, hogar.codigo, hogar.fecha_creacion
#             FROM hogar
#             WHERE hogar.id_usuario = %s
#         """, (id_usuario,))
#         for row in cursor.fetchall():
#             hogares.append({
#                 'id': row[0],
#                 'nombre': row[1],
#                 'descripcion': row[2],
#                 'codigo': row[3],
#                 'fecha_creacion': row[4].strftime('%Y-%m-%d %H:%M:%S'),
#                 'es_creador': True
#             })

#         # UNIDO
#         cursor.execute("""
#             SELECT hogar.id, hogar.nombre, hogar.descripcion, hogar.codigo, hogar.fecha_creacion
#             FROM hogar
#             INNER JOIN casas_usuarios ON hogar.id = casas_usuarios.id_hogar
#             WHERE casas_usuarios.id_usuario = %s
#         """, (id_usuario,))
#         for row in cursor.fetchall():
#             hogares.append({
#                 'id': row[0],
#                 'nombre': row[1],
#                 'descripcion': row[2],
#                 'codigo': row[3],
#                 'fecha_creacion': row[4].strftime('%Y-%m-%d %H:%M:%S'),
#                 'es_creador': False
#             })

#         return jsonify({"status": "Correcto", "hogares": hogares}), 200

#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al consultar hogares: {err}"}), 500
#     finally:
#         cursor.close()

# #esta ruta sirve para obtener los residentes de un hogar
# #se le pasa el id del hogar, el cual se utiliza para obtener los residentes de ese hogar
# @Api.route('/hogar/residentes/<int:id_hogar>', methods=['GET'])
# def obtener_residentes(id_hogar):
#     cursor = conexion.cursor(dictionary=True)
#     try:
#         # CREADOR
#         cursor.execute("""
#             SELECT 
#                 u.Id AS id, 
#                 u.usuario, 
#                 CAST(AES_DECRYPT(u.correo, %s) AS CHAR) AS correo,
#                 CAST(AES_DECRYPT(u.telefono, %s) AS CHAR) AS telefono,
#                 h.fecha_creacion AS fecha, 
#                 TRUE AS es_creador
#                 FROM usuarios u
#                 JOIN hogar h ON u.Id = h.id_usuario
#                 WHERE h.id = %s
#         """, (SECRET_KEY, SECRET_KEY, id_hogar,))
#         residentes = cursor.fetchall()

#         # UNIDOS
#         cursor.execute("""
#             SELECT     
#                 u.Id AS id, 
#                 u.usuario, 
#                 CAST(AES_DECRYPT(u.correo, %s) AS CHAR) AS correo,
#                 CAST(AES_DECRYPT(u.telefono, %s)AS CHAR) AS telefono, 
#                 cu.fecha_ingreso AS fecha, 
#                 FALSE AS es_creador
#             FROM usuarios u
#             JOIN casas_usuarios cu ON u.Id = cu.id_usuario
#             WHERE cu.id_hogar = %s
#         """, (SECRET_KEY,SECRET_KEY, id_hogar,))
#         residentes += cursor.fetchall()

#         return jsonify({"status": "Correcto", "residentes": residentes}), 200
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al obtener residentes: {err}"}), 500
#     finally:
#         cursor.close()       
    
# #esta ruta sirve para crear una categoria en la base de datos
# #se le pasa el id del hogar, el nombre de la categoria, la descripcion y el grado de privilegio. la fecha de creacion se le asigna automaticamente la fecha actual
# @Api.route("/categorias-hogar/agregar", methods=['POST'])
# def agregar_categoria_a_hogar():
#     data = request.get_json()
#     id_hogar = data.get('id_hogar')
#     id_categoria = data.get('id_categoria')

#     if not id_hogar or not id_categoria:
#         return jsonify({"status": "error", "message": "Datos incompletos"}), 400

#     try:
#         cursor = conexion.cursor()

#         cursor.execute("""
#             SELECT 1 FROM categorias_hogar
#             WHERE id_hogar = %s AND id_categoria = %s
#         """, (id_hogar, id_categoria))

#         if cursor.fetchone():
#             return jsonify({"status": "error", "message": "La categoría ya está asignada a este hogar"}), 400

#         cursor.execute("""
#             INSERT INTO categorias_hogar (id_hogar, id_categoria)
#             VALUES (%s, %s)
#         """, (id_hogar, id_categoria))
#         conexion.commit()

#         return jsonify({"status": "Correcto", "message": "Categoría asociada correctamente"}), 201
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al asociar categoría: {err}"}), 500
#     finally:
#         cursor.close()


# #esta ruta sirve para consultar las categorias de un hogar
# #se le pasa el id del hogar, el cual se utiliza para obtener las categorias de ese hogar
# @Api.route("/categorias/disponible/<int:id_hogar>", methods=['GET'])
# def obtener_categorias_disponibles(id_hogar):
#     try:
#         cursor = conexion.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT c.id, c.nombre, c.descripcion
#             FROM categoria c
#             WHERE c.id NOT IN (
#                 SELECT ch.id_categoria
#                 FROM categorias_hogar ch
#                 WHERE ch.id_hogar = %s
#             )
#         """, (id_hogar,))
#         categorias = cursor.fetchall()
#         return jsonify(categorias), 200
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error al obtener categorías: {err}"}), 500
#     finally:
#         cursor.close()

# #esta ruta sirve para consultar las categorias de un hogar
# #se le pasa el id del hogar, el cual se utiliza para obtener las categorias de ese hogar
# @Api.route("/categorias/seleccionadas/<int:id_hogar>", methods=["GET"])
# def obtener_categorias_seleccionadas(id_hogar):
#     try:
#         cursor = conexion.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT ch.id AS id, c.nombre, c.descripcion
#             FROM categoria c
#             JOIN categorias_hogar ch ON c.id = ch.id_categoria
#             WHERE ch.id_hogar = %s
#         """, (id_hogar,))
#         categorias = cursor.fetchall()
#         return jsonify(categorias), 200
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error: {err}"}), 500
#     finally:
#         cursor.close()

# #retorna el monto total y el nombre de la categoria, tomando en cuenta el mes y el año actual
# #se le pasa id del usuario y el id del hogar
# @Api.route("/DesgloseMensual", methods=['GET'])
# def desglose():
#     cursor = conexion.cursor()
#     token = request.get_json('token').split(" ")[1]
#     decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#     usuario = decoded_token['id_usuario']
#     hogar_id = request.args.get('hogar_id')
#     cursor.execute("""SELECT 
#                         categoria.nombre AS categoria,
#                         SUM(monto_individual.monto_abonado) AS total_abonado
#                     FROM 
#                         monto_individual
#                         INNER JOIN ticket ON monto_individual.id_ticket = ticket.id
#                         INNER JOIN categoria ON ticket.id_categoria = categoria.id
#                         INNER JOIN hogar ON categoria.id_hogar = hogar.id
#                     WHERE 
#                         MONTH(monto_individual.fecha_pago) = MONTH(CURRENT_DATE()) AND
#                         YEAR(monto_individual.fecha_pago) = YEAR(CURRENT_DATE()) AND
#                         monto_individual.id_usuario = %s AND
#                         hogar.id = %s
#                     GROUP BY 
#                         categoria.nombre;
#                     ;
# """, (usuario, hogar_id))
#     resultado = cursor.fetchall()
#     conexion.close()
#     if resultado:
#         desglose = [{"categoria": row[0], "total_abonado": row[1]} for row in resultado]
#         return jsonify({"status": "success", "desglose": desglose}), 200
#     else:
#         return jsonify({"status": "error", "message": "No se encontraron datos"}), 404
    



# #sirve para obtener los tickets de los hogares al que pertenece el usuario
# #se le pasa el id del hogar y el id del usuario
# @Api.route("/tickets", methods=["POST"])
# def crear_ticket():
#     try:
#         data = request.json

#         query = """
#             INSERT INTO ticket (
#                 id_categoriahogar, nombre, descripcion, id_usuario, monto_total, fecha_creacion, fecha_expiracion, estado
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """

#         valores = (
#             data["id_categoriahogar"], data["nombre"], data.get("descripcion", ""), data["id_usuario"], data["monto_total"], data["fecha_creacion"] ,data["fecha_expiracion"], data["estado"]
#         )

#         cursor = conexion.cursor()
#         cursor.execute(query, valores)
#         conexion.commit()

#         return jsonify({"status": "success", "message": "Ticket creado correctamente"}), 201

#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error: {err}"}), 500

#     finally:
#         cursor.close()

# #ruta para obtener los tickets PENDIENTES de un hogar
# @Api.route("/tickets/pendientes/<int:id_hogar>", methods=["GET"])
# def obtener_tickets_pendientes(id_hogar):
#     try:
#         query = """
#             SELECT 
#                 t.id,
#                 t.nombre,
#                 t.descripcion,
#                 t.monto_total,
#                 t.fecha_creacion,
#                 t.fecha_expiracion,
#                 u.usuario as nombre_usuario,
#                 c.nombre as nombre_categoria
#             FROM ticket t
#             JOIN usuarios u ON t.id_usuario = u.id
#             JOIN categorias_hogar ch ON t.id_categoriahogar = ch.id
#             JOIN categoria c ON ch.id_categoria = c.id
#             WHERE ch.id_hogar = %s AND t.estado = 'P'
#             ORDER BY t.fecha_creacion DESC
#         """
        
#         cursor = conexion.cursor(dictionary=True)
#         cursor.execute(query, (id_hogar,))
#         tickets = cursor.fetchall()
        
#         for ticket in tickets:
#             if ticket['fecha_creacion']:
#                 ticket['fecha_creacion'] = ticket['fecha_creacion'].isoformat()
#             if ticket['fecha_expiracion']:
#                 ticket['fecha_expiracion'] = ticket['fecha_expiracion'].isoformat()
        
#         return jsonify({"status": "success", "tickets": tickets}), 200
        
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error: {err}"}), 500
        
#     finally:
#         cursor.close()

# #esta ruta sirve para actualizar el estado de un ticket
# #se le pasa el id del ticket y el nuevo estado, el cual puede ser 'A' (Aprobado) o 'R' (Rechazado)
# @Api.route("/tickets/<int:id_ticket>/estado", methods=["PUT"])
# def actualizar_estado_ticket(id_ticket):
#     cursor = None 
#     try:
#         data = request.json
#         nuevo_estado = data.get("estado")
        
#         if nuevo_estado not in ['A', 'R']:
#             return jsonify({"status": "error", "message": "Estado inválido. Debe ser 'A' (Aprobado) o 'R' (Rechazado)"}), 400
        
#         query = """
#             UPDATE ticket 
#             SET estado = %s
#             WHERE id = %s
#         """
        
#         cursor = conexion.cursor()
#         cursor.execute(query, (nuevo_estado, id_ticket))
#         conexion.commit()
        
#         if cursor.rowcount == 0:
#             return jsonify({"status": "error", "message": "Ticket no encontrado"}), 404
        
#         estado_texto = "aprobado" if nuevo_estado == 'A' else "rechazado"
#         return jsonify({"status": "success", "message": f"Ticket {estado_texto} correctamente"}), 200
        
#     except mysql.connector.Error as err:
#         return jsonify({"status": "error", "message": f"Error: {err}"}), 500
        
#     finally:
#         if cursor:
#             cursor.close()  


# #funcion utulizada para crear un codigo aleatorio de 6 caracteres, el cual se utiliza para agregar usuarios a los hogares
# def crearcodigo():
#     codigo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
#     cursor = conexion.cursor()
#     cursor.execute("SELECT COUNT(*) FROM hogar WHERE codigo = %s", (codigo,))
#     resultado = cursor.fetchone()[0]
#     cursor.close()
    
#     if resultado > 0:
#         return crearcodigo()  # Genera un nuevo código si ya existe uno igual
#     else:
#         return codigo
    


# #se ejecuta la api
# if __name__ == '__main__':
#     Api.run(debug=True)






# from flask import Flask, jsonify, request
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import random
import string
import jwt
import os
import datetime

# --- CONFIGURACIÓN ---
# Render espera que la app se llame 'Api' porque tu comando es 'gunicorn main:Api'
Api = Flask(__name__) 

# Configura CORS
CORS(Api, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Clave secreta
SECRET_KEY = os.environ.get('SECRET_KEY', 'UnaDeCasaParaElGaelPlis')

# --- FUNCIÓN PARA CONECTAR A LA BD ---
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'hola12'),
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'apuntanet_db'),
            port=int(os.environ.get('DB_PORT', 3306))
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error conectando a BD: {err}")
        return None

# --- RUTAS ---
@Api.route("/login", methods=['POST'])
def login():
    conn = get_db_connection()
    if not conn: return jsonify({"status": "error", "message": "Error de conexión BD"}), 500
    
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        password = data.get('password')
        
        cursor = conn.cursor()
        
        # Usamos HEX y AES_ENCRYPT para que coincida con el registro
        cursor.execute("""
            SELECT id, usuario 
            FROM usuarios 
            WHERE usuario = %s AND password = HEX(AES_ENCRYPT(%s, %s))
        """, (usuario, password, SECRET_KEY))
        
        resultado = cursor.fetchone()
        
        if resultado:
            token_payload = {
                'usuario': usuario,
                'id_usuario': resultado[0],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
            return jsonify({"status": "Correcto", "message": "Inicio de sesión exitoso", "token": token}), 200
        else:
            return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
# --- RUTAS DE HOGAR ---

@Api.route("/registro", methods=['POST'])
def registro():
    conn = get_db_connection()
    if not conn: return jsonify({"status": "error", "message": "Error de conexión BD"}), 500

    try:
        data = request.get_json()
        cursor = conn.cursor()
        
        # --- CAMBIO AQUÍ: Usamos HEX(...) para el password ---
        # Nota: Correo y teléfono pueden quedarse igual si usas CAST(... AS CHAR) al leerlos, 
        # pero el password es el crítico para el login.
        cursor.execute("""
             INSERT INTO usuarios (usuario, password, correo, telefono)
             VALUES (%s, HEX(AES_ENCRYPT(%s, %s)), aes_encrypt(%s, %s), aes_encrypt(%s, %s));
        """, (data['usuario'], data['password'], SECRET_KEY, data['correo'], SECRET_KEY, data['telefono'], SECRET_KEY))
        # ----------------------------------------------------
        
        conn.commit()
        return jsonify({"status": "Correcto", "message": "Usuario registrado exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": f"Error al registrar: {err}"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def crear_hogar(data):
    conn = get_db_connection()
    if not conn: return jsonify({"status": "error", "message": "Error de conexión BD"}), 500
    
    try:
        id_usuario = data.get('id_usuario')
        codigo = crearcodigo(conn)
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT estado FROM usuarios WHERE Id = %s", (id_usuario,))
        estado = cursor.fetchone()
        if estado and estado[0] == 'A':
            return jsonify({"status": "error", "message": "Ya perteneces a un hogar"}), 400

        cursor.execute("""
            INSERT INTO hogar (nombre, descripcion, id_usuario, fecha_creacion, codigo)
            VALUES (%s, %s, %s, NOW(), %s)
        """, (data['nombre_hogar'], data['descripcion_hogar'], id_usuario, codigo))
        
        cursor.execute("UPDATE usuarios SET estado = 'A' WHERE Id = %s", (id_usuario,))
        conn.commit()
        return jsonify({"status": "Correcto", "message": "Hogar creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def unirse_hogar(data):
    conn = get_db_connection()
    if not conn: return jsonify({"status": "error", "message": "Error de conexión BD"}), 500

    try:
        token = data.get('token').split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        id_usuario = decoded['id_usuario']
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT estado FROM usuarios WHERE Id = %s", (id_usuario,))
        estado = cursor.fetchone()
        if estado and estado[0] == 'A':
            return jsonify({"status": "error", "message": "Ya tienes un hogar"}), 400

        cursor.execute("""
            INSERT INTO casas_usuarios (id_usuario, id_hogar, fecha_ingreso)
            VALUES (%s, (SELECT id FROM hogar WHERE codigo = %s LIMIT 1), NOW())
        """, (id_usuario, data['codigo']))
        
        cursor.execute("UPDATE usuarios SET estado = 'A' WHERE Id = %s", (id_usuario,))
        conn.commit()
        return jsonify({"status": "Correcto", "message": "Ingreso exitoso"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@Api.route("/consultarHogar", methods=['POST'])
def consultar_hogar():
    conn = get_db_connection()
    if not conn: return jsonify({"status": "error", "message": "Error de conexión BD"}), 500
    
    try:
        token = request.get_json().get('token').split(" ")[1]
        id_usuario = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['id_usuario']
        
        cursor = conn.cursor()
        hogares = []

        query = """
            SELECT h.id, h.nombre, h.descripcion, h.codigo, h.fecha_creacion, 'true' as es_creador
            FROM hogar h WHERE h.id_usuario = %s
            UNION
            SELECT h.id, h.nombre, h.descripcion, h.codigo, h.fecha_creacion, 'false' as es_creador
            FROM hogar h JOIN casas_usuarios cu ON h.id = cu.id_hogar WHERE cu.id_usuario = %s
        """
        cursor.execute(query, (id_usuario, id_usuario))
        
        for row in cursor.fetchall():
            hogares.append({
                'id': row[0], 'nombre': row[1], 'descripcion': row[2], 
                'codigo': row[3], 'fecha_creacion': str(row[4]), 'es_creador': row[5] == 'true'
            })
            
        return jsonify({"status": "Correcto", "hogares": hogares}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@Api.route("/DesgloseMensual", methods=['GET'])
def desglose():
    conn = get_db_connection()
    if not conn: return jsonify({"status": "error", "message": "Error de conexión BD"}), 500
    
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            data = request.get_json(silent=True)
            if data and 'token' in data:
                auth_header = data['token']
            else:
                return jsonify({"status": "error", "message": "Token requerido"}), 401

        token = auth_header.split(" ")[1] if "Bearer" in auth_header else auth_header
        id_usuario = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['id_usuario']
        hogar_id = request.args.get('hogar_id')

        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT categoria.nombre, SUM(monto_individual.monto_abonado)
            FROM monto_individual
            INNER JOIN ticket ON monto_individual.id_ticket = ticket.id
            INNER JOIN categoria ON ticket.id_categoria = categoria.id
            INNER JOIN hogar ON categoria.id_hogar = hogar.id
            WHERE MONTH(monto_individual.fecha_pago) = MONTH(CURRENT_DATE()) 
            AND YEAR(monto_individual.fecha_pago) = YEAR(CURRENT_DATE()) 
            AND monto_individual.id_usuario = %s AND hogar.id = %s
            GROUP BY categoria.nombre
        """, (id_usuario, hogar_id))
        
        resultado = cursor.fetchall()
        desglose = [{"categoria": row[0], "total_abonado": float(row[1])} for row in resultado]
        return jsonify({"status": "success", "desglose": desglose}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- UTILIDADES ---

def crearcodigo(existing_conn=None):
    codigo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    if existing_conn:
        cursor = existing_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM hogar WHERE codigo = %s", (codigo,))
        if cursor.fetchone()[0] > 0:
            return crearcodigo(existing_conn)
        cursor.close()
    return codigo

if __name__ == '__main__':
    Api.run(debug=True, port=5000)