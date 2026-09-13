from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# WAHA Ayarları (Endpoint /api/sendText eklendi)
WAHA_URL = "https://c8c9865ab1b6b904-78-190-153-51.serveousercontent.com"
HEADERS = {
    'Content-Type': 'application/json',
    'X-Api-Key': 'patronbenim'
}

# WhatsApp Dark Mode Tasarımlı Arayüz
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>WhatsApp Otomasyon Paneli - Dark Mode</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            background: #111b21; 
            color: #e9edef; 
            margin: 0; 
            padding: 0; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
        }
        .container { 
            width: 100%; 
            max-width: 550px; 
            background: #202c33; 
            padding: 35px; 
            border-radius: 12px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); 
            border: 1px solid #222d34;
        }
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            border-bottom: 1px solid #222d34;
            padding-bottom: 15px;
        }
        .header-icon {
            font-size: 28px;
            margin-right: 12px;
        }
        h2 { 
            color: #00a884; 
            margin: 0;
            font-size: 22px;
        }
        label { 
            font-size: 14px;
            color: #8696a0;
            display: block; 
            margin-top: 15px; 
            margin-bottom: 5px;
            font-weight: 500;
        }
        select, textarea { 
            width: 100%; 
            padding: 12px; 
            background: #2a3942; 
            color: #e9edef; 
            border-radius: 8px; 
            border: 1px solid #222d34; 
            box-sizing: border-box; 
            font-size: 15px;
            outline: none;
            transition: border 0.3s;
        }
        select:focus, textarea:focus {
            border-color: #00a884;
        }
        textarea { 
            height: 130px; 
            resize: vertical; 
        }
        button { 
            width: 100%; 
            padding: 12px; 
            background: #00a884; 
            color: #111b21; 
            font-size: 16px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            margin-top: 25px; 
            font-weight: bold;
            transition: background 0.3s;
        }
        button:hover { 
            background: #008f72; 
        }
        #result { 
            margin-top: 20px; 
            font-size: 14px;
            font-weight: 600; 
            text-align: center; 
            padding: 10px;
            border-radius: 6px;
        }
        .loading { color: #34b7f1; background: rgba(52, 183, 241, 0.1); }
        .success { color: #00a884; background: rgba(0, 168, 132, 0.1); }
        .error { color: #f15c6d; background: rgba(241, 92, 109, 0.1); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="header-icon">💬</span>
            <h2>WhatsApp Toplu Mesaj Paneli</h2>
        </div>
        <form id="messageForm">
            <label for="chatId">Hedef Grup:</label>
            <select id="chatId" name="chatId">
                <option value="120363026491322759@g.us">🔒 Adminler | UNIGG</option>
                <option value="905415411461-1538554898@g.us">👥 Başkanlar | UNIGG</option>
                <option value="120363045454726513@g.us">⚙️ YÖNETİM EKİBİ | UNIGG</option>
                <option value="905336905956-1633951872@g.us">☕ Cafe Fuego</option>
                <option value="120363390401189372@g.us">📢 UNIGG | SOSYAL MEDYA</option>
                <option value="120363412155909249@g.us">🌍 SOSYAL MEDYA | MARMARA BÖLGE</option>
                <option value="120363427633464628@g.us">📍 SOSYAL MEDYA | ANADOLU BÖLGE</option>
            </select>

            <label for="text">Gönderilecek Mesaj:</label>
            <textarea id="text" name="text" placeholder="Mesajınızı buraya yazın..."></textarea>

            <button type="submit">Mesajı Gönder 🚀</button>
        </form>
        <div id="result"></div>
    </div>

    <script>
        document.getElementById('messageForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const chatId = document.getElementById('chatId').value;
            const text = document.getElementById('text').value;
            const resultDiv = document.getElementById('result');

            if (!text.trim()) {
                resultDiv.className = "error";
                resultDiv.innerText = "⚠️ Lütfen boş bir mesaj göndermeyin!";
                return;
            }

            resultDiv.className = "loading";
            resultDiv.innerText = "⏳ Mesaj gönderiliyor...";

            try {
                const response = await fetch('/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chatId, text })
                });

                const data = await response.json();
                if (response.ok) {
                    resultDiv.className = "success";
                    resultDiv.innerText = "✅ " + data.message;
                    document.getElementById('text').value = ''; 
                } else {
                    resultDiv.className = "error";
                    resultDiv.innerText = "❌ Hata: " + (data.error || "Bilinmeyen hata");
                }
            } catch (err) {
                resultDiv.className = "error";
                resultDiv.innerText = "❌ Sunucu bağlantı hatası!";
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    chat_id = data.get('chatId')
    text = data.get('text')

    payload = json.dumps({
        "session": "default",
        "chatId": chat_id,
        "text": text
    })

    response = requests.request("POST", WAHA_URL, headers=HEADERS, data=payload)

    if response.status_code in [200, 201]:
        return jsonify({"message": "Mesaj başarıyla gruba gönderildi!"})
    else:
        return jsonify({"error": response.text}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)