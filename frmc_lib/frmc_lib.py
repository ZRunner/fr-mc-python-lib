
import requests, re
from typing import List, Optional, Tuple, Literal

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
    """Raised when an item cannot be found"""
    def __init__(self,message):
        self.message = message
        
class WrongDataError(Error):
    """Raised when there is an error during parsing data"""
    def __init__(self,message):
        self.message = message


#----- Classes -----#
class Entity():
    """This class represents an entity, and all information about it.

    Here is a list of all variables accessible after creation:

    .. hlist::
    :columns: 2

    * name
    * entity_ids
    * entity_ype
    * health
    * attack
    * xp
    * biomes
    * dimensions
    * version
    * image
    * url
    
    Parameters
    ----------
        diverses All information that will be stored in the class

    .. tip:: Details on each of the information are given in comments in the source code
    """
    def __init__(self,name, entity_ids, entity_type, health, attack, xp, biomes, sizes, version, image, url=None):
        self.name: str = name  # Name of the entity
        self.entity_ids: List[str] = entity_ids  # Text id
        self.entity_type: str = entity_type  # Type of the entity
        self.health: int = health  # Health points
        self.attack: Optional[float] = attack  # Attack points
        self.xp: int = xp  # XP droped
        self.biomes: List[str] = biomes  # Favorites biomes
        self.sizes: list[float] = sizes  # Entity 3D sizes (width, length, height)
        self.version: str = version  # Game version when adding
        self.image: Optional[str] = image  # Image url
        self.url: str = url  # Url of the entity page

class Item():
    """This class represent an item or a block. Some information can be empty depending on the type of item (weapon, block...).

    Here is a list of all variables accessible after creation:

    .. hlist::
    :columns: 2

    * name
    * item_ids
    * stack
    * creative_tab
    * damages
    * durability
    * tnt_resistance
    * tool
    * version
    * mobs
    * image
    * url
    
    Parameters
    ----------
        diverses All information that will be stored in the class

    .. tip:: Details on each of the information are given in comments in the source code
    """
    def __init__(self, name, item_ids, stack_size, tab, damages, durability, tnt_resistance, tool, version, mobs, image, url=None):
        self.name: str = name  # Name of the item
        self.item_ids: List[str] = item_ids  # Text id
        self.stack_size: Optional[int] = stack_size  # Size of a stack
        self.creative_tab: Optional[str] = tab  # Tab in creative gamemode
        self.damages: Optional[float] = damages  # Weapon damage
        self.durability: Optional[int] = durability  # Durability
        self.tnt_resistance: Optional[int] = tnt_resistance # Resistance to TNT explosion
        self.tool: str = tool  # Tool able to destroy it
        self.version: str = version  # Game version when adding
        self.mobs: List[str] = mobs  # List of mobs that can drop this item
        self.image: Optional[str] = image  # Url of an image
        self.url: str = url  # Url of the item page

class Command():
    """This class represent a command (sometimes also called *cheat*).

    Here is a very long list of the immensity of the hundreds of information accessible after creation (yes there are only 4, it's not a bug)

    .. hlist::
    :columns: 1

    * name
    * syntax
    * examples
    * version
    * url
    
    Parameters
    ----------
        diverses All information that will be stored in the class

    .. tip:: Details on each of the information are given in comments in the source code
    """
    def __init__(self, name, syntax, examples, version, url=None):
        self.name: str = name  # Name of the command
        self.syntax: List[str] = syntax  # List of parameters, sorted in order of use
        self.examples: list[Tuple[str, str]] = examples  # List of some examples, contained in tuples in the form (syntax, explanation)
        self.version: str = version  # Game version when adding
        self.url: str = url  # Url of the command page

class Advancement():
    """This class represents an advancement, the event that replaces achievements since Minecraft Java Edition 1.12.

    Here is the list of information that can be obtained after creating the object:

    .. hlist::
        :columns: 1

        * name
        * adv_id
        * adv_type
        * description
        * parent
        * children
        * version
        * image
        * url

    Parameters
    ----------
        diverses All information that will be stored in the class

    .. tip:: Details on each of the information are given in comments in the source code
    """
    def __init__(self, name, adv_id, adv_type, description, parent, children, version, image, url=None):
        self.name: str = name  # Name of the advancement
        self.adv_id: str = adv_id  # Text identifier
        self.adv_type: Literal["Progrès", "Objectif (Goal)"] = adv_type  # Type of the advancement (Progrès/Objectif)
        self.description: str = description  # Description of the advancement (fr)
        self.parent: Optional[str] = parent  # Previous advancement in the Tree structure
        self.children: List[str] = children  # List of next advancement(s) in the Tree structure
        self.version: str = version  # Game version when adding
        self.image: Optional[str] = image  # Logo of the advancement
        self.url: str = url  # Url of the advancement page

class SearchType:
    ENTITY = "entité"
    BLOCK = "bloc"
    ITEM = "item"
    POTION = "potion" # NOT IMPLEMENTED
    ENCHANT = "enchant" # NOT IMPLEMENTED
    ADVANCEMENT = "progrès"
    EFFECT = "effet" # NOT IMPLEMENTED
    SUCCESS = "succès" # NOT IMPLEMENTED
    COMMAND = "commande"

    @classmethod
    def as_list(cls) -> Tuple[str, ...]:
        return (cls.ENTITY, cls.BLOCK, cls.ITEM, cls.POTION, cls.ENCHANT,
            cls.ADVANCEMENT, cls.EFFECT, cls.SUCCESS, cls.COMMAND)

#----- Useful functions -----#
def main(name: str, item_type: str):
    """The main function shortens the information acquisition method. It allows to generate an object from a simple word \
    and a type, without having to execute all the sub-functions. This is probably the function you will use most often for \
    standard library use.

    Parameters
    ----------
    name: :class:`str`
        The name of the item to search for
    item_type: :class:`str`
        The type of item. Use :class:`~SearchType` to make sure to get the right identifier

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
    urls = search_links(data, item_type)
    if len(urls) == 0:
        raise ItemNotFoundError("This item cannot be found: {} (Type: {})".format(name,item_type))
    if item_type.lower() in {SearchType.BLOCK, SearchType.ITEM}:
        item = search_item(url=urls[0])
    elif item_type.lower() == SearchType.ENTITY:
        item = search_entity(url=urls[0])
    elif item_type.lower() == SearchType.COMMAND:
        item = search_cmd(url=urls[0])
    elif item_type.lower() == SearchType.ADVANCEMENT:
        item = search_adv(url=urls[0])
    else:
        raise ItemNotFoundError("This item type is not available: {}".format(item_type))
    return item

def url_to_data(url: str):
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
    if not isinstance(url, str):
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
def search(item: str):
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
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    p = "http://fr-minecraft.net/recherche.php?search="+"+".join(item.split(" "))
    p = url_to_data(p)
    return p

def search_links(html: str, result_type: str=None, limit: int=1):
    """This function allows you to find a certain number of links to item records from the \
    html code of the search page. For example if you want to get the url addresses \
    of all the swords, you have to give in arguments the code of the page \
    https://fr-minecraft.net/recherche.php?search=sword and "Item" in type. 
    You can get several links by changing the value of the limit argument (1 by default)

    Parameters
    ----------
    html: :class:`str`
        The html string of the search page
    result_type: :class:`str`
        The type of item to find. Use the :class:`~SearchType` to make sure to use the right one. result_type=None admits all types
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
    if result_type is not None and not isinstance(html, str) and not isinstance(result_type, str) and not isinstance(limit, int):
        raise TypeError("One of these arguments is not in the right type")
    if result_type is not None:
        if result_type not in SearchType.as_list():
            raise ValueError("The given type is not valid : {}".format(result_type))
    if limit < 1:
        raise ValueError("The limit must be strictly positive!")
    matches = re.findall(r"<td class='id'><a[^>]+>([^<]+)",html)
    links = re.findall(r"<a href=\"([^\"]+)\"  class=\"content_link \">Voir la fiche complète</a>",html)
    results1 = list()
    results2 = list()
    if result_type is None:
        return links[limit:]
    else:
        for e, m in enumerate(matches):
            if m.lower() == result_type and len(results1) < limit:
                results1.append("https://fr-minecraft.net/"+links[e])
    for i in results1:
        if not i in results2:
            results2.append(i)
    return results2


#----- Entity infos -----#
def search_entity(html: str=None, url: str=None):
    """Function that retrieves all information about an entity from the html code of its page, and creates an :class:`~frmc_lib.Entity` object.

    Parameters
    ----------
    html: :class:`str`
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
    if html is not None and url is not None and not isinstance(html, str) and not isinstance(url, str):
        raise TypeError("data and url must be string or None")
    if html is None and url is None:
        raise ValueError("data and url cannot be empty at the same time")
    if url is not None and html is None:
        html = url_to_data(url)
    health = None
    attack = None
    #-- Image --#
    try:
        img = "http://fr-minecraft.net/"+re.search(r"<img src=\"([^\"]+)\" class=\"img\" alt=[^>]+>",html).group(1)
    except AttributeError:
        img =  None
        pass
    #-- Health --#
    try:
        health = re.search(r"<u>Points? de vie :</u>(?:[^>]+)><img[^>]+title=\"(\d+) points?\"", html, re.MULTILINE).group(1)
        health = int(health)
    except AttributeError:
        health = 0
    #-- Attack --#
    try:
        attack = re.search(r"<u>Points? d'attaque :</u>(?:[^>]+)><img[^>]+title=\"(\d+(?:\.\d+)?) points?\"", html, re.MULTILINE).group(1)
        attack = float(attack)
    except AttributeError:
        attack = None
    #-- ID --#
    entity_ids = list()
    try:
        for match in re.finditer(r"<p class=\"identifiant\"><b>([^<]+)</b>([^<]+)",html,re.MULTILINE):
            entity_ids.append(match.group(1)+" "+match.group(2))
    except AttributeError:
        pass
    #-- Type --#
    try:
        entity_type = re.search(r"<u>Type :</u> <span style=\"color: red;\">([^<]+)</span>",html).group(1)
    except AttributeError:
        entity_type = None
        pass
    #-- Dropped xp --#
    try:
        xp = int(re.search(r"<u>Experience :</u> <img [^>]+> (\d)<br/>",html).group(1))
    except AttributeError:
        xp = None
        pass
    #-- Biomes --#
    biomes = list()
    for match in re.finditer(r"<li><img [^>]+ /> <a [^>]+>([^<]+)</a>",html):
        biomes.append(match.group(1))
    #-- Dimensions --#
    size = [0,0,0]
    try:
        r = re.search(r"<div class=\"dimensions\"><[^>]+>Dimensions :</span> <br/>\s*<ul>\s*<li>[^<\d]+([\d|.]+)</li>\s*<li>[^<\d]+([\d|.]+)</li>\s*<li>[^<\d]+([\d|.]+)",html)
        size = list()
        for group in r.groups():
            size.append(float(group))
    except AttributeError:
        pass
    if len(size) < 3:
        size = (0,0,0)
    #-- Version --#
    try:
        version = re.search(regex_version,html).group(1).strip()
    except AttributeError:
        version = None
    #-- Name --#
    name = re.search(r"<h3>(.+)<span>",html,re.MULTILINE)
    if name is not None:
        name = name.group(1).strip()
    else:
        name = None
    #-- Final entity --#
    result = Entity(name=name, entity_ids="\n".join(entity_ids), entity_type=entity_type, health=health,
                attack=attack, xp=xp, biomes=biomes, sizes=size, version=version, image=img)
    if url is not None:
        result.url = url
    return result


#----- Bloc/item infos -----#
def search_item(html: str=None, url: str=None):
    """Function that retrieves all information about an item from the html code of its page, and creates an :class:`~frmc_lib.Item` object.

    Parameters
    ----------
    html: :class:`str`
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
    if html is not None and url is not None and not isinstance(html, str) and not isinstance(url, str):
        raise TypeError("data and url must be string or None")
    if html is None and url is None:
        raise ValueError("data and url cannot be empty at the same time")
    if url is not None and html is None:
        html = url_to_data(url)
    #-- Name --#
    name = re.search(r"<div class=\"popnom\">([^<]+)<br /> <em>[^<]+</em></div>",html,re.MULTILINE)
    if name is not None:
        name = name.group(1)
    #-- ID --#
    item_ids = list()
    try:
        for match in re.finditer(r"<p class=\"identifiant\"><b>([^<]+)</b>([^<]+)",html,re.MULTILINE):
            item_ids.append(match.group(1)+" "+match.group(2))
    except AttributeError:
        pass
    #-- Stack --#
    stacks = re.search(r"<p>Stackable par (\d+) </p></div>",html,re.MULTILINE)
    if stacks is not None:
        stacks = int(stacks.group(1))
    #-- Tab --#
    tab = re.search(r"<p class=\"onglet-crea\">Onglet Créatif : <span><img[^>]+></span>([^<]+)</p>",html,re.MULTILINE)
    if tab is not None:
        tab = tab.group(1).strip()
    else:
        tab = None
    #-- Damage --#
    dmg = re.search(r"Cette arme inflige des dégats: <span class=\"healthbar\"><img src=\"[^\"]+\" style=\"[^\"]+\" alt=\"([\d.]+) [^>]+>",html,re.MULTILINE)
    if dmg is not None:
        dmg = float(dmg.group(1))
    #-- Durability --#
    dura = re.search(r"<p>Solidité : Cet objet est utilisable <strong style=\"color: green;\">([\d]+)</strong> fois.</p>",html,re.MULTILINE)
    if dura is not None:
        dura = int(dura.group(1))
    #-- TNT resistance --#
    tnt = re.search(r"<p><span>Résistance à la TNT :</span> ?(\d+)</p>", html, re.MULTILINE)
    if tnt is not None:
        tnt = int(tnt.group(1))
    #-- Tool --#
    tool = re.search(r"<a rel=\"popup\" href=\"[^\"]+\" onclick=\"[^\"]+\"  class=\"content_popup_link \">([^>]+)</a></span><br/>",html,re.MULTILINE)
    if tool is not None:
        tool = tool.group(1)
    #-- Version --#
    try:
        version = re.search(regex_version,html).group(1).strip()
    except AttributeError:
        version = ""
    #-- Mobs --#
    mobs = list()
    try:
        for match in re.finditer(r"<img src=\"img/creatures/small/[^\"]+\" alt=\"([^\"]+)\" />",html,re.MULTILINE):
            if not match.group(1) in mobs:
                mobs.append(match.group(1))
    except AttributeError:
        pass
    #-- Image --#
    image = re.search(r"<img class='block-big tooltip' src='([^']+)' alt='[^']+' />[^<]+<div class=\"popid\">ID : <strong>[^<]+</strong></div>",html,re.MULTILINE)
    if image is not None:
        image = "https://fr-minecraft.net/"+image.group(1)
    #-- Final entity --#
    result = Item(name=name, item_ids=item_ids, stack_size=stacks, tab=tab, damages=dmg,
                  durability=dura, tnt_resistance=tnt, tool=tool, version=version, mobs=mobs, image=image)
    if url is not None:
        result.url = url
    return result


#----- Command infos -----#
def search_cmd(html: str=None, url: str=None):
    """Function that retrieves all information about a command from the html code of its page, and creates an :class:`~frmc_lib.Command` object.

    Parameters
    ----------
    html: :class:`str`
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
    if html is not None and url is not None and not isinstance(html, str) and not isinstance(url, str):
        raise TypeError("data and url must be string or None")
    if html is None and url is None:
        raise ValueError("data and url cannot be empty at the same time")
    if url is not None and html is None:
        html = url_to_data(url)
    #-- Syntax --#
    html = html.replace("\r\n        ","         ")
    #c1 = re.search(r"(?<=Syntaxe : <b>)(\d+|\D+)(?=</span>\s{8,}<a class=\"legende-bouton\")",data.replace("\r\n        ","         "),re.MULTILINE)
    part1  = re.search(r'(?<=Syntaxe : <b>)((\s|.)+)',html)
    c1 = None
    if part1 is not None:
        part2 = re.search(r'(?=\s{8,}<a class=\"legende-bouton\")((.|\s)+)',part1.group(1))
        if part2 is not None:
            c1 = part1.group(1).replace(part2.group(1),"")
    if c1 is not None:
        syntaxes = list()
        s = c1
        name = c1.split("<")[0].replace("/","")
        for m in re.finditer(r'<[^>]+>',c1):
            s = s.replace(m.group(0),'')
        s = s.replace("&lt;","<").replace("&gt;",">")
        s = s.split("         ")
        for i in s:
            if len(i) > 0:
                syntaxes.append(i.strip())
    else:
        raise WrongDataError("Unable to find the syntax of this command")
    #-- Examples --#
    examples = list()
    for m in re.finditer(r"<textarea class=\"input-exemple\">([^<]+)</textarea><br/>([^<]+)(?:<a[^>]+>([^<]+))?", html):
        syn = m.group(1)
        ex = m.group(2)+m.group(3) if m.group(3)!=None else m.group(2)
        examples.append((syn,ex))
    #-- Derived commands --#
    # DOES NOT WORK FOR SOME REASONS
    # derived = list()
    # for m in re.finditer(r"<h\d>Commm?ande\(s\) dérivée\(s\) :</h\d>(<[^>]+>)*?(/[^<]+)", html):
    #     derived.append(m.group(1).strip())
    #-- Version --#
    try:
        version = re.search(regex_version,html).group(1).strip()
    except AttributeError:
        version = None
    #-- Final command --#
    result = Command(name=name, syntax=syntaxes, examples=examples, version=version)
    if url is not None:
        result.url = url
    return result


#----- Advancement infos -----#
def search_adv(html: str=None, url: str=None):
    """Function that retrieves all information about an advancement from the html code of its page, and creates an :class:`~frmc_lib.Advancement` object.

    Parameters
    ----------
    html: :class:`str`
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
    if html is not None and url is not None and not isinstance(html, str) and not isinstance(url, str):
        raise TypeError("data and url must be string or None")
    if html is None and url is None:
        raise ValueError("data and url cannot be empty at the same time")
    if url is not None and html is None:
        html = url_to_data(url)
    data2 = html.replace("\r\n        ","")
    #-- Name --#
    try:
        names = re.search(r'<div class=\"popnom\">([^<]+)<br />',html).group(1)
    except AttributeError:
        names = None
    #-- ID --#
    try:
        ids = re.search(r'<div class=\"popid\">ID : <strong>([^<]+)</strong></div>',html).group(1)
    except AttributeError:
        ids = None
    #-- Type --#
    try:
        adv_type = re.search(r'<u>Type :</u> <span [^>]+>([^<]+)</span><br/>',html).group(1)
    except AttributeError:
        adv_type = None
    #-- Action --#
    try:
        act = re.search(r"<br><u>Action pour débloquer ce progr.s :</u><br/>\s*<span class='news-content'>([^\n]+)",data2).group(1)
        actions = act
        for m in re.finditer(r'<[^>]+>',act):
            actions = actions.replace(m.group(0),'')
        actions = actions.replace("\r","").replace("\n","")
    except AttributeError:
        actions = None
    #-- Parent --#
    try:
        parent = re.search(r"<u>Pour d.bloquer ce progr.s, il vous faudra :</u>\s*<a rel=\"popup\" href=\"[^\"]+\" onclick=\"return hs\.htmlExpand\(this, { objectType: 'ajax', minWidth: '700', headingText: 'Progrès - ([^\']+)'} \)\"  class=\"content_popup_link \"> ",data2).group(1).rstrip()
    except AttributeError:
        parent = None
    #-- Children --#
    children = list()
    try:
        pattern = re.search(r"(?<=<u>Succès débloqués par ce progr.s :</u><br/>)\s*<ul>(?:\s*<li><a[^>]+>\s*<div[^>]+>\s*<img[^>]+>\s*</div> [^<]+</a></li>)*",data2).group(0)
        for m in re.finditer(r'> ([^<]+[^\s])<', pattern):
            children.append(m.group(1))
    except AttributeError:
        pass
    #-- Image --#
    try:
        image = "https://fr-minecraft.net/" + re.search(r"<div class=\"advancement_icon_big tooltip_advancement.?\" [^<]+<img(?:.*)(?=src='([^']+)' [^<]+</div>)",html).group(1)
    except AttributeError:
        image = None
    if image == "https://fr-minecraft.net/css/img/pixel.png":  #Fake image
        image = None
    #-- Version --#
    try:
        version = re.search(regex_version,html).group(1).strip()
    except AttributeError:
        version = None
    result = Advancement(name=names,adv_id=ids,adv_type=adv_type,description=actions,parent=parent,children=children,image=image,version=version)
    if url is not None:
        result.url = url
    return result
