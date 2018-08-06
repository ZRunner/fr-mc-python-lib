
#Here are the libraries used by the code:
libs = ["requests","re"]


#----- Errors management -----#
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MissingLibError(Error):
    """Raised when a library is missing"""
    def __init__(self,message):
        self.message = message



#----- Import libraries -----#
not_loaded_modules = list()
for m in libs:
    try:
        exec("import "+m)
    except ModuleNotFoundError:
        print("The {} module has not been installed on your computer".format(m))
        not_loaded_modules.append(m)
if len(not_loaded_modules)>=1:
    raise MissingLibError("{} missing module(s)".format(len(not_loaded_modules)))



#----- Classes -----#
class Entity():
    """This class represents an entity, and all information about it"""
    def __init__(self,Name="",ID="",Type="",PV=0,PA=0,XP=0,Biomes=[],Dimensions=[0,0,0],Version="1.0",Img="",url=""):
        self.Name = Name  #name of the entity
        self.ID = ID  #text id
        self.Type=Type  #type of the entity
        self.PV = PV  #health points
        self.PA = PA  #attack points
        self.XP = XP  #xp droped
        self.Biomes = Biomes  #favorites biomes
        self.Dimensions = Dimensions  #dimensions (width, length, height)
        self.Version = Version  #game version when adding
        self.Img = Img  #image link
        self.Url = url  #url of the entity page



#----- Useful functions -----#
def url_to_data(url):
    """Returns the html string of a site from its url.

Parameters:
- url (str): the url of the page

Return:
the html string of the page
"""
    if type(url) != str:
        raise TypeError("url must be a string")
    try:
        data = requests.get(url,timeout=5).text
    except UnicodeDecodeError:
        data = requests.get(url).content.decode("utf-8")
    except Exception as exc:
        print("Error while converting the url \"{}\" to data:".format(url))
        raise exc
    return data



#----- Searching functions -----#
def search(item):
    """Returns the search page html from the item searched for.

Parameters:
- item (str): the name of the item to search. 

Return:
The url, in string"""
    if type(item) != str:
        raise TypeError("item must be a string")
    p = "http://fr-minecraft.net/recherche.php?search="+"+".join(item.split(" "))
    p = url_to_data(p)
    return p

def search_links(code,Type=None,limit=1):
    """Search for links from the search page code and return the corresponding links.

Parameters: 
- code (str): the html string of the search page
- Type (str): the type of item sought (Entity, Block, Item, Potion, Enchant, Progress, Effect, Success, Command), insensitive case
- limit (int): the maximum number of links to return

Return: 
List of matching links"""
    if type(code) != str or type(Type) != str or type(limit) != int:
        raise TypeError("One of these arguments is not in the right type")
    matches = re.findall(r"<td class='id'><a[^>]+>([^<]+)",code)
    links = re.findall(r"<a href=\"([^\"]+)\"  class=\"content_link \">Voir la fiche complète</a>",code)
    results1 = list()
    results2 = list()
    if Type==None:
        return links
    else:
        for e,m in enumerate(matches):
            if m.lower() == Type.lower() and len(results1)<limit:
                results1.append(links[e])
    for i in results1:
        if not i in results2:
            results2.append(i)
    return results2



#----- Entity infos -----#
#----- Bloc/item infos -----#
#----- Command infos -----#


#----- Init -----#
data = search("sword")
