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
    global fdic
    global mdic
    global colordic
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    fdic = {}
    print('Scraping familiars...')
    fdic = scrape.scrapefamiliar(fdic)
    print('Scraping fusions...')
    fdic = scrape.scrapefusion(fdic)
    print('Scraping mythics...')
    mdic = scrape.scrapemythic()
    colordic = {'Common':0x97ff7d, 'Rare':0x939ef4, 'Epic':0xff807d, 'Legendary':0xffff00, 'Set':0x00fffc, 'Mythic':0xff00ae}
    print('Ready')
    
@bot.command()
async def f(ctx, *args):
    global fdic
    global colordic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        f = fdic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        if f['type'] == 'familiar':
            embed = discord.Embed(title=f['name'], description=f['rarity']+"\n"+f['location'], color=colordic[f['rarity']])
        else:
            embed = discord.Embed(title=f['name'], description=f['rarity']+"\n"+f['recipe'], color=colordic[f['rarity']])
            embed.add_field(name="Bonus", value=f['bonus'], inline=False)
        embed.set_image(url=f['image'])
        embed.add_field(name="Power", value=f['power'])
        embed.add_field(name="Stamina", value=f['stamina'])
        embed.add_field(name="Agility", value=f['agility'])
        for skill in f['skills']:
            embed.add_field(name=skill['name'], value=skill['target']+skill['values'])
        await ctx.send(embed=embed)
    except KeyError as error:
        await ctx.send("Invalid familiar/fusion name.")
        
@bot.command()
async def m(ctx, *args):
    global mdic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        m = mdic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        print(pattern.sub('', s).lower())
        embed = discord.Embed(title=m['name'], description=m['type']+"\n"+m['location'], color=0xff00ae)
        embed.set_image(url=m['image'])
#        embed.add_field(name="Bonus", value=m['bonus'], inline=False)
        if 'power' in m:
            embed.add_field(name="Power", value=m['power'])
        if 'stamina' in m:
            embed.add_field(name="Stamina", value=m['stamina'])
        if 'agility' in m:
            embed.add_field(name="Agility", value=m['agility'])
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
    embed.add_field(name="$f", value="Gives info about familiar/fusion", inline=False)
    embed.add_field(name="$info", value="Gives info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    
    await ctx.send(embed=embed)
    
bot.run('')
