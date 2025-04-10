دقیقاً! می‌تونیم این اعتبارسنجی آدرس کیف پول رو بعداً اضافه کنیم. فعلاً با همین کد اولیه پیش بریم، بعداً هر زمان که لازم بود این ویژگی رو اضافه خواهیم کرد.

حالا بریم سراغ کد نهایی و مراحل اجرا:


---

کد نهایی (با توجه به اطلاعات شما):

import csv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = '7639076590:AAHP_e7PJlNmHt1ydRew1Mtcg6iAj6zin4I'
CHANNEL = '@tt_memecoin'
INSTAGRAM = 'https://www.instagram.com/tttoken1970'
X_LINK = 'https://x.com/tractormemecoin'

users_file = 'users.csv'
user_data = {}

# ذخیره‌سازی اطلاعات کاربران به فایل CSV
def save_to_csv(user_id, username, wallet, inviter_id, reward):
    file_exists = os.path.isfile(users_file)
    with open(users_file, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['user_id', 'username', 'wallet', 'inviter_id', 'reward']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'user_id': user_id,
            'username': username or '',
            'wallet': wallet,
            'inviter_id': inviter_id or '',
            'reward': reward
        })

# فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    inviter_id = None
    if context.args:
        try:
            inviter_id = int(context.args[0])
        except:
            inviter_id = None

    user_data[user.id] = {
        'inviter': inviter_id,
        'wallet': '',
        'reward': 30000  # 3 تسک اولیه برای کاربر
    }

    keyboard = [
        [InlineKeyboardButton("عضویت در تلگرام", url=f"https://t.me/{CHANNEL[1:]}")],
        [InlineKeyboardButton("فالو اینستاگرام", url=INSTAGRAM)],
        [InlineKeyboardButton("فالو ایکس (توییتر)", url=X_LINK)],
        [InlineKeyboardButton("ادامه ➡️", callback_data='next')]
    ]

    await update.message.reply_text(
        "سلام به ایردراپ رایگان میم‌کوین تراکتور خوش اومدی!\n\n"
        "برای هر تسک ۱۰,۰۰۰ توکن و برای هر دعوت موفق ۲,۰۰۰ توکن دریافت می‌کنی.\n"
        "ابتدا روی لینک‌ها کلیک کن و عضو شو، بعد دکمه ادامه رو بزن.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# مرحله بعدی (دکمه ادامه)
async def next_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("حالا لطفاً آدرس کیف پولت رو بفرست (مثلاً 0x...)")

# دریافت و ذخیره آدرس کیف پول کاربر
async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    wallet = update.message.text

    # بررسی اعتبار آ

