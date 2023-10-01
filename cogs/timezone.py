import discord
import random
import pytz
import re
import json
import datetime

from discord.ext import commands
from pytz import country_timezones
from pytz import all_timezones

class timezones(commands.Cog, name='timezone+', description="timezone"):

    def __init__(self, client):
        self.client = client
        self.msgID = {}
        self.userID = {}

    #global variable #vary bad habbit of using it, but if it works, i'll take it
    #msgID = 0
    OT = 0
    HOUR = 0
    MINUTE = 0
    APM = ''
    #userID = 0

    #Events
    @commands.Cog.listener()
    async def on_ready(self): #must pass in self
        pass

    @commands.Cog.listener() #overall function that listens to events
    async def on_message(self,msg):
        #global variables that will need to pass on
        #global msgID
        global OT
        global HOUR
        global MINUTE
        global APM
        #global userID

        if msg.author == self.client.user: #This denies all the bot's own input
            return

        if re.search('^[^0-9]*((0?[1-9]|1[0-2]):?([0-5][0-9])? ?[AaPp][Mm])[^0-9]*$', msg.content):  #12hrs
            #print(re.search('^[^0-9]*((0?[1-9]|1[0-2]):?([0-5][0-9])? ?[AaPp][Mm])[^0-9]*$', msg.content).group(1))
            HOUR = re.search('^[^0-9]*((0?[1-9]|1[0-2])):?([0-5][0-9])? ?[AaPp][Mm][^0-9]*$', msg.content).group(1)
            MINUTE =re.search('^[^0-9]*(0?[1-9]|1[0-2]):?([0-5][0-9])? ?[AaPp][Mm][^0-9]*$', msg.content).group(2)
            APM = re.search('^[^0-9]*(0?[1-9]|1[0-2]):?([0-5][0-9])? ?([AaPp][Mm])[^0-9]*$', msg.content).group(3)

            if APM == 'PM' or APM == 'pm' or APM == 'Pm' or APM == 'pM':
                if HOUR != '12':
                    HOUR = int(HOUR) + 12
            if MINUTE == None:
                MINUTE = 0

            OT = re.search('^[^0-9]*((0?[1-9]|1[0-2]):?([0-5][0-9])? ?[AaPp][Mm])[^0-9]*$', msg.content).group(1)
            await msg.add_reaction("⏰")
            if self.msgID and msg.channel.id in self.msgID:
                oldMsg = await msg.channel.fetch_message(self.msgID[msg.channel.id])
                await oldMsg.remove_reaction("⏰", self.client.user)
            self.msgID.update({msg.channel.id: msg.id})
            self.userID.update({msg.channel.id: msg.author.id})
            #await msg.channel.send(re.search('^[^0-9]*((0?[1-9]|1[0-2]):?([0-5][0-9])? ?[AaPp][Mm])[^0-9]*$', msg.content).group(1))

        elif re.search('^[^0-9]*(0[0-9]|1[0-9]|2[0-3]):?[0-5][0-9][^0-9]*$', msg.content): #24hrs
            #print(re.search('^[^0-9]*((0[0-9]|1[0-9]|2[0-3]):?[0-5][0-9])[^0-9]*$', msg.content).group(1))
            HOUR = re.search('^[^0-9]*((0[0-9]|1[0-9]|2[0-3])):?[0-5][0-9][^0-9]*$', msg.content).group(1)
            MINUTE = re.search('^[^0-9]*(0[0-9]|1[0-9]|2[0-3]):?([0-5][0-9])[^0-9]*$', msg.content).group(2)

            OT = re.search('^[^0-9]*((0[0-9]|1[0-9]|2[0-3]):?[0-5][0-9])[^0-9]*$', msg.content).group(1)
            await msg.add_reaction("⏰")
            if self.msgID and msg.channel.id in self.msgID:
                oldMsg = await msg.channel.fetch_message(self.msgID[msg.channel.id])
                await oldMsg.remove_reaction("⏰", self.client.user)
            self.msgID.update({msg.channel.id: msg.id})
            self.userID.update({msg.channel.id: msg.author.id})
            #await msg.channel.send(re.search('^[^0-9]*((0[0-9]|1[0-9]|2[0-3]):?[0-5][0-9])[^0-9]*$', msg.content).group(1))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #embed for dm
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(user.guild.id)]

        DM_embed = discord.Embed(
           title = 'Timezone',
            description = 'Here is the time you requested',
            colour = self.client.MAINCOLOUR
        )
        #embed for message that hasn't have a timezone set
        sentTIME_embed = discord.Embed(
            title = 'Error',
            description = f"The user that sent the time doesn't have a region set up.\nPlease set it up with `{prefix}timezone <region>`\nA list of the regions can be found [here](https://intellipaat.com/community/5476/is-there-a-list-of-pytz-timezones)\n\ne.g. `{prefix}timezone Africa/Abidjan` \n\n*Refer to `{prefix}help timezone` for more information on the command*",
            colour = self.client.ERRORCOLOUR
        )
        #embed for checking DM
        checkDM_embed = discord.Embed(
            description = f'**{user}**, please check your private messages',
            colour = self.client.MAINCOLOUR
        )
        #check timezone for user Embed
        checkTZ_embed = discord.Embed(
            title = 'Error',
            description = f"**{user}**, you don't seem to have a region set up.\nPlease set it up with `{prefix}timezone <region>`\nA list of the regions can be found [here](https://intellipaat.com/community/5476/is-there-a-list-of-pytz-timezones)\n\ne.g. `{prefix}timezone Africa/Abidjan` \n\n*Refer to `{prefix}help timezone` for more information on the command*",
            colour = self.client.ERRORCOLOUR
        )
        checkTZ_embed.set_thumbnail(url = f'{user.avatar}')

        #global variables that needs to take
        #global msgID
        global OT
        global HOUR
        global MINUTE
        #global userID
        #global APM

        if user.bot == True: #if a bot reacted to it, it won't do anything
            return

        #i only want the "clock" emoji from the bot able to send message, not the clock emojis that any user can make
        try:
            if reaction.message.id == self.msgID[reaction.message.channel.id]: #matching id with the message

                if reaction.emoji == "⏰":
                    #get the message's user's id and find the timezone
                    with open('setZone.json','r') as file:
                        data = json.load(file)


                    valid = False
                    for person in data:
                        #await reaction.message.channel.send(person)
                        if str(user.id) == str(person):
                            error = False

                            try:
                                messageArea = data[str(self.userID[reaction.message.channel.id])] #get the message's user's timezone #aka original timezone
                                #print(messageArea)
                            except:
                                await reaction.message.channel.send(embed = sentTIME_embed, delete_after = 30)
                                error = True


                            userArea = data[str(user.id)] #get the area of the user #aka target timezone
                            #print(userArea)

                            #need to get today's date and put it into the equation
                            todate = datetime.date.today()

                            toyear = todate.year
                            today = todate.day
                            tomonth = todate.month

                            #do the convertion Here
                            originalTime = datetime.datetime(int(toyear),int(tomonth),int(today),int(HOUR), int(MINUTE))
                            #print(originalTime)
                            originalTZ = pytz.timezone(messageArea)
                            originalTZwithZone = originalTZ.localize(originalTime)
                            targetTZ = pytz.timezone(userArea)
                            targetTZwithZone = originalTZwithZone.astimezone(targetTZ)
                            #print(targetTZwithZone.strftime('%H:%M'))

                            #here i should also check is the user in the json file. true than run the procedure, false, then make them do it in a server?
                            DM_embed.add_field(name = f'Original Time: ({originalTZ})', value = OT, inline = "false")
                            DM_embed.add_field(name = f'Converted Time: ({targetTZ})', value = targetTZwithZone.strftime('%H:%M'), inline = "false")

                            if error == False:
                                await reaction.message.channel.send(embed = checkDM_embed, delete_after = 7)
                                await user.send(embed = DM_embed)

                            valid = True

                    if valid == False:
                        await reaction.message.channel.send(embed = checkTZ_embed)

                    #get the area from the message #aka original timezone
        except Exception as e:
            pass
        else:
            pass




    @commands.command()
    async def timezone(self, ctx, *, countryName):
        #embed for invalid input
        invalid_embed = discord.Embed(
           title = 'Invalid input',
           description = f"Ensure the format is `{ctx.prefix}timezone <region>` **(case sensitive)**.\nA list of the regions can be found [here](https://intellipaat.com/community/5476/is-there-a-list-of-pytz-timezones)\n\ne.g. `{ctx.prefix}timezone Africa/Abidjan` \n\n*Refer to `{ctx.prefix}help timezone` for more information on the command*",
           colour = self.client.ERRORCOLOUR
        )

        #embed for updating input
        updated_embed = discord.Embed(
            title = 'Updated',
            description = "You have updated your personal timezone",
            colour = self.client.MAINCOLOUR
        )

        #do a check is the input valid or not
        if countryName in all_timezones:
            with open('setZone.json','r') as file:
                timezones = json.load(file)
            timezones[str(ctx.author.id)] = countryName

            with open('setZone.json','w') as file:
                json.dump(timezones, file, indent = 4)

            #print("true")
            await ctx.send(embed = updated_embed, delete_after = 30)#, delete_after = 30

        else:
            await ctx.send(embed = invalid_embed, delete_after = 30)
            #print('false')

    #missing argument function
    @timezone.error
    async def timezone_error(self, ctx, error):
        #embed for the error message when missing an argument for the timezone
        error_embed = discord.Embed(
           title = 'Invalid input',
           description = f"Ensure the format is `{ctx.prefix}timezone <region>` **(case sensitive)**.\nA list of the regions can be found [here](https://intellipaat.com/community/5476/is-there-a-list-of-pytz-timezones)\n\ne.g. `{ctx.prefix}timezone Africa/Abidjan`\nThis command is to allow user to set a timezone for themselves in order to use the timezone features, which include converting time into other country, and to allow others to convert your time into their timezone. \n\n*Refer to `{ctx.prefix}help timezone` for more information on the command*",
           colour = self.client.ERRORCOLOUR
        )

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = error_embed)



async def setup(client):
    await client.add_cog(timezones(client)) #pass the class into it
