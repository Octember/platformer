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

```shell
git clone https://github.com/Data5tream/platformer.git
```
    
How to play
---

* Run the platformer.py script within the platformer folder

```shell
./platformer.py
```
or
    
```shell
python platformer.py
```

*Running the script this way, it will automatically load the map 'map2.db'.*
Running the game with the first map:

```shell
./platformer.py --map map
```

or

```shell
python platformer.py --map map
```

**CONTROLS**
* Move with WASD
* Jump with space
* Shoot bullets with the mouse
* Quit with escape

Configuration
---
	
* In platformer.py lines 11 & 12:

```python
screen_width = *Your desired screen width*
screen_height = *Your desired screen height*
```

* In globals.py line 16:

```python
GRAVITY = *desired gravity*
```
    
0.001 is normal Gravity, 0.0001 is funny to play. Over 0.002, jumping is almost impossible.
    
Changelog (differences to original project)
---

* Player can now die (Game ends when player's health goes beyond 0)
* Player can now win (Game ends when all enemies are dead)
* Replaced taps with spaces in platformer.py and spite.py
* New bigger map for testing
* Added command line arguments
* **GRAPHICS**