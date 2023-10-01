import discord
import asyncio
import os
import json
from discord.ext import commands


class Leaderboard(commands.Cog, name = 'leaderboard+'): #'+' means 'Utilities' category
    #All minigames (when played with >=2 players except rps as the bot is included as an additional player instead) allows users to gain/lose points
    #These points currently don't have a use and is just a way of showing who's the best at the minigames
    def __init__(self, client):
        self.client = client
        self.minigamesList = ['dice', 'charades', 'rps', 'trivia'] #Current list of minigames - 4 as of now
        #If there isn't a leaderboard folder, create one automatically
        if not os.path.exists('./leaderboard'):
            os.mkdir('./leaderboard')


    @commands.group(invoke_without_command = True, aliases = ['lb'])
    #Displays the leaderboard for the <minigame> - displays the top 10 players sorted by number of players (also shows wins(points gained) and losses(points lost))
    #Without the <minigame> argument, will instead display the subcommands
    async def leaderboard(self, ctx, minigame = None):
        #If no <minigame> argument, then display subcommands
        if not minigame:
            aliases = ', '.join(commands.Bot.get_command(self.client, 'leaderboard').aliases)
            msgEmbed = discord.Embed(title = '__Leaderboard Subcommands__', colour = self.client.MAINCOLOUR)
            msgEmbed.add_field(name = f'{ctx.prefix}leaderboard all', value = 'Displays the top 10 players overall sorted by points.\n\u200b', inline = False)
            msgEmbed.add_field(name = f'{ctx.prefix}leaderboard <minigame>', value = 'Displays the top 10 players in <minigame> sorted by number of plays.\n\u200b', inline = False)
            msgEmbed.add_field(
                name = f'{ctx.prefix}leaderboard wipe all/<minigame>',
                value = f'Wipes all the leaderboards or just the <minigame> leaderboard (the points will be corrected to reflect this wipe).\n\n*Please refer to `{ctx.prefix}help` to see what minigames there are.*',
                inline = False)
            msgEmbed.set_footer(text = f'Aliases: {aliases}')
            await ctx.send(embed = msgEmbed)

        #Otherwise there's a <minigame> argument, so display the relevant leaderboard (if there is one)
        elif minigame.lower() in self.minigamesList: #Checks if it's an existing minigame
            #Checks if there is a json file stored for this server for the relevant minigame leaderboard, if so then display
            minigame = minigame.lower()
            minigamePath = os.path.join('./leaderboard', str(ctx.guild.id), f'{minigame}.json')
            if os.path.exists(minigamePath):
                with open(minigamePath, 'r') as file:
                    minigameDict = json.load(file)
                #Sorts the players by their number of plays and shows top 10
                sortedMinigameDict = dict(sorted(minigameDict.items(), key = lambda item: item[1]['plays'], reverse = True)[:10])

                #Puts the players into an organised leaderboard table ensuring the column widths are fixed
                minigameLeaderboard = 'Player         | Plays    | Wins     | Losses        \n--------------------------------------------------------'
                for player, stats in sortedMinigameDict.items():
                    user = await self.client.fetch_user(int(player))
                    winsPoints = '{:<8}'.format(str(stats['wins']) + '(' + '{:+}'.format(stats['pointsWon']) + ')')
                    lossesPoints = '{:<8}'.format(str(stats['losses']) + '(' + '{:+}'.format(stats['pointsLost']) + ')')
                    minigameLeaderboard += f'\n{"{:<14}".format(str(user)[:14])} | {"{:<8}".format(str(stats["plays"]))} | {winsPoints} | {lossesPoints}'

                #Uses 'asciidoc' for blue headings
                msgEmbed = discord.Embed(title = f'__{minigame.upper()} | Top 10__', description = f'```asciidoc\n{minigameLeaderboard}```', colour = self.client.MAINCOLOUR)
                authorID = str(ctx.author.id)
                #Displays the stats of the invoker related to the minigame in the footer
                if authorID in minigameDict:
                    msgEmbed.set_footer(text = f'You have played {minigameDict[authorID]["plays"]} games with {minigameDict[authorID]["wins"]}({"{:+}".format(minigameDict[authorID]["pointsWon"])}) wins and {minigameDict[authorID]["losses"]}({"{:+}".format(minigameDict[authorID]["pointsLost"])}) losses', icon_url = ctx.author.avatar)
                else:
                    msgEmbed.set_footer(text = f'You have not played {minigame}', icon_url = ctx.author.avatar)
                await ctx.send(embed = msgEmbed)
            else:
                await ctx.send(f'No **{minigame}** games have been played yet.')

        #If the <minigame> value isn't one of the current four existing minigames, then display error message embed
        else:
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the <minigame> value is spelt correctly and is an existing minigame.\nPlease refer to `{ctx.prefix}help` to see what minigames there are.\n\ne.g. `{ctx.prefix}leaderboard trivia`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)

    @leaderboard.command()
    #Displays the overall leaderboard of all minigames - displays the top 10 players sorted by points
    async def all(self, ctx):
        #Checks if there is a json file stored for this server for the overall leaderboard, if so then display
        allPath = os.path.join('./leaderboard', str(ctx.guild.id), 'all.json')
        if os.path.exists(allPath):
            with open(allPath, 'r') as file:
                allDict = json.load(file)
            #Sorts the players by their points and shows top 10
            sortedAllDict = dict(sorted(allDict.items(), key = lambda item: item[1], reverse = True)[:10])

            #Puts the players into an organised leaderboard table ensuring the column widths are fixed
            allLeaderboard = 'Player         | Points   \n-------------------------------'
            for player, points in sortedAllDict.items():
                user = await self.client.fetch_user(int(player))
                allLeaderboard += f'\n{"{:<14}".format(str(user)[:14])} | {"{:<8}".format(str(points))}'

            #Uses 'asciidoc' for blue headings
            msgEmbed = discord.Embed(title = '__ALL | Top 10__', description = f'```asciidoc\n{allLeaderboard}```', colour = self.client.MAINCOLOUR)
            authorID = str(ctx.author.id)
            #Displays the points of the invoker in the footer
            if authorID in allDict:
                msgEmbed.set_footer(text = f'You have {allDict[authorID]} points', icon_url = ctx.author.avatar)
            else:
                msgEmbed.set_footer(text = "You haven't played any minigames", icon_url = ctx.author.avatar)
            await ctx.send(embed = msgEmbed)
        else:
            await ctx.send(f'No minigames have been played yet.')

    @leaderboard.command()
    @commands.has_permissions(manage_guild = True) #Ensures only higher-ups can wipe leaderboards
    #Wipes the relevant leaderboard (by deleting json files and updating points if need be)
    async def wipe(self, ctx, minigame):
        #Checks <minigame> is 'all', if so, then wipe all leaderboards (if possible)
        minigame = minigame.lower()
        if minigame == 'all':
            #First double checks with user
            msgEmbed = discord.Embed(
               title = 'Are you sure?',
               description = 'This will wipe **all** leaderboards, effectively resetting back to when this server hadn\'t played any minigames yet.\n\n**This is irreversible**',
               colour = self.client.MAINCOLOUR)
            msgEmbed.set_footer(text = 'React ✅ to accept\nReact ❎ to decline')
            msg = await ctx.send(embed = msgEmbed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❎')

            def check(reaction, user):
                return str(reaction.emoji) in ['✅', '❎'] and user == ctx.author and reaction.message == msg #Checks reaction added is tick/cross, is from the invoker, and is from the same message

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 15, check = check)
            except asyncio.TimeoutError:
                await ctx.send('The wipe has been automatically declined due to no response.')
            else:
                #If they end up accepting the wipe then go through each leaderboard and delete the json file (provided there is one)
                if str(reaction.emoji) == '✅':
                    for lb in ['all'] + self.minigamesList:
                        leaderboardPath = os.path.join('./leaderboard', str(ctx.guild.id), f'{lb}.json')
                        if os.path.exists(leaderboardPath):
                            os.remove(leaderboardPath)
                    await ctx.send('**All** leaderboards have been wiped.')
                elif str(reaction.emoji) == '❎':
                    await ctx.send('The wipe has been declined.')

        #Checks <minigame> is one of the four current minigames, if so, then wipe relevant leaderboard and update points (if possible)
        elif minigame in self.minigamesList:
            #First double checks with user
            msgEmbed = discord.Embed(
               title = 'Are you sure?',
               description = f'This will wipe the **{minigame}** leaderboard, effectively resetting back to when this server hadn\'t played any **{minigame}** games yet.\nThis will correct any points gained/lost from **{minigame}** in the overall leaderboard to reflect the wipe.\n\n**This is irreversible**',
               colour = self.client.MAINCOLOUR)
            msgEmbed.set_footer(text = 'React ✅ to accept\nReact ❎ to decline')
            msg = await ctx.send(embed = msgEmbed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❎')

            def check(reaction, user):
                return str(reaction.emoji) in ['✅', '❎'] and user == ctx.author and reaction.message == msg #Checks reaction added is tick/cross, is from the invoker, and is from the same message

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 15, check = check)
            except asyncio.TimeoutError:
                await ctx.send('The wipe has been automatically declined due to no response.')
            else:
                #If they end up accepting the wipe then correct the points and delete the relevant json file
                if str(reaction.emoji) == '✅':
                    minigamePath = os.path.join('./leaderboard', str(ctx.guild.id), f'{minigame}.json')
                    #Checks if there is a minigame leaderboard, if so, then correct points then delete json file
                    if os.path.exists(minigamePath):
                        allPath = os.path.join('./leaderboard', str(ctx.guild.id), 'all.json')
                        pointsUpdate = {}

                        #Gets the current leaderboards for the purpose of correcting the points before deleting
                        with open(allPath, 'r') as file:
                            allDict = json.load(file)
                        with open(minigamePath, 'r') as file:
                            minigameDict = json.load(file)

                        #Goes through the minigame leaderboard, fetching each players' points overall gain/loss, then corrects it in the overall leaderboard
                        for player, stats in minigameDict.items():
                            pointsUpdate.update({player: stats['pointsWon'] + stats['pointsLost']})
                        for player, points in pointsUpdate.items():
                            allDict.update({player: allDict[player] - points})

                        #Saves the overall leaderboard with the corrected points and deletes the json file of the minigame leaderboard
                        with open(allPath, 'w') as file:
                            json.dump(allDict, file)
                        os.remove(minigamePath)
                        await ctx.send(f'The **{minigame}** leaderboard has been wiped.')
                    else:
                        await ctx.send(f'No **{minigame}** games have been played yet so there is no **{minigame}** leaderboard.')
                elif str(reaction.emoji) == '❎':
                    await ctx.send('The wipe has been declined.')
        else:
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure 'all' or the <minigame> value is spelt correctly and is an existing minigame.\nPlease refer to `{ctx.prefix}help` to see what minigames there are.\n\ne.g. `{ctx.prefix}leaderboard trivia`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)

    @wipe.error
    #Either displays an error message embed (for missing <minigame> or missing permissions) or raises an error
    async def wipe_error(self, ctx, error):
        #Missing <minigame> argument
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the format is `{ctx.prefix}leaderboard wipe all/<minigame>`.\n\ne.g. `{ctx.prefix}leaderboard wipe all`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        #Missing permissions (manage server)
        elif isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(
               title = 'Missing permissions',
               description = f'Ensure you have permissions to **manage the server**.',
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        else:
            raise error


async def setup(client):
    await client.add_cog(Leaderboard(client))
