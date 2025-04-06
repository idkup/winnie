import discord
from discord.ext import commands
import datetime
import random
import re
import pickle
import json
from quote_db import QuoteDB
from quoted import Quoted
from typing import Tuple, Optional


# REACTION ROLES
class ReactionRoleFlags(commands.FlagConverter):
    Title: str
    Description: Optional[str]
    Emojis: Tuple[int, ...]
    Roles: Tuple[int, ...]
    Unique: bool = False


MAGMA_GUILD = 234822474611687424
IRIZ_GUILD = 1102367514786279424
LISS_GUILD = 1357538074183336087

REACTION_ROLES_CHANNELS = [863188820325695508, 1109582389337931907, 1357577842271064265]
POINT_LOG_CHANNEL = 1357885239514628186
STARBOARD_CHANNELS = {LISS_GUILD: 1358358519291842671}

ROLE_SLYTHERIN = 1357741779449024582
ROLE_GRYFFINDOR = 1357741193919729894
ROLE_RAVENCLAW = 1357745890009419796
ROLE_HUFFLEPUFF = 1357746016786579476

STAR_THRESHOLD = 1

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

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
    with open('data/quotes.txt', 'rb') as q:
        quote_db = pickle.load(q)
        q.close()
except FileNotFoundError:
    quote_db = QuoteDB()

try:
    with open('data/points.json', 'r') as pts:
        points_db = json.load(pts)
        pts.close()
except FileNotFoundError:
    points_db = {str(ROLE_SLYTHERIN): 0, str(ROLE_GRYFFINDOR): 0, str(ROLE_RAVENCLAW): 0, str(ROLE_HUFFLEPUFF): 0}


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
        with open("data/quotes.txt", "wb+") as qf:
            pickle.dump(quote_db, qf)
            qf.close()
        if ctx.guild.id in STARBOARD_CHANNELS.keys():
            e = discord.Embed()
            e.set_author(alias)
            e.description = quote_text
            await bot.get_channel(STARBOARD_CHANNELS[ctx.guild.id]).send(embed=e)
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
            with open("data/quotes.txt", "wb+") as qf:
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
async def generate_reaction_roles(ctx, *, flags: ReactionRoleFlags):
    embed = discord.Embed(title=flags.Title)
    desc = flags.Description or ""
    if flags.Unique:
        desc += "\n*You may only select one of the following roles.*\n\n"
    for e, r in zip(flags.Emojis, flags.Roles):
        desc += f"{bot.get_emoji(e)} <@&{r}>\n"
    embed.description = desc
    message = await ctx.channel.send(embed=embed)
    for e in flags.Emojis:
        await message.add_reaction(bot.get_emoji(e))


@bot.command(aliases=["hc"])
async def headcount(ctx, dungeon):
    if ctx.author.guild_permissions.manage_messages:
        e = discord.Embed(title=f"Headcount for {dungeon}",
                          description=f"React with {bot.get_emoji(314146023243251712)} to participate!")
        message = await ctx.channel.send(f"Headcount started by {ctx.author.mention}.", embed=e)
        await message.add_reaction(bot.get_emoji(314146023243251712))


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
async def houses(ctx):
    if ctx.guild.id == LISS_GUILD:
        e = discord.Embed(title="Current Points")

        e.add_field(name="Slytherin", value=points_db[str(ROLE_SLYTHERIN)])
        e.add_field(name="Gryffindor", value=points_db[str(ROLE_GRYFFINDOR)])
        e.add_field(name="Ravenclaw", value=points_db[str(ROLE_RAVENCLAW)])
        e.add_field(name="Hufflepuff", value=points_db[str(ROLE_HUFFLEPUFF)])

        await ctx.send(embed=e)

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
async def quote(ctx, name=None):
    has_quotes = []
    for u in quote_db.quoted:
        if len(u.quotes) > 0 and ctx.guild.get_member(u.uid) is not None:
            has_quotes.append(u)
    if not name:
        user = random.choice(has_quotes)
        name = user.aliases[0]
    else:
        for u in has_quotes:
            if name.lower() in u.aliases:
                user = u
                break
        else:
            return await ctx.send("This alias is not in the database or has no quotes!")
    q = user.get_random_quote()
    return await ctx.send(f"\"{q}\" - {name.title()}")


@bot.command()
async def remove_quote(ctx, quote_text):
    for u in quote_db.quoted:
        if quote_text in u.quotes:
            u.quotes.remove(quote_text)
            return await ctx.send("Quote removed from database.")
    return await ctx.send("Quote not found in database.")

@bot.command()
async def reset(ctx):
    global points_db
    if ctx.guild.id != LISS_GUILD or not ctx.author.guild_permissions.manage_messages:
        return
    points_db = {str(ROLE_SLYTHERIN): 0, str(ROLE_GRYFFINDOR): 0, str(ROLE_RAVENCLAW): 0, str(ROLE_HUFFLEPUFF): 0}
    with open('data/points.json', 'w+') as f:
        json.dump(points_db, f)
    return await ctx.send("All points reset.")


@bot.command()
async def rules(ctx):
    if ctx.guild.id == MAGMA_GUILD:
        await ctx.send("""Team Magma Rules:
1. Keep Chat pg 13 overall.\
 This rule may be loosely enforced at times, but tone it down when an officer/leader asks you to.
2. Only use tags when necessary.
3. Do not spam images/videos/gifs. \
Try to keep them relevant to the discussion at hand.
4. Do not post links to other discords without permission from an officer/leader. \
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
    if member.guild.id == MAGMA_GUILD:
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
    elif member.guild.id == IRIZ_GUILD:
        await bot.get_channel(1109581230372036719).send(f"Hey <@{member.id}>! Welcome to {member.guild.name}! {str(bot.get_emoji(1109943681487753226))} Please check out <#1109582389337931907>! I hope you enjoy your stay!")
        await member.add_roles(member.guild.get_role(1109963220812300374))


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
        if "pts" in txt or "points" in txt and message.guild.id == LISS_GUILD:
            if message.author.guild_permissions.manage_messages:
                number_pattern = r"[-+]?\d+"
                matches = list(re.finditer(number_pattern, txt))
                for match in matches:
                    start = match.start()
                    if start > 0 and txt[start - 1] == '@':
                        continue
                    to_add = int(match[0])
                    break
                culprit = "Someone"
                if message.mentions:
                    culprit = f"<@{message.mentions[0].id}>"
                if "slytherin" in txt:
                    house = "Slytherin"
                    points_db[str(ROLE_SLYTHERIN)] += to_add
                elif "gryffindor" in txt:
                    house = "Gryffindor"
                    points_db[str(ROLE_GRYFFINDOR)] += to_add
                elif "ravenclaw" in txt:
                    house = "Ravenclaw"
                    points_db[str(ROLE_RAVENCLAW)] += to_add
                elif "hufflepuff" in txt:
                    house = "Hufflepuff"
                    points_db[str(ROLE_HUFFLEPUFF)] += to_add
                else:
                    return await bot.process_commands(message)

                splits = re.split(r"[-+]?\d+|slytherin|gryffindor|ravenclaw|hufflepuff|pts|points", txt, flags=re.IGNORECASE)
                splits = [x for x in splits if x is not None]
                reason = max(splits, key=len)
                reason = reason.strip()
                reason = None if len(reason.strip()) <= 3 else reason

                await bot.get_channel(POINT_LOG_CHANNEL).send(f"{culprit} has earned {house} {to_add} points courtesy of <@{message.author.id}>!\nReason: {reason}")

                with open('data/points.json', 'w+') as f:
                    json.dump(points_db, f)

        if "iriz" in txt and message.guild.id in [MAGMA_GUILD, IRIZ_GUILD]:
            iriz = random.choice(["what", "WHAT", "wat", "WAT", "wot", "WOT", "wut", "WUT", "IM HUNGRY"])
            await message.channel.send(iriz)
            spam_horizon = datetime.datetime.now()
        elif "no u" in txt and message.guild.id == MAGMA_GUILD:
            await message.channel.send(message.content)
            spam_horizon = datetime.datetime.now()
        elif "iron" in txt and message.guild.id in [MAGMA_GUILD, IRIZ_GUILD]:
            iron = random.choice([":frog:", bot.get_emoji(314143184840294400), bot.get_emoji(549410120480587776)])
            await message.channel.send(iron)
            spam_horizon = datetime.datetime.now()
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    embeds = message.embeds
   # REACTION ROLES
    if payload.channel_id in REACTION_ROLES_CHANNELS and message.author == bot.user:
        parse = embeds[0].description
        unique = "*You may only select one of the following roles.*" in parse
        parsed_lines = parse.splitlines()[1:]
        for line in parsed_lines:
            role_id = int(re.search(r'(?<=\<@&)(.*?)(?=>)', line)[1])
            if str(payload.emoji) in line:
                await guild.get_member(payload.user_id).add_roles(guild.get_role(role_id))
                continue
            if unique:
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))

    # STARBOARD?
    if str(payload.emoji) == "⭐" and guild.id in STARBOARD_CHANNELS.keys():
        for react in message.reactions:
            if str(react.emoji) == "⭐":
                users = [user async for user in react.users()]
                try:
                    users.remove(message.author)
                except ValueError:
                    pass
                if len(users) == STAR_THRESHOLD:
                    # for u in quote_db.quoted:
                    #     if u.uid == message.author.id:
                    #         to_quote = u
                    #         break
                    # else:
                    #     new_user = Quoted(message.author.id)
                    #     alias = message.author.name
                    #     if alias.lower() not in quote_db.taken_aliases:
                    #         new_user.add_alias(alias.lower())
                    #         quote_db.add_taken_alias(alias.lower())
                    #     else:
                    #         await channel.send(
                    #             f"{alias} has been taken by another user. A new alias must be manually assigned.")
                    #     quote_db.add_user(new_user)
                    #     to_quote = new_user
                    # to_quote.add_quote(message.content)
                    with open("data/quotes.txt", "wb+") as qf:
                        pickle.dump(quote_db, qf)
                        qf.close()
                    e = discord.Embed()
                    await channel.send(message.author.name)
                    e.set_author(message.author.name)
                    e.description = message.content
                    await bot.get_channel(STARBOARD_CHANNELS[guild.id]).send(embed=e)
                break

    # MAGMA GIVEAWAYS
    if payload.channel_id != 608098962305581070:
        return
    if str(payload.emoji) != "❌":
        return
    if payload.user_id != message.author.id:
        return
    if "!g" not in message.content:
        return
    for react in message.reactions:
        if str(react.emoji) == '<:magma:314146023243251712>':
            users = [user async for user in react.users()]
            try:
                users.remove(bot.user)
            except ValueError:
                break
            winner = random.choice(users)
            await channel.send(f"{winner.mention} has won {message.content.replace('!g', '').strip()} from {message.author.mention}!")


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    embeds = message.embeds
    # REACTION ROLES
    if payload.channel_id in REACTION_ROLES_CHANNELS and message.author == bot.user:
        parse = embeds[0].description
        parsed_lines = parse.splitlines()[1:]
        for line in parsed_lines:
            role_id = int(re.search(r'(?<=\<@&)(.*?)(?=>)', line)[1])
            if str(payload.emoji)[1:-1] in line:
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))


bot.run(key)
