import discord
import random
import asyncio
import os
import json
from discord.ext import commands


class Dice(commands.Cog, name='dice#', description='2 player dice game that rolls a dice for both players'):
    #access our client within our cog
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

####################################Embedded dice
    @commands.command(aliases=['dice', 'Dice'])
    async def eDice(self,ctx,erNumMin:int, erNumMax:int):
        try: #if command is entered, try these.
            enumMin = 0 #set the min number for the dice
            if erNumMin > enumMin and erNumMax > erNumMin: #if statement to check to see if the given min number is the bigger than the set min number and check to see if the max number is bigger than the min number

                erNumber1 = random.randint(erNumMin,erNumMax) #create random number between the min number and max number
                #print embed
                embmsg=discord.Embed(description=f'Dice rolled: **{erNumber1}**, between {erNumMin} & {erNumMax}. \nGame expires in 15 seconds if no one reacts to this embed.', colour=self.client.MAINCOLOUR)
                embmsg.set_footer(text=f'React ✅ to play against {ctx.author} \nReact ❎ to cancel the game')
                embmsg.add_field(
                    name = f'2 Player | Points system',
                    value = f'Winner +5\nLoser -3',
                    inline = False)
                embmsg.set_author(name = ctx.author, icon_url = ctx.author.avatar)
                msg=await ctx.channel.send(embed=embmsg)
                #add the reactions
                await msg.add_reaction('✅')
                await msg.add_reaction('❎')

                def check(reaction, user): #check
                    #check to see if the user is not a robot. and what they clicked in the tick or the x reaction from the embed and check to see if user is not the ctx.author(person that started the game, this prevents players playing themselves)
                    return user!=self.client.user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎') and reaction.message == msg and user!=ctx.author

                try:#Try to wait for user input with a timeout(expire)
                    reaction, user= await self.client.wait_for('reaction_add', timeout=15.0, check=check)
                except asyncio.TimeoutError: #When time expires
                    challengeName='Dice Game'
                    embmsg=discord.Embed(description=f'The "{challengeName}" challenge has expired.')
                    msg=await ctx.channel.send(embed=embmsg)
                else: #When user clicks on the tick reaction and goes through.
                    if reaction.emoji=='✅':
                        erNumber2 = random.randint(erNumMin,erNumMax)

                        #If the server has yet to play a game, create a folder for them in leaderboard
                        if not os.path.exists(os.path.join('./leaderboard', str(ctx.guild.id))):
                            os.mkdir(os.path.join('./leaderboard', str(ctx.guild.id)))
                        #Create variables of the paths for the all leaderboard and trivia leaderboard
                        allPath = os.path.join('./leaderboard', str(ctx.guild.id), 'all.json')
                        minigamePath = os.path.join('./leaderboard', str(ctx.guild.id), 'dice.json')

                        #Creating empty dictionaries of the leaderboards and if available, update with existing leaderboards
                        allDict = {}
                        minigameDict = {}
                        if os.path.exists(allPath):
                            with open(allPath, 'r') as file:
                                allDict = json.load(file)
                        if os.path.exists(minigamePath):
                            with open(minigamePath, 'r') as file:
                                minigameDict = json.load(file)

                        player1ID = str(ctx.author.id)
                        wins1 = 0
                        pointsWon1 = 0
                        losses1 = 0
                        pointsLost1 = 0

                        player2ID = str(user.id)
                        wins2 = 0
                        pointsWon2 = 0
                        losses2 = 0
                        pointsLost2 = 0

                        if player1ID not in allDict:
                            allDict.update({player1ID: 0})
                        if player1ID not in minigameDict:
                            minigameDict.update({player1ID: {'plays': 0, 'wins': 0, 'pointsWon': 0, 'losses': 0, 'pointsLost': 0}})

                        if player2ID not in allDict:
                            allDict.update({player2ID: 0})
                        if player2ID not in minigameDict:
                            minigameDict.update({player2ID: {'plays': 0, 'wins': 0, 'pointsWon': 0, 'losses': 0, 'pointsLost': 0}})

                        ##Decides which player has won
                        if erNumber1 > erNumber2:
                            #if the ctx.author wins
                            embmsg=discord.Embed(title= f'**{ctx.author} wins!**', description=f'{ctx.author} rolled: **{erNumber1}**\n{user} rolled: **{erNumber2}**\n', colour=self.client.MAINCOLOUR)
                            embmsg.set_thumbnail(url = ctx.author.avatar)
                            embmsg.set_footer(text=f'dice')
                            msg=await ctx.channel.send(embed=embmsg)

                            #add points
                            wins1 = 1
                            pointsWon1 = 5
                            losses2 = 1
                            pointsLost2 = -3

                        elif erNumber1 == erNumber2: #if its a draw

                            embmsg=discord.Embed(title= '**DRAW!**',description=f'both players rolled: {erNumber2}', colour=self.client.MAINCOLOUR)
                            msg=await ctx.channel.send(embed=embmsg)

                        else: #else if the user wins
                            embmsg=discord.Embed(title= f'**{user} wins!**',description=f'{ctx.author} rolled: **{erNumber1}**\n{user} rolled: **{erNumber2}**\n', colour=self.client.MAINCOLOUR)
                            embmsg.set_thumbnail(url = user.avatar)
                            embmsg.set_footer(text=f'dice')
                            msg=await ctx.channel.send(embed=embmsg)
                            #add points
                            wins2 = 1
                            pointsWon2 = 5
                            losses1 = 1
                            pointsLost1 = -3

                        #Update player 1's stats
                        allDict.update({player1ID: allDict[player1ID] + pointsWon1 + pointsLost1})
                        minigameDict.update({player1ID: {'plays': minigameDict[player1ID]['plays'] + 1,
                                                         'wins': minigameDict[player1ID]['wins'] + wins1,
                                                         'pointsWon': minigameDict[player1ID]['pointsWon'] + pointsWon1,
                                                         'losses': minigameDict[player1ID]['losses'] + losses1,
                                                         'pointsLost': minigameDict[player1ID]['pointsLost'] + pointsLost1}})

                        #Update player 2's stats
                        if (player1ID != player2ID):
                            allDict.update({player2ID: allDict[player2ID] + pointsWon2 + pointsLost2})
                            minigameDict.update({player2ID: {'plays': minigameDict[player2ID]['plays'] + 1,
                                                             'wins': minigameDict[player2ID]['wins'] + wins2,
                                                             'pointsWon': minigameDict[player2ID]['pointsWon'] + pointsWon2,
                                                             'losses': minigameDict[player2ID]['losses'] + losses2,
                                                             'pointsLost': minigameDict[player2ID]['pointsLost'] + pointsLost2}})

                        #Store the updated leaderboards
                        with open(allPath, 'w') as file:
                            json.dump(allDict, file)
                        with open(minigamePath, 'w') as file:
                            json.dump(minigameDict, file)

                    elif reaction.emoji=='❎': #when user clicks on the x reaction, itll cancel the game
                        challengeName='Dice Game'
                        embmsg=discord.Embed(description=f'The "{challengeName}" challenge has been cancelled.', colour = self.client.EXPIREDCOLOUR)
                        msg=await ctx.channel.send(embed=embmsg)

            else: #show error when the min is lower than 0
                error_embed = discord.Embed(
                    title = 'Error',
                    description = f'Please ensure the <min> value is higher than 0 and is lower than the <max> value.\ne.g. `{ctx.prefix}dice 1 100` \n\n*Refer to `{ctx.prefix}help dice` for more information on the command*',
                    colour = self.client.ERRORCOLOUR)
                await ctx.send(embed = error_embed)


        except Exception as e:
            pass
        else:
            pass

    #error
    @eDice.error
    async def eDice_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): #checks to see if missing argument !dice
            error_embed = discord.Embed(
                title = 'Invalid input',
                description = f'Ensure the format is `{ctx.prefix}dice <min> <max>`\ne.g `{ctx.prefix}dice 1 100` \n\n*Refer to `{ctx.prefix}help dice` for more information on the command*',
                colour = self.client.ERRORCOLOUR)

            await ctx.send(embed = error_embed)
        elif isinstance(error, commands.BadArgument): #checks to see if argument is typed in correctly. e.g only integers
            error_embed = discord.Embed(
                title = 'Invalid input',
                description = f'Please ensure the <min> and <max> values are integers.\ne.g `{ctx.prefix}dice 1 100` \n\n*Refer to `{ctx.prefix}help dice` for more information on the command*',
                colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = error_embed)


####################################Embedded dice END

async def setup(client):
    await client.add_cog(Dice(client))
