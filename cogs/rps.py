import discord
from discord.ext import commands
import random
from random import randint
import os
import json
import asyncio

class Rps(commands.Cog, name ='rps#', description ='Rock Paper scissors against the bot!'):
#A rock paper scissors game against the bot. Playrs react with their choice and the bot shows the result based on it.
    def __init__(self, client):
        self.client = client

    @commands.command()
    #send an embed displaying the players' options
    async def rps(self, ctx):
        choices=['🗻', '📃', '✂']
        embedmsg = discord.Embed(title = f'Rock paper scissors vs {self.client.user}!', description='\nGame expires in 15 seconds if no one reacts to this embed.', colour = self.client.MAINCOLOUR)
        embedmsg.add_field(
            name = f'1 Player | Points system',
            value = f'Winner +5\nLoser -3',
            inline = False)
        embedmsg.set_footer(text = 'React with rock, paper or scissors')
        msg = await ctx.send(embed = embedmsg)
        await msg.add_reaction('🗻')
        await msg.add_reaction('📃')
        await msg.add_reaction('✂')

        #randomise the bot choice
        botChoice = choices[randint(0, 2)]

        def check(reaction, user):
        #If nobody reacts after a set time then the game timeouts otherwise a set of if statements are used to display the result depending on the users' choice.
            return user != self.client.user and (str(reaction.emoji) == '🗻' or str(reaction.emoji) == '📃' or str(reaction.emoji) == '✂') and reaction.message == msg

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 15.0, check = check)
        except asyncio.TimeoutError:
            embedmsg = discord.Embed(description = 'The rock paper scissors challenge has expired.')
            await ctx.channel.send(embed = embedmsg)
        else:
            #If the server has yet to play a game, create a folder for them in leaderboard
            if not os.path.exists(os.path.join('./leaderboard', str(ctx.guild.id))):
                os.mkdir(os.path.join('./leaderboard', str(ctx.guild.id)))
            #Create variables of the paths for the all leaderboard and trivia leaderboard
            allPath = os.path.join('./leaderboard', str(ctx.guild.id), 'all.json')
            minigamePath = os.path.join('./leaderboard', str(ctx.guild.id), 'rps.json')

            #Creating empty dictionaries of the leaderboards and if available, update with existing leaderboards
            allDict = {}
            minigameDict = {}
            if os.path.exists(allPath):
                with open(allPath, 'r') as file:
                    allDict = json.load(file)
            if os.path.exists(minigamePath):
                with open(minigamePath, 'r') as file:
                    minigameDict = json.load(file)

            playerID = str(user.id)
            wins = 0
            pointsWon = 0
            losses = 0
            pointsLost = 0

            if playerID not in allDict:
                allDict.update({playerID: 0})
            if playerID not in minigameDict:
                minigameDict.update({playerID: {'plays': 0, 'wins': 0, 'pointsWon': 0, 'losses': 0, 'pointsLost': 0}})

            #--- Checks who won ---
            #Draw
            if reaction.emoji == botChoice:
                embedmsg = discord.Embed(title = 'DRAW!', description = f'{self.client.user}: {botChoice}\n{user}: {reaction.emoji}', colour = self.client.MAINCOLOUR)
                embedmsg.set_footer(text = 'rps')
                await ctx.send(embed = embedmsg)


            elif reaction.emoji == '🗻':
                if botChoice == '📃':
                    losses = 1
                    pointsLost = -3

                    embmsg = discord.Embed(title = f'{self.client.user} wins!', description = f'{self.client.user}: {botChoice}\n{user}: {reaction.emoji}', colour = self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = self.client.user.avatar)
                    embmsg.set_footer(text = f'rps')
                    await ctx.channel.send(embed = embmsg)

                else:
                    wins = 1
                    pointsWon = 5

                    embmsg = discord.Embed(title = f'{user} wins!', description=f'{user}: {reaction.emoji}\n {self.client.user}: {botChoice}', colour = self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = user.avatar)
                    embmsg.set_footer(text = f'rps')
                    await ctx.channel.send(embed = embmsg)

            elif reaction.emoji == '📃':
                if botChoice == '✂':
                    losses = 1
                    pointsLost = -3

                    embmsg = discord.Embed(title = f'{self.client.user} wins!', description = f'{self.client.user}: {botChoice}\n{user}: {reaction.emoji}', colour = self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = self.client.user.avatar)
                    embmsg.set_footer(text = f'rps')
                    await ctx.channel.send(embed = embmsg)
                else:
                    wins = 1
                    pointsWon = 5

                    embmsg = discord.Embed(title = f'{user} wins!', description=f'{user}: {reaction.emoji}\n {self.client.user}: {botChoice}', colour = self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = user.avatar)
                    embmsg.set_footer(text = f'rps')
                    await ctx.channel.send(embed = embmsg)

            elif reaction.emoji == '✂':
                if botChoice == '🗻':
                    losses = 1
                    pointsLost = -3

                    embmsg = discord.Embed(title = f'{self.client.user} wins!', description = f'{self.client.user}: {botChoice}\n{user}: {reaction.emoji}', colour = self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = self.client.user.avatar)
                    embmsg.set_footer(text = f'rps')
                    await ctx.channel.send(embed = embmsg)
                else:
                    wins = 1
                    pointsWon = 5

                    embmsg = discord.Embed(title = f'{user} wins!', description=f'{user}: {reaction.emoji}\n {self.client.user}: {botChoice}', colour = self.client.MAINCOLOUR)
                    embmsg.set_thumbnail(url = user.avatar)
                    embmsg.set_footer(text = f'rps')
                    await ctx.channel.send(embed = embmsg)

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


async def setup(client):
    await client.add_cog(Rps(client))
