import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class xbps:
    """Search for packages in the Void Repos"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def xbps(self, ctx, searchterm, arch="x86_64"):
        r = requests.get("https://repo.voidlinux.eu/current/")
        soup = BeautifulSoup(r.text, 'html.parser')

        results_limit = 10
        archlist = ["x86_64", "i686", "armv6l", "armv7l", "noarch"]
        if arch not in archlist:
            arch="x86_64"
        results = []

        for link in soup.find_all('a'):
            if ".sig" not in link.contents[0]:
                if searchterm.lower() in link.contents[0].lower() and (arch in link.contents[0].lower() or "noarch" in link.contents[0].lower()):
                    if len(results) <= results_limit:
                        results.append("[" + link.contents[0][: -5] + "]" +
                            "(https://github.com/voidlinux/void-packages/tree/master/srcpkgs/" +
                            '-'.join(link.contents[0][: -5].split('-')[: -1]) + ")")
                    else:
                        break
        if len(results) == 0:
            results.append("No results found.")
        results.append("―――――――――――\n[Search on github](https://github.com/voidlinux/void-packages/search?q%5B%5D=filename%3Atemplate+path%3A%2Fsrcpkgs&q%5B%5D="+
                searchterm + 
                "&s=indexed)")
        em = discord.Embed(title='Void Repo Search', description='\n'.join(results), colour=0x478061)
    await self.bot.send_message(ctx.message.channel,embed=em)

def setup(bot):
    bot.add_cog(xbps(bot))
