.. automodule:: frmc_lib


.. role:: python(code)
	:language: python

============
Advancements
============

Advancements are rewards earned when you do certain actions during your Minecraft game. They can help you progress in the game, giving you goals, quests, and sometimes with a small reward at stake. Advancements also replace the achievements, which were removed in Minecraft version 1.12. This library offers you to retrieve some details about these new advancements, such as their place in the general tree structure, or the way to get them. It's up to you how to use this information wisely! 

And like the other objects, the advancements come from the site `fr-minecraft.net <https://fr-minecraft.net>`_. Most of the texts are therefore in French. 


---------
The class
---------

When you search with the :func:`~frmc_lib.search_adv` function, you get an :class:`~frmc_lib.Advancement` object that summarizes all the characteristics of the advancement.
The details of this class are explained here: 

.. automodule:: frmc_lib
	:members: Advancement

-------------
How to search
-------------

using main()
~~~~~~~~~~~~

.. automodule:: frmc_lib
	:members: main
	:noindex:

using search_adv()
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: frmc_lib
	:members: search_adv
