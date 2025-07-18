![Crypto Signal Tracker Bot](https://github.com/abu-sinan/crypto-signal-tracker-bot/blob/main/assets/thumbnail.png)
# 📈 Crypto Signal Tracker Bot

A Telegram bot that listens to crypto trading signals from a private channel or group, fetches real-time prices from Binance, tracks signals (TP/SL), logs everything into Google Sheets, and sends alert notifications when targets are hit.

---

## 🚀 Features

- ✅ Telegram Channel/Group Signal Listener
- ✅ Binance Price Tracking (Real-time)
- ✅ Logs Signals into Google Sheets
- ✅ Tracks:
  - TP/SL Status
  - Maximum Favorable Excursion (MFE)
  - Maximum Adverse Excursion (MAE)
- ✅ Sends TP/SL Alerts via Telegram
- ✅ Handles All Binance Pairs

---

## 📷 Example Signal Format

PAIR: BTCUSDT Entry: 99500 SL: 99000 TP: 100500

---

## ⚙️ Requirements

- Python 3.8+
- Binance API (Read-only)
- Google Sheets API Credentials

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📄 Setup Guide

### 1. Clone the Repository:

```bash
git clone https://github.com/abu-sinan/crypto-signal-tracker-bot.git
cd crypto-signal-tracker-bot
```

### 2. Google Sheets Setup:

  - Enable Google Sheets API.

  - Create service account credentials.

  - Download `credentials.json`.

  - Place it in the project folder.

  - Sheet access with service account email.

### 3. Bot Configuration:

  - Add your Telegram bot token.

  - Add your Binance API key (read-only).

  - Add your Binance API secret.

### 4. Run the Bot:

```bash
python bot_listener.py
```

---

## 📊 Google Sheet Columns

| Pair    | Entry  | SL    | TP    | Status | MFE  | MAE  |
|---------|--------|-------|-------|--------|------|------|
| BTCUSDT | 34500  | 34000 | 35500 | OPEN   | 85776  | 0.0  |
| ETHUSDT | 2400   | 2300  | 2600  | CLOSED | 200  | 20   |

---

## 📬 Telegram Alerts

Example:
> 🎉 BTCUSDT TP HIT at 119574.61

---

## 🛡️ Security Note

Do NOT share your real `credentials.json` publicly.

Use `.gitignore` to protect sensitive files.

---

## 📄 License

This project is open-source under the [MIT License](https://github.com/abu-sinan/crypto-signal-tracker-bot/blob/main/LICENSE).

---

## 🤝 Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first.

---

## 📞 Contact

For support or inquiries, reach out via [LinkedIn](https://www.linkedin.com/in/abusinan) or open a GitHub issue.