import curses.ascii as ascii
import re

import npyscreen
from century.classes.cards import MerchantCard
from century.core.rules import RULES as R
from century.helpers.helpers import read_merchant_card, read_point_card
from century.helpers.switch import Caravan


class MultiSelectEditable(npyscreen.MultiLineEditable):
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
                    ascii.SP: self.h_select_toggle,
                    "^U":        self.h_select_none,
                } )

class BoxTitleMultiSelect(npyscreen.BoxTitle):
    _contained_widget = MultiSelectEditable

class Textfield_1t4(npyscreen.Textfield):
    def safe_to_exit(self):
        filtered = [int(x) for x in re.findall('[1-4]{1}', self.value)[:R['caravan limit']] ]
        self.find_parent_app().game.ai.caravan = Caravan(filtered)
        self.value = self.find_parent_app().game.cube_string()
        return True 

class BoxTitle_1t4(npyscreen.BoxTitle):
    _contained_widget = Textfield_1t4

class ReplaceTrade(npyscreen.ActionForm):
    def create(self):
        app = self.parentApp
        try:
            replace_index = int(app.get_message())
        except ValueError: # error when message isn't an int
            replace_index = 0
        self.remove = self.add(npyscreen.TitleSelectOne, name = "Remove", values = self.parentApp.game.trade_string(),
                        max_height=8, value = [replace_index])
        self.newCard = self.add(npyscreen.TitleText, name = "Add (ex 4,123)", value = "")
    
    def on_ok(self):
        addCard = read_merchant_card(self.newCard.value)
        delCard = self.remove.value[0]
        if not addCard or len(self.remove.values) == 0:
            return
        lst = self.parentApp.game.gs.merchant_list
        lst.pop(delCard)
        lst.append(addCard)

    def afterEditing(self):
        self.parentApp.switchFormPrevious()

class ReplacePoint(npyscreen.ActionForm):
    def create(self):
        app = self.parentApp
        try:
            replace_index = int(app.get_message())
        except ValueError: # error when message isn't an int
            replace_index = 0
        self.remove = self.add(npyscreen.TitleSelectOne, name = "Remove", values = self.parentApp.game.point_string(),
                        max_height=8, value = [replace_index])
        self.newCard = self.add(npyscreen.TitleText, name = "Add (ex. 17, 123)", value = "")
    
    
    def on_ok(self):
        addCard = read_point_card(self.newCard.value)
        delCard = self.remove.value[0]
        if not addCard or len(self.remove.values) == 0:
            return
        lst = self.parentApp.game.gs.point_list
        lst.pop(delCard)
        lst.append(addCard)
        
    def afterEditing(self):
        self.parentApp.switchFormPrevious()

class ChangeTrade(npyscreen.ActionForm):
    def create(self):
        game = self.parentApp.game
        self.trades = self.add(npyscreen.MultiLineEditableBoxed, name="Merchant Cards", values = game.trade_string(), 
                        max_width = 29, max_height = 9)

    def on_ok(self):
        lst = self.parentApp.game.gs.merchant_list
        lst[:] = [read_merchant_card(x) for x in self.trades.values][:R['mc supply len']]

    def afterEditing(self):
        self.parentApp.switchFormPrevious()

class ChangePoint(npyscreen.ActionForm):
    def create(self):
        game = self.parentApp.game
        self.points = self.add(npyscreen.MultiLineEditableBoxed, name="Point Cards", values = game.point_string(), 
                        max_width = 29, max_height = 9)

    def on_ok(self):
        lst = self.parentApp.game.gs.point_list
        lst[:] = [read_point_card(x) for x in self.points.values][:R['pc supply len']]
    
    def afterEditing(self):
        self.parentApp.switchFormPrevious()
