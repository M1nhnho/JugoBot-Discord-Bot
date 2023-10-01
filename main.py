#change status
import discord
import asyncio
import os
import json
from discord.ext.commands import MissingPermissions
from datetime import datetime
from discord.ext import commands

####use ctx.xxx to use these info from other cogs
####################################Custom prefix - determines what prefix i use
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]
####################################End of Custom prefix
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = get_prefix, intents = intents) #command prefix
client.remove_command('help')
TOKEN = '' #Jugo Bot =====================================TOKEN HERE========================================= IF YOURE SEEING THIS FROM GITHUB AND DOWNLOADING THIS FROM GITHUB, PLEASE INSERT ANY BOT TOKEN HERE

#Main colours the bot use
client.MAINCOLOUR = discord.Colour.purple()
client.ERRORCOLOUR = discord.Colour.red()
client.EXPIREDCOLOUR = discord.Colour.default()

#Variables for date time
now = datetime.now()
current_time = now.strftime("%X %x")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Ping me for server prefix'))#change status
    print('====================================')
    print(' Bot is online!')
    print(" Startup time:", current_time)
    print('====================================')

#ANY bot errors, would show this but also if the user dont have permission to do certain commands, itll also show this.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"{ctx.author} You don't have permission to use this command")
    else:
        raise error
        print("=============================================================================================")
        print('error, you can undo the # comment to see the error')
        pass


############################## WHEN USER @ THE BOT IN CHANNEL CHAT IT WOULD SHOW THE USER THE SERVER PREFIX
@client.event
async def on_message(message):
    try:
        if message.mentions[0] == client.user:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefix = prefixes[str(message.guild.id)]

            await message.channel.send(f'This server\'s prefix is `{prefix}`')

    except:
        pass

    await client.process_commands(message)
#############################


####################################Custom prefix -Start prefix (default prefix)
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        prefixes[str(guild.id)] = 'j.' #cast the guild id in the string

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        prefixes.pop(str(guild.id)) #pop the guild id #remove a piece

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4) #add it back in


@client.command(aliases=['prefix'])
@commands.has_permissions(administrator=True)
async def prefixChange(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix #= prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
    embmsg = discord.Embed(tile='prefix changed', description=f'Server prefix has been changed to `{prefix}`', colour = client.MAINCOLOUR)
    await ctx.channel.send(embed = embmsg)

@prefixChange.error
async def prefixChange_error(ctx, error): #Prefix change error, when the user didnt put in the prefix they want to change into
    if isinstance(error, commands.MissingRequiredArgument):
        error_embed = discord.Embed(title = 'Invalid input', description = f'Ensure the format is `{ctx.prefix}prefix <prefix>`', colour = client.ERRORCOLOUR)
        await ctx.send(embed = error_embed)

####################################End of Custom prefix



#list of ids
liang_id=250342826527686658
tien_id=168723540839759872
hamzah_id=244015754591207426
daisy_id=240918281249095680
####################################COG
#load command
@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == liang_id or ctx.message.author.id == tien_id or ctx.message.author.id == hamzah_id or ctx.message.author.id == daisy_id:#check to see the sender is the jugo bot owners
        client.load_extension(f'cogs.{extension}') #!THIS IS BASED ON THE FILENAME
        embmsg=discord.Embed(tile='load cog' , description=f'The function "{extension}" has been loaded',colour=client.MAINCOLOUR)
        embmsg.set_footer(text=f'Server time: {current_time}')
        await ctx.channel.send(embed=embmsg)


#unload command
@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == liang_id or ctx.message.author.id == tien_id or ctx.message.author.id == hamzah_id or ctx.message.author.id == daisy_id: #check to see the sender is the jugo bot owners
        client.unload_extension(f'cogs.{extension}') #!THIS IS BASED ON THE FILENAME
        embmsg=discord.Embed(tile='unload cog' , description=f'The function "{extension}" has been unloaded',colour=client.MAINCOLOUR)
        embmsg.set_footer(text=f'Server time: {current_time}')
        await ctx.channel.send(embed=embmsg)


#reload cogs
@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == liang_id or ctx.message.author.id == tien_id or ctx.message.author.id == hamzah_id or ctx.message.author.id == daisy_id:#check to see the sender is the jugo bot owners
        client.unload_extension(f'cogs.{extension}')#!THIS IS BASED ON THE FILENAME
        client.load_extension(f'cogs.{extension}')#!THIS IS BASED ON THE FILENAME
        embmsg=discord.Embed(tile='reload cog' , description=f'The function "{extension}" has been reloaded',colour=client.MAINCOLOUR)
        embmsg.set_footer(text=f'Server time: {current_time}')
        await ctx.channel.send(embed=embmsg)


@client.command()
async def reloadAll(ctx):
    if ctx.message.author.id == liang_id or ctx.message.author.id == tien_id or ctx.message.author.id == hamzah_id or ctx.message.author.id == daisy_id:#check to see the sender is the jugo bot owners
        try:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}') #take away the last 3 characters
                    client.load_extension(f'cogs.{filename[:-3]}') #take away the last 3 characters
                    print(f'{filename[:-3]} COG is reloaded')
        except Exception as e:
            #await ctx.channel.send(f'please load the cog "{filename[:-3]}" first before reloading all')
            await ctx.channel.send(f'Please load the cog "{filename[:-3]}" first before reloading all', colour = client.ERRORCOLOUR)
            pass
        else:
            embmsg=discord.Embed(tile='Reloaded Cogs' , description=f'**All Cogs have been reloaded**\n\n',colour=client.MAINCOLOUR)
            embmsg.set_footer(text=f'Server time: {current_time}')
            await ctx.channel.send(embed=embmsg)
            print('All good')

            print('====================================')
            print(' Server has been reloaded!')
            print(" Startup time:", current_time)
            print('====================================')
    else:
        pass






#load every cog on start
async def start_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}') #take away the last 3 characters
            print(f'▶ "{filename[:-3]}" cog is ready')
        else:
            print(f'✖ Non-python found: "{filename[:-3]}"')

async def main():
    async with client:
        await start_cogs()
        await client.start(TOKEN) #bot token

asyncio.run(main())