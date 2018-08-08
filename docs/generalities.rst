.. automodule:: frmc_lib


.. role:: python(code)
	:language: python

============
Generalities
============

Some functions are common to several (or all) classes, and are used to avoid copy and paste in the codes of each class. They are used automatically by the library, especially in the :func:`main` function, but you can also use them yourself in your code. 

You will also find on this page a summary of each class that can be returned to you by the main() function, each corresponding to a type of content (entity, item, command...)

This library depends on :mod:`regex` library to find the information in the html code, and :mod:`requests` to get the code from each page. 


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


.. automodule:: frmc_lib
	:members: main

---------------
Search function
---------------

.. automodule:: frmc_lib
	:members: search_links


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
