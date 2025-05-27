from pymongo import MongoClient

client = MongoClient("mongodb+srv://wsbuser:wsb1234@cluster0.xxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

try:
    client.admin.command("ping")
    print("✅ Udało się połączyć")
except Exception as e:
    print("❌ Błąd połączenia:", e)
