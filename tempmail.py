# Author (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev

import re
import requests
import random
import string
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize the bot and dispatcher
API_TOKEN = '123456:ABCDEFGHIJLLJOdMttZ5hEZ78'  # Change the token with your bot token
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Dictionary to store user request data
user_data = {}

#For Mail Read Funtion
user_tokens = {}
MAX_MESSAGE_LENGTH = 4000

BASE_URL = "https://api.mail.tm"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def generate_random_username(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def get_domain():
    response = requests.get(f"{BASE_URL}/domains", headers=HEADERS)
    data = response.json()
    if isinstance(data, list) and data:
        return data[0]['domain']
    elif 'hydra:member' in data and data['hydra:member']:
        return data['hydra:member'][0]['domain']
    return None

def create_account(email, password):
    data = {
        "address": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/accounts", headers=HEADERS, json=data)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_token(email, password):
    data = {
        "address": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/token", headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Token Error Code: {response.status_code}")
        print(f"Token Response: {response.text}")
        return None


def get_text_from_html(html_content_list):
    html_content = ''.join(html_content_list)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract URLs from anchor tags and append them to the anchor text
    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']
        new_content = f"{a_tag.text} [{url}]"
        a_tag.string = new_content

    text_content = soup.get_text()
    cleaned_content = re.sub(r'\s+', ' ', text_content).strip()
    return cleaned_content


def list_messages(token):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/messages", headers=headers)
    data = response.json()
    if isinstance(data, list):
        return data
    elif 'hydra:member' in data:
        return data['hydra:member']
    else:
        return []


@dp.message_handler(commands=['tmail'])    #You Can chnage the tmail command
async def generate_mail(message: types.Message):
    # Check if the chat type is not private
    if message.chat.type != 'private':
        await bot.send_message(message.chat.id, "<b>❌ Bro TempMail Feature Only Work In Privately, Because This is Private things.</b>", parse_mode="html")
        return
        
    if not message.text.startswith(('/tmail', '.tmail')):
        return

    # Send a loading message
    loading_msg = await message.answer("<b>Generating your temporary email...</b>", parse_mode='html')

    # Retrieve arguments based on the command format
    args_text = ""
    if message.text.startswith('/tmail'):
        args_text = message.get_args()
    elif message.text.startswith('.tmail'):
        args_text = message.text.replace('.tmail', '').strip()

    args = args_text.split()
    if len(args) == 1 and ':' in args[0]:
        username, password = args[0].split(':')
    elif len(args) == 2:
        username, password = args
    else:
        # Default to generating random username and password
        username = generate_random_username()
        password = generate_random_password()

    domain = get_domain()
    if not domain:
        await message.answer("<b>Failed to retrieve domain try Again</b>", parse_mode='html')
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)
        return

    email = f"{username}@{domain}"
    account = create_account(email, password)
    if not account:
        await message.answer("<b>Username is already taken. Please choose another one.</b>", parse_mode='html')
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)
        return

    if "address" in account and "has already been taken" in account["address"]:
        await message.answer("<b>Username is already taken. Please choose another one.</b>", parse_mode='html')
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)
        return

    # Introduce a delay before retrieving the token
    time.sleep(2)

    token = get_token(email, password)
    if not token:
        await message.answer("<b>Failed to retrieve token.</b>", parse_mode='html')
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)
        return

    # Updated output format
    output_message = (
        "<b>📧 Smart-Email Details 📧</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📧 Email: <code>{email}</code>\n"
        f"🔑 Password: <code>{password}</code>\n"
        f"🔒 Token: <code>{token}</code>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "<b>Note: The token is sensitive and provides access to your temporary email.</b>"
    )
    await message.answer(output_message, parse_mode='html')

    # Delete the loading message
    await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)
    
    
    
@dp.message_handler(commands=['cmail']) #You Can chnage the cmail command
async def check_mail(message: types.Message):
    # Check if the chat type is not private
    if message.chat.type != 'private':
        await bot.send_message(message.chat.id, "<b>❌ Bro TempMail Feature Only Work In Privately</b>", parse_mode="html")
        return

    # Send a loading message
    loading_msg = await bot.send_message(message.chat.id, "<code>⏳ Checking Mails.. Please wait.</code>", parse_mode='html')

    token = message.get_args()
    if not token:
        await message.answer("<b>Please provide a token after the /cmail command.</b>", parse_mode='html')
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)  # Delete the loading message
        return

    user_tokens[message.from_user.id] = token
    messages = list_messages(token)
    if not messages:
        await message.answer("<b>❌ No messages found maybe wrong token</b>", parse_mode='html')
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)  # Delete the loading message
        return

    output = "📧 <b>Your Smart-Mail Messages</b> 📧\n"
    output += "━━━━━━━━━━━━━━━━━━\n"
    
    keyboard = InlineKeyboardMarkup(row_width=5)
    buttons = []
    for idx, msg in enumerate(messages[:10], 1):
        output += f"<b>{idx}. From: <code>{msg['from']['address']}</code> - Subject: {msg['subject']}</b>\n"
        button = InlineKeyboardButton(f"{idx}", callback_data=f"read_{msg['id']}")
        buttons.append(button)
    
    for i in range(0, len(buttons), 5):
        keyboard.row(*buttons[i:i+5])

    await message.answer(output, reply_markup=keyboard, parse_mode='html')
    await bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)  # Delete the loading message
    
   

@dp.callback_query_handler(lambda c: c.data.startswith('read_'))
async def read_message(callback_query: types.CallbackQuery):   
    _, message_id = callback_query.data.split('_')
    
    token = user_tokens.get(callback_query.from_user.id)
    if not token:
        await bot.send_message(callback_query.message.chat.id, "Token not found. Please use /cmail with your token again.")
        return

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/messages/{message_id}", headers=headers)
    
    if response.status_code == 200:
        details = response.json()
        if 'html' in details:
            message_text = get_text_from_html(details['html'])
        elif 'text' in details:
            message_text = details['text']
        else:
            message_text = "Content not available."
        
        # Check if the message length exceeds the maximum allowed by Telegram
        if len(message_text) > MAX_MESSAGE_LENGTH:
            message_text = message_text[:MAX_MESSAGE_LENGTH - 100] + "... [message truncated]"

        output = f"From: {details['from']['address']}\nSubject: {details['subject']}\n━━━━━━━━━━━━━━━━━━\n{message_text}"
        await bot.send_message(callback_query.message.chat.id, output, disable_web_page_preview=True)
    else:
        await bot.send_message(callback_query.message.chat.id, "Error retrieving message details.")
        
        
# Run the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
