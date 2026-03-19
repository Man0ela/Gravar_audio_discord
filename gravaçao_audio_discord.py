import discord
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()


intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = discord.Bot(intents=intents) 
connections = {}

@bot.command()
async def record(ctx):
    await ctx.defer() 
    
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("Você não está em um canal de voz")

    # limpa conexões fantasmas e aguarda estabilidade
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await asyncio.sleep(1)
    
    print("Tentando conectar ao canal de voz")
    try:
        vc = await asyncio.wait_for(voice.channel.connect(reconnect=False), timeout=15.0)
        connections.update({ctx.guild.id: vc})
    except asyncio.TimeoutError:
        print("ERRO: O servidor não respondeu. Possível bloqueio de porta UDP.")
        return await ctx.respond("O servidor bloqueou a conexão de voz.")
    except Exception as e:
        print(f"ERRO TÉCNICO: {e}")
        return await ctx.respond(f"Erro técnico ao conectar: {e}")

    # garante que o handshake de voz (UDP) terminou
    while not vc.is_connected():
        await asyncio.sleep(0.1)
        
    print("Conexão de voz estabelecida. Iniciando gravaçao")

    try:
        vc.start_recording(
            discord.sinks.WaveSink(),
            once_done,
            ctx.channel
        )
        await ctx.respond("Começou a gravar!")
    except Exception as e:
        await ctx.respond(f"Erro ao iniciar gravação: {e}")

async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()
    
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await channel.send(f"Finished recording audio for: {', '.join(recorded_users)}.", files=files)

@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.respond("Parei de gravar!") 
    else:
        await ctx.respond("Não estou gravando nada!")

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN:
    print("Tentando conectar...")
    bot.run(TOKEN)
else:
    print("Erro Verifique o arquivo .env")
