from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required

from models import Barang, Transaksi
from extensions import db

transaksi_bp = Blueprint(
    "transaksi",
    __name__,
    url_prefix="/transaksi"
)


@transaksi_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    daftar_barang = Barang.query.all()

    if request.method == "POST":

        barang_id = int(request.form["barang"])

        jumlah = int(request.form["jumlah"])

        barang = Barang.query.get_or_404(barang_id)

        if jumlah <= 0:

            flash("Jumlah harus lebih dari 0")

            return redirect(url_for("transaksi.index"))

        if jumlah > barang.stok:

            flash("Stok tidak mencukupi")

            return redirect(url_for("transaksi.index"))

        total = barang.harga * jumlah

        transaksi = Transaksi(

            barang_id=barang.id,

            jumlah=jumlah,

            total=total

        )

        barang.stok -= jumlah

        db.session.add(transaksi)

        db.session.commit()

        flash("Transaksi berhasil")

        return redirect(url_for("transaksi.riwayat"))

    return render_template(
        "transaksi/index.html",
        barang=daftar_barang
    )


@transaksi_bp.route("/riwayat")
@login_required
def riwayat():

    data = Transaksi.query.order_by(
        Transaksi.tanggal.desc()
    ).all()

    return render_template(
        "transaksi/riwayat.html",
        transaksi=data
    )