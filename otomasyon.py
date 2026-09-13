import requests
import json

# WAHA API Adresi
url = "http://127.0.0.1:3000/api/sendText"

# Gönderilecek mesajın ve hedefin detayları
payload = json.dumps({
  "session": "default",
  "chatId": "120363026491322759@g.us", # Adminler | UNIGG Grup ID'si
  "text": "Merhaba Adminler! Bu mesaj Python otomasyonu üzerinden test amaçlı gönderilmiştir. 🚀"
})

# Güvenlik şifremiz ve veri tipi ayarları
headers = {
  'Content-Type': 'application/json',
  'X-Api-Key': 'patronbenim'
}

# Mesajı sunucuya ateşle
response = requests.request("POST", url, headers=headers, data=payload)

# Sunucudan gelen cevabı kontrol et
if response.status_code == 201 or response.status_code == 200:
    print("✅ Mesaj başarıyla gruba gönderildi!")
else:
    print(f"❌ Bir hata oluştu. Hata Kodu: {response.status_code}")
    print("Detay:", response.text)