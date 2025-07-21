from .. import db


class ProductoCompra(db.Model):
    __tablename__ = "productos_compras"
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey("compras.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    compra = db.relationship(
        "Compra", back_populates="productos_compra", uselist=False, single_parent=True
    )
    producto = db.relationship(
        "Producto", back_populates="productos_compra", uselist=False
    )

    def __repr__(self):
        return f"<ProductoCompra {self.id} para Compra {self.compra_id}>"

    def to_json(self):
        return {
            "id": self.id,
            "compra_id": self.compra_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
        }
