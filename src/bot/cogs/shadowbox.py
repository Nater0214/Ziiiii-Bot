# src/bot/cogs/shadowbox.py
# A cog for shadowboxing


# Imports
from os import getenv

from discord import ApplicationContext, ButtonStyle, Interaction, Member, Option, SlashCommandGroup, ui
from discord.ext.commands import Cog


# Definitions
class Shadowbox(Cog):
    """Shadowbox commands"""
    
    # Command group
    command_group = SlashCommandGroup("shadowbox", "Commands for shadowboxing", guild_ids=[getenv("GUILD_ID")], guild_only=True)
    
    
    # Views
    class GameView(ui.View):
        """View for starting a shadowbox game"""
        
        # Init
        def __init__(self, challenger: Member, opponent: Member):
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Add buttons
            self.up_button = ui.Button(label="⬆️", style=ButtonStyle.gray)
            self.down_button = ui.Button(label="⬇️", style=ButtonStyle.gray)
            self.left_button = ui.Button(label="➡️", style=ButtonStyle.gray)
            self.right_button = ui.Button(label="⬅️", style=ButtonStyle.gray)
            
            self.up_button.callback = self.up
            self.down_button.callback = self.down
            self.left_button.callback = self.left
            self.right_button.callback = self.right
            
            self.add_item(self.up_button)
            self.add_item(self.down_button)
            self.add_item(self.left_button)
            self.add_item(self.right_button)
            
            # Set challenger
            self.challenger = challenger
            
            # Set opponent
            self.opponent = opponent
            
            # Setup game
            self.boxing = challenger
            self.score = 0
            
            self.challenger_move = None
            self.opponent_move = None
        
        
        # Button methods
        async def up(self, interaction: Interaction):
            """User played up"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = "up"
            elif interaction.user == self.opponent:
                self.opponent_move = "up"
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game goofy")
                return
            
            await self.scoring(interaction)
        
        
        async def down(self, interaction: Interaction):
            """User played down"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = "down"
            elif interaction.user == self.opponent:
                self.opponent_move = "down"
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game goofy")
                return
            
            await self.scoring(interaction)
        
        
        async def left(self, interaction: Interaction):
            """User played left"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = "left"
            elif interaction.user == self.opponent:
                self.opponent_move = "left"
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game goofy")
                return
            
            await self.scoring(interaction)
        
        
        async def right(self, interaction: Interaction):
            """User played right"""
            
            # Set player move
            if interaction.user == self.challenger:
                self.challenger_move = "right"
            elif interaction.user == self.opponent:
                self.opponent_move = "right"
            else:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You aren't in this game goofy")
                return
            
            await self.scoring(interaction)
        
        
        # Methods
        async def scoring(self, interaction: Interaction) -> None:
            """Do scoring"""
            
            # Check if both players have made a move
            if self.challenger_move is None or self.opponent_move is None:
                pass
            
            else:
                # Check if moves are the same
                if self.challenger_move == self.opponent_move:
                    # Change score accordingly
                    if self.boxing == self.challenger:
                        self.score -= 1
                    elif self.boxing == self.opponent:
                        self.score += 1
                    
                    # Disable button
                    if self.challenger_move == "up":
                        self.up_button.disabled = True
                    elif self.challenger_move == "down":
                        self.down_button.disabled = True
                    elif self.challenger_move == "left":
                        self.left_button.disabled = True
                    elif self.challenger_move == "right":
                        self.right_button.disabled = True
                else:
                    # Set score to 0
                    self.score = 0
                    
                    # Enable all buttons
                    self.up_button.disabled = False
                    self.down_button.disabled = False
                    self.left_button.disabled = False
                    self.right_button.disabled = False
                    
                    # Set other player to boxing
                    if self.boxing == self.challenger:
                        self.boxing = self.opponent
                    elif self.boxing == self.opponent:
                        self.boxing = self.challenger
                
                # Reset player moves
                self.challenger_move = None
                self.opponent_move = None
            
            await interaction.response.edit_message(content=f"{'⬛' if self.challenger_move is None else '🟨'}{'🥊' if self.boxing == self.challenger else '💨'}{self.challenger.mention} {'🟩' if self.score <= -3 else '⬛'}{'🟩' if self.score <= -2 else '⬛'}{'🟩' if self.score <= -1 else '⬛'}⏹{'🟩' if self.score >= 1 else '⬛'}{'🟩' if self.score >= 2 else '⬛'}{'🟩' if self.score >= 3 else '⬛'} {self.opponent.mention}{'🥊' if self.boxing == self.opponent else '💨'}{'⬛' if self.opponent_move is None else '🟨'}", view=self)
            if self.score == -3:
                await interaction.response.edit_message(content=f"{interaction.message.content}\n{self.challenger.mention} won 🏆", view=None)
            elif self.score == 3:
                await interaction.response.edit_message(content=f"{interaction.message.content}\n{self.opponent.mention} won 🏆", view=None)
    
    
    class AcceptView(ui.View):
        """View for accepting a challenge"""
        
        # Init
        def __init__(self, cog: Cog, challenger: Member, opponent: Member):
            """Init"""
            
            # Run super init
            super().__init__()
            
            # Set cog
            self.cog = cog
            
            # Set challenger
            self.challenger = challenger
            
            # Set opponent
            self.opponent = opponent
        
        
        # Buttons
        @ui.button(label="Accept", style=ButtonStyle.green)
        async def accept(self, button: ui.Button, interaction: Interaction):
            """Accept the challenge"""
            
            # Make sure the button was clicked by the challenged user
            if interaction.user != self.opponent:
                await interaction.user.send(f"{interaction.message.jump_url}\n>>>You weren't the one challenged goofy")
                return
            
            await interaction.response.edit_message(content=f"⬛🥊{self.challenger.mention} ⬛⬛⬛⏹️⬛⬛⬛ {self.opponent.mention}💨⬛", view=self.cog.GameView(self.challenger, self.opponent))
        
        
        @ui.button(label="Decline", style=ButtonStyle.red)
        async def decline(self, button: ui.Button, interaction: Interaction):
            """Decline the challenge"""
            
            # Make sure the button was clicked by the challenged user
            if interaction.user != self.opponent:
                await interaction.user.send(f"{interaction.message.jump_url}\n↘>>>You weren't the one challenged goofy")
                return
            
            await interaction.response.edit_message(content="Yikes", view=None)
    
    
    # Commands
    @command_group.command()
    async def challenge(self, ctx: ApplicationContext, user: Option(Member)):
        """Challenge someone to a shadowbox game"""
        
        if ctx.author.id != 721422610164088832:
            if ctx.author == user:
                await ctx.response.send_message("You can't challenge yourself")
                return
        
        await ctx.response.send_message(f"{ctx.author.mention} challenged {user.mention} to a shadowbox game", view=self.AcceptView(self, ctx.author, user))