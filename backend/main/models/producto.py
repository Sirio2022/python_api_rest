from .. import db
import datetime as dt
from datetime import timezone


class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)  # URL o ruta de la imagen
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    productos_compra = db.relationship(
        "ProductoCompra", back_populates="producto", cascade="all, delete-orphan"
    )
    fecha_creacion = db.Column(
        db.DateTime, default=dt.datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<Producto {self.nombre}>"

    def to_json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "precio": self.precio,
            "stock": self.stock,
            "fecha_creacion": self.fecha_creacion.isoformat(),
        }

    @staticmethod
    def from_json(data):
        return Producto(
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion"),
            imagen=data.get("imagen", None),
            precio=data.get("precio"),
            stock=data.get("stock", 0),
        )
