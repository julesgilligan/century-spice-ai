RULES = {
    'pc supply len': 5,
    'mc supply len': 6,
    'start token mult': 2,
    'start hand': 'TODO',
    'start cubes':{1:[1,1,1],2:[1,1,1,1],3:[1,1,1,1],4:[1,1,1,2],5:[1,1,1,2]},
    'require actions' : True,
    'cards stay down': True,
    'multiple trades': True,
    'aquire with': [1,2,3,4],
    'limited tokens': True,
    'slide silver': True,
    'caravan limit': 10,
    'supply limit': False,
    'gold multiplier': 3,
    'silver multiplier': 1,
    'cube multiplier': [0,1,1,1]
}

"""
 ##------------------##
##  RULES, plain txt  ##
 ##__________________##
Set up:
(1) Point card (orange) 5 face up, rest face down deck
(2) Gold tokens (2x players) above first Point card (furthest from deck)
(2.1) Silver tokens (2x players) above second Point card
(3) Each player gets Merchant cards Create 2 and Upgrade 2
(4) Merchant cards (purple) 6 face up, rest face down deck
(5) Spices are cubes, separate by color. Y<R<G<B
(6) Caravan card (grey) to each player
(7) Players start with cubes based on turn order (1:YYY, 2,3:YYYY, 4,5:YYYR)

Taking a Turn
Game played over a series of rounds, a round is a sequence of individuals' turns
On player turn must take 1 of the following actions:
- Play:     play a card from hand
- Aquire:   get a Merchant card
- Rest:     all previously played cards back to hand
- Claim:    get a Point card

Play
Place card face up and execute the card's effect. 
3 types of MCs:Spice, Upgrade, Trade
Spice: add cubes shown on the card to your caravan
Upgrade: MAY upgrade any cube up 1 level and then MAY upgrade any cube up 1 level.
        Can be the same.
Trade: Give spices shown above the arrow then take spices shown below. 
        Can be done any number of times.

Aquire
Pay for the card by placing ANY cube each Merchant card before the one you aquire
Take the Merchant card into your hand, any cubes on it go into your caravan
Slide all cards away from the deck and draw a card to fill the empty slot

Rest
Take all cards played in front of you back into your hand

Claim
Spend cubes from your caravan matching the cubes on the Point card.
Take the Point card and place it face down.
Slide all cards away from the deck and draw a card to fill the empty slot.
If you take a card below a pile of gold or silver tokens, take a token.
If there are no more gold tokens, slide the silver tokens above the first card

Limit
If a player's caravan has more than 10 cubes, they must return cubes of their choice
Cube supply is unlimited

Game End
Count points on point card
gold tokens are worth 3
silver tokens are worth 1
non-yellow cubes are worth 1
"""