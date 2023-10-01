#This is the absolute base code for your cog template
#Copy this template into your cogs file, then duplicate it when u want to create new cog, make sure to rename ur file . easy.
import discord
from discord.ext import commands

#Please name your .py file in lowercase #For example, <XXX.py> would be <xxx.py>
#Change <Template> to ur file name #For example, <template.py> would be <class Template(...)> #capital in first character
#Change <name here> to your cog name #For example, <name='name here'> would be <name='Template'> #capital in first character #DONT ADD THE CHARACTER '_' AFTER YOUR NAME unless if you dont want it to show up in help menu.
#Change <description here> to your call command without prefix. #For example, <%color> would be <color>
class Template(commands.Cog, name='name here_', description='description here'):

    def __init__(self, client):
        self.client = client

####################################Your code






####################################End of code


async def setup(client):
    await client.add_cog(Template(client)) #Change <Template>into ur class name
