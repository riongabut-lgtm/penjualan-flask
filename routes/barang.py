from flask import flash
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_login import login_required

from models import Barang
from extensions import db

barang_bp = Blueprint(
    "barang",
    __name__,
    url_prefix="/barang"
)

@barang_bp.route("/hapus/<int:id>")
@login_required
def hapus(id):
    print("ROUTE HAPUS DIPANGGIL")

    barang = Barang.query.get_or_404(id)

    db.session.delete(barang)

    db.session.commit()
    
    flash("Barang berhasil dihapus.")

    return redirect(url_for("barang.index"))

@barang_bp.route("/")
@login_required
def index():

    keyword = request.args.get("q")

    if keyword:

        data = Barang.query.filter(
            Barang.nama.contains(keyword) |
            Barang.kode.contains(keyword)
        ).all()

    else:

        data = Barang.query.all()

    return render_template(
        "barang/index.html",
        barang=data
    )


@barang_bp.route("/tambah", methods=["GET", "POST"])
@login_required
def tambah():

    if request.method == "POST":

        barang = Barang(

            kode=request.form["kode"],

            nama=request.form["nama"],

            harga=request.form["harga"],

            stok=request.form["stok"]

        )

        db.session.add(barang)

        db.session.commit()
        
        flash("Barang berhasil ditambahkan.")
        
        return redirect(url_for("barang.index"))

    return render_template("barang/tambah.html")


@barang_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    barang = Barang.query.get_or_404(id)

    if request.method == "POST":

        barang.kode = request.form["kode"]

        barang.nama = request.form["nama"]

        barang.harga = request.form["harga"]

        barang.stok = request.form["stok"]

        db.session.commit()
        
        flash("Barang berhasil diedit.")

        return redirect(url_for("barang.index"))

    return render_template(
        "barang/edit.html",
        barang=barang
    )