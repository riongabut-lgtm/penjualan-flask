from flask import Blueprint, render_template, request, make_response
from flask_login import login_required
from sqlalchemy import func
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from models import Transaksi
from extensions import db

laporan_bp = Blueprint(
    "laporan",
    __name__,
    url_prefix="/laporan"
)

# =========================
# Halaman Laporan
# =========================
@laporan_bp.route("/")
@login_required
def index():

    tanggal_awal = request.args.get("awal")
    tanggal_akhir = request.args.get("akhir")

    query = Transaksi.query

    if tanggal_awal:
        query = query.filter(func.date(Transaksi.tanggal) >= tanggal_awal)

    if tanggal_akhir:
        query = query.filter(func.date(Transaksi.tanggal) <= tanggal_akhir)

    transaksi = query.order_by(
        Transaksi.tanggal.desc()
    ).all()

    total = sum(t.total for t in transaksi)

    return render_template(
        "laporan/index.html",
        transaksi=transaksi,
        total=total,
        awal=tanggal_awal,
        akhir=tanggal_akhir
    )

# =========================
# Export PDF
# =========================
@laporan_bp.route("/pdf")
@login_required
def pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>LAPORAN PENJUALAN</b>", styles["Heading1"])
    )

    transaksi = Transaksi.query.all()

    data = [["Tanggal", "Barang", "Jumlah", "Total"]]

    total = 0

    for t in transaksi:

        data.append([
            t.tanggal.strftime("%d-%m-%Y"),
            t.barang.nama,
            str(t.jumlah),
            f"Rp {t.total:,}"
        ])

        total += t.total

    data.append(["", "", "TOTAL", f"Rp {total:,}"])

    table = Table(data)

    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    response = make_response(buffer.read())

    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=laporan_penjualan.pdf"

    return response