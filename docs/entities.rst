.. automodule:: frmc_lib


.. role:: python(code)
	:language: python

========
Entities
========

Entities form a significant part of Minecraft's cubic world. That's why this library makes it easy to retrieve much of the information about any entity in the game. From the famous creeper to the orbe of xp, passing through the armor stands and the slimes, you can find their identifiers, their life points, the number of xp dropped to death, a link to an image representing the entity (png)... All taken directly from the site fr-minecraft.net!

When you search with the :func:`~frmc_lib.search_entity` function, you get an :class:`~frmc_lib.Entity` object that summarizes all the characteristics of the entity.
The details of this class are explained here: 

.. automodule:: frmc_lib
	:members: Entity

-------------
How to search
-------------

.. automodule:: frmc_lib
	:members: search_entity
