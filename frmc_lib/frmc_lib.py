
#Here are the libraries used by the code:
libs = ["requests","regex"]



#----- Some useful data -----#
regex_version = r'<div class=\"version\">[^<]+<br/>\s*<[^>]+>\s*([^<\n\r]+)\s*</a>'
timeout = 5



#----- Errors management -----#
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MissingLibError(Error):
    """Raised when a library is missing"""
    def __init__(self,message):
        self.message = message

class ItemNotFoundError(Error):
    """Raised when an item can't be found"""
    def __init__(self,message):
        self.message = message
        
class WrongDataError(Error):
    """Raised when there is an error during parsing data"""
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
    """This class represents an entity, and all information about it.

Here is a list of all variables accessible after creation:

.. hlist::
   :columns: 2

   * Name
   * ID
   * Type
   * PV
   * PA
   * XP
   * Biomes
   * Dimensions
   * Version
   * Image
   * Url
   
Parameters
----------
    diverses All information that will be stored in the class

.. tip:: Details on each of the information are given in comments in the source code
"""
    def __init__(self,Name,ID,Type,PV,PA,XP,Biomes,Dimensions,Version,Img,url=""):
        self.Name = Name  #Name of the entity
        self.ID = ID  #Text id
        self.Type = Type  #Type of the entity
        self.PV = PV  #Health points
        self.PA = PA  #Attack points
        self.XP = XP  #HP droped
        self.Biomes = Biomes  #Favorites biomes
        self.Dimensions = Dimensions  #Dimensions (width, length, height)
        self.Version = Version  #Game version when adding
        self.Image = Img  #Image link
        self.Url = url  #Url of the entity page

class Item():
    """This class represent an item or a block. Some information can be empty depending on the type of item (weapon, block...).

Here is a list of all variables accessible after creation:

.. hlist::
   :columns: 2

   * Name
   * ID
   * Stack
   * CreativeTab
   * Damage
   * Strength
   * Tool
   * Version
   * Mobs
   * Image
   * Url
   
Parameters
----------
    diverses All information that will be stored in the class

.. tip:: Details on each of the information are given in comments in the source code"""
    def __init__(self,Name,ID,Stack,Tab,Damage,Strength,Tool,Version,Mobs,Image,Url=""):
        self.Name = Name  #Name of the item
        self.ID = ID  #Text id
        self.Stack = Stack  #Size of a stack
        self.CreativeTab = Tab  #Tab in creative gamemode
        self.Damage = Damage  #Weapon damage
        self.Strength = Strength  #Durability
        self.Tool = Tool  #Tool able to destroy it
        self.Version = Version  #Game version when adding
        self.Mobs = Mobs  #List of mobs that can drop this item
        self.Image = Image  #Url of an image
        self.Url = Url  #Url of the item page

class Command():
    """This class represent a command (sometimes also called *cheat*).

Here is a very long list of the immensity of the hundreds of information accessible after creation (yes there are only 4, it's not a bug)

.. hlist::
   :columns: 1

   * Name
   * Syntax
   * Examples
   * Version
   
Parameters
----------
    diverses All information that will be stored in the class

.. tip:: Details on each of the information are given in comments in the source code"""
    def __init__(self,Name,Syntax,Ex,Version,Url):
        self.Name = Name  #Name of the command
        self.Syntax = Syntax  #List of parameters, sorted in order of use
        self.Examples = Ex  #List of some examples, contained in tuples in the form (syntax, explanation)
        self.Version = Version  #Game version when adding
        self.Url = Url  #Url of the command page

class Advancement():
    """This class represents an advancement, the event that replaces achievements since Minecraft Java Edition 1.12.

Here is the list of information that can be obtained after creating the object:

.. hlist::
    :columns: 1

    * Name
    * ID
    * Type
    * Action
    * Parent
    * Children
    * Version
    * Url

Parameters
----------
    diverses All information that will be stored in the class

.. tip:: Details on each of the information are given in comments in the source code
"""
    def __init__(self,Name,ID,Type,Action,Parent,Children,Version,Url=""):
        self.Name = Name  #Name of the advancement
        self.ID = ID  #Text identifier
        self.Type = Type  #Type of the advancement (Progrès/Objectif)
        self.Action = Action  #description of the advancement (fr)
        self.Parent = Parent  #Previous advancement in the Tree structure
        self.Children = Children  #List of next advancement(s) in the Tree structure
        self.Version = Version  #Game version when adding
        self.Url = Url  #Url of the advancement page



#----- Useful functions -----#
def main(name,Type):
    """The main function shortens the information acquisition method. It allows to generate an object from a simple word \
and a type, without having to execute all the sub-functions. This is probably the function you will use most often for \
standard library use.

Parameters
----------
name: :class:`str`
    The name of the item to search for
Type: :class:`str`
    The type of item (Entité, Bloc, Item, etc.)

Return
------
    diverses
        Object of type Entity(), Item() or other, depending on the Type given in parameters

Raises
------
    :class:`~frmc_lib.ItemNotFoundError`
        The type of the given item is not available yet, or the given item can't be found
"""
    data = search(name)
    urls = search_links(data,Type)
    if len(urls) == 0:
        raise ItemNotFoundError("This item can't be found: {} (Type: {})".format(name,Type))
    if Type.lower() in ["bloc","item"]:
        item = search_item(url=urls[0])
    elif Type.lower() == "entité":
        item = search_entity(url=urls[0])
    elif Type.lower() == "commande":
        item = search_cmd(url=urls[0])
    elif Type.lower() == "progrès":
        item = search_adv(url=urls[0])
    else:
        raise ItemNotFoundError("The type of this item is not available (Given type: {})".format(Type))
    return item

def url_to_data(url):
    """This function allows you to retrieve the source code of a web page, from its url address. \
You just have to give the url as parameter to receive a string containing the html code. 

Parameters
----------
url: :class:`str`
    The url of the page

Return
------
    :class:`str`
        The html string of the page

Raises
------
    :class:`TypeError`
        The url must be a string.
"""
    if type(url) != str:
        raise TypeError("url must be a string")
    try:
        data = requests.get(url,timeout=timeout).text
    except UnicodeDecodeError:
        data = requests.get(url,timeout=timeout).content.decode("utf-8")
    except Exception as exc:
        print("Error while converting the url \"{}\" to data:".format(url))
        raise exc
    return data



#----- Searching functions -----#
def search(item):
    """This function returns the source code of the search page, initialized with a string containing the query. 

Parameters
----------
item: :class:`str`
    The name of the item to search. 

Return
------
    :class:`str`
        The url, in string

Raises
------
    :class:`TypeError`
        The given item must be a string
    """
    if type(item) != str:
        raise TypeError("item must be a string")
    p = "http://fr-minecraft.net/recherche.php?search="+"+".join(item.split(" "))
    p = url_to_data(p)
    return p

def search_links(code,Type=None,limit=1):
    """This function allows you to find a certain number of links to item records from the \
html code of the search page. For example if you want to get the url addresses \
of all the swords, you have to give in arguments the code of the page \
https://fr-minecraft.net/recherche.php?search=sword and "Item" in type. 
You can get several links by changing the value of the limit argument (1 by default)

Parameters
----------
code: :class:`str`
    The html string of the search page
Type: :class:`str`
    The type of item sought (Entité, Bloc, Item, Potion, Enchant, Progress, Effect, Success, Command), insensitive case. Type=None admits all types
limit: :class:`int`
    The maximum number of links to return

Return
------
    :class:`list`
        List of matching links

Raises
------
    :class:`TypeError`
        One of these arguments is not in the right type. Please check that :code:`code` is a :class:`str`, :code:`Type` is a :class:`str` or \
        :class:`None, and :code:`limit` an :class:`int`.
    :class:`ValueError`
        The given type is not valid, or the limit isn't strictly positive.
    """
    if type(code) != str or type(Type) not in [str,None] or type(limit) != int:
        raise TypeError("One of these arguments is not in the right type")
    if Type != None:
        if Type.lower() not in ["entité","bloc", "item", "potion", "enchant", "progrès", "effet", "succès", "commande"]:
            raise ValueError("The given type is not valid : {}".format(Type))
    if limit<1:
        raise ValueError("The limit must be strictly positive!")
    matches = regex.findall(r"<td class='id'><a[^>]+>([^<]+)",code)
    links = regex.findall(r"<a href=\"([^\"]+)\"  class=\"content_link \">Voir la fiche complète</a>",code)
    results1 = list()
    results2 = list()
    if Type==None:
        return links[limit:]
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
    """Function that retrieves all information about an entity from the html code of its page, and creates an :class:`~frmc_lib.Entity` object.

Parameters
----------
data: :py:class:`str`
    Source code of the page, in html (useless if you fill url)
url: :class:`str`
    Url of the page (useless if you enter data)

Return
------
    :class:`~frmc_lib.Entity`
        Object that contains all the information found about this entity

Raises
------
    :class:`TypeError`
        Data and url must be string or None
    :class:`ValueError`
        Data and url cannot be empty at the same time
        """
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
        img = "http://fr-minecraft.net/"+regex.search(r"<img src=\"([^\"]+)\" class=\"img\" alt=[^>]+>",data).group(1)
    except AttributeError:
        img =  ""
        pass
    #-- PV/PA --#
    matches = regex.finditer(r"<u>(.+)</u>(?:[^>]+)><img[^>]+title=\"([^\"]+)",data,regex.MULTILINE)
    if matches != None:
        for match in matches:
            if match.group(1)=="Points de vie :":
                PVs = match.group(2)
            elif match.group(1)=="Points d'attaque :":
                PAs = match.group(2)
    #-- ID --#
    IDs = list()
    try:
        for matchNum,match in enumerate(regex.finditer(r"<p class=\"identifiant\"><b>([^<]+)</b>([^<]+)",data,regex.MULTILINE)):
            IDs.append(match.group(1)+" "+match.group(2))
    except AttributeError:
        pass
    #-- Type --#
    try:
        Type = regex.search(r"<u>Type :</u> <span style=\"color: red;\">([^<]+)</span>",data).group(1)
    except AttributeError:
        Type = ""
        pass
    #-- Dropped xp --#
    try:
        XPs = regex.search(r"<u>Experience :</u> <img [^>]+> (\d)<br/>",data).group(1)
    except AttributeError:
        XPs = 0
        pass
    #-- Biomes --#
    Bioms = list()
    for matchNum,match in enumerate(regex.finditer(r"<li><img [^>]+ /> <a [^>]+>([^<]+)</a>",data)):
        Bioms.append(match.group(1))
    #-- Dimensions --#
    Dimensions = [0,0,0]
    try:
        r = regex.search(r"<div class=\"dimensions\"><[^>]+>Dimensions :</span> <br/>\s*<ul>\s*<li>[^<\d]+([\d|.]+)</li>\s*<li>[^<\d]+([\d|.]+)</li>\s*<li>[^<\d]+([\d|.]+)",data)
        Dimensions = list()
        for group in r.groups():
            Dimensions.append(float(group))
    except AttributeError:
        pass
    if len(Dimensions)<3:
        Dimensions = [0,0,0]
    #-- Version --#
    try:
        Vs = regex.search(regex_version,data).group(1)
    except AttributeError:
        Vs =""
    #-- Name --#
    Names = regex.search(r"<h3>(.+)<span>",data,regex.MULTILINE)
    if Names != None:
        Names = Names.group(1)
    else:
        Names = ""
    #-- Final entity --#
    En = Entity(Name=Names,ID="\n".join(IDs),Type=Type,PV=PVs,PA=PAs,XP=XPs,Biomes=Bioms,Dimensions=Dimensions,Version=Vs,Img=img)
    if url != None:
        En.Url = url
    return En



#----- Bloc/item infos -----#
def search_item(data=None,url=None):
    """Function that retrieves all information about an item from the html code of its page, and creates an :class:`~frmc_lib.Item` object.

Parameters
----------
data: :class:`str`
    Source code of the page, in html (useless if you fill url)
url: :class:`str`
    Url of the page (useless if you enter data)

Return
------
    :class:`~frmc_lib.Item`
        Object that contains all the information found about this item/block

Raises
------
    :class:`TypeError`
        Data and url must be string or None
    :class:`ValueError`
        Data and url cannot be empty at the same time
"""
    if type(data) not in [str,None] and type(url) not in [str,None]:
        raise TypeError("data and url must be string or None")
    if data == url == None:
        raise ValueError("data and url cannot be empty at the same time")
    if url != None and data == None:
        data = url_to_data(url)
    #-- Name --#
    Names = regex.search(r"<div class=\"popnom\">([^<]+)<br /> <em>[^<]+</em></div>",data,regex.MULTILINE)
    if Names != None:
        Names = Names.group(1)
    else:
        Names = ""
    #-- ID --#
    IDs = list()
    try:
        for matchNum,match in enumerate(regex.finditer(r"<p class=\"identifiant\"><b>([^<]+)</b>([^<]+)",data,regex.MULTILINE)):
            IDs.append(match.group(1)+" "+match.group(2))
    except AttributeError:
        pass
    #-- Stack --#
    Stacks = regex.search(r"<p>Stackable par (\d+) </p></div>",data,regex.MULTILINE)
    if Stacks != None:
        Stacks = Stacks.group(1)
    else:
        Stacks = 0
    #-- Tab --#
    Tabs = regex.search(r"</span> ([^<]+)</p>",data,regex.MULTILINE)
    if Tabs != None:
        Tabs = Tabs.group(1)
    else:
        Tabs = None
    #-- Damage --#
    Dmgs = regex.search(r"Cette arme inflige des dégats: <span class=\"healthbar\"><img src=\"[^\"]+\" style=\"[^\"]+\" alt=\"([\d.]+) [^>]+>",data,regex.MULTILINE)
    if Dmgs != None:
        Dmgs = Dmgs.group(1)
    else:
        Dmgs = None
    #-- Strength --#
    Strs = regex.search(r"<p>Solidité : Cet objet est utilisable <strong style=\"color: green;\">([\d]+)</strong> fois.</p>",data,regex.MULTILINE)
    if Strs != None:
        Strs = Strs.group(1)
    else:
        Strs = None
    #-- Tool --#
    Tools = regex.search(r"<a rel=\"popup\" href=\"[^\"]+\" onclick=\"[^\"]+\"  class=\"content_popup_link \">([^>]+)</a></span><br/>",data,regex.MULTILINE)
    if Tools != None:
        Tools = Tools.group(1)
    else:
        Tools = None
    #-- Version --#
    try:
        #Vs = regex.search(r"<div class=\"version\">[^<]+<br/><[^>]+>([^<]+)</a>",data).group(1)
        Vs = regex.search(regex_version,data).group(1)
    except AttributeError:
        Vs =""
    #-- Mobs --#
    Mobs = list()
    try:
        for match in regex.finditer(r"<img src=\"img/creatures/small/[^\"]+\" alt=\"([^\"]+)\" />",data,regex.MULTILINE):
            if not match.group(1) in Mobs:
                Mobs.append(match.group(1))
    except AttributeError:
        pass
    #-- Image --#
    Imgs = regex.search(r"<img class='block-big tooltip' src='([^']+)' alt='[^']+' />[^<]+<div class=\"popid\">ID : <strong>[^<]+</strong></div>",data,regex.MULTILINE)
    if Imgs != None:
        Imgs = "https://fr-minecraft.net/"+Imgs.group(1)
    else:
        Imgs != None
    #-- Final entity --#
    Bl = Item(Name=Names,ID=IDs,Stack=Stacks,Tab=Tabs,Damage=Dmgs,Strength=Strs,Tool=Tools,Version=Vs,Mobs=Mobs,Image=Imgs)
    if url != None:
        Bl.Url = url
    return Bl



#----- Command infos -----#
def search_cmd(data=None,url=None):
    """Function that retrieves all information about a command from the html code of its page, and creates an :class:`~frmc_lib.Command` object.

Parameters
----------
data: :py:class:`str`
    Source code of the page, in html (useless if you fill url)
url: :class:`str`
    Url of the page (useless if you enter data)

Return
------
    :class:`~frmc_lib.Command`
        Object that contains all the information found about this command

Raises
------
    :class:`TypeError`
        Data and url must be string or None
    :class:`ValueError`
        Data and url cannot be empty at the same time
    :class:`~frmc_lib.WrongDataError`
        Unable to find the syntax of this command. Please check the given data/url
"""
    if type(data) not in [str,None] and type(url) not in [str,None]:
        raise TypeError("data and url must be string or None")
    if data == url == None:
        raise ValueError("data and url cannot be empty at the same time")
    if url != None and data == None:
        data = url_to_data(url)
    #-- Syntax --#
    c1 = regex.search(r"(?<=Syntaxe : <b>)([^<]+)(?:.|\n)+(?=</span>\s{9}<a class=\"legende-bouton\")",data.replace("\r\n        ","         "),regex.MULTILINE)
    if c1 != None:
        Syntaxs = list()
        s = c1.group(0)
        Names = c1.group(1).replace("/","")
        for m in regex.finditer(r'<[^>]+>',c1.group(0)):
            s = s.replace(m.group(0),'')
        s = s.replace("&lt;","<").replace("&gt;",">")
        s = s.split("         ")
        for i in s:
            if len(i)>0:
                Syntaxs.append(i)
    else:
        raise WrongDataError("Unable to find the syntax of this command")
    #-- Examples --#
    Examples = list()
    for m in regex.finditer(r"<textarea class=\"input-exemple\">([^<]+)</textarea><br/>([^<]+)(?:<a[^>]+>([^<]+))?",data):
        syn = m.group(1)
        ex = m.group(2)+m.group(3) if m.group(3)!=None else m.group(2)
        Examples.append((syn,ex))
    #-- Version --#
    try:
        Vs = regex.search(regex_version,data).group(1)
    except AttributeError:
        Vs =""
    #-- Final command --#
    Cm = Command(Name=Names,Syntax=Syntaxs,Ex=Examples,Version=Vs)
    if url != None:
        Cm.Url = url
    return Cm



#----- Advancement infos -----#
def search_adv(data=None,url=None):
    """Function that retrieves all information about an advancement from the html code of its page, and creates an :class:`~frmc_lib.Advancement` object.

Parameters
----------
data: :py:class:`str`
    Source code of the page, in html (useless if you fill url)
url: :class:`str`
    Url of the page (useless if you enter data)

Return
------
    :class:`~frmc_lib.Advancement`
        Object that contains all the information found about this command

Raises
------
    :class:`TypeError`
        Data and url must be string or None
    :class:`ValueError`
        Data and url cannot be empty at the same time
"""
    if type(data) not in [str,None] and type(url) not in [str,None]:
        raise TypeError("data and url must be string or None")
    if data == url == None:
        raise ValueError("data and url cannot be empty at the same time")
    if url != None and data == None:
        data = url_to_data(url)
    data2 = data.replace("\r\n        ","")
    #-- Name --#
    try:
        Names = regex.search(r'<div class=\"popnom\">([^<]+)<br />',data).group(1)
    except:
        Names = ""
    #-- ID --#
    try:
        IDs = regex.search(r'<div class=\"popid\">ID : <strong>([^<]+)</strong></div>',data).group(1)
    except:
        IDs = ""
    #-- Type --#
    try:
        Ts = regex.search(r'<u>Type :</u> <span [^>]+>([^<]+)</span><br/>',data).group(1)
    except:
        Ts = ""
    #-- Action --#
    try:
        act = regex.search(r"<br><u>Action pour débloquer ce progrès :</u><br/>\s*<span class='news-content'>([^\n]+)",data2).group(1)
        Actions = act
        for m in regex.finditer(r'<[^>]+>',act):
            Actions = Actions.replace(m.group(0),'')
        Actions = Actions.replace("\r","").replace("\n","")
    except:
        Actions = ""
    #-- Parent --#
    try:
        Ps = regex.search(r"<u>Pour d.bloquer ce progrès, il vous faudra :</u>\s*<a rel=\"popup\" href=\"[^\"]+\" onclick=\"return hs\.htmlExpand\(this, { objectType: 'ajax', minWidth: '700', headingText: 'Progrès - ([^\']+)'} \)\"  class=\"content_popup_link \"> ",data2).group(1).rstrip()
    except:
        Ps = ""
    #-- Children --#
    Cs = list()
    try:
        c = regex.search(r"(?<=<u>Succès débloqués par ce progrès :</u><br/>)\s*<ul>(?:\s*<li><a[^>]+>\s*<div[^>]+>\s*<img[^>]+>\s*</div> [^<]+</a></li>)*",data2).group(0)
        #for m in regex.finditer(r"> ([^<]+)<",c):
        for m in regex.finditer(r'> ([^<]+[^\s])<',c):
            Cs.append(m.group(1))
    except:
        pass
    #-- Version --#
    try:
        Vs = regex.search(regex_version,data).group(1)
    except AttributeError:
        Vs =""
    Ad = Advancement(Name=Names,ID=IDs,Type=Ts,Action=Actions,Parent=Ps,Children=Cs,Version=Vs)
    if url != None:
        Ad.Url = url
    return Ad
