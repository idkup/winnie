from discord.ext import commands
import datetime
import random

bot = commands.Bot(command_prefix='%')
spam_horizon = datetime.datetime(year=1000, month=1, day=1)

with open('data/aliases.txt', 'r') as a:
    al = a.readlines()
    a.close()
with open('data/quotes.txt', 'r') as q:
    qs = q.readlines()
    q.close()
aliases = {}
quotes = {}
censoredquotes = {}
for line in al:
    line = line.strip()
    names = line.split(" ")
    for n in names:
        aliases[n] = names[0]
for line in qs:
    line = line.replace("\\n", "\n")
    ls = line.split(" , ")
    quotes[ls[0]] = ls[-1].strip()
for k, v in quotes.items():
    if all(a not in k.lower() for a in ["ass", "fuck", "sex", "penis", "scrotum", "bitch", " tit", "dick"]):
        censoredquotes[k] = v


@bot.command()
async def evspots(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/404811373546176514/549088567603888128/image0.jpg")


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
            if name.lower() in aliases.keys():
                name = aliases[name]
            final = random.choice([i for i, j in qf.items() if j == name])
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


@bot.event
async def on_member_join(member):
    await bot.get_channel(234822474611687424).send(f"""Welcome to Team Magma HQ {member.mention}!\
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
    try:
        await bot.get_channel(428701985701756930).send(
            f"Message in #{before.channel}, sent by {before.author}, edited from ```{before.content}``` to\
         ```{after.content}```")
    except discord.errors.HTTPException:
        await bot.get_channel(428701985701756930).send(
            f"Message in #{before.channel}, sent by {before.author}, edited from ```{before.content}```")
        await bot.get_channel(428701985701756930).send(" to\
         ```{after.content}```")


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

bot.run('NTg1NjQ4MDI3OTU2NDEyNDQw.XPchQw.NMjHTzNC-pvKL8p80QjgIenKIL0')
