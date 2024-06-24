from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    provincia = db.Column(db.String(30), nullable=False)
    localidad = db.Column(db.String(30), nullable=False)
    direccion = db.Column(db.String(60), nullable=False)
    repartidores = db.relationship("Repartidor", backref="sucursal")
    transportes = db.relationship("Transporte", backref="sucursal")
    paquetes = db.relationship("Paquete", backref="sucursal")
    
    def get_id(self):
        return self.id

    
class Repartidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    paquetes = db.relationship('Paquete', backref="repartidor")
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    
    def get_id(self):
        return self.id
    
class Transporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numerotransporte =  db.Column(db.Integer, nullable=False)
    fechahorasalida =  db.Column(db.DateTime)
    fechahorallegada =  db.Column(db.DateTime)
    paquetes = db.relationship('Paquete', backref="transporte")
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    
class Paquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeroenvio = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer)
    nomdestinatario = db.Column(db.String(60), nullable=False)
    dirdestinatario = db.Column(db.String(100), nullable=False)
    entregado = db.Column(db.Boolean)
    observaciones = db.Column(db.Text)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    idtransporte = db.Column(db.Integer, db.ForeignKey('transporte.id'))
    idrepartidor = db.Column(db.Integer, db.ForeignKey('repartidor.id'))
    
    def getEstado(self):
        return self.entregado
    
    def get_idrepartidor(self):
        return self.idrepartidor