from dataclasses import dataclass, field

import npyscreen

from century.classes.app_forms import (BoxTitle_1t4, BoxTitleMultiSelect,
                                       ChangePoint, ChangeTrade, ReplacePoint,
                                       ReplaceTrade)
from century.core import (Action, ActionType, GameState, MerchantCard, Path,
                          Player, PointCard)
from century.core.rules import RULES as R
from century.core.SpiceAI import play_card, run_game
from century.helpers.switch import Caravan, remove_each


class MyTestApp(npyscreen.NPSAppManaged):
    def __init__(self):
        super().__init__()
        self.game: Game = Game(GameState([],[]), 
                                Player(Caravan([1,1,1]), Player.starting_hand()))
        self._internal_message = "DEFAULT"

    def onStart(self):
        self.addForm("MAIN", DesktopForm, name="Small Form")
        self.addFormClass("RTRADE", ReplaceTrade, name="Replace Merchant Card")
        self.addFormClass("RPOINT", ReplacePoint, name="Replace Point Card")
        self.addFormClass("CTRADE", ChangeTrade, name="Change Trades")
        self.addFormClass("CPOINT", ChangePoint, name="Change Points")
        # REMOVED ChangeHand and ChangeCube form because changing 
        # in the main form is working well
        # self.addFormClass("CHAND", ChangeHand, name="Change Hand")
        # self.addFormClass("CCUBE", ChangeCube, name="Change Cubes") 
    
    def get_message(self):
        'Returns the currently stored message and resets to default'
        message = self._internal_message
        self._internal_message = "DEFAULT"
        return message
    
    def set_message(self, msg):
        self._internal_message = msg

class DesktopForm(npyscreen.FormBaseNewWithMenus):
    def create(self):
        col_width = 32
        row_height = R['mc supply len'] + 3
        self.trades = self.add(npyscreen.BoxTitle, name="Merchant Cards", 
                        max_width = col_width, max_height = row_height,
                        contained_widget_arguments = {'allow_filtering': False})
        self.points = self.add(npyscreen.BoxTitle, name="Point Cards", 
                        max_width = col_width, max_height = row_height,
                        relx = col_width + 3, rely = 2,
                        contained_widget_arguments = {'allow_filtering': False})
        self.hand = self.add(BoxTitleMultiSelect, name="Hand", footer="SPC toggle, Ctrl-U wipe", 
                        max_width = col_width,
                        contained_widget_arguments = {'allow_filtering': False})
        self.cubes = self.add(BoxTitle_1t4, name="Cubes", 
                        max_width = col_width, max_height = 6,
                        relx = col_width + 3, rely = 11)
        self.path = self.add(npyscreen.BoxTitle, name="Path", values = ["Open Menu to Run"],
                        max_width = col_width,
                        relx = col_width + 3, rely = 18,
                        contained_widget_arguments = {'allow_filtering': False})

        action_menu = self.new_menu()
        action_menu.addItem(text = "Run", onSelect = self.update_path)
        action_menu.addItem(text = "Step Once", onSelect = self.step_path)

        replace_menu = action_menu.addNewSubmenu(name = "Replace")
        replace_menu.addItem(text = "Trade", onSelect = lambda : self.parentApp.switchForm("RTRADE"))
        replace_menu.addItem(text = "Point", onSelect = lambda : self.parentApp.switchForm("RPOINT"))

        change_menu = action_menu.addNewSubmenu(name = "Change")
        change_menu.addItem(text = "Trade", onSelect = lambda : self.parentApp.switchForm("CTRADE"))
        change_menu.addItem(text = "Point", onSelect = lambda : self.parentApp.switchForm("CPOINT"))

    def beforeEditing(self):
        'Called before every time the form becomes visible (editable)'
        self.trades.values = self.parentApp.game.trade_string()
        self.points.values = self.parentApp.game.point_string()
        self.hand.values = self.parentApp.game.ai.hand
        self.cubes.value = self.parentApp.game.cube_string()

    def update_path(self):
        self.parentApp.game.play()
        self.path.values = Game.path_string( self.parentApp.game.path )
    
    def step_path(self):
        path = self.parentApp.game.path

        temp = path
        if temp == None or temp == [] or temp.head == None:
            return
        
        if temp.prev == None:
            next_form = follow_action(temp.head, self.parentApp)
            temp.head = None
        else:
            while temp.prev.prev is not None:
                temp = temp.prev
            next_form = follow_action(temp.prev.head, self.parentApp)
            temp.prev = None

        self.path.values = Game.path_string( self.parentApp.game.path )
        self.cubes.value = self.parentApp.game.cube_string()
        if next_form:
            self.parentApp.switchForm(next_form)

@dataclass
class Game():
    gs: GameState
    ai: Player
    path: list[str] = field(default_factory=lambda: [])

    def play(self):
        self.path = run_game(
            self.gs.point_list, 
            self.ai.hand, 
            self.ai.caravan, 
            self.gs.merchant_list)

    def trade_string(self):
        return [x.num_str() if isinstance(x, MerchantCard)
                else str(x)
                for x in self.gs.merchant_list]
    
    def point_string(self):
        return [x.num_str() if isinstance(x, PointCard)
                else str(x)
                for x in self.gs.point_list]
    
    def hand_string(self):
        return [x.num_str() if isinstance(x, MerchantCard)
                else str(x)
                for x in self.ai.hand]

    def cube_string(self):
        return ''.join((str(x) for x in self.ai.caravan.elements()))

    @staticmethod
    def path_string(p: Path):
        string = str(p)
        return string.splitlines()[1:-1] # drop ">>Start" and "<<End"

def follow_action(action: Action, app: MyTestApp):
    game: Game = app.game

    if action.type == ActionType.BUY:
        index = game.gs.merchant_list.index( action.card )
        remove_each( game.ai.caravan, [1] * index )
        app.set_message(index)
        game.ai.hand.append(action.card)
        return 'RTRADE'

    if action.type == ActionType.RECLAIM:
        for card in game.ai.hand:
            card['playable'] = True
        return

    if action.type == ActionType.PLAY:
        action.card.playable = True
        multi_plays = play_card(action.card, game.ai.caravan)
        game.ai.caravan = multi_plays[action.times - 1][1]

        for card in game.ai.hand:
            if card == action.card:
                card['playable'] = False
        return

    if action.type == ActionType.SCORE:
        index = game.gs.point_list.index( action.card )
        app.set_message(index)
        remove_each(game.ai.caravan, action.card.cost)
        return 'RPOINT'
    
    return

def run():
    try:
        MyTestApp().run()
    except (EOFError,KeyboardInterrupt) as e:
        print("\nGoodbye! Play again soon")
        exit(e)
    
if __name__ == '__main__':
    run()   
    