import discord
from redbot.core import commands
import requests
import re
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

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

        print(searchterm)
        urlterm = searchterm.replace(' ', '+')
        r = requests.get("http://steinscraft.net:8197/v1/query/{}?q={}".format(arch, urlterm))
        links = []
        length = 0
        embeds = []


        if len(r.json()["data"]) == 0:
            em = discord.Embed(title='Void Repo Search: ' + searchterm , url="https://github.com/void-linux/void-packages/search?q%5B%5D=filename%3Atemplate+path%3A%2Fsrcpkgs&q%5B%5D=" + urlterm + "&s=indexed)", description='No packages found', colour=0x478061)
            em.set_footer(text="Search results from https://xbps.spiff.io", icon_url="https://voidlinux.org/assets/img/void_bg.png")
            await ctx.send(embed=em)

        else:
            for package in r.json()["data"]:
                packageString =("[" + package["name"] + " " + str(package["version"]) + "_" + str(package["revision"]) +"]" +
                                "(https://github.com/void-linux/void-packages/tree/master/srcpkgs/"
                                + package["name"] + ") - " + package["desc"])

                if len(packageString) + length < 2000:
                    links.append(packageString)
                    length += len(packageString)
                else:
                    em = discord.Embed(title='Void Repo Search: ' + searchterm , url="https://github.com/void-linux/void-packages/search?q%5B%5D=filename%3Atemplate+path%3A%2Fsrcpkgs&q%5B%5D=" + urlterm + "&s=indexed)" ,description='\n'.join(links), colour=0x478061)
                    em.set_footer(text="Search results from https://xbps.spiff.io", icon_url="https://voidlinux.org/assets/img/void_bg.png")
                    embeds.append(em)
                    links = []
                    links.append(packageString)
                    length = len(packageString)
            em = discord.Embed(title='Void Repo Search: ' + searchterm , url="https://github.com/void-linux/void-packages/search?q%5B%5D=filename%3Atemplate+path%3A%2Fsrcpkgs&q%5B%5D=" + urlterm + "&s=indexed)" ,description='\n'.join(links), colour=0x478061)
            em.set_footer(text="Search results from https://xbps.spiff.io", icon_url="https://voidlinux.org/assets/img/void_bg.png")
            embeds.append(em)
            if len(embeds) > 1:
                await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS)
            else:
                await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(xbps(bot))


