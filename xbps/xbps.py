import discord
from discord.ext import commands
import requests
import requests_cache
import re

requests_cache.install_cache()

class xbps:
    """Search for packages in the Void Repos"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def xbps(self, ctx, searchterm, arch="x86_64"):
        results_limit = 10
        archlist = ["x86_64", "i686", "armv6l", "armv7l", "noarch"]

        arch = arch.lower()

        if arch not in archlist:
            arch="x86_64"

        r = requests.get("https://xbps.spiff.io/v1/query/{}?q={}".format(archlist, searchterm))
        links = ""
        for package in r.json().["data"]:
            print(package)
            if len(links) <= results_limit:
                links.append("[" + package["name"] + package["version"] + "_" + packge["revision"] +"]" +
                               "(https://github.com/voidlinux/void-packages/tree/master/srcpkgs/"
                               + package["name"] + ")")
            else:
                break
        if len(results) == 0:
            links.append("No results found.")
        links.append("―――――――――――\n[Search on github](https://github.com/voidlinux/void-packages/search?q%5B%5D=filename%3Atemplate+path%3A%2Fsrcpkgs&q%5B%5D="+
                searchterm + 
                "&s=indexed)")
        em = discord.Embed(title='Void Repo Search', description='\n'.join(links), colour=0x478061)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(xbps(bot))


