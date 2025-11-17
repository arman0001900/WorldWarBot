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
        print(f"Error sending message: {e}")
        return None

def edit_message(chat_id, message_id, text, reply_markup=None):
    url = f"{BASE_URL}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error editing message: {e}")
        return None

def create_main_menu():
    keyboard = [
        [{"text": "📅 لیست ایونت ها", "callback_data": "events"}],
        [{"text": "🏛️ مدیریت کشور", "callback_data": "manage_country"}],
        [{"text": "🛒 خرید عادی", "callback_data": "normal_shop"}],
        [{"text": "💎 خرید وی آی پی", "callback_data": "vip_shop"}],
        [{"text": "🛟 پشتیبانی", "callback_data": "support"}],
        [{"text": "⚔️ حمله نظامی", "callback_data": "military_attack"}],
        [{"text": "📚 قوانین بازی", "callback_data": "rules"}],
        [{"text": "🏴 انتخاب کشور", "callback_data": "select_country"}]
    ]
    return {"inline_keyboard": keyboard}

def create_back_button():
    return {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]]}

def create_shop_menu():
    keyboard = [
        [{"text": "✈️ جنگنده", "callback_data": "shop_fighters"}],
        [{"text": "🎯 تانک", "callback_data": "shop_tanks"}],
        [{"text": "👮 سرباز", "callback_data": "shop_soldiers"}],
        [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
    ]
    return {"inline_keyboard": keyboard}

def create_fighters_menu():
    keyboard = [
        [{"text": "🛒 خرید F-4", "callback_data": "buy_f4"}],
        [{"text": "🛒 خرید F-14", "callback_data": "buy_f14"}],
        [{"text": "🛒 خرید Su-35", "callback_data": "buy_su35"}],
        [{"text": "🔙 بازگشت", "callback_data": "normal_shop"}]
    ]
    return {"inline_keyboard": keyboard}

def handle_callback(update):
    query = update["callback_query"]
    callback_data = query["data"]
    chat_id = query["message"]["chat"]["id"]
    message_id = query["message"]["message_id"]
    
    if callback_data == "events":
        text = "📅 <b>لیست ایونت ها</b>\n\n❌ در حال حاضر هیچ ایونتی فعال نیست."
        edit_message(chat_id, message_id, text, create_back_button())
    
    elif callback_data == "manage_country":
        text = """🏛️ <b>مدیریت کشور</b>

📊 <b>لیست دارایی</b>

🇮🇷 <b>نام کشور:</b> ایران

💰 <b>بودجه کل:</b> 1.5M
💵 <b>سود اقتصادی:</b> 150K
😊 <b>رضایت مردمی:</b> 50%
🛡️ <b>امنیت:</b> 50%
🌐 <b>اعتبار جهانی:</b> 50%
👥 <b>جمعیت:</b> 85M

🔫 <b>پایگاه نظامی</b>
🎖️ <b>وفاداری ارتش:</b> 50%
📡 <b>سامانه اطلاعاتی:</b> 50%
🛂 <b>امنیت مرزی:</b> 50%"""
        keyboard = {
            "inline_keyboard": [
                [{"text": "🏭 سود کارخانه ها", "callback_data": "factory_profit"}],
                [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        edit_message(chat_id, message_id, text, keyboard)
    
    elif callback_data == "factory_profit":
        text = "🏭 <b>سود کارخانه ها</b>\n\n❌ متاسفانه شما کارخانه ای ندارید"
        edit_message(chat_id, message_id, text, create_back_button())
    
    elif callback_data == "normal_shop":
        text = "🛒 <b>فروشگاه عادی</b>\n\nلطفا دسته مورد نظر را انتخاب کنید:"
        edit_message(chat_id, message_id, text, create_shop_menu())
    
    elif callback_data == "shop_fighters":
        text = """🎮 <b>World War Game</b>

✈️ <b>12 جنگنده F-4 (بمب افکن)</b>
💰 قیمت: 450K

✈️ <b>12 جنگنده F-14 (رهگیر)</b>
💰 قیمت: 550K

✈️ <b>12 جنگنده Su-35</b>
💰 قیمت: 650K

✈️ <b>12 جنگنده Su-34 (بمب افکن)</b>
💰 قیمت: 750K"""
        edit_message(chat_id, message_id, text, create_fighters_menu())
    
    elif callback_data == "shop_tanks":
        text = """🎮 <b>World War Game</b>

🎯 <b>50 تانک T64</b>
💰 قیمت: 350K

🎯 <b>50 تانک T72</b>
💰 قیمت: 450K

🎯 <b>50 تانک T90</b>
💰 قیمت: 600K

🎯 <b>25 تانک آبرامز</b>
💰 قیمت: 850K"""
        keyboard = {
            "inline_keyboard": [
                [{"text": "🛒 خرید T64", "callback_data": "buy_t64"}],
                [{"text": "🛒 خرید T72", "callback_data": "buy_t72"}],
                [{"text": "🛒 خرید T90", "callback_data": "buy_t90"}],
                [{"text": "🛒 خرید آبرامز", "callback_data": "buy_abrams"}],
                [{"text": "🔙 بازگشت", "callback_data": "normal_shop"}]
            ]
        }
        edit_message(chat_id, message_id, text, keyboard)
    
    elif callback_data == "support":
        text = "🛟 <b>پشتیبانی</b>\n\nبرای ارتباط با پشتیبانی روی دکمه زیر کلیک کنید:"
        keyboard = {
            "inline_keyboard": [
                [{"text": "📞 پیوی پشتیبانی", "url": "https://t.me/WorldWar_Support"}],
                [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        edit_message(chat_id, message_id, text, keyboard)
    
    elif callback_data == "vip_shop":
        text = "💎 <b>فروشگاه VIP</b>\n\nبرای دسترسی به فروشگاه VIP از دکمه‌های زیر استفاده کنید:"
        keyboard = {
            "inline_keyboard": [
                [{"text": "🛍️ آیدی شاپ وی آی پی", "url": "https://t.me/W0rldWarGameVIP"}],
                [{"text": "👤 پیوی مالک برای خرید", "url": "https://t.me/MrArmanQ"}],
                [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        edit_message(chat_id, message_id, text, keyboard)
    
    elif callback_data == "military_attack":
        text = "⚔️ <b>حمله نظامی</b>\n\n❌ این قابلیت فعلا در حال ساخت است"
        edit_message(chat_id, message_id, text, create_back_button())
    
    elif callback_data == "rules":
        text = "📚 <b>قوانین بازی</b>\n\nبرای مشاهده قوانین و آموزشات روی دکمه زیر کلیک کنید:"
        keyboard = {
            "inline_keyboard": [
                [{"text": "📖 مشاهده قوانین", "url": "https://t.me/W0rldWarGameGhavanin"}],
                [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
            ]
        }
        edit_message(chat_id, message_id, text, keyboard)
    
    elif callback_data == "select_country":
        text = "🏴 <b>انتخاب کشور</b>\n\n❌ فصل در حال اجراست و نمیتوانید کشور پر کنید"
        edit_message(chat_id, message_id, text, create_back_button())
    
    elif callback_data == "back_to_main":
        text = "🎮 <b>World War Game</b>\n\nبه ربات خوش آمدید! لطفا یک گزینه را انتخاب کنید:"
        edit_message(chat_id, message_id, text, create_main_menu())
    
    elif callback_data.startswith("buy_"):
        text = "✅ <b>خرید با موفقیت ثبت شد!</b>\n\nخرید شما در صف پردازش قرار گرفت."
        edit_message(chat_id, message_id, text, create_back_button())
    
    # پاسخ به کلیک کاربر
    requests.post(f"{BASE_URL}/answerCallbackQuery", json={
        "callback_query_id": query["id"]
    })

def handle_message(update):
    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")
    
    if text == "/start":
        welcome_text = """🎮 <b>World War Game</b>

به ربات مدیریت کشور خوش آمدید!

🔸 <b>امکانات ربات:</b>
• مدیریت کامل کشور
• سیستم خرید تجهیزات
• حمله نظامی
• سیستم ایونت

لطفا یک گزینه را انتخاب کنید:"""
        send_message(chat_id, welcome_text, create_main_menu())

print("🤖 ربات شروع به کار کرد...")
print("✅ منتظر پیام ها...")

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
