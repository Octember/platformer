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

    ```
    screen_width = *Your desired screen width*
    screen_height = *Your desired screen height*
    ```

In globals.py line 16:

    ```
    GRAVITY = *desired gravity*
    ```
    
    0.001 is normal Gravity, 0.0001 is funny to play. Over 0.002, jumping is almost imposible.
    
Changelog (diferences to original project)
---

* Player can now die (Game ends when player's health goes beyond 0)
* Player can now win (Game ends when all enemies are dead)
* Replaced taps with spaces in platformer.py and spite.py
* New bigger map for testing
* **GRAPICS**