import os
import uuid
import csv
import zipfile
import traceback
from datetime import datetime
from flask import Flask, send_file
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# ✅ Wczytanie zmiennych środowiskowych
load_dotenv()

app = Flask(__name__)
report_data = []

# ✅ Pobieranie zmiennych
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "test"
COLLECTION_NAME = "test_render"

def log_result(test_name, status, message):
    print(f"{'✅' if status == 'PASS' else '❌'} [{test_name}] {message}")
    report_data.append({
        "test": test_name,
        "status": status,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })

def test_connection(client):
    print("🔌 Testuję połączenie z MongoDB...")
    try:
        client.admin.command('ping')
        log_result("TEST 1", "PASS", "Połączenie z MongoDB powiodło się.")
        return True
    except ConnectionFailure as e:
        log_result("TEST 1", "FAIL", f"Błąd połączenia: {e}")
        return False

def test_insert_and_read(collection):
    print("🧪 Wykonuję test INSERT/READ...")
    doc_id = str(uuid.uuid4())
    test_doc = {"_id": doc_id, "test": "insert", "status": "ok"}
    collection.insert_one(test_doc)
    retrieved = collection.find_one({"_id": doc_id})
    if retrieved:
        log_result("TEST 2", "PASS", "Insert i odczyt dokumentu powiodły się.")
    else:
        log_result("TEST 2", "FAIL", "Insert lub odczyt dokumentu nie powiódł się.")

def test_empty_collection_behavior(collection):
    print("🧼 Wykonuję test pustej kolekcji...")
    collection.delete_many({})
    results = list(collection.find({}))
    if not results:
        log_result("TEST 3", "PASS", "Kolekcja pusta – brak danych jak oczekiwano.")
    else:
        log_result("TEST 3", "FAIL", f"Kolekcja nie jest pusta: {results}")

def test_schema_validation(collection):
    print("📋 Wykonuję test zgodności ze schematem...")
    test_doc = {"name": "Jan", "age": 30}
    try:
        collection.insert_one(test_doc)
        log_result("TEST 4", "PASS", "Dokument zgodny ze schematem (jeśli ustawiony).")
    except Exception as e:
        log_result("TEST 4", "FAIL", f"Wstawienie niezgodne ze schematem: {e}")

def save_report_csv(filename="raport.csv"):
    print("💾 Zapisuję raport CSV...")
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Test", "Status", "Komunikat", "Czas"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in report_data:
            writer.writerow({
                "Test": row["test"],
                "Status": "Sukces" if row["status"] == "PASS" else "Błąd",
                "Komunikat": row["message"],
                "Czas": row["timestamp"]
            })

def save_report_html(filename="raport.html"):
    print("💾 Zapisuję raport HTML...")
    with open(filename, "w", encoding="utf-8") as htmlfile:
        htmlfile.write("<html><head><meta charset='utf-8'><title>Raport testów MongoDB</title></head><body>")
        htmlfile.write("<h1>Raport testów MongoDB</h1><table border='1'>")
        htmlfile.write("<tr><th>Test</th><th>Status</th><th>Komunikat</th><th>Czas</th></tr>")
        for row in report_data:
            color = "#c8e6c9" if row["status"] == "PASS" else "#ffcdd2"
            htmlfile.write(f"<tr bgcolor='{color}'>")
            htmlfile.write(
                f"<td>{row['test']}</td><td>{'Sukces' if row['status'] == 'PASS' else 'Błąd'}</td><td>{row['message']}</td><td>{row['timestamp']}</td>")
            htmlfile.write("</tr>")
        htmlfile.write("</table></body></html>")

def zip_reports(zip_filename="raport_mongodb.zip"):
    print("📦 Pakuję pliki raportu do ZIP...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("raport.csv")
        zipf.write("raport.html")

@app.route("/generuj-raport")
def generate_report():
    print("▶️ Wywołano /generuj-raport")
    print("🔍 MONGO_URI =", MONGO_URI)

    try:
        report_data.clear()

        if not MONGO_URI:
            print("❌ Brak zmiennej MONGO_URI – upewnij się, że plik .env istnieje.")
            return "Brak zmiennej środowiskowej MONGO_URI", 500

        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)

        if test_connection(client):
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            test_empty_collection_behavior(collection)
            test_insert_and_read(collection)
            test_schema_validation(collection)

            save_report_csv()
            save_report_html()
            zip_reports()

            print("✅ Raport wygenerowany i ZIP gotowy do wysyłki.")
            return send_file("raport_mongodb.zip", as_attachment=True)
        else:
            print("❌ Nie udało się połączyć z MongoDB.")
            return "Błąd połączenia z MongoDB", 500
    except Exception as e:
        print("💥 Błąd krytyczny podczas generowania raportu!")
        traceback.print_exc()
        return f"Internal Server Error: {e}", 500

@app.route("/healthz")
def health():
    print("📡 Wywołano /healthz")
    return "OK", 200

@app.route("/")
def home():
    print("🏠 Wejście na stronę główną")
    return "<h2>MongoDB Tester Flask API</h2><p>Wejdź na <a href='/generuj-raport'>/generuj-raport</a> aby pobrać raport ZIP.</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Aplikacja startuje na porcie {port}...")
    app.run(debug=False, host="0.0.0.0", port=port)
