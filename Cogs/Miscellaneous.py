import discord, sys, datetime, json
from discord.ext import commands
from time import time
from dpymenus import PaginatedMenu, Page

class Miscellaneous(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        with open("Configuration/config.json") as f:
            self.STARTTIME = json.loads(f.read())["starttime"]
        
        with open("Configuration/Help.json") as f:
            self.CONFIG = json.load(f)

    ## ==> ERROR HANDLING
    #############################################################################################

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            if str(ctx.command) == "ban" or str(ctx.command) == "kick":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Tell me the user you want to {str(ctx.command)} too!", color=discord.Color.red()))
            elif str(ctx.command) == "unban":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Pass Either the ID of the user or `name#discriminator` for me to identify them", color=discord.Color.red()))
            elif str(ctx.command) == "SetWelcomeMessage":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Enter the Message for me to welcome users with!", color=discord.Color.red()))
            elif str(ctx.command) == "SetLeaveMessage":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Enter the Message for me to send if someone leaves!", color=discord.Color.red()))
            elif str(ctx.command) == "setWelcomeChannel":
                await ctx.send(embed=discord.Embed(title="Whoops", description=f"Mention the channel where I will welcome users", color=discord.Color.red()))
            elif str(ctx.command) == "ttt":
                await ctx.send(embed=discord.Embed(title="Whoops", description="Please pass the user with whom you want to play TicTacToe too!", color = discord.Color.red()))
            elif str(ctx.command) == "Embed":
                await ctx.send(embed=discord.Embed(title="Whoops", description="Please mention the channel you want to send embed to", color=discord.Color.red()))
            else:
                await ctx.send(embed=discord.Embed(title="Whoops", description="Please pass all the arguements for that command", color = discord.Color.red()))
            
        elif str(ctx.command) == "setWelcomeChannel" and isinstance(error, commands.ChannelNotFound):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"That channel doesn't Exist!", color=discord.Color.red()))
        elif str(ctx.command) == "setWelcomeChannel" and isinstance(error, commands.ChannelNotReadable):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"I cannot read that channel!", color=discord.Color.red()))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"{str(ctx.command).capitalize()} Command is on Cooldown!", color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Whoops", description="It looks like I don't have perms to Process that", color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title="Whoops", description=f"An Unexpected Error has popped out of nowhere: {error}", color = discord.Color.red()))

            
    ##############################################################################################

    ## ==> AVATAR
    #############################################################################################

    @commands.command(aliases=['av'])
    async def avatar(self, ctx: commands.Context, user: commands.MemberConverter = None) -> None:
        if user == None: user = ctx.author
        embed = discord.Embed(color=user.color,title="AVATAR")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    #############################################################################################

    ## ==> HELP COMMAND
    ##############################################################################################

    @commands.command()
    @commands.cooldown(1,60,commands.cooldowns.BucketType.user)
    async def help(self, ctx: commands.Context) -> None:
        
        pages = []
        menu = PaginatedMenu(ctx)
        
        for i in self.CONFIG:
            description = ""
            for j in self.CONFIG[i]:
                description += "\n{}".format(j + '\n' +  self.CONFIG[i][j])
            
            pages.append(
                Page(
                    title = i,
                    description = description,
                    color = ctx.author.color
                )
            )
        menu.add_pages(pages)
            
        await menu.open()

    #############################################################################################

    ## ==> STATS
    #############################################################################################

    @commands.command()
    async def stats(self,ctx: commands.Context) -> None:
        pyver = str(sys.version[:6])
        embed_ = discord.Embed(title="STATS",color=ctx.author.color,inline=False)
        embed_.add_field(inline=False,name="Uptime",value=str(datetime.timedelta(seconds=int(round(time() - self.STARTTIME)))))
        embed_.add_field(inline=False,name="Ping",value=f"{round(self.bot.latency * 1000)}ms")
        embed_.add_field(inline=False,name="Discord.py version",value=discord.__version__)
        embed_.add_field(inline=False,name="Python Version",value=pyver)
        embed_.add_field(inline=False,name="Server",value=ctx.guild)
        embed_.add_field(inline=False,name='Total Servers',value=f'Playing in {str(len(self.bot.guilds))} servers')
        embed_.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed = embed_)

    #############################################################################################

    ## ==> USER INFO
    #############################################################################################

    @commands.command(aliases=['abt'])
    async def about(self, ctx: commands.Context, user: commands.MemberConverter = None) -> None:
        if user is None: user = ctx.author

        embed = discord.Embed(title=f"{str(user).upper()}", color=user.color)
        embed.add_field(name="Discriminator", value=str(user.discriminator))
        embed.add_field(name="User ID", value=str(user.id))
        embed.add_field(name="Created at", value=str(user.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC")))
        embed.add_field(name="Joined at", value=str(user.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC")))
        try: embed.add_field(name="Roles", inline=False, value=str(" **|** ".join(j.mention for j in [i for i in user.roles])))
        except Exception:
            embed.add_field(name="Roles", inline=False, value="Too Many Roles")
        embed.add_field(name="Top Role", value=str(user.top_role.mention))
        if user.guild.owner.id == user.id:
            embed.add_field(name="Owner", value=f"{user.mention} is the owner of {user.guild}", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    #############################################################################################
    
    ## ==> DONATE COMMAND
    ############################################################################################

    @commands.command()
    async def donate(self,ctx: commands.Context) -> None:
        emb_=discord.Embed(title="Support Us",color=ctx.author.color, url=f"https://patreon.com/hackarmour")
        emb_.add_field(name='Please support the development by becoming a patron!',value="[Click here](https://patreon.com/hackarmour) to go our Patreon page.")
        await ctx.send(embed=emb_)

    ############################################################################################
    
## ==> ADDING THE COG TO BOT
#############################################################################################

def setup(bot:commands.Bot) -> None: bot.add_cog(Miscellaneous(bot))

#############################################################################################