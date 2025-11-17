import requests
import json
import time

TOKEN = "8286188115:AAE4aGQvPIWZkX4GByNllhOoo0ae4etYNY4"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = 0

def get_updates():
    global last_update_id
    url = f"{BASE_URL}/getUpdates"
    params = {"offset": last_update_id + 1, "timeout": 30}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json().get("result", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_main_menu():
    keyboard = [
        [{"text": "لیست ایونت ها", "callback_data": "events"}],
        [{"text": "مدیریت کشور", "callback_data": "manage_country"}],
        [{"text": "خرید عادی", "callback_data": "normal_shop"}],
        [{"text": "خرید وی آی پی", "callback_data": "vip_shop"}],
        [{"text": "پشتیبانی", "callback_data": "support"}],
        [{"text": "حمله نظامی", "callback_data": "military_attack"}],
        [{"text": "قوانین بازی", "callback_data": "rules"}],
        [{"text": "انتخاب کشور", "callback_data": "select_country"}]
    ]
    return {"inline_keyboard": keyboard}

def handle_callback(update):
    callback_data = update["callback_query"]["data"]
    chat_id = update["callback_query"]["message"]["chat"]["id"]
    
    if callback_data == "events":
        send_message(chat_id, "❌ در حال حاضر هیچ ایونتی فعال نیست.")
    
    elif callback_data == "manage_country":
        country_info = """
لیست_دارایی 📊

نام کشور:
💵بودجه کل: 1.5Mil
رضایت مردمی: 50%
امنیت: 50%
🌐اعتبار جهانی: 50%
        """
        send_message(chat_id, country_info)
    
    elif callback_data == "normal_shop":
        keyboard = {
            "inline_keyboard": [
                [{"text": "جنگنده", "callback_data": "shop_fighters"}],
                [{"text": "تانک", "callback_data": "shop_tanks"}],
                [{"text": "سرباز", "callback_data": "shop_soldiers"}],
                [{"text": "بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        send_message(chat_id, "🛒 فروشگاه عادی", keyboard)
    
    elif callback_data == "shop_fighters":
        fighters_text = """
[W]orld [W]ar [G]ame

✈️12جنگنده اف 4
💵قیمت:450K

✈️12جنگنده اف14
💵قیمت: 550K
        """
        send_message(chat_id, fighters_text)
    
    elif callback_data == "support":
        keyboard = {
            "inline_keyboard": [
                [{"text": "پیوی پشتیبانی", "url": "https://t.me/WorldWar_Support"}],
                [{"text": "بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        send_message(chat_id, "🛟 پشتیبانی", keyboard)
    
    elif callback_data == "vip_shop":
        keyboard = {
            "inline_keyboard": [
                [{"text": "آیدی شاپ وی آی پی", "url": "https://t.me/W0rldWarGameVIP"}],
                [{"text": "پیوی مالک", "url": "https://t.me/MrArmanQ"}],
                [{"text": "بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        send_message(chat_id, "💎 فروشگاه VIP", keyboard)
    
    elif callback_data == "military_attack":
        send_message(chat_id, "⚔️ در حال ساخت")
    
    elif callback_data == "rules":
        keyboard = {
            "inline_keyboard": [
                [{"text": "قوانین بازی", "url": "https://t.me/W0rldWarGameGhavanin"}],
                [{"text": "بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        send_message(chat_id, "📚 قوانین", keyboard)
    
    elif callback_data == "select_country":
        send_message(chat_id, "🏴 فصل در حال اجراست")
    
    elif callback_data == "back_to_main":
        send_message(chat_id, "منوی اصلی:", create_main_menu())
    
    elif callback_data.startswith("buy_"):
        send_message(chat_id, "✅ خرید ثبت شد!")

def handle_message(update):
    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")
    
    if text == "/start":
        send_message(chat_id, "به ربات World War Game خوش آمدید!", create_main_menu())

print("🤖 ربات شروع به کار کرد...")

while True:
    try:
        updates = get_updates()
        
        for update in updates:
            last_update_id = update["update_id"]
            
            if "message" in update:
                handle_message(update)
            elif "callback_query" in update:
                handle_callback(update)
        
        time.sleep(1)
        
    except Exception as e:
        print(f"خطا: {e}")
        time.sleep(5)
