Platformer
===

A RPG inspired by Terreria

About
---
Run, shoot and... freak out with the graphics!
Right now you can't do much, so just star and sit back (if you can't code, and if you can: **contribute**!).
*This is an unofficial fork.*

Installation & requirements
---

**Requirements**

* Requires Python
* Requires PyGame

**Installation**

* Download the source

    ```
    git clone https://github.com/Data5tream/platformer.git
    ```
    
* Run the platformer.py script within the platformer folder

    ```
    ./platformer.py
    ```
    or
    
    ```
    python platformer.py
    ```

How to play
---
* Move with WASD
* Jump with space
* Shoot bullets with the mouse
* Quit with escape

Configuration
---
	
In platformer.py lines 11 & 12:

    ```python
    screen_width = *Your desired screen width*
    screen_height = *Your desired screen height*
    ```

Changelog (diferences to original project)
---

* Player can now die (Game ends when player's health goes beyond 0)
* Replaced taps with spaces in platformer.py and spite.py
* New bigger map for testing