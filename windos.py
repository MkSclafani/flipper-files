import os
import sys
import shutil
import subprocess

# Controlla se le librerie richieste sono installate
REQUIRED_MODULES = ["telegram", "telegram.ext"]

def install_missing_modules():
    for module in REQUIRED_MODULES:
        try:
            _import_(module)
        except ImportError:
            print(f"[⚠] Modulo '{module}' non trovato. Installazione in corso...")
            subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot", "--upgrade"])
    print("[✔] Tutti i moduli sono installati!")

# Esegui il controllo delle librerie
install_missing_modules()

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Inserisci il tuo TOKEN API
TOKEN = "7895216596:AAHkQdNkg5XrCElVjXvfnVfkKKk8DFB_yYE"

# ID Telegram autorizzati (deve essere il tuo ID)
ADMIN_ID = [1108744122]

# Percorsi dei file
BAT_FILE = "C:\\ProgramData\\windos\\windos.bat"
STARTUP_FOLDER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

# Copia windos.bat nella cartella di avvio se non è già presente
def setup_autostart():
    destination = os.path.join(STARTUP_FOLDER, "windos.bat")
    if not os.path.exists(destination):
        shutil.copy(BAT_FILE, destination)
        print("[✔] File bat copiato nella cartella di avvio.")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔹 Il bot è attivo! Usa /spegni, /riavvia o /annulla.")

async def spegni(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        await update.message.reply_text("🛑 Spegnimento in corso...")
        os.system("shutdown /s /t 5")
    else:
        await update.message.reply_text("❌ Accesso negato!")

async def riavvia(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        await update.message.reply_text("🔄 Riavvio in corso...")
        os.system("shutdown /r /t 5")
    else:
        await update.message.reply_text("❌ Accesso negato!")

async def annulla(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        await update.message.reply_text("⛔ Spegnimento annullato!")
        os.system("shutdown /a")
    else:
        await update.message.reply_text("❌ Accesso negato!")

def main():
    # Configura l'avvio automatico del bot
    setup_autostart()

    # Avvia il bot Telegram
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spegni", spegni))
    app.add_handler(CommandHandler("riavvia", riavvia))
    app.add_handler(CommandHandler("annulla", annulla))

    app.run_polling()

if _name_ == "_main_":
    main()