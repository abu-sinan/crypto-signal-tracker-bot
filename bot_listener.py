import nest_asyncio
nest_asyncio.apply()
import asyncio
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from binance.client import Client  # Import Binance client

# ==== CONFIG ====
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
ALERT_CHANNEL_ID = -1002518××××××  # Replace with your channel ID

BINANCE_API_KEY = 'YOUR_BINANCE_API_KEY'
BINANCE_API_SECRET = 'YOUR_BINANCE_API_SECRET'

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope) #Replace with your credentials.json
client_gsheets = gspread.authorize(creds)
spreadsheet = client_gsheets.open('Crypto Signals')
worksheet = spreadsheet.sheet1

HEADERS = ['Pair', 'Entry', 'SL', 'TP', 'Status', 'MFE', 'MAE']

def initialize_sheet_headers():
    existing_headers = worksheet.row_values(1)
    if existing_headers != HEADERS:
        worksheet.update(values=[HEADERS], range_name='A1:G1')

# Set headers
initialize_sheet_headers()

# Initialize signals list
open_signals = []

# Initialize Binance client with API keys
binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# ==== FUNCTIONS ====

def parse_signal(text):
    pair = re.search(r'PAIR:\s*(\w+)', text)
    entry = re.search(r'Entry:\s*([\d\.]+)', text)
    sl = re.search(r'SL:\s*([\d\.]+)', text)
    tp = re.search(r'TP:\s*([\d\.]+)', text)

    if all([pair, entry, sl, tp]):
        return {
            'pair': pair.group(1).upper(),
            'entry': float(entry.group(1)),
            'sl': float(sl.group(1)),
            'tp': float(tp.group(1)),
            'status': 'OPEN',
            'mfe': 0.0,
            'mae': 0.0
        }
    return None

def update_or_append_signal(signal):
    all_rows = worksheet.get_all_values()

    # Search for existing signal row
    for idx, row in enumerate(all_rows, start=1):
        if (row[0] == signal['pair'] and
            row[1] == str(signal['entry']) and
            row[2] == str(signal['sl']) and
            row[3] == str(signal['tp'])):

            # Update existing row
            worksheet.update(f'E{idx}', signal['status'])
            worksheet.update(f'F{idx}', str(signal['mfe']))
            worksheet.update(f'G{idx}', str(signal['mae']))
            return  # Exit after updating

    # If no existing row, append as new
    worksheet.append_row([
        signal['pair'],
        signal['entry'],
        signal['sl'],
        signal['tp'],
        signal['status'],
        signal['mfe'],
        signal['mae']
    ])

async def send_alert(bot, message):
    await bot.send_message(
        chat_id=ALERT_CHANNEL_ID,
        text=message,
        parse_mode='Markdown'
    )

async def handle_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.text:
        text = update.channel_post.text
        print("\n--- New Message From Channel ---\n", text)

        signal = parse_signal(text)
        if signal:
            open_signals.append(signal)
            update_or_append_signal(signal)
            print("\n--- New Signal Stored and Logged ---\n", signal)
        else:
            print("\n--- Message Ignored (Not a Signal) ---")

async def price_tracker(application):
    while True:
        if not open_signals:
            await asyncio.sleep(10)
            continue

        for signal in open_signals:
            if signal['status'] != 'OPEN':
                continue

            try:
                ticker = binance_client.get_symbol_ticker(symbol=signal["pair"])
                current_price = float(ticker['price'])
            except Exception as e:
                print(f"Error fetching price for {signal['pair']}: {e}")
                continue

            print(f"{signal['pair']} Current Price: {current_price}")

            # Track MFE/MAE
            diff = current_price - signal['entry']
            if diff > signal['mfe']:
                signal['mfe'] = diff
            if diff < signal['mae']:
                signal['mae'] = diff

            # TP Hit
            if current_price >= signal['tp']:
                signal['status'] = 'TP HIT'
                await send_alert(application.bot, f"🎉 *{signal['pair']}* TP HIT at `{current_price}`")
                update_or_append_signal(signal)

            # SL Hit
            elif current_price <= signal['sl']:
                signal['status'] = 'SL HIT'
                await send_alert(application.bot, f"⚠️ *{signal['pair']}* SL HIT at `{current_price}`")
                update_or_append_signal(signal)

        await asyncio.sleep(10)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_signal))

    print("Bot is running... Listening for signals...")

    asyncio.create_task(price_tracker(app))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
