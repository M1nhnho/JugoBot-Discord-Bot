from datetime import datetime, timedelta
from random import choice
import apscheduler #pip install APScheduler
import asyncio
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import discord

numbers = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")

class Poll(commands.Cog, name ='poll+', description ='Make a poll for people in chat to react to. Has maximum 10 options and provides a summary after a set time'):
#Make a poll for people in chat to react to. The number of reactions is customizable up to a max of 10 and the duration of the poll can be set in the main command
	def __init__(self, client):
		self.client = client
		self.polls = []

	@commands.command(name="createpoll", aliases=["poll"])
	async def create_poll(self, ctx, seconds: int, question: str, *options):
		if len(options) > 10:
			await ctx.send("Max 10 options.")
		else:#create the poll
			embed = Embed(title="Poll", description=question, colour=self.client.MAINCOLOUR, timestamp=datetime.utcnow())
			fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False)]
			embed.set_footer(text ='React to cast a vote!')
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		message = await ctx.send(embed=embed)
		for emoji in numbers[:len(options)]:
			await message.add_reaction(emoji)
		self.polls.append((message.channel.id, message.id))

		await asyncio.sleep(seconds)
		#Get the message then count and sort the votes
		msg = await message.channel.fetch_message(message.id)
		votes = msg.reactions
		most_voted = max(votes, key=lambda r: r.count)
		votes.remove(most_voted)
		second_most_voted = max(votes, key=lambda r: r.count)
		#Send an embed with the results
		if most_voted.count != second_most_voted.count:

			win_embed = discord.Embed(title = 'Vote result', description = f'{most_voted.emoji} {options[numbers.index(most_voted.emoji)]}\n\u200b', colour = self.client.MAINCOLOUR)
			win_embed.set_footer(text=f'Question: {question}')
			await ctx.send(embed = win_embed)

		else:
			tie_embed = discord.Embed(title = 'Vote result', description = f'Its a tie!\n\u200b', colour = self.client.MAINCOLOUR)
			tie_embed.set_footer(text=f'Question: {question}')
			await ctx.send(embed = tie_embed)

		self.polls.remove((message.channel.id, message.id))

	@create_poll.error
	#standard error embed message triggered when an error occurs
	async def create_poll_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			error_embed = discord.Embed(title = 'Invalid input', description = f'Ensure the format is\n`{ctx.prefix}poll <time in seconds> <"question"> <option1> <option2>...` \n\neg. `{ctx.prefix}poll 5 "Do you like apples?" Yes No Maybe...` \n\n*Refer to `{ctx.prefix}help poll` for more information on the command*', colour = self.client.ERRORCOLOUR)
			await ctx.send(embed = error_embed)


	@commands.Cog.listener()
	#Check to see if a person has reacted more than once in the poll, if they have then it removes their previous reaction
	async def on_raw_reaction_add(self, payload):
		if payload.message_id in (poll [1] for poll in self.polls):
			message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)

			for reaction in message.reactions:
				if(not payload.member.bot and payload.member in await reaction.users().flatten() and reaction.emoji != payload.emoji.name):
					await message.remove_reaction(reaction.emoji, payload.member)


async def setup(client):
    await client.add_cog(Poll(client))
