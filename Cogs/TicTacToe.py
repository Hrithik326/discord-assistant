import discord, asyncio
from discord.ext import commands


class TicTacToe(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
        ## ==> DECLARING VARIABLES
        ##############################################################################################
        
        self._board_template = [
            ":white_large_square:",":white_large_square:",":white_large_square:\n",
            ":white_large_square:",":white_large_square:",":white_large_square:\n",
            ":white_large_square:",":white_large_square:",":white_large_square:"
        ]
        self._emoji_template = ['↖', '⬆', '↗', '⬅', '⏹', '➡', '↙', '⬇', '↘']
        self.data = {}
        
        ##############################################################################################
        
    @commands.command()
    async def ttt(self, ctx: commands.Context, p2: commands.MemberConverter) -> None:
        
        ## ==> CHECKS
        ##############################################################################################
        
        if ctx.author.bot: return
        if p2.bot: 
            await ctx.send("You can't play against a bot!")
            return
        if ctx.author.id == p2.id:
            await ctx.send("You can't invite yourself!")
            return
        
        ##############################################################################################
        
        ## ==> ASK FOR A GAME
        ##############################################################################################
        
        message = await ctx.send(embed=discord.Embed(title="TIC TAC TOE *REVAMP*", description=f"{p2.mention}, {ctx.author.mention} invites you to a game of Tic Tac Toe!\nReact with ✋ to accept the invite!"))
        await message.add_reaction("✋")
        try:
            await self.bot.wait_for("reaction_add", timeout=25.0, check=lambda reaction, user: user == p2 and str(reaction.emoji) == "✋")
        except asyncio.TimeoutError:
            await ctx.send("Request Timed Out")
            return
            
        ##############################################################################################
            
        await message.edit(embed=discord.Embed(title="THE GAME HAS BEGUN!", description="Please Wait for the bot to react with all emojis before entering your choice"))
        await message.clear_reactions()
        await asyncio.sleep(2.0)
        await message.clear_reactions()
        
        ## ==> EDIT THE EMBED TO SET THE GRID
        ##############################################################################################
        
        embed = discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", description="".join(self._board_template), color=ctx.author.color)
        embed.set_footer(text=f"{ctx.author.name}'s Turn")
        await message.edit(embed=embed)
        
        ##############################################################################################
        
        ## ==> VARIABLES
        ##############################################################################################
        
        _turn = ctx.author
        _current_board = self._board_template.copy()
        self.data[f"{ctx.author.id} & {p2.id}"] = {"CUR_REACTION": None, "TURN_NO": 1}
        
        ##############################################################################################
        
        ## ==> ADD REACTIONS
        ##############################################################################################
        
        for i in self._emoji_template: await message.add_reaction(i)
        
        ##############################################################################################
        
        ## ==> CHECK FOR `wait_for`
        ##############################################################################################
        
        def check(reaction, user):
            if user == _turn:
                self.data[F"{ctx.author.id} & {p2.id}"]["CUR_REACTION"] = str(reaction.emoji)
            return user == _turn
        
        ##############################################################################################        
           
        ## ==> MAIN LOOP
        ##############################################################################################
        
        while True:
            
            ## ==> TO CHECK IF WHAT THE USER REACTED WITH IS VALID OR NOT
            ##############################################################################################
            
            x = []
            for index, item in enumerate(_current_board):
                if item == ":white_large_square:" or item == ":white_large_square:\n":
                    if index == 0:
                        x.append(self._emoji_template[0])
                    if index == 1:
                        x.append(self._emoji_template[1])
                    if index == 2:
                        x.append(self._emoji_template[2])
                    if index == 3:
                        x.append(self._emoji_template[3])
                    if index == 4:
                        x.append(self._emoji_template[4])
                    if index == 5:
                        x.append(self._emoji_template[5])
                    if index == 6:
                        x.append(self._emoji_template[6])
                    if index == 7:
                        x.append(self._emoji_template[7])
                    if index == 8:
                        x.append(self._emoji_template[8])
            
            ##############################################################################################
            
            ## ==> WAIT FOR PLAYER TO REACT
            ##############################################################################################
            
            try: await self.bot.wait_for("reaction_add", timeout=25.0, check=check)
            except asyncio.TimeoutError:
                await message.edit(embed=discord.Embed(color=discord.Color.green(), title=f"Game Between {ctx.author.name} and {p2.name}", description=f"{ctx.author.name if _turn == p2 else p2.name} has won the game since {p2.name if _turn == p2 else ctx.author.name} didn't respond in time!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
                
            ##############################################################################################
            
            ## ==> CHECK IF REACTION WAS VALID OR NOT
            ##############################################################################################
            
            if self.data[f"{ctx.author.id} & {p2.id}"]["CUR_REACTION"] not in x:
                await message.remove_reaction(self.data[f"{ctx.author.id} & {p2.id}"]["CUR_REACTION"], _turn)
                continue
            
            ##############################################################################################
            
            ## ==> PUT THE MARK ON THE BOARD
            ##############################################################################################
            
            index = f"{ctx.author.id} & {p2.id}"
                
            mark = ":x:" if _turn == ctx.author else ":o:"
                
            if self.data[index]["CUR_REACTION"] == self._emoji_template[0]:
                _current_board[0] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[1]:
                _current_board[1] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[2]:
                _current_board[2] = f"{mark}\n"
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[3]:
                _current_board[3] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[4]:
                _current_board[4] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[5]:
                _current_board[5] = f"{mark}\n"
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[6]:
                _current_board[6] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[7]:
                _current_board[7] = mark
            elif self.data[index]["CUR_REACTION"] == self._emoji_template[8]:
                _current_board[8] = mark
            
            ##############################################################################################
            
            ## ==> CHECK FOR WINNER
            ##############################################################################################
            
            if (_current_board[0], _current_board[1], _current_board[2]) == (":x:", ":x:", ":x:\n") or (_current_board[0], _current_board[1], _current_board[2]) == (":o:", ":o:", ":o:\n"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[3], _current_board[4], _current_board[5]) == (":x:", ":x:", ":x:\n") or (_current_board[3], _current_board[4], _current_board[5]) == (":o:", ":o:", ":o:\n"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[6], _current_board[7], _current_board[8]) == (":x:", ":x:", ":x:") or (_current_board[6], _current_board[7], _current_board[8]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[0], _current_board[3], _current_board[6]) == (":x:", ":x:", ":x:") or (_current_board[0], _current_board[3], _current_board[6]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[1], _current_board[4], _current_board[7]) == (":x:", ":x:", ":x:") or (_current_board[1], _current_board[4], _current_board[7]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[2], _current_board[5], _current_board[8]) == (":x:\n", ":x:\n", ":x:") or (_current_board[2], _current_board[5], _current_board[8]) == (":o:\n", ":o:\n", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[0], _current_board[4], _current_board[8]) == (":x:", ":x:", ":x:") or (_current_board[0], _current_board[4], _current_board[8]) == (":o:", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            elif (_current_board[2], _current_board[4], _current_board[6]) == (":x:\n", ":x:", ":x:") or (_current_board[2], _current_board[4], _current_board[6]) == (":o:\n", ":o:", ":o:"): 
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description=f"{_turn} has won the Game!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            
            ##############################################################################################
            
            ## ==> CHANGE THE TURN TO THE OTHER PLAYER
            ##############################################################################################
            
            _turn = p2 if _turn == ctx.author else ctx.author
            
            ##############################################################################################            
            
            ## ==> RESET X FOR THE BOT TO REACT TO THE EMBED
            ##############################################################################################
            
            x = []
            for index, item in enumerate(_current_board):
                if item == ":white_large_square:" or item == ":white_large_square:\n":
                    if index == 0:
                        x.append(self._emoji_template[0])
                    if index == 1:
                        x.append(self._emoji_template[1])
                    if index == 2:
                        x.append(self._emoji_template[2])
                    if index == 3:
                        x.append(self._emoji_template[3])
                    if index == 4:
                        x.append(self._emoji_template[4])
                    if index == 5:
                        x.append(self._emoji_template[5])
                    if index == 6:
                        x.append(self._emoji_template[6])
                    if index == 7:
                        x.append(self._emoji_template[7])
                    if index == 8:
                        x.append(self._emoji_template[8])
            
            ##############################################################################################
            
            ## ==> UPDATE THE EMBED
            ##############################################################################################
            
            embed = discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=ctx.author.color, description="".join(_current_board))
            embed.set_footer(text=f"{_turn.name}'s Turn")
            await message.edit(embed=embed)
            await message.clear_reactions()
            for i in x: await message.add_reaction(i)
            del x
            
            ##############################################################################################
            
            ## ==> UPDATE TURN NUMBER
            ##############################################################################################
            
            # IF TURN NUMBER = 9, GAME IS OVER
            
            if self.data[f"{ctx.author.id} & {p2.id}"]["TURN_NO"] == 9:
                await message.clear_reactions()
                await message.edit(embed=discord.Embed(title=f"Game Between {ctx.author.name} and {p2.name}", color=discord.Color.green(), description="Game Draw!"))
                del self.data[f"{ctx.author.id} & {p2.id}"]
                break
            
            self.data[f"{ctx.author.id} & {p2.id}"]["TURN_NO"] += 1
            
            ##############################################################################################
        
        await ctx.send(f"Final Board:\n{''.join(_current_board)}")    
        
        ##############################################################################################

def setup(bot:commands.Bot):
    bot.add_cog(TicTacToe(bot))
