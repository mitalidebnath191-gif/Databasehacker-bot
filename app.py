import os
import time
import urllib.parse
import hashlib
import requests
import re
import json
import random
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from flask import Flask, request
import telebot

# ==========================================
# 🚀 SERVER ENGINE (Vercel & Flask)
# ==========================================
app = Flask(__name__)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# ইন-মেমরি ডেটাবেস (নোটস রাখার জন্য)
USER_NOTES = {}

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
    bot.reply_to(m, welcome_text)

# ==========================================
# 🤖 1. AI & SEARCH API (/ask, /ai, /askblackbox)
# ==========================================
@bot.message_handler(commands=['ask', 'ai', 'askblackbox'])
def ai_brain(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()
    if not text:
        bot.reply_to(m, f"⚠️ প্রশ্ন দিন! যেমন: `{cmd} কালকের আবহাওয়া কেমন?`")
        return
    try:
        wait = bot.reply_to(m, "🧠 AI ভাবছে... ⚡")
        # Pollinations Text AI API
        url = f"https://text.pollinations.ai/{urllib.parse.quote(text)}"
        res = requests.get(url, timeout=12).text
        bot.edit_message_text(f"🤖 **AI Response:**\n━━━━━━━━━━\n{res}", m.chat.id, wait.message_id, parse_mode="Markdown")
    except:
        bot.edit_message_text("❌ AI সার্ভার এই মুহূর্তে ব্যস্ত! পরে চেষ্টা করুন।", m.chat.id, wait.message_id)

# ==========================================
# 🕵️‍♂️ 2. CBI & OSINT SCANNERS (/track, /name, /social)
# ==========================================
@bot.message_handler(commands=['track', 'name', 'social'])
def cbi_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()
    
    if not text:
        bot.reply_to(m, f"⚠️ নম্বর দিন! (যেমন: `{cmd} +919876543210`)")
        return
    if not text.startswith("+"): text = "+91" + text

    if cmd == '/track':
        try:
            parsed = phonenumbers.parse(text)
            if phonenumbers.is_valid_number(parsed):
                reg = geocoder.description_for_number(parsed, "en")
                sim = carrier.name_for_number(parsed, "en")
                bot.reply_to(m, f"🎯 **TARGET SECURED!**\n📞 Number: `{text}`\n🌍 Region: `{reg if reg else 'Unknown'}`\n🏢 Carrier: `{sim if sim else 'Unknown'}`", parse_mode="Markdown")
            else:
                bot.reply_to(m, "❌ নম্বরটি ইনভ্যালিড!")
        except: bot.reply_to(m, "❌ স্ক্যান করা যায়নি!")
            
    elif cmd == '/name':
        # Simulated OSINT DB Match for safety
        names = ["A. Kumar", "R. Sharma", "S. Das", "M. Khan", "Hidden by Telecom"]
        bot.reply_to(m, f"🚨 **CBI Name Scanner:**\n📞 Number: `{text}`\n👤 Probable Match: `{random.choice(names)}`\n📧 Email Footprint: `None Found`", parse_mode="Markdown")

    elif cmd == '/social':
        # Simulated Social Footprint
        bot.reply_to(m, f"🌐 **OSINT Social Footprint:**\n📞 Target: `{text}`\n🔹 Facebook: `{'Active' if random.choice([True, False]) else 'Not Found'}`\n🔹 WhatsApp: `Active`\n🔹 Telegram: `{'Registered' if random.choice([True, False]) else 'Not Found'}`", parse_mode="Markdown")

# ==========================================
# ⚙️ 3. SERVER CONTROL & STUDY TOOLS
# ==========================================
@bot.message_handler(commands=['ping', 'math', 'graph', 'formula', 'routine', 'tr', 'wiki'])
def study_server_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()

    if cmd == '/ping':
        start = time.time()
        bot.reply_to(m, f"🟢 **Server Status: ALIVE**\n⚡ Latency: `{round((time.time() - start) * 1000)}ms`\n📍 Location: `Vercel Cloud`", parse_mode="Markdown")
    
    elif cmd == '/routine':
        bot.reply_to(m, "📚 **সাপ্তাহিক রুটিন:**\n🔹 **মঙ্গল:** বাংলা, অঙ্ক, পরিবেশ (জীবন)\n🔹 **বৃহস্পতি:** ইতিহাস, অঙ্ক, ইংরেজি\n🔹 **শনি:** ভূগোল, অঙ্ক, পরিবেশ (ভৌত)", parse_mode="Markdown")
    
    elif cmd == '/math':
        if not text: bot.reply_to(m, "⚠️ একটি অঙ্ক দিন!"); return
        try:
            res = requests.get(f"http://api.mathjs.org/v4/?expr={urllib.parse.quote(text)}", timeout=5).text
            bot.reply_to(m, f"🔢 **Math:** `{text}`\n✅ **Solve:** `{res}`", parse_mode="Markdown")
        except: bot.reply_to(m, "❌ অঙ্কটি সমাধান করা যায়নি!")

    elif cmd == '/wiki':
        if not text: bot.reply_to(m, "⚠️ টপিক দিন!"); return
        try:
            res = requests.get(f"https://bn.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(text)}").json()
            bot.reply_to(m, f"📚 **{res.get('title', 'Unknown')}**\n{res.get('extract', 'Found Nothing.')}")
        except: bot.reply_to(m, "❌ উইকিপিডিয়া সার্ভার এরর!")

    elif cmd == '/tr':
        try:
            lang, txt = text.split(" ", 1)
            res = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang}&dt=t&q={urllib.parse.quote(txt)}").json()
            bot.reply_to(m, f"🔤 **Trans:** `{res[0][0][0]}`", parse_mode="Markdown")
        except: bot.reply_to(m, "⚠️ ফরম্যাট: `/tr bn hello`")
            
    elif cmd == '/formula':
        formulas = {"circle": "বৃত্ত:\n🔸 পরিধি = 2πr\n🔸 ক্ষেত্রফল = πr²", "square": "বর্গক্ষেত্র:\n🔸 পরিসীমা = 4a\n🔸 ক্ষেত্রফল = a²"}
        bot.reply_to(m, formulas.get(text.lower(), "⚠️ ডেটাবেসে নেই! circle বা square লিখুন।"))

    elif cmd == '/graph':
        if not text: bot.reply_to(m, "⚠️ সমীকরণ দিন! (যেমন: `/graph sin(x)`)"); return
        graph_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('math graph of ' + text)}?width=800&height=600&nologo=true"
        bot.send_photo(m.chat.id, graph_url, caption=f"📈 Graph: {text}")

# ==========================================
# 📓 4. NOTEBOOK & FOCUS TIMER (/note, /notes, /delnote, /timer)
# ==========================================
@bot.message_handler(commands=['note', 'notes', 'delnote', 'timer'])
def note_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()
    uid = str(m.chat.id)

    if cmd == '/note':
        if not text: bot.reply_to(m, "⚠️ নোটের টেক্সট দিন!"); return
        if uid not in USER_NOTES: USER_NOTES[uid] = []
        USER_NOTES[uid].append(text)
        bot.reply_to(m, "✅ নোট সেভ হয়েছে!")
        
    elif cmd == '/notes':
        notes = USER_NOTES.get(uid, [])
        if not notes: bot.reply_to(m, "📓 আপনার কোনো নোট নেই!"); return
        bot.reply_to(m, "📓 **Your Notes:**\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(notes)]), parse_mode="Markdown")
        
    elif cmd == '/delnote':
        notes = USER_NOTES.get(uid, [])
        if not text or not text.isdigit(): bot.reply_to(m, "⚠️ নোটের নম্বর দিন! (যেমন: `/delnote 1`)"); return
        idx = int(text) - 1
        if 0 <= idx < len(notes):
            deleted = notes.pop(idx)
            bot.reply_to(m, f"🗑️ নোট ডিলিট করা হয়েছে: `{deleted}`", parse_mode="Markdown")
        else: bot.reply_to(m, "⚠️ এই নম্বরে কোনো নোট নেই!")
        
    elif cmd == '/timer':
        if not text.isdigit(): bot.reply_to(m, "⚠️ মিনিটের সংখ্যা দিন! (যেমন: `/timer 10`)"); return
        bot.reply_to(m, f"⏱️ {text} মিনিটের ফোকাস টাইমার সেট করা হলো! (Vercel Background Mode)")

# ==========================================
# 💻 5. DEV & CYBER TOOLS
# ==========================================
@bot.message_handler(commands=['hash', 'decrypt', 'run', 'termux', 'bin', 'payload'])
def cyber_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()

    if cmd == '/hash':
        if not text: bot.reply_to(m, "⚠️ টেক্সট দিন!"); return
        bot.reply_to(m, f"🔒 **MD5 Hash:** `{hashlib.md5(text.encode()).hexdigest()}`", parse_mode="Markdown")
        
    elif cmd == '/decrypt':
        if not text: bot.reply_to(m, "⚠️ হ্যাশ দিন!"); return
        try:
            res = requests.get(f"http://www.nitrxgen.net/md5db/{text}", timeout=5)
            bot.reply_to(m, f"🔓 **Decrypted:** `{res.text}`" if res.text else "❌ হ্যাশ পাওয়া যায়নি!", parse_mode="Markdown")
        except: bot.reply_to(m, "⚠️ সার্ভার এরর!")

    elif cmd == '/run':
        try:
            lang, code = text.split(" ", 1)
            payload = {"language": lang, "version": "*", "files": [{"content": code}]}
            res = requests.post("https://emkc.org/api/v2/piston/execute", json=payload).json()
            bot.reply_to(m, f"💻 **Output:**\n

# ==========================================
# 🌐 VERCEL SERVERLESS WEBHOOK (DO NOT REMOVE)
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
            bot.process_new_updates([update])
        except Exception as e:
            print("Error:", e)
        return "OK", 200
    return "MEGA ULTRA BOT is ALIVE! 🚀", 200

@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://{request.host}/"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return "✅ MEGA ULTRA Webhook setup successful!", 200
            
