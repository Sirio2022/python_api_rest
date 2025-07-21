from .. import db
import datetime as dt
from datetime import timezone


class Compra(db.Model):
    __tablename__ = "compras"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    productos_compra = db.relationship(
        "ProductoCompra", back_populates="compra", cascade="all, delete-orphan"
    )
    fecha_compra = db.Column(
        db.DateTime, default=dt.datetime.now(timezone.utc), nullable=False
    )

    usuario = db.relationship(
        "Usuario", back_populates="compras", uselist=False, single_parent=True
    )

    def __repr__(self):
        return f"<Compra {self.id} para Usuario {self.usuario_id}>"

    def to_json(self):
        return {
            "id": self.id,
            "usuario": self.usuario.to_json(),
            "fecha_compra": self.fecha_compra.isoformat(),
        }

    @staticmethod
    def from_json(data):
        return Compra(
            usuario_id=data.get("usuario_id"),
        )
