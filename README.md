# Century Spice AI
Lot's of fun work on ways to make a computer play Century Spice Road

This Read ME is mostly just a placeholder for future clarifications. But here's some information anyway.

## Calling the AI
Originally there was a command line based interface for setting up the hands, possible merchant trades, victory point cards, etc. ~~I've kept it around for no particularly good reason and will probably remove it when I get tired of scrolling past it.~~ (I did, now it is only in version history back at the beginning ne)

The signifcantly better option is the terminal based UI using forms from **pyscreen**. This accessed by running the module `>$ python3 -m century`. Use Ctrl-X to pull up the menu.
* Use the *Change* menu to populate the Trades and Points lists based on the current game state. 
* The *Run* option will populate the Path box with the next couple steps the AI wants to take. I'd recommend using *Run* every time someone else scores points or buys a card in case something better comes up.
* Use the *Replace* submenu to reflect these single card changes. It will allow you to select the card someone else grabbed and give upturned replacement.
* Use *Step Once* to move gradually through the printed path as the game progresses in the real world.
* To change the AI's avaiable spices if it gets off, use the *Change/Cubes* form
* To add or modify cards in the AI's hand, navigate directly to the Hand box and press Enter. Typing a new Merchant Card will save it to the hand. The space bar or the 'x' key will toggle if a card needs to be reclaimed before being played again. Using *Step Once* should automatically add cards from the BUY action, should mark the appropriate card after PLAY, and clear marks after RECLAIM.

## File Details
The currently working AI is housed in `century/*`. Crucially, `source/SpiceAI.py` is the brain of the algorithm and `source/structures.py` is the growing list of classes needed to support the game environment.

Outside of the main module there are some files under `nn_training`. This is an ongoing effort to create a competing AI that could learn based on Deep Q Learning (DQN). Good luck, me.


## Profiling notes
For an interactive html time tree, run `>$ pyinstrument -r html <script>`

For a sampled memory plot, run `>$ mprof run <script> ; mprof plot`
    
If you want both on the same run then add into whichever script you're going to `mprof`:
```python
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
#### Code to profile goes here
profiler.stop()
profiler.open_in_browser()
```