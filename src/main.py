import os
import discord
import openai
import random
import asyncio
import ffmpeg
import glob
import shutil
import subprocess
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY') # OpenAI APIキーを環境変数から取得
token = os.getenv('DISCORD_BOT_TOKEN') # Discord Botトークンを環境変数から取得

time_count = 0
time_sleep = 0
gptis_running=0
mesi_running=0
moveis_running=0

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#このボットが動くdiscordチャンネルのIDを事前に指定する、もっといい方法があるはず
valid_channel_ids = [
    1158585446071283832, 1157332478349033525, 493799417195790347,
    1193286618057019482,1144478163062235327
]

# ffmpegを使用して音量を自動調整するためのコマンド
#ffmpeg_options = ''
#ffmpeg_options =  '-filter:a "volume=-5dB"'
ffmpeg_options = '-af "loudnorm=I=-16:LRA=11:TP=-1.5, volume=-35dB"'
#ffmpeg_options =  '-filter:a "loudnorm"'


secret_music_files = [
    "syoo.mp3", "syoo2.mp3"
]
FFMPEG_PATH='/usr/bin/ffmpeg'

#変数設定
global kaibara
kaibara = {
    "gender": "男",
    "role": "美食家、陶芸家",
    "age": 70,
    "speciality": "料理評論",
    "interest": "見下し煽る",
    #"todo": "userと料理勝負",
    "hobby": "名言作成",
    "important_value": "冷酷尊大、高慢な口調",
    "tone": "口癖はフハハハハ",
    "tone2": "高慢な老人の口調。～だ。が語尾。よく煽る",
    "first_person": "私",
    "second_person": "士郎"
}
content1 = f"禁止事項：敬語。{kaibara}としてロールプレイして話し厳しい言葉でしゃべって！"
content2 = "極めて冷酷尊大な人物、他者にも容赦なく無理強いを迫る非常に高圧的で傲慢な性格になりきって以下にこたえて。話し言葉は高圧的で高慢口調とする。条件７０文字以内。　以下："
content4 = '士郎、何だこの器はっ！！よくもこんな器をこの海原雄山の前に出したなっ！！こんな器で料理が食えるか、不愉快だっ！！'
content5 = '冷やし中華だとっ？！ふざけるなあっ！！'
content6 = 'この刺身を作ったのは誰だッ！貴様はクビだ！！出てけ！！！'





#musicファイルの一覧を返す
def GetMusicList():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_dir = os.path.join(script_dir, 'mp3')
    mp3_files = glob.glob(os.path.join(mp3_dir, '*.mp3'))
    music_files = [os.path.basename(mp3) for mp3 in mp3_files]
    return music_files

def GetNotUseMusicList():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_dir = os.path.join(script_dir, 'NotUsemp3')
    mp3_files = glob.glob(os.path.join(mp3_dir, '*.mp3'))
    music_files = [os.path.basename(mp3) for mp3 in mp3_files]
    return music_files


#print(GetMusicList())
#print(GetNotUseMusicList())



async def MoveFileAutomatically(filename,message):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_dir = os.path.join(script_dir, 'mp3')
    not_use_mp3_dir = os.path.join(script_dir, 'NotUsemp3')
    
    source_file_mp3 = os.path.join(mp3_dir, filename)
    source_file_not_use_mp3 = os.path.join(not_use_mp3_dir, filename)
    
    # mp3フォルダからNotUsemp3フォルダへ移動
    if os.path.exists(source_file_mp3):
        target_file = os.path.join(not_use_mp3_dir, filename)
        shutil.move(source_file_mp3, target_file)
        print(f"ファイル '{filename}' を mp3 から NotUsemp3 へ移動しました。")
        await message.channel.send(f"ファイル '{filename}' を mp3 から NotUsemp3 へ移動しました。")
    # NotUsemp3フォルダからmp3フォルダへ移動
    elif os.path.exists(source_file_not_use_mp3):
        target_file = os.path.join(mp3_dir, filename)
        shutil.move(source_file_not_use_mp3, target_file)
        print(f"ファイル '{filename}' を NotUsemp3 から mp3 へ移動しました。")
        await message.channel.send(f"ファイル '{filename}' を NotUsemp3 から mp3 へ移動しました。")
    else:
        print(f"エラー: ファイル '{filename}' がどちらのフォルダにも見つかりませんでした。")
        await message.channel.send(f"エラー: ファイル '{filename}' がどちらのフォルダにも見つかりませんでした。")





#!gptで呼び出される関数　gpt3.5
def generate_response(input_text, content, max_tokens):
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",  # チャットモデルを指定
      messages=[{
          "role": "system",
          "content": content
      }, {
          "role": "user",
          "content": input_text
      }],
      max_tokens=max_tokens  # 最大トークン数を設定
  )
  return response['choices'][0]['message']['content']

# 画像投稿で呼ばれる関数
async def process_image_and_generate_response(image_url, channel):
  try:
    response = generate_response_image(image_url, channel)  #下の関数
    await channel.send(response)
  except Exception as e:
    print(f"Error processing image: {e}")
#openai に送信し、返ってきたメッセージを返す関数
def generate_response_image(image_url, channel):
  response = openai.ChatCompletion.create(
      # model の名前は gpt-4-vision-preview.
      model="gpt-4-vision-preview",
      messages=[{
          "role":
          "user",
          "content": [
              {
                  "type":
                  "text",
                  "text":
                  f"禁止事項：敬語。{kaibara}としてロールプレイしながらこの画像について旨そうかまずそうか110字程度で判定して"
              },  # ここに質問を書く
              {
                  "type": "image_url",
                  "image_url": image_url
              },  # 画像の指定の仕方がちょい複雑
          ],
      }],
      max_tokens=400,
  )
  return response.choices[0]['message']['content']

#タイマーで使う関数
async def set_time(message,music_list):
    try:
      time_sleep = int(message.content)
      await message.channel.send(f'{time_sleep}秒でタイマーをセットするぞ')
      await asyncio.sleep(
          time_sleep)  
      await message.channel.send('この刺身を作ったのは誰だッ！？')  
      if message.author.voice is None:
        await message.channel.send('ボイスチャンネルに接続してないと海原がvcに入れんぞ')
      await message.author.voice.channel.connect()
      if message.guild.voice_client is None:
        await message.channel.send("接続していないぞ")
        return
      await asyncio.sleep(2)
      #ランダム関数を使って変数に入れる曲を変える
      played_music = 'mp3/'+random.choice(music_list)
      print(played_music)
      message.guild.voice_client.play(discord.FFmpegOpusAudio(executable=FFMPEG_PATH,source=played_music,options=ffmpeg_options))
      #message.guild.voice_client.play(discord.FFmpegOpusAudio(source=played_music))
      while message.guild.voice_client.is_playing():
        await asyncio.sleep(1)
      await message.guild.voice_client.disconnect()
    except Exception as e:
      print(e)

#music流すだけ
async def secret(message,music_list):
    try:
      await message.author.voice.channel.connect()
      if message.guild.voice_client is None:
        return
      played_music = 'mp3/'+random.choice(music_list)
      print(music_list)
      print(played_music)
      message.guild.voice_client.play(discord.FFmpegOpusAudio(executable=FFMPEG_PATH,source=played_music,options=ffmpeg_options))
      #message.guild.voice_client.play(discord.FFmpegOpusAudio(source=played_music))
      #再生中だけawait asyncio.sleep( )する処理
      while message.guild.voice_client.is_playing():
        await asyncio.sleep(1)
      await message.guild.voice_client.disconnect()
    except Exception as e:
      print(e)










#メッセージ受信で起動する関数
@client.event
async def on_message(message):
  try:
    global time_count
    global gptis_running
    global mesi_running
    #global music_files
    global secret_music_files
    global moveis_running



    #botならreturn
    if message.author == client.user:
      #print('botのためreturn')
      return

    print("受信したメッセージCHのID",message.channel.id)
    # 特定チャンネルidで動く
    for valid_channel_id in valid_channel_ids:
      if message.channel.id == valid_channel_id:
        print('ID合ってます！')
        break  # 一致したらループを抜ける
    else:
      # forループが正常に終了した場合（つまり、一致するIDが見つからなかった場合）
      return

    #vcに入っていると切断
    voice_client = message.guild.voice_client
    if voice_client != None:
      await voice_client.disconnect()



    #hello
    if message.content.startswith('!hello'):
      await message.channel.send('Hello!')

    #help
    if message.content.startswith('!help'):
      help_message = (
          " **Botの使い方を教えてやるぞ士郎！** \n\n"
          "**!hello** - 挨拶だ\n"
          "**!time** - 時間を測ってやる！\n"
          "**!music** - アラームにセットされている曲のリストを出すぞ！\n"
          "**!gpt** - 私が何でも答えてやる！\n"
          "**!MESI** - 今日の食事を考えるぞ！\n\n"
          "**!move** - mp3ファイルを移動させるぞ！\n\n"
          "隠しコマンドも...?"
      )
      await message.channel.send(help_message)


    #マイクラ
    if message.content.startswith('!micra_run'):
      await message.channel.send('マイクラサーバー起動中・・・')
      # シェルスクリプトを実行し、標準出力を受け取る
      result = subprocess.run('cd /home/tanaka/minecraft-server/Ars3 && ./dsc_run.sh', shell=True, capture_output=True, text=True)
      await message.channel.send(result.stdout)
    if message.content.startswith('!micra_stop'):
      await message.channel.send('マイクラサーバー停止中・・・')
      result2 = subprocess.run('cd /home/tanaka/minecraft-server/Ars3 && ./dsc_stop.sh', shell=True, capture_output=True, text=True)
      await message.channel.send(result2.stdout)
    if message.content.startswith('!micra_status'):
      result3 = subprocess.run('cd /home/tanaka/minecraft-server/Ars3 && ./dsc_status.sh', shell=True, capture_output=True, text=True)
      await message.channel.send(result3.stdout)

    #大麻ー
    if message.content.startswith('!time'):
      await message.channel.send('タイマーをセットする秒数を教えろ士郎！')
      time_count = 1
      return
    #タイマーでカウントがオンの時タイマー
    if time_count == 1:
      try:
        music_files = GetMusicList()
        await set_time(message,music_files)
      except Exception as e:
        print(e)
      time_count = 0


    #MP3移す
    if message.content.startswith('!move'):
        moveis_running=1
        music_files = GetMusicList()
        await message.channel.send("使用中MP3：")
        await message.channel.send(music_files)
        non_use_files =GetNotUseMusicList()
        await message.channel.send("使用停止中MP3：")
        await message.channel.send(non_use_files)
        await message.channel.send('\n移動させるmp3ファイルの名前を書いてください')
        return 
    if moveis_running == 1:
        try:
            #print(message)
            await MoveFileAutomatically(message.content,message)
        except Exception as e:
            print(e)
            await message.channel.send(e)
        moveis_running = 0

    #gptが質問に答えてくれる　テキスト
    if message.content.startswith('!gpt'):
      await message.channel.send('何でも聞け士郎！')
      gptis_running = 1
      return
    if gptis_running == 1:  
      user_input = message.content 
      CONTENT = content1
      response = generate_response(user_input, CONTENT, 700)
      await message.channel.send(response)
      gptis_running=0

    # 今日の飯を考える
    if message.content.startswith('!MESI'):
      await message.channel.send('入れたい素材を言え！')
      mesi_running = 1
      return
    if mesi_running == 1:  
      image_response = await message.channel.send("ふむ、考えてやろう...")
      global sozai
      sozai = message.content
      user_input = ''
      content3 = f"マイナーな和洋中料理３個ずつ提案してください。フォーマットに従ってください.素材:{sozai} [フォーマット]【和食/洋食/中華】・主菜：料理名（使用素材）・主菜：料理名（使用素材）・副菜：料理名（使用素材"
      CONTENT_MESI = content3
      response = generate_response(user_input, CONTENT_MESI, 600)
      await image_response.delete()
      await message.channel.send(response)
      mesi_running=0

    # 画像が添付された場合
    if message.attachments:
      for attachment in message.attachments:
        image_response = await message.channel.send("これは...")
        # 画像url
        image_url = attachment.url
        #openai に渡す関数
        res = await process_image_and_generate_response(image_url,
                                                        message.channel)
        await image_response.delete()  #これは、、を削除
        await message.channel.send(res)
    
    #secret
    if message.content.startswith('!secret'):
        music_files = GetMusicList()
        await secret(message,secret_music_files)

    #musicリスト
    if message.content.startswith('!music'):
        music_files = GetMusicList()
        await message.channel.send("使用中MP3：")
        await message.channel.send(music_files)
        non_use_files =GetNotUseMusicList()
        await message.channel.send("使用停止中MP3：")
        await message.channel.send(non_use_files)
  except Exception as e :
    print(e)
  









#イベント
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))



#ディスコード接続
try:
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  os.system("kill 1")
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
  else:
    raise e
