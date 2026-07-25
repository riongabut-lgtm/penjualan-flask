from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.username}>"
    
class Barang(db.Model):

    __tablename__ = "barang"

    id = db.Column(db.Integer, primary_key=True)

    kode = db.Column(db.String(20), unique=True, nullable=False)

    nama = db.Column(db.String(100), nullable=False)

    harga = db.Column(db.Integer, nullable=False)

    stok = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Barang {self.nama}>"
    
from datetime import datetime

class Transaksi(db.Model):

    __tablename__ = "transaksi"

    id = db.Column(db.Integer, primary_key=True)

    barang_id = db.Column(
        db.Integer,
        db.ForeignKey("barang.id"),
        nullable=False
    )

    jumlah = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Integer, nullable=False)

    tanggal = db.Column(
        db.DateTime,
        default=datetime.now
    )

    barang = db.relationship("Barang")
