class Mafia:
    def __init__(self, userlist):
        self.pc = len(userlist)
        self.pl = {"town": [], "mafia": []}
        self.phase = 1
        self.votes = {}
        self.mafiakill = True
        m = len(userlist) // 4
        maf = random.sample(userlist, m)
        for i in userlist:
            if i in maf:
                self.pl["mafia"].append(i)
            else:
                self.pl["town"].append(i)

    def changephase(self):
        self.phase += 1
        self.votes = {}
        self.mafiakill = False


@bot.command()
async def initialize_mafia(ctx, *args):
    global game
    if ctx.author.id != 590336288935378950:
        return
    userlist = []
    for i in args:
        u = bot.get_user(int(i))
        userlist.append(u)
    game = Mafia(userlist)
    print(userlist)
    for j in userlist:
        if j in game.pl["town"]:
            await j.send("u town")
        else:
            await j.send("u mafia")
    print(game.pl)


@bot.command()
async def lynch(ctx):
    global game
    if game is False:
        return
    if ctx.author not in game.pl["town"] and ctx.author not in game.pl["mafia"]:
        return
    if game.phase % 2 == 0:
        return
    try:
        x = ctx.message.mentions[0]
        if x not in game.pl["town"] and x not in game.pl["mafia"]:
            return
    except:
        return
    try:
        game.votes[x].append(ctx.author)
    except KeyError:
        game.votes[x] = [ctx.author]
    print(game.votes)
    for p, v in game.votes.items():
        if len(v) > game.pc / 2:
            await ctx.send(f"{p.name} was lynched.")
            game.changephase()