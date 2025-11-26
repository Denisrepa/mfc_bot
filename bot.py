import telebot
import gspread
from google.oauth2.service_account import Credentials
import json
import os

# ✅ ХАРДКОД - НИКАКИХ Environment Variables!
TOKEN = "8044674232:AAFc9Fa31bTyx0L405YGQwI3YYvmvIccguo"
SPREADSHEET_ID = "1SYcQqEK0TQ4ptwSshuijJLH0cFkXHaY4wUho1vnefjI"
ADMIN_CHAT_ID = 816837965

# ✅ ТВОЙ credentials.json (ИСПРАВЛЕННЫЙ!)
GOOGLE_CREDENTIALS = {
  "type": "service_account",
  "project_id": "mfcbot",
  "private_key_id": "7b6f861e57a82f4560806a21b12d2913124f22b2",
  "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC8tp45l4D0XzJ4
p/AwBGXGprFHVI7ogJhebbsAITeYvTXvh7e7L1FTtKy3byDftX1/mtkX1GoQ+nJo
4SgABXRAGZWcyYUGGKfLeMUlgc7eQBIBLtw2/2btF4SaWTmiEqcUX9f17tsEaQdn
OYZfPe0Gz0bv8ES/2RCdkMBnSl25aprkVevf1Cw400YNswtQvMq2cw4QINi1voww
R7HeUp9kTENwBlxhXOFlXjOq0ee1NvOAF5Nx96RjVk98Y+5JWzfwGYPlaEBKIzlg
Tmy4j4js1Rk80EncDc83oZvUvJ1lmRC80pMTHEIlJ/E6w0fb8YqTfKX6NsjY1dG1
T5EfPZg1AgMBAAECggEAFWvoG22BQTwqhIZmaMJMXfe/bp4V+CUw0UyaH5z7Afw9
ynTuJvIWGe8LyWl0ooWoO1CejWqap6wQ9KrVBDuaQ0nO2+oG5ExEL9VZEQrigAQR
3HnZ8ZGduL16BfNUQXuQj8AuyZyq1p39gyWFL/vdk2+lWR3oZUavRijk+P9OEvqU
Yq6qxGqD+Oyc5Km6bdK1LMeD7BC3wcZ1QAs9HClK8EhoQhPXBtvBUtPmqrszjXmP
qTeQDePWt09epeuH9BQRBcs7hj4bboI6okl6tr/bFPs07DdSene1p3C1jyPsHdN6
UqE7UdePQ1AsIzR9AkrsEhXeG/lKVxKYjHRdAeqlOQKBgQDcAsu2prrzw4MKrfVB
OahRsn7IDphn7LTeYjbr0JQs3LHdAhgv+zFcOh1AShjTOGRtzRgAk5SueT3KLpxh
nG0Fdx/HQPS9uasBuK4s7TVX3PK+n00Ao0ZHxpUj+VBIhvhuNaAYXgPUPc7yrwro
upHGQds6yk/f/qamxVfZTnk2BwKBgQDblTOUBj1ipLCLiEHHK0xBDod8RrONlRd6
Ja8M9mBCWFIvj31nGrZyBBjSNMW1+EauEl5Mu8uHQLfwpZeJwKLd0xo41zuLfXxs
FJeoYAOeHkgCZ1FF/oxh9k0a1gbjdRbeSTnA3suJ3KFwN7Aye6ZYHeaCuuxEWhg9
WIw8A/vQ4wKBgQDYc9OyHnUd8ANTlXQOOMiVn/PFpT5iOGp1w9DezjWJsZM3qaDc
S9jzMKWoo32rCPcdY8Myhf+oa9XTvWnTSs+jqeBU614d7rYEmoqZ3sI1cEZOLnHW
p8w0P3ZpjxZiVI/D9fRNJOnFfQ3Gi1pDP5K9p/sk6vgMmv+gYdUdEWyFLwKBgQCD
opYhDvyNvhz4CN8l/xbfiU4/ekL5hX9lgmHGa4yZOUlLqcGLpb/p6frXSTudMxFs
GSbe6VXB51JduWd29Tytrnfxy1Wu8bM9N7sS/Twt9glFJ5rZUxflQjpG9Dd89ByZ
dVxh+y4Zn2JIW5oNKYM3H/WoOVaaQ0h0vjiTYe/78QKBgQCdzDlIXOsFxvcb8Ofn
rC/xv/AxB1EqgeuntBu1Y5RhRoRchObQRWeUVfNHEaVATZYBITMm+DcstxQd6Ree
B18pcvW72JaTAn7JDSK45BK+6Fs9/cYfbpoCpjgjIs8KNRcKN+1csuo0xk6cHwBi
zMo4L7KKg5cWRWz9mUcZRZaq8w==
-----END PRIVATE KEY-----
""",
  "client_email": "mfc-bot-service@mfcbot.iam.gserviceaccount.com",
  "client_id": "118108345819461755893",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mfc-bot-service%40mfcbot.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

bot = telebot.TeleBot(TOKEN)
print("🚀 Бот запущен (v6.0 PRO)")

# Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(GOOGLE_CREDENTIALS, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet('Продукты')
print("✅ Google Sheets подключен!")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "🌍 **МФЦ ДЛЯ ПУТЕШЕСТВИЙ**\n\nВсе для путешествий в одном месте!", parse_mode='Markdown')

print("✅ Готов к работе!")
bot.infinity_polling()
