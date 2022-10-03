from correo_electronico.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #MÉTODOS DE CONSULTA
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultado =  connectToMySQL('esquema_correo').query_db(query)
        usuarios =[]
        for u in resultado:
            usuarios.append(cls(u))
        return usuarios

    #MÉTODOS DE CREACIÓN/BORRAR DATOS
    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (email) VALUES (%(email)s)"
        resultado = connectToMySQL('esquema_correo').query_db(query,data)
        return resultado

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('esquema_correo').query_db(query,data)

    #MÉTODO DE VALIDACIÓN
    @staticmethod
    def is_valid(usuario):
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL('esquema_correo').query_db(query,usuario)
        if len(resultado) >= 1:
            is_valid = False
            flash("Este correo ya existe en nuestra BD")
        # prueba si un campo coincide con el patrón
        if not EMAIL_REGEX.match(usuario['email']): 
            flash("Correo inválido")
            is_valid = False
        return is_valid