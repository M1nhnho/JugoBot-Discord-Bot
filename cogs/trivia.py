import discord
import random
import asyncio
import os
import json
import shutil
from discord.ext import commands


class Trivia(commands.Cog, name = 'trivia#'): #'#' means 'Games' category
    #Allows users to play trivia
    #Has multiple subcommands (8 in total): lists, copy, play, stop, add, delete, download, settings
    #Ones of note is `add` which works by a user sending in a text file of the trivia list
    #And `copy` to get ready-made trivia lists from Jugo (copies from the main server folder to their server folder)
    def __init__(self, client):
        self.client = client
        self.stopped = {} #Used to make sure only one game per channel is on at a time
        #If there isn't a trivia folder, create one automatically
        if not os.path.exists('./trivia'):
            os.mkdir('./trivia')


    @commands.group(invoke_without_command = True, aliases = ['tri'])
    #Displays the trivia subcommands
    async def trivia(self, ctx):
        aliases = ', '.join(commands.Bot.get_command(self.client, 'trivia').aliases) #Gets the aliases, in this case: 'tri'
        #Embeds for each page
        page1Embed = discord.Embed(title = '__Page 1 | Trivia Subcommands__', colour = self.client.MAINCOLOUR)
        page1Embed.add_field(name = f'{ctx.prefix}trivia lists', value = 'Displays all the trivia lists in this server.\n\u200b', inline = False)
        page1Embed.add_field(name = f'{ctx.prefix}trivia copy <list>', value = f'Lets you copy over a ready-made trivia list from **{self.client.user}**\'s collection.\nCall this command without <list> to see this collection.\n\u200b', inline = False)
        page1Embed.add_field(name = f'{ctx.prefix}trivia play <list>', value = 'Plays an existing trivia list.\n\u200b', inline = False)
        page1Embed.add_field(name = f'{ctx.prefix}trivia stop', value = f'Stops the current trivia game in play (in this channel).', inline = False)
        page1Embed.set_footer(text = f'Aliases: {aliases}')

        page2Embed = discord.Embed(title = '__Page 2 | Trivia Subcommands__', colour = self.client.MAINCOLOUR)
        page2Embed.add_field(name = f'{ctx.prefix}trivia add <list>', value = 'Lets you add your own trivia list.\nCall this command without <list> to get the instructions.\n\u200b', inline = False)
        page2Embed.add_field(name = f'{ctx.prefix}trivia delete <list>', value = 'Deletes an existing trivia list.\n\u200b', inline = False)
        page2Embed.add_field(name = f'{ctx.prefix}trivia download/dl <list>', value = 'Uploads an existing trivia list for the user to download.\n\u200b', inline = False)
        page2Embed.add_field(name = f'{ctx.prefix}trivia settings', value = 'Displays the current settings, which can be modified.', inline = False)
        page2Embed.set_footer(text = f'Aliases: {aliases}')

        #Organises pages into a list, allows for easy access for each page
        pageNo = 0
        pagesEmbed = [page1Embed, page2Embed]
        helpMsg = await ctx.send(embed = pagesEmbed[pageNo])
        await helpMsg.add_reaction('◀')
        await helpMsg.add_reaction('▶')

        def check(reaction, user):
            return str(reaction.emoji) in ['◀', '▶'] and not user.bot and reaction.message == helpMsg #Checks reaction added is left/right arrow, isn't from a bot, and is from the same message

        #Move onto the next or previous page based on the reaction (gives the user 60s to react, timer resets when they do react)
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 60, check = check)
            except asyncio.TimeoutError:
                break
            else:
                if str(reaction.emoji) == '◀' and pageNo > 0:
                    pageNo -= 1
                elif str(reaction.emoji) == '▶' and pageNo < 1:
                    pageNo += 1
                await helpMsg.edit(embed = pagesEmbed[pageNo]) #Updates message embed to correct page
                await helpMsg.remove_reaction(reaction, user) #Removes the user's reaction for convenience (so they don't need to remove and add again)

    @trivia.command()
    #Displays the trivia lists currently stored in their server folder (if empty, refers them to add/copy)
    async def lists(self, ctx):
        #Checks if the server folder exists, if so, get the trivia lists
        listsPath = os.path.join('./trivia', str(ctx.guild.id))
        if os.path.exists(listsPath):
            listsList = []
            for filename in os.listdir(listsPath):
                if filename.endswith('.txt'):
                    listsList.append(filename[:-4])
            #Checks if the server folder contains any trivia lists, if so, display them
            if listsList:
                msgEmbed = discord.Embed(title = '__Trivia Lists__', description = f'{", ".join(sorted(listsList))}', colour = self.client.MAINCOLOUR)
                msgEmbed.set_footer(text = f'{ctx.guild}', icon_url = ctx.guild.icon)
                await ctx.send(embed = msgEmbed)
                return

        #If it ends up not returning, there is no trivia lists, then refer user to add/copy
        errorEmbed = discord.Embed(title = 'Error', colour = self.client.ERRORCOLOUR)
        errorEmbed.add_field(
            name = 'There are no trivia lists',
            value = f"To get started, use `{ctx.prefix}trivia copy` to see existing trivia lists from **{self.client.user}**'s collection.\nThen use `{ctx.prefix}trivia copy <list>` to copy it over to this server.\n\nAlternatively, refer to `{ctx.prefix}trivia add` for instructions if you'd rather make and add your own trivia list.")
        await ctx.send(embed = errorEmbed)

    @trivia.command()
    #Allows the user to copy over a trivia list from Jugo's collection (the main server) to their server
    #Without the <list> argument, will instead display what trivia lists there is in Jugo's collection (in the main server)
    async def copy(self, ctx, list = None):
        MAINID = '818428122113245204' #Main server ID
        #If no <list> argument, then display collection
        if not list:
            #Same layout as the above `lists` command but for the main server - will repeat comments for convenience
            #Checks if the server folder exists, if so, get the trivia lists
            listsPath = os.path.join('./trivia', MAINID)
            if os.path.exists(listsPath):
                listsList = []
                for filename in os.listdir(listsPath):
                    if filename.endswith('.txt'):
                        listsList.append(filename[:-4])
                #Checks if the server folder contains any trivia lists, if so, display them
                if listsList:
                    msgEmbed = discord.Embed(title = '__Trivia Lists__', description = f'{", ".join(sorted(listsList))}', colour = self.client.MAINCOLOUR)
                    msgEmbed.set_footer(text = f'{self.client.user}', icon_url = self.client.user.avatar)
                    await ctx.send(embed = msgEmbed)
                    return
            #If it ends up not returning, there is no trivia lists (in this case, there should be trivia lists)
            await ctx.send('The collection appears to be empty...')

        #Otherwise there's a <list> argument, so copy that trivia list over if possible
        else:
            #If the server doesn't have any custom trivia lists, create a folder for them to store the lists
            serverPath = os.path.join('./trivia', str(ctx.guild.id))
            if not os.path.exists(serverPath):
                os.mkdir(serverPath)

            #Copy the trivia list from the main server folder to their server folder (if the trivia list exists)
            sourcePath = os.path.join('./trivia', MAINID, f'{list}.txt')
            destinationPath = os.path.join('./trivia', str(ctx.guild.id), f'{list}.txt')
            if os.path.exists(sourcePath):
                shutil.copy(sourcePath, destinationPath)
                await ctx.send(f'**{list}.txt** has been copied to this server.')
            else:
                await ctx.send(f'**{list}.txt** does not exist in {self.client.user}\'s collection.')

    @trivia.command()
    #Starts a trivia game using the questions, images, answers from the provided <list>
    async def play(self, ctx, list):
        #Creates an stop check for the channel if there isn't one already
        if ctx.channel.id not in self.stopped:
            self.stopped.update({ctx.channel.id: True})
        if self.stopped[ctx.channel.id]: #Ensures that only one trivia game per channel can be played
            list = list.lower()
            listPath = os.path.join('./trivia', str(ctx.guild.id), f'{list}.txt')
            if os.path.exists(listPath): #Checks if the trivia list exists, get the game ready if so
                with open(listPath, 'r') as file:
                    #--------------------
                    #----- Settings -----
                    #--------------------
                    #Grabs the settings from stored json for the server, otherwise use default
                    settingsPath = os.path.join('./trivia', str(ctx.guild.id), 'settings.json')
                    if os.path.exists(settingsPath):
                        with open(settingsPath, 'r') as settingsFile:
                            settingsDict = json.load(settingsFile)
                    else:
                        settingsDict = {
                                        'corrects': 3,
                                        'time': 15
                                        }

                    #----------------------------------------------------
                    #----- Retrieving questions, images and answers -----
                    #----------------------------------------------------
                    channel = ctx.channel
                    contents = file.readlines()
                    questions = []
                    errorQuestions = []
                    images = []
                    answers = []
                    tempAnswers = []

                    questionNo = 0
                    winner = None

                    #Goes through each line in the text file, checking which ones are either question, image or answer
                    for line in contents:
                        #If question, then update all lists so that each index match up to the same question, image and answer
                        if line.startswith('Q:'):
                            if questions: #This updates the images + answers with the previous question, so don't update on the first question as there's no previous question and no images + answers yet
                                #So if the question doesn't come with an image, append None to allow algorithm to know to not add an image when question appears
                                if len(images) != len(questions):
                                    images.append(None)
                                #Only append if there is a set of answers - allows for error checking that there are missing sets of answers
                                if tempAnswers:
                                    answers.append(tempAnswers)
                                    tempAnswers = []
                                else:
                                    errorQuestions.append(questions[-1]) #If no answer, then add question for the error embed below (no need to update answer)
                            questions.append(line[2:].rstrip('\n'))
                        elif line.startswith('I:'):
                            if len(images) != len(questions): #Ensures a limit of one image per question
                                images.append(line[2:].rstrip('\n'))
                        elif line.startswith('A:'):
                            tempAnswers.append(line[2:].rstrip('\n'))
                    #As the previous images + answers get updated on each new question, the final images + answers still need to get updated
                    if len(images) != len(questions):
                        images.append(None)
                    if tempAnswers:
                        answers.append(tempAnswers)
                    else:
                        errorQuestions.append(questions[-1])

                #If there were missing answers, then tell user these questions need answers
                if errorQuestions:
                    errorQs = '\n▸'.join(errorQuestions)
                    errorEmbed = discord.Embed(
                        title = 'Error',
                        description = f'These questions are missing at least one answer each:\n▸{errorQs}\n\nPlease re-add the updated **{list}.txt** with the missing answers.\nUse `{ctx.prefix}trivia download {list}`, if needed, to get the text file.',
                        colour = self.client.ERRORCOLOUR)
                    await ctx.send(embed = errorEmbed)
                    return #End here as the trivia game will not work correctly as the answers are now misaligned with the wrong questions

                #---------------------------
                #----- Game invitation -----
                #---------------------------
                self.stopped[channel.id] = False #No issues with the trivia list, trivia game is ready to play
                countdown = 15 #How long users have to react to join
                msgEmbed = discord.Embed(
                    title = 'Game invite',
                    description = f'{ctx.author} is inviting people to a **trivia** game!\n▸Playing **{list}** ({len(questions)} questions)\n▸First to **{settingsDict["corrects"]}** correct answers\n▸**{settingsDict["time"]}** seconds on each question.\n\nGame starts in **{countdown}**!',
                    colour = self.client.MAINCOLOUR)
                msgEmbed.set_footer(text = 'React ✅ to play')
                msgEmbed.set_thumbnail(url = ctx.author.avatar)
                msg = await ctx.channel.send(embed = msgEmbed)
                await msg.add_reaction('✅')

                #As it counts down, updates the invitation message embed to reflect the current countdown
                while countdown > 0:
                    await asyncio.sleep(1)
                    if not self.stopped[channel.id]:
                        countdown -= 1
                        #Embed is repeated so the countdown is updated
                        msgEmbed = discord.Embed(
                            title = 'Game invite',
                            description = f'{ctx.author} is inviting people to a **trivia** game!\n▸Playing **{list}** ({len(questions)} questions)\n▸First to **{settingsDict["corrects"]}** correct answers\n▸**{settingsDict["time"]}** seconds on each question.\n\nGame starts in **{countdown}**!',
                            colour = self.client.MAINCOLOUR)
                        msgEmbed.set_footer(text = 'React ✅ to play')
                        msgEmbed.set_thumbnail(url = ctx.author.avatar)
                        await msg.edit(embed = msgEmbed)
                    #If a user decides to stop the game, update to reflect the trivia game is now cancelled
                    else:
                        cancelledEmbed = discord.Embed(
                            title = f'Game invite',
                            description = f'{ctx.author} is inviting people to a **trivia** game!\n▸Playing **{list}** ({len(questions)} questions)\n▸First to **{settingsDict["corrects"]}** correct answers\n▸**{settingsDict["time"]}** seconds on each question\n\nGame **cancelled**.',
                            colour = self.client.MAINCOLOUR)
                        cancelledEmbed.set_footer(text = 'React ✅ to play')
                        cancelledEmbed.set_thumbnail(url = ctx.author.avatar)
                        await msg.edit(embed = cancelledEmbed)
                        return #Ends trivia game

                #Countdowns over, find the users who have reacted and assign them as players (automatically includes the invoker)
                msgFetched = await ctx.channel.fetch_message(msg.id) #Fetches the message to get the correct current reactions
                playersList = set()
                async for player in msgFetched.reactions[0].users():
                    if player != self.client.user: #Removes Jugo from playing
                        playersList.add(player)
                if ctx.author not in playersList:
                    playersList.add(ctx.author)
                noOfPlayers = len(playersList)

                #-----------------------
                #----- Game start! -----
                #-----------------------
                msgEmbed = discord.Embed(
                    title = 'Game started',
                    description = f'Playing **{list}!** ({len(questions)} questions)\nFirst to **{settingsDict["corrects"]}** correct answers.\n**{settingsDict["time"]}** seconds on each question.',
                    colour = self.client.MAINCOLOUR)
                #Displays the point distribution based on number of players
                if noOfPlayers == 1:
                    winnerPoints = 0
                    loserPoints = 0
                elif noOfPlayers == 2:
                    winnerPoints = 5
                    loserPoints = -3
                elif noOfPlayers == 3:
                    winnerPoints = 6
                    loserPoints = -2
                elif noOfPlayers >= 4:
                    winnerPoints = 7
                    loserPoints = -1
                msgEmbed.add_field(name = f'List of players', value = f'{", ".join(str(player) for player in playersList)}\n\u200b', inline = False)
                msgEmbed.add_field(
                    name = f'{noOfPlayers} Player | Points system',
                    value = f'Winner {"{:+}".format(winnerPoints)}\nLosers {"{:+}".format(loserPoints)}',
                    inline = False)
                msgEmbed.set_footer(text = 'trivia')
                await ctx.channel.send(embed=msgEmbed)

                #Defaults everyone's scores to 0 as no one has any correct answers yet
                scores = {}
                for player in playersList:
                    scores.update({player: 0})
                #Continues the game until there is a winner
                while not winner:
                    questionNo += 1
                    #If the game is stopped early, then this will return an embed containing the current scores to be displayed
                    def endGame():
                        sortedScores = dict(sorted(scores.items(), key = lambda item: item[1], reverse = True))
                        titles = 'Player        | Corrects      \n-----------------------------------\n'
                        stoppedScores = '\n'.join('{:<14}'.format(str(player)[:14]) + '| ' + '{:<8}'.format(str(score)) for player, score in sortedScores.items())
                        stoppedScores = titles + stoppedScores
                        #Using 'asciidoc' for blue headings
                        msgEmbed = discord.Embed(title = f'__Scores__', description = f'```asciidoc\n{stoppedScores}```', colour = self.client.EXPIREDCOLOUR)
                        msgEmbed.set_footer(text = f'trivia | {list} | {settingsDict["corrects"]} corrects, {settingsDict["time"]} seconds')
                        return msgEmbed

                    #Puts a delay between question and answer to allow people time to see what the correct answers are and/or who got it correct
                    #Checks each second if the trivia game has been stopped - done this way as if outside a loop, there could be a small 3 second delay on ending the trivia game
                    for _ in range(3):
                        if self.stopped[channel.id]:
                            await ctx.send(embed = endGame())
                            return
                        await asyncio.sleep(1)

                    #Displays a random question
                    qna = random.randint(0, len(questions) - 1)
                    msgEmbed = discord.Embed(title = f'Question {questionNo}', description = f'{questions[qna]}', colour = self.client.MAINCOLOUR)
                    msgEmbed.set_footer(text = f'{list} | {settingsDict["corrects"]} corrects, {settingsDict["time"]} seconds')
                    if images[qna]:
                        msgEmbed.set_image(url = images[qna])

                    #Trys to send the embed but if an error occurs (notably with the image URL) then tell user it needs fixing
                    #Would be preferable if it focused on the HTTPException
                    try:
                        await ctx.send(embed = msgEmbed)
                    except:
                        self.stopped[channel.id] = True
                        errorEmbed = discord.Embed(
                           title = 'Error',
                           description = f'There is an issue with this URL:\n▸{images[qna]}\n\nPlease re-add the updated **{list}.txt** with a working URL.\nUse `{ctx.prefix}trivia download {list}`, if needed, to get the text file.',
                           colour = self.client.ERRORCOLOUR)
                        await ctx.send(embed = errorEmbed)
                        return

                    #Checks:
                    #If message is the correct answer (case INsensitive)
                    #And if same channel (so a player can't guess in another channel from where the trivia game is taking place)
                    #And if it is a player (so a user that joined (reacted) during the invitation) - this is to allow for others to chat without becoming a player and risk losing points
                    #Or if the trivia game has been stopped, ignoring the above conditions
                    def check(m):
                        return (m.content.lower() in [ans.lower() for ans in answers[qna]] and m.channel == channel and m.author in playersList) or self.stopped[channel.id]

                    try:
                        msg = await self.client.wait_for('message', timeout = settingsDict['time'], check = check)
                    except asyncio.TimeoutError:
                        if self.stopped[channel.id]:
                            await ctx.send(embed = endGame())
                            return
                        #Time ran out, display all the possible correct answers
                        correctAnswers = '\n'.join(answers[qna])
                        msgEmbed = discord.Embed(title = 'No one got it...', colour = self.client.MAINCOLOUR)
                        msgEmbed.add_field(name = f'Correct answers (case __in__sensitive)', value = f'{correctAnswers}')
                        msgEmbed.set_footer(text = f'{list} | {questions[qna]}')
                        await ctx.send(embed = msgEmbed)
                    else:
                        if self.stopped[channel.id]:
                            await ctx.send(embed = endGame())
                            return
                        #Displays who got it right, what their answer is, and how many correct answers they've got so far
                        scores.update({msg.author: scores[msg.author] + 1})
                        msgEmbed = discord.Embed(description = f'**{msg.content}** is correct!', colour = self.client.MAINCOLOUR)
                        msgEmbed.set_author(name = f'{msg.author}', icon_url = msg.author.avatar)
                        msgEmbed.set_footer(text = f'{scores[msg.author]} corrects so far')
                        await ctx.send(embed = msgEmbed)

                        #Check if the last correct answer results in a win
                        if scores[msg.author] == settingsDict['corrects']: #If default settings, then the winner is whoever gets 3 correct answers first
                            winner = msg.author

                #----------------------------------------------
                #----- Game results (update leaderboards) -----
                #----------------------------------------------
                self.stopped[channel.id] = True #Game has finished, so is currently 'stopped' - users can now play a new trivia game (in the same channel)
                #Display who won along with their opponents (and their scores) and what trivia list + settings were in play
                msgEmbed = discord.Embed(title = f'{winner} won!',
                                         description = f'vs. {", ".join(str(player) + " **(" + str(score) + ")**" for player, score in scores.items() if player != winner)}',
                                         colour = self.client.MAINCOLOUR)
                msgEmbed.set_footer(text = f'trivia | {list} | {settingsDict["corrects"]} corrects, {settingsDict["time"]} seconds')
                msgEmbed.set_thumbnail(url = winner.avatar)
                await ctx.send(embed = msgEmbed)

                #If the server has yet to play a trivia game, create a folder for them in leaderboard
                if not os.path.exists(os.path.join('./leaderboard', str(ctx.guild.id))):
                    os.mkdir(os.path.join('./leaderboard', str(ctx.guild.id)))
                allPath = os.path.join('./leaderboard', str(ctx.guild.id), 'all.json')
                minigamePath = os.path.join('./leaderboard', str(ctx.guild.id), 'trivia.json')

                #Creating empty dictionaries of the leaderboards and if available, update with existing leaderboards
                allDict = {}
                minigameDict = {}
                if os.path.exists(allPath):
                    with open(allPath, 'r') as file:
                        allDict = json.load(file)
                if os.path.exists(minigamePath):
                    with open(minigamePath, 'r') as file:
                        minigameDict = json.load(file)

                #Go through each player and update their stats in the leaderboards
                for player in scores:
                    playerID = str(player.id) #Unsure as to why but the json files stored the ID as strings rather than integers
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

                    if player == winner:
                        wins = 1
                        #Checks how many players were playing - determines their point gain
                        if noOfPlayers > 1: #You can't gain points playing solo, but will still update your play count
                            if noOfPlayers == 2:
                                pointsWon = 5
                            elif noOfPlayers == 3:
                                pointsWon = 6
                            else:
                                pointsWon = 7
                    else:
                        losses = 1
                        #Checks how many players were playing - determines their point loss
                        if noOfPlayers > 1: #You can't lose points playing solo, but will still update your play count
                            if noOfPlayers == 2:
                                pointsLost = -3
                            elif noOfPlayers == 3:
                                pointsLost = -2
                            else:
                                pointsLost = -1

                    #Updates the player's stats
                    allDict.update({playerID: allDict[playerID] + pointsWon + pointsLost})
                    minigameDict.update({playerID: {'plays': minigameDict[playerID]['plays'] + 1,
                                                    'wins': minigameDict[playerID]['wins'] + wins,
                                                    'pointsWon': minigameDict[playerID]['pointsWon'] + pointsWon,
                                                    'losses': minigameDict[playerID]['losses'] + losses,
                                                    'pointsLost': minigameDict[playerID]['pointsLost'] + pointsLost}})

                #Stores the updated leaderboards
                with open(allPath, 'w') as file:
                    json.dump(allDict, file)
                with open(minigamePath, 'w') as file:
                    json.dump(minigameDict, file)
            else:
                await ctx.send(f'**{list}.txt** does not exist.')
        else:
            await ctx.send('There is already a trivia game in play (in this channel)!')

    @play.error
    #Either displays an error message embed (for missing <list>) or raises an error
    async def play_error(self, ctx, error):
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

    @trivia.command()
    #Stops the trivia game in play in the same channel this is invoked in (if there is a trivia game in play)
    async def stop(self, ctx):
        #First checks if there is a stop check for the channel (if not, then there hasn't been any trivia games)
        #Then if there is a trivia game in play, once both passes, then end trivia game
        if ctx.channel.id in self.stopped and not self.stopped[ctx.channel.id]:
            self.stopped[ctx.channel.id] = True
            msgEmbed = discord.Embed(description = 'The game "trivia" has forcibly expired.', colour = self.client.EXPIREDCOLOUR)
            await ctx.send(embed = msgEmbed)
        else:
            await ctx.send('There is no trivia game in play (in this channel).')

    @trivia.command()
    #Allows the user to send their own trivia list as a text file and saves it to be played
    #Without the <list> argument, will instead display the instructions
    async def add(self, ctx, list = None):
        #If no <list> argument, then display instructions
        if not list:
            msgEmbed = discord.Embed(
                title = '__Instructions__',
                description = f'You will be asked to send a text file, ensure it is of this format:\n```<heading>\nQ:<question>\nI:<image URL>\nA:<answer1>\nA:<answer2>\netc.```\n▸Replace <???> with your own (arrows are not needed)\n▸Headings are optional (you are free to organise as you wish, including empty lines, as only lines starting with **Q:**/**I:**/**A:** are considered)\n▸Image URLs are optional (limit of one per question)\n▸You can have as many answers as you like\n\nFor text file examples,\nuse `{ctx.prefix}trivia copy <list>` then `{ctx.prefix}trivia download <list>`\nto check out **mhw** and **paimon**.\n\n*Note: The <list> value must not contain any spaces and will overwrite if there is another with the same name.*\n\u200b',
                colour = self.client.MAINCOLOUR)
            msgEmbed.add_field(name = 'Command Syntax', value = f'{ctx.prefix}trivia add <list>', inline = True)
            msgEmbed.add_field(name = 'Example', value = f'{ctx.prefix}trivia add whosthatpokemon', inline = True)
            await ctx.send(embed = msgEmbed)

        #Otherwise there's a <list> argument, so add that trivia list if possible
        else:
            #If the server doesn't have any custom trivia lists, create a folder for them to store the lists
            listPath = os.path.join('./trivia', str(ctx.guild.id))
            if not os.path.exists(listPath):
                os.mkdir(listPath)

            try:
                await ctx.send('Send the text file now.')
                channel = ctx.channel

                #Checks that the message is from the same channel as the invoker
                def check(m):
                    return m.channel == channel

                #Gets the next message with the text file (the trivia list) and saves it to the server folder (provided there is a text file)
                list = list.lower()
                msg = await self.client.wait_for('message', check = check)
                if msg.attachments[0].filename.endswith('.txt'):
                    await msg.attachments[0].save(os.path.join(listPath, f'{list}.txt'))
                    await ctx.send(f'**{list}.txt** has been saved.')
                else:
                    await ctx.send('Incorrect file type - looking for a text file.')
            except:
                await ctx.send('I could not find a text file.')

    @trivia.command()
    #Checks if the trivia list exists, delete if so
    async def delete(self, ctx, list):
        list = list.lower()
        listPath = os.path.join('./trivia', str(ctx.guild.id), f'{list}.txt')
        if os.path.exists(listPath):
            os.remove(listPath)
            await ctx.send(f'**{list}.txt** has been deleted from this server.')
        else:
            await ctx.send(f'**{list}.txt** does not exist in this server.')

    @delete.error
    #Either displays an error message embed (for missing <list>) or raises an error
    async def delete_error(self, ctx, error):
        #Missing <list> argument
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the format is `{ctx.prefix}trivia delete <list>`.\n\ne.g. `{ctx.prefix}trivia delete whosthatpokemon`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        else:
            raise error

    @trivia.command(aliases = ['dl'])
    #Sends the text file of the trivia list to the user for them to download
    async def download(self, ctx, list):
        list = list.lower()
        listPath = os.path.join('./trivia', str(ctx.guild.id), f'{list}.txt')
        if os.path.exists(listPath):
            await ctx.send(file = discord.File(listPath))
        else:
            await ctx.send(f'**{list}.txt** does not exist in this server.')

    @download.error
    #Either displays an error message embed (for missing <list>) or raises an error
    async def download_error(self, ctx, error):
        #Missing <list> argument
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the format is `{ctx.prefix}trivia download <list>`.\n\ne.g. `{ctx.prefix}trivia download whosthatpokemon`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        else:
            raise error

    @trivia.group(invoke_without_command = True, aliases = ['set'])
    #Displays the current settings of the server (along with how to change them)
    async def settings(self, ctx):
        #Grabs the settings from stored json for the server, otherwise use default
        settingsPath = os.path.join('./trivia', str(ctx.guild.id), 'settings.json')
        if os.path.exists(settingsPath):
            with open(settingsPath, 'r') as file:
                settingsDict = json.load(file)
        else:
            settingsDict = {
                            'corrects': 3,
                            'time': 15
                            }

        aliases = ', '.join(commands.Bot.get_command(self.client, 'trivia settings').aliases) #Gets the aliases, in this case: 'set'
        msgEmbed = discord.Embed(title = '__Trivia Settings__', colour = self.client.MAINCOLOUR)
        msgEmbed.add_field(name = f'Current Settings', value = f'Correct answers to win: **{settingsDict["corrects"]}**\nTime per question: **{settingsDict["time"]} seconds**', inline = False)
        msgEmbed.add_field(name = f'{ctx.prefix}trivia settings corrects <amount>', value = 'Change the number of correct answers needed to win.', inline = False)
        msgEmbed.add_field(name = f'{ctx.prefix}trivia settings time <amount>', value = 'Change the time (seconds) allowed to answer per question.', inline = False)
        msgEmbed.set_footer(text = f'Aliases: {aliases}')
        await ctx.send(embed = msgEmbed)

    @settings.command()
    #Allows the user to update the number of correct answers needed to win
    async def corrects(self, ctx, amount:int):
        #Checks <amount> is higher than 0 as trivia games will continue on for eternity as it'll never hit a negative number or 0
        if amount > 0:
            #Grabs the settings from stored json for the server, otherwise use default
            settingsPath = os.path.join('./trivia', str(ctx.guild.id), 'settings.json')
            if os.path.exists(settingsPath):
                with open(settingsPath, 'r') as file:
                    settingsDict = json.load(file)
            else:
                settingsDict = {
                                'corrects': 3,
                                'time': 15
                                }

            #Updates the settings with the new corrects and stores it
            await ctx.send(f'Correct answers to win: **{settingsDict["corrects"]} -> {amount}**')
            settingsDict['corrects'] = amount
            with open(settingsPath, 'w') as file:
                json.dump(settingsDict, file)
        else:
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Please ensure the <amount> value is higher than 0.\n\ne.g. `{ctx.prefix}trivia settings time 15`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)

    @corrects.error
    #Either displays an error message embed (for missing <amount> or <amount> is not an integer) or raises an error
    async def corrects_error(self, ctx, error):
        #Missing <amount> argument
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the format is `{ctx.prefix}trivia settings corrects <amount>`.\n\ne.g. `{ctx.prefix}trivia settings corrects 5`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        #<amount> value is not an integer
        elif isinstance(error, commands.BadArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Please ensure the <amount> value is an integer.\n\ne.g. `{ctx.prefix}trivia settings corrects 5`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        else:
            raise error

    @settings.command()
    #Allows the user to update the time (in seconds) allowed per question
    async def time(self, ctx, amount:int):
        #Checks <amount> is higher than 0 as time can't be negative and in the case of 0, it will spam questions and answers giving no time for guesses
        if amount > 0:
            #Grabs the settings from stored json for the server, otherwise use default
            settingsPath = os.path.join('./trivia', str(ctx.guild.id), 'settings.json')
            if os.path.exists(settingsPath):
                with open(settingsPath, 'r') as file:
                    settingsDict = json.load(file)
            else:
                settingsDict = {
                                'corrects': 3,
                                'time': 15
                                }

            #Updates the settings with the new time and stores it
            await ctx.send(f'Time per question: **{settingsDict["time"]}s -> {amount}s**')
            settingsDict['time'] = amount
            with open(settingsPath, 'w') as file:
                json.dump(settingsDict, file)
        else:
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Please ensure the <amount> value is higher than 0.\n\ne.g. `{ctx.prefix}trivia settings time 20`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)

    @time.error
    #Either displays an error message embed (for missing <amount> or <amount> is not an integer) or raises an error
    async def time_error(self, ctx, error):
        #Missing <amount> argument
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Ensure the format is `{ctx.prefix}trivia settings time <amount>`.\n\ne.g. `{ctx.prefix}trivia settings time 15`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        #<amount> value is not an integer
        elif isinstance(error, commands.BadArgument):
            errorEmbed = discord.Embed(
               title = 'Invalid input',
               description = f"Please ensure the <amount> value is an integer.\n\ne.g. `{ctx.prefix}trivia settings time 15`",
               colour = self.client.ERRORCOLOUR)
            await ctx.send(embed = errorEmbed)
        else:
            raise error


async def setup(client):
    await client.add_cog(Trivia(client))
