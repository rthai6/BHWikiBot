import re
import scrape
import discord
from builtins import str
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
familiardic = None
fusiondic = None
mythicdic = None

@bot.event
async def on_ready():
    global familiardic
    global fusiondic
    global mythicdic
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Scraping...')
    familiardic = scrape.scrapefamiliar()
    fusiondic = scrape.scrapefusion()
    mythicdic = scrape.scrapemythic()
    print('Ready')
    
@bot.command()
async def familiar(ctx, *args):
    global familiardic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        familiar = familiardic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        embed = discord.Embed(title=familiar['name'], description=familiar['rarity']+"\n"+familiar['location'], color=0xeee657)
        embed.set_image(url=familiar['image'])
        embed.add_field(name="Power", value=familiar['power'])
        embed.add_field(name="Stamina", value=familiar['stamina'])
        embed.add_field(name="Agility", value=familiar['agility'])
        for skill in familiar['skills']:
            embed.add_field(name=skill['name'], value=skill['target']+skill['values'])
        await ctx.send(embed=embed)
    except KeyError as error:
        await ctx.send("Invalid familiar name.")
        

@bot.command()
async def fusion(ctx, *args):
    global fusiondic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        fusion = fusiondic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        embed = discord.Embed(title=fusion['name'], description=fusion['rarity']+"\n"+fusion['recipe'], color=0xeee657)
        embed.set_image(url=fusion['image'])
        embed.add_field(name="Bonus", value=fusion['bonus'], inline=False)
        embed.add_field(name="Power", value=fusion['power'])
        embed.add_field(name="Stamina", value=fusion['stamina'])
        embed.add_field(name="Agility", value=fusion['agility'])
        for skill in fusion['skills']:
            embed.add_field(name=skill['name'], value=skill['target']+skill['values'])
        await ctx.send(embed=embed)
    except KeyError as error:
        await ctx.send("Invalid fusion name.")
        
@bot.command()
async def mythic(ctx, *args):
    global mythicdic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        mythic = mythicdic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        print(pattern.sub('', s).lower())
        embed = discord.Embed(title=mythic['name'], description=mythic['type']+"\n"+mythic['location'], color=0xeee657)
        embed.set_image(url=mythic['image'])
#        embed.add_field(name="Bonus", value=mythic['bonus'], inline=False)
        if 'power' in mythic:
            embed.add_field(name="Power", value=mythic['power'])
        if 'stamina' in mythic:
            embed.add_field(name="Stamina", value=mythic['stamina'])
        if 'agility' in mythic:
            embed.add_field(name="Agility", value=mythic['agility'])
        await ctx.send(embed=embed)
    except KeyError as error:   
        await ctx.send("Invalid mythic name.")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="BHWikiBot", description="All information from http://bit-heroes.wikia.com/wiki/Bit_Heroes_Wiki", color=0xeee657)
    
    # give info about you here
    embed.add_field(name="Author", value="ranthai")

    # give users a link to invite thsi bot to their server
    # embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="BHWikiBot", description="List of commands are:", color=0xeee657)
    embed.add_field(name="$fam", value="Gives info about familiar", inline=False)
    embed.add_field(name="$fus", value="Gives info about fusion", inline=False)
    embed.add_field(name="$info", value="Gives info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    
    await ctx.send(embed=embed)
    
bot.run('')
