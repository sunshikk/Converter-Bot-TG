import logging
import asyncio
import os
import traceback
import tempfile

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from moviepy import VideoFileClip

class Form(StatesGroup):
    waiting_mp4_file = State()
    waiting_mp4wav_file = State()
    waiting_mp4flac_file = State()
    waiting_mp4opus_file = State()
    waiting_mp4ogg_file = State()
    waiting_mp4mpeg_file = State()
    waiting_mp4avi_file = State()
    waiting_mp4mov_file = State()
    waiting_avi_file = State()
    waiting_mpeg_file = State()
    waiting_mov_file = State()

choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎬 MP4 в MP3", callback_data="mp4to3"),
        InlineKeyboardButton(text="🎬 MP4 в WAV", callback_data="mp4towav"),
        InlineKeyboardButton(text="🎬 MP4 в FLAC", callback_data="mp4toflac"),
    ],
    [
        InlineKeyboardButton(text="🎬 MP4 в OPUS", callback_data="mp4toopus"),
        InlineKeyboardButton(text="🎬 MP4 в OGG", callback_data="mp4toogg")
    ],
    [InlineKeyboardButton(text="◀️ Назад", callback_data="cancel")]
])

choicevid = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎬 MP4 в MPEG", callback_data="mp4tompeg"),
        InlineKeyboardButton(text="🎬 MP4 в AVI", callback_data="mp4toavi"),
        InlineKeyboardButton(text="🎬 MP4 в MOV", callback_data="mp4tomov")
    ],
    [
        InlineKeyboardButton(text="🎬 AVI в MP4", callback_data="avitomp4"),
        InlineKeyboardButton(text="🎬 MPEG в MP4", callback_data="mpegtomp4"),
        InlineKeyboardButton(text="🎬 MOV в MP4", callback_data="movtomp4")
    ],
    [InlineKeyboardButton(text="◀️ Назад", callback_data="cancel")]
])

choicestart = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1️⃣ Конвертирование видео в аудио", callback_data="vitoaudio")],
    [InlineKeyboardButton(text="2️⃣ Конвертирование видео в видео", callback_data="vitovideo")],
])

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="◀️ Назад", callback_data="cancel")]
])

MAX_FILE_SIZE = 20 * 1024 * 1024

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7844735010:AAHZuVDSxU88dnxCpjs73KkTVCGuboSoeyE')
dp = Dispatcher()
router = Router()

@router.message(StateFilter(None), CommandStart())
async def send_welcome(message: Message):
    await message.answer("📄 Данный бот может конвертировать файлы с одного типа в другое\n\nВыберите наиболее подходящий вариант для Вас.", reply_markup=choicestart)

@router.callback_query() 
async def process_callback(callback_query: CallbackQuery, state: FSMContext): 
    data = callback_query.data

    if data == "vitoaudio":
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий раздел конвертации файлов: <b>Видео в аудио</b>\nВыберите, что вы хотите конвертировать",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=choice
        )

    if data == "vitovideo":
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий раздел конвертации файлов: <b>Видео в видео</b>\nВыберите, что вы хотите конвертировать",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=choicevid
        )

    if data == "mp4to3":
        await state.set_state(Form.waiting_mp4_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в MP3</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4towav":
        await state.set_state(Form.waiting_mp4wav_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в WAV</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4toflac":
        await state.set_state(Form.waiting_mp4flac_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в FLAC</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4toopus":
        await state.set_state(Form.waiting_mp4opus_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в OPUS</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4toogg":
        await state.set_state(Form.waiting_mp4ogg_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в OGG</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4tompeg":
        await state.set_state(Form.waiting_mp4mpeg_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в MPEG</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4toavi":
        await state.set_state(Form.waiting_mp4avi_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в AVI</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mp4tomov":
        await state.set_state(Form.waiting_mp4mov_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MP4 в MOV</b>\nОтправьте файл с расширением .mp4 боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "avitomp4":
        await state.set_state(Form.waiting_avi_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>AVI в MP4</b>\nОтправьте файл с расширением .avi боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "mpegtomp4":
        await state.set_state(Form.waiting_mpeg_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MPEG в MP4</b>\nОтправьте файл с расширением .mpeg боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "movtomp4":
        await state.set_state(Form.waiting_mov_file)
        await callback_query.bot.edit_message_text(
            text="✅ Вы выбрали следующий тип конвертации файлов: <b>MOV в MP4</b>\nОтправьте файл с расширением .mov боту для конвертации.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=cancel
        )

    if data == "cancel":
        await state.clear()
        await callback_query.bot.edit_message_text(
            text="📄 Данный бот может конвертировать файлы с одного типа в другое\n\nВыберите наиболее подходящий вариант для Вас.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode=None,
            reply_markup=choicestart
        )


@router.message(Form.waiting_mp4_file)
async def process_video(message: Message, state: FSMContext):
    if message.document and message.document.mime_type == "video/mp4":
        await message.reply(" Получил видео, начинаю конвертацию...")
        try:
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            file_size = file_info.file_size

            if file_size > MAX_FILE_SIZE:
                await message.reply("❌ Ошибка: размер файла превышает 20 МБ. Пожалуйста, отправьте файл меньшего размера.")
                return

            video_file_bytes = await bot.download_file(file_path)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_file_bytes.getvalue())
                temp_file_path = temp_file.name

            video = VideoFileClip(temp_file_path)
            mp3_file = "audio.mp3"
            video.audio.write_audiofile(mp3_file)
            video.close()

            chat_id = message.chat.id
            reply_message_id = message.message_id

            audio_file = types.FSInputFile("audio.mp3")

            await bot.send_audio(chat_id, audio_file, reply_to_message_id=reply_message_id)

            await message.reply("✅ Конвертация завершена!", reply_markup=cancel)

            os.remove(temp_file_path)
            os.remove("audio.mp3")
            await state.clear()

        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}\n{traceback.format_exc()}")
            return
    else:
        await message.reply("❌ Пожалуйста, отправьте корректный MP4 файл.")

@router.message(Form.waiting_mp4wav_file)
async def process_video2(message: Message, state: FSMContext):
    if message.document and message.document.mime_type == "video/mp4":
        await message.reply("Получил видео, начинаю конвертацию...")
        try:
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            file_size = file_info.file_size

            if file_size > MAX_FILE_SIZE:
                await message.reply("❌ Ошибка: размер файла превышает 20 МБ. Пожалуйста, отправьте файл меньшего размера.")
                return

            video_file_bytes = await bot.download_file(file_path)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_file_bytes.getvalue())
                temp_file_path = temp_file.name

            video = VideoFileClip(temp_file_path)
            wav_file = "audio.wav"
            video.audio.write_audiofile(wav_file)
            video.close()

            chat_id = message.chat.id
            reply_message_id = message.message_id

            audio_file = types.FSInputFile(wav_file)

            await bot.send_audio(chat_id, audio_file, reply_to_message_id=reply_message_id)

            await message.reply("✅ Конвертация завершена!", reply_markup=cancel)

            os.remove(temp_file_path)
            os.remove(wav_file)
            await state.clear()

        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}\n{traceback.format_exc()}")
            return
    else:
        await message.reply("❌ Пожалуйста, отправьте корректный MP4 файл.")

@router.message(Form.waiting_mp4flac_file)
async def process_video3(message: Message, state: FSMContext):
    if message.document and message.document.mime_type == "video/mp4":
        await message.reply("Получил видео, начинаю конвертацию...")
        try:
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            file_size = file_info.file_size

            if file_size > MAX_FILE_SIZE:
                await message.reply("❌ Ошибка: размер файла превышает 20 МБ. Пожалуйста, отправьте файл меньшего размера.")
                return

            video_file_bytes = await bot.download_file(file_path)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_file_bytes.getvalue())
                temp_file_path = temp_file.name

            video = VideoFileClip(temp_file_path)
            flac_file = "audio.flac"
            video.audio.write_audiofile(flac_file)
            video.close()

            chat_id = message.chat.id
            reply_message_id = message.message_id

            audio_file = types.FSInputFile(flac_file)

            await bot.send_audio(chat_id, audio_file, reply_to_message_id=reply_message_id)

            await message.reply("✅ Конвертация завершена!", reply_markup=cancel)

            os.remove(temp_file_path)
            os.remove(flac_file)
            await state.clear()

        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}\n{traceback.format_exc()}")
            return
    else:
        await message.reply("❌ Пожалуйста, отправьте корректный MP4 файл.")

@router.message(Form.waiting_mp4opus_file)
async def process_video4(message: Message, state: FSMContext):
    if message.document and message.document.mime_type == "video/mp4":
        await message.reply("Получил видео, начинаю конвертацию...")
        try:
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            file_size = file_info.file_size

            if file_size > MAX_FILE_SIZE:
                await message.reply("❌ Ошибка: размер файла превышает 20 МБ. Пожалуйста, отправьте файл меньшего размера.")
                return

            video_file_bytes = await bot.download_file(file_path)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_file_bytes.getvalue())
                temp_file_path = temp_file.name

            video = VideoFileClip(temp_file_path)
            opus_file = "audio.opus"
            video.audio.write_audiofile(opus_file)
            video.close()

            chat_id = message.chat.id
            reply_message_id = message.message_id

            audio_file = types.FSInputFile(opus_file)

            await bot.send_audio(chat_id, audio_file, reply_to_message_id=reply_message_id)

            await message.reply("✅ Конвертация завершена!", reply_markup=cancel)

            os.remove(temp_file_path)
            os.remove(opus_file)
            await state.clear()

        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}\n{traceback.format_exc()}")
            return
    else:
        await message.reply("❌ Пожалуйста, отправьте корректный MP4 файл.")

@router.message(Form.waiting_mp4ogg_file)
async def process_video5(message: Message, state: FSMContext):
    if message.document and message.document.mime_type == "video/mp4":
        await message.reply("Получил видео, начинаю конвертацию...")
        try:
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            file_size = file_info.file_size

            if file_size > MAX_FILE_SIZE:
                await message.reply("❌ Ошибка: размер файла превышает 20 МБ. Пожалуйста, отправьте файл меньшего размера.")
                return

            video_file_bytes = await bot.download_file(file_path)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_file_bytes.getvalue())
                temp_file_path = temp_file.name

            video = VideoFileClip(temp_file_path)
            ogg_file = "audio.ogg"
            video.audio.write_audiofile(ogg_file)
            video.close()

            chat_id = message.chat.id
            reply_message_id = message.message_id

            audio_file = types.FSInputFile(ogg_file)

            await bot.send_audio(chat_id, audio_file, reply_to_message_id=reply_message_id)

            await message.reply("✅ Конвертация завершена!", reply_markup=cancel)

            os.remove(temp_file_path)
            os.remove(ogg_file)
            await state.clear()

        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}\n{traceback.format_exc()}")
            return
    else:
        await message.reply("❌ Пожалуйста, отправьте корректный MP4 файл.")

@router.message(Form.waiting_mp4mpeg_file)
async def convert_video(message: Message):
    video_file = message.document
    if not video_file or video_file.mime_type != 'video/mp4':
        await message.reply("❌ Пожалуйста, отправьте видеофайл в формате MP4.")
        return

    await message.reply("🎬 Скачиваю видеофайл...")

    file_path = None
    output_path = None

    try:
        file_info = await bot.get_file(video_file.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            await bot.download_file(file_info.file_path, destination=tmp_file.name)
            file_path = tmp_file.name

        await message.reply("⏳ Конвертирую видео...")

        output_path = os.path.splitext(file_path)[0] + ".mpeg"

        try:
            clip = VideoFileClip(file_path)
            clip.write_videofile(output_path, codec="mpeg4")
            clip.close()
        except Exception as e:
            error_message = f"❌ Ошибка конвертации: {e}"
            print(error_message)
            logging.exception("Ошибка конвертации видео")
            await message.reply(error_message)
            return

        await message.reply("⏳ Отправляю конвертированное видео...")

        file_size = os.path.getsize(output_path)
        max_telegram_size = 50 * 1024 * 1024

        if file_size > max_telegram_size:
            await message.reply("⚠️ Видео слишком большое для отправки напрямую.")
        else:
            try:
                with open(output_path, 'rb') as video_file:
                    media = types.InputMediaVideo(media=types.FSInputFile(output_path, filename="video.mpeg"))

                    await bot.send_media_group(message.chat.id, [media])

                await message.reply("✅ Видео успешно сконвертировано и отправлено!", reply_markup=cancel)

            except Exception as e:
                error_message = f"❌ Ошибка отправки: {e}"
                print(error_message)
                logging.exception("Ошибка отправки видео")
                await message.reply(error_message)

    finally:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {file_path}: {e}")
                logging.error(f"Ошибка удаления файла {file_path}: {e}")
        if output_path:
            try:
                os.remove(output_path)
                print(f"Файл {output_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {output_path}: {e}")
                logging.error(f"Ошибка удаления файла {output_path}: {e}")

@router.message(Form.waiting_mp4avi_file)
async def convert_video2(message: Message):
    video_file = message.document
    if not video_file or video_file.mime_type != 'video/mp4':
        await message.reply("❌ Пожалуйста, отправьте видеофайл в формате MP4.")
        return

    await message.reply("🎬 Скачиваю видеофайл...")

    file_path = None
    output_path = None

    try:
        file_info = await bot.get_file(video_file.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            await bot.download_file(file_info.file_path, destination=tmp_file.name)
            file_path = tmp_file.name

        await message.reply("⏳ Конвертирую видео...")

        output_path = os.path.splitext(file_path)[0] + ".avi"

        try:
            clip = VideoFileClip(file_path)
            clip.write_videofile(output_path, codec="libx264")
            clip.close()
        except Exception as e:
            error_message = f"❌ Ошибка конвертации: {e}"
            print(error_message)
            logging.exception("Ошибка конвертации видео")
            await message.reply(error_message)
            return

        await message.reply("⏳ Отправляю конвертированное видео...")

        file_size = os.path.getsize(output_path)
        max_telegram_size = 50 * 1024 * 1024

        if file_size > max_telegram_size:
            await message.reply("⚠️ Видео слишком большое для отправки напрямую.")
        else:
            try:
                with open(output_path, 'rb') as video_file:
                    media = types.InputMediaVideo(media=types.FSInputFile(output_path, filename="video.avi"))

                    await bot.send_media_group(message.chat.id, [media])

                await message.reply("✅ Видео успешно сконвертировано и отправлено!", reply_markup=cancel)

            except Exception as e:
                error_message = f"❌ Ошибка отправки: {e}"
                print(error_message)
                logging.exception("Ошибка отправки видео")
                await message.reply(error_message)

    finally:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {file_path}: {e}")
                logging.error(f"Ошибка удаления файла {file_path}: {e}")
        if output_path:
            try:
                os.remove(output_path)
                print(f"Файл {output_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {output_path}: {e}")
                logging.error(f"Ошибка удаления файла {output_path}: {e}")

@router.message(Form.waiting_mp4mov_file)
async def convert_video3(message: Message):
    video_file = message.document
    if not video_file or video_file.mime_type != 'video/mp4':
        await message.reply("❌ Пожалуйста, отправьте видеофайл в формате MP4.")
        return

    await message.reply("🎬 Скачиваю видеофайл...")

    file_path = None
    output_path = None

    try:
        file_info = await bot.get_file(video_file.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            await bot.download_file(file_info.file_path, destination=tmp_file.name)
            file_path = tmp_file.name

        await message.reply("⏳ Конвертирую видео...")

        output_path = os.path.splitext(file_path)[0] + ".mov"

        try:
            clip = VideoFileClip(file_path)
            clip.write_videofile(output_path, codec="libx264")
            clip.close()
        except Exception as e:
            error_message = f"❌ Ошибка конвертации: {e}"
            print(error_message)
            logging.exception("Ошибка конвертации видео")
            await message.reply(error_message)
            return

        await message.reply("⏳ Отправляю конвертированное видео...")

        file_size = os.path.getsize(output_path)
        max_telegram_size = 50 * 1024 * 1024

        if file_size > max_telegram_size:
            await message.reply("⚠️ Видео слишком большое для отправки напрямую.")
        else:
            try:
                with open(output_path, 'rb') as video_file:
                    media = types.InputMediaVideo(media=types.FSInputFile(output_path, filename="video.mov"))

                    await bot.send_media_group(message.chat.id, [media])

                await message.reply("✅ Видео успешно сконвертировано и отправлено!", reply_markup=cancel)

            except Exception as e:
                error_message = f"❌ Ошибка отправки: {e}"
                print(error_message)
                logging.exception("Ошибка отправки видео")
                await message.reply(error_message)

    finally:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {file_path}: {e}")
                logging.error(f"Ошибка удаления файла {file_path}: {e}")
        if output_path:
            try:
                os.remove(output_path)
                print(f"Файл {output_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {output_path}: {e}")
                logging.error(f"Ошибка удаления файла {output_path}: {e}")

@router.message(Form.waiting_avi_file)
async def convert_video4(message: Message):
    video_file = message.document
    if not video_file or video_file.mime_type != 'video/avi':
        await message.reply("❌ Пожалуйста, отправьте видеофайл в формате AVI.")
        return

    await message.reply("🎬 Скачиваю видеофайл...")

    file_path = None
    output_path = None

    try:
        file_info = await bot.get_file(video_file.file_id)

        with tempfile.NamedTemporaryFile(suffix=".avi", delete=False) as tmp_file:
            await bot.download_file(file_info.file_path, destination=tmp_file.name)
            file_path = tmp_file.name

        await message.reply("⏳ Конвертирую видео...")

        output_path = os.path.splitext(file_path)[0] + ".mp4"

        try:
            clip = VideoFileClip(file_path)
            clip.write_videofile(output_path, codec="libx264")
            clip.close()
        except Exception as e:
            error_message = f"❌ Ошибка конвертации: {e}"
            print(error_message)
            logging.exception("Ошибка конвертации видео")
            await message.reply(error_message)
            return

        await message.reply("⏳ Отправляю конвертированное видео...")

        file_size = os.path.getsize(output_path)
        max_telegram_size = 50 * 1024 * 1024

        if file_size > max_telegram_size:
            await message.reply("⚠️ Видео слишком большое для отправки напрямую.")
        else:
            try:
                with open(output_path, 'rb') as video_file:
                    media = types.InputMediaVideo(media=types.FSInputFile(output_path, filename="video.mp4"))

                    await bot.send_media_group(message.chat.id, [media])

                await message.reply("✅ Видео успешно сконвертировано и отправлено!", reply_markup=cancel)

            except Exception as e:
                error_message = f"❌ Ошибка отправки: {e}"
                print(error_message)
                logging.exception("Ошибка отправки видео")
                await message.reply(error_message)

    finally:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {file_path}: {e}")
                logging.error(f"Ошибка удаления файла {file_path}: {e}")
        if output_path:
            try:
                os.remove(output_path)
                print(f"Файл {output_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {output_path}: {e}")
                logging.error(f"Ошибка удаления файла {output_path}: {e}")

@router.message(Form.waiting_mpeg_file)
async def convert_video5(message: Message):
    video_file = message.document
    if not video_file or video_file.mime_type != 'video/mpeg':
        await message.reply("❌ Пожалуйста, отправьте видеофайл в формате MPEG.")
        return

    await message.reply("🎬 Скачиваю видеофайл...")

    file_path = None
    output_path = None

    try:
        file_info = await bot.get_file(video_file.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mpeg", delete=False) as tmp_file:
            await bot.download_file(file_info.file_path, destination=tmp_file.name)
            file_path = tmp_file.name

        await message.reply("⏳ Конвертирую видео...")

        output_path = os.path.splitext(file_path)[0] + ".mp4"

        try:
            clip = VideoFileClip(file_path)
            clip.write_videofile(output_path, codec="libx264")
            clip.close()
        except Exception as e:
            error_message = f"❌ Ошибка конвертации: {e}"
            print(error_message)
            logging.exception("Ошибка конвертации видео")
            await message.reply(error_message)
            return

        await message.reply("⏳ Отправляю конвертированное видео...")

        file_size = os.path.getsize(output_path)
        max_telegram_size = 50 * 1024 * 1024

        if file_size > max_telegram_size:
            await message.reply("⚠️ Видео слишком большое для отправки напрямую.")
        else:
            try:
                with open(output_path, 'rb') as video_file:
                    media = types.InputMediaVideo(media=types.FSInputFile(output_path, filename="video.mp4"))

                    await bot.send_media_group(message.chat.id, [media])

                await message.reply("✅ Видео успешно сконвертировано и отправлено!", reply_markup=cancel)

            except Exception as e:
                error_message = f"❌ Ошибка отправки: {e}"
                print(error_message)
                logging.exception("Ошибка отправки видео")
                await message.reply(error_message)

    finally:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {file_path}: {e}")
                logging.error(f"Ошибка удаления файла {file_path}: {e}")
        if output_path:
            try:
                os.remove(output_path)
                print(f"Файл {output_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {output_path}: {e}")
                logging.error(f"Ошибка удаления файла {output_path}: {e}")

@router.message(Form.waiting_mov_file)
async def convert_video6(message: Message):
    video_file = message.document
    if not video_file or video_file.mime_type != 'video/mov':
        await message.reply("❌ Пожалуйста, отправьте видеофайл в формате MOV.")
        return

    await message.reply("🎬 Скачиваю видеофайл...")

    file_path = None
    output_path = None

    try:
        file_info = await bot.get_file(video_file.file_id)

        with tempfile.NamedTemporaryFile(suffix=".mov", delete=False) as tmp_file:
            await bot.download_file(file_info.file_path, destination=tmp_file.name)
            file_path = tmp_file.name

        await message.reply("⏳ Конвертирую видео...")

        output_path = os.path.splitext(file_path)[0] + ".mp4"

        try:
            clip = VideoFileClip(file_path)
            clip.write_videofile(output_path, codec="libx264")
            clip.close()
        except Exception as e:
            error_message = f"❌ Ошибка конвертации: {e}"
            print(error_message)
            logging.exception("Ошибка конвертации видео")
            await message.reply(error_message)
            return

        await message.reply("⏳ Отправляю конвертированное видео...")

        file_size = os.path.getsize(output_path)
        max_telegram_size = 50 * 1024 * 1024

        if file_size > max_telegram_size:
            await message.reply("⚠️ Видео слишком большое для отправки напрямую.")
        else:
            try:
                with open(output_path, 'rb') as video_file:
                    media = types.InputMediaVideo(media=types.FSInputFile(output_path, filename="video.mp4"))

                    await bot.send_media_group(message.chat.id, [media])

                await message.reply("✅ Видео успешно сконвертировано и отправлено!", reply_markup=cancel)

            except Exception as e:
                error_message = f"❌ Ошибка отправки: {e}"
                print(error_message)
                logging.exception("Ошибка отправки видео")
                await message.reply(error_message)

    finally:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {file_path}: {e}")
                logging.error(f"Ошибка удаления файла {file_path}: {e}")
        if output_path:
            try:
                os.remove(output_path)
                print(f"Файл {output_path} удален.")
            except Exception as e:
                print(f"Ошибка удаления файла {output_path}: {e}")
                logging.error(f"Ошибка удаления файла {output_path}: {e}")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
