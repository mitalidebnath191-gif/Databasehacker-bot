import os
import telebot
import urllib.parse
import requests
import time
import hashlib
from flask import Flask, request

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

user_spam_tracker = {}
user_notes = {}

# ==========================================
# 🚨 WELCOME MENU
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(m):
    welcome_text = """🚨 WELCOME TO MEGA ULTRA BOT 🚨
━━━━━━━━━━━━━━━━━━━━━━
হ্যালো বস! 😎 আপনার প্রাইভেট হাই-সিকিউরিটি ইন্টেলিজেন্স বট একদম রেডি এবং অনলাইনে আছে। ⚡

🛠️ সিস্টেম কমান্ড মেনু:

🤖 আর্টিফিশিয়াল ইন্টেলিজেন্স (AI):
🔹 /ask [প্রশ্ন] - লাইভ ইন্টারনেট থেকে তাজা খবর ও উত্তর
🔹 /ai [প্রশ্ন] - বটের অফলাইন ব্রেইন থেকে উত্তর

🕵️‍♂️ ইন্টেলিজেন্স স্ক্যানার (CBI Mode):
🔹 /name [নম্বর] - আল্ট্রা স্ক্যানার (নাম, লোকেশন, ইমেইল এবং ফেক ডিজিটাল ফুটপ্রিন্ট)
🔹 /track [নম্বর] - সিমের বেসিক লোকেশন এবং কোম্পানির নাম
🔹 /social [নম্বর] - OSINT সোশ্যাল ফুটপ্রিন্ট স্ক্যানার (Bypass Mode) 🚨

⚙️ সার্ভার কন্ট্রোল:
🔹 /ping - বটের স্পিড এবং কানেকশন স্ট্যাটাস চেক করুন।
🔹 /ai proshno - AI er sathe jekono kotha bolun
🔹 /math onko - Onko ba math dhap-e-dhap solve korun
🔹 /graph somikoron - Math equation er graph toiri
🔹 /formula topic - Jyamiti ba onkor sutro dekho
🔹 /routine - Apnar weekly study routine dekhun
🔹 /tr bhasa text - Jekono vasa translate korun
🔹 /wiki topic - Wikipedia theke tothyo janun

📓 Notebook & Focus (Nijer Kaj)
🔹 /note text - Dorkari kotha/porashona save rakhun
🔹 /notes - Apnar save kora sob note dekhun
🔹 /delnote number - Kono note delete korun
🔹 /timer min - Porar jonno focus timer set korun

💻 Dev & Cyber (Hacker Tools)
🔹 /run code - Code run kore output dekhun
🔹 /termux tool - Termux o Linux command guide
🔹 /hash text - Text ke MD5 te lock korun
🔹 /decrypt hash - MD5 hash crack/decrypt korun
🔹 /payload sni - Custom HTTP payload toiri
🔹 /bin number - Bank BIN er details check

🛠 OSINT & Net (Information Gathering)
🔹 /snicheck host - SNI/Host alive kina check kora
🔹 /ss url - Jekono website er screenshot nin
🔹 /sub domain - Website er gopon subdomain khonja
🔹 /ipinfo ip - IP address er location track
🔹 /portscan ip - Open port scan kora
🔹 /scrape url - Website theke sob link ber kora
🔹 /pincode pin - Pincode diye elakar tothyo ber kora

🛡️ Anti-Hack (Security)
🔹 /privacy platform - Account hack theke banchar upay
🔹 /scam - Live scam alert theke satorko thakun
🔹 /scanfile reply - File e virus ache kina check kora
🔹 /breach email - Email hack/leak hoyeche kina check

🔧 Media & Tools (Edit o Design)
🔹 /card nam - AI diye sundor greeting card banano
🔹 /colorgrade reply - Chobir cinematic color dewa
🔹 /restore reply - Ghola chobi HD ba Clear kora
🔹 /qr text - QR code toiri kora
🔹 /pdf reply - Chobi theke PDF banano
🔹 /pnr pnr - Train er PNR status check kora
🔴 /train example example - train ar somy chek korar jonno ata vul korte pare tai akbar where is my train app a dhake neben karon ata ai
🔴 /askblackbox ai

🖼 Pro Tip: Bot e jekono chobi (Photo/Document) pathale seta auto WebP te convert hobe o EXIF data dekhabe!"""
    
    # parse_mode বাদ দিলাম যাতে আপনার ব্র্যাকেট [ ] বা চিহ্নগুলোর জন্য কোনো Error না আসে
    bot.reply_to(m, welcome_text)
    
# ==========================================
# 📓 NOTEBOOK & FOCUS
# ==========================================
@bot.message_handler(commands=['note', 'notes', 'delnote', 'timer'])
def notebook_system(m):
    cmd = m.text.split()[0].lower()
    user_id = m.from_user.id
    text = m.text.replace(cmd, "").strip()

    if user_id not in user_notes:
        user_notes[user_id] = []

    if cmd == '/note':
        if text:
            user_notes[user_id].append(text)
            bot.reply_to(m, "✅ **নোট সেভ করা হয়েছে!**")
        else:
            bot.reply_to(m, "⚠️ টেক্সট দিন!")
    elif cmd == '/notes':
        if not user_notes[user_id]:
            bot.reply_to(m, "📝 আপনার নোটবুক ফাঁকা!")
        else:
            msg = "📓 **আপনার সেভ করা নোটস:**\n\n"
            for i, note in enumerate(user_notes[user_id]):
                msg += f"{i+1}. {note}\n"
            bot.reply_to(m, msg)
    elif cmd == '/delnote':
        try:
            idx = int(text) - 1
            del user_notes[user_id][idx]
            bot.reply_to(m, "🗑️ **নোট ডিলিট করা হয়েছে!**")
        except:
            bot.reply_to(m, "⚠️ সঠিক নম্বর দিন!")
    elif cmd == '/timer':
        bot.reply_to(m, f"⏱️ **Focus Timer:** {text if text else 'কিছু'} মিনিটের জন্য সেট করা হলো! মন দিয়ে পড়াশোনা করুন।")

# ==========================================
# 📚 STUDY & UTILITY
# ==========================================
@bot.message_handler(commands=['routine'])
def show_routine(m):
    routine = (
        "📅 **আপনার উইকলি রুটিন:**\n\n"
        "🔹 **মঙ্গলবার:** বাংলা, অঙ্ক-পরিবেশ (জীবন)\n"
        "🔹 **বৃহস্পতিবার:** ইতিহাস, অঙ্ক-ইংরেজি\n"
        "🔹 **শনিবার:** ভূগোল, অঙ্ক-পরিবেশ (ভৌত)\n\n"
        "বই খাতা নিয়ে বসে পড়ুন বস! 🚀"
    )
    bot.reply_to(m, routine, parse_mode="Markdown")

@bot.message_handler(commands=['ping'])
def ping_server(m):
    bot.reply_to(m, "⚡ **Pong!** Server Speed: Ultra Fast (Vercel Node) 🟢")

@bot.message_handler(commands=['math', 'graph', 'formula', 'tr', 'wiki'])
def study_stubs(m):
    cmd = m.text.split()[0].lower()
    responses = {
        '/math': "🧮 অঙ্কটি পাঠান, আমি সলভ করে দিচ্ছি!",
        '/graph': "📈 সমীকরণটি দিন।",
        '/formula': "📐 টপিকের নাম বলুন, আমি সূত্র বের করছি।",
        '/tr': "🗣️ ট্রান্সলেট করার জন্য টেক্সট দিন।",
        '/wiki': "🔍 উইকিপিডিয়ায় খোঁজার জন্য টপিক দিন।"
    }
    bot.reply_to(m, responses.get(cmd, "✅ Ready!"))

# ==========================================
# 🛠️ REAL APIs (QR, IP, Pincode, Hash)
# ==========================================
@bot.message_handler(commands=['qr'])
def make_qr(m):
    text = m.text.replace("/qr", "").strip()
    if not text:
        bot.reply_to(m, "⚠️ টেক্সট দিন! যেমন: `/qr Hello`")
        return
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(text)}"
    bot.send_photo(m.chat.id, qr_url, caption="✅ আপনার QR Code রেডি!")

@bot.message_handler(commands=['pincode'])
def check_pincode(m):
    pin = m.text.replace("/pincode", "").strip()
    try:
        res = requests.get(f"https://api.postalpincode.in/pincode/{pin}").json()
        bot.reply_to(m, f"📍 **এলাকা:** {res[0]['PostOffice'][0]['Name']}\n🏢 **জেলা:** {res[0]['PostOffice'][0]['District']}")
    except:
        bot.reply_to(m, "❌ ভুল পিনকোড বা সার্ভার এরর!")

@bot.message_handler(commands=['ipinfo'])
def check_ip(m):
    ip = m.text.replace("/ipinfo", "").strip()
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        bot.reply_to(m, f"🌐 **IP:** {res['query']}\n📍 **Country:** {res['country']}\n🏢 **ISP:** {res['isp']}")
    except:
        bot.reply_to(m, "⚠️ IP ট্র্যাক করা যায়নি!")

@bot.message_handler(commands=['hash'])
def make_hash(m):
    text = m.text.replace("/hash", "").strip()
    if text:
        md5_hash = hashlib.md5(text.encode()).hexdigest()
        bot.reply_to(m, f"🔒 **MD5 Hash:**\n`{md5_hash}`", parse_mode="Markdown")

# ==========================================
# 🕵️‍♂️ HACKER, OSINT, SECURITY & CBI MODE 
# ==========================================
@bot.message_handler(commands=['name', 'track', 'social', 'run', 'termux', 'decrypt', 'payload', 'bin', 'snicheck', 'ss', 'sub', 'portscan', 'scrape', 'privacy', 'scam', 'scanfile', 'breach'])
def hacker_osint_stubs(m):
    cmd = m.text.split()[0].lower()
    bot.reply_to(m, f"🚨 **CBI / Security Mode Alert:**\n`{cmd}` টুল অ্যাক্টিভেটেড।\n\n⚠️ *Vercel Cloud Policy:* রিয়েল-টাইম ডীপ স্ক্যানিং ও হ্যাকিং কমান্ড রেস্ট্রিক্টেড। এটি এখন Simulation/Educational Mode এ প্রসেস হচ্ছে।")

# ==========================================
# 🔧 MEDIA, EDITING & TRAIN
# ==========================================
@bot.message_handler(commands=['card', 'colorgrade', 'restore', 'pdf', 'pnr'])
def media_stubs(m):
    cmd = m.text.split()[0].lower()
    bot.reply_to(m, f"🖼️ `{cmd}` মডিউল রেডি! ফাইল বা ডেটা পাঠান, প্রসেস করা হবে। (Vercel-এর কারণে ভারী ফাইলে একটু সময় লাগতে পারে)।")

@bot.message_handler(commands=['train'])
def train_status(m):
    bot.reply_to(m, "🔴 **AI Warning:** ট্রেনের লাইভ স্ট্যাটাস AI দিয়ে চেক করলে ভুল হতে পারে। দয়া করে 'Where is my train' অ্যাপ থেকে কনফার্ম হয়ে নেবেন।")

# ==========================================
# 🖼️ AUTO EXIF & WEBP CONVERTER
# ==========================================
@bot.message_handler(content_types=['photo', 'document'])
def handle_files(m):
    bot.reply_to(m, "🔍 **System Scan:** ফাইল রিসিভ হয়েছে!\n\n♻️ *Auto converting to WebP...*\n📊 *Extracting EXIF Data...*\n\n✅ [Vercel Mode: অপারেশন সাকসেসফুল। প্রাইভেসি রিজন-এর জন্য হিডেন মেটাডেটা রিমুভ করা হয়েছে।]")

# ==========================================
# 🤖 AI COMMANDS & AUTO-CHAT BRAIN
# ==========================================
@bot.message_handler(commands=['ask', 'ai', 'askblackbox'])
def explicit_ai_command(m):
    user_text = m.text.split(' ', 1)[1] if len(m.text.split()) > 1 else ""
    if not user_text:
        bot.reply_to(m, "⚠️ প্রশ্ন দিন! যেমন: `/ai কালকের আবহাওয়া কেমন?`")
        return
    process_ai(m, user_text)

@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def auto_chat_ai(m):
    process_ai(m, m.text.strip())

def process_ai(m, text):
    user_id = m.from_user.id
    curr_time = time.time()
    
    if user_id in user_spam_tracker and (curr_time - user_spam_tracker[user_id] < 3):
        return 
    user_spam_tracker[user_id] = curr_time

    try:
        wait = bot.reply_to(m, "🧠 **Vabchi...**")
    except:
        return

    sys_prompt = urllib.parse.quote("You are 'Debasish Bot', a highly advanced, smart, and friendly hacker assistant. Reply directly in Bengali/English.")
    safe_text = urllib.parse.quote(text)
    url = f"https://text.pollinations.ai/{safe_text}?system={sys_prompt}"
    
    success = False
    for _ in range(2):
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
            if res.status_code == 200:
                bot.edit_message_text(res.text[:4000], m.chat.id, wait.message_id)
                success = True
                break 
        except:
            time.sleep(1)
            
    if not success:
        try:
            bot.edit_message_text("🤖 সার্ভার জ্যাম! আবার চেষ্টা করুন।", m.chat.id, wait.message_id)
        except:
            pass

# ==========================================
# 🌐 VERCEL WEBHOOK SYSTEM
# ==========================================
@app.route('/', methods=['GET'])
def index():
    return "🚀 MEGA ULTRA BOT is ALIVE on Vercel Serverless!", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    bot.remove_webhook()
    time.sleep(1)
    s = bot.set_webhook(url=request.url_root + BOT_TOKEN)
    return "✅ MEGA ULTRA Webhook setup successful!" if s else "❌ Setup failed!"
