import os
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")
FILE = "commands.json"

def load_commands():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_commands(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot assist aktif!")

async def set_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Format:\n/set nama_command isi pesan"
        )
        return

    name = context.args[0]
    text = " ".join(context.args[1:])

    data = load_commands()
    data[name] = text
    save_commands(data)

    await update.message.reply_text(f"✅ Command /{name} disimpan")

async def get_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.replace("/", "")
    data = load_commands()

    if cmd in data:
        await update.message.reply_text(data[cmd])

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_commands()
    welcome_text = data.get(
        "welcome",
        "Halo {name}! Selamat datang 👋"
    )

    for user in update.message.new_chat_members:
        await update.message.reply_text(
            welcome_text.replace("{name}", user.first_name)
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("set", set_command))
app.add_handler(MessageHandler(filters.COMMAND, get_command))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

app.run_polling()
