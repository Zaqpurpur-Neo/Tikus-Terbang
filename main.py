from flask import Flask, render_template, request, redirect, send_file
from io import BytesIO

import base64
import qrcode
import random
import os
app = Flask(__name__)

user = {
    "username": "",
    "password": ""
}
ticket_order = []

tiket = {
    "tribun-timur": {
        "nama": "Tribun Timur",
        "harga": 150000
    },
    "tribun-barat": {
        "nama": "Tribun Barat",
        "harga": 150000
    },
    "selatan-vvip": {
        "nama": "Selatan VVIP",
        "harga": 300000
    },
    "utara-vvip": {
        "nama": "Utara VVIP",
        "harga": 300000
    },
}

events = [
        {
            "id": 0,
            "host": "Myanmar",
            "lawan": "Indonesia",
            "hari": "Senin",
            "tanggal": 9,
            "bulan": "Desember",
            "bulan-int": 12,
            "jam": "19.30",
            "deskripsi": "Kualifikasi Piala Dunia kali ini mempertemukan Indonesia dengan Myanmar dalam laga yang diprediksi penuh tensi dan antusiasme. Bermain pada hari Senin, 9 Desember pukul 19.30, Timnas Indonesia mendapat dukungan penuh dari ribuan suporter Garuda yang siap menyemangati para pemain di stadion. Pertandingan ini menjadi momen penting untuk membuktikan kemampuan Indonesia melawan salah satu rival kuat di kawasan Asia Tenggara. Dengan strategi dan kerja sama tim yang matang, mampukah mereka mengamankan kemenangan dan melangkah lebih dekat ke panggung Piala Dunia? Laga ini pasti akan menyuguhkan aksi-aksi seru dan momen yang tak terlupakan."
        },
        {
            "id": 1,
            "host": "Indonesia",
            "lawan": "Laos",
            "hari": "Kamis",
            "tanggal": 12,
            "bulan": "Desember",
            "bulan-int": 12,
            "jam": "20.00",
            "deskripsi": "Kualifikasi Piala Dunia terus berlanjut, kali ini mempertemukan Indonesia dengan Laos dalam laga yang berlangsung pada Kamis, 12 Desember pukul 20.00. Bermain di hadapan ribuan pendukung Garuda, pertandingan ini menjadi kesempatan emas bagi Indonesia untuk menunjukkan konsistensi dan dominasi di kandang sendiri. Dengan kerja keras para pemain dan dukungan luar biasa dari suporter, mampukah Timnas Indonesia memastikan poin penuh dan semakin memperbesar peluang lolos? Pertandingan ini dijamin penuh dengan aksi-aksi menarik yang memacu adrenalin."
        },
        {
            "id": 2,
            "host": "Vietnam",
            "lawan": "Indonesia",
            "hari": "Minggu",
            "tanggal": 15,
            "bulan": "Desember",
            "bulan-int": 12,
            "jam": "20.00",
            "deskripsi": "Pertandingan yang ditunggu-tunggu dalam kualifikasi Piala Dunia, Indonesia akan berhadapan dengan Vietnam pada Minggu, 15 Desember pukul 20.00. Dikenal sebagai salah satu tim kuat di Asia Tenggara, Vietnam akan menjadi ujian berat bagi Timnas Indonesia. Dengan dukungan penuh dari ribuan suporter di stadion, laga ini menjadi ajang pembuktian kemampuan tim dalam menghadapi tekanan besar. Mampukah Indonesia menunjukkan keunggulan strategi dan performa di pertandingan yang dipastikan akan menyuguhkan intensitas tinggi ini? Semua mata tertuju pada aksi seru yang akan terjadi di lapangan."
        },
        {
            "id": 3,
            "host": "Indonesia",
            "lawan": "Filipina",
            "hari": "Sabtu",
            "tanggal": 21,
            "bulan": "Desember",
            "bulan-int": 12,
            "jam": "20.00",
            "deskripsi": "Kualifikasi Piala Dunia semakin mendekati akhir, dan kali ini Indonesia dijadwalkan bertemu dengan Filipina pada Sabtu, 21 Desember pukul 20.00. Pertandingan ini menjadi penentuan penting dalam perjuangan Indonesia untuk melangkah lebih jauh di kualifikasi. Bermain di kandang dengan dukungan luar biasa dari suporter Garuda, laga ini menjadi panggung bagi para pemain untuk memberikan penampilan terbaik mereka. Dengan strategi matang dan semangat juang tinggi, mampukah Timnas Indonesia mengakhiri tahun dengan kemenangan gemilang? Pertandingan ini dijamin akan menjadi tontonan penuh momen tak terlupakan."
        },
    ]


@app.route("/")
def home():
    return render_template("home.html", username=user["username"], events=events)


@app.route("/bookings")
def booking():
    if user["username"] == "":
        return redirect("/login")

    book_id = request.args.get("id", type=int)
    print(type(book_id))

    return render_template("booking.html", events=events[int(book_id)])


@app.route("/payment/<ids>", methods=["GET", "POST"])
def payment(ids):
    if user["username"] == "":
        return redirect("/login")

    tiket_id = request.args.get("id", type=int)

    if request.method == "POST":
        idx = random.randint(10000, 99999)

        ticket_order.append({
            "id": f"{idx}",
            "lokasi_id": ids,
            "nama": tiket[ids]["nama"],
            "user": user["username"],
            "tiket_id": tiket_id,
            "qrcode": ""
        })

        return redirect(f"/ticket")

    jenis_tiket = tiket[ids]["nama"]
    harga_ticket = tiket[ids]["harga"]
    jumlah_tiket = 1
    totaL_tiket = harga_ticket * jumlah_tiket

    pajak = harga_ticket * (10/100)
    biaya_admin = harga_ticket * (1/100)
    total_keseluruhan = totaL_tiket + pajak + biaya_admin

    jenis_pembayaran_e_wallet = [
        {"nama": "dana", "title": "DANA", "ext": "svg"},
        {"nama": "ovo", "title": "OVO", "ext": "svg"},
        {"nama": "doku", "title": "DOKU", "ext": "png"},
        {"nama": "gopay", "title": "GoPay", "ext": "png"},
        {"nama": "kredivo", "title": "Kredivo", "ext": "png"},
        {"nama": "shopeepay", "title": "ShopeePay", "ext": "png"},
        {"nama": "linkaja", "title": "LinkAja", "ext": "png"},
    ]

    jenis_pembayaran_bank = [
        {"nama": "mandiri", "title": "Mandiri", "ext": "webp"},
        {"nama": "bca", "title": "BCA", "ext": "png"},
        {"nama": "bank indonesia", "title": "Bank Indonesia", "ext": "png"},
        {"nama": "bni", "title": "BNI", "ext": "png"},
        {"nama": "bri", "title": "BRI", "ext": "png"},
        {"nama": "btn", "title": "BNA", "ext": "png"},
    ]

    jenis_pembayaran_mitra = [
        {"nama": "indomaret", "title": "Indomaret", "ext": "webp"},
        {"nama": "alfamart", "title": "Alfamart", "ext": "webp"},
    ]

    return render_template(
        "payment.html",
        jenis_tiket=jenis_tiket,
        harga_ticket=harga_ticket,
        jumlah_tiket=jumlah_tiket,
        totaL_tiket=totaL_tiket,
        pajak=pajak,
        biaya_admin=biaya_admin,
        total_keseluruhan=total_keseluruhan,
        jenis_pembayaran_e_wallet=jenis_pembayaran_e_wallet,
        jenis_pembayaran_bank=jenis_pembayaran_bank,
        jenis_pembayaran_mitra=jenis_pembayaran_mitra,
        match=events[tiket_id]
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user["username"] = username
        user["password"] = password
        return redirect("/")
    return render_template("login.html")


@app.route("/signout")
def signout():
    user["username"] = ""
    user["password"] = ""
    return redirect("/")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/ticket")
def ticket():
    if user["username"] == "":
        return redirect("/login")

    if len(ticket_order) <= 0:
        return render_template("tiket-none.html")

    ticket_filter = []

    for i in range(len(ticket_order)):
        if ticket_order[i]["user"] == user["username"]:
            username = user['username']
            lokasi = ticket_order[i]['lokasi_id']
            matchid = ticket_order[i]['tiket_id']
            ticket_order[i]["qrcode"] = generate_qrcode(
                    request.url_root +
                    f"ticket-download?user={username}&lokasi={lokasi}&matchid={matchid}"
            )

            ticket_filter.append(ticket_order[i])

    if len(ticket_filter) <= 0:
        return render_template("tiket-none.html")

    return render_template(
            "tiket.html",
            username=user["username"],
            ticket_order=ticket_filter,
            match=events
    )


@app.route("/ticket-download")
def download():
    lokasi = request.args.get("lokasi", type=str)
    matchid = request.args.get("matchid", type=int)

    lokasi_name = tiket[lokasi]['nama']

    if matchid == 1:
        if lokasi == "tribun-timur" or lokasi == "tribun-barat": 
            return send_file("static/tiket-img/indo-laos.pdf")
        else:
            return send_file("static/tiket-img/indo-laos-vvip.pdf")
    elif matchid == 3:
        if lokasi == "tribun-timur" or lokasi == "tribun-barat": 
            return send_file("static/tiket-img/indo-filipina.pdf")
        else:
            return send_file("static/tiket-img/indo-filipina-vvip.pdf")


def generate_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=40,
        border=1
    )
    # http://bit.ly/4ij6LJE
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    out = BytesIO()
    img.save(out, format="PNG")
    encoded_out = base64.b64encode(out.getvalue()).decode('ascii')

    img_format = f"data:image/png;base64, {encoded_out}"
    return img_format


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
