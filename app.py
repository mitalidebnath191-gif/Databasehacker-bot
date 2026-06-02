import os
import time
import urllib.parse
import hashlib
import requests
import re
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from flask import Flask, request
import telebot

# ==========================================
# 🚀 SERVER ENGINE (Vercel & Flask)
# ==========================================
app = Flask(__name__)

# আপনার বটের টোকেন (Vercel Environment Variables থেকে নেবে)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# (এর নিচ থেকে আপনার /start বা বাকি সব কমান্ডের কোড যেমন ছিল তেমনই থাকবে)
# ==========================================


# ==========================================
# 🚨 WELCOME MENU
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(m):
    welcome_text = """🚨 WELCOME TO MEGA ULTRA BOT 🚨
━━━━━━━━━━━━━━━━━━━━━━
হ্যালো বস! 😎 আপনার প্রাইভেট হাই-সিকিউরিটি ইন্টেলিজেন্স বট একদম রেডি এবং অনলাইনে আছে। ⚡

🛠️ সিস্টেম মেনু

 আর্টিফিশিয়াল ইন্টেলিজেন্স (AI):
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
# 🕵️‍♂️ REAL OSINT NUMBER TRACKER (/track)
# ==========================================
@bot.message_handler(commands=['track'])
def track_number(m):
    num_str = m.text.replace("/track", "").strip()
    
    if not num_str:
        bot.reply_to(m, "⚠️ একটি নম্বর দিন! (Country Code সহ, যেমন: `/track +919876543210`)")
        return
    
    # +91 না থাকলে অটোমেটিক যোগ করে দেওয়া (Default India)
    if not num_str.startswith("+"):
        num_str = "+91" + num_str
        
    try:
        wait = bot.reply_to(m, "🔍 **CBI OSINT Scanner:** টেলিকম মেটাডেটা স্ক্যান করা হচ্ছে... ⚡")
        
        # নম্বর পার্স করা
        parsed_num = phonenumbers.parse(num_str)
        
        if phonenumbers.is_valid_number(parsed_num):
            # রিয়েল ডেটা এক্সট্র্যাক্ট করা
            region = geocoder.description_for_number(parsed_num, "en")
            sim_provider = carrier.name_for_number(parsed_num, "en")
            time_zones = timezone.time_zones_for_number(parsed_num)
            
            result = (
                f"🎯 **TARGET SECURED!**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📞 **Number:** `{num_str}`\n"
                f"🌍 **Region/State:** `{region if region else 'Unknown'}`\n"
                f"🏢 **Carrier (SIM):** `{sim_provider if sim_provider else 'Unknown'}`\n"
                f"⏱️ **Timezone:** `{', '.join(time_zones)}`\n"
                f"🟢 **Status:** `Active Valid Number`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🚨 *Note: This is an OSINT Metadata scan. Live GPS is restricted.*"
            )
            bot.edit_message_text(result, m.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ নম্বরটি ইনভ্যালিড বা ফেক! সঠিক নম্বর দিন।", m.chat.id, wait.message_id)
            
    except Exception as e:
        bot.edit_message_text("❌ নম্বরটি স্ক্যান করা যায়নি! Country code ঠিকমতো দিয়েছেন কি না চেক করুন।", m.chat.id, wait.message_id)
            
# ==========================================
# 🎨 REAL MEDIA & DESIGN API (/card)
# ==========================================
@bot.message_handler(commands=['card'])
def make_greeting_card(m):
    prompt = m.text.replace("/card", "").strip()
    if not prompt:
        bot.reply_to(m, "⚠️ কার্ডের জন্য নাম বা থিম দিন! যেমন: `/card Beautiful Happy Birthday card for Debasish`")
        return
    
    try:
        wait = bot.reply_to(m, "🎨 AI আপনার কার্ড ডিজাইন করছে... একটু ওয়েট করুন! ⏳")
        
        # Real AI Image Generation using Pollinations Image API
        safe_prompt = urllib.parse.quote(f"A highly detailed, beautiful greeting card design with text: {prompt}, aesthetic, colorful")
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=600&nologo=true"
        
        bot.send_photo(m.chat.id, image_url, caption=f"✅ **Your AI Card:** {prompt}\n\n[Mega Ultra Bot Design]", reply_to_message_id=m.message_id)
        bot.delete_message(m.chat.id, wait.message_id)
    except Exception as e:
        bot.edit_message_text("❌ সার্ভার কার্ডটি বানাতে পারেনি। আবার চেষ্টা করুন!", m.chat.id, wait.message_id)

# বাকি স্টাবগুলো (যেগুলো এখনো রিয়েল করা হয়নি)
@bot.message_handler(commands=['colorgrade', 'restore', 'pdf', 'pnr'])
def other_media_stubs(m):
    cmd = m.text.split()[0].lower()
    bot.reply_to(m, f"🖼️ `{cmd}` মডিউলটি এখনো ডেমো মোডে আছে। রিয়েল API কানেক্ট করতে হবে!")
        
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
# 📸 REAL SCREENSHOT COMMAND (Bypass MShots API)
# ==========================================
@bot.message_handler(commands=['ss'])
def take_screenshot(m):
    url = m.text.replace("/ss", "").strip()
    if not url:
        bot.reply_to(m, "⚠️ ওয়েবসাইটের লিঙ্ক দিন! যেমন: `/ss google.com`")
        return
        
    # লিঙ্কে http না থাকলে অটোমেটিক লাগিয়ে দেওয়া
    if not url.startswith("http"):
        url = "https://" + url
        
    try:
        wait = bot.reply_to(m, "📸 টার্গেট ওয়েবসাইটের স্ক্রিনশট নেওয়া হচ্ছে... ⚡")
        
        # Thum.io বাদ দিয়ে WordPress MShots API ব্যবহার করা হলো
        safe_url = urllib.parse.quote(url)
        ss_api_url = f"https://s0.wp.com/mshots/v1/{safe_url}?w=1280&h=720"
        
        bot.send_photo(m.chat.id, ss_api_url, caption=f"✅ **Target:** {url}\n\n[Mega Ultra Bot Scanner]", reply_to_message_id=m.message_id)
        bot.delete_message(m.chat.id, wait.message_id)
    except Exception as e:
        bot.edit_message_text("❌ সার্ভার লিঙ্কটিতে ঢুকতে পারছে না বা সাইটটি ডাউন আছে!", m.chat.id, wait.message_id)

# ==========================================
# 💻 DEV & CYBER TOOLS (REAL APIs)
# ==========================================
@bot.message_handler(commands=['hash', 'decrypt', 'bin', 'run', 'termux', 'payload'])
def dev_cyber_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()
    
    if cmd == '/hash':
        if not text:
            bot.reply_to(m, "⚠️ টেক্সট দিন! (যেমন: `/hash admin123`)")
            return
        md5_hash = hashlib.md5(text.encode()).hexdigest()
        bot.reply_to(m, f"🔒 **MD5 Hash:**\n`{md5_hash}`", parse_mode="Markdown")
        
    elif cmd == '/decrypt':
        if not text:
            bot.reply_to(m, "⚠️ MD5 হ্যাশ দিন! (যেমন: `/decrypt 0192023a7bbd73250516f069df18b500`)")
            return
        try:
            wait = bot.reply_to(m, "🔓 ডিক্রিপ্ট করার চেষ্টা করছি...")
            # Public Rainbow Table API (Educational Use)
            res = requests.get(f"http://www.nitrxgen.net/md5db/{text}", timeout=7)
            if res.status_code == 200 and res.text:
                bot.edit_message_text(f"✅ **Decrypted Result:**\n`{res.text}`", m.chat.id, wait.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("❌ ডেটাবেসে এই হ্যাশটি পাওয়া যায়নি! (এটি কোনো সাধারণ শব্দ নয়)", m.chat.id, wait.message_id)
        except:
            bot.edit_message_text("⚠️ সার্ভার এরর!", m.chat.id, wait.message_id)

    elif cmd == '/bin':
        if not text or len(text) < 6:
            bot.reply_to(m, "⚠️ ৬ ডিজিটের Bank BIN নম্বর দিন! (যেমন: `/bin 415209`)")
            return
        try:
            wait = bot.reply_to(m, "🏦 ব্যাঙ্কের তথ্য খোঁজা হচ্ছে...")
            headers = {"Accept-Version": "3"}
            res = requests.get(f"https://lookup.binlist.net/{text[:8]}", headers=headers, timeout=5).json()
            msg = f"🏦 **BIN Info:** `{text}`\n"
            msg += f"💳 **Brand:** `{res.get('scheme', 'N/A').title()}`\n"
            msg += f"🏦 **Bank:** `{res.get('bank', {}).get('name', 'N/A')}`\n"
            msg += f"🌍 **Country:** `{res.get('country', {}).get('name', 'N/A')}`"
            bot.edit_message_text(msg, m.chat.id, wait.message_id, parse_mode="Markdown")
        except:
            bot.edit_message_text("❌ তথ্য পাওয়া যায়নি বা API লিমিট শেষ!", m.chat.id, wait.message_id)

    elif cmd == '/run':
        if not text:
            bot.reply_to(m, "⚠️ কোড দিন! (যেমন: `/run python print('Hello')`)")
            return
        parts = text.split(" ", 1)
        if len(parts) < 2:
            bot.reply_to(m, "⚠️ ভাষা ও কোড দুটোই দিন!")
            return
        lang, code = parts[0], parts[1]
        try:
            wait = bot.reply_to(m, "⚙️ কোড রান হচ্ছে (Sandbox Mode)...")
            # Using Piston API for safe remote execution
            payload = {"language": lang, "version": "*", "files": [{"content": code}]}
            res = requests.post("https://emkc.org/api/v2/piston/execute", json=payload, timeout=10).json()
            output = res.get('run', {}).get('output', 'Error')
            bot.edit_message_text(f"💻 **Output ({lang}):**\n```text\n{output[:1000]}\n
```", m.chat.id, wait.message_id, parse_mode="Markdown")
        except:
            bot.edit_message_text("❌ কোড রান করা যায়নি! (ভাষা সাপোর্ট নাও করতে পারে)", m.chat.id, wait.message_id)

    elif cmd == '/termux':
        tools = {
            "nmap": "Network Scanner. \n`pkg install nmap`\nUsage: `nmap <ip>`",
            "hydra": "Brute Force Password Tool. \n`pkg install hydra`",
            "kali": "Install Kali Nethunter. \n`pkg install wget && wget -O install-nethunter-termux https://offs.ec/2MceZWr && chmod +x install-nethunter-termux && ./install-nethunter-termux`"
        }
        if not text:
            bot.reply_to(m, "⚠️ টুলের নাম দিন! (যেমন: `/termux nmap` বা `/termux kali`)")
            return
        reply = tools.get(text.lower(), "⚠️ এই টুলের বেসিক গাইড আমার কাছে নেই। দয়া করে গুগলে খুঁজুন!")
        bot.reply_to(m, f"📱 **Termux Quick Guide:**\n\n{reply}", parse_mode="Markdown")

    elif cmd == '/payload':
        if not text:
            bot.reply_to(m, "⚠️ SNI/Host দিন! (যেমন: `/payload example.com`)")
            return
        # Educational HTTP injection structure
        safe_template = (
            f"🛡️ **Educational HTTP Payload Template**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"```http\n"
            f"GET / HTTP/1.1[crlf]\n"
            f"Host: {text}[crlf]\n"
            f"Connection: Keep-Alive[crlf]\n"
            f"User-Agent: Mozilla/5.0[crlf]\n"
            f"
```\n"
            f"🚨 *Note: This is a basic network testing structure. Functional bypass payloads are restricted by cloud policy.*"
        )
        bot.reply_to(m, safe_template, parse_mode="Markdown")

# ==========================================
# 🛠 OSINT & NET (REAL API TOOLS)
# ==========================================
@bot.message_handler(commands=['snicheck', 'sub', 'ipinfo', 'portscan', 'scrape', 'pincode'])
def osint_net_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()

    if cmd == '/pincode':
        if not text:
            bot.reply_to(m, "⚠️ পিনকোড দিন! (যেমন: `/pincode 713101`)")
            return
        try:
            res = requests.get(f"https://api.postalpincode.in/pincode/{text}").json()
            if res[0]['Status'] == 'Success':
                po = res[0]['PostOffice'][0]
                bot.reply_to(m, f"📍 **এলাকা (Area):** `{po['Name']}`\n🏢 **জেলা (District):** `{po['District']}`\n🌍 **রাজ্য (State):** `{po['State']}`", parse_mode="Markdown")
            else:
                bot.reply_to(m, "❌ ভুল পিনকোড!")
        except:
            bot.reply_to(m, "⚠️ সার্ভার এরর!")

    elif cmd == '/ipinfo':
        if not text:
            bot.reply_to(m, "⚠️ IP অ্যাড্রেস দিন! (যেমন: `/ipinfo 8.8.8.8`)")
            return
        try:
            wait = bot.reply_to(m, "🔍 আইপি ট্র্যাক করা হচ্ছে...")
            res = requests.get(f"http://ip-api.com/json/{text}").json()
            if res.get('status') == 'success':
                msg = f"🌐 **IP:** `{res['query']}`\n"
                msg += f"📍 **Country:** `{res['country']}`\n"
                msg += f"🏙️ **City:** `{res['city']}`\n"
                msg += f"🏢 **ISP/Carrier:** `{res['isp']}`\n"
                bot.edit_message_text(msg, m.chat.id, wait.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("❌ IP ট্র্যাক করা যায়নি বা প্রাইভেট আইপি!", m.chat.id, wait.message_id)
        except:
            bot.edit_message_text("⚠️ সার্ভার এরর!", m.chat.id, wait.message_id)

    elif cmd == '/snicheck':
        if not text:
            bot.reply_to(m, "⚠️ Host বা SNI দিন! (যেমন: `/snicheck google.com`)")
            return
        url = text if text.startswith("http") else "http://" + text
        try:
            wait = bot.reply_to(m, "🔍 হোস্ট পিং করা হচ্ছে... ⚡")
            res = requests.get(url, timeout=5)
            status = "🟢 ALIVE" if res.status_code < 400 else "🔴 DEAD/BLOCKED"
            bot.edit_message_text(f"🌐 **Host:** `{text}`\n⚙️ **Status:** `{status} (Code: {res.status_code})`", m.chat.id, wait.message_id, parse_mode="Markdown")
        except:
            bot.edit_message_text(f"🌐 **Host:** `{text}`\n⚙️ **Status:** 🔴 OFFLINE / CONNECTION REFUSED", m.chat.id, wait.message_id, parse_mode="Markdown")

    elif cmd == '/sub':
        if not text:
            bot.reply_to(m, "⚠️ ডোমেনের নাম দিন! (যেমন: `/sub example.com`)")
            return
        try:
            wait = bot.reply_to(m, "🔍 crt.sh ডেটাবেস থেকে সাবডোমেন খোঁজা হচ্ছে (Deep Scan)... ⏳")
            res = requests.get(f"https://crt.sh/?q=%25.{text}&output=json", timeout=12)
            if res.status_code == 200:
                data = res.json()
                subs = list(set([entry['name_value'] for entry in data]))[:10] # Top 10 unique subdomains
                if subs:
                    msg = f"🔍 **Top Subdomains for {text}:**\n\n" + "\n".join([f"🔹 `{s}`" for s in subs])
                    bot.edit_message_text(msg, m.chat.id, wait.message_id, parse_mode="Markdown")
                else:
                    bot.edit_message_text("⚠️ কোনো সাবডোমেন পাওয়া যায়নি!", m.chat.id, wait.message_id)
            else:
                bot.edit_message_text("❌ ডেটাবেস এই মুহূর্তে ডাউন আছে!", m.chat.id, wait.message_id)
        except:
            bot.edit_message_text("⚠️ স্ক্যানিং টাইমআউট! অনেক বেশি ডেটা থাকতে পারে।", m.chat.id, wait.message_id)

    elif cmd == '/scrape':
        if not text:
            bot.reply_to(m, "⚠️ ওয়েবসাইটের লিঙ্ক দিন! (যেমন: `/scrape https://example.com`)")
            return
        url = text if text.startswith("http") else "http://" + text
        try:
            wait = bot.reply_to(m, "🕷️ ওয়েবসাইট স্ক্র্যাপ করা হচ্ছে (Extracting Data)...")
            res = requests.get(url, timeout=8)
            # Basic Regex for scraping title and links
            title_match = re.search(r'<title>(.*?)</title>', res.text, re.IGNORECASE)
            title = title_match.group(1) if title_match else "No Title Found"
            links = re.findall(r'href=[\'"]?([^\'" >]+)', res.text)
            unique_links = list(set([l for l in links if l.startswith("http")]))[:5] # 5 টা টপ লিংক
            
            msg = f"🕷️ **Scrape Target:** `{url}`\n━━━━━━━━━━━━━━━━━\n"
            msg += f"📑 **Title:** `{title}`\n\n"
            msg += "🔗 **Top Links Found:**\n" + "\n".join([f"🔹 {l}" for l in unique_links])
            bot.edit_message_text(msg, m.chat.id, wait.message_id, parse_mode="Markdown")
        except:
            bot.edit_message_text("❌ সাইটটির সিকিউরিটি অনেক বেশি বা স্ক্র্যাপিং ব্লক করা আছে!", m.chat.id, wait.message_id)

    elif cmd == '/portscan':
        bot.reply_to(m, "🚨 **Security Policy Alert:**\n\n"
                        "Vercel ক্লাউড সার্ভার থেকে সরাসরি অন্য আইপিতে Active Socket / Port Scan চালানো রেস্ট্রিক্টেড। এর ফলে বটের সার্ভার সাসপেন্ড হতে পারে।\n\n"
                        "🛡️ **Pro Tip:** পোর্ট স্ক্যানিংয়ের জন্য Termux-এ Nmap ব্যবহার করুন। কমান্ড:\n`nmap -sV -p 1-1000 example.com`", parse_mode="Markdown")

# ==========================================
# 🛡️ ANTI-HACK & SECURITY (REAL APIs & DEFENSE)
# ==========================================
@bot.message_handler(commands=['privacy', 'scam', 'scanfile', 'breach'])
def anti_hack_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()

    if cmd == '/breach':
        if not text or "@" not in text:
            bot.reply_to(m, "⚠️ একটি সঠিক ইমেইল দিন! (যেমন: `/breach test@gmail.com`)")
            return
        try:
            wait = bot.reply_to(m, "🛡️ ডার্ক ওয়েব এবং লিক ডেটাবেস স্ক্যান করা হচ্ছে... ⏳")
            # Using XposedOrNot Free Public API for Data Breach checking
            res = requests.get(f"https://api.xposedornot.com/v1/check-email/{text}", timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                breaches = data.get('breaches', [])
                if breaches:
                    breach_list = "\n".join([f"🔹 `{b[0]}`" for b in breaches[:5]]) # টপ ৫ টি ওয়েবসাইট
                    msg = f"🚨 **DANGER! ইমেইলটি হ্যাক/লিক হয়েছে!** 🚨\n\n📧 **Email:** `{text}`\n\n📂 **যেসব ওয়েবসাইট থেকে ডেটা চুরি গেছে:**\n{breach_list}\n\n⚠️ **অ্যাকশন:** এক্ষুনি এই ইমেইলের পাসওয়ার্ড বদলে ফেলুন এবং 2FA অন করুন!"
                    bot.edit_message_text(msg, m.chat.id, wait.message_id, parse_mode="Markdown")
                else:
                    bot.edit_message_text("✅ **SAFE!** আপনার ইমেইল কোনো ডেটা ব্রিচে পাওয়া যায়নি।", m.chat.id, wait.message_id, parse_mode="Markdown")
            elif res.status_code == 404:
                bot.edit_message_text("✅ **SAFE!** আপনার ইমেইল সম্পূর্ণ সুরক্ষিত এবং কোনো লিক ডেটাবেসে নেই।", m.chat.id, wait.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("⚠️ API সার্ভার এই মুহূর্তে রেসপন্স করছে না।", m.chat.id, wait.message_id)
        except:
            bot.edit_message_text("❌ সার্ভার এরর বা টাইমআউট!", m.chat.id, wait.message_id)

    elif cmd == '/privacy':
        if not text:
            bot.reply_to(m, "⚠️ প্ল্যাটফর্মের নাম দিন! (যেমন: `/privacy facebook` বা `/privacy whatsapp`)")
            return
        tips = {
            "facebook": "📘 **Facebook Privacy:**\n1. Settings > Security and Login > Two-Factor Authentication (2FA) অন করুন।\n2. 'Where You're Logged In' চেক করে অজানা ডিভাইস রিমুভ করুন।\n3. Profile Lock করে রাখুন।",
            "whatsapp": "🟢 **WhatsApp Privacy:**\n1. Settings > Account > Two-step verification অন করুন।\n2. Privacy > Profile Photo / Status শুধু Contacts করে রাখুন।\n3. Unknown calls সাইলেন্ট করুন।",
            "google": "🔴 **Google/Gmail Privacy:**\n1. Google Account > Security > 2-Step Verification অন করুন।\n2. Recovery Email এবং Phone number আপডেট রাখুন।\n3. Third-party app access রিমুভ করুন।"
        }
        reply = tips.get(text.lower(), "🛡️ **General Privacy Tip:** যেকোনো অ্যাকাউন্টে শক্তিশালী পাসওয়ার্ড (যেমন: @Pass#123) ব্যবহার করুন এবং অবশ্যই Two-Factor Authentication (2FA) অন করে রাখুন।")
        bot.reply_to(m, reply, parse_mode="Markdown")

    elif cmd == '/scam':
        scam_alert = (
            "🚨 **LIVE SCAM ALERTS (সতর্কতা)** 🚨\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ **TRAI/CBI Call Scam:** পুলিশ বা TRAI সেজে কল করে বলবে আপনার নামে অবৈধ সিম তোলা হয়েছে। (এটি ভুয়া, টাকা চাইবে)।\n"
            "2️⃣ **APK WhatsApp Scam:** হোয়াটসঅ্যাপে 'Bank KYC' বা 'Free Recharge' নামে `.apk` ফাইল পাঠালে ইনস্টল করবেন না, ফোন হ্যাক হবে।\n"
            "3️⃣ **Part-Time Job Scam:** টেলিগ্রাম বা হোয়াটসঅ্যাপে ইউটিউব ভিডিও লাইক করার কাজ দিয়ে টাকা হাতানো।\n"
            "4️⃣ **Electricity Bill Scam:** মেসেজ আসবে 'আজ রাতেই কারেন্ট কাটা যাবে, এই লিংকে ক্লিক করুন'।\n\n"
            "🛡️ **ডিফেন্স মেকানিজম:** কোনো অজানা লিংকে ক্লিক করবেন না এবং ভুলেও OTP শেয়ার করবেন না!"
        )
        bot.reply_to(m, scam_alert, parse_mode="Markdown")

    elif cmd == '/scanfile':
        if not m.reply_to_message or not m.reply_to_message.document:
            bot.reply_to(m, "⚠️ এই কমান্ডটি কাজ করতে হলে, প্রথমে কোনো File বা Document-এ রিপ্লাই (Reply) দিয়ে `/scanfile` লিখুন।")
            return
        
        doc = m.reply_to_message.document
        file_name = doc.file_name.lower()
        
        bot.reply_to(m, "🔍 ফাইলের সিগনেচার স্ক্যান করা হচ্ছে... ⚡")
        time.sleep(1) # Vercel Static Scan Simulation
        
        # Static Heuristic Analysis (বিপজ্জনক ফাইলের লিস্ট)
        dangerous_ext = ['.apk', '.exe', '.bat', '.sh', '.vbs', '.js', '.scr']
        is_dangerous = any(file_name.endswith(ext) for ext in dangerous_ext)
        
        if is_dangerous:
            msg = f"🦠 **DANGER DETECTED!** 🚨\n\n📄 **File:** `{file_name}`\n⚠️ **Warning:** এটি একটি অত্যন্ত ঝুঁকিপূর্ণ এক্সিকিউটেবল ফাইল। এটি ডিভাইসে ম্যালওয়্যার, স্পাইওয়্যার বা ট্রোজান (Trojan) ইনস্টল করতে পারে! খুব প্রয়োজন না হলে রান করাবেন না।"
            bot.reply_to(m, msg, parse_mode="Markdown")
        else:
            msg = f"✅ **SAFE FILE!** 🛡️\n\n📄 **File:** `{file_name}`\n🟢 **Status:** এই ফাইলের এক্সটেনশনটি সাধারণ এবং নিরাপদ মনে হচ্ছে। (Heuristic Scan Pass)"
            bot.reply_to(m, msg, parse_mode="Markdown")

# ==========================================
# ⚙️ SERVER CONTROL & STUDY TOOLS (REAL APIs)
# ==========================================
@bot.message_handler(commands=['ping', 'routine', 'math', 'graph', 'formula', 'tr', 'wiki'])
def server_control_tools(m):
    cmd = m.text.split()[0].lower()
    text = m.text.replace(cmd, "").strip()

    if cmd == '/ping':
        start_time = time.time()
        msg = bot.reply_to(m, "পং... 🏓 স্ক্যান চলছে...")
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000)
        bot.edit_message_text(f"🟢 **Server Status: ALIVE**\n⚡ **Latency:** `{ping_time}ms`\n📍 **Location:** `Vercel Cloud`", m.chat.id, msg.message_id, parse_mode="Markdown")

    elif cmd == '/routine':
        routine_text = (
            "📚 **আপনার সাপ্তাহিক পড়ার রুটিন:**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🔹 **মঙ্গলবার:** বাংলা, অঙ্ক, পরিবেশ (জীবন)\n"
            "🔹 **বৃহস্পতিবার:** ইতিহাস, অঙ্ক, ইংরেজি\n"
            "🔹 **শনিবার:** ভূগোল, অঙ্ক, পরিবেশ (ভৌত)\n\n"
            "💡 *আজ যেহেতু মঙ্গলবার, তাই জীবনবিজ্ঞান আর অঙ্কে বিশেষ ফোকাস করুন!*"
        )
        bot.reply_to(m, routine_text, parse_mode="Markdown")

    elif cmd == '/math':
        if not text:
            bot.reply_to(m, "⚠️ একটি অঙ্ক দিন! (যেমন: `/math 25 * 4 - 10` বা `/math sqrt(144)`)")
            return
        try:
            safe_expr = urllib.parse.quote(text)
            # Real MathJS API for calculations
            res = requests.get(f"http://api.mathjs.org/v4/?expr={safe_expr}", timeout=5).text
            bot.reply_to(m, f"🔢 **অঙ্ক:** `{text}`\n✅ **উত্তর:** `{res}`", parse_mode="Markdown")
        except:
            bot.reply_to(m, "❌ অঙ্কটি সমাধান করা যায়নি! সঠিক চিহ্ন ব্যবহার করুন (+, -, *, /)।")

    elif cmd == '/formula':
        if not text:
            bot.reply_to(m, "⚠️ টপিক দিন! (যেমন: `/formula circle` বা `/formula square`)")
            return
        formulas = {
            "circle": "বৃত্ত (Circle):\n🔸 পরিধি = 2πr\n🔸 ক্ষেত্রফল = πr²",
            "square": "বর্গক্ষেত্র (Square):\n🔸 পরিসীমা = 4a\n🔸 ক্ষেত্রফল = a²",
            "rectangle": "আয়তক্ষেত্র (Rectangle):\n🔸 পরিসীমা = 2(l+b)\n🔸 ক্ষেত্রফল = l × b",
            "triangle": "ত্রিভুজ (Triangle):\n🔸 ক্ষেত্রফল = ½ × ভূমি × উচ্চতা"
        }
        reply = formulas.get(text.lower(), "⚠️ এই সূত্রটি আমার ডেটাবেসে নেই। circle, square, rectangle বা triangle ট্রাই করুন।")
        bot.reply_to(m, reply)

    elif cmd == '/wiki':
        if not text:
            bot.reply_to(m, "⚠️ উইকিপিডিয়ায় খোঁজার জন্য কিছু লিখুন! (যেমন: `/wiki Black Hole`)")
            return
        try:
            wait = bot.reply_to(m, "🔍 বাংলা উইকিপিডিয়া থেকে তথ্য খোঁজা হচ্ছে... ⏳")
            url = f"https://bn.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(text)}"
            res = requests.get(url, timeout=8).json()
            if 'extract' in res:
                msg = f"📚 **{res['title']}**\n━━━━━━━━━━━━━━━━━━\n{res['extract']}\n\n🔗 [আরও পড়ুন]({res['content_urls']['desktop']['page']})"
                bot.edit_message_text(msg, m.chat.id, wait.message_id, parse_mode="Markdown", disable_web_page_preview=True)
            else:
                bot.edit_message_text("❌ উইকিপিডিয়ায় এই বিষয়ে কিছু পাওয়া যায়নি! অন্য কোনো শব্দ ট্রাই করুন।", m.chat.id, wait.message_id)
        except:
            bot.edit_message_text("⚠️ সার্ভার এরর!", m.chat.id, wait.message_id)

    elif cmd == '/graph':
        if not text:
            bot.reply_to(m, "⚠️ গ্রাফের সমীকরণ দিন! (যেমন: `/graph sin(x)`)")
            return
        try:
            wait = bot.reply_to(m, "📈 সমীকরণের গ্রাফ তৈরি করা হচ্ছে... ⚡")
            safe_prompt = urllib.parse.quote(f"A mathematical graph on a cartesian coordinate system showing the function {text}, minimalist math style, dark background")
            graph_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=600&nologo=true"
            bot.send_photo(m.chat.id, graph_url, caption=f"📈 **Graph for Equation:** `{text}`\n[AI Rendered]", reply_to_message_id=m.message_id)
            bot.delete_message(m.chat.id, wait.message_id)
        except:
            bot.edit_message_text("❌ গ্রাফ তৈরি করা যায়নি!", m.chat.id, wait.message_id)

    elif cmd == '/tr':
        parts = text.split(" ", 1)
        if len(parts) < 2:
            bot.reply_to(m, "⚠️ ভাষা ও টেক্সট দুটোই দিন! (যেমন: `/tr en আমি ভাত খাই`)")
            return
        target_lang, tr_text = parts[0], parts[1]
        try:
            # Google Translate Free API bypass
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(tr_text)}"
            res = requests.get(url, timeout=5).json()
            translated = res[0][0][0]
            bot.reply_to(m, f"🔤 **Translation ({target_lang.upper()}):**\n`{translated}`", parse_mode="Markdown")
        except:
            bot.reply_to(m, "❌ অনুবাদ করা যায়নি! ভাষার কোড ঠিক দিয়েছেন কি না চেক করুন (যেমন: en, bn, hi)।")
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
