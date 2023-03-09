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

from operator import or_
from functools import reduce

class DialogBuilder:
    partner_bitwise = None
    pre_state_string = None
    condition_tuples = []
    dialog_string = ""
    post_state_string = None
    consequence_tuples = []

    def partner(self, partner):
        """
        Set the partner for the dialog.

        Args:
            partner (Union[str, list]): The partner for the dialog. Can be a string or a list of strings.

        Returns:
            DialogBuilder: The builder object.

        Examples:
            >>> DialogBuilder().partner([anyone, plyr])
        """
        if type(partner) == str:
            partner = [partner]

        self.partner_bitwise = reduce(or_, partner)
        return self
        
    def pre_state(self, prestate):
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
    
    def post_state(self, poststate):
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
        return self.build()
    
    def build(self):
        """
        Build the dialog.

        Returns:
            list: The dialog.

        Raises:
            ValueError: If the partner is not set.
            ValueError: If the pre-state is not set.
            ValueError: If the post-state is not set.
            ValueError: If the dialog is not set.
        """
        if self.partner_bitwise is None:
            raise ValueError("partner not set")
        
        if self.pre_state_string is None:
            raise ValueError("pre_state not set")
        
        if self.post_state_string is None:
            raise ValueError("post_state not set")
        
        if self.dialog_string is None or self.dialog_string == "":
            raise ValueError("dialog not set")
        
        return [self.partner_bitwise, self.pre_state_string, self.condition_tuples, self.dialog_string, self.post_state_string, self.consequence_tuples]
    