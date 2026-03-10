import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get(“BOT_TOKEN”)

PROMTS = {
“camera”: {
“title”: “Управление камерой в ИИ”,
“text”: (
“<b>КАК УПРАВЛЯТЬ КАМЕРОЙ В ИИ</b>\n\n”
“Твое видео может быть красивым, но только движение камеры делает его кинематографичным.\n\n”
“<b>БАЗОВЫЙ УРОВЕНЬ</b>\n\n”
“<b>Left / Right Circling</b> - камера движется по дуге вокруг объекта.\n”
“Зачем: Создает объем и эпичность. Идеально для одежды, моделей, архитектуры.\n\n”
“<b>Upward / Downward Tilt</b> - камера меняет угол обзора вверх или вниз.\n”
“Зачем: Показать масштаб здания или детали под ногами.\n\n”
“<b>Left / Right Walking</b> - камера имитирует шаг оператора.\n”
“Зачем: Эффект присутствия. Идеально для прогулок и лайфстайл-контента.\n\n”
“<b>ПРОДВИНУТЫЙ УРОВЕНЬ</b>\n\n”
“<b>Zoom In / Out</b> - плавное приближение или отдаление.\n”
“<b>Pan Left / Right</b> - плавный поворот камеры.\n”
“<b>POV</b> - съемка из глаз. Максимальное вовлечение зрителя.\n”
“<b>Handheld Camera</b> - эффект живой камеры с тряской. Убирает пластиковость ИИ.\n”
“<b>Drone Shot</b> - вид с высоты. Для масштабных сцен и городских панорам.”
),
“video_file_id”: None,
},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
keyboard = [
[InlineKeyboardButton(data[“title”], callback_data=key)]
for key, data in PROMTS.items()
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text(
“Привет! Выбери тему - получишь промт и пример видео:”,
reply_markup=reply_markup
)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

```
if query.data == "__back__":
    keyboard = [
        [InlineKeyboardButton(data["title"], callback_data=key)]
        for key, data in PROMTS.items()
    ]
    await query.message.reply_text("Выбери тему:", reply_markup=InlineKeyboardMarkup(keyboard))
    return

promt = PROMTS.get(query.data)
if not promt:
    await query.message.reply_text("Промт не найден.")
    return

if promt["video_file_id"]:
    await query.message.reply_video(
        video=promt["video_file_id"],
        caption=promt["text"],
        parse_mode="HTML"
    )
else:
    await query.message.reply_text(promt["text"], parse_mode="HTML")

keyboard = [[InlineKeyboardButton("Назад к списку", callback_data="__back__")]]
await query.message.reply_text(".", reply_markup=InlineKeyboardMarkup(keyboard))
```

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.video:
file_id = update.message.video.file_id
await update.message.reply_text(
“file_id твоего видео:\n<code>” + file_id + “</code>”,
parse_mode=“HTML”
)

def main():
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.VIDEO, get_file_id))
app.run_polling()

if **name** == “**main**”:
main()
