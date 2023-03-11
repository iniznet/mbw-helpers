# Chainable dialog methods as wrapper of implementation:
#   [trp_ramun_the_slave_trader, "start", [
#    (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
#    ], "Good day to you, {young man/lassie}.", "ramun_introduce_1",[]],
# break down to:
# 1)Dialogue partner : trp_ramun_the_slave_trader
# 2)Starting Dialog-State : "start"
# 3)Conditions block : (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
# 4) Dialog text string : "Good day to you, {young man/lassie}."
# 5) Ending dialog-state : "ramun_introduce_1"
# 6) Consequences : []

import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from operator import or_
from functools import reduce
from _imports import *

class DialogBuilder:
    dialogs = []
    partner_bitwise = None
    pre_state_string = None
    pre_state_reply_string = None
    condition_tuples = []
    dialog_string = ""
    post_state_string = None
    consequence_tuples = []

    def append(self, dialog = []):
        """
        Append a dialog to the list of dialogs and reset the builder.
        If no dialog is passed, the current dialog is appended.

        Args:
            dialog (list): The dialog to append.

        Returns:
            DialogBuilder: The builder object.

        Raises:
            ValueError: If the dialog is set and is not a list.
            ValueError: If the partner is not set.
            ValueError: If the pre-state is not set.
            ValueError: If the post-state is not set.
            ValueError: If the dialog is not set.

        Examples:
            >>> DialogBuilder().append()
        """
        if dialog != [] and type(dialog) != list:
            raise ValueError("dialog must be a list")

        if self.partner_bitwise == None:
            raise ValueError("partner must be set")
        
        if self.pre_state_string == None:
            raise ValueError("pre_state must be set")
        
        if self.post_state_string == None:
            raise ValueError("post_state must be set")
        
        if self.dialog_string == None:
            raise ValueError("dialog must be set")
        
        if dialog == []:
            dialog = [self.partner_bitwise, self.pre_state_string, self.condition_tuples, self.dialog_string, self.post_state_string, self.consequence_tuples]

        self.partner_bitwise = None
        self.pre_state_string = None
        self.condition_tuples = []
        self.dialog_string = ""
        self.post_state_string = None
        self.consequence_tuples = []

        self.dialogs.append(dialog)

        return self

    def build(self):
        """
        Build the dialog and return it.

        Returns:
            tuple: The dialog.

        Examples:
            >>> DialogBuilder().build()
        """
        return (self.partner_bitwise, self.pre_state_string, self.condition_tuples, self.dialog_string, self.post_state_string, self.consequence_tuples)
    
    def done(self):
        """
        Return the list of dialogs and reset the builder.

        Returns:
            list: The list of dialogs.

        Examples:
            >>> DialogBuilder().done()
        """
        if self.dialogs == []:
            self.append()

        dialogs = self.dialogs
        self.dialogs = []
        return dialogs

    def partner(self, partner):
        """
        Set the partner for the dialog.

        Args:
            partner (Union[int, list]): The partner for the dialog. Can be a string or a list of strings.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().partner([anyone, plyr])
        """
        self.partner_bitwise = partner

        if type(partner) == list:
            self.partner_bitwise = reduce(or_, partner)

        return self
        
    def pre_state(self, prestate, on_reply = False):
        """
        Set the pre-state for the dialog.
        
        Args:
            prestate (str): The pre-state for the dialog.
            
        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().pre_state("start")
        """
        self.pre_state_string = prestate

        if on_reply:
            self.pre_state_reply_string = prestate

        return self
    
    def condition(self, condition):
        """
        Set the condition for the dialog.

        Args:
            condition (list): The condition for the dialog.

        Returns:
            DialogBuilder: The builder object.

        Raises:
            ValueError: If the condition is not a list.

        Examples:
            >>> DialogBuilder().condition([
                    (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
                ])
        """
        if type(condition) != list:
            raise ValueError("condition must be a list")

        self.condition_tuples = condition
        return self
    
    def state(self, prestate, poststate):
        """
        Set the pre-state and post-state for the dialog.

        Args:
            prestate (str): The pre-state for the dialog.
            poststate (str): The post-state for the dialog.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().state("start", "close_window")
        """
        self.pre_state(prestate)
        self.post_state(poststate)
        return self
    
    def dialog(self, text):
        """
        Set the dialog text for the dialog.

        Args:
            text (str): The dialog text for the dialog.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().dialog("Have you come to buy or sell?")
        """
        self.dialog_string = text
        return self
    
    def post_state(self, poststate = "close_window"):
        """
        Set the post-state for the dialog.

        Args:
            poststate (str): The post-state for the dialog.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().post_state("close_window")
        """
        self.post_state_string = poststate
        return self
    
    def consequence(self, consequence):
        """
        Set the consequence for the dialog. Automatically calls build() after setting the consequence.

        Args:
            consequence (list): The consequence for the dialog.

        Returns:
            list: The dialog, returned by build().

        Raises:
            ValueError: If the consequence is not a list.

        Examples:
            >>> DialogBuilder().consequence([
                    (troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),
                ])
        """
        if type(consequence) != list:
            raise ValueError("consequence must be a list")
        
        self.consequence_tuples = consequence
        return self.append()
    
    def end(self):
        """
        Mark the end of a dialog. Useful for readability when chaining multiple dialogs together
        so you can see where one ends and the next one begins.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().end()
        """
        return self
    
    def start(self):
        """
        Start a new dialog. Useful for readability when chaining multiple dialogs together
        so you can see where one ends and the next one begins.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().start_new()
        """
        return self

    def replies_start(self, prestate = ""):
        """
        Create a reply for the last dialog you created or passed prestate and poststate.
        Useful for readability when chaining multiple replies in a parent dialog.

        Args:
            prestate (str): The pre-state for the dialog.
    
        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().replies_start("start")
        """
        self.pre_state(prestate, True)

        if prestate == "":
            self.pre_state(self.dialogs[-1][4], True)

        return self
    
    def reply(self, text, poststate = "close_window", append = True):
        """
        Create a reply for the last dialog you created or passed poststate.
        Useful for readability when chaining multiple replies in a parent dialog.

        Args:
            text (str): The dialog text for the dialog.
            poststate (str): The post-state for the dialog.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().reply("I am {playername}.", "close_window")
        """
        self.partner([anyone, plyr])
        self.pre_state(self.pre_state_reply_string)
        self.talk(text)
        self.post_state(poststate)
        
        if append:
            self.append()

        return self
    
    def replies_end(self):
        """
        Mark the end of a dialog replies. Useful for readability when chaining multiple reply in a parent dialog.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().replies_end()
        """
        return self
    