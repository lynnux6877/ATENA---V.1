import discord
import openai
from discord.ext import commands
from mylife import ATHENAS
import os

# Configuração do token do Discord
TOKEN = os.environ['DISCORD_BOT_TOKEN']

# Configuração da chave da API do OpenAI
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

async def buscar_historico_canal(canal,limit=5):
  messages_list = []

  async for message in canal.history(limit=limit):
      messages_list.append(
          {
              "role":"user" if message.author.id!=client.user.id else "system",
              "content":message.content
          }
      )

  messages_list.reverse()
  return messages_list

# Configuração do nome e da personalidade do bot
BOT_NAME = ""
AUTHORIZED_USER_ID = int(os.environ['AUTHORIZED_USER_ID'])
PERSONA = ATHENAS
# Inicialização do cliente do Discord
intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)


# Configuração da API do OpenAI
openai.api_key = OPENAI_API_KEY

def enviar_para_openai(msg):
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0125",
      messages=[{"role": "system", "content": f"{PERSONA}: {msg}"}]
  )
  return response.choices[0].message['content']

# Evento de inicialização do bot do Discord
@client.event
async def on_ready():
    print(f"O {client.user.name} ficou ligado!")
    await client.change_presence(activity=discord.CustomActivity(emoji="👉",name="Sábia guerreira."))

# Evento de resposta a mensagens no Discord
@client.event
async def on_message(message):
    # Verifica se a mensagem foi enviada por um bot para evitar loops
    if message.author.bot or message.author.id != AUTHORIZED_USER_ID:
        return
    async with message.channel.typing():
        # Verifica se a mensagem menciona o nome do bot
        if BOT_NAME.lower() in message.content.lower():
            # Remove o nome do bot da mensagem
            msg = message.content.replace(BOT_NAME, "")

            # Envia a mensagem para o modelo da OpenAI
            response = enviar_para_openai(msg)

            # Envia a resposta para o canal do Discord
            await message.reply(response)



# Conecta o bot ao Discord

client.run(TOKEN)
