import os
import random
import time
import threading
from datetime import datetime
from flask import Flask
from instagrapi import Client

# --- كود الوهمي لتشغيل الخدمة كـ Web Service مجاناً ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- إعدادات البوت ---
USERNAME = os.environ.get('INSTA_USER')
PASSWORD = os.environ.get('INSTA_PASS')

def get_styled_comment():
    base_text = "يا جماعة الخير، أنا أختكم، سدت كل الأبواب بوجهي وقررت أترزق الله بمتجري الخاص (شذر هوم) بدل ما أحتاج لأحد. الشغل مو سهل والمنافسة صعبة، بس عندي ثقة بالله وبغيرة أهل ديرتي. فدوة بس ادعموا الصفحة، متابعتكم هي رأس مالي. الله يستر على كل وحدة تدعمني ويوفق كل شاب يدعم حلمي"
    emojis = [" 🥺💔", " 🙏✨", " 📥🌹", " 🧿🤲", " 🦋💎", " ❤️🇮🇶"]
    return f"{base_text} {random.choice(emojis)}"

def bot_logic():
    cl = Client()
    try:
        cl.login(USERNAME, PASSWORD)
        print("تم تسجيل الدخول بنجاح ✅")
    except Exception as e:
        print(f"فشل تسجيل الدخول: {e}")
        return

    while True:
        now_hour = (datetime.utcnow().hour + 3) % 24
        if 0 <= now_hour < 6:
            print(f"وقت النوم بالعراق ({now_hour})... سبات 😴")
            time.sleep(1800)
            continue

        try:
            medias = cl.explore_medias(amount=5)
            for media in medias:
                if media.media_type == 2:
                    comment_text = get_styled_comment()
                    try:
                        cl.media_comment(media.id, comment_text)
                        print(f"تم التعليق ✅")
                    except:
                        time.sleep(1200)
                    time.sleep(random.randint(450, 900))
            time.sleep(1200)
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(600)

if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خيط (Thread) منفصل
    t = threading.Thread(target=run_flask)
    t.start()
    # تشغيل منطق البوت
    bot_logic()
