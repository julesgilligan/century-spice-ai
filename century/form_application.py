from century.source.caravan_helpers import Caravan, remove_each
import curses
import re
from dataclasses import dataclass, field

import npyscreen

from century.source import (Action, ActionType, GameState, MerchantCard, Path,
                            Player, PointCard)
from century.source.helpers import read_merchant_card, read_point_card
from century.source.rules import RULES as R
from century.source.SpiceAI import play_card, run_game


class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.game : Game = Game(GameState([],[]), 
                                Player(Caravan([1,1,1]), Player.starting_hand()))
        self.addForm("MAIN", DesktopForm, name="Small Form")
        self.addFormClass("RTRADE", ReplaceTrade, name="Replace Merchant Card")
        self.addFormClass("RPOINT", ReplacePoint, name="Replace Point Card")
        self.addFormClass("CTRADE", ChangeTrade, name="Change Trades")
        self.addFormClass("CPOINT", ChangePoint, name="Change Points")
        self.addFormClass("CHAND", ChangeHand, name="Change Hand")
        self.addFormClass("CCUBE", ChangeCube, name="Change Cubes") 


class MultiMerchantHand(npyscreen.MultiLineEditable):
    _contained_widgets = npyscreen.Textfield

    def display_value(self, vl):
        if isinstance(vl, MerchantCard):
            string = "["
            string += " " if vl['playable'] else "X"
            string += "] "
            string += vl.num_str()
            return string
        return "[ ]"

    def h_select_none(self, _):
        for line in self.values:
            line['playable'] = True
        self.display()

    def h_select_toggle(self, _):
        card: MerchantCard = self.values[self.cursor_line]
        card['playable'] = not card['playable']
        self.display()
    
    def edit_cursor_line_value(self):
        if len(self.values) == 0:
            self.insert_line_value()
            return False
        try:
            active_line = self._my_widgets[(self.cursor_line-self.start_display_at)]
        except IndexError:
            # self._my_widgets[0]
            self.cursor_line = 0
            self.insert_line_value()
            return True
        active_line.highlight = False
        ## vvv THE ONLY PART JULES HAS CHANGED FROM ORIGINAL
        _, result = active_line.edit()
        try:
            self.values[self.cursor_line] = read_merchant_card(result)
        ## ^^^ THE ONLY PART JULES HAS CHANGED FROM ORIGINAL
        except IndexError:
            self.values.append(active_line.value)
            if not self.cursor_line:
                self.cursor_line = 0
            self.cursor_line = len(self.values) - 1
        self.reset_display_cache()
        
        if self.CHECK_VALUE:
            if not self.check_line_value(self.values[self.cursor_line]):
                self.delete_line_value()
                return False
        
        self.display()
        return True

    def set_up_handlers(self):
        super().set_up_handlers()
        self.handlers.update ( {
                    # ord('i'):           self.h_insert_value,
                    # ord('o'):           self.h_insert_next_line,
                    # curses.ascii.NL:    self.h_edit_cursor_line_value,
                    # curses.KEY_BACKSPACE:   self.h_delete_line_value,
                    ord("x"):    self.h_select_toggle,
                    curses.ascii.SP: self.h_select_toggle,
                    "^U":        self.h_select_none,
                } )

class BoxTitleMultiSelect(npyscreen.BoxTitle):
    _contained_widget = MultiMerchantHand

class DesktopForm(npyscreen.FormBaseNewWithMenus):
    def create(self):
        col_width = 32
        row_height = R['mc supply len'] + 3
        game = self.parentApp.game
        self.trades = self.add(npyscreen.BoxTitle, name="Merchant Cards", values = game.trade_string(), 
                        max_width = col_width, max_height = row_height, contained_widget_arguments = {'allow_filtering': False})
        self.points = self.add(npyscreen.BoxTitle, name="Point Cards", values = game.point_string(), 
                        max_width = col_width, max_height = row_height, relx = col_width + 3, rely = 2
                        , allow_filtering = False)
        self.hand = self.add(BoxTitleMultiSelect, name="Hand", footer="SPC toggle, Ctrl-U wipe", values = game.ai.hand, 
                        max_width = col_width, contained_widget_arguments = {'allow_filtering': False})
        self.cubes = self.add(npyscreen.BoxTitle, name="Cubes", values = [game.cube_string()], 
                        max_width = col_width, max_height = 6, relx = col_width + 3, rely = 11
                        , allow_filtering = False)
        self.path = self.add(npyscreen.BoxTitle, name="Path", values = ["Open Menu to Run"],
                        max_width = col_width, relx = col_width + 3, rely = 18, allow_filtering = False)
        

        action_menu = self.new_menu()
        action_menu.addItem(text = "Run", onSelect = self.update_path)
        action_menu.addItem(text = "Step Once", onSelect = self.step_path)

        replace_menu = action_menu.addNewSubmenu(name = "Replace")
        replace_menu.addItem(text = "Trade", onSelect = lambda : self.parentApp.switchForm("RTRADE"))
        replace_menu.addItem(text = "Point", onSelect = lambda : self.parentApp.switchForm("RPOINT"))

        change_menu = action_menu.addNewSubmenu(name = "Change")
        change_menu.addItem(text = "Trade", onSelect = lambda : self.parentApp.switchForm("CTRADE"))
        change_menu.addItem(text = "Point", onSelect = lambda : self.parentApp.switchForm("CPOINT"))
        change_menu.addItem(text = "Cubes", onSelect = lambda : self.parentApp.switchForm("CCUBE"))

    def beforeEditing(self):
        'Called before every time the form becomes visible (editable)'
        self.trades.values = self.parentApp.game.trade_string()
        self.points.values = self.parentApp.game.point_string()
        self.hand.values = self.parentApp.game.ai.hand
        self.cubes.values = [self.parentApp.game.cube_string()]

    def update_path(self):
        self.parentApp.game.play()
        self.path.values = Game.path_string( self.parentApp.game.path )
    
    def step_path(self):
        path = self.parentApp.game.path

        temp = path
        if temp == None or temp == [] or temp.head == None:
            return
        
        if temp.prev == None:
            follow_action(temp.head, self.parentApp.game)
            temp.head = None
        else:
            while temp.prev.prev is not None:
                temp = temp.prev
            follow_action(temp.prev.head, self.parentApp.game)
            temp.prev = None

        self.path.values = Game.path_string( self.parentApp.game.path )
        self.cubes.values = [self.parentApp.game.cube_string()]

class ReplaceTrade(npyscreen.ActionForm):
    def create(self):
        self.remove = self.add(npyscreen.TitleSelectOne, name = "Remove", values = self.parentApp.game.trade_string(),
                        max_height=8, value = [0])
        self.newCard = self.add(npyscreen.TitleText, name = "Add (ex 4,123)", value = "")
        self.message = self.add(npyscreen.FixedText)
    
    def on_ok(self):
        addCard = read_merchant_card(self.newCard.value)
        delCard = self.remove.value[0]
        if not addCard:
            self.message.value = "ERROR: Bad card formatting "
            return
        lst = self.parentApp.game.gs.merchant_list
        lst.pop(delCard)
        lst.append(addCard)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class ReplacePoint(npyscreen.ActionForm):
    def create(self):
        self.remove = self.add(npyscreen.TitleSelectOne, name = "Remove", values = self.parentApp.game.point_string(),
                        max_height=8, value = [0])
        self.newCard = self.add(npyscreen.TitleText, name = "Add (ex. 17, 123)", value = "")
        self.message = self.add(npyscreen.FixedText)
    
    
    def on_ok(self):
        addCard = read_point_card(self.newCard.value)
        delCard = self.remove.value
        if not addCard:
            self.message.value = "ERROR: Bad card formatting "
            return
        lst = self.parentApp.game.gs.point_list
        lst.pop(delCard[0])
        lst.append(addCard)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class ChangeTrade(npyscreen.ActionForm):
    def create(self):
        game = self.parentApp.game
        self.trades = self.add(npyscreen.MultiLineEditableBoxed, name="Merchant Cards", values = game.trade_string(), 
                        max_width = 29, max_height = 9)

    def on_ok(self):
        lst = self.parentApp.game.gs.merchant_list
        lst[:] = [read_merchant_card(x) for x in self.trades.values][:R['mc supply len']]
        self.parentApp.switchFormPrevious()
    
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class ChangePoint(npyscreen.ActionForm):
    def create(self):
        game = self.parentApp.game
        self.points = self.add(npyscreen.MultiLineEditableBoxed, name="Point Cards", values = game.point_string(), 
                        max_width = 29, max_height = 9)

    def on_ok(self):
        lst = self.parentApp.game.gs.point_list
        lst[:] = [read_point_card(x) for x in self.points.values][:R['pc supply len']]
        self.parentApp.switchFormPrevious()
    
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class ChangeHand(npyscreen.ActionForm):
    def create(self):
        game = self.parentApp.game
        self.hand = self.add(npyscreen.MultiLineEditableBoxed, name="Hand", values = game.hand_string(), 
                        max_width = 29)

    def on_ok(self):
        lst = self.parentApp.game.ai.hand
        lst[:] = [read_merchant_card(x) for x in self.hand.values]
        self.parentApp.switchFormPrevious()
    
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class ChangeCube(npyscreen.ActionForm):
    def create(self):
        game = self.parentApp.game
        self.cubes = self.add(npyscreen.TitleText, name="Cubes", value = game.cube_string())

    def on_ok(self):
        # lst = self.parentApp.game.ai.caravan
        self.parentApp.game.ai.caravan = Caravan([int(x) for x in re.findall('[1-4]{1}', self.cubes.value)[:R['caravan limit']]])
        self.parentApp.switchFormPrevious()
    
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

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
        return string.splitlines()[1:-1]

def follow_action(action: Action, game: Game):
    if action.type == ActionType.BUY:
        game.ai.hand.append(action.card)
        return

    if action.type == ActionType.RECLAIM:
        for card in game.ai.hand:
            card['playable'] = True
        return

    if action.type == ActionType.PLAY:

        if action.type == ActionType.PLAY:
            action.card.playable = True
            multi_plays = play_card(action.card, game.ai.caravan)
            game.ai.caravan = multi_plays[action.times - 1][1]

        for card in game.ai.hand:
            if card == action.card:
                card['playable'] = False
        return

    if action.type == ActionType.SCORE:
        remove_each(game.ai.caravan, action.card.cost)
        # for cube in action.card.cost:
        #     game.ai.caravan.remove(cube)
        return

def run():
    try:
        MyTestApp().run()
    except (EOFError,KeyboardInterrupt) as e:
        print("\nGoodbye! Play again soon")
        exit(e)
    
if __name__ == '__main__':
    run()   
    