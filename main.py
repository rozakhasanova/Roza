import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get(“BOT_TOKEN”)

# ====== ПРОМТЫ ======

# Чтобы добавить новый: скопируй блок и вставь ниже

# video_file_id: получишь после загрузки видео в бота (инструкция ниже)

PROMTS = {
“camera”: {
“title”: “🎬 Управление камерой в ИИ”,
“text”: “””<b>КАК УПРАВЛЯТЬ КАМЕРОЙ В ИИ</b>

Твое видео может быть красивым, но только движение камеры делает его «дорогим» и кинематографичным.

🟢 <b>БАЗОВЫЙ УРОВЕНЬ (Кнопки в приложении)</b>

<b>Left / Right Circling (Облет)</b> — камера движется по дуге вокруг объекта.
<i>Зачем:</i> Создает объем и эпичность. Идеально для показа одежды, моделей или архитектуры.

<b>Upward / Downward Tilt (Наклон)</b> — камера закреплена, но меняет угол обзора.
<i>Зачем:</i> Показать масштаб здания (вверх) или детали под ногами (вниз).

<b>Left / Right Walking (Следование)</b> — камера имитирует шаг оператора.
<i>Зачем:</i> Эффект присутствия. Идеально для прогулок и лайфстайл-контента.

🔵 <b>ПРОДВИНУТЫЙ УРОВЕНЬ (Команды в промпте)</b>

<b>Zoom In / Out</b> — плавное приближение/отдаление.
<b>Pan Left / Right</b> — плавный поворот камеры.
<b>POV</b> — съемка «из глаз». Максимальное вовлечение зрителя.
<b>Handheld Camera</b> — эффект «живой» камеры с тряской. Убирает «пластиковость» ИИ.
<b>Drone Shot</b> — вид с высоты. Для масштабных сцен и городских панорам.”””,
“video_file_id”: None,  # сюда вставишь file_id после загрузки видео
},

```
# Сюда добавляй следующие промты по образцу выше:
# "ключ": {
#     "title": "Название",
#     "text": "Текст промта",
#     "video_file_id": None,
# },
```

}

# ====== ОБРАБОТЧИКИ ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
keyboard = [
[InlineKeyboardButton(data[“title”], callback_data=key)]
for key, data in PROMTS.items()
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text(
“Привет! 👋\nВыбери тему — получишь промт и пример видео:”,
reply_markup=reply_markup
)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

```
key = query.data
promt = PROMTS.get(key)

if not promt:
    await query.message.reply_text("Промт не найден.")
    return

# Отправляем видео если есть
if promt["video_file_id"]:
    await query.message.reply_video(
        video=promt["video_file_id"],
        caption=promt["text"],
        parse_mode="HTML"
    )
else:
    await query.message.reply_text(promt["text"], parse_mode="HTML")

# Кнопка "назад"
keyboard = [[InlineKeyboardButton("⬅️ Назад к списку", callback_data="__back__")]]
await query.message.reply_text("⬆️ Промт выше", reply_markup=InlineKeyboardMarkup(keyboard))
```

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
keyboard = [
[InlineKeyboardButton(data[“title”], callback_data=key)]
for key, data in PROMTS.items()
]
await query.message.reply_text(“Выбери тему:”, reply_markup=InlineKeyboardMarkup(keyboard))

# Получить file_id загруженного видео

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.video:
file_id = update.message.video.file_id
await update.message.reply_text(f”file_id твоего видео:\n<code>{file_id}</code>”, parse_mode=“HTML”)

def main():
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(CallbackQueryHandler(back, pattern=”**back**”))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.VIDEO, get_file_id))
app.run_polling()

if **name** == “**main**”:
from telegram.ext import MessageHandler, filters
main()
