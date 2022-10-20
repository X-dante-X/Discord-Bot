import discord
from discord.ext import commands
from discord.utils import get
import csv
import config


intents = discord.Intents.all()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents=intents)

@bot.event
async def on_ready():
    print("Ready!")

    




            




@bot.event    
async def on_member_join(member):
    welcome = bot.get_channel(config.WELCOME_CHANNEL) 
    with open(config.CSV_EXP,'r', newline='') as expfile:
        reader = csv.DictReader(expfile, delimiter=";")
        for row in reader:
            if int(row['id'])==member.id:
                embed=discord.Embed(title="С возращением", description=f"{member.mention}", color=0xDC143C)
                embed.set_image(url="https://cdn.discordapp.com/attachments/751072033709752410/890944676188807198/cbef6804c67b8a34.jpg")
                await welcome.send(embed=embed)
                role = get(member.guild.roles, id=int(row['role']))
                await member.add_roles(role)
                return 0
        else:
            with open(config.CSV_EXP,'a', newline='') as wexpfile:
                writer = csv.writer(wexpfile, delimiter=";")
                writer.writerow([member.id,0,config.ROLES['1']])
            embed=discord.Embed(title="Стал ганстером", description=f"{member.mention} становится частью семьи", color=0xDC143C)
            embed.set_image(url="https://cdn.discordapp.com/attachments/751072033709752410/890944676188807198/cbef6804c67b8a34.jpg")
            await welcome.send(embed=embed)
            role = get(member.guild.roles, id=config.ROLES['1'])
            await member.add_roles(role)    


@bot.event    
async def on_member_remove(member):
    welcome = bot.get_channel(config.WELCOME_CHANNEL) 
    embed=discord.Embed(title="Пока", description=f"{member.mention}!", color=0xDC143C) 
    await welcome.send(embed=embed)    
    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def exp(ctx):
    with open(config.CSV_EXP,'r', newline='') as expfile:
        reader = csv.DictReader(expfile, delimiter=";")
        for row in reader:
            if int(row['id'])==int(ctx.message.author.id):
                x='твой опыт: '+ row["exp"]
                await ctx.send(x)

bot.run(config.TOKEN)
