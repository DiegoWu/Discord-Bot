# 檔名：guess.py
# 功能：猜數字

#################################################################
# TODO: 實作猜數字
# 分類: 作業 (10 pts)
# HINT: 認真上課
#################################################################
import discord
from discord.ext import commands
import random
class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        help = 
            "guess number",
        brief = "for fun"
    )
    async def guess(self, ctx):
        await ctx.send("guess four digits, and do not try 0 ")
        ans= "".join(random.sample("123456789", 4))
        def valid(m):
            return m.author== ctx.author
        for _ in range(100):
            guess= await self.bot.wait_for('message', check= valid, timeout= 300.0)
            if guess.content== "i give up":
                await ctx.send(f"the answer is {ans}")
                return 
            a= sum (1 for i in range(4) if guess.content[i]== ans[i] )
            b= sum(1 for i in range(4) if guess.content[i] in ans ) -a
            if guess.content == ans:
                await ctx.send("you are correct!!!")
                return 
            else:
                await ctx.send(f"{a}A{b}B")
        await ctx.send("why am i so weak?")
def setup(bot):
    bot.add_cog(Guess(bot))