============
Generalities
============

Some functions are common to several (or all) classes, and are used to avoid copy and paste in the codes of each class. They are used automatically by the library, especially in the main() function, but you can also use them yourself in your code. 

You will also find on this page a summary of each class that can be returned to you by the main() function, each corresponding to a type of content (entity, item, command...)


.. note:: All given information come directly from the site fr-minecraft.net


.. warning:: Some information can be empty, depending on the entities: an xp orb will have no dimensions, or life points! 

------------
Classes used
------------

~~~~~~
Entity
~~~~~~

This class represents an entity of the Minecraft game, and several information about it. 
You will find in particular: 

* His name, in French

* A list of its identifiers (text), according to the different versions of the game

* Its type (passive, hostile...)

* Its points of attack and life

* An url to an image representing it (in png)



~~~~
Item
~~~~

This class represents an item or a block. As for the other classes, you will find there several information, such as : 

* A list of identifiers (text and sometimes numeric) according to the different versions of the game

* The size of a stack of this object (1 for tools, 16 for snowballs...)

* The tab where the item is in creative mode

* The version of the game where the item was added

* A list of mobs that can drop this item


~~~~~~~
Command
~~~~~~~

Oh please, be patient....

-------------
Main function
-------------


**Syntax**::

    main(name,Type)

The main function shortens the information acquisition method. It allows to generate an object from a simple word and a type, without having to execute all the sub-functions. This is probably the function you will use most often for standard library use.

* Parameters:
	- name (str): the name of the item to search for
	- Type (str): the type of item, in French (Entité, Bloc, Item, etc.)

* Return:
	Entity(), Item(), or other object type, depending on the Type given in parameters

---------------
Search function
---------------

**Syntax**::

	search_links(code,Type=None,limit=1)

This function allows you to find a certain number of links to item records from the html code of the search page. For example if you want to get the url addresses of all the swords, you have to give in arguments the code of the page https://fr-minecraft.net/recherche.php?search=sword and "Item" in type. 
You can get several links by changing the value of the limit argument (1 by default)

* Parameters: 
	- code (str): the html string of the search page
	- Type (str) (opt): the type of item sought (Entité, Bloc, Item, Potion, Enchant, Progress, Effect, Success, Command), insensitive case. Type=None admits all types
	- limit (int) (opt): the maximum number of links to return. The limit must be strictly positive

* Return: 
	List of matching links


-----------------------
Miscellaneous functions
-----------------------

~~~~~~~~~~~
Url to data
~~~~~~~~~~~

**Syntax**::

	url_to_data(url)

This function allows you to retrieve the source code of a web page, from its url address. You just have to give the url as parameter to receive a string containing the html code. 

* Parameters:
	- url (str): the url of the page

* Return:
	The html string of the page

~~~~~~~~~~~~~~~~~~~~~~~
Searching item function
~~~~~~~~~~~~~~~~~~~~~~

**Syntax**::

	search(item)

This function returns the source code of the search page, initialized with a string containing the query. 

* Parameters:
	- item (str): the name of the item to search. 

* Return:
	The url, in string
