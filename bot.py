import discord
from discord.ext import commands
import datetime
import random
import pickle
import json
from quote_db import QuoteDB
from quoted import Quoted

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='%', intents=intents)
spam_horizon = datetime.datetime(year=1000, month=1, day=1)

with open('key.txt', 'r') as k:
    key = k.readline()
with open('data/learnsets.json', 'r') as learn:
    learnset = json.load(learn)
    learn.close()
with open('data/pokedex.json', 'r') as dex:
    pokedex = json.load(dex)
    dex.close()
with open('data/typecolors.json', 'r') as tc:
    typecolors = json.load(tc)
    tc.close()

try:
    with open('quotes.txt', 'rb') as q:
        quote_db = pickle.load(q)
        q.close()
except FileNotFoundError:
    quote_db = QuoteDB()


@bot.command()
async def add_alias(ctx, alias):
    if ctx.message.author.guild_permissions.manage_messages:
        if not ctx.message.mentions:
            return await ctx.send("Please mention the user you are trying to add an alias for.")
        if alias.lower() in quote_db.taken_aliases:
            return await ctx.send("This alias has already been taken by another user.")
        uid = ctx.message.mentions[0].id
        for u in quote_db.quoted:
            if u.uid == uid:
                user = u
                break
        else:
            return await ctx.send("The user you mentioned is not in the quote database.")
        user.add_alias(alias.lower())
        quote_db.add_taken_alias(alias.lower())
        print(user.aliases)
        return await ctx.send(f"<@{uid}> has received the alias {alias}!")
    return await ctx.send("This is an officer-only command.")


@bot.command()
async def add_quote(ctx, alias, quote_text):
    if ctx.message.author.guild_permissions.manage_messages:
        for u in quote_db.quoted:
            if alias.lower() in u.aliases:
                user = u
                break
        else:
            return await ctx.send("This alias is not in the database!")
        user.add_quote(quote_text)
        with open("quotes.txt", "wb+") as qf:
            pickle.dump(quote_db, qf)
            qf.close()
        return await ctx.send("Quote added.")
    return await ctx.send("This is an officer-only command.")


@bot.command()
async def add_user(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        if ctx.message.mentions:
            uid = ctx.message.mentions[0].id
            for u in quote_db.quoted:
                if u.uid == uid:
                    return await ctx.send("This user is already in the database!")
            new_user = Quoted(uid)
            alias = ctx.message.mentions[0].name
            if alias.lower() not in quote_db.taken_aliases:
                new_user.add_alias(alias.lower())
                quote_db.add_taken_alias(alias.lower())
            else:
                await ctx.send(f"{alias} has been taken by another user. A new alias must be manually assigned.")
            quote_db.add_user(new_user)
            with open("quotes.txt", "wb+") as qf:
                pickle.dump(quote_db, qf)
                qf.close()
            return await ctx.send(f"<@{uid}> has been added to the quote database.")
    return await ctx.send("This is an officer-only command.")


@bot.command()
async def calc(ctx):
    await ctx.send("Pokemon Damage Calculator: https://pokemonshowdown.com/damagecalc/")


@bot.command(aliases=['dt', 'poke', 'pokemon'])
async def data(ctx, args):
    poke = "".join(args)
    poke = poke.replace(" ", "")
    poke = poke.replace("'", "")
    poke = poke.replace("-", "")
    try:
        entry = pokedex[poke.lower()]
    except KeyError:
        return await ctx.send(f"{poke} is not recognized!")
    imgn = format(entry['num'], '03d')
    e = discord.Embed(title=f"{imgn}. {entry['species']}")
    if 'alola' in poke:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-a.png"
    elif poke == 'giratinaorigin':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-o.png"
    elif poke == 'kyuremblack':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-b.png"
    elif poke == 'kyuremwhite':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-w.png"
    elif poke == 'keldeoresolute':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-r.png"
    elif poke == 'darmanitanzen':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}d.png"
    elif poke == 'rotomwash':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}w.png"
    elif poke == 'rotomheat':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}h.png"
    elif poke == 'rotommow':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}m.png"
    elif poke == 'rotomfrost':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}f.png"
    elif poke == 'rotomfan':
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}s.png"
    elif poke == 'shayminsky' or 'therian' in poke:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-s.png"
    elif 'primal' in poke or 'pirouette' in poke:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-p.png"
    elif 'megax' in poke:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-mx.png"
    elif 'megay' in poke:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-my.png"
    elif 'mega' in poke:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}-m.png"
    else:
        url = f"https://www.serebii.net/pokedex-sm/icon/{imgn}.png"
    e.set_thumbnail(url=url)
    e.add_field(name='Type:', value=', '.join(entry['types']))
    e.colour = typecolors[entry['types'][0]]
    e.add_field(name="Base Stats:", value=f"{entry['baseStats']['hp']}/{entry['baseStats']['atk']}/{entry['baseStats']['def']}/{entry['baseStats']['spa']}/{entry['baseStats']['spd']}/{entry['baseStats']['spe']}")
    try:
        ha = entry["abilities"]["H"]
        e.add_field(name="Abilities:", value=", ".join(entry["abilities"].values())+" (H)")
    except KeyError:
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
async def purge(ctx, ct=10):
    if ctx.author.guild_permissions.manage_messages:
        try:
            count = int(ct) + 1
        except ValueError:
            return
        async for msg in ctx.channel.history(limit=count):
            if not msg.pinned:
                await msg.delete()


@bot.command()
async def pvpbasics(ctx):
    await ctx.send("""Here are some resources for beginning PvP:
    Battling: <https://docs.google.com/document/d/1fcnYDUwigMt4ykwCtO0d0cJXAEA5oKupB4MO-ZGN6xQ/edit?usp=sharing>
    General Teambuilding: \
<https://docs.google.com/document/d/1cx_A6fsuUC6BPBP5CPT7ibpNSab-Z9HlZskD1q5MQ8w/edit?usp=sharing>
    Teambuilding Checklist: \
<https://docs.google.com/document/d/1y1qZ3-Llrxifm2uS5iNb-5anhfMmN-xybyTMfS-CpH4/edit?usp=sharing>""")


@bot.command()
async def quote(ctx, name=None):
    if not name:
        user = random.choice(quote_db.quoted)
        name = user.aliases[0]
    else:
        for u in quote_db.quoted:
            if name.lower() in u.aliases:
                user = u
                break
        else:
            return await ctx.send("This alias is not in the database!")
    q = user.get_random_quote()
    return await ctx.send(f"\"{q}\" - {name}")



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
async def on_ready():
    pass


@bot.event
async def on_member_join(member):
    await bot.get_channel(234822474611687424).send(f"""Welcome to Team Magma HQ {member.mention}! \
Please read over the rules.

Team Magma Rules:
1. Keep Chat PG-13 overall.\
 This rule may be loosely enforced at times, but tone it down when an officer/leader asks you to.
2. Only use tags when necessary.
3. Do not spam images/videos/gifs. \
Try to keep them relevant to the discussion at hand.
4. Do not post links to other discords without permission from an officer/leader. \
5. Be respectful, and if an officer/leader asks you to stop something, drop it or take it to PMs.

Reminder: 
-If you have any problems (officers included) please bring them up to an officer or leader.
-If you break a rule you will be warned.\
 If you break rules repeatedly you will be put into Time Out and further action may be taken.
-Please read over the pins or descriptions of each channel before messaging.""")


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
    if message.channel.id == 608098962305581070 and "!g" in txt:
        await message.add_reaction(bot.get_emoji(314146023243251712))
        await message.add_reaction("❌")
    else:
        if message.author == bot.get_user(159985870458322944):
            await message.delete()
        if "nigger" in txt:
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


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.id == 864985245178527765:
        if str(payload.emoji) == "1️⃣":
            await guild.get_member(payload.user_id).add_roles(guild.get_role(863192043860787200))
        elif str(payload.emoji) == "2️⃣":
            await guild.get_member(payload.user_id).add_roles(guild.get_role(865006742411804673))
        elif str(payload.emoji) == "3️⃣":
            await guild.get_member(payload.user_id).add_roles(guild.get_role(865006785835302913))
        elif str(payload.emoji) == "4️⃣":
            await guild.get_member(payload.user_id).add_roles(guild.get_role(863192453351079986))
        elif str(payload.emoji) == "5️⃣":
            await guild.get_member(payload.user_id).add_roles(guild.get_role(863192504332845117))

    if payload.channel_id != 608098962305581070:
        return
    if str(payload.emoji) != "❌":
        return
    if payload.user_id != message.author.id:
        return
    if "!g" not in message.content:
        return
    for react in message.reactions:
        if react.custom_emoji:
            if react.emoji.id == 314146023243251712:
                users = await react.users().flatten()
                try:
                    users.remove(bot.user)
                except ValueError:
                    pass
                winner = random.choice(users)
                await channel.send(f"{winner.mention} has won {message.content.replace('!g', '').strip()} from {message.author.mention}!")


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.id == 864985245178527765:
        if str(payload.emoji) == "1️⃣":
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(863192043860787200))
        elif str(payload.emoji) == "2️⃣":
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(865006742411804673))
        elif str(payload.emoji) == "3️⃣":
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(865006785835302913))
        elif str(payload.emoji) == "4️⃣":
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(863192453351079986))
        elif str(payload.emoji) == "5️⃣":
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(863192504332845117))

bot.run(key)
