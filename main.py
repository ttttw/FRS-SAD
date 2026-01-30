from instagrapi import Client
import time
import os
import random

# جلب البيانات من إعدادات الاستضافة (Render) وليس من الكود
USERNAME = os.getenv('IG_USERNAME')
PASSWORD = os.getenv('IG_PASSWORD')

MY_COMMENT = "عائلتنا بالتليجرام غير! ❤️ هناك نسولف براحتنا وننزل كواليس وتفاصيل ما تشوفوها هنا. تعالوا لمتنا تجنن وما تكتمل إلا بيكم.. الرابط فوگ بالبروفايل، انتظركم"

def start_bot():
    if not USERNAME or not PASSWORD:
        print("❌ خطأ: لم يتم ضبط اليوزر والباسورد في إعدادات Render!")
        return

    cl = Client()
    # ملاحظة: في الاستضافات السحابية مثل Render، ملفات Session قد تُحذف عند إعادة التشغيل
    # لذا سنعتمد على تسجيل الدخول المباشر أو استخدام Persistent Storage
    
    try:
        print(f"🔐 محاولة تسجيل الدخول للحساب: {USERNAME}")
        cl.login(USERNAME, PASSWORD)
        print("✅ تم الدخول بنجاح")
        
        while True:
            try:
                print("🔎 سحب منشورات من الاكسبلور...")
                medias = cl.explore_medias(amount=12)
                
                for media in medias:
                    if media.user.username == USERNAME:
                        continue
                        
                    wait_time = random.randint(5, 60) 
                    print(f"⏳ انتظار {wait_time} ثانية...")
                    time.sleep(wait_time)
                    
                    try:
                        cl.media_comment(media.id, MY_COMMENT)
                        print(f"✅ تم التعليق على: {media.id}")
                    except Exception as e:
                        print(f"⚠️ فشل التعليق: {e}")
                        if "feedback_required" in str(e):
                            time.sleep(1800)
                        continue
                
                # الاستراحة الطويلة المتفاوتة (نص ساعة إلى ساعة ونصف)
                long_break = random.randint(1800, 5400)
                print(f"💤 استراحة طويلة لمدة {long_break // 60} دقيقة...")
                time.sleep(long_break)

            except Exception as e:
                print(f"🛑 خطأ في الدورة: {e}")
                time.sleep(600)
                
    except Exception as e:
        print(f"🚫 فشل نهائي: {e}")

if __name__ == "__main__":
    start_bot()
