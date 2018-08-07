from frmcLib import *


data_search = search("iron sword")
url = search_links(data_search,Type="Item")
print("URLs:",url)
data_item = url_to_data(url[0])
iron_sword = search_item(data=data_item)
print("\n-- Iron sword --")
for k,v in iron_sword.__dict__.items():
	print(k,":",v)

print("")

data_search = search("stonebrick")
url = search_links(data_search,Type="Bloc")
print("URLs:",url)
iron_sword = search_item(url=url[0])
print("\n-- Stone brick --")
for k,v in iron_sword.__dict__.items():
	print(k,":",v)
