
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

class ItemNotFound(Error):
    """Raised when an item can't be found"""
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
    def __init__(self,Name="",ID="",Type="",PV=0,PA=0,XP=0,Biomes=[],Dimensions=[0,0,0],Version="0.0",Img="",url=""):
        self.Name = Name  #Name of the entity
        self.ID = ID  #Text id
        self.Type=Type  #Type of the entity
        self.PV = PV  #Health points
        self.PA = PA  #Attack points
        self.XP = XP  #HP droped
        self.Biomes = Biomes  #Favorites biomes
        self.Dimensions = Dimensions  #Dimensions (width, length, height)
        self.Version = Version  #Game version when adding
        self.Img = Img  #Image link
        self.Url = url  #Url of the entity page

class Item():
    """This class represent an item or a block. Some information can be empty depending on the type of item (weapon, block...)"""
    def __init__(self,Name="",ID="",Stack=0,Tab=None,Damage=0,Strength=0,Tool="",Version="0.0",Mobs=[]):
        self.Name = Name  #Name of the item
        self.ID = ID  #Text id
        self.Stack = Stack  #Size of a stack
        self.CreativeTab = Tab  #Tab in creative gamemode
        self.Damage = Damage  #>eapon damage
        self.Strength = Strength  #Durability
        self.Tool = Tool  #Tool able to destroy it
        self.Version = Version  #Game version when adding
        self.Mobs = Mobs  #List of mobs that can drop this item



#----- Useful functions -----#
def main(name,Type):
    """General function that allows to generate an object from a simple search.

Parameters:
- name (str): the name of the item to search for
- Type (str): the type of item (Entité, Bloc, Item, etc.)

Return:
Object of type Entity(), Item(), or other"""
    data = search(name)
    urls = search_links(data,Type)
    if len(urls) == 0:
        raise ItemNotFound("This item can't be found: {} (Type: {})".format(name,Type))
    item = search_item(url=urls[0])
    return item

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
- Type (str): the type of item sought (Entité, Bloc, Item, Potion, Enchant, Progress, Effect, Success, Command), insensitive case
- limit (int): the maximum number of links to return

Return: 
List of matching links"""
    if type(code) != str or type(Type) != str or type(limit) != int:
        raise TypeError("One of these arguments is not in the right type")
    if Type.lower() not in ["entité","bloc", "item", "potion", "enchant", "progrès", "effet", "succès", "commande"]:
        raise ValueError("The given type is not valid : {}".format(Type))
    matches = re.findall(r"<td class='id'><a[^>]+>([^<]+)",code)
    links = re.findall(r"<a href=\"([^\"]+)\"  class=\"content_link \">Voir la fiche complète</a>",code)
    results1 = list()
    results2 = list()
    if Type==None:
        return links
    else:
        for e,m in enumerate(matches):
            if m.lower() == Type.lower() and len(results1)<limit:
                results1.append("https://fr-minecraft.net/"+links[e])
    for i in results1:
        if not i in results2:
            results2.append(i)
    return results2



#----- Entity infos -----#
def search_entity(data=None,url=None):
    """Function that retrieves all information about an entity from the html code of its page, and creates an Entity() object.

Parameters : 
- data (str): source code of the page, in html (useless if you fill url)
- url (str): url of the page (useless if you enter data)

Return:
Object of type Entity()"""
    if type(data) not in [str,None] and type(url) not in [str,None]:
        raise TypeError("data and url must be string or None")
    if data == url == None:
        raise ValueError("data and url cannot be empty at the same time")
    if url != None and data == None:
        data = url_to_data(url)
    PVs = 0
    PAs = 0
    #-- Image --#
    try:
        img = "http://fr-minecraft.net/"+re.search(r"<img src=\"([^\"]+)\" class=\"img\" alt=[^>]+>",data).group(1)
    except AttributeError:
        img =  ""
        pass
    #-- PV/PA --#
    matches = re.finditer(r"<u>(.+)</u>(?:[^>]+)><img[^>]+title=\"([^\"]+)",data,re.MULTILINE)
    if matches != None:
        for match in matches:
            if match.group(1)=="Points de vie :":
                PVs = match.group(2)
            elif match.group(1)=="Points d'attaque :":
                PAs = match.group(2)
    #-- ID --#
    IDs = list()
    try:
        for matchNum,match in enumerate(re.finditer(r"<p class=\"identifiant\"><b>([^<]+)</b>([^<]+)",data,re.MULTILINE)):
            IDs.append(match.group(1)+" "+match.group(2))
    except AttributeError:
        pass
    #-- Type --#
    try:
        Type = re.search(r"<u>Type :</u> <span style=\"color: red;\">([^<]+)</span>",data).group(1)
    except AttributeError:
        Type = "Inconnu"
        pass
    #-- Dropped xp --#
    try:
        XPs = re.search(r"<u>Experience :</u> <img [^>]+> (\d)<br/>",data).group(1)
    except AttributeError:
        XPs = 0
        pass
    #-- Biomes --#
    Bioms = list()
    for matchNum,match in enumerate(re.finditer(r"<li><img [^>]+ /> <a [^>]+>([^<]+)</a>",data)):
        Bioms.append(match.group(1))
    #-- Dimensions --#
    Dimensions = [0,0,0]
    try:
        r = re.search(r"<div class=\"dimensions\"><[^>]+>Dimensions :</span> <br/>\s*<ul>\s*<li>[^<\d]+([\d|.]+)</li>\s*<li>[^<\d]+([\d|.]+)</li>\s*<li>[^<\d]+([\d|.]+)",data)
        Dimensions = list()
        for group in r.groups():
            Dimensions.append(float(group))
    except AttributeError:
        pass
    if len(Dimensions)<3:
        Dimensions = [0,0,0]
    #-- Version --#
    try:
        Vs = re.search(r"<div class=\"version\">[^<]+<br/><[^>]+>([^<]+)</a>",data).group(1)
    except AttributeError:
        Vs ="Introuvable"
    #-- Name --#
    Names = re.search(r"<h3>(.+)<span>",data,re.MULTILINE)
    if Names != None:
        Names = Names.group(1)
    else:
        Names = "Inconnu"
    #-- Final entity --#
    En = Entity(Name=Names,ID="\n".join(IDs),Type=Type,PV=PVs,PA=PAs,XP=XPs,Biomes=Bioms,Dimensions=Dimensions,Version=Vs,Img=img)
    if url != None:
        En.Url = url
    return En



#----- Bloc/item infos -----#
def search_item(data=None,url=None):
    """Function that retrieves all information about an item from the html code of its page, and creates an Item() object.

Parameters : 
- data (str): source code of the page, in html (useless if you fill url)
- url (str): url of the page (useless if you enter data)

Return:
Object of type Item()"""
    if type(data) not in [str,None] and type(url) not in [str,None]:
        raise TypeError("data and url must be string or None")
    if data == url == None:
        raise ValueError("data and url cannot be empty at the same time")
    if url != None and data == None:
        data = url_to_data(url)
    #-- Name --#
    Names = re.search(r"<div class=\"popnom\">([^<]+)<br /> <em>[^<]+</em></div>",data,re.MULTILINE)
    if Names != None:
        Names = Names.group(1)
    else:
        Names = "Inconnu"
    #-- ID --#
    IDs = list()
    try:
        for matchNum,match in enumerate(re.finditer(r"<p class=\"identifiant\"><b>([^<]+)</b>([^<]+)",data,re.MULTILINE)):
            IDs.append(match.group(1)+" "+match.group(2))
    except AttributeError:
        pass
    #-- Stack --#
    Stacks = re.search(r"<p>Stackable par (\d+) </p></div>",data,re.MULTILINE)
    if Stacks != None:
        Stacks = Stacks.group(1)
    else:
        Stacks = 0
    #-- Tab --#
    Tabs = re.search(r"</span> ([^<]+)</p>",data,re.MULTILINE)
    if Tabs != None:
        Tabs = Tabs.group(1)
    else:
        Tabs = None
    #-- Damage --#
    Dmgs = re.search(r"Cette arme inflige des dégats: <span class=\"healthbar\"><img src=\"[^\"]+\" style=\"[^\"]+\" alt=\"([\d.]+) [^>]+>",data,re.MULTILINE)
    if Dmgs != None:
        Dmgs = Dmgs.group(1)
    else:
        Dmgs = None
    #-- Strength --#
    Strs = re.search(r"<p>Solidité : Cet objet est utilisable <strong style=\"color: green;\">([\d]+)</strong> fois.</p>",data,re.MULTILINE)
    if Strs != None:
        Strs = Strs.group(1)
    else:
        Strs = None
    #-- Tool --#
    Tools = re.search(r"<a rel=\"popup\" href=\"[^\"]+\" onclick=\"[^\"]+\"  class=\"content_popup_link \">([^>]+)</a></span><br/>",data,re.MULTILINE)
    if Tools != None:
        Tools = Tools.group(1)
    else:
        Tools = None
    #-- Version --#
    try:
        Vs = re.search(r"<div class=\"version\">[^<]+<br/><[^>]+>([^<]+)</a>",data).group(1)
    except AttributeError:
        Vs ="Introuvable"
    #-- Mobs --#
    Mobs = list()
    try:
        for match in re.finditer(r"<img src=\"img/creatures/small/[^\"]+\" alt=\"([^\"]+)\" />",data,re.MULTILINE):
            if not match.group(1) in Mobs:
                Mobs.append(match.group(1))
    except AttributeError:
        pass
    #-- Final entity --#
    Bl = Item(Name=Names,ID=IDs,Stack=Stacks,Tab=Tabs,Damage=Dmgs,Strength=Strs,Tool=Tools,Version=Vs,Mobs=Mobs)
    if url != None:
        Bl.Url = url
    return Bl



#----- Command infos -----#


#----- Init -----#
data = search("sword")
