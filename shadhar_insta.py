import os
import random
import time
from datetime import datetime
from instagrapi import Client

# سحب المعلومات الحساسة من إعدادات Render (أمان 100%)
USERNAME = os.environ.get('INSTA_USER')
PASSWORD = os.environ.get('INSTA_PASS')

def get_styled_comment():
    base_text = "يا جماعة الخير، أنا أختكم، سدت كل الأبواب بوجهي وقررت أترزق الله بمتجري الخاص (شذر هوم) بدل ما أحتاج لأحد. الشغل مو سهل والمنافسة صعبة، بس عندي ثقة بالله وبغيرة أهل ديرتي. فدوة بس ادعموا الصفحة، متابعتكم هي رأس مالي. الله يستر على كل وحدة تدعمني ويوفق كل شاب يدعم حلمي"
    emojis = [" 🥺💔", " 🙏✨", " 📥🌹", " 🧿🤲", " 🦋💎", " ❤️🇮🇶"]
    selected_emoji = random.choice(emojis)
    return f"{base_text} {selected_emoji}"

def run_bot():
    cl = Client()
    # في Render، لا نضمن بقاء ملف الجلسة دائماً، لذا سنسجل الدخول عند كل تشغيل
    try:
        cl.login(USERNAME, PASSWORD)
        print("تم تسجيل الدخول بنجاح ✅")
    except Exception as e:
        print(f"فشل تسجيل الدخول: {e}")
        return

    while True:
        # نظام النوم (Render يعمل بتوقيت UTC، لذا انتبهي لفرق التوقيت)
        # توقيت العراق (UTC+3)، لذا الساعة 12 ليلاً بالعراق هي 9 مساءً UTC
        now_hour = datetime.utcnow().hour + 3
        if now_hour >= 24: now_hour -= 24
        
        if 0 <= now_hour < 6:
            print(f"وقت النوم بالعراق (الساعة {now_hour})... سبات 😴")
            time.sleep(1800)
            continue

        try:
            medias = cl.explore_medias(amount=5)
            for media in medias:
                if media.media_type == 2:
                    comment_text = get_styled_comment()
                    cl.media_comment(media.id, comment_text)
                    print(f"تم التعليق على ريلز {media.code}")
                    time.sleep(random.randint(400, 800)) # انتظار بشري
            time.sleep(1200)
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(600)

if __name__ == "__main__":
    run_bot()
