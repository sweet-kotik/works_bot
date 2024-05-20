import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.rss_parser import work_parser
import os
from dotenv import load_dotenv

router = Router()
load_dotenv()

CHAT_ID = os.getenv('CHAT_ID')
ADMIN_ID = os.getenv('ADMIN_ID')

class Posting(StatesGroup):
    post = State()

""" @router.message(F.text)
async def echo(message: Message):
    chat_id = message.chat.id
    try:
        msg_thread_id = message.reply_to_message.message_thread_id
    except AttributeError:
        msg_thread_id = "General"
    await message.answer(f'{chat_id}\n{msg_thread_id}') """


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Hi!')

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Help')

@router.message(Command('stop_posting'), Posting.post)
async def stop_posting(message: Message, state: FSMContext):

    task.cancel()
    await message.answer('Stop posting')
    await state.clear()
    

@router.message(Command('rss_posting'))
async def rss_posting(message: Message, state: FSMContext):

    global task
    await state.set_state(Posting.post)
    task = asyncio.create_task(work_parser(message, CHAT_ID))
    await task