.. role:: python(code)
	:language: python

==============
Items & Blocks
==============

The blocks are the essence of Minecraft. This cubist world being essentially composed of blocks, it is unthinkable that the library does not propose to collect information on them. By the same method, you will find information on the different items of the game, such as tools, food, etc.

The information provided is quite diverse, and the :class:`~frmc_lib.Item` class is flexible enough to adapt to each type of item : for a weapon you will find its durability and its attack points; for a block you will have the type of tool capable of breaking it ; for others you will get a list of mobs that could potentially drop this item, or the name of the creative mode tab... all this always retrieved directly from the site `fr-minecraft.net <https://fr-minecraft.net>`_ !


---------
The class
---------

When you search with the :func:`~frmc_lib.search_item` function, you get an :class:`~frmc_lib.Item` object that summarizes all the characteristics of the item (or the block).
The details of this class are explained here: 

.. autoclass:: frmc_lib.Item
	:members:

-------------
How to search
-------------

using main()
~~~~~~~~~~~~

.. autofunction:: frmc_lib.main
	:noindex:

using search_item()
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: frmc_lib.search_item
	:noindex:
