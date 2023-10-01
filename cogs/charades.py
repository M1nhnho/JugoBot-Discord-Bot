#This is the absolute base code for your cog template
#Copy this template into your cogs file, then duplicate it when u want to create new cog, make sure to rename ur file . easy.
import discord
import random
import asyncio
import os
import json
from discord.ext import commands

#Please name your .py file in lowercase #For example, <XXX.py> would be <xxx.py>
#Change <Template> to ur file name #For example, <template.py> would be <class Template(...)> #capital in first character
#Change <name here> to your cog name #For example, <name='name here'> would be <name='Template'> #capital in first character #DONT ADD THE CHARACTER '_' AFTER YOUR NAME unless if you dont want it to show up in help menu.
#Change <description here> to your call command without prefix. #For example, <%color> would be <color>
class Charades(commands.Cog, name='charades#', description='charades game that would send the user the word and other players have to guess that word'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass


####################################Your code
    @commands.command()
    async def charades(self,ctx):

        #Open the charades file and read all its info by each line
        filename = "charades.txt"
        with open(filename) as f:
            content = f.readlines()
            content = [x.strip() for x in content]#remove \n (lines)
        randomword = random.choice(content) #choose a random word from the charades file.
        #print(len(content)) #get the length of the overall words
        print("===============================")
        print(f"random word: {randomword}" ) #print in console

        countdown = 15 #count down for the game start timer
        #embed for start of game.
        embmsg=discord.Embed(
            title=f'Game invite',
            description=f'{ctx.author} is inviting people to a **charades** game!\n\nGame starts in **{countdown}**!',
            colour=self.client.MAINCOLOUR)
        embmsg.set_footer(text=f'React ✅ to play')
        embmsg.set_thumbnail(url = ctx.author.avatar)
        msg = await ctx.channel.send(embed=embmsg) #send the embed
        await msg.add_reaction('✅') #add the reaction

        #countdown
        while countdown > 0:
            await asyncio.sleep(1) #delay each countdown to 1 second.
            countdown -= 1 #take 1 away from download, so 20 -> 19
            #embed for start of game - DURING count down
            embmsg=discord.Embed(
                title=f'Game invite',
                description=f'{ctx.author} is inviting people to a **charades** game!\n\nGame starts in **{countdown}**!',
                colour=self.client.MAINCOLOUR)
            embmsg.set_footer(text=f'React ✅ to play')
            embmsg.set_thumbnail(url = ctx.author.avatar)
            await msg.edit(embed = embmsg)#edit the previous embed

        #get the list of players from the reaction. and remove robot from the reacted list.
        getmsg = await ctx.channel.fetch_message(msg.id)
        playersList = set()
        async for player in getmsg.reactions[0].users():
            if player != self.client.user: #Removes Jugo from playing
                playersList.add(player)
        if ctx.author not in playersList: #if the author of the command is not in player list. add the author in.
            playersList.add(ctx.author)

        #if length of player is not equals to 1 then send the word to the author so he could start describing.
        if len(playersList) != 1:
            embmsg=discord.Embed(title='charades', description=f'The word is: `{randomword}` \n\n \u200b', colour=self.client.MAINCOLOUR)
            embmsg.set_footer(text=f'Please describe this word to others that are playing without mentioning the word.')
            msg=await ctx.author.send(embed=embmsg)

            #embed for the started game to show the list of players. and the person describing and the amount of points they can get.
            embmsg=discord.Embed(
                title='Game started',
                description=f'You have 2 minutes to guess the word **{ctx.author}** is describing!', colour=self.client.MAINCOLOUR)

            if len(playersList) == 2:
                winnerPoints = 5
                loserPoints = -3
            elif len(playersList) == 3:
                winnerPoints = 6
                loserPoints = -2
            elif len(playersList) >= 4:
                winnerPoints = 7
                loserPoints = -1
            #ahhh niceee
            embmsg.add_field(name=f'List of players', value=f'{", ".join(str(player) for player in playersList if player != ctx.author)}\n\u200b',inline=False)
            embmsg.add_field(
                name=f'{len(playersList)} Player | Points system',
                value=f'Winner (if host) +3\nWinner (if player) {"{:+}".format(winnerPoints)}\nLosers {"{:+}".format(loserPoints)}',inline=False)
            embmsg.set_footer(text=f'charades')

            msg=await ctx.channel.send(embed=embmsg) #send the embed

            channel = ctx.channel #variable for ctx.channel
            def check(m): #check def
                #check to see if the message channel is the ctx.channel, check to see if the content and random word is lower case or message author and equal to ctx.author and random word is in content lowercase
                return m.channel == channel and (m.content.lower() == randomword or (m.author == ctx.author and randomword in m.content.lower()))
            try: #try to do these
                msg = await self.client.wait_for('message',timeout=120, check=check) #wait for guesser messages, and game would timeout after set amount of time.s
            except asyncio.TimeoutError: #When time expires
                challengeName='charades'
                embmsg=discord.Embed(description=f'The game "{challengeName}" has expired, no one was able to guess the word.')
                await ctx.channel.send(embed=embmsg)
            else: #when time is still running
                if msg.author != ctx.author: #if msg author is not the ctx.author(the person that started the game) then
                    #embed for the winner that guessed the correct word.
                    embmsg=discord.Embed(title=f'**{msg.author} wins!**', description=f'The correct answer was: **{randomword}**.', colour=self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = msg.author.avatar)
                    embmsg.set_footer(text=f'charades')
                    await ctx.channel.send(embed=embmsg)

                    #If the server has yet to play a game, create a folder for them in leaderboard
                    if not os.path.exists(os.path.join('./leaderboard', str(ctx.guild.id))):
                        os.mkdir(os.path.join('./leaderboard', str(ctx.guild.id)))
                    #Create variables of the paths for the all leaderboard and trivia leaderboard
                    allPath = os.path.join('./leaderboard', str(ctx.guild.id), 'all.json')
                    minigamePath = os.path.join('./leaderboard', str(ctx.guild.id), 'charades.json')

                    #Creating empty dictionaries of the leaderboards and if available, update with existing leaderboards
                    allDict = {}
                    minigameDict = {}
                    if os.path.exists(allPath):
                        with open(allPath, 'r') as file:
                            allDict = json.load(file)
                    if os.path.exists(minigamePath):
                        with open(minigamePath, 'r') as file:
                            minigameDict = json.load(file)

                    #Go through each player who played trivia and update their stats in the leaderboards
                    for player in playersList:
                        playerID = str(player.id)
                        noOfPlayers = len(playersList) - 1 #Minus the one who invoked the command
                        #Stats to add to the player's current stats
                        wins = 0
                        pointsWon = 0
                        losses = 0
                        pointsLost = 0

                        #First default the player's stats if new
                        if playerID not in allDict:
                            allDict.update({playerID: 0})
                        if playerID not in minigameDict:
                            minigameDict.update({playerID: {'plays': 0, 'wins': 0, 'pointsWon': 0, 'losses': 0, 'pointsLost': 0}})

                        #Check if the player won
                        if player == msg.author:
                            wins = 1
                            if noOfPlayers == 1:
                                pointsWon = 3
                            elif noOfPlayers == 2:
                                pointsWon = 5
                            elif noOfPlayers == 3:
                                pointsWon = 6
                            elif noOfPlayers >= 4:
                                pointsWon = 7
                        #Check if the player is the one who invoked the command
                        elif player == ctx.author:
                            wins = 1
                            pointsWon = 3
                        else:
                            losses = 1
                            if noOfPlayers == 2:
                                pointsLost = -3
                            elif noOfPlayers == 3:
                                pointsLost = -2
                            elif noOfPlayers >= 4:
                                pointsLost = -1

                        #Update the player's stats
                        allDict.update({playerID: allDict[playerID] + pointsWon + pointsLost})
                        minigameDict.update({playerID: {'plays': minigameDict[playerID]['plays'] + 1,
                                                        'wins': minigameDict[playerID]['wins'] + wins,
                                                        'pointsWon': minigameDict[playerID]['pointsWon'] + pointsWon,
                                                        'losses': minigameDict[playerID]['losses'] + losses,
                                                        'pointsLost': minigameDict[playerID]['pointsLost'] + pointsLost}})

                    #Store the updated leaderboards
                    with open(allPath, 'w') as file:
                        json.dump(allDict, file)
                    with open(minigamePath, 'w') as file:
                        json.dump(minigameDict, file)

                else: #or else the ctx.author (person that started the game) mentioned the word that he was supposed to describe then the end games and print this command.
                    embmsg=discord.Embed(title=f'**Nobody wins!**', description=f'**{ctx.author}** cheated. \nThe correct answer was: **{randomword}**.', colour=self.client.MAINCOLOUR)
                    embmsg.set_footer(text=f'charades')
                    msg=await ctx.channel.send(embed=embmsg)


        else: #or else the time expires.
            challengeName='charades'
            embmsg=discord.Embed(description=f'The game "{challengeName}" has expired, not enough players joined. ', colour= self.client.EXPIREDCOLOUR)
            await ctx.channel.send(embed=embmsg)

    @charades.error
    #Either displays an error message embed (for missing <list>) or raises an error
    async def charades_error(self, ctx, error):
        #Missing <list> argument
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the format is `{ctx.prefix}trivia play <list>`.\n\ne.g. `{ctx.prefix}trivia play whosthatpokemon`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        else:
            print(error)
            raise error






####################################End of code


async def setup(client):
    await client.add_cog(Charades(client)) #Change <Template>into ur class name
