========
Entities
========

Entities form a significant part of Minecraft's cubic world. That's why this library makes it easy to retrieve much of the information about any entity in the game. From the famous creeper to the orbe of xp, passing through the armor stands and the slimes, you can find their identifiers, their life points, the number of xp dropped to death, a link to an image representing the entity (png)... All taken directly from the site `fr-minecraft.net <https://fr-minecraft.net>`_ !

---------
The class
---------

When you search with the :func:`~frmc_lib.search_entity` function, you get an :class:`~frmc_lib.Entity` object that summarizes all the characteristics of the entity.
The details of this class are explained here: 

.. autoclass:: frmc_lib.Entity
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
