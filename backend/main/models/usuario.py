from .. import db
import datetime as dt
from datetime import timezone


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    user_surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(
        db.DateTime, default=dt.datetime.now(timezone.utc), nullable=False
    )
    compra = db.relationship(
        "Compra", back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario {self.username} {self.role}>"

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "user_surname": self.user_surname,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_json(data):
        return Usuario(
            username=data.get("username"),
            user_surname=data.get("user_surname"),
            email=data.get("email"),
            role=data.get("role", "user"),
            phone_number=data.get("phone_number"),
        )
