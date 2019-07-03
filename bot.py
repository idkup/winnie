import discord
from discord.ext import commands
import datetime
import random
import json

bot = commands.Bot(command_prefix='%')
spam_horizon = datetime.datetime(year=1000, month=1, day=1)

with open('data/aliases.json', 'r') as a:
    aliases = json.load(a)
    a.close()
with open('data/quotes.json', 'r') as q:
    quotes = json.load(q)
    q.close()
with open('key.txt', 'r') as k:
    key = k.readline()
with open('data/learnsets.json', 'r') as learn:
    learnset = json.load(learn)
    learn.close()
with open('data/pokedex.json', 'r') as dex:
    pokedex = json.load(dex)
    dex.close()

censoredquotes = {}
for k, v in quotes.items():
    if all(a not in k.lower() for a in ["ass", "fuck", "sex", "penis", "scrotum", "bitch", " tit", "dick"]):
        censoredquotes[k] = v


@bot.command()
async def ass(ctx):
    await ctx.author.send("leave me alone you pervert")
    await ctx.message.delete()


@bot.command()
async def calc(ctx):
    await ctx.send("Pokemon Damage Calculator: https://pokemonshowdown.com/damagecalc/")


@bot.command()
async def data(ctx, args):
    poke = "".join(args)
    poke = poke.replace(" ", "")
    poke = poke.replace("-", "")
    poke = poke.replace("'", "")
    entry = pokedex[poke.lower()]
    e = discord.Embed(title=entry["species"])
    e.add_field(name="Type:", value=", ".join(entry["types"]))
    e.add_field(name="Base Stats:", value=f"{entry['baseStats']['hp']}/{entry['baseStats']['atk']}/{entry['baseStats']['def']}/{entry['baseStats']['spa']}/{entry['baseStats']['spd']}/{entry['baseStats']['spe']}")
    e.add_field(name="Abilities:", value=", ".join(entry["abilities"].values()))
    await ctx.send(embed=e)

@bot.command()
async def evspots(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/404811373546176514/549088567603888128/image0.jpg")


@bot.command()
async def fudzillabistirdmebzergingvarie(ctx):
    await ctx.author.send("What the fuck did you just fucking say about me, you little bitch? \
    I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret \
    raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in \
    the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with \
    precision the likes of which has never been seen before on this Earth, mark my fucking words. \
    You think you can get away with saying that shit to me over the Internet? Think again, fucker. \
    As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you \
    better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. \
    You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s \
    just with my bare hands. Not only am I extensively trained in unarmed combat, \
    but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to \
    wipe your miserable ass off the face of the continent, you little shit. \
    If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you,\
     maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, \
     you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo.")


@bot.command()
async def learn(ctx, pokemon, *args):
    move = "".join(args)
    pokeh = pokemon.title()
    moveh = " ".join(args).title()
    pokemon = pokemon.replace("-", "")
    pokemon = pokemon.replace(".", "")
    pokemon = pokemon.replace(" ", "")
    move = move.replace("-", "")
    if pokemon.lower() not in learnset:
        return await ctx.send(f"{pokeh} is not recognized!")
    if move.lower() in learnset[pokemon.lower()]["learnset"]:
        return await ctx.send(f"{pokeh} can learn {moveh}!")
    return await ctx.send(f"{pokeh} cannot learn {moveh}!")


@bot.command()
async def pick(ctx, *args):
    await ctx.send(random.choice([*args]))


@bot.command()
async def pvpbasics(ctx):
    await ctx.send("""Here are some resources for beginning PvP:
    Battling: <https://docs.google.com/document/d/1fcnYDUwigMt4ykwCtO0d0cJXAEA5oKupB4MO-ZGN6xQ/edit?usp=sharing>
    General Teambuilding: \
<https://docs.google.com/document/d/1cx_A6fsuUC6BPBP5CPT7ibpNSab-Z9HlZskD1q5MQ8w/edit?usp=sharing>
    Teambuilding Checklist: \
<https://docs.google.com/document/d/1y1qZ3-Llrxifm2uS5iNb-5anhfMmN-xybyTMfS-CpH4/edit?usp=sharing>""")


@bot.command()
async def quote(ctx, name=None, pg=None):
    qf = {}
    if name == "-":
        name = None
        pg = "-"
    if pg:
        if pg.strip() == "-":
            qf = censoredquotes
    else:
        qf = quotes
    if not name:
        final = random.choice(list(qf.keys()))
        await ctx.send(f"{final} - {qf[final].title()}")
    else:
        try:
            ign = ""
            if name.lower() in aliases.keys():
                ign = aliases[name.lower()]
            final = random.choice([i for i, j in qf.items() if j == ign])
            await ctx.send(f"{final} - {name.title()}")
        except IndexError:
            await ctx.send(f"I don't have any quotes for {name.title()}!")


@bot.command()
async def rules(ctx):
    await ctx.send("""Team Magma Rules:
1. Keep Chat pg 13 overall.\
 This rule may be loosely enforced at times, but tone it down when an officer/leader asks you to.
2. Only use tags when necessary.
3. Do not spam images/videos/gifs. \
Try to keep them relevant to the discussion at hand.
4. Do not post links to other discords without permission from an officer/leader. \
The Official Pro Discord is an exception to this rule.
5. Be respectful, and if an officer/leader ask you to stop something, drop it or take it to PMs.

Reminder: 
-If you have any problems (officers included) please bring them up to an officer or leader.
-If you break a rule you will be warned.\
 If you break rules repeatedly you will be put into Time Out and further action may be taken.
-Please read over the pins or descriptions of each channel to learn what they are for.""")


@bot.command()
async def servers(ctx):
    serverlist = list(bot.guilds)
    await ctx.send(f"Connected on {len(serverlist)} servers:")
    await ctx.send('\n'.join(server.name for server in serverlist))


@bot.command()
async def smogdex(ctx, pokemon):
    await ctx.send(f"<https://smogon.com/dex/sm/pokemon/{pokemon.lower()}>")


@bot.event
async def on_member_join(member):
    await bot.get_channel(234822474611687424).send(f"""Welcome to Team Magma HQ {member.mention}! \
Please read over the rules.

Team Magma Rules:
1. Keep Chat pg 13 overall.\
 This rule may be loosely enforced at times, but tone it down when an officer/leader asks you to.
2. Only use tags when necessary.
3. Do not spam images/videos/gifs. \
Try to keep them relevant to the discussion at hand.
4. Do not post links to other discords without permission from an officer/leader. \
The Official Pro Discord is an exception to this rule.
5. Be respectful, and if an officer/leader ask you to stop something, drop it or take it to PMs.

Reminder: 
-If you have any problems (officers included) please bring them up to an officer or leader.
-If you break a rule you will be warned.\
 If you break rules repeatedly you will be put into Time Out and further action may be taken.
-Please read over the pins or descriptions of each channel to learn what they are for.""")


@bot.event
async def on_member_remove(member):
    await bot.get_channel(428701985701756930).send(f"**{member}** has left the server.")


@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        try:
            await bot.get_channel(428701985701756930).send(
                f"Message in #{before.channel}, sent by {before.author}, edited from ```{before.content}``` to\
             ```{after.content}```")
        except discord.errors.HTTPException:
            await bot.get_channel(428701985701756930).send(
                f"Message in #{before.channel}, sent by {before.author}, edited from ```{before.content}```")
            await bot.get_channel(428701985701756930).send(f" to ```{after.content}```")


@bot.event
async def on_message_delete(message):
    await bot.get_channel(428701985701756930).send(
        f"Deleted message in #{message.channel}, sent by {message.author}: ```{message.content}```")


@bot.event
async def on_message(message):
    global spam_horizon
    txt = message.content.lower()
    if message.author == bot.get_user(159985870458322944):
        await message.delete()
    if (datetime.datetime.now() - spam_horizon).total_seconds() <= 30 or bot.user == message.author:
        return await bot.process_commands(message)
    if "iriz" in txt:
        iriz = random.choice(["what", "WHAT", "wat", "WAT", "wot", "WOT", "wut", "WUT", "IM HUNGRY"])
        await message.channel.send(iriz)
        spam_horizon = datetime.datetime.now()
    elif "no u" in txt:
        await message.channel.send(message.content)
        spam_horizon = datetime.datetime.now()
    elif "iron" in txt:
        iron = random.choice([":frog:", bot.get_emoji(314143184840294400), bot.get_emoji(549410120480587776)])
        await message.channel.send(iron)
        spam_horizon = datetime.datetime.now()
    await bot.process_commands(message)


bot.run(key)
