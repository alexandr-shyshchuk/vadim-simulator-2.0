from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import voice
import config

bot = Bot(config.tg_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


labels = {}

class botStates(Helper):
    mode = HelperMode.snake_case

    DEFAULT_STATE = ListItem()
    SET_VOICE_NAME = ListItem()
    SET_VOICE = ListItem()


@dp.message_handler(state='*', commands=["start", 'cancel'])
async def cmd_start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(botStates.DEFAULT_STATE[0])
    await bot.send_message(chat_id=message.chat.id, text="State rested")
    try:
        labels.pop(message.from_user.id)
    except:
        pass


@dp.message_handler(state='*', commands=['addVoice'])
async def add_voice(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.reply('Send name: ', reply=False)
    await state.set_state(botStates.SET_VOICE_NAME[0])


@dp.message_handler(state=botStates.SET_VOICE_NAME, content_types=['text'])
async def set_voice_name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    labels[message.from_user.id] = message.text
    if voice.is_valid_name(message.text):
        await message.reply('Send voice: ', reply=False)
        await state.set_state(botStates.SET_VOICE[0])
    else:
        await message.reply('invalid key')


@dp.message_handler(state=botStates.SET_VOICE, content_types=['voice'])
async def third_or_fourth_test_state_case_met(message: types.Message):
    await message.voice.download('voices/'+labels[message.from_user.id]+'.mp3')
    await message.reply(labels[message.from_user.id])
    labels.pop(message.from_user.id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
