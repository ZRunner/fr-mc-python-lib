from frmcLib import *


data = search("slime")
url = search_links(data,Type="Entité")
print("URL:",url)
slime = search_entity(url=url[0])
print("\n-- Slime --")
for k,v in slime.__dict__.items():
	print(k,":",v)
