import discord, sys, datetime, json
from discord.ext import commands
from time import time
from random import choice

class Miscellaneous(commands.Cog):
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        with open("Configuration/config.json") as f:
            self.STARTTIME = json.loads(f.read())["starttime"]

    ## ==> ERROR HANDLING
    #############################################################################################

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=discord.Embed(title="Whoops", description="Command Not Found", color=discord.Color.red()))        
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
    async def help(self, ctx: commands.Context,*,thing=None) -> None:
        embed = discord.Embed(title="HELP",color=ctx.author.color)

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/848185831940030485/849958477366427648/assistant2.png")

        if thing == None:
            embed.add_field(
                name="What do you want help with?",
                value="Type any of the commands below to get help:",
                inline=False
            )
            embed.add_field(name=f"{'■'*15}\n:hand_splayed: >help Welcomer",value="```\nTo Get Help with Welcomer Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:face_with_monocle: >help Moderation",value="```\nTo Get Help with Moderation Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:grin: >help Fun",value=f"```\nTo Get Help with Fun Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:musical_note: >help Music",value=f"```\nTo Get Help with Music Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:o2: >help Miscellaneous", value=f"```\nTo Get Help with Other Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:game_die: >help Tic Tac Toe",value=f"```\nTo Get Help with Tic Tac Toe Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:notepad_spiral: >help Embeds", value=f"```\nTo Get Help with Embed Commands\n```\n", inline=False)
            embed.add_field(name=f"{'■'*15}\n:alien: >help Lon", value=f"```\nTo Get Help with LON Commands\n```\n", inline=False)

        elif thing.lower() == "welcomer":
            embed.add_field(
                name="**WELCOMER**",
                inline=False,
                value=f"""
{'■'*15}
:white_check_mark: `>toggleWelcomer`:
```
To Toggle Welcomer On or Off
```
{'■'*15}
:scroll: `>SetWelcomeMessage <message>`:
```
To Set the Welcome Message

Using "|user|" in message will replace it with a mention of the new user

Using "|guild|" in message will replace it with the name of the server
```
{'■'*15}
:scroll: `>SetLeaveMessage <message>`:
```
To Set the Leave Message

Using "|user|" in message will replace it with User's Name

Using "|guild|" in message will replace it with Server's Name
```
{'■'*15}
:dart: `>setWelcomeChannel <Channel>`:
```
To Set the channel to send Welcome message in

Mention channel as #<channel name>
```
    """
        )

        elif thing.lower() in ["moderation", "mod"]:
            embed.add_field(
                name="MODERATION",
                inline=False,
                value=f"""
{'■'*15}
:x: `>ban <user>`
```
To Ban <user>
```
{'■'*15}
:negative_squared_cross_mark: `>kick <user>`
```
To Kick <user>
```
{'■'*15}
:white_check_mark: `>unban <username>#<discriminator>`
```
To Unban the user passed in the function
```
{'■'*15}
:mute: `>mute <user> <time>`
```
To Mute <user> for <time>. 
Time: s, m, h, d, w
```
{'■'*15}
:loud_sound: `>unmute <user>`
```
To Unmute <user>
```
{'■'*15}
:ninja: `>setLogChannel <channel>`
```
To Set the Log Channel on the server

It will not send logs until this is not set
```
{'■'*15}
:white_check_mark: `>toggleLog`
```
To Toggle Logs

The Bot will not send logs until this is not done
```
{'■'*15}
:ninja: `>toggleMod`
```
To toggle AutoMod Feature of the bot 
```
{'■'*15}
:x: `>purge <number>`
```
It will clear <number> amount of messages
```
""",
        )

        elif thing.lower() == "fun":
            embed.add_field(
                name="FUN",
                inline=False,
                value=f"""
{'■'*15}
:thinking_face: `>8ball <question>`
```
Give a random answer for <question>
```
{'■'*15}
:joy: `>meme`
```
Sends a meme from Reddit
```
{'■'*15}
:rofl: `>memes <number>`
```
Sends <number> amount of memes
Maximum: 3
```
{'■'*15} 
:regional_indicator_f: `>F <reason>`
```
To press F for <reason> [reason is optional]
```
{'■'*15}
:coin: `>coin`
```
To toss a coin
```
"""
        )

        elif thing.lower() == "music":
            embed.add_field(
                name="MUSIC",
                inline=False,
                value=f"""
{'■'*15}
:musical_note: `>play <music>`
```
Adds <music> to queue or starts playing if queue is empty
```
{'■'*15}
:track_next: `>skip`
```
Skips to next song
```
{'■'*15}
:pause_button: `>pause`
```
Pauses the music
```
{'■'*15}
:arrow_forward: `>resume`
```
Resumes music
```
{'■'*15}
:notepad_spiral: `>queue`
```
Displays the song queue
```
{'■'*15}
:no_entry_sign: `>disconnect`
```
Disconnects the bot from voice channel and clears the queue
```
"""
        )

        elif thing.lower() in ["miscellaneous", "misc", "others"]:
            embed.add_field(
                name="MISCELLANEOUS COMMANDS",
                inline=False,
                value=f"""
{'■'*15}
:bar_chart: `>stats`
```
To Get the stats for the Bot
```
{'■'*15}
:face_with_monocle: `>av <user>`
```
To Get the Avatar of <user>

If nothing is passed it will send the authors avatar
```
{'■'*15}
:eyes: `>about <user>`
```
To Get the info of <user>

If nothing is passed it will send the authors info
```
{'■'*15}
:moneybag:`>donate`
```
To get patreon link of HackArmour
```
"""
        )

        elif thing.lower() in ["tic tac toe", "tictactoe", "ttt"]:
            embed.add_field(
                name="TIC TAC TOE",
                inline=False,
                value="""
:video_game: `>ttt <user>`:
```
To Start a game of Tic Tac Toe with <user>

Please wait until the bot reacts with all the emojis before you select one
```
"""
        )

        elif thing.lower() in ["embeds", "embed"]:
            embed.add_field(
                name="**EMBEDS**",
                inline=False,
                value="""
:notepad_spiral: `>embed <mention_channel>`
```
Sends an embed at <mention_channel>
    
Bot will Prompt you for the values
    
You can enter the value as "none" if you don't want to enter it in "description", "number of fields" and "footer"
```
"""
        )
        
        elif thing.lower() == "lon":
            embed.add_field(
                name = "**LON**",
                inline=False,
                value=f"""
{'■'*15}
**L**ACK **O**F **N**ITRO

{choice([":laughing:", ":grinning:", ":smiley:", ":smile:", ":grin:", ":laughing:"])} `>lon <emoji name>`
```
Sends an emoji with name <emoji name> if it exists in the configuration file
```
{'■'*15}
:ballot_box_with_check: `>lonall`
```
Get list of all emojis which can be used
```
"""
        )

        else:
            embed.add_field(name="I can't Understand what do you mean", value="Use just `>help` without any arguements")

        await ctx.send(embed=embed)

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