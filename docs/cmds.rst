.. automodule:: frmc_lib


.. role:: python(code)
	:language: python

========
Commands
========

Minecraft commands are kind of the hidden part of the game. They do a lot of things, *really* a lot. From simple teleporting to the creation of new gameplays, as well as counting statistics or placing blocks, the possibilities are almost infinite to who knows how to use them. This is why the library proposes to display for each command its syntax caption, and some examples to understand well. 

Again here all information is directly retrieved from the  `fr-minecraft.net <https://fr-minecraft.net>`_ site, so it is possible to have a latency time between the game update and the library update. 


---------
The class
---------

When you search with the :func:`~frmc_lib.search_cmd` function, you get an :class:`~frmc_lib.Command` object that summarizes all the characteristics of the command.
The details of this class are explained here: 

.. automodule:: frmc_lib
	:members: Command

-------------
How to search
-------------

using main()
~~~~~~~~~~~~

.. automodule:: frmc_lib
	:members: main
	:noindex:

using search_cmd()
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: frmc_lib
	:members: search_cmd
