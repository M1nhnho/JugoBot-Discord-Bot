import discord
from discord.ext import commands


class Clear(commands.Cog, name='clear+', description='clear [Amount]'):
    #access our client within our cog
    def __init__(self, client):
        self.client = client

#add command to cogs
    @commands.Cog.listener()
    async def on_ready(self):
        pass



####################################Clear/Purge
    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def Clear(self, ctx, amount:int):
        if amount <= 0:
            #await ctx.send(f'Please provide the amount of messages to be cleared')
            error_embed = discord.Embed(
                title = 'Error',
                description = f'Please ensure the <amount> value is higher than 0.\ne.g. `{ctx.prefix}clear 5`',
                colour = discord.Colour.purple())
            await ctx.send(embed = error_embed)
        else:
            await ctx.channel.purge(limit=amount+1)
            #await ctx.send(f'Amount of messages cleared: {amount}')
            clearembed = discord.Embed(title='', description= f'Amount of messages cleared: {amount}', colour=self.client.MAINCOLOUR)
            clearembed.set_footer(text=f'clear | This message will be cleared in 10 seconds')
            msg=await ctx.channel.send(embed=clearembed, delete_after = 10)

    @Clear.error
    async def Clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title = 'Invalid input',
                description = f'Ensure the format is `{ctx.prefix}clear <amount>`\ne.g `{ctx.prefix}clear 5` \n\n*Refer to `{ctx.prefix}help clear` for more information on the command* ',
                colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = error_embed)
        elif isinstance(error, commands.BadArgument):
            error_embed = discord.Embed(
                title = 'Invalid input',
                description = f'Please ensure the <amount> value is an integer.\ne.g `{ctx.prefix}clear 5` \n\n*Refer to `{ctx.prefix}help clear` for more information on the command*',
                colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = error_embed)

####################################End of Clear/Purge

async def setup(client):
    await client.add_cog(Clear(client))
