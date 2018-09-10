import requests
arch = ""
searchterm = "firefox"
archlist = ["x86_64", "i686", "armv6l", "armv7l", "noarch"]

arch = arch.lower()

results_limit = 10

if arch not in archlist:
        arch="x86_64"

r = requests.get("https://xbps.spiff.io/v1/query/{}?q={}".format(arch, searchterm))
links = []

print(r.text)

for package in r.json()["data"]:
    if len(links) <= results_limit:
        links.append("[{}](https://github.com/voidlinux/void-packages/tree/master/srcpkgs/{}) {}_{}".format(package["name"],package["name"],package["version"],package["revision"]))
    else:
        break

if len(links) == 0:
        links.append("No results found.")

links.append("―――――――――――\n[Search on github](https://github.com/voidlinux/void-packages/search?q%5B%5D=filename%3Atemplate+path%3A%2Fsrcpkgs&q%5B%5D="+
        searchterm +
        "&s=indexed)")

print(links)
