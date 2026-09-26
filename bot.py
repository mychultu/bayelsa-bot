import os, telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
CHANNEL_ID = os.environ.get("CHANNEL_ID")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "👋 Welcome to Bayelsa Secret!\n\nSend your confession anonymously, I will post it for you.\n\nJust type it now:")

@bot.message_handler(func=lambda m: True)
def confess(m):
    if m.chat.id == ADMIN_ID: return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Approve", callback_data=f"a_{m.chat.id}_{m.message_id}"))
    markup.add(InlineKeyboardButton("❌ Reject", callback_data="r"))
    bot.send_message(ADMIN_ID, f"NEW SECRET:\n\n{m.text}", reply_markup=markup)
    bot.reply_to(m, "✅ Received! Anonymous and safe. Waiting for admin to post.")

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    if c.data.startswith("a_"):
        _, cid, mid = c.data.split("_")
        bot.copy_message(CHANNEL_ID, cid, int(mid))
        bot.send_message(int(cid), "Your secret has been posted anonymously! 🔥")
        bot.edit_message_text("✅ Posted!", c.message.chat.id, c.message.message_id)
    else:
        bot.edit_message_text("❌ Rejected", c.message.chat.id, c.message.message_id)

bot.infinity_polling()
