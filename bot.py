import re
import scrape
import discord
from builtins import str
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
famdic = None
fusdic = None

@bot.event
async def on_ready():
    global famdic
    global fusdic
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Scraping...')
    famdic = scrape.scrapefam()
    fusdic = scrape.scrapefus()
    print('Ready')

@bot.command()
async def fam(ctx, *args):
    global famdic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        fam = famdic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        embed = discord.Embed(title=fam['id'], description=fam['rarity'], color=0xeee657)
        embed.set_image(url=fam['image'])
        embed.add_field(name="Power", value=fam['power'])
        embed.add_field(name="Stamina", value=fam['stamina'])
        embed.add_field(name="Agility", value=fam['agility'])
        for skill in fam['skills']:
            embed.add_field(name=skill['name'], value=skill['target']+skill['values'])
        await ctx.send(embed=embed)
    except KeyError as error:
        await ctx.send("Invalid familiar name.")
        

@bot.command()
async def fus(ctx, *args):
    global fusdic
    try:
        s = "".join(args)
        pattern = re.compile('[\W_]+', re.UNICODE)
        fus = fusdic[pattern.sub('', s).lower()] # for case and whitespace and symbol-insensitive searching
        embed = discord.Embed(title=fus['id'], description=fus['rarity']+"\n"+fus['recipe'], color=0xeee657)
        embed.set_image(url=fus['image'])
        embed.add_field(name="Power", value=fus['power'])
        embed.add_field(name="Stamina", value=fus['stamina'])
        embed.add_field(name="Agility", value=fus['agility'])
        for skill in fus['skills']:
            embed.add_field(name=skill['name'], value=skill['target']+skill['values'])
        await ctx.send(embed=embed)
    except KeyError as error:
        await ctx.send("Invalid fusion name.")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)
    
    # give info about you here
    embed.add_field(name="Author", value="ranthai")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    
    await ctx.send(embed=embed)
    
bot.run('')
