from flask import render_template, redirect, request
from correo_electronico.models.email import Usuario
from correo_electronico import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registro():
    if not Usuario.is_valid(request.form):
        # redirigimos a la plantilla con el formulario
        return redirect('/')
    Usuario.save(request.form)
    return redirect('/correos')

@app.route('/correos')
def correos():
    return render_template('resultados.html', todos_correos=Usuario.get_all())

@app.route('/correos/eliminar/<int:id>')
def borrar_usuario(id):
    
    data ={ 
        "id":id
    }
    Usuario.destroy(data)
    return redirect('/correos')