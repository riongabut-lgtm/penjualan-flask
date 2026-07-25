from flask import Flask, redirect, url_for, render_template
from flask_login import login_required
from sqlalchemy import func

from config import Config
from extensions import db, login_manager

from models import User, Barang, Transaksi

from routes.auth import auth
from routes.barang import barang_bp
from routes.transaksi import transaksi_bp
from routes.laporan import laporan_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================
# Register Blueprint
# ==========================

app.register_blueprint(auth)
app.register_blueprint(barang_bp)
app.register_blueprint(transaksi_bp)
app.register_blueprint(laporan_bp)


# ==========================
# Home
# ==========================

@app.route("/")
def home():
    return redirect(url_for("auth.login"))


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
@login_required
def dashboard():

    # Statistik
    total_barang = Barang.query.count()

    total_transaksi = Transaksi.query.count()

    total_penjualan = (
        db.session.query(func.sum(Transaksi.total)).scalar() or 0
    )

    stok_menipis = Barang.query.filter(Barang.stok <= 5).count()

    # 5 transaksi terbaru
    transaksi_terbaru = (
        Transaksi.query
        .order_by(Transaksi.tanggal.desc())
        .limit(5)
        .all()
    )

    # Barang stok menipis
    barang_menipis = (
        Barang.query
        .filter(Barang.stok <= 5)
        .order_by(Barang.stok.asc())
        .limit(5)
        .all()
    )
    # ==========================
    # Grafik Penjualan
    # ==========================

    grafik = (
    db.session.query(
        Barang.nama.label("nama_barang"),
        func.sum(Transaksi.jumlah).label("total_terjual")
        )
        .join(Transaksi, Barang.id == Transaksi.barang_id)
        .group_by(Barang.id, Barang.nama)
        .order_by(Barang.nama)
        .all()
    )

    labels = [item.nama_barang for item in grafik]
    data = [int(item.total_terjual or 0) for item in grafik]
    
    print(labels)
    print(data)
    return render_template(
        "dashboard.html",
        total_barang=total_barang,
        total_transaksi=total_transaksi,
        total_penjualan=total_penjualan,
        stok_menipis=stok_menipis,
        transaksi_terbaru=transaksi_terbaru,
        barang_menipis=barang_menipis,
        labels=labels,
        data=data
    )

# ==========================
# Database
# ==========================

with app.app_context():

    db.create_all()

    if User.query.count() == 0:

        admin = User(
            username="admin",
            password="admin123"
        )

        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)