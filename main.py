import os
try:
    import discord
    from discord.ext import commands
except:
    os.system("pip install -r requirements.txt")
    try:
        os.system("clear")
    except:
        pass
    import discord
    from discord.ext import commands
import httpserver    
import db
import time


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

server_id = os.environ['server_id']
bot_token = os.environ['bot_token']

bot_forever = True



@bot.slash_command(name="ping", guild_ids=[server_id], description='Mostra latencia do bot') #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def ping(ctx):
    await ctx.respond(f"Ping: {round(bot.latency * 1000)}ms")

@bot.slash_command(name="slowmode", guild_ids=[server_id], description='Ativa modo lento do canal (somente moderadores)') #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def slowmode(ctx, seconds: int):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.channel.edit(slowmode_delay=seconds) 
        await ctx.respond(f"Slowmode em {seconds} segundos.")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")

@bot.slash_command(name="kick", guild_ids=[server_id], description='Expulsa membro do servidor (somente moderadores)') #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def kick(ctx, member: discord.Member):
    #if ctx.author.guild_permissions.administrator:
    if ctx.author.guild_permissions.manage_channels:
        if member == ctx.guild.owner:
            await ctx.respond("Você não pode expulsar o dono do servidor!")
        else:
            try:
                await member.kick()
                await ctx.respond(f"{member} foi expulso com sucesso.")
            except:
                await ctx.respond(f"{member} não foi expulso.")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")

@bot.slash_command(name="ban", guild_ids=[server_id], description='Bane um membro do servidor (somente administradores)') # Adicione os IDs de servidor nos quais o comando de barra aparecerá. Se deve estar em todos, remova o argumento, mas note que levará algum tempo (até uma hora) para registrar o comando se for para todos os servidores.
async def ban(ctx, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.administrator:
        if member == ctx.guild.owner:
            await ctx.respond("Você não pode banir o dono do servidor!")
        else:       
            try:
                await member.ban(reason=reason)
                await ctx.respond(f"{member} foi banido com sucesso.")
            except:
                await ctx.respond(f"{member} não foi banido.")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")

@bot.slash_command(name="unban", guild_ids=[server_id], description='Desbane um membro do servidor (somente administradores)') # Adicione os IDs de servidor nos quais o comando de barra aparecerá. Se deve estar em todos, remova o argumento, mas note que levará algum tempo (até uma hora) para registrar o comando se for para todos os servidores.
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.administrator:
        member_name, member_discriminator = member.split("#")
    
        async for ban_entry in ctx.guild.bans():
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.respond(f"{user.name}#{user.discriminator} foi desbanido com sucesso.")
                return
    
        await ctx.send(f"Usuário {member} não encontrado na lista de banidos.")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")

@bot.slash_command(name="bans", guild_ids=[server_id], description='Exibe a lista de banidos do servidor')
async def bans(ctx):
    ban_list = []
    async for ban_entry in ctx.guild.bans():
        user = ban_entry.user
        ban_list.append(user)

    if ban_list:
        response = "\n".join([f"{ban.name}#{ban.discriminator}" for ban in ban_list])
        await ctx.respond(f'Aqui está a lista de usuários banidos:\n{response}')
    else:
        await ctx.respond('Não há usuários banidos neste servidor.')
    

@bot.slash_command(name="antilink", guild_ids=[server_id], description='ativa e desativa links no servidor (somente moderador)') #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def antilink(ctx):
    if ctx.author.guild_permissions.manage_messages:
        antilinks = db.get_antilink()
        if antilinks == 'True':
            antilinks = True
        else:
            antilinks = False
        if antilinks:
            db.update_antilink('False')
            antilinks = False
        else:
            db.update_antilink('True')
            antilinks = True
        #await ctx.send(f"Anti-link agora está {'ativado' if not links else 'desativado'}.")
        await ctx.respond(f"Anti-link agora está {'ativado' if antilinks else 'desativado'}.")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")

@bot.slash_command(name="antiflood", guild_ids=[server_id], description='ativa e desativa anti-flood (somente moderador)') #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def antiflood(ctx):
    if ctx.author.guild_permissions.manage_messages:    
        anti_flood = db.get_antiflood()
        if anti_flood == 'True':
            anti_flood = True
        else:
            anti_flood = False
        if anti_flood:
            db.update_antiflood('False')
            anti_flood = False
        else:
            db.update_antiflood('True')
            anti_flood = True
        #await ctx.send(f"Anti-link agora está {'ativado' if not links else 'desativado'}.")
        await ctx.respond(f"Anti-flood agora está {'ativado' if anti_flood else 'desativado'}.")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")


@bot.slash_command(name="cls", guild_ids=[server_id], description='Limpa o chat (somente moderador)') #Adicione as IDs do servidor nas quais o comando de barra aparecerá. Se deve ser em todas, remova o argumento, mas observe que levará algum tempo (até uma hora) para registrar o comando se for para todos os servidores.
async def clear(ctx, amount: int):
    #async def clear(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        try:
            #messages = await ctx.channel.history(limit=None).flatten()
            #message_count = len(messages)
            #diference = message_count - amount
            #if diference >= 0:
            await ctx.respond("Iniciando limpeza do chat...")
            await ctx.channel.purge(limit=amount)
            await ctx.respond("Chat limpo com sucesso!")
            #else:
            #    await ctx.respond("Quantidade superior ao limite de mensagens, use uma menor")
        except:
            await ctx.respond("Falha ao limpar o chat")
    else:
        await ctx.respond("Você não tem permissão para usar este comando.")
    

@bot.slash_command(name="radio", guild_ids=[server_id], description='Toca a rádio coca-cola') #Adicione as IDs do servidor nas quais o comando de barra aparecerá. Se deve ser em todas, remova o argumento, mas observe que levará algum tempo (até uma hora) para registrar o comando se for para todos os servidores.
async def radio(ctx):
    # Verifica se o usuário está em um canal de voz
    if ctx.author.voice is None:
        await ctx.respond('Você precisa estar em um canal de voz para usar esse comando.')
        return
    
    await ctx.respond("Iniciando radio...")
    
    voice_client_ = ctx.guild.voice_client
    if voice_client_:
        await voice_client_.disconnect()

    # Se conecta ao canal de voz do usuário
    voice_client = await ctx.author.voice.channel.connect()

    # Reproduz o stream da rádio
    try:
        radio_stream = discord.FFmpegPCMAudio('https://str3.openstream.co/1084') # coca cola fm
        voice_client.play(radio_stream)
        await ctx.respond("Tocando a radio coca-cola")
    except:
        await ctx.respond("Falha ao tocar o link da radio")

@bot.slash_command(name="radiostop", guild_ids=[server_id], description='Para a rádio web') #Adicione as IDs do servidor nas quais o comando de barra aparecerá. Se deve ser em todas, remova o argumento, mas observe que levará algum tempo (até uma hora) para registrar o comando se for para todos os servidores.
async def radiostop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        try:
            voice_client = bot.voice_clients[0]
            voice_client.stop()
            await voice_client.disconnect()
            await ctx.respond("Radio parada")
        except:
            await ctx.respond("Não foi possivel parar a radio")
    else:
        await ctx.respond("não estou em nenhum canal de voz")


# LISTA OS COMANDO NA CAIXA DE TEXTO

#@bot.command()
@bot.slash_command(name="help", guild_ids=[server_id], description='Lista de comandos disponíveis para TenetBot') #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def help(ctx):
    embed = discord.Embed(title="Ajuda do TenetBot", description="Lista de comandos disponíveis para o TenetBot")

    # Adicione uma linha para cada comando
    embed.add_field(name="/help", value="comando de ajuda", inline=False)
    embed.add_field(name="/antilink", value="ativa ou desativa os links no servidor (somente moderador)", inline=False)
    embed.add_field(name="/antiflood", value="ativa ou desativa o anti-flood (somente moderador)", inline=False)
    embed.add_field(name="/slowmode", value="ativa ou desativa o modo lento (somente moderador)", inline=False)
    embed.add_field(name="/cls", value="Limpa o chat (somente moderador)", inline=False)
    embed.add_field(name="/kick", value="Expulsa membro do servidor (somente moderador)", inline=False)
    embed.add_field(name="/ban", value="Bane um membro do servidor (somente administrador)", inline=False)
    embed.add_field(name="/unban", value="Desbane um membro do servidor (somente administrador)", inline=False)
    embed.add_field(name="/bans", value="Exibie a lista de banidos do servidor", inline=False)       
    embed.add_field(name="/ping", value="Mostra latencia do bot", inline=False)

    await ctx.respond(embed=embed)

    #await ctx.send(embed=embed)
    

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.content.startswith(bot.command_prefix):
            # Trate a mensagem como um comando
            await bot.process_commands(message)
            return
        antilinks = db.get_antilink()
        anti_flood = db.get_antiflood()
        if antilinks == 'True':
            antilinks = True
        else:
            antilinks = False
        if anti_flood == 'True':
            anti_flood = True
        else:
            anti_flood = False            

        if antilinks:
            #if any(word.startswith("http") for word in message.content.split()):
            if any('http' in word for word in message.content.split()):
                await message.delete()
                #await message.author.send("Desculpe, você não pode enviar links neste canal.")
        
        if anti_flood:
            # Get the last 5 messages from the database for this user
            messages = db.get_last_messages(message.author.id)
            # If the user has sent more than 5 messages, check the time between the latest and the 5th latest message
            if len(messages) >= 5:
                time_between_messages = time.time() - messages[4][0]
                # If the time between the latest and 5th latest message is less than 2 seconds, delete the message
                if time_between_messages < 20:
                    await message.delete()
                    await message.author.send("Você está floodando o servidor!.")
                    return
                # erases message history if more than 10 minutes pass from the first registered message
                time_first_message = time.time() - messages[0][0]
                if time_first_message > 600:
                    db.clear_messages(message.author.id)
            # Insert the current message into the database
            db.insert_messages(message.author.id,time.time())
        
        
print('Iniciando servidor')
if bot_forever:
    while True:
        try:
            bot.run(bot_token)
        except:
            pass
else:
    bot.run(bot_token)

