============
Generalities
============

Some functions are common to several (or all) classes, and are used to avoid copy and paste in the codes of each class. They are used automatically by the library, especially in the :func:`main` function, but you can also use them yourself in your code. 

You will also find on this page a summary of each class that can be returned to you by the main() function, each corresponding to a type of content (entity, item, command...)

This library depends on :mod:`regex` library to find the information in the html code, and :mod:`requests` to get the code from each page. 


.. note:: All given information come directly from the site `fr-minecraft.net <https://fr-minecraft.net>`_ !


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

This class represent a command (sometimes also called *cheat*). Here is the very long list of all available information : 

* The name of the command (the thing right after the slash)

* Syntax, in the form of a list of parameters

* Some examples to understand the use

* The version of the game where the item was added


~~~~~~~~~~~
Advancement
~~~~~~~~~~~

This class represents an advancement, the event that replaces achievements since Minecraft Java Edition 1.12. For those who are lazy enough to click on the word :class:`~frmc_lib.Advancement`, here is a list of information retrieved by the library :  

* The name of the advancement

* The type of the advancement (Progrès/Objectif)

* The previous and next advancement(s) in the Tree structure

* The url of the advancement page

* and some other information


-------------
Main function
-------------


.. autofunction:: frmc_lib.main

---------------
Search function
---------------

.. autofunction:: frmc_lib.search_links

-----------------------
Miscellaneous functions
-----------------------

~~~~~~~~~~~
Url to data
~~~~~~~~~~~

.. autofunction:: frmc_lib.url_to_data

~~~~~~~~~~~~~~~~~~~~~~~
Searching item function
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: frmc_lib.search

-----------------------
Miscellaneous constants
-----------------------

.. note:: These constants will probably never be useful to you; nevertheless they are an integral part of the library, so I preferred to indicate them here.

**regex_version:** The regex string used to retrieve the item version (one of the few that are common to almost all items)

.. code-block:: python

    regex_version = r'<div class=\"version\">[^<]+<br/>\s*<[^>]+>\s*([^<\n\r]+)\s*</a>'

**timeout:** When searching for the html version of a page, this is the maximum time, in seconds, the program waits before raising an exception `requests.Timeout <https://docs.python-requests.org/en/master/api/#requests.Timeout>`_.

.. code-block:: python

    timeout = 5

-----------
Some errors
-----------

~~~~~~~~~~~~~~~
MissingLibError
~~~~~~~~~~~~~~~

.. autoclass:: frmc_lib.MissingLibError
	:members:

~~~~~~~~~~~~~~~~~
ItemNotFoundError
~~~~~~~~~~~~~~~~~

.. autoclass:: frmc_lib.ItemNotFoundError
	:members:

~~~~~~~~~~~~~~
WrongDataError
~~~~~~~~~~~~~~

.. autoclass:: frmc_lib.WrongDataError
	:members:
