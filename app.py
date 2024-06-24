from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import *
import random
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'mateopin123'

from models import db
from models import Paquete, Repartidor, Sucursal, Transporte

@app.route('/')
def index():
    return render_template('index.html')     

@app.route('/selectSucursalDespachante')
def mostrarSucursales():
    sucursales = Sucursal.query.all()
    return render_template('sucursales.html', sucursales = sucursales)
    
@app.route('/select/<int:id>')
def initSucursalElegida(id):
    sucursal = Sucursal.query.get(id)
    if sucursal:
        session['sucursal_id'] = id
        return render_template("inicioSucursal.html", sucursal=sucursal)
    else:
        return "Sucursal no encontrada"

@app.route('/regPaquete')
def regPaq():
    return render_template('/registrarPaquete.html')

@app.route('/registrarPaquete', methods=['POST'])
def registrarPaquete():
    if request.method == 'POST':
        try:
            peso = int(request.form["peso"].strip())
            nombre = request.form["nombre"].strip()
            dirdestinatario = request.form["dirdestinatario"].strip()
            nroEnvio = random.randint(1000, 5000)

            paquete = Paquete(
                numeroenvio=nroEnvio,
                peso=peso,
                nomdestinatario=nombre,
                dirdestinatario=dirdestinatario,
                entregado=False,  
                idsucursal= session.get('sucursal_id')
            )
            db.session.add(paquete)
            db.session.commit()
            category = 'success'
            return render_template('notify.html', message="Paquete registrado exitosamente.", category = category)
        
        except Exception as e:
            db.session.rollback()
            return render_template('notify.html', message=f"Hubo un error al cargar el paquete: {str(e)}") 

@app.route('/selectSucursalTransporte')
def selectSucursalTransporte():
    sucursales = Sucursal.query.filter(Sucursal.id != session.get('sucursal_id')).all()
    return render_template('sucursalesTransporte.html', sucursales=sucursales)

@app.route('/selectSucursalDestino/<int:id>')
def selectSucursalDestino(id):
    sucursal = Sucursal.query.get(id)
    if sucursal:
        session['destino_sucursal_id'] = id
        paquetes = Paquete.query.filter_by(idsucursal = session.get('sucursal_id'),entregado=False, idrepartidor=None).all()
        return render_template('paquetesTransporte.html', sucursal=sucursal, paquetes=paquetes)
    else:
        return "Sucursal no encontrada"

@app.route('/registrarTransporte', methods=['POST'])
def registrarTransporte():
    if request.method == 'POST':
        paquetes_ids = request.form.getlist('paquetesSeleccionados[]')

        if len(paquetes_ids) == 0:
            category = 'error'
            return render_template('notify.html', message="No seleccionó ningún paquete.", category=category)

        try:
            transporte = Transporte(
                numerotransporte=random.randint(100, 500),
                fechahorasalida=datetime.now(),
                idsucursal=session.get('destino_sucursal_id')
            )
            db.session.add(transporte)
            db.session.commit()
            
            for paquete_id in paquetes_ids:
                paquete = Paquete.query.get(paquete_id)
                if paquete:
                    paquete.idtransporte = session.get('destino_sucursal_id')
                    db.session.commit()

            category = 'success'
            return render_template('notify.html', message="Transporte registrado exitosamente.", category=category)
        
        except Exception as e:
            db.session.rollback()
            return render_template('notify.html', message=f"Hubo un error al registrar el transporte: {str(e)}")

@app.route('/transportesPendientesLlegada')
def transportesPendientesLlegada():
    transportes = Transporte.query.filter_by(idsucursal=session.get('sucursal_id'), fechahorallegada = None).all()
    if len(transportes) == 0:
        category = 'error'
        return render_template('notify.html', message = "La sucursal no tiene que recibir ningún transporte.", category = category)
    else:
        return render_template('transportesPendientesLlegada.html', transportes=transportes)

@app.route('/registrarLlegadaTransporte', methods=['POST'])
def registrarLlegadaTransporte():
    if request.method == 'POST':
        try:
            transportes_seleccionados = request.form.getlist('transportesSeleccionados[]')

            for transporte_id in transportes_seleccionados:
                transporte = Transporte.query.get(transporte_id)
                if transporte:
                    transporte.fechahorallegada = datetime.now()
                    db.session.commit()
                else:
                    flash(f"Transporte con ID {transporte_id} no encontrado.", 'error')

            flash('Llegada de transportes registrada exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la llegada de transportes: {str(e)}', 'error')

    category = 'success'
    return render_template('notify.html', message = "La llegada del transporte se registró con éxito.", category = category)

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)
    