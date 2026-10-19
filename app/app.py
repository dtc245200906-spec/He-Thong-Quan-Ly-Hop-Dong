
import os
import sqlite3
from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
metrics = PrometheusMetrics(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "contracts.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                partner TEXT NOT NULL,
                signed_date TEXT NOT NULL,
                value REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'Đang thực hiện'
            )
        """)


@app.route("/")
def home():
    with get_db() as conn:
        contracts = conn.execute(
            "SELECT * FROM contracts ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", contracts=contracts)


@app.route("/add", methods=["POST"])
def add_contract():
    code = request.form.get("code", "").strip()
    name = request.form.get("name", "").strip()
    partner = request.form.get("partner", "").strip()
    signed_date = request.form.get("signed_date", "").strip()
    status = request.form.get("status", "Đang thực hiện")

    try:
        value = float(request.form.get("value", "0"))
    except ValueError:
        return "Giá trị hợp đồng không hợp lệ", 400

    if not all([code, name, partner, signed_date]) or value < 0:
        return "Vui lòng nhập đầy đủ thông tin hợp lệ", 400

    try:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO contracts
                (code, name, partner, signed_date, value, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (code, name, partner, signed_date, value, status))
    except sqlite3.IntegrityError:
        return "Mã hợp đồng đã tồn tại", 400

    return redirect(url_for("home"))


@app.route("/edit/<int:contract_id>", methods=["GET", "POST"])
def edit_contract(contract_id):
    with get_db() as conn:
        contract = conn.execute(
            "SELECT * FROM contracts WHERE id = ?",
            (contract_id,)
        ).fetchone()

    if contract is None:
        abort(404)

    if request.method == "POST":
        code = request.form.get("code", "").strip()
        name = request.form.get("name", "").strip()
        partner = request.form.get("partner", "").strip()
        signed_date = request.form.get("signed_date", "").strip()
        status = request.form.get("status", "Đang thực hiện")

        try:
            value = float(request.form.get("value", "0"))
        except ValueError:
            return "Giá trị hợp đồng không hợp lệ", 400

        if not all([code, name, partner, signed_date]) or value < 0:
            return "Vui lòng nhập đầy đủ thông tin hợp lệ", 400

        try:
            with get_db() as conn:
                conn.execute("""
                    UPDATE contracts
                    SET code=?, name=?, partner=?, signed_date=?,
                        value=?, status=?
                    WHERE id=?
                """, (code, name, partner, signed_date,
                      value, status, contract_id))
        except sqlite3.IntegrityError:
            return "Mã hợp đồng đã tồn tại", 400

        return redirect(url_for("home"))

    return render_template("edit.html", contract=contract)


@app.route("/delete/<int:contract_id>", methods=["POST"])
def delete_contract(contract_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM contracts WHERE id = ?",
            (contract_id,)
        )
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {
        "status": "ok",
        "application": "contract-management"
    }


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
