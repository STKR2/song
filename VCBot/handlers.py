from VCBot.queues import QUEUE, get_queue, pop_an_item, clear_queue
from config import bot, call_py
from pytgcalls import StreamType
from pyrogram import Client
from pyrogram.raw.base import Update
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.stream import StreamAudioEnded  

async def skip_current_song(chat_id):
   if chat_id in QUEUE:
      chat_queue = get_queue(chat_id)
      if len(chat_queue)==1:
         await call_py.leave_group_call(chat_id)
         clear_queue(chat_id)
         return 1
      else:
         songname = chat_queue[1][0]
         url = chat_queue[1][1]
         link = chat_queue[1][2]
         await call_py.change_stream(
            chat_id,
            AudioPiped(
               url,
            )
         ) 
         pop_an_item(chat_id)
         return [songname, link]
   else:
      return 0

async def skip_item(chat_id, h):
   if chat_id in QUEUE:
      chat_queue = get_queue(chat_id)
      try:
         x = int(h)
         songname = chat_queue[x][0]
         chat_queue.pop(x)
         return songname
      except Exception as e:
         print(e)
         return 0
   else:
      return 0
      

@call_py.on_stream_end()
async def on_end_handler(client, update: Update):
   if isinstance(update, StreamAudioEnded):
      chat_id = update.chat_id
      print(chat_id)
      op = await skip_current_song(chat_id)
      if op==1:
         await bot.send_message(chat_id, "`قائمة الانتضار فارغة ، مغادرة الدردشة الصوتية 🚶🍃💓...`")
      else:
         await bot.send_message(chat_id, f"**🎧 الان يشغل** \n[{op[0]}]({op[1]})", disable_web_page_preview=True)
   else:
      pass
