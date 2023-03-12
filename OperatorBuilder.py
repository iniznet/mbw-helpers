from _headers import *

class OperatorBuilder:
    def __init__(self):
        self.tuples = []
    
    def append(self, item):
        """
        Appends a tuple to the tuple list.

        Args:
            item (tuple): Tuple to append

        Returns:
            TupleBuilder: self

        Example:
            >>> append((call_script, "script_name"))
        """
        self.tuples.append(item)
        return self

    # Simple operation tuple
    def tuple(self, *args):
        """
        Appends a tuple to the tuple list.

        Args:
            args (any): Tuple to append

        Returns:
            TupleBuilder: self

        Example:
            >>> tuple(call_script, "script_name")
        """
        operation = (args)
        flattened_operation = tuple(j for i in operation for j in (i if type(i) is tuple else (i,)))

        return self.append(flattened_operation)

    # All done? call this to get the tuple list
    def done(self):
        """
        Returns:
            list: Tuple list

        Example:
            >>> build()
        """
        return self.tuples

    ################################################################################
    # [ Z01 ] OPERATION MODIFIERS
    ################################################################################

    ################################################################################
    # [ Z02 ] FLOW CONTROL
    ################################################################################

    def call_script(self, script, *args):
        """
        Calls specified script with or without parameters. Maximum number of parameters you can pass with the operation is 16.
        
        Args:
            script (str): Script name
            args (any): Script parameters (optional)

        Returns:
            TupleBuilder: self

        Raises:
            ValueError: If you pass more than 16 parameters to the script

        Example:
            >>> call_script("script_name", "param1", "param2", and so on...)
        """
        if len(args) > 16:
            raise ValueError("Maximum number of parameters you can pass with the operation is 16.")
        
        operation = (call_script, script, args)
        flattened_operation = tuple(j for i in operation for j in (i if type(i) is tuple else (i,)))

        return self.append(flattened_operation)
        
    def try_begin(self):
        """
        (try_begin),
        Opens a conditional block.

        Returns:
            TupleBuilder: self

        Example:
            >>> try_begin()
        """
        return self.append((try_begin))

    def else_try(self):
        """
        (else_try),
        If conditional operations in the conditional block fail, this block of code will be executed.

        Returns:
            TupleBuilder: self

        Example:
            >>> else_try()
        """
        return self.append((else_try))

    def else_try_begin(self, variable):
        """
        (else_try_begin),
        Deprecated form of (else_try).

        Returns:
            TupleBuilder: self

        Example:
            >>> else_try_begin()
        """
        return self.append((else_try_begin))

    def try_end(self):
        """
        (try_end),
        Concludes a conditional block or a cycle.

        Returns:
            TupleBuilder: self

        Example:
            >>> try_end()
        """
        return self.append((try_end))

    def end_try(self):
        """
        (end_try),
        Deprecated form of (try_end),

        Returns:
            TupleBuilder: self

        Example:
            >>> end_try()
        """
        return self.append((end_try))

    def try_for_range(self, iterable, lower_bound, upper_bound):
        """
        (try_for_range, <destination>, <lower_bound>, <upper_bound>),
        Runs a cycle, iterating the value in the <lower_bound>..<upper_bound>-1 range.

        Args:
            iterable (any): Variable to iterate
            lower_bound (str|int): Lower bound to start iterating from
            upper_bound (str|int): Upper bound to stop iterating at

        Returns:
            TupleBuilder: self

        Example:
            >>> try_for_range(":cur_center", centers_begin, centers_end)
        """
        return self.append((try_for_range, iterable, lower_bound, upper_bound))

    def try_for_range_backwards(self, iterable, lower_bound, upper_bound):
        """
        (try_for_range_backwards, <destination>, <lower_bound>, <upper_bound>),
        Same as above, but iterates the value in the opposite direction (from higher values to lower).

        Args:
            iterable (str): Variable to iterate
            lower_bound (str|int): Lower bound to stop iterating at
            upper_bound (str|int): Upper bound to start iterating from

        Returns:
            TupleBuilder: self

        Example:
            >>> try_for_range_backwards(":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end)
        """
        return self.append((try_for_range_backwards, iterable, lower_bound, upper_bound))

    def try_for_parties(self, iterable):
        """
        (try_for_parties, <destination>),
        Runs a cycle, iterating all parties on the map.

        Args:
            iterable (str): Variable to iterate

        Returns:
            TupleBuilder: self

        Example:
            >>> try_for_parties(":cur_party")
        """
        return self.append((try_for_parties, iterable))

    def try_for_agents(self, iterable):
        """
        (try_for_agents, <destination>),
        Runs a cycle, iterating all agents on the scene.

        Args:
            iterable (str): Variable to iterate

        Returns:
            TupleBuilder: self

        Example:
            >>> try_for_agents(":cur_agent")
        """
        return self.append((try_for_agents, iterable))

    def try_for_prop_instances(self, iterable, **args):
        """
        (try_for_prop_instances, <destination>, [<scene_prop_id>]),
        Version 1.161+. Runs a cycle, iterating all scene prop instances on the scene, or all scene prop instances of specific type if optional parameter is provided.

        Args:
            iterable (str): Variable to iterate

        Returns:
            TupleBuilder: self

        Example:
            >>> try_for_prop_instances(":props", "spr_cannon)
        """
        operation = (try_for_prop_instances, iterable, args)
        flattened_operation = tuple(j for i in operation for j in (i if type(i) is tuple else (i,)))

        return self.append(flattened_operation)

    def try_for_players(self, iterable, skip_server = 0):
        """
        (try_for_players, <destination>, [skip_server]),
        Version 1.165+. Iterates through all players in a multiplayer game. Set optional parameter to 1 to skip server player entry.

        Args:
            iterable (str): Variable to iterate
            skip_server (Union[int, bool]): Whether to skip server player entry, bool will be converted to int

        Returns:
            TupleBuilder: self

        Example:
            >>> try_for_players(":player")
        """
        if type(skip_server) is bool:
            skip_server = int(skip_server)

        return self.append((try_for_players, iterable, skip_server))

    ################################################################################
    # [ Z03 ] MATHEMATICAL OPERATIONS
    ################################################################################

    # Mathematical operations deal with numbers. Warband Module System can only
    # deal with integers. Floating point numbers are emulated by the so-called
    # "fixed point numbers". Wherever you encounter a fixed point parameter for
    # some Module System operation, keep in mind that it is actually just a
    # regular integer number, HOWEVER it is supposed to represent a floating
    # point number equal to fixed_point_number / fixed_point_multiplier. As you
    # might have guessed, to convert a floating point number to fixed point, you
    # have to multiply it by fixed_point_multiplier. You can change the value of
    # multiplier with the operation (set_fixed_point_multiplier), thus influencing
    # the precision of all operations dealing with fixed point numbers.

    # A notion very important for Warband modding is that you reference all
    # Warband objects by their numeric values. In other words, you can do maths
    # with your items, troops, agents, scenes, parties et cetera. This is used
    # extensively in the code, so don't be surprised to see code looking like
    # (store_add, ":value", "itm_pike", 4). This code is just calculating a
    # reference to an item which is located 4 positions after "itm_pike" inside
    # the module_items.py file.

    # Conditional operations

    def gt(self, value1, value2):
        """
        (gt, <value1>, <value2>),
        Checks that value1 > value2

        Args:
            value1 (str|int): First value to compare
            value2 (str|int): Second value to compare

        Returns:
            TupleBuilder: self

        Example:
            >>> gt(1, ":variable_contain_number_two")
        """
        return self.append((gt, value1, value2))

    def ge(self, value1, value2):
        """
        (ge, <value1>, <value2>),
        Checks that value1 >= value2

        Args:
            value1 (str|int): First value to compare
            value2 (str|int): Second value to compare

        Returns:
            TupleBuilder: self

        Example:
            >>> ge(1, ":variable_contain_number_two")
        """
        return self.append((ge, value1, value2))

    def eq(self, value1, value2):
        """
        (eq, <value1>, <value2>),
        Checks that value1 == value2

        Args:
            value1 (str|int): First value to compare
            value2 (str|int): Second value to compare

        Returns:
            TupleBuilder: self

        Example:
            >>> eq(1, ":variable_contain_number_two")
        """
        return self.append((eq, value1, value2))

    def neq(self, value1, value2):
        """
        (neq, <value1>, <value2>),
        Checks that value1 != value2

        Args:
            value1 (str|int): First value to compare
            value2 (str|int): Second value to compare

        Returns:
            TupleBuilder: self

        Example:
            >>> neq(2, ":variable_contain_number_two")
        """
        return self.append((neq, value1, value2))

    def le(self, value1, value2):
        """
        (le, <value1>, <value2>),
        Checks that value1 <= value2

        Args:
            value1 (str|int): First value to compare
            value2 (str|int): Second value to compare

        Returns:
            TupleBuilder: self

        Example:
            >>> le(2, ":variable_contain_number_two")
        """
        return self.append((le, value1, value2))

    def lt(self, value1, value2):
        """
        (lt, <value1>, <value2>),
        Checks that value1 < value2

        Args:
            value1 (str|int): First value to compare
            value2 (str|int): Second value to compare

        Returns:
            TupleBuilder: self

        Example:
            >>> lt(2, ":variable_contain_number_three")
        """
        return self.append((lt, value1, value2))

    def is_between(self, value, lower_bound, upper_bound):
        """
        (is_between, <value>, <lower_bound>, <upper_bound>),
        Checks that lower_bound <= value < upper_bound

        Args:
            value (str|int): Value to check
            lower_bound (str|int): Lower bound to check
            upper_bound (str|int): Upper bound to check

        Returns:
            TupleBuilder: self

        Example:
            >>> is_between(":variable_one", 0, 2)
        """
        return self.append((is_between, value, lower_bound, upper_bound))

    # Mathematical and assignment operations

    def assign(self, variable, value):
        """
        (assign, <destination>, <value>),
        Directly assigns a value to a variable or register.

        Args:
            variable (str|int): Variable to assign to
            value (any): Value to assign


        Returns:
            TupleBuilder: self

        Example:
            >>> assign("$g_ally_strength", reg0)
        """
        return self.append((assign, variable, value))

    def store_add(self, variable, value1, value2):
        """
        (store_add, <destination>, <value>, <value>),
        Assigns <destination> := <value> + <value>

        Args:
            variable (str|int): Variable to assign to
            value1 (str|int): First value to add
            value2 (str|int): Second value to add

        Returns:
            TupleBuilder: self

        Example:
            >>> store_add(":cur_object_no", "scn_town_1_prison", ":offset")
        """
        return self.append((store_add, variable, value1, value2))

    def store_sub(self, variable, value1, value2):
        """
        (store_sub, <destination>, <value>, <value>),
        Assigns <destination> := <value> - <value>

        Args:
            variable (str|int): Variable to assign to
            value1 (str|int): First value to subtract
            value2 (str|int): Second value to subtract

        Returns:
            TupleBuilder: self

        Example:
            >>> store_sub(":difference", 20, ":cur_relation")
        """
        return self.append((store_sub, variable, value1, value2))

    def store_mul(self, variable, value1, value2):
        """
        (store_mul, <destination>, <value>, <value>),
        Assigns <destination> := <value> * <value>

        Args:
            variable (str|int): Variable to assign to
            value1 (str|int): First value to multiply
            value2 (str|int): Second value to multiply

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mul(":difference", 2, ":cur_relation")
        """
        return self.append((store_mul, variable, value1, value2))

    def store_div(self, variable, value1, value2):
        """
        (store_div, <destination>, <value>, <value>),
        Assigns <destination> := <value> / <value>

        Args:
            variable (str|int): Variable to assign to
            value1 (str|int): First value to divide
            value2 (str|int): Second value to divide

        Returns:
            TupleBuilder: self

        Example:
            >>> store_div(":difference", 2, ":cur_relation")
        """
        return self.append((store_div, variable, value1, value2))

    def store_mod(self, variable, value1, value2):
        """
        (store_mod, <destination>, <value>, <value>),
        Assigns <destination> := <value> MOD <value>

        Args:
            variable (str|int): Variable to assign to
            value1 (str|int): First value to divide
            value2 (str|int): Second value to divide

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mod(":cur_hours_mod", ":cur_hours", 11)
        """
        return self.append((store_mod, variable, value1, value2))

    def val_add(self, variable, value):
        """
        (val_add, <destination>, <value>),
        Assigns <destination> := <destination> + <value>

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_add(":screening_party_score")
        """
        return self.append((val_add, variable, value))

    def val_sub(self, variable, value):
        """
        (val_sub, <destination>, <value>),
        Assigns <destination> := <destination> - <value>

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_sub(":screening_party_score")
        """
        return self.append((val_sub, variable, value))

    def val_mul(self, variable):
        """
        (val_mul, <destination>, <value>),
        Assigns <destination> := <destination> * <value>

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_mul(":screening_party_score")
        """
        return self.append((val_mul, variable))

    def val_div(self, variable, value):
        """
        (val_div, <destination>, <value>),
        Assigns <destination> := <destination> / <value>

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_div(":screening_party_score")
        """
        return self.append((val_div, variable, value))

    def val_mod(self, variable, value):
        """
        (val_mod, <destination>, <value>),
        Assigns <destination> := <destination> MOD <value>

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_mod(":screening_party_score")
        """
        return self.append((val_mod, variable, value))

    def val_min(self, variable, value):
        """
        (val_min, <destination>, <value>),
        Assigns <destination> := MIN (<destination>, <value>)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_min(":screening_party_score")
        """
        return self.append((val_min, variable, value))

    def val_max(self, variable, value):
        """
        (val_max, <destination>, <value>),
        Assigns <destination> := MAX (<destination>, <value>)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_max(":screening_party_score")
        """
        return self.append((val_max, variable, value))

    def val_clamp(self, variable, lower_bound, upper_bound):
        """
        (val_clamp, <destination>, <lower_bound>, <upper_bound>),
        Enforces <destination> value to be within <lower_bound>..<upper_bound>-1 range.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_clamp(":screening_party_score")
        """
        return self.append((val_clamp, variable, lower_bound, upper_bound))

    def val_abs(self, variable):
        """
        (val_abs, <destination>),
        Assigns <destination> := ABS (<destination>)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_abs(":screening_party_score")
        """
        return self.append((val_abs, variable))

    def store_or(self, variable, value1, value2):
        """
        (store_or, <destination>, <value>, <value>),
        Binary OR

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_or(":screening_party_score")
        """
        return self.append((store_or, variable, value1, value2))

    def store_and(self, variable, value1, value2):
        """
        (store_and, <destination>, <value>, <value>),
        Binary AND

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_and(":screening_party_score")
        """
        return self.append((store_and, variable, value1, value2))

    def val_or(self, variable, value):
        """
        (val_or, <destination>, <value>),
        Binary OR, overwriting first operand.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_or(":screening_party_score")
        """
        return self.append((val_or, variable, value))

    def val_and(self, variable, value):
        """
        (val_and, <destination>, <value>),
        Binary AND, overwriting first operand.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_and(":screening_party_score")
        """
        return self.append((val_and, variable, value))

    def val_lshift(self, variable, value):
        """
        (val_lshift, <destination>, <value>),
        Bitwise shift left (dest = dest * 2 ^ value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_lshift(":screening_party_score")
        """
        return self.append((val_lshift, variable, value))

    def val_rshift(self, variable, value):
        """
        (val_rshift, <destination>, <value>),
        Bitwise shift right (dest = dest / 2 ^ value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> val_rshift(":screening_party_score")
        """
        return self.append((val_rshift, variable, value))

    def store_sqrt(self, destinaton, value):
        """
        (store_sqrt, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := SQRT (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_sqrt(":screening_party_score")
        """
        return self.append((store_sqrt, destinaton, value))

    def store_pow(self, destinaton, value, power):
        """
        (store_pow, <destination_fixed_point>, <value_fixed_point>, <power_fixed_point),
        Assigns dest := value ^ power

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_pow(":screening_party_score")
        """
        return self.append((store_pow, destinaton, value, power))

    def store_sin(self, destinaton, value):
        """
        (store_sin, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := SIN (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_sin(":screening_party_score")
        """
        return self.append((store_sin, destinaton, value))

    def store_cos(self, destinaton, value):
        """
        (store_cos, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := COS (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_cos(":screening_party_score")
        """
        return self.append((store_cos, destinaton, value))

    def store_tan(self, destinaton, value):
        """
        (store_tan, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := TAN (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_tan(":screening_party_score")
        """
        return self.append((store_tan, destinaton, value))

    def store_asin(self, destinaton, value):
        """
        (store_asin, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := ARCSIN (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_asin(":screening_party_score")
        """
        return self.append((store_asin, destinaton, value))

    def store_acos(self, destinaton, value):
        """
        (store_acos, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := ARCCOS (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_acos(":screening_party_score")
        """
        return self.append((store_acos, destinaton, value))

    def store_atan(self, destinaton, value):
        """
        (store_atan, <destination_fixed_point>, <value_fixed_point>),
        Assigns dest := ARCTAN (value)

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_atan(":screening_party_score")
        """
        return self.append((store_atan, destinaton, value))

    def store_atan2(self, destinaton, y, x):
        """
        (store_atan2, <destination_fixed_point>, <y_fixed_point>, <x_fixed_point>),
        Returns the angle between the x axis and a point with coordinates (X,Y) in degrees. Note the angle is calculated counter-clockwise, i.e. (1,1) will return 45, not -45.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_atan2(":screening_party_score")
        """
        return self.append((store_atan2, destinaton, y, x))

    # Random number generation

    def store_random(self, destination, upper_range):
        """
        (store_random, <destination>, <upper_range>),
        Stores a random value in the range of 0..<upper_range>-1. Deprecated, use (store_random_in_range) instead.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random(":screening_party_score")
        """
        return self.append((store_random, destination, upper_range))

    def store_random_in_range(self, destination, range_low, range_high):
        """
        (store_random_in_range, <destination>, <range_low>, <range_high>),
        Stores a random value in the range of <range_low>..<range_high>-1.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_in_range(":screening_party_score")
        """
        return self.append((store_random_in_range, destination, range_low, range_high))

    def shuffle_range(self, reg1, reg2):
        """
        (shuffle_range, <reg_no>, <reg_no>),
        Randomly shuffles a range of registers, reordering the values contained in them. Commonly used for list randomization.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> shuffle_range(":screening_party_score")
        """
        return self.append((shuffle_range, reg1, reg2))

    # Fixed point values handling

    def set_fixed_point_multiplier(self, value):
        """
        (set_fixed_point_multiplier, <value>),
        Affects all operations dealing with fixed point numbers. Default value is 1.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> set_fixed_point_multiplier(":screening_party_score")
        """
        return self.append((set_fixed_point_multiplier, value))

    def convert_to_fixed_point(self, destination):
        """
        (convert_to_fixed_point, <destination_fixed_point>),
        Converts integer value to fixed point (multiplies by the fixed point multiplier).

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> convert_to_fixed_point(":screening_party_score")
        """
        return self.append((convert_to_fixed_point, destination))

    def convert_from_fixed_point(self, destination):
        """
        (convert_from_fixed_point, <destination>),
        Converts fixed point value to integer (divides by the fixed point multiplier).

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> convert_from_fixed_point(":screening_party_score")
        """
        return self.append((convert_from_fixed_point, destination))

    ################################################################################
    # [ Z04 ] SCRIPT/TRIGGER PARAMETERS AND RESULTS
    ################################################################################

    # Many scripts can accept additional parameters, and many triggers have some
    # parameters of their own (as details in header_triggers.py file). You can
    # only pass numeric values as parameters. Since string constants are also
    # Warband objects, you can pass them as well, and you can also pass string
    # or position registers. However you cannot pass quick strings (string
    # defined directly in the code).

    # You can declare your scripts with as many parameters as you wish. Triggers,
    # however, are always called with their predefined parameters. Also the game
    # engine does not support more than 3 parameters per trigger. As the result,
    # some triggers receive extra information which could not be fit into those
    # three parameters in numeric, string or position registers.

    # Some triggers and scripts called from the game engine (those have names
    # starting with "game_") expect you to return some value to the game engine.
    # That value may be either a number or a string and is set by special
    # operations listed below. Scripts called from the Module System, however,
    # typically use registers to store their return data.

    # Note that if you call a script from a trigger, you can still use operations
    # to retrieve trigger's calling parameters, and they will retrieve values that
    # have been passed to the trigger, not values that have been passed to the
    # script.

    def store_script_param_1(self, destination):
        """
        (store_script_param_1, <destination>),
        Retrieve the value of the first script parameter.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_script_param_1(":screening_party_score")
        """
        return self.append((store_script_param_1, destination))

    def store_script_param_2(self, destination):
        """
        (store_script_param_2, <destination>),
        Retrieve the value of the second script parameter.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_script_param_2(":screening_party_score")
        """
        return self.append((store_script_param_2, destination))

    def store_script_param(self, destination, script_index):
        """
        (store_script_param, <destination>, <script_param_index>),
        Retrieve the value of arbitrary script parameter (generally used when script accepts more than two). Parameters are enumerated starting from 1.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_script_param(":screening_party_score")
        """
        return self.append((store_script_param, destination, script_index))

    def set_result_string(self, string):
        """
        (set_result_string, <string>),
        Sets the return value of a game_* script, when a string value is expected by game engine.

        Args:
            string (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> set_result_string(":screening_party_score")
        """
        return self.append((set_result_string, string))

    def store_trigger_param_1(self, destination):
        """
        (store_trigger_param_1, <destination>),
        Retrieve the value of the first trigger parameter. Will retrieve trigger's parameters even when called from inside a script, for as long as that script is running within trigger context.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_trigger_param_1(":screening_party_score")
        """
        return self.append((store_trigger_param_1, destination))

    def store_trigger_param_2(self, destination):
        """
        (store_trigger_param_2, <destination>),
        Retrieve the value of the second trigger parameter. Will retrieve trigger's parameters even when called from inside a script, for as long as that script is running within trigger context.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_trigger_param_2(":screening_party_score")
        """
        return self.append((store_trigger_param_2, destination))

    def store_trigger_param_3(self, destination):
        """
        (store_trigger_param_3, <destination>),
        Retrieve the value of the third trigger parameter. Will retrieve trigger's parameters even when called from inside a script, for as long as that script is running within trigger context.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_trigger_param_3(":screening_party_score")
        """
        return self.append((store_trigger_param_3, destination))

    def store_trigger_param(self, destination, trigger_no):
        """
        (store_trigger_param, <destination>, <trigger_param_no>),
        Version 1.153+. Retrieve the value of arbitrary trigger parameter. Parameters are enumerated starting from 1. Note that despite the introduction of this operation, there's not a single trigger with more than 3 parameters.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_trigger_param(":screening_party_score")
        """
        return self.append((store_trigger_param, destination, trigger_no))

    def get_trigger_object_position(self, position):
        """
        (get_trigger_object_position, <position>),
        Retrieve the position of an object which caused the trigger to fire (when appropriate).

        Args:
            position (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> get_trigger_object_position(":screening_party_score")
        """
        return self.append((get_trigger_object_position, position))

    def set_trigger_result(self, value):
        """
        (set_trigger_result, <value>),
        Sets the return value of a trigger or game_* script, when an integer value is expected by game engine.

        Args:
            value (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> set_trigger_result(":screening_party_score")
        """
        return self.append((set_trigger_result, value))

    ################################################################################
    # [ Z05 ] KEYBOARD AND MOUSE INPUT
    ################################################################################

    # The game provides modders with limited ability to control keyboard input and
    # mouse movements. It is also possible to tamper with game keys (i.e. keys
    # bound to specific game actions), including the ability to override game's
    # reaction to those keys. Note that mouse buttons are keys too, and can be
    # detected with the corresponding operations.

    # Conditional operations

    def key_is_down(self, key_code):
        """
        (key_is_down, <key_code>),
        Checks that the specified key is currently pressed. See header_triggers.py for key code reference.

        Args:
            key_code (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> key_is_down(":screening_party_score")
        """
        return self.append((key_is_down, key_code))

    def key_clicked(self, key_code):
        """
        (key_clicked, <key_code>),
        Checks that the specified key has just been pressed. See header_triggers.py for key code reference.

        Args:
            key_code (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> key_clicked(":screening_party_score")
        """
        return self.append((key_clicked, key_code))

    def game_key_is_down(self, game_key_code):
        """
        (game_key_is_down, <game_key_code>),
        Checks that the specified game key is currently pressed. See header_triggers.py for game key code reference.

        Args:
            game_key_code (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> game_key_is_down(":screening_party_score")
        """
        return self.append((game_key_is_down, game_key_code))

    def game_key_clicked(self, game_key_code):
        """
        (game_key_clicked, <game_key_code>),
        Checks that the specified key has just been pressed. See header_triggers.py for game key code reference.

        Args:
            game_key_code (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> game_key_clicked(":screening_party_score")
        """
        return self.append((game_key_clicked, game_key_code))

    # Generic operations

    def omit_key_once(self, key_code):
        """
        (omit_key_once, <key_code>),
        Forces the game to ignore default bound action for the specified game key on current game frame.

        Args:
            key_code (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> omit_key_once(":screening_party_score")
        """
        return self.append((omit_key_once, key_code))

    def clear_omitted_keys(self):
        """
        (clear_omitted_keys),
        Commonly called when exiting from a presentation which made any calls to (omit_key_once). However the effects of those calls disappear by the next frame, so apparently usage of this operation is not necessary. It is still recommended to be on the safe side though.

        Returns:
            TupleBuilder: self

        Example:
            >>> clear_omitted_keys()
        """
        return self.append((clear_omitted_keys))

    def mouse_get_position(self, position):
        """
        (mouse_get_position, <position>),
        Stores mouse x and y coordinates in the specified position.

        Args:
            position (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> mouse_get_position(":screening_party_score")
        """
        return self.append((mouse_get_position, position))

    ################################################################################
    # [ Z06 ] WORLD MAP
    ################################################################################

    # Generally, all operations which only make sense on the worldmap and have no
    # specific category have been assembled here. These mostly deal with weather,
    # time and resting.

    # Conditional operations

    def is_currently_night(self):
        """
        (is_currently_night),
        Checks that it's currently night in the game.

        Returns:
            TupleBuilder: self

        Example:
            >>> is_currently_night()
        """
        return self.append((is_currently_night))

    def map_free(self):
        """
        (map_free),
        Checks that the player is currently on the global map and no game screens are open.

        Returns:
            TupleBuilder: self

        Example:
            >>> map_free(":screening_party_score")
        """
        return self.append((map_free))

    # Weather-handling operations

    def get_global_cloud_amount(self, destination):
        """
        (get_global_cloud_amount, <destination>),
        Returns current cloudiness (a value between 0..100).

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> get_global_cloud_amount(":screening_party_score")
        """
        return self.append((get_global_cloud_amount, destination))

    def set_global_cloud_amount(self, value):
        """
        (set_global_cloud_amount, <value>),
        Sets current cloudiness (value is clamped to 0..100).

        Args:
            value (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> set_global_cloud_amount(":screening_party_score")
        """
        return self.append((set_global_cloud_amount, value))

    def get_global_haze_amount(self, destination):
        """
        (get_global_haze_amount, <destination>),
        Returns current fogginess (value between 0..100).

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> get_global_haze_amount(":screening_party_score")
        """
        return self.append((get_global_haze_amount, destination))

    def set_global_haze_amount(self, value):
        """
        (set_global_haze_amount, <value>),
        Sets current fogginess (value is clamped to 0..100).

        Args:
            value (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> set_global_haze_amount(":screening_party_score")
        """
        return self.append((set_global_haze_amount, value))

    # Time-related operations

    def store_current_hours(self, destination):
        """
        (store_current_hours, <destination>),
        Stores number of hours that have passed since beginning of the game. Commonly used to track time when accuracy up to hours is required.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_current_hours(":screening_party_score")
        """
        return self.append((store_current_hours, destination))

    def store_time_of_day(self, destination):
        """
        (store_time_of_day, <destination>),
        Stores current day hour (value in 0..24 range).

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_time_of_day(":screening_party_score")
        """
        return self.append((store_time_of_day, destination))

    def store_current_day(self, destination):
        """
        (store_current_day, <destination>),
        Stores number of days that have passed since beginning of the game. Commonly used to track time when high accuracy is not required.

        Args:
            destination (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> store_current_day(":screening_party_score")
        """
        return self.append((store_current_day, destination))

    def rest_for_hours(self, rest_time_in_hours_var = 0, time_speed_multiplier = 0, remain_attackable = 0):
        """
        (rest_for_hours, <rest_time_in_hours>, [time_speed_multiplier], [remain_attackable]),
        Forces the player party to rest for specified number of hours. Time can be accelerated and player can be made immune or subject to attacks.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> rest_for_hours(":screening_party_score")
        """
        return self.append((rest_for_hours, rest_time_in_hours_var, time_speed_multiplier, remain_attackable))

    def rest_for_hours_interactive(self, rest_time_in_hours_var = 0, time_speed_multiplier = 0, remain_attackable = 0):
        """
        (rest_for_hours_interactive, <rest_time_in_hours>, [time_speed_multiplier], [remain_attackable]),
        Forces the player party to rest for specified number of hours. Player can break the rest at any moment. Time can be accelerated and player can be made immune or subject to attacks.

        Args:
            variable (str|int): Variable to assign to

        Returns:
            TupleBuilder: self

        Example:
            >>> rest_for_hours_interactive(":screening_party_score")
        """
        return self.append((rest_for_hours_interactive, rest_time_in_hours_var, time_speed_multiplier, remain_attackable))

    ################################################################################
    # [ Z07 ] GAME SETTINGS AND STATISTICS
    ################################################################################

    # This group of operations allows you to retrieve some of the game settings
    # as configured by the player on Options page, and change them as necessary
    # (possibly forcing a certain level of difficulty on the player). Operations
    # dealing with achievements (an interesting, but underdeveloped feature of
    # Warband) are also placed in this category.

    # Conditional operations

    def is_trial_version(self):
        """
        (is_trial_version),
        Checks if the game is in trial mode (has not been purchased). Player cannot get higher than level 6 in this mode.

        Returns:
            TupleBuilder: self

        Example:
            >>> is_trial_version(rest_time_in_hours, time_speed_multiplier, remain_attackable)
        """
        return self.append((is_trial_version))
        
    def is_edit_mode_enabled(self):
        """
        (is_edit_mode_enabled),
        Version 1.153+. Checks that Edit Mode is currently enabled in the game.

        Returns:
            TupleBuilder: self

        Example:
            >>> is_edit_mode_enabled(rest_time_in_hours, time_speed_multiplier, remain_attackable)
        """
        return self.append((is_edit_mode_enabled))
        
    def get_operation_set_version(self, destination):
        """
        (get_operation_set_version, <destination>),
        Version 1.165+. 4research. Apparently returns the current version of Module System operations set, allowing transparent support for multiple Warband engine versions.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_operation_set_version(destination)
        """
        return self.append((get_operation_set_version, destination))
        
    def set_player_troop(self, troop_id):
        """
        (set_player_troop, <troop_id>),
        Changes the troop player controls. Generally used in quick-battle scenarios to give player a predefined character.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_player_troop(troop_id)
        """
        return self.append((set_player_troop, troop_id))
        
    def show_object_details_overlay(self, value):
        """
        (show_object_details_overlay, <value>),
        Turns various popup tooltips on (value = 1) and off (value = 0). This includes agent names and dropped item names during missions, item stats in inventory on mouse over, etc.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> show_object_details_overlay(value)
        """
        return self.append((show_object_details_overlay, value))
        
    def auto_save(self):
        """
        (auto_save),
        Version 1.161+. Saves the game to the current save slot.

        Returns:
            TupleBuilder: self

        Example:
            >>> auto_save(value)
        """
        return self.append((auto_save))
        
    def options_get_damage_to_player(self, destination):
        """
        (options_get_damage_to_player, <destination>),
        0 = 1/4, 1 = 1/2, 2 = 1/1

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_get_damage_to_player(destination)
        """
        return self.append((options_get_damage_to_player, destination))
        
    def options_set_damage_to_player(self, value):
        """
        (options_set_damage_to_player, <value>),
        0 = 1/4, 1 = 1/2, 2 = 1/1

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_set_damage_to_player(value)
        """
        return self.append((options_set_damage_to_player, value))
        
    def options_get_damage_to_friends(self, destination):
        """
        (options_get_damage_to_friends, <destination>),
        0 = 1/2, 1 = 3/4, 2 = 1/1

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_get_damage_to_friends(destination)
        """
        return self.append((options_get_damage_to_friends, destination))
        
    def options_set_damage_to_friends(self, value):
        """
        (options_set_damage_to_friends, <value>),
        0 = 1/2, 1 = 3/4, 2 = 1/1

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_set_damage_to_friends(value)
        """
        return self.append((options_set_damage_to_friends, value))
        
    def options_get_combat_ai(self, destination):
        """
        (options_get_combat_ai, <destination>),
        0 = good, 1 = average, 2 = poor

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_get_combat_ai(destination)
        """
        return self.append((options_get_combat_ai, destination))
        
    def options_set_combat_ai(self, value):
        """
        (options_set_combat_ai, <value>),
        0 = good, 1 = average, 2 = poor

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_set_combat_ai(value)
        """
        return self.append((options_set_combat_ai, value))
        
    def game_get_reduce_campaign_ai(self, destination):
        """
        (game_get_reduce_campaign_ai, <destination>),
        Deprecated operation. Use options_get_campaign_ai instead

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> game_get_reduce_campaign_ai(destination)
        """
        return self.append((game_get_reduce_campaign_ai, destination))
        
    def options_get_campaign_ai(self, destination):
        """
        (options_get_campaign_ai, <destination>),
        0 = good, 1 = average, 2 = poor

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_get_campaign_ai(destination)
        """
        return self.append((options_get_campaign_ai, destination))
        
    def options_set_campaign_ai(self, value):
        """
        (options_set_campaign_ai, <value>),
        0 = good, 1 = average, 2 = poor

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_set_campaign_ai(value)
        """
        return self.append((options_set_campaign_ai, value))
        
    def options_get_combat_speed(self, destination):
        """
        (options_get_combat_speed, <destination>),
        0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_get_combat_speed(destination)
        """
        return self.append((options_get_combat_speed, destination))
        
    def options_set_combat_speed(self, value):
        """
        (options_set_combat_speed, <value>),
        0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_set_combat_speed(value)
        """
        return self.append((options_set_combat_speed, value))
        
    def options_get_battle_size(self, destination):
        """
        (options_get_battle_size, <destination>),
        Version 1.161+. Retrieves current battle size slider value (in the range of 0..1000). Note that this is the slider value, not the battle size itself.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_get_battle_size(destination)
        """
        return self.append((options_get_battle_size, destination))
        
    def options_set_battle_size(self, value):
        """
        (options_set_battle_size, <value>),
        Version 1.161+. Sets battle size slider to provided value (in the range of 0..1000). Note that this is the slider value, not the battle size itself.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> options_set_battle_size(value)
        """
        return self.append((options_set_battle_size, value))
        
    def get_average_game_difficulty(self, destination):
        """
        (get_average_game_difficulty, <destination>),
        Returns calculated game difficulty rating (as displayed on the Options page). Commonly used for score calculation when ending the game.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_average_game_difficulty(destination)
        """
        return self.append((get_average_game_difficulty, destination))
        
    def get_achievement_stat(self, destination, achievement_id, stat_index):
        """
        (get_achievement_stat, <destination>, <achievement_id>, <stat_index>),
        Retrieves the numeric value associated with an achievement. Used to keep track of player's results before finally unlocking it.

		Args:
			destination (str|int):
			achievement_id (str|int):
			stat_index (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_achievement_stat(destination, achievement_id, stat_index)
        """
        return self.append((get_achievement_stat, destination, achievement_id, stat_index))
        
    def set_achievement_stat(self, achievement_id, stat_index, value):
        """
        (set_achievement_stat, <achievement_id>, <stat_index>, <value>),
        Sets the new value associated with an achievement. Used to keep track of player's results before finally unlocking it.

		Args:
			achievement_id (str|int):
			stat_index (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_achievement_stat(achievement_id, stat_index, value)
        """
        return self.append((set_achievement_stat, achievement_id, stat_index, value))
        
    def unlock_achievement(self, achievement_id):
        """
        (unlock_achievement, <achievement_id>),
        Unlocks player's achievement. Apparently doesn't have any game effects.

		Args:
			achievement_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> unlock_achievement(achievement_id)
        """
        return self.append((unlock_achievement, achievement_id))
        
    def get_player_agent_kill_count(self, destination, get_wounded):
        """
        (get_player_agent_kill_count, <destination>, [get_wounded]),
        Retrieves the total number of enemies killed by the player. Call with non-zero <get_wounded> parameter to retrieve the total number of knocked down enemies.

		Args:
			destination (str|int):
			get_wounded (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_player_agent_kill_count(destination, get_wounded)
        """
        return self.append((get_player_agent_kill_count, destination, get_wounded))
        
    def get_player_agent_own_troop_kill_count(self, destination, get_wounded):
        """
        (get_player_agent_own_troop_kill_count, <destination>, [get_wounded]),
        Retrieves the total number of allies killed by the player. Call with non-zero <get_wounded> parameter to retrieve the total number of knocked down allies.

		Args:
			destination (str|int):
			get_wounded (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_player_agent_own_troop_kill_count(destination, get_wounded)
        """
        return self.append((get_player_agent_own_troop_kill_count, destination, get_wounded))
        
    def faction_set_slot(self, faction_id, slot_no, value):
        """
        (faction_set_slot, <faction_id>, <slot_no>, <value>),
        

		Args:
			faction_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_set_slot(faction_id, slot_no, value)
        """
        return self.append((faction_set_slot, faction_id, slot_no, value))
        
    def faction_get_slot(self, destination, faction_id, slot_no):
        """
        (faction_get_slot, <destination>, <faction_id>, <slot_no>),
        

		Args:
			destination (str|int):
			faction_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_get_slot(destination, faction_id, slot_no)
        """
        return self.append((faction_get_slot, destination, faction_id, slot_no))
        
    def faction_slot_eq(self, faction_id, slot_no, value):
        """
        (faction_slot_eq, <faction_id>, <slot_no>, <value>),
        

		Args:
			faction_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_slot_eq(faction_id, slot_no, value)
        """
        return self.append((faction_slot_eq, faction_id, slot_no, value))
        
    def faction_slot_ge(self, faction_id, slot_no, value):
        """
        (faction_slot_ge, <faction_id>, <slot_no>, <value>),
        

		Args:
			faction_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_slot_ge(faction_id, slot_no, value)
        """
        return self.append((faction_slot_ge, faction_id, slot_no, value))
        
    def set_relation(self, faction_id_1, faction_id_2, value):
        """
        (set_relation, <faction_id_1>, <faction_id_2>, <value>),
        Sets relation between two factions. Relation is in -100..100 range.

		Args:
			faction_id_1 (str|int):
			faction_id_2 (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_relation(faction_id_1, faction_id_2, value)
        """
        return self.append((set_relation, faction_id_1, faction_id_2, value))
        
    def store_relation(self, destination, faction_id_1, faction_id_2):
        """
        (store_relation, <destination>, <faction_id_1>, <faction_id_2>),
        Retrieves relation between two factions. Relation is in -100..100 range.

		Args:
			destination (str|int):
			faction_id_1 (str|int):
			faction_id_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_relation(destination, faction_id_1, faction_id_2)
        """
        return self.append((store_relation, destination, faction_id_1, faction_id_2))
        
    def faction_set_name(self, faction_id, string):
        """
        (faction_set_name, <faction_id>, <string>),
        Sets the name of the faction. See also (str_store_faction_name) in String Operations.

		Args:
			faction_id (str|int):
			string (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_set_name(faction_id, string)
        """
        return self.append((faction_set_name, faction_id, string))
        
    def faction_set_color(self, faction_id, color_code):
        """
        (faction_set_color, <faction_id>, <color_code>),
        Sets the faction color. All parties and centers belonging to this faction will be displayed with this color on global map.

		Args:
			faction_id (str|int):
			color_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_set_color(faction_id, color_code)
        """
        return self.append((faction_set_color, faction_id, color_code))
        
    def faction_get_color(self, destination, faction_id):
        """
        (faction_get_color, <destination>, <faction_id>),
        Gets the faction color value.

		Args:
			destination (str|int):
			faction_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_get_color(destination, faction_id)
        """
        return self.append((faction_get_color, destination, faction_id))
        
    def hero_can_join(self, party_id):
        """
        (hero_can_join, [party_id]),
        Checks if party can accept one hero troop. Player's party is default value.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> hero_can_join(party_id)
        """
        return self.append((hero_can_join, party_id))
        
    def hero_can_join_as_prisoner(self, party_id):
        """
        (hero_can_join_as_prisoner, [party_id]),
        Checks if party can accept one hero prisoner troop. Player's party is default value.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> hero_can_join_as_prisoner(party_id)
        """
        return self.append((hero_can_join_as_prisoner, party_id))
        
    def party_can_join(self):
        """
        (party_can_join),
        During encounter dialog, checks if encountered party can join player's party.

        Returns:
            TupleBuilder: self

        Example:
            >>> party_can_join(party_id)
        """
        return self.append((party_can_join))
        
    def party_can_join_as_prisoner(self):
        """
        (party_can_join_as_prisoner),
        During encounter dialog, checks if encountered party can join player's party as prisoners.

        Returns:
            TupleBuilder: self

        Example:
            >>> party_can_join_as_prisoner(party_id)
        """
        return self.append((party_can_join_as_prisoner))
        
    def troops_can_join(self, value):
        """
        (troops_can_join, <value>),
        Checks if player party has enough space for provided number of troops.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troops_can_join(value)
        """
        return self.append((troops_can_join, value))
        
    def troops_can_join_as_prisoner(self, value):
        """
        (troops_can_join_as_prisoner, <value>),
        Checks if player party has enough space for provided number of prisoners..

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troops_can_join_as_prisoner(value)
        """
        return self.append((troops_can_join_as_prisoner, value))
        
    def party_can_join_party(self, joiner_party_id, host_party_id, flip_prisoners):
        """
        (party_can_join_party, <joiner_party_id>, <host_party_id>, [flip_prisoners]),
        Checks if first party can join second party (enough space for both troops and prisoners). If flip_prisoners flag is 1, then members and prisoners in the joinning party are flipped.

		Args:
			joiner_party_id (str|int):
			host_party_id (str|int):
			flip_prisoners (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_can_join_party(joiner_party_id, host_party_id, flip_prisoners)
        """
        return self.append((party_can_join_party, joiner_party_id, host_party_id, flip_prisoners))
        
    def main_party_has_troop(self, troop_id):
        """
        (main_party_has_troop, <troop_id>),
        Checks if player party has specified troop.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> main_party_has_troop(troop_id)
        """
        return self.append((main_party_has_troop, troop_id))
        
    def party_is_in_town(self, party_id, town_party_id):
        """
        (party_is_in_town, <party_id>, <town_party_id>),
        Checks that the party has successfully reached it's destination (after being set to ai_bhvr_travel_to_party) and that it's destination is actually the referenced town_party_id.

		Args:
			party_id (str|int):
			town_party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_is_in_town(party_id, town_party_id)
        """
        return self.append((party_is_in_town, party_id, town_party_id))
        
    def party_is_in_any_town(self, party_id):
        """
        (party_is_in_any_town, <party_id>),
        Checks that the party has successfully reached it's destination (after being set to ai_bhvr_travel_to_party).

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_is_in_any_town(party_id)
        """
        return self.append((party_is_in_any_town, party_id))
        
    def party_is_active(self, party_id):
        """
        (party_is_active, <party_id>),
        Checks that <party_id> is valid and not disabled.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_is_active(party_id)
        """
        return self.append((party_is_active, party_id))
        
    def party_template_set_slot(self, party_template_id, slot_no, value):
        """
        (party_template_set_slot, <party_template_id>, <slot_no>, <value>),
        

		Args:
			party_template_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_template_set_slot(party_template_id, slot_no, value)
        """
        return self.append((party_template_set_slot, party_template_id, slot_no, value))
        
    def party_template_get_slot(self, destination, party_template_id, slot_no):
        """
        (party_template_get_slot, <destination>, <party_template_id>, <slot_no>),
        

		Args:
			destination (str|int):
			party_template_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_template_get_slot(destination, party_template_id, slot_no)
        """
        return self.append((party_template_get_slot, destination, party_template_id, slot_no))
        
    def party_template_slot_eq(self, party_template_id, slot_no, value):
        """
        (party_template_slot_eq, <party_template_id>, <slot_no>, <value>),
        

		Args:
			party_template_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_template_slot_eq(party_template_id, slot_no, value)
        """
        return self.append((party_template_slot_eq, party_template_id, slot_no, value))
        
    def party_template_slot_ge(self, party_template_id, slot_no, value):
        """
        (party_template_slot_ge, <party_template_id>, <slot_no>, <value>),
        

		Args:
			party_template_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_template_slot_ge(party_template_id, slot_no, value)
        """
        return self.append((party_template_slot_ge, party_template_id, slot_no, value))
        
    def party_set_slot(self, party_id, slot_no, value):
        """
        (party_set_slot, <party_id>, <slot_no>, <value>),
        

		Args:
			party_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_slot(party_id, slot_no, value)
        """
        return self.append((party_set_slot, party_id, slot_no, value))
        
    def party_get_slot(self, destination, party_id, slot_no):
        """
        (party_get_slot, <destination>, <party_id>, <slot_no>),
        

		Args:
			destination (str|int):
			party_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_slot(destination, party_id, slot_no)
        """
        return self.append((party_get_slot, destination, party_id, slot_no))
        
    def party_slot_eq(self, party_id, slot_no, value):
        """
        (party_slot_eq, <party_id>, <slot_no>, <value>),
        

		Args:
			party_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_slot_eq(party_id, slot_no, value)
        """
        return self.append((party_slot_eq, party_id, slot_no, value))
        
    def party_slot_ge(self, party_id, slot_no, value):
        """
        (party_slot_ge, <party_id>, <slot_no>, <value>),
        

		Args:
			party_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_slot_ge(party_id, slot_no, value)
        """
        return self.append((party_slot_ge, party_id, slot_no, value))
        
    def set_party_creation_random_limits(self, min_value, max_value):
        """
        (set_party_creation_random_limits, <min_value>, <max_value>),
        Affects party sizes spawned from templates. May be used to spawn larger parties when player is high level. Values should be in 0..100 range.

		Args:
			min_value (str|int):
			max_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_party_creation_random_limits(min_value, max_value)
        """
        return self.append((set_party_creation_random_limits, min_value, max_value))
        
    def set_spawn_radius(self, value):
        """
        (set_spawn_radius, <value>),
        Sets radius for party spawning with subsequent <spawn_around_party> operations.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_spawn_radius(value)
        """
        return self.append((set_spawn_radius, value))
        
    def spawn_around_party(self, party_id, party_template_id):
        """
        (spawn_around_party, <party_id>, <party_template_id>),
        Creates a new party from a party template and puts it's <party_id> into reg0.

		Args:
			party_id (str|int):
			party_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> spawn_around_party(party_id, party_template_id)
        """
        return self.append((spawn_around_party, party_id, party_template_id))
        
    def disable_party(self, party_id):
        """
        (disable_party, <party_id>),
        Party disappears from the map. Note that (try_for_parties) will still iterate over disabled parties, so you need to make additional checks with (party_is_active).

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> disable_party(party_id)
        """
        return self.append((disable_party, party_id))
        
    def enable_party(self, party_id):
        """
        (enable_party, <party_id>),
        Reactivates a previously disabled party.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> enable_party(party_id)
        """
        return self.append((enable_party, party_id))
        
    def remove_party(self, party_id):
        """
        (remove_party, <party_id>),
        Destroys a party completely. Should ONLY be used with dynamically spawned parties, as removing parties pre-defined in module_parties.py file will corrupt the savegame.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_party(party_id)
        """
        return self.append((remove_party, party_id))
        
    def party_get_current_terrain(self, destination, party_id):
        """
        (party_get_current_terrain, <destination>, <party_id>),
        Returns a value from header_terrain_types.py

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_current_terrain(destination, party_id)
        """
        return self.append((party_get_current_terrain, destination, party_id))
        
    def party_relocate_near_party(self, relocated_party_id, target_party_id, spawn_radius):
        """
        (party_relocate_near_party, <relocated_party_id>, <target_party_id>, <spawn_radius>),
        Teleports party into vicinity of another party.

		Args:
			relocated_party_id (str|int):
			target_party_id (str|int):
			spawn_radius (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_relocate_near_party(relocated_party_id, target_party_id, spawn_radius)
        """
        return self.append((party_relocate_near_party, relocated_party_id, target_party_id, spawn_radius))
        
    def party_get_position(self, dest_position, party_id):
        """
        (party_get_position, <dest_position>, <party_id>),
        Stores current position of the party on world map.

		Args:
			dest_position (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_position(dest_position, party_id)
        """
        return self.append((party_get_position, dest_position, party_id))
        
    def party_set_position(self, party_id, position):
        """
        (party_set_position, <party_id>, <position>),
        Teleports party to a specified position on the world map.

		Args:
			party_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_position(party_id, position)
        """
        return self.append((party_set_position, party_id, position))
        
    def set_camera_follow_party(self, party_id):
        """
        (set_camera_follow_party, <party_id>),
        Self-explanatory. Can be used on world map only. Commonly used to make camera follow a party which has captured player as prisoner.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_camera_follow_party(party_id)
        """
        return self.append((set_camera_follow_party, party_id))
        
    def party_attach_to_party(self, party_id, party_id_to_attach_to):
        """
        (party_attach_to_party, <party_id>, <party_id_to_attach_to>),
        Attach a party to another one (like lord's army staying in a town/castle).

		Args:
			party_id (str|int):
			party_id_to_attach_to (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_attach_to_party(party_id, party_id_to_attach_to)
        """
        return self.append((party_attach_to_party, party_id, party_id_to_attach_to))
        
    def party_detach(self, party_id):
        """
        (party_detach, <party_id>),
        Remove a party from attachments and place it on the world map.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_detach(party_id)
        """
        return self.append((party_detach, party_id))
        
    def party_collect_attachments_to_party(self, source_party_id, collected_party_id):
        """
        (party_collect_attachments_to_party, <source_party_id>, <collected_party_id>),
        Mostly used in various battle and AI calculations. Will create an aggregate party from all parties attached to the source party.

		Args:
			source_party_id (str|int):
			collected_party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_collect_attachments_to_party(source_party_id, collected_party_id)
        """
        return self.append((party_collect_attachments_to_party, source_party_id, collected_party_id))
        
    def party_get_cur_town(self, destination, party_id):
        """
        (party_get_cur_town, <destination>, <party_id>),
        When a party has reached it's destination (using ai_bhvr_travel_to_party), this operation will retrieve the party_id of the destination party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_cur_town(destination, party_id)
        """
        return self.append((party_get_cur_town, destination, party_id))
        
    def party_get_attached_to(self, destination, party_id):
        """
        (party_get_attached_to, <destination>, <party_id>),
        Retrieves the party that the referenced party is attached to, if any.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_attached_to(destination, party_id)
        """
        return self.append((party_get_attached_to, destination, party_id))
        
    def party_get_num_attached_parties(self, destination, party_id):
        """
        (party_get_num_attached_parties, <destination>, <party_id>),
        Retrieves total number of parties attached to referenced party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_num_attached_parties(destination, party_id)
        """
        return self.append((party_get_num_attached_parties, destination, party_id))
        
    def party_get_attached_party_with_rank(self, destination, party_id, attached_party_index):
        """
        (party_get_attached_party_with_rank, <destination>, <party_id>, <attached_party_index>),
        Extract party_id of a specified party among attached.

		Args:
			destination (str|int):
			party_id (str|int):
			attached_party_index (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_attached_party_with_rank(destination, party_id, attached_party_index)
        """
        return self.append((party_get_attached_party_with_rank, destination, party_id, attached_party_index))
        
    def party_set_name(self, party_id, string):
        """
        (party_set_name, <party_id>, <string>),
        Sets party name (will be displayed as label and/or in the party details popup).

		Args:
			party_id (str|int):
			string (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_name(party_id, string)
        """
        return self.append((party_set_name, party_id, string))
        
    def party_set_extra_text(self, party_id, string):
        """
        (party_set_extra_text, <party_id>, <string>),
        Allows to put extra text in party details popup. Used in Native to set status for villages or towns (being raided, razed, under siege...).

		Args:
			party_id (str|int):
			string (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_extra_text(party_id, string)
        """
        return self.append((party_set_extra_text, party_id, string))
        
    def party_get_icon(self, destination, party_id):
        """
        (party_get_icon, <destination>, <party_id>),
        Retrieve map icon used for the party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_icon(destination, party_id)
        """
        return self.append((party_get_icon, destination, party_id))
        
    def party_set_icon(self, party_id, map_icon_id):
        """
        (party_set_icon, <party_id>, <map_icon_id>),
        Sets what map icon will be used for the party.

		Args:
			party_id (str|int):
			map_icon_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_icon(party_id, map_icon_id)
        """
        return self.append((party_set_icon, party_id, map_icon_id))
        
    def party_set_banner_icon(self, party_id, map_icon_id):
        """
        (party_set_banner_icon, <party_id>, <map_icon_id>),
        Sets what map icon will be used as the party banner. Use 0 to remove banner from a party.

		Args:
			party_id (str|int):
			map_icon_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_banner_icon(party_id, map_icon_id)
        """
        return self.append((party_set_banner_icon, party_id, map_icon_id))
        
    def party_set_extra_icon(self, party_id, map_icon_id, vertical_offset_fixed_point, up_down_frequency_fixed_point, rotate_frequency_fixed_point, fade_in_out_frequency_fixed_point):
        """
        (party_set_extra_icon, <party_id>, <map_icon_id>, <vertical_offset_fixed_point>, <up_down_frequency_fixed_point>, <rotate_frequency_fixed_point>, <fade_in_out_frequency_fixed_point>),
        Adds or removes an extra map icon to a party, possibly with some animations. Use -1 as map_icon_id to remove extra icon.

		Args:
			party_id (str|int):
			map_icon_id (str|int):
			vertical_offset_fixed_point (str|int):
			up_down_frequency_fixed_point (str|int):
			rotate_frequency_fixed_point (str|int):
			fade_in_out_frequency_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_extra_icon(party_id, map_icon_id, vertical_offset_fixed_point, up_down_frequency_fixed_point, rotate_frequency_fixed_point, fade_in_out_frequency_fixed_point)
        """
        return self.append((party_set_extra_icon, party_id, map_icon_id, vertical_offset_fixed_point, up_down_frequency_fixed_point, rotate_frequency_fixed_point, fade_in_out_frequency_fixed_point))
        
    def party_add_particle_system(self, party_id, particle_system_id):
        """
        (party_add_particle_system, <party_id>, <particle_system_id>),
        Appends some special visual effects to the party on the map. Used in Native to add fire and smoke over villages.

		Args:
			party_id (str|int):
			particle_system_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_particle_system(party_id, particle_system_id)
        """
        return self.append((party_add_particle_system, party_id, particle_system_id))
        
    def party_clear_particle_systems(self, party_id):
        """
        (party_clear_particle_systems, <party_id>),
        Removes all special visual effects from the party on the map.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_clear_particle_systems(party_id)
        """
        return self.append((party_clear_particle_systems, party_id))
        
    def context_menu_add_item(self, string_id, value):
        """
        (context_menu_add_item, <string_id>, <value>),
        Must be called inside script_game_context_menu_get_buttons. Adds context menu option for a party and it's respective identifier (will be passed to script_game_event_context_menu_button_clicked).

		Args:
			string_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> context_menu_add_item(string_id, value)
        """
        return self.append((context_menu_add_item, string_id, value))
        
    def party_get_template_id(self, destination, party_id):
        """
        (party_get_template_id, <destination>, <party_id>),
        Retrieves what party template was used to create the party (if any). Commonly used to identify encountered party type.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_template_id(destination, party_id)
        """
        return self.append((party_get_template_id, destination, party_id))
        
    def party_set_faction(self, party_id, faction_id):
        """
        (party_set_faction, <party_id>, <faction_id>),
        Sets party faction allegiance. Party color is changed appropriately.

		Args:
			party_id (str|int):
			faction_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_faction(party_id, faction_id)
        """
        return self.append((party_set_faction, party_id, faction_id))
        
    def store_faction_of_party(self, destination, party_id):
        """
        (store_faction_of_party, <destination>, <party_id>),
        Retrieves current faction allegiance of the party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_faction_of_party(destination, party_id)
        """
        return self.append((store_faction_of_party, destination, party_id))
        
    def store_random_party_in_range(self, destination, lower_bound, upper_bound):
        """
        (store_random_party_in_range, <destination>, <lower_bound>, <upper_bound>),
        Retrieves one random party from the range. Generally used only for predefined parties (towns, villages etc).

		Args:
			destination (str|int):
			lower_bound (str|int):
			upper_bound (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_party_in_range(destination, lower_bound, upper_bound)
        """
        return self.append((store_random_party_in_range, destination, lower_bound, upper_bound))
        
    def store01_random_parties_in_range(self, lower_bound, upper_bound):
        """
        (store01_random_parties_in_range, <lower_bound>, <upper_bound>),
        Stores two random, different parties in a range to reg0 and reg1. Generally used only for predefined parties (towns, villages etc).

		Args:
			lower_bound (str|int):
			upper_bound (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store01_random_parties_in_range(lower_bound, upper_bound)
        """
        return self.append((store01_random_parties_in_range, lower_bound, upper_bound))
        
    def store_distance_to_party_from_party(self, party_id1, party_id2):
        """
        (store_distance_to_party_from_party, <destination>, <party_id>, <party_id>),
        Retrieves distance between two parties on the global map.

		Args:
			party_id1 (str|int):
			party_id2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_distance_to_party_from_party(party_id1, party_id2)
        """
        return self.append((store_distance_to_party_from_party, party_id1, party_id2))
        
    def store_num_parties_of_template(self, destination, party_template_id):
        """
        (store_num_parties_of_template, <destination>, <party_template_id>),
        Stores number of active parties which were created using specified party template.

		Args:
			destination (str|int):
			party_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_parties_of_template(destination, party_template_id)
        """
        return self.append((store_num_parties_of_template, destination, party_template_id))
        
    def store_random_party_of_template(self, destination, party_template_id):
        """
        (store_random_party_of_template, <destination>, <party_template_id>),
        Retrieves one random party which was created using specified party template. Fails if no party exists with provided template.

		Args:
			destination (str|int):
			party_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_party_of_template(destination, party_template_id)
        """
        return self.append((store_random_party_of_template, destination, party_template_id))
        
    def store_num_parties_created(self, destination, party_template_id):
        """
        (store_num_parties_created, <destination>, <party_template_id>),
        Stores the total number of created parties of specified type. Not used in Native.

		Args:
			destination (str|int):
			party_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_parties_created(destination, party_template_id)
        """
        return self.append((store_num_parties_created, destination, party_template_id))
        
    def store_num_parties_destroyed(self, destination, party_template_id):
        """
        (store_num_parties_destroyed, <destination>, <party_template_id>),
        Stores the total number of destroyed parties of specified type.

		Args:
			destination (str|int):
			party_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_parties_destroyed(destination, party_template_id)
        """
        return self.append((store_num_parties_destroyed, destination, party_template_id))
        
    def store_num_parties_destroyed_by_player(self, destination, party_template_id):
        """
        (store_num_parties_destroyed_by_player, <destination>, <party_template_id>),
        Stores the total number of parties of specified type which have been destroyed by player.

		Args:
			destination (str|int):
			party_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_parties_destroyed_by_player(destination, party_template_id)
        """
        return self.append((store_num_parties_destroyed_by_player, destination, party_template_id))
        
    def party_get_morale(self, destination, party_id):
        """
        (party_get_morale, <destination>, <party_id>),
        Returns a value in the range of 0..100. Party morale does not affect party behavior on the map, but will be taken in account if the party is engaged in battle (except auto-calc).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_morale(destination, party_id)
        """
        return self.append((party_get_morale, destination, party_id))
        
    def party_set_morale(self, party_id, value):
        """
        (party_set_morale, <party_id>, <value>),
        Value should be in the range of 0..100. Party morale does not affect party behavior on the map, but will be taken in account if the party is engaged in battle (except auto-calc).

		Args:
			party_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_morale(party_id, value)
        """
        return self.append((party_set_morale, party_id, value))
        
    def party_join(self):
        """
        (party_join),
        During encounter, joins encountered party to player's party

        Returns:
            TupleBuilder: self

        Example:
            >>> party_join(party_id, value)
        """
        return self.append((party_join))
        
    def party_join_as_prisoner(self):
        """
        (party_join_as_prisoner),
        During encounter, joins encountered party to player's party as prisoners

        Returns:
            TupleBuilder: self

        Example:
            >>> party_join_as_prisoner(party_id, value)
        """
        return self.append((party_join_as_prisoner))
        
    def troop_join(self, troop_id):
        """
        (troop_join, <troop_id>),
        Specified hero joins player's party

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_join(troop_id)
        """
        return self.append((troop_join, troop_id))
        
    def troop_join_as_prisoner(self, troop_id):
        """
        (troop_join_as_prisoner, <troop_id>),
        Specified hero joins player's party as prisoner

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_join_as_prisoner(troop_id)
        """
        return self.append((troop_join_as_prisoner, troop_id))
        
    def add_companion_party(self, troop_id_hero):
        """
        (add_companion_party, <troop_id_hero>),
        Creates a new empty party with specified hero as party leader and the only member. Party is spawned at the position of player's party.

		Args:
			troop_id_hero (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_companion_party(troop_id_hero)
        """
        return self.append((add_companion_party, troop_id_hero))
        
    def party_add_members(self, party_id, troop_id, number):
        """
        (party_add_members, <party_id>, <troop_id>, <number>),
        Returns total number of added troops in reg0.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_members(party_id, troop_id, number)
        """
        return self.append((party_add_members, party_id, troop_id, number))
        
    def party_add_prisoners(self, party_id, troop_id, number):
        """
        (party_add_prisoners, <party_id>, <troop_id>, <number>),
        Returns total number of added prisoners in reg0.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_prisoners(party_id, troop_id, number)
        """
        return self.append((party_add_prisoners, party_id, troop_id, number))
        
    def party_add_leader(self, party_id, troop_id, number):
        """
        (party_add_leader, <party_id>, <troop_id>, [number]),
        Adds troop(s) to the party and makes it party leader.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_leader(party_id, troop_id, number)
        """
        return self.append((party_add_leader, party_id, troop_id, number))
        
    def party_force_add_members(self, party_id, troop_id, number):
        """
        (party_force_add_members, <party_id>, <troop_id>, <number>),
        Adds troops to party ignoring party size limits. Mostly used to add hero troops.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_force_add_members(party_id, troop_id, number)
        """
        return self.append((party_force_add_members, party_id, troop_id, number))
        
    def party_force_add_prisoners(self, party_id, troop_id, number):
        """
        (party_force_add_prisoners, <party_id>, <troop_id>, <number>),
        Adds prisoners to party ignoring party size limits. Mostly used to add hero prisoners.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_force_add_prisoners(party_id, troop_id, number)
        """
        return self.append((party_force_add_prisoners, party_id, troop_id, number))
        
    def party_add_template(self, party_id, party_template_id, reverse_prisoner_status):
        """
        (party_add_template, <party_id>, <party_template_id>, [reverse_prisoner_status]),
        Reinforces the party using the specified party template. Optional flag switches troop/prisoner status for reinforcements.

		Args:
			party_id (str|int):
			party_template_id (str|int):
			reverse_prisoner_status (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_template(party_id, party_template_id, reverse_prisoner_status)
        """
        return self.append((party_add_template, party_id, party_template_id, reverse_prisoner_status))
        
    def distribute_party_among_party_group(self, party_to_be_distributed, group_root_party):
        """
        (distribute_party_among_party_group, <party_to_be_distributed>, <group_root_party>),
        Distributes troops from first party among all parties attached to the second party. Commonly used to divide prisoners and resqued troops among NPC parties.

		Args:
			party_to_be_distributed (str|int):
			group_root_party (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> distribute_party_among_party_group(party_to_be_distributed, group_root_party)
        """
        return self.append((distribute_party_among_party_group, party_to_be_distributed, group_root_party))
        
    def remove_member_from_party(self, troop_id, party_id):
        """
        (remove_member_from_party, <troop_id>, [party_id]),
        Removes hero member from party. Player party is default value. Will display a message about companion leaving the party. Should not be used with regular troops (it will successfully remove one of them, but will produce some meaningless spam).

		Args:
			troop_id (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_member_from_party(troop_id, party_id)
        """
        return self.append((remove_member_from_party, troop_id, party_id))
        
    def remove_regular_prisoners(self, party_id):
        """
        (remove_regular_prisoners, <party_id>),
        Removes all non-hero prisoners from the party.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_regular_prisoners(party_id)
        """
        return self.append((remove_regular_prisoners, party_id))
        
    def remove_troops_from_companions(self, troop_id, value):
        """
        (remove_troops_from_companions, <troop_id>, <value>),
        Removes troops from player's party, duplicating functionality of (party_remove_members) but providing less flexibility.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_troops_from_companions(troop_id, value)
        """
        return self.append((remove_troops_from_companions, troop_id, value))
        
    def remove_troops_from_prisoners(self, troop_id, value):
        """
        (remove_troops_from_prisoners, <troop_id>, <value>),
        Removes prisoners from player's party.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_troops_from_prisoners(troop_id, value)
        """
        return self.append((remove_troops_from_prisoners, troop_id, value))
        
    def party_remove_members(self, party_id, troop_id, number):
        """
        (party_remove_members, <party_id>, <troop_id>, <number>),
        Removes specified number of troops from a party. Stores number of actually removed troops in reg0.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_remove_members(party_id, troop_id, number)
        """
        return self.append((party_remove_members, party_id, troop_id, number))
        
    def party_remove_prisoners(self, party_id, troop_id, number):
        """
        (party_remove_prisoners, <party_id>, <troop_id>, <number>),
        Removes specified number of prisoners from a party. Stores number of actually removed prisoners in reg0.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_remove_prisoners(party_id, troop_id, number)
        """
        return self.append((party_remove_prisoners, party_id, troop_id, number))
        
    def party_clear(self, party_id):
        """
        (party_clear, <party_id>),
        Removes all members and prisoners from the party.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_clear(party_id)
        """
        return self.append((party_clear, party_id))
        
    def add_gold_to_party(self, value, party_id):
        """
        (add_gold_to_party, <value>, <party_id>),
        Marks the party as carrying the specified amount of gold, which can be pillaged by player if he destroys it. Operation must not be used to give gold to player's party.

		Args:
			value (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_gold_to_party(value, party_id)
        """
        return self.append((add_gold_to_party, value, party_id))
        
    def party_get_num_companions(self, destination, party_id):
        """
        (party_get_num_companions, <destination>, <party_id>),
        Returns total number of party members, including leader.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_num_companions(destination, party_id)
        """
        return self.append((party_get_num_companions, destination, party_id))
        
    def party_get_num_prisoners(self, destination, party_id):
        """
        (party_get_num_prisoners, <destination>, <party_id>),
        Returns total number of party prisoners.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_num_prisoners(destination, party_id)
        """
        return self.append((party_get_num_prisoners, destination, party_id))
        
    def party_count_members_of_type(self, destination, party_id, troop_id):
        """
        (party_count_members_of_type, <destination>, <party_id>, <troop_id>),
        Returns total number of party members of specific type.

		Args:
			destination (str|int):
			party_id (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_count_members_of_type(destination, party_id, troop_id)
        """
        return self.append((party_count_members_of_type, destination, party_id, troop_id))
        
    def party_count_companions_of_type(self, destination, party_id, troop_id):
        """
        (party_count_companions_of_type, <destination>, <party_id>, <troop_id>),
        Duplicates (party_count_members_of_type).

		Args:
			destination (str|int):
			party_id (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_count_companions_of_type(destination, party_id, troop_id)
        """
        return self.append((party_count_companions_of_type, destination, party_id, troop_id))
        
    def party_count_prisoners_of_type(self, destination, party_id, troop_id):
        """
        (party_count_prisoners_of_type, <destination>, <party_id>, <troop_id>),
        Returns total number of prisoners of specific type.

		Args:
			destination (str|int):
			party_id (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_count_prisoners_of_type(destination, party_id, troop_id)
        """
        return self.append((party_count_prisoners_of_type, destination, party_id, troop_id))
        
    def party_get_free_companions_capacity(self, destination, party_id):
        """
        (party_get_free_companions_capacity, <destination>, <party_id>),
        Calculates how many members can be added to the party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_free_companions_capacity(destination, party_id)
        """
        return self.append((party_get_free_companions_capacity, destination, party_id))
        
    def party_get_free_prisoners_capacity(self, destination, party_id):
        """
        (party_get_free_prisoners_capacity, <destination>, <party_id>),
        Calculates how many prisoners can be added to the party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_free_prisoners_capacity(destination, party_id)
        """
        return self.append((party_get_free_prisoners_capacity, destination, party_id))
        
    def party_get_num_companion_stacks(self, destination, party_id):
        """
        (party_get_num_companion_stacks, <destination>, <party_id>),
        Returns total number of troop stacks in the party (including player and heroes).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_num_companion_stacks(destination, party_id)
        """
        return self.append((party_get_num_companion_stacks, destination, party_id))
        
    def party_get_num_prisoner_stacks(self, destination, party_id):
        """
        (party_get_num_prisoner_stacks, <destination>, <party_id>),
        Returns total number of prisoner stacks in the party (including any heroes).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_num_prisoner_stacks(destination, party_id)
        """
        return self.append((party_get_num_prisoner_stacks, destination, party_id))
        
    def party_stack_get_troop_id(self, destination, party_id, stack_no):
        """
        (party_stack_get_troop_id, <destination>, <party_id>, <stack_no>),
        Extracts troop type of the specified troop stack.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_stack_get_troop_id(destination, party_id, stack_no)
        """
        return self.append((party_stack_get_troop_id, destination, party_id, stack_no))
        
    def party_stack_get_size(self, destination, party_id, stack_no):
        """
        (party_stack_get_size, <destination>, <party_id>, <stack_no>),
        Extracts number of troops in the specified troop stack.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_stack_get_size(destination, party_id, stack_no)
        """
        return self.append((party_stack_get_size, destination, party_id, stack_no))
        
    def party_stack_get_num_wounded(self, destination, party_id, stack_no):
        """
        (party_stack_get_num_wounded, <destination>, <party_id>, <stack_no>),
        Extracts number of wounded troops in the specified troop stack.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_stack_get_num_wounded(destination, party_id, stack_no)
        """
        return self.append((party_stack_get_num_wounded, destination, party_id, stack_no))
        
    def party_stack_get_troop_dna(self, destination, party_id, stack_no):
        """
        (party_stack_get_troop_dna, <destination>, <party_id>, <stack_no>),
        Extracts DNA from the specified troop stack. Used to properly generate appereance in conversations.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_stack_get_troop_dna(destination, party_id, stack_no)
        """
        return self.append((party_stack_get_troop_dna, destination, party_id, stack_no))
        
    def party_prisoner_stack_get_troop_id(self, destination, party_id, stack_no):
        """
        (party_prisoner_stack_get_troop_id, <destination>, <party_id>, <stack_no>),
        Extracts troop type of the specified prisoner stack.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_prisoner_stack_get_troop_id(destination, party_id, stack_no)
        """
        return self.append((party_prisoner_stack_get_troop_id, destination, party_id, stack_no))
        
    def party_prisoner_stack_get_size(self, destination, party_id, stack_no):
        """
        (party_prisoner_stack_get_size, <destination>, <party_id>, <stack_no>),
        Extracts number of troops in the specified prisoner stack.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_prisoner_stack_get_size(destination, party_id, stack_no)
        """
        return self.append((party_prisoner_stack_get_size, destination, party_id, stack_no))
        
    def party_prisoner_stack_get_troop_dna(self, destination, party_id, stack_no):
        """
        (party_prisoner_stack_get_troop_dna, <destination>, <party_id>, <stack_no>),
        Extracts DNA from the specified prisoner stack. Used to properly generate appereance in conversations.

		Args:
			destination (str|int):
			party_id (str|int):
			stack_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_prisoner_stack_get_troop_dna(destination, party_id, stack_no)
        """
        return self.append((party_prisoner_stack_get_troop_dna, destination, party_id, stack_no))
        
    def store_num_free_stacks(self, destination, party_id):
        """
        (store_num_free_stacks, <destination>, <party_id>),
        Deprecated, as Warband no longer has limits on number of stacks in the party. Always returns 10.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_free_stacks(destination, party_id)
        """
        return self.append((store_num_free_stacks, destination, party_id))
        
    def store_num_free_prisoner_stacks(self, destination, party_id):
        """
        (store_num_free_prisoner_stacks, <destination>, <party_id>),
        Deprecated, as Warband no longer has limits on number of stacks in the party. Always returns 10.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_free_prisoner_stacks(destination, party_id)
        """
        return self.append((store_num_free_prisoner_stacks, destination, party_id))
        
    def store_party_size(self, destination, party_id):
        """
        (store_party_size, <destination>, [party_id]),
        Stores total party size (all members and prisoners).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_party_size(destination, party_id)
        """
        return self.append((store_party_size, destination, party_id))
        
    def store_party_size_wo_prisoners(self, destination, party_id):
        """
        (store_party_size_wo_prisoners, <destination>, [party_id]),
        Stores total number of members in the party (without prisoners), duplicating (party_get_num_companions).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_party_size_wo_prisoners(destination, party_id)
        """
        return self.append((store_party_size_wo_prisoners, destination, party_id))
        
    def store_troop_kind_count(self, destination, troop_type_id):
        """
        (store_troop_kind_count, <destination>, <troop_type_id>),
        Counts number of troops of specified type in player's party. Deprecated, use party_count_members_of_type instead.

		Args:
			destination (str|int):
			troop_type_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_kind_count(destination, troop_type_id)
        """
        return self.append((store_troop_kind_count, destination, troop_type_id))
        
    def store_num_regular_prisoners(self, destination, party_id):
        """
        (store_num_regular_prisoners, <destination>, <party_id>),
        Deprecated and does not work. Do not use.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_num_regular_prisoners(destination, party_id)
        """
        return self.append((store_num_regular_prisoners, destination, party_id))
        
    def store_troop_count_companions(self, destination, troop_id, party_id):
        """
        (store_troop_count_companions, <destination>, <troop_id>, [party_id]),
        Apparently deprecated, duplicates (party_get_num_companions). Not used in Native.

		Args:
			destination (str|int):
			troop_id (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_count_companions(destination, troop_id, party_id)
        """
        return self.append((store_troop_count_companions, destination, troop_id, party_id))
        
    def store_troop_count_prisoners(self, destination, troop_id, party_id):
        """
        (store_troop_count_prisoners, <destination>, <troop_id>, [party_id]),
        Apparently deprecated, duplicates (party_get_num_prisoners). Not used in Native.

		Args:
			destination (str|int):
			troop_id (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_count_prisoners(destination, troop_id, party_id)
        """
        return self.append((store_troop_count_prisoners, destination, troop_id, party_id))
        
    def party_add_xp_to_stack(self, party_id, stack_no, xp_amount):
        """
        (party_add_xp_to_stack, <party_id>, <stack_no>, <xp_amount>),
        Awards specified number of xp points to a single troop stack in the party.

		Args:
			party_id (str|int):
			stack_no (str|int):
			xp_amount (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_xp_to_stack(party_id, stack_no, xp_amount)
        """
        return self.append((party_add_xp_to_stack, party_id, stack_no, xp_amount))
        
    def party_upgrade_with_xp(self, party_id, xp_amount, upgrade_path):
        """
        (party_upgrade_with_xp, <party_id>, <xp_amount>, <upgrade_path>),
        upgrade_path can be:
		Awards specified number of xp points to entire party (split between all stacks) and upgrades all eligible troops. Upgrade direction: (0 = random, 1 = first, 2 = second).

		Args:
			party_id (str|int):
			xp_amount (str|int):
			upgrade_path (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_upgrade_with_xp(party_id, xp_amount, upgrade_path)
        """
        return self.append((party_upgrade_with_xp, party_id, xp_amount, upgrade_path))
        
    def party_add_xp(self, party_id, xp_amount):
        """
        (party_add_xp, <party_id>, <xp_amount>),
        Awards specified number of xp points to entire party (split between all stacks).

		Args:
			party_id (str|int):
			xp_amount (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_add_xp(party_id, xp_amount)
        """
        return self.append((party_add_xp, party_id, xp_amount))
        
    def party_get_skill_level(self, destination, party_id, skill_no):
        """
        (party_get_skill_level, <destination>, <party_id>, <skill_no>),
        Retrieves skill level for the specified party (usually max among the heroes). Makes a callback to (script_game_get_skill_modifier_for_troop).

		Args:
			destination (str|int):
			party_id (str|int):
			skill_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_skill_level(destination, party_id, skill_no)
        """
        return self.append((party_get_skill_level, destination, party_id, skill_no))
        
    def heal_party(self, party_id):
        """
        (heal_party, <party_id>),
        Heals all wounded party members.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> heal_party(party_id)
        """
        return self.append((heal_party, party_id))
        
    def party_wound_members(self, party_id, troop_id, number):
        """
        (party_wound_members, <party_id>, <troop_id>, <number>),
        Wounds a specified number of troops in the party.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_wound_members(party_id, troop_id, number)
        """
        return self.append((party_wound_members, party_id, troop_id, number))
        
    def party_remove_members_wounded_first(self, party_id, troop_id, number):
        """
        (party_remove_members_wounded_first, <party_id>, <troop_id>, <number>),
        Removes a certain number of troops from the party, starting with wounded. Stores total number removed in reg0.

		Args:
			party_id (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_remove_members_wounded_first(party_id, troop_id, number)
        """
        return self.append((party_remove_members_wounded_first, party_id, troop_id, number))
        
    def party_quick_attach_to_current_battle(self, party_id, side):
        """
        (party_quick_attach_to_current_battle, <party_id>, <side>),
        Adds any party into current encounter at specified side (0 = ally, 1 = enemy).

		Args:
			party_id (str|int):
			side (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_quick_attach_to_current_battle(party_id, side)
        """
        return self.append((party_quick_attach_to_current_battle, party_id, side))
        
    def party_leave_cur_battle(self, party_id):
        """
        (party_leave_cur_battle, <party_id>),
        Forces the party to leave it's current battle (if it's engaged).

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_leave_cur_battle(party_id)
        """
        return self.append((party_leave_cur_battle, party_id))
        
    def party_set_next_battle_simulation_time(self, party_id, next_simulation_time_in_hours):
        """
        (party_set_next_battle_simulation_time, <party_id>, <next_simulation_time_in_hours>),
        Defines the period of time (in hours) after which the battle must be simulated for the specified party for the next time. When a value <= 0 is passed, the combat simulation round is performed immediately.

		Args:
			party_id (str|int):
			next_simulation_time_in_hours (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_next_battle_simulation_time(party_id, next_simulation_time_in_hours)
        """
        return self.append((party_set_next_battle_simulation_time, party_id, next_simulation_time_in_hours))
        
    def party_get_battle_opponent(self, destination, party_id):
        """
        (party_get_battle_opponent, <destination>, <party_id>),
        When a party is engaged in battle with another party, returns it's opponent party. Otherwise returns -1.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_battle_opponent(destination, party_id)
        """
        return self.append((party_get_battle_opponent, destination, party_id))
        
    def inflict_casualties_to_party_group(self, parent_party_id, damage_amount, party_id_to_add_causalties_to):
        """
        (inflict_casualties_to_party_group, <parent_party_id>, <damage_amount>, <party_id_to_add_causalties_to>),
        Delivers auto-calculated damage to the party (and all other parties attached to it). Killed troops are moved to another party to keep track of.

		Args:
			parent_party_id (str|int):
			damage_amount (str|int):
			party_id_to_add_causalties_to (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> inflict_casualties_to_party_group(parent_party_id, damage_amount, party_id_to_add_causalties_to)
        """
        return self.append((inflict_casualties_to_party_group, parent_party_id, damage_amount, party_id_to_add_causalties_to))
        
    def party_end_battle(self, party_no):
        """
        (party_end_battle, <party_no>),
        Version 1.153+. UNTESTED. Supposedly ends the battle in which the party is currently participating.

		Args:
			party_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_end_battle(party_no)
        """
        return self.append((party_end_battle, party_no))
        
    def party_set_marshall(self, party_id, value):
        """
        (party_set_marshall, <party_id>, <value>),
        

		Args:
			party_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_marshall(party_id, value)
        """
        return self.append((party_set_marshall, party_id, value))
        
    def party_set_marshal(self, party_id, value):
        """
        (party_set_marshal, <party_id>, <value>),
        Sets party as a marshall party or turns it back to normal party. Value is either 1 or 0. This affects party behavior, but exact effects are not known. Alternative operation name spelling added to enable compatibility with Viking Conquest DLC module system.

		Args:
			party_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_marshal(party_id, value)
        """
        return self.party_set_marshall(party_id, value)
        
    def party_set_flags(self, party_id, flag, clear_or_set):
        """
        (party_set_flags, <party_id>, <flag>, <clear_or_set>),
        Sets (1) or clears (0) party flags in runtime. See header_parties.py for flags reference.

		Args:
			party_id (str|int):
			flag (str|int):
			clear_or_set (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_flags(party_id, flag, clear_or_set)
        """
        return self.append((party_set_flags, party_id, flag, clear_or_set))
        
    def party_set_aggressiveness(self, party_id, number):
        """
        (party_set_aggressiveness, <party_id>, <number>),
        Sets aggressiveness value for the party (range 0..15).

		Args:
			party_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_aggressiveness(party_id, number)
        """
        return self.append((party_set_aggressiveness, party_id, number))
        
    def party_set_courage(self, party_id, number):
        """
        (party_set_courage, <party_id>, <number>),
        Sets courage value for the party (range 4..15).

		Args:
			party_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_courage(party_id, number)
        """
        return self.append((party_set_courage, party_id, number))
        
    def party_get_ai_initiative(self, destination, party_id):
        """
        (party_get_ai_initiative, <destination>, <party_id>),
        Gets party current AI initiative value (range 0..100).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_ai_initiative(destination, party_id)
        """
        return self.append((party_get_ai_initiative, destination, party_id))
        
    def party_set_ai_initiative(self, party_id, value):
        """
        (party_set_ai_initiative, <party_id>, <value>),
        Sets AI initiative value for the party (range 0..100).

		Args:
			party_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_ai_initiative(party_id, value)
        """
        return self.append((party_set_ai_initiative, party_id, value))
        
    def party_set_ai_behavior(self, party_id, ai_bhvr):
        """
        (party_set_ai_behavior, <party_id>, <ai_bhvr>),
        Sets AI behavior for the party. See header_parties.py for reference.

		Args:
			party_id (str|int):
			ai_bhvr (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_ai_behavior(party_id, ai_bhvr)
        """
        return self.append((party_set_ai_behavior, party_id, ai_bhvr))
        
    def party_set_ai_object(self, party_id, object_party_id):
        """
        (party_set_ai_object, <party_id>, <object_party_id>),
        Sets another party as the object for current AI behavior (follow that party).

		Args:
			party_id (str|int):
			object_party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_ai_object(party_id, object_party_id)
        """
        return self.append((party_set_ai_object, party_id, object_party_id))
        
    def party_set_ai_target_position(self, party_id, position):
        """
        (party_set_ai_target_position, <party_id>, <position>),
        Sets a specific world map position as the object for current AI behavior (travel to that point).

		Args:
			party_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_ai_target_position(party_id, position)
        """
        return self.append((party_set_ai_target_position, party_id, position))
        
    def party_set_ai_patrol_radius(self, party_id, radius_in_km):
        """
        (party_set_ai_patrol_radius, <party_id>, <radius_in_km>),
        Sets a radius for AI patrolling behavior.

		Args:
			party_id (str|int):
			radius_in_km (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_ai_patrol_radius(party_id, radius_in_km)
        """
        return self.append((party_set_ai_patrol_radius, party_id, radius_in_km))
        
    def party_ignore_player(self, party_id, duration_in_hours):
        """
        (party_ignore_player, <party_id>, <duration_in_hours>),
        Makes AI party ignore player for the specified time.

		Args:
			party_id (str|int):
			duration_in_hours (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_ignore_player(party_id, duration_in_hours)
        """
        return self.append((party_ignore_player, party_id, duration_in_hours))
        
    def party_set_bandit_attraction(self, party_id, attaraction):
        """
        (party_set_bandit_attraction, <party_id>, <attaraction>),
        Sets party attractiveness to parties with bandit behavior (range 0..100).

		Args:
			party_id (str|int):
			attaraction (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_bandit_attraction(party_id, attaraction)
        """
        return self.append((party_set_bandit_attraction, party_id, attaraction))
        
    def party_get_helpfulness(self, destination, party_id):
        """
        (party_get_helpfulness, <destination>, <party_id>),
        Gets party current AI helpfulness value (range 0..100).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_helpfulness(destination, party_id)
        """
        return self.append((party_get_helpfulness, destination, party_id))
        
    def party_set_helpfulness(self, party_id, number):
        """
        (party_set_helpfulness, <party_id>, <number>),
        Sets AI helpfulness value for the party (range 0..10000, default 100).

		Args:
			party_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_helpfulness(party_id, number)
        """
        return self.append((party_set_helpfulness, party_id, number))
        
    def get_party_ai_behavior(self, destination, party_id):
        """
        (get_party_ai_behavior, <destination>, <party_id>),
        Retrieves current AI behavior pattern for the party.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_party_ai_behavior(destination, party_id)
        """
        return self.append((get_party_ai_behavior, destination, party_id))
        
    def get_party_ai_object(self, destination, party_id):
        """
        (get_party_ai_object, <destination>, <party_id>),
        Retrieves what party is currently used as object for AI behavior.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_party_ai_object(destination, party_id)
        """
        return self.append((get_party_ai_object, destination, party_id))
        
    def party_get_ai_target_position(self, position, party_id):
        """
        (party_get_ai_target_position, <position>, <party_id>),
        Retrieves what position is currently used as object for AI behavior.

		Args:
			position (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_ai_target_position(position, party_id)
        """
        return self.append((party_get_ai_target_position, position, party_id))
        
    def get_party_ai_current_behavior(self, destination, party_id):
        """
        (get_party_ai_current_behavior, <destination>, <party_id>),
        Retrieves current AI behavior pattern when it was overridden by current situation (fleeing from enemy when en route to destination).

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_party_ai_current_behavior(destination, party_id)
        """
        return self.append((get_party_ai_current_behavior, destination, party_id))
        
    def get_party_ai_current_object(self, destination, party_id):
        """
        (get_party_ai_current_object, <destination>, <party_id>),
        Retrieves what party has caused temporary behavior switch.

		Args:
			destination (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_party_ai_current_object(destination, party_id)
        """
        return self.append((get_party_ai_current_object, destination, party_id))
        
    def party_set_ignore_with_player_party(self, party_id, value):
        """
        (party_set_ignore_with_player_party, <party_id>, <value>),
        Version 1.161+. Effects uncertain. 4research

		Args:
			party_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_ignore_with_player_party(party_id, value)
        """
        return self.append((party_set_ignore_with_player_party, party_id, value))
        
    def party_get_ignore_with_player_party(self, party_id):
        """
        (party_get_ignore_with_player_party, <party_id>),
        Version 1.161+. Effects uncertain. Documented official syntax is suspicious and probably incorrect. 4research

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_get_ignore_with_player_party(party_id)
        """
        return self.append((party_get_ignore_with_player_party, party_id))
        
    def troop_has_item_equipped(self, troop_id, item_id):
        """
        (troop_has_item_equipped, <troop_id>, <item_id>),
        Checks that the troop has this item equipped (worn or wielded).

		Args:
			troop_id (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_has_item_equipped(troop_id, item_id)
        """
        return self.append((troop_has_item_equipped, troop_id, item_id))
        
    def troop_is_mounted(self, troop_id):
        """
        (troop_is_mounted, <troop_id>),
        Checks the troop for tf_mounted flag (see header_troops.py). Does NOT check that the troop has a horse.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_is_mounted(troop_id)
        """
        return self.append((troop_is_mounted, troop_id))
        
    def troop_is_guarantee_ranged(self, troop_id):
        """
        (troop_is_guarantee_ranged, <troop_id>),
        Checks the troop for tf_guarantee_ranged flag (see header_troops.py). Does not check that troop actually has some ranged weapon.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_is_guarantee_ranged(troop_id)
        """
        return self.append((troop_is_guarantee_ranged, troop_id))
        
    def troop_is_guarantee_horse(self, troop_id):
        """
        (troop_is_guarantee_horse, <troop_id>),
        Checks the troop for tf_guarantee_horse flag (see header_troops.py). Does not check that troop actually has some horse.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_is_guarantee_horse(troop_id)
        """
        return self.append((troop_is_guarantee_horse, troop_id))
        
    def troop_is_hero(self, troop_id):
        """
        (troop_is_hero, <troop_id>),
        Checks the troop for tf_hero flag (see header_troops.py). Hero troops are actual characters and do not stack in party window.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_is_hero(troop_id)
        """
        return self.append((troop_is_hero, troop_id))
        
    def troop_is_wounded(self, troop_id):
        """
        (troop_is_wounded, <troop_id>),
        Checks that the troop is wounded. Only works for hero troops.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_is_wounded(troop_id)
        """
        return self.append((troop_is_wounded, troop_id))
        
    def player_has_item(self, item_id):
        """
        (player_has_item, <item_id>),
        Checks that player has the specified item.

		Args:
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_has_item(item_id)
        """
        return self.append((player_has_item, item_id))
        
    def troop_set_slot(self, troop_id, slot_no, value):
        """
        (troop_set_slot, <troop_id>, <slot_no>, <value>),
        

		Args:
			troop_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_slot(troop_id, slot_no, value)
        """
        return self.append((troop_set_slot, troop_id, slot_no, value))
        
    def troop_get_slot(self, destination, troop_id, slot_no):
        """
        (troop_get_slot, <destination>, <troop_id>, <slot_no>),
        

		Args:
			destination (str|int):
			troop_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_slot(destination, troop_id, slot_no)
        """
        return self.append((troop_get_slot, destination, troop_id, slot_no))
        
    def troop_slot_eq(self, troop_id, slot_no, value):
        """
        (troop_slot_eq, <troop_id>, <slot_no>, <value>),
        

		Args:
			troop_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_slot_eq(troop_id, slot_no, value)
        """
        return self.append((troop_slot_eq, troop_id, slot_no, value))
        
    def troop_slot_ge(self, troop_id, slot_no, value):
        """
        (troop_slot_ge, <troop_id>, <slot_no>, <value>),
        

		Args:
			troop_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_slot_ge(troop_id, slot_no, value)
        """
        return self.append((troop_slot_ge, troop_id, slot_no, value))
        
    def troop_set_type(self, troop_id, gender):
        """
        (troop_set_type, <troop_id>, <gender>),
        Changes the troop skin. There are two skins in Native: male and female, so in effect this operation sets troop gender. However mods may declare other skins.

		Args:
			troop_id (str|int):
			gender (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_type(troop_id, gender)
        """
        return self.append((troop_set_type, troop_id, gender))
        
    def troop_get_type(self, destination, troop_id):
        """
        (troop_get_type, <destination>, <troop_id>),
        Returns troop current skin (i.e. gender).

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_type(destination, troop_id)
        """
        return self.append((troop_get_type, destination, troop_id))
        
    def troop_set_class(self, troop_id, value):
        """
        (troop_set_class, <troop_id>, <value>),
        Sets troop class (infantry, archers, cavalry or any of custom classes). Accepts values in range 0..8. See grc_* constants in header_mission_templates.py.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_class(troop_id, value)
        """
        return self.append((troop_set_class, troop_id, value))
        
    def troop_get_class(self, destination, troop_id):
        """
        (troop_get_class, <destination>, <troop_id>),
        Retrieves troop class. Returns values in range 0..8.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_class(destination, troop_id)
        """
        return self.append((troop_get_class, destination, troop_id))
        
    def class_set_name(self, sub_class, string_id):
        """
        (class_set_name, <sub_class>, <string_id>),
        Sets a new name for troop class (aka "Infantry", "Cavalry", "Custom Group 3"...).

		Args:
			sub_class (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> class_set_name(sub_class, string_id)
        """
        return self.append((class_set_name, sub_class, string_id))
        
    def add_xp_to_troop(self, value, troop_id):
        """
        (add_xp_to_troop, <value>, [troop_id]),
        Adds some xp points to troop. Only makes sense for player and hero troops. Default troop_id is player. Amount of xp can be negative.

		Args:
			value (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_xp_to_troop(value, troop_id)
        """
        return self.append((add_xp_to_troop, value, troop_id))
        
    def add_xp_as_reward(self, value):
        """
        (add_xp_as_reward, <value>),
        Adds the specified amount of xp points to player. Typically used as a quest reward operation.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_xp_as_reward(value)
        """
        return self.append((add_xp_as_reward, value))
        
    def troop_get_xp(self, destination, troop_id):
        """
        (troop_get_xp, <destination>, <troop_id>),
        Retrieves total amount of xp specified troop has.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_xp(destination, troop_id)
        """
        return self.append((troop_get_xp, destination, troop_id))
        
    def store_attribute_level(self, destination, troop_id, attribute_id):
        """
        (store_attribute_level, <destination>, <troop_id>, <attribute_id>),
        Stores current value of troop attribute. See ca_* constants in header_troops.py for reference.

		Args:
			destination (str|int):
			troop_id (str|int):
			attribute_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_attribute_level(destination, troop_id, attribute_id)
        """
        return self.append((store_attribute_level, destination, troop_id, attribute_id))
        
    def troop_raise_attribute(self, troop_id, attribute_id, value):
        """
        (troop_raise_attribute, <troop_id>, <attribute_id>, <value>),
        Increases troop attribute by the specified amount. See ca_* constants in header_troops.py for reference. Use negative values to reduce attributes. When used on non-hero troop, will affect all instances of that troop.

		Args:
			troop_id (str|int):
			attribute_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_raise_attribute(troop_id, attribute_id, value)
        """
        return self.append((troop_raise_attribute, troop_id, attribute_id, value))
        
    def store_skill_level(self, destination, skill_id, troop_id):
        """
        (store_skill_level, <destination>, <skill_id>, [troop_id]),
        Stores current value of troop skill. See header_skills.py for reference.

		Args:
			destination (str|int):
			skill_id (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_skill_level(destination, skill_id, troop_id)
        """
        return self.append((store_skill_level, destination, skill_id, troop_id))
        
    def troop_raise_skill(self, troop_id, skill_id, value):
        """
        (troop_raise_skill, <troop_id>, <skill_id>, <value>),
        Increases troop skill by the specified value. Value can be negative. See header_skills.py for reference. When used on non-hero troop, will affect all instances of that troop.

		Args:
			troop_id (str|int):
			skill_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_raise_skill(troop_id, skill_id, value)
        """
        return self.append((troop_raise_skill, troop_id, skill_id, value))
        
    def store_proficiency_level(self, destination, troop_id, attribute_id):
        """
        (store_proficiency_level, <destination>, <troop_id>, <attribute_id>),
        Stores current value of troop weapon proficiency. See wpt_* constants in header_troops.py for reference.

		Args:
			destination (str|int):
			troop_id (str|int):
			attribute_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_proficiency_level(destination, troop_id, attribute_id)
        """
        return self.append((store_proficiency_level, destination, troop_id, attribute_id))
        
    def troop_raise_proficiency(self, troop_id, proficiency_no, value):
        """
        (troop_raise_proficiency, <troop_id>, <proficiency_no>, <value>),
        Increases troop weapon proficiency by the specified value. Value can be negative. Increase is subject to limits defined by Weapon Master skill. When used on non-hero troop, will affect all instances of that troop.

		Args:
			troop_id (str|int):
			proficiency_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_raise_proficiency(troop_id, proficiency_no, value)
        """
        return self.append((troop_raise_proficiency, troop_id, proficiency_no, value))
        
    def troop_raise_proficiency_linear(self, troop_id, proficiency_no, value):
        """
        (troop_raise_proficiency_linear, <troop_id>, <proficiency_no>, <value>),
        Same as (troop_raise_proficiency), but does not take Weapon Master skill into account (i.e. can increase proficiencies indefinitely).

		Args:
			troop_id (str|int):
			proficiency_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_raise_proficiency_linear(troop_id, proficiency_no, value)
        """
        return self.append((troop_raise_proficiency_linear, troop_id, proficiency_no, value))
        
    def troop_add_proficiency_points(self, troop_id, value):
        """
        (troop_add_proficiency_points, <troop_id>, <value>),
        Adds some proficiency points to a hero troop which can later be distributed by player.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_add_proficiency_points(troop_id, value)
        """
        return self.append((troop_add_proficiency_points, troop_id, value))
        
    def store_troop_health(self, destination, troop_id, absolute):
        """
        (store_troop_health, <destination>, <troop_id>, [absolute]),
        set absolute to 1 to get actual health; otherwise this will return percentage health in range (0-100)
		Retrieves current troop health. Use absolute = 1 to retrieve actual number of hp points left, use absolute = 0 to retrieve a value in 0..100 range (percentage).

		Args:
			destination (str|int):
			troop_id (str|int):
			absolute (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_health(destination, troop_id, absolute)
        """
        return self.append((store_troop_health, destination, troop_id, absolute))
        
    def troop_set_health(self, troop_id, relative_health):
        """
        (troop_set_health, <troop_id>, <relative_health>),
        Sets troop health. Accepts value in range 0..100 (percentage).

		Args:
			troop_id (str|int):
			relative_health (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_health(troop_id, relative_health)
        """
        return self.append((troop_set_health, troop_id, relative_health))
        
    def troop_get_upgrade_troop(self, destination, troop_id, upgrade_path):
        """
        (troop_get_upgrade_troop, <destination>, <troop_id>, <upgrade_path>),
        Retrieves possible directions for non-hero troop upgrade. Use 0 to retrieve first upgrade path, and 1 to return second. Result of -1 means there's no such upgrade path for this troop.

		Args:
			destination (str|int):
			troop_id (str|int):
			upgrade_path (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_upgrade_troop(destination, troop_id, upgrade_path)
        """
        return self.append((troop_get_upgrade_troop, destination, troop_id, upgrade_path))
        
    def store_character_level(self, destination, troop_id):
        """
        (store_character_level, <destination>, [troop_id]),
        Retrieves character level of the troop. Default troop is the player.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_character_level(destination, troop_id)
        """
        return self.append((store_character_level, destination, troop_id))
        
    def get_level_boundary(self, destination, level_no):
        """
        (get_level_boundary, <destination>, <level_no>),
        Returns the amount of experience points required to reach the specified level (will return 0 for 1st level). Maximum possible level in the game is 63.

		Args:
			destination (str|int):
			level_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_level_boundary(destination, level_no)
        """
        return self.append((get_level_boundary, destination, level_no))
        
    def add_gold_as_xp(self, value, troop_id):
        """
        (add_gold_as_xp, <value>, [troop_id]),
        Default troop is player
		Adds a certain amount of experience points, depending on the amount of gold specified. Conversion rate is unclear and apparently somewhat randomized (three runs with 1000 gold produced values 1091, 804 and 799).

		Args:
			value (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_gold_as_xp(value, troop_id)
        """
        return self.append((add_gold_as_xp, value, troop_id))
        
    def troop_set_auto_equip(self, troop_id, value):
        """
        (troop_set_auto_equip, <troop_id>, <value>),
        Sets (value = 1) or disables (value = 0) auto-equipping the troop with any items added to it's inventory or purchased. Similar to tf_is_merchant flag.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_auto_equip(troop_id, value)
        """
        return self.append((troop_set_auto_equip, troop_id, value))
        
    def troop_ensure_inventory_space(self, troop_id, value):
        """
        (troop_ensure_inventory_space, <troop_id>, <value>),
        Removes items from troop inventory until troop has specified number of free inventory slots. Will free inventory slots starting from the end (items at the bottom of inventory will be removed first if there's not enough free space).

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_ensure_inventory_space(troop_id, value)
        """
        return self.append((troop_ensure_inventory_space, troop_id, value))
        
    def troop_sort_inventory(self, troop_id):
        """
        (troop_sort_inventory, <troop_id>),
        Sorts items in troop inventory by their price (expensive first).

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_sort_inventory(troop_id)
        """
        return self.append((troop_sort_inventory, troop_id))
        
    def troop_add_item(self, troop_id, item_id, modifier):
        """
        (troop_add_item, <troop_id>, <item_id>, [modifier]),
        Adds an item to the troop, optionally with a modifier (see imod_* constants in header_item_modifiers.py).

		Args:
			troop_id (str|int):
			item_id (str|int):
			modifier (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_add_item(troop_id, item_id, modifier)
        """
        return self.append((troop_add_item, troop_id, item_id, modifier))
        
    def troop_remove_item(self, troop_id, item_id):
        """
        (troop_remove_item, <troop_id>, <item_id>),
        Removes an item from the troop equipment or inventory. Operation will remove first matching item it finds.

		Args:
			troop_id (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_remove_item(troop_id, item_id)
        """
        return self.append((troop_remove_item, troop_id, item_id))
        
    def troop_clear_inventory(self, troop_id):
        """
        (troop_clear_inventory, <troop_id>),
        Clears entire troop inventory. Does not affect equipped items.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_clear_inventory(troop_id)
        """
        return self.append((troop_clear_inventory, troop_id))
        
    def troop_equip_items(self, troop_id):
        """
        (troop_equip_items, <troop_id>),
        Makes the troop reconsider it's equipment. If troop has better stuff in it's inventory, he will equip it. Note this operation sucks with weapons and may force the troop to equip himself with 4 two-handed swords.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_equip_items(troop_id)
        """
        return self.append((troop_equip_items, troop_id))
        
    def troop_inventory_slot_set_item_amount(self, troop_id, inventory_slot_no, value):
        """
        (troop_inventory_slot_set_item_amount, <troop_id>, <inventory_slot_no>, <value>),
        Sets the stack size for a specified equipment or inventory slot. Only makes sense for items like ammo or food (which show stuff like "23/50" in inventory). Equipment slots are in range 0..9, see ek_* constants in header_items.py for reference.

		Args:
			troop_id (str|int):
			inventory_slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_inventory_slot_set_item_amount(troop_id, inventory_slot_no, value)
        """
        return self.append((troop_inventory_slot_set_item_amount, troop_id, inventory_slot_no, value))
        
    def troop_inventory_slot_get_item_amount(self, destination, troop_id, inventory_slot_no):
        """
        (troop_inventory_slot_get_item_amount, <destination>, <troop_id>, <inventory_slot_no>),
        Retrieves the stack size for a specified equipment or inventory slot (if some Bread is 23/50, this operation will return 23).

		Args:
			destination (str|int):
			troop_id (str|int):
			inventory_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_inventory_slot_get_item_amount(destination, troop_id, inventory_slot_no)
        """
        return self.append((troop_inventory_slot_get_item_amount, destination, troop_id, inventory_slot_no))
        
    def troop_inventory_slot_get_item_max_amount(self, destination, troop_id, inventory_slot_no):
        """
        (troop_inventory_slot_get_item_max_amount, <destination>, <troop_id>, <inventory_slot_no>),
        Retrieves the maximum possible stack size for a specified equipment or inventory slot (if some Bread is 23/50, this operation will return 50).

		Args:
			destination (str|int):
			troop_id (str|int):
			inventory_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_inventory_slot_get_item_max_amount(destination, troop_id, inventory_slot_no)
        """
        return self.append((troop_inventory_slot_get_item_max_amount, destination, troop_id, inventory_slot_no))
        
    def troop_add_items(self, troop_id, item_id, number):
        """
        (troop_add_items, <troop_id>, <item_id>, <number>),
        Adds multiple items of specified type to the troop.

		Args:
			troop_id (str|int):
			item_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_add_items(troop_id, item_id, number)
        """
        return self.append((troop_add_items, troop_id, item_id, number))
        
    def troop_remove_items(self, troop_id, item_id, number):
        """
        (troop_remove_items, <troop_id>, <item_id>, <number>),
        Removes multiple items of specified type from the troop. Total price of actually removed items will be stored in reg0.

		Args:
			troop_id (str|int):
			item_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_remove_items(troop_id, item_id, number)
        """
        return self.append((troop_remove_items, troop_id, item_id, number))
        
    def troop_loot_troop(self, target_troop, source_troop_id, probability):
        """
        (troop_loot_troop, <target_troop>, <source_troop_id>, <probability>),
        Adds to target_troop's inventory some items from source_troop's equipment and inventory with some probability. Does not actually remove items from source_troop. Commonly used in Native to generate random loot after the battle.

		Args:
			target_troop (str|int):
			source_troop_id (str|int):
			probability (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_loot_troop(target_troop, source_troop_id, probability)
        """
        return self.append((troop_loot_troop, target_troop, source_troop_id, probability))
        
    def troop_get_inventory_capacity(self, destination, troop_id):
        """
        (troop_get_inventory_capacity, <destination>, <troop_id>),
        Returns the total inventory capacity (number of inventory slots) for the specified troop. Note that this number will include equipment slots as well. Substract num_equipment_kinds (see header_items.py) to get the number of actual *inventory* slots.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_inventory_capacity(destination, troop_id)
        """
        return self.append((troop_get_inventory_capacity, destination, troop_id))
        
    def troop_get_inventory_slot(self, destination, troop_id, inventory_slot_no):
        """
        (troop_get_inventory_slot, <destination>, <troop_id>, <inventory_slot_no>),
        Retrieves the item_id of a specified equipment or inventory slot. Returns -1 when there's nothing there.

		Args:
			destination (str|int):
			troop_id (str|int):
			inventory_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_inventory_slot(destination, troop_id, inventory_slot_no)
        """
        return self.append((troop_get_inventory_slot, destination, troop_id, inventory_slot_no))
        
    def troop_get_inventory_slot_modifier(self, destination, troop_id, inventory_slot_no):
        """
        (troop_get_inventory_slot_modifier, <destination>, <troop_id>, <inventory_slot_no>),
        Retrieves the modifier value (see imod_* constants in header_items.py) for an item in the specified equipment or inventory slot. Returns 0 when there's nothing there, or if item does not have any modifiers.

		Args:
			destination (str|int):
			troop_id (str|int):
			inventory_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_get_inventory_slot_modifier(destination, troop_id, inventory_slot_no)
        """
        return self.append((troop_get_inventory_slot_modifier, destination, troop_id, inventory_slot_no))
        
    def troop_set_inventory_slot(self, troop_id, inventory_slot_no, item_id):
        """
        (troop_set_inventory_slot, <troop_id>, <inventory_slot_no>, <item_id>),
        Puts the specified item into troop's equipment or inventory slot. Be careful with setting equipment slots this way.

		Args:
			troop_id (str|int):
			inventory_slot_no (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_inventory_slot(troop_id, inventory_slot_no, item_id)
        """
        return self.append((troop_set_inventory_slot, troop_id, inventory_slot_no, item_id))
        
    def troop_set_inventory_slot_modifier(self, troop_id, inventory_slot_no, imod_value):
        """
        (troop_set_inventory_slot_modifier, <troop_id>, <inventory_slot_no>, <imod_value>),
        Sets the modifier for the item in the troop's equipment or inventory slot. See imod_* constants in header_items.py for reference.

		Args:
			troop_id (str|int):
			inventory_slot_no (str|int):
			imod_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_inventory_slot_modifier(troop_id, inventory_slot_no, imod_value)
        """
        return self.append((troop_set_inventory_slot_modifier, troop_id, inventory_slot_no, imod_value))
        
    def store_item_kind_count(self, destination, item_id, troop_id):
        """
        (store_item_kind_count, <destination>, <item_id>, [troop_id]),
        Calculates total number of items of specified type that the troop has. Default troop is player.

		Args:
			destination (str|int):
			item_id (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_item_kind_count(destination, item_id, troop_id)
        """
        return self.append((store_item_kind_count, destination, item_id, troop_id))
        
    def store_free_inventory_capacity(self, destination, troop_id):
        """
        (store_free_inventory_capacity, <destination>, [troop_id]),
        Calculates total number of free inventory slots that the troop has. Default troop is player.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_free_inventory_capacity(destination, troop_id)
        """
        return self.append((store_free_inventory_capacity, destination, troop_id))
        
    def reset_price_rates(self):
        """
        (reset_price_rates),
        Resets customized price rates for merchants.

        Returns:
            TupleBuilder: self

        Example:
            >>> reset_price_rates(destination, troop_id)
        """
        return self.append((reset_price_rates))
        
    def set_price_rate_for_item(self, item_id, value_percentage):
        """
        (set_price_rate_for_item, <item_id>, <value_percentage>),
        Sets individual price rate for a single item type. Normal price rate is 100. Deprecated, as Warband uses (game_get_item_[buy/sell]_price_factor) scripts instead.

		Args:
			item_id (str|int):
			value_percentage (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_price_rate_for_item(item_id, value_percentage)
        """
        return self.append((set_price_rate_for_item, item_id, value_percentage))
        
    def set_price_rate_for_item_type(self, item_type_id, value_percentage):
        """
        (set_price_rate_for_item_type, <item_type_id>, <value_percentage>),
        Sets individual price rate for entire item class (see header_items.py for itp_type_* constants). Normal price rate is 100. Deprecated, as Warband uses (game_get_item_[buy/sell]_price_factor) scripts instead.

		Args:
			item_type_id (str|int):
			value_percentage (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_price_rate_for_item_type(item_type_id, value_percentage)
        """
        return self.append((set_price_rate_for_item_type, item_type_id, value_percentage))
        
    def set_merchandise_modifier_quality(self, value):
        """
        (set_merchandise_modifier_quality, <value>),
        Affects the probability of items with quality modifiers appearing in merchandise. Value is percentage, standard value is 100.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_merchandise_modifier_quality(value)
        """
        return self.append((set_merchandise_modifier_quality, value))
        
    def set_merchandise_max_value(self, value):
        """
        (set_merchandise_max_value, <value>),
        Not used in Native. Apparently prevents items with price higher than listed from being generated as merchandise.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_merchandise_max_value(value)
        """
        return self.append((set_merchandise_max_value, value))
        
    def reset_item_probabilities(self, value):
        """
        (reset_item_probabilities, <value>),
        Sets all items probability of being generated as merchandise to the provided value. Use zero with subsequent calls to (set_item_probability_in_merchandise) to only allow generation of certain items.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> reset_item_probabilities(value)
        """
        return self.append((reset_item_probabilities, value))
        
    def set_item_probability_in_merchandise(self, item_id, value):
        """
        (set_item_probability_in_merchandise, <item_id>, <value>),
        Sets item probability of being generated as merchandise to the provided value.

		Args:
			item_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_item_probability_in_merchandise(item_id, value)
        """
        return self.append((set_item_probability_in_merchandise, item_id, value))
        
    def troop_add_merchandise(self, troop_id, item_type_id, value):
        """
        (troop_add_merchandise, <troop_id>, <item_type_id>, <value>),
        Adds a specified number of random items of certain type (see itp_type_* constants in header_items.py) to troop inventory. Only adds items with itp_merchandise flags.

		Args:
			troop_id (str|int):
			item_type_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_add_merchandise(troop_id, item_type_id, value)
        """
        return self.append((troop_add_merchandise, troop_id, item_type_id, value))
        
    def troop_add_merchandise_with_faction(self, troop_id, faction_id, item_type_id, value):
        """
        (troop_add_merchandise_with_faction, <troop_id>, <faction_id>, <item_type_id>, <value>),
        faction_id is given to check if troop is eligible to produce that item
		Same as (troop_add_merchandise), but with additional filter: only adds items which belong to specified faction, or without any factions at all.

		Args:
			troop_id (str|int):
			faction_id (str|int):
			item_type_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_add_merchandise_with_faction(troop_id, faction_id, item_type_id, value)
        """
        return self.append((troop_add_merchandise_with_faction, troop_id, faction_id, item_type_id, value))
        
    def troop_set_name(self, troop_id, string_no):
        """
        (troop_set_name, <troop_id>, <string_no>),
        Renames the troop, setting a new singular name for it.

		Args:
			troop_id (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_name(troop_id, string_no)
        """
        return self.append((troop_set_name, troop_id, string_no))
        
    def troop_set_plural_name(self, troop_id, string_no):
        """
        (troop_set_plural_name, <troop_id>, <string_no>),
        Renames the troop, setting a new plural name for it.

		Args:
			troop_id (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_plural_name(troop_id, string_no)
        """
        return self.append((troop_set_plural_name, troop_id, string_no))
        
    def troop_set_face_key_from_current_profile(self, troop_id):
        """
        (troop_set_face_key_from_current_profile, <troop_id>),
        Forces the troop to adopt the face from player's currently selected multiplayer profile.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_face_key_from_current_profile(troop_id)
        """
        return self.append((troop_set_face_key_from_current_profile, troop_id))
        
    def troop_add_gold(self, troop_id, value):
        """
        (troop_add_gold, <troop_id>, <value>),
        Adds gold to troop. Generally used with player or hero troops.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_add_gold(troop_id, value)
        """
        return self.append((troop_add_gold, troop_id, value))
        
    def troop_remove_gold(self, troop_id, value):
        """
        (troop_remove_gold, <troop_id>, <value>),
        Removes gold from troop. Generally used with player or hero troops.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_remove_gold(troop_id, value)
        """
        return self.append((troop_remove_gold, troop_id, value))
        
    def store_troop_gold(self, destination, troop_id):
        """
        (store_troop_gold, <destination>, <troop_id>),
        Retrieves total number of gold that the troop has.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_gold(destination, troop_id)
        """
        return self.append((store_troop_gold, destination, troop_id))
        
    def troop_set_faction(self, troop_id, faction_id):
        """
        (troop_set_faction, <troop_id>, <faction_id>),
        Sets a new faction for the troop (mostly used to switch lords allegiances in Native).

		Args:
			troop_id (str|int):
			faction_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_faction(troop_id, faction_id)
        """
        return self.append((troop_set_faction, troop_id, faction_id))
        
    def store_troop_faction(self, destination, troop_id):
        """
        (store_troop_faction, <destination>, <troop_id>),
        Retrieves current troop faction allegiance.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_faction(destination, troop_id)
        """
        return self.append((store_troop_faction, destination, troop_id))
        
    def store_faction_of_troop(self, destination, troop_id):
        """
        (store_faction_of_troop, <destination>, <troop_id>),
        Alternative spelling of the above operation.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_faction_of_troop(destination, troop_id)
        """
        return self.append((store_faction_of_troop, destination, troop_id))
        
    def troop_set_age(self, troop_id, age_slider_pos):
        """
        (troop_set_age, <troop_id>, <age_slider_pos>),
        Defines a new age for the troop (will be used by the game engine to generate appropriately aged face). Age is in range 0.100.

		Args:
			troop_id (str|int):
			age_slider_pos (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_age(troop_id, age_slider_pos)
        """
        return self.append((troop_set_age, troop_id, age_slider_pos))
        
    def store_troop_value(self, destination, troop_id):
        """
        (store_troop_value, <destination>, <troop_id>),
        Stores some value which is apparently related to troop's overall fighting value. Swadian infantry line troops from Native produced values 24, 47, 80, 133, 188. Calling on player produced 0.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_troop_value(destination, troop_id)
        """
        return self.append((store_troop_value, destination, troop_id))
        
    def str_store_player_face_keys(self, string_no, player_id):
        """
        (str_store_player_face_keys, <string_no>, <player_id>),
        Version 1.161+. Stores player's face keys into string register.

		Args:
			string_no (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_player_face_keys(string_no, player_id)
        """
        return self.append((str_store_player_face_keys, string_no, player_id))
        
    def player_set_face_keys(self, player_id, string_no):
        """
        (player_set_face_keys, <player_id>, <string_no>),
        Version 1.161+. Sets player's face keys from string.

		Args:
			player_id (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_face_keys(player_id, string_no)
        """
        return self.append((player_set_face_keys, player_id, string_no))
        
    def str_store_troop_face_keys(self, string_no, troop_no, alt):
        """
        (str_store_troop_face_keys, <string_no>, <troop_no>, [<alt>]),
        Version 1.161+. Stores specified troop's face keys into string register. Use optional <alt> parameter to determine what facekey set to retrieve: 0 for first and 1 for second.

		Args:
			string_no (str|int):
			troop_no (str|int):
			alt (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_troop_face_keys(string_no, troop_no, alt)
        """
        return self.append((str_store_troop_face_keys, string_no, troop_no, alt))
        
    def troop_set_face_keys(self, troop_no, string_no, alt):
        """
        (troop_set_face_keys, <troop_no>, <string_no>, [<alt>]),
        Version 1.161+. Sets troop face keys from string. Use optional <alt> parameter to determine what face keys to update: 0 for first and 1 for second.

		Args:
			troop_no (str|int):
			string_no (str|int):
			alt (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_face_keys(troop_no, string_no, alt)
        """
        return self.append((troop_set_face_keys, troop_no, string_no, alt))
        
    def face_keys_get_hair(self, destination, string_no):
        """
        (face_keys_get_hair, <destination>, <string_no>),
        Version 1.161+. Unpacks selected hair mesh from string containing troop/player face keys to <destination>.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_hair(destination, string_no)
        """
        return self.append((face_keys_get_hair, destination, string_no))
        
    def face_keys_set_hair(self, string_no, value):
        """
        (face_keys_set_hair, <string_no>, <value>),
        Version 1.161+. Updates face keys string with a new hair value. Hair meshes associated with skin (as defined in module_skins) are numbered from 1. Use 0 for no hair.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_hair(string_no, value)
        """
        return self.append((face_keys_set_hair, string_no, value))
        
    def face_keys_get_beard(self, destination, string_no):
        """
        (face_keys_get_beard, <destination>, <string_no>),
        Version 1.161+. Unpacks selected beard mesh from string containing troop/player face keys to <destination>.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_beard(destination, string_no)
        """
        return self.append((face_keys_get_beard, destination, string_no))
        
    def face_keys_set_beard(self, string_no, value):
        """
        (face_keys_set_beard, <string_no>, <value>),
        Version 1.161+. Updates face keys string with a new beard value. Beard meshes associated with skin (as defined in module_skins) are numbered from 1. Use 0 for no beard.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_beard(string_no, value)
        """
        return self.append((face_keys_set_beard, string_no, value))
        
    def face_keys_get_face_texture(self, destination, string_no):
        """
        (face_keys_get_face_texture, <destination>, <string_no>),
        Version 1.161+. Unpacks selected face texture from string containing troop/player face keys to <destination>.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_face_texture(destination, string_no)
        """
        return self.append((face_keys_get_face_texture, destination, string_no))
        
    def face_keys_set_face_texture(self, string_no, value):
        """
        (face_keys_set_face_texture, <string_no>, <value>),
        Version 1.161+. Updates face keys string with a new face texture value. Face textures associated with skin (as defined in module_skins) are numbered from 0.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_face_texture(string_no, value)
        """
        return self.append((face_keys_set_face_texture, string_no, value))
        
    def face_keys_get_hair_texture(self, destination, string_no):
        """
        (face_keys_get_hair_texture, <destination>, <string_no>),
        Version 1.161+. Unpacks selected hair texture from string containing troop/player face keys to <destination>. Apparently hair textures have no effect. 4 research.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_hair_texture(destination, string_no)
        """
        return self.append((face_keys_get_hair_texture, destination, string_no))
        
    def face_keys_set_hair_texture(self, string_no, value):
        """
        (face_keys_set_hair_texture, <string_no>, <value>),
        Version 1.161+. Updates face keys string with a new hair texture value. Doesn't seem to have an effect. 4research.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_hair_texture(string_no, value)
        """
        return self.append((face_keys_set_hair_texture, string_no, value))
        
    def face_keys_get_hair_color(self, destination, string_no):
        """
        (face_keys_get_hair_color, <destination>, <string_no>),
        Version 1.161+. Unpacks hair color slider value from face keys string. Values are in the range of 0..63. Mapping to specific colors depends on the hair color range defined for currently selected skin / face_texture combination.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_hair_color(destination, string_no)
        """
        return self.append((face_keys_get_hair_color, destination, string_no))
        
    def face_keys_set_hair_color(self, string_no, value):
        """
        (face_keys_set_hair_color, <string_no>, <value>),
        Version 1.161+. Updates face keys string with a new hair color slider value. Value should be in the 0..63 range.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_hair_color(string_no, value)
        """
        return self.append((face_keys_set_hair_color, string_no, value))
        
    def face_keys_get_age(self, destination, string_no):
        """
        (face_keys_get_age, <destination>, <string_no>),
        Version 1.161+. Unpacks age slider value from face keys string. Values are in the range of 0..63.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_age(destination, string_no)
        """
        return self.append((face_keys_get_age, destination, string_no))
        
    def face_keys_set_age(self, string_no, value):
        """
        (face_keys_set_age, <string_no>, <value>),
        Version 1.161+. Updates face keys string with a new age slider value. Value should be in the 0..63 range.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_age(string_no, value)
        """
        return self.append((face_keys_set_age, string_no, value))
        
    def face_keys_get_skin_color(self, destination, string_no):
        """
        (face_keys_get_skin_color, <destination>, <string_no>),
        Version 1.161+. Apparently doesn't work. Should retrieve skin color value from face keys string into <destination>.

		Args:
			destination (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_skin_color(destination, string_no)
        """
        return self.append((face_keys_get_skin_color, destination, string_no))
        
    def face_keys_set_skin_color(self, string_no, value):
        """
        (face_keys_set_skin_color, <string_no>, <value>),
        Version 1.161+. Apparently doesn't work. Should update face keys string with a new skin color value.

		Args:
			string_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_skin_color(string_no, value)
        """
        return self.append((face_keys_set_skin_color, string_no, value))
        
    def face_keys_get_morph_key(self, destination, string_no, key_no):
        """
        (face_keys_get_morph_key, <destination>, <string_no>, <key_no>),
        Version 1.161+. Unpacks morph key value from face keys string. See morph key indices in module_skins.py file. Note that only 8 out of 27 morph keys are actually accessible (from 'chin_size' to 'cheeks'). Morph key values are in the 0..7 range.

		Args:
			destination (str|int):
			string_no (str|int):
			key_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_get_morph_key(destination, string_no, key_no)
        """
        return self.append((face_keys_get_morph_key, destination, string_no, key_no))
        
    def face_keys_set_morph_key(self, string_no, key_no, value):
        """
        (face_keys_set_morph_key, <string_no>, <key_no>, <value>),
        Version 1.161+. Updates face keys string with a new morph key value. See morph key indices in module_skins.py file. Note that only 8 out of 27 morph keys are actually accessible (from 'chin_size' to 'cheeks'). Morph key values should be in the 0..7 range.

		Args:
			string_no (str|int):
			key_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> face_keys_set_morph_key(string_no, key_no, value)
        """
        return self.append((face_keys_set_morph_key, string_no, key_no, value))
        
    def check_quest_active(self, quest_id):
        """
        (check_quest_active, <quest_id>),
        Checks that the quest has been started but not yet cancelled or completed. Will not fail for concluded, failed or succeeded quests for as long as they have not yet been completed.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> check_quest_active(quest_id)
        """
        return self.append((check_quest_active, quest_id))
        
    def check_quest_finished(self, quest_id):
        """
        (check_quest_finished, <quest_id>),
        Checks that the quest has been completed (result does not matter) and not taken again yet.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> check_quest_finished(quest_id)
        """
        return self.append((check_quest_finished, quest_id))
        
    def check_quest_succeeded(self, quest_id):
        """
        (check_quest_succeeded, <quest_id>),
        Checks that the quest has succeeded and not taken again yet (check will be successful even after the quest is completed).

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> check_quest_succeeded(quest_id)
        """
        return self.append((check_quest_succeeded, quest_id))
        
    def check_quest_failed(self, quest_id):
        """
        (check_quest_failed, <quest_id>),
        Checks that the quest has failed and not taken again yet (check will be successful even after the quest is completed).

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> check_quest_failed(quest_id)
        """
        return self.append((check_quest_failed, quest_id))
        
    def check_quest_concluded(self, quest_id):
        """
        (check_quest_concluded, <quest_id>),
        Checks that the quest was concluded with any result and not taken again yet.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> check_quest_concluded(quest_id)
        """
        return self.append((check_quest_concluded, quest_id))
        
    def quest_set_slot(self, quest_id, slot_no, value):
        """
        (quest_set_slot, <quest_id>, <slot_no>, <value>),
        

		Args:
			quest_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> quest_set_slot(quest_id, slot_no, value)
        """
        return self.append((quest_set_slot, quest_id, slot_no, value))
        
    def quest_get_slot(self, destination, quest_id, slot_no):
        """
        (quest_get_slot, <destination>, <quest_id>, <slot_no>),
        

		Args:
			destination (str|int):
			quest_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> quest_get_slot(destination, quest_id, slot_no)
        """
        return self.append((quest_get_slot, destination, quest_id, slot_no))
        
    def quest_slot_eq(self, quest_id, slot_no, value):
        """
        (quest_slot_eq, <quest_id>, <slot_no>, <value>),
        

		Args:
			quest_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> quest_slot_eq(quest_id, slot_no, value)
        """
        return self.append((quest_slot_eq, quest_id, slot_no, value))
        
    def quest_slot_ge(self, quest_id, slot_no, value):
        """
        (quest_slot_ge, <quest_id>, <slot_no>, <value>),
        

		Args:
			quest_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> quest_slot_ge(quest_id, slot_no, value)
        """
        return self.append((quest_slot_ge, quest_id, slot_no, value))
        
    def start_quest(self, quest_id, giver_troop_id):
        """
        (start_quest, <quest_id>, <giver_troop_id>),
        Starts the quest and marks giver_troop as the troop who gave it.

		Args:
			quest_id (str|int):
			giver_troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_quest(quest_id, giver_troop_id)
        """
        return self.append((start_quest, quest_id, giver_troop_id))
        
    def conclude_quest(self, quest_id):
        """
        (conclude_quest, <quest_id>),
        Sets quest status as concluded but keeps it in the list. Frequently used to indicate "uncertain" quest status, when it's neither fully successful nor a total failure.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> conclude_quest(quest_id)
        """
        return self.append((conclude_quest, quest_id))
        
    def succeed_quest(self, quest_id):
        """
        (succeed_quest, <quest_id>),
        also concludes the quest
		Sets quest status as successful but keeps it in the list (player must visit quest giver to complete it before he can get another quest of the same type).

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> succeed_quest(quest_id)
        """
        return self.append((succeed_quest, quest_id))
        
    def fail_quest(self, quest_id):
        """
        (fail_quest, <quest_id>),
        also concludes the quest
		Sets quest status as failed but keeps it in the list (player must visit quest giver to complete it before he can get another quest of the same type).

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> fail_quest(quest_id)
        """
        return self.append((fail_quest, quest_id))
        
    def complete_quest(self, quest_id):
        """
        (complete_quest, <quest_id>),
        Successfully completes specified quest, removing it from the list of active quests.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> complete_quest(quest_id)
        """
        return self.append((complete_quest, quest_id))
        
    def cancel_quest(self, quest_id):
        """
        (cancel_quest, <quest_id>),
        Cancels specified quest without completing it, removing it from the list of active quests.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cancel_quest(quest_id)
        """
        return self.append((cancel_quest, quest_id))
        
    def setup_quest_text(self, quest_id):
        """
        (setup_quest_text, <quest_id>),
        Operation will refresh default quest description (as defined in module_quests.py). This is important when quest description contains references to variables and registers which need to be initialized with their current values.

		Args:
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> setup_quest_text(quest_id)
        """
        return self.append((setup_quest_text, quest_id))
        
    def store_partner_quest(self, destination):
        """
        (store_partner_quest, <destination>),
        During conversation, if there's a quest given by conversation partner, the operation will return it's id.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_partner_quest(destination)
        """
        return self.append((store_partner_quest, destination))
        
    def setup_quest_giver(self, quest_id, string_id):
        """
        (setup_quest_giver, <quest_id>, <string_id>),
        Apparently deprecated, as quest giver troop is now defined as a parameter of (start_quest).

		Args:
			quest_id (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> setup_quest_giver(quest_id, string_id)
        """
        return self.append((setup_quest_giver, quest_id, string_id))
        
    def store_random_quest_in_range(self, destination, lower_bound, upper_bound):
        """
        (store_random_quest_in_range, <destination>, <lower_bound>, <upper_bound>),
        Apparently deprecated as the logic for picking a new quest has been moved to module_scripts.

		Args:
			destination (str|int):
			lower_bound (str|int):
			upper_bound (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_quest_in_range(destination, lower_bound, upper_bound)
        """
        return self.append((store_random_quest_in_range, destination, lower_bound, upper_bound))
        
    def set_quest_progression(self, quest_id, value):
        """
        (set_quest_progression, <quest_id>, <value>),
        Deprecated and useless, operation has no game effects and it's impossible to retrieve quest progression status anyway.

		Args:
			quest_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_quest_progression(quest_id, value)
        """
        return self.append((set_quest_progression, quest_id, value))
        
    def store_random_troop_to_raise(self, destination, lower_bound, upper_bound):
        """
        (store_random_troop_to_raise, <destination>, <lower_bound>, <upper_bound>),
        Apparently deprecated.

		Args:
			destination (str|int):
			lower_bound (str|int):
			upper_bound (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_troop_to_raise(destination, lower_bound, upper_bound)
        """
        return self.append((store_random_troop_to_raise, destination, lower_bound, upper_bound))
        
    def store_random_troop_to_capture(self, destination, lower_bound, upper_bound):
        """
        (store_random_troop_to_capture, <destination>, <lower_bound>, <upper_bound>),
        Apparently deprecated.

		Args:
			destination (str|int):
			lower_bound (str|int):
			upper_bound (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_troop_to_capture(destination, lower_bound, upper_bound)
        """
        return self.append((store_random_troop_to_capture, destination, lower_bound, upper_bound))
        
    def store_quest_number(self, destination, quest_id):
        """
        (store_quest_number, <destination>, <quest_id>),
        Apparently deprecated.

		Args:
			destination (str|int):
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_quest_number(destination, quest_id)
        """
        return self.append((store_quest_number, destination, quest_id))
        
    def store_quest_item(self, destination, item_id):
        """
        (store_quest_item, <destination>, <item_id>),
        Apparently deprecated. Native now uses quest slots to keep track of this information.

		Args:
			destination (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_quest_item(destination, item_id)
        """
        return self.append((store_quest_item, destination, item_id))
        
    def store_quest_troop(self, destination, troop_id):
        """
        (store_quest_troop, <destination>, <troop_id>),
        Apparently deprecated. Native now uses quest slots to keep track of this information.

		Args:
			destination (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_quest_troop(destination, troop_id)
        """
        return self.append((store_quest_troop, destination, troop_id))
        
    def item_has_property(self, item_kind_no, property):
        """
        (item_has_property, <item_kind_no>, <property>),
        Version 1.161+. Check that the item has specified property flag set. See the list of itp_* flags in header_items.py.

		Args:
			item_kind_no (str|int):
			property (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_has_property(item_kind_no, property)
        """
        return self.append((item_has_property, item_kind_no, property))
        
    def item_has_capability(self, item_kind_no, capability):
        """
        (item_has_capability, <item_kind_no>, <capability>),
        Version 1.161+. Checks that the item has specified capability flag set. See the list of itcf_* flags in header_items.py

		Args:
			item_kind_no (str|int):
			capability (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_has_capability(item_kind_no, capability)
        """
        return self.append((item_has_capability, item_kind_no, capability))
        
    def item_has_modifier(self, item_kind_no, item_modifier_no):
        """
        (item_has_modifier, <item_kind_no>, <item_modifier_no>),
        Version 1.161+. Checks that the specified modifiers is valid for the item. See the list of imod_* values in header_item_modifiers.py.

		Args:
			item_kind_no (str|int):
			item_modifier_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_has_modifier(item_kind_no, item_modifier_no)
        """
        return self.append((item_has_modifier, item_kind_no, item_modifier_no))
        
    def item_has_faction(self, item_kind_no, faction_no):
        """
        (item_has_faction, <item_kind_no>, <faction_no>),
        Version 1.161+. Checks that the item is available for specified faction. Note that an item with no factions set is available to all factions.

		Args:
			item_kind_no (str|int):
			faction_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_has_faction(item_kind_no, faction_no)
        """
        return self.append((item_has_faction, item_kind_no, faction_no))
        
    def item_set_slot(self, item_id, slot_no, value):
        """
        (item_set_slot, <item_id>, <slot_no>, <value>),
        

		Args:
			item_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_set_slot(item_id, slot_no, value)
        """
        return self.append((item_set_slot, item_id, slot_no, value))
        
    def item_get_slot(self, destination, item_id, slot_no):
        """
        (item_get_slot, <destination>, <item_id>, <slot_no>),
        

		Args:
			destination (str|int):
			item_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_slot(destination, item_id, slot_no)
        """
        return self.append((item_get_slot, destination, item_id, slot_no))
        
    def item_slot_eq(self, item_id, slot_no, value):
        """
        (item_slot_eq, <item_id>, <slot_no>, <value>),
        

		Args:
			item_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_slot_eq(item_id, slot_no, value)
        """
        return self.append((item_slot_eq, item_id, slot_no, value))
        
    def item_slot_ge(self, item_id, slot_no, value):
        """
        (item_slot_ge, <item_id>, <slot_no>, <value>),
        

		Args:
			item_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_slot_ge(item_id, slot_no, value)
        """
        return self.append((item_slot_ge, item_id, slot_no, value))
        
    def item_get_type(self, destination, item_id):
        """
        (item_get_type, <destination>, <item_id>),
        Returns item class (see header_items.py for itp_type_* constants).

		Args:
			destination (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_type(destination, item_id)
        """
        return self.append((item_get_type, destination, item_id))
        
    def store_item_value(self, destination, item_id):
        """
        (store_item_value, <destination>, <item_id>),
        Stores item nominal price as listed in module_items.py. Does not take item modifier or quantity (for food items) into account.

		Args:
			destination (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_item_value(destination, item_id)
        """
        return self.append((store_item_value, destination, item_id))
        
    def store_random_horse(self, destination):
        """
        (store_random_horse, <destination>),
        Deprecated since early M&B days.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_horse(destination)
        """
        return self.append((store_random_horse, destination))
        
    def store_random_equipment(self, destination):
        """
        (store_random_equipment, <destination>),
        Deprecated since early M&B days.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_equipment(destination)
        """
        return self.append((store_random_equipment, destination))
        
    def store_random_armor(self, destination):
        """
        (store_random_armor, <destination>),
        Deprecated since early M&B days.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_random_armor(destination)
        """
        return self.append((store_random_armor, destination))
        
    def cur_item_add_mesh(self, mesh_name_string, lod_begin, lod_end):
        """
        (cur_item_add_mesh, <mesh_name_string>, [<lod_begin>], [<lod_end>]),
        Version 1.161+. Only call inside ti_on_init_item trigger. Adds another mesh to item, allowing the creation of combined items. Parameter <mesh_name_string> should contain mesh name itself, NOT a mesh reference. LOD values are optional. If <lod_end> is used, it will not be loaded.

		Args:
			mesh_name_string (str|int):
			lod_begin (str|int):
			lod_end (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_item_add_mesh(mesh_name_string, lod_begin, lod_end)
        """
        return self.append((cur_item_add_mesh, mesh_name_string, lod_begin, lod_end))
        
    def cur_item_set_material(self, string_no, sub_mesh_no, lod_begin, lod_end):
        """
        (cur_item_set_material, <string_no>, <sub_mesh_no>, [<lod_begin>], [<lod_end>]),
        Version 1.161+. Only call inside ti_on_init_item trigger. Replaces material that will be used to render the item mesh. Use 0 for <sub_mesh_no> to replace material for base mesh. LOD values are optional. If <lod_end> is used, it will not be loaded.

		Args:
			string_no (str|int):
			sub_mesh_no (str|int):
			lod_begin (str|int):
			lod_end (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_item_set_material(string_no, sub_mesh_no, lod_begin, lod_end)
        """
        return self.append((cur_item_set_material, string_no, sub_mesh_no, lod_begin, lod_end))
        
    def item_get_weight(self, destination_fixed_point, item_kind_no):
        """
        (item_get_weight, <destination_fixed_point>, <item_kind_no>),
        Version 1.161+. Retrieves item weight as a fixed point value.

		Args:
			destination_fixed_point (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_weight(destination_fixed_point, item_kind_no)
        """
        return self.append((item_get_weight, destination_fixed_point, item_kind_no))
        
    def item_get_value(self, destination, item_kind_no):
        """
        (item_get_value, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item base price. Essentially a duplicate of (store_item_value).

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_value(destination, item_kind_no)
        """
        return self.append((item_get_value, destination, item_kind_no))
        
    def item_get_difficulty(self, destination, item_kind_no):
        """
        (item_get_difficulty, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item difficulty value.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_difficulty(destination, item_kind_no)
        """
        return self.append((item_get_difficulty, destination, item_kind_no))
        
    def item_get_head_armor(self, destination, item_kind_no):
        """
        (item_get_head_armor, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item head armor value.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_head_armor(destination, item_kind_no)
        """
        return self.append((item_get_head_armor, destination, item_kind_no))
        
    def item_get_body_armor(self, destination, item_kind_no):
        """
        (item_get_body_armor, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item body armor value.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_body_armor(destination, item_kind_no)
        """
        return self.append((item_get_body_armor, destination, item_kind_no))
        
    def item_get_leg_armor(self, destination, item_kind_no):
        """
        (item_get_leg_armor, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item leg armor value.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_leg_armor(destination, item_kind_no)
        """
        return self.append((item_get_leg_armor, destination, item_kind_no))
        
    def item_get_hit_points(self, destination, item_kind_no):
        """
        (item_get_hit_points, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item hit points amount.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_hit_points(destination, item_kind_no)
        """
        return self.append((item_get_hit_points, destination, item_kind_no))
        
    def item_get_weapon_length(self, destination, item_kind_no):
        """
        (item_get_weapon_length, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item length (for weapons) or shield half-width (for shields). To get actual shield width, multiply this value by 2. Essentially, it is a distance from shield's "center" point to it's left, right and top edges (and bottom edge as well if shield height is not defined).

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_weapon_length(destination, item_kind_no)
        """
        return self.append((item_get_weapon_length, destination, item_kind_no))
        
    def item_get_speed_rating(self, destination, item_kind_no):
        """
        (item_get_speed_rating, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item speed rating.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_speed_rating(destination, item_kind_no)
        """
        return self.append((item_get_speed_rating, destination, item_kind_no))
        
    def item_get_missile_speed(self, destination, item_kind_no):
        """
        (item_get_missile_speed, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item missile speed rating.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_missile_speed(destination, item_kind_no)
        """
        return self.append((item_get_missile_speed, destination, item_kind_no))
        
    def item_get_max_ammo(self, destination, item_kind_no):
        """
        (item_get_max_ammo, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item max ammo amount.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_max_ammo(destination, item_kind_no)
        """
        return self.append((item_get_max_ammo, destination, item_kind_no))
        
    def item_get_accuracy(self, destination, item_kind_no):
        """
        (item_get_accuracy, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves item accuracy value. Note that this operation will return 0 for an item with undefined accuracy, even though the item accuracy will actually default to 100.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_accuracy(destination, item_kind_no)
        """
        return self.append((item_get_accuracy, destination, item_kind_no))
        
    def item_get_shield_height(self, destination_fixed_point, item_kind_no):
        """
        (item_get_shield_height, <destination_fixed_point>, <item_kind_no>),
        Version 1.161+. Retrieves distance from shield "center" to it's bottom edge as a fixed point number. Use (set_fixed_point_multiplier, 100), to retrieve the correct value with this operation. To get actual shield height, use shield_height + weapon_length if this operation returns a non-zero value, otherwise use 2 * weapon_length.

		Args:
			destination_fixed_point (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_shield_height(destination_fixed_point, item_kind_no)
        """
        return self.append((item_get_shield_height, destination_fixed_point, item_kind_no))
        
    def item_get_horse_scale(self, destination_fixed_point, item_kind_no):
        """
        (item_get_horse_scale, <destination_fixed_point>, <item_kind_no>),
        Version 1.161+. Retrieves horse scale value as fixed point number.

		Args:
			destination_fixed_point (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_horse_scale(destination_fixed_point, item_kind_no)
        """
        return self.append((item_get_horse_scale, destination_fixed_point, item_kind_no))
        
    def item_get_horse_speed(self, destination, item_kind_no):
        """
        (item_get_horse_speed, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves horse speed value.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_horse_speed(destination, item_kind_no)
        """
        return self.append((item_get_horse_speed, destination, item_kind_no))
        
    def item_get_horse_maneuver(self, destination, item_kind_no):
        """
        (item_get_horse_maneuver, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves horse maneuverability value.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_horse_maneuver(destination, item_kind_no)
        """
        return self.append((item_get_horse_maneuver, destination, item_kind_no))
        
    def item_get_food_quality(self, destination, item_kind_no):
        """
        (item_get_food_quality, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves food quality coefficient (as of Warband 1.165, this coefficient is actually set for many food items, but never used in the code as there was no way to retrieve this coeff before 1.161 patch).

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_food_quality(destination, item_kind_no)
        """
        return self.append((item_get_food_quality, destination, item_kind_no))
        
    def item_get_abundance(self, destination, item_kind_no):
        """
        (item_get_abundance, <destination>, <item_kind_no>),
        Version 1.161+. Retrieve item abundance value. Note that this operation will return 0 for an item with undefined abundance, even though the item abundance will actually default to 100.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_abundance(destination, item_kind_no)
        """
        return self.append((item_get_abundance, destination, item_kind_no))
        
    def item_get_thrust_damage(self, destination, item_kind_no):
        """
        (item_get_thrust_damage, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves thrust base damage value for item.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_thrust_damage(destination, item_kind_no)
        """
        return self.append((item_get_thrust_damage, destination, item_kind_no))
        
    def item_get_thrust_damage_type(self, destination, item_kind_no):
        """
        (item_get_thrust_damage_type, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves thrust damage type for item (see definitions for "cut", "pierce" and "blunt" in header_items.py).

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_thrust_damage_type(destination, item_kind_no)
        """
        return self.append((item_get_thrust_damage_type, destination, item_kind_no))
        
    def item_get_swing_damage(self, destination, item_kind_no):
        """
        (item_get_swing_damage, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves swing base damage value for item.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_swing_damage(destination, item_kind_no)
        """
        return self.append((item_get_swing_damage, destination, item_kind_no))
        
    def item_get_swing_damage_type(self, destination, item_kind_no):
        """
        (item_get_swing_damage_type, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves swing damage type for item (see definitions for "cut", "pierce" and "blunt" in header_items.py).

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_swing_damage_type(destination, item_kind_no)
        """
        return self.append((item_get_swing_damage_type, destination, item_kind_no))
        
    def item_get_horse_charge_damage(self, destination, item_kind_no):
        """
        (item_get_horse_charge_damage, <destination>, <item_kind_no>),
        Version 1.161+. Retrieves horse charge base damage.

		Args:
			destination (str|int):
			item_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> item_get_horse_charge_damage(destination, item_kind_no)
        """
        return self.append((item_get_horse_charge_damage, destination, item_kind_no))
        
    def play_sound_at_position(self, sound_id, position, options):
        """
        (play_sound_at_position, <sound_id>, <position>, [options]),
        Plays a sound in specified scene position. See sf_* flags in header_sounds.py for reference on possible options.

		Args:
			sound_id (str|int):
			position (str|int):
			options (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> play_sound_at_position(sound_id, position, options)
        """
        return self.append((play_sound_at_position, sound_id, position, options))
        
    def play_sound(self, sound_id, options):
        """
        (play_sound, <sound_id>, [options]),
        Plays a sound. If the operation is called from agent, scene_prop or item trigger, then the sound will be positional and 3D. See sf_* flags in header_sounds.py for reference on possible options.

		Args:
			sound_id (str|int):
			options (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> play_sound(sound_id, options)
        """
        return self.append((play_sound, sound_id, options))
        
    def play_track(self, track_id, options):
        """
        (play_track, <track_id>, [options]),
        Plays specified music track. Possible options: 0 = finish current then play this, 1 = fade out current and start this, 2 = stop current abruptly and start this

		Args:
			track_id (str|int):
			options (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> play_track(track_id, options)
        """
        return self.append((play_track, track_id, options))
        
    def play_cue_track(self, track_id):
        """
        (play_cue_track, <track_id>),
        Plays specified music track OVER any currently played music track (so you can get two music tracks playing simultaneously). Hardly useful.

		Args:
			track_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> play_cue_track(track_id)
        """
        return self.append((play_cue_track, track_id))
        
    def music_set_situation(self, situation_type):
        """
        (music_set_situation, <situation_type>),
        Sets current situation(s) in the game (see mtf_* flags in header_music.py for reference) so the game engine can pick matching tracks from module_music.py. Use 0 to stop any currently playing music (it will resume when situation is later set to something).

		Args:
			situation_type (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> music_set_situation(situation_type)
        """
        return self.append((music_set_situation, situation_type))
        
    def music_set_culture(self, culture_type):
        """
        (music_set_culture, <culture_type>),
        Sets current culture(s) in the game (see mtf_* flags in header_music.py for reference) so the game engine can pick matching tracks from module_music.py. Use 0 to stop any currently playing music (it will resume when cultures are later set to something).

		Args:
			culture_type (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> music_set_culture(culture_type)
        """
        return self.append((music_set_culture, culture_type))
        
    def stop_all_sounds(self, options):
        """
        (stop_all_sounds, [options]),
        Stops all playing sounds. Version 1.153 options: 0 = stop only looping sounds, 1 = stop all sounds. Version 1.143 options: 0 = let current track finish, 1 = fade it out, 2 = stop it abruptly.

		Args:
			options (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> stop_all_sounds(options)
        """
        return self.append((stop_all_sounds, options))
        
    def store_last_sound_channel(self, destination):
        """
        (store_last_sound_channel, <destination>),
        Version 1.153+. UNTESTED. Stores the sound channel used for the last sound operation.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_last_sound_channel(destination)
        """
        return self.append((store_last_sound_channel, destination))
        
    def stop_sound_channel(self, sound_channel_no):
        """
        (stop_sound_channel, <sound_channel_no>),
        Version 1.153+. UNTESTED. Stops sound playing on specified sound channel.

		Args:
			sound_channel_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> stop_sound_channel(sound_channel_no)
        """
        return self.append((stop_sound_channel, sound_channel_no))
        
    def init_position(self, position):
        """
        (init_position, <position>),
        Sets position coordinates to [0,0,0], without any rotation and default scale.

		Args:
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> init_position(position)
        """
        return self.append((init_position, position))
        
    def copy_position(self, position_target, position_source):
        """
        (copy_position, <position_target>, <position_source>),
        Makes a duplicate of position_source.

		Args:
			position_target (str|int):
			position_source (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> copy_position(position_target, position_source)
        """
        return self.append((copy_position, position_target, position_source))
        
    def position_copy_origin(self, position_target, position_source):
        """
        (position_copy_origin, <position_target>, <position_source>),
        Copies coordinates from source position to target position, without changing rotation or scale.

		Args:
			position_target (str|int):
			position_source (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_copy_origin(position_target, position_source)
        """
        return self.append((position_copy_origin, position_target, position_source))
        
    def position_copy_rotation(self, position_target, position_source):
        """
        (position_copy_rotation, <position_target>, <position_source>),
        Copies rotation from source position to target position, without changing coordinates or scale.

		Args:
			position_target (str|int):
			position_source (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_copy_rotation(position_target, position_source)
        """
        return self.append((position_copy_rotation, position_target, position_source))
        
    def position_transform_position_to_parent(self, position_dest, position_anchor, position_relative_to_anchor):
        """
        (position_transform_position_to_parent, <position_dest>, <position_anchor>, <position_relative_to_anchor>),
        Converts position from local coordinate space to parent coordinate space. In other words, if you have some position on the scene (anchor) and a position describing some place *relative* to anchor (for example [10,20,0] means "20 meters forward and 10 meters to the right"), after calling this operation you will get that position coordinates on the scene in <position_dest>. Rotation and scale is also taken care of, so you can use relative angles.

		Args:
			position_dest (str|int):
			position_anchor (str|int):
			position_relative_to_anchor (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_transform_position_to_parent(position_dest, position_anchor, position_relative_to_anchor)
        """
        return self.append((position_transform_position_to_parent, position_dest, position_anchor, position_relative_to_anchor))
        
    def position_transform_position_to_local(self, position_dest, position_anchor, position_source):
        """
        (position_transform_position_to_local, <position_dest>, <position_anchor>, <position_source>),
        The opposite to (position_transform_position_to_parent), this operation allows you to get source's *relative* position to your anchor. Suppose you want to run some decision making for your bot agent depending on player's position. In order to know where player is located relative to your bot you call (position_transform_position_to_local, <position_dest>, <bot_position>, <player_position>). Then we check position_dest's Y coordinate - if it's negative, then the player is behind our bot's back.

		Args:
			position_dest (str|int):
			position_anchor (str|int):
			position_source (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_transform_position_to_local(position_dest, position_anchor, position_source)
        """
        return self.append((position_transform_position_to_local, position_dest, position_anchor, position_source))
        
    def position_get_x(self, destination_fixed_point, position):
        """
        (position_get_x, <destination_fixed_point>, <position>),
        Return position X coordinate (to the east, or to the right). Base unit is meters. Use (set_fixed_point_multiplier) to set another measurement unit (100 will get you centimeters, 1000 will get you millimeters, etc).

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_x(destination_fixed_point, position)
        """
        return self.append((position_get_x, destination_fixed_point, position))
        
    def position_get_y(self, destination_fixed_point, position):
        """
        (position_get_y, <destination_fixed_point>, <position>),
        Return position Y coordinate (to the north, or forward). Base unit is meters. Use (set_fixed_point_multiplier) to set another measurement unit (100 will get you centimeters, 1000 will get you millimeters, etc).

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_y(destination_fixed_point, position)
        """
        return self.append((position_get_y, destination_fixed_point, position))
        
    def position_get_z(self, destination_fixed_point, position):
        """
        (position_get_z, <destination_fixed_point>, <position>),
        Return position Z coordinate (to the top). Base unit is meters. Use (set_fixed_point_multiplier) to set another measurement unit (100 will get you centimeters, 1000 will get you millimeters, etc).

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_z(destination_fixed_point, position)
        """
        return self.append((position_get_z, destination_fixed_point, position))
        
    def position_set_x(self, position, value_fixed_point):
        """
        (position_set_x, <position>, <value_fixed_point>),
        Set position X coordinate.

		Args:
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_x(position, value_fixed_point)
        """
        return self.append((position_set_x, position, value_fixed_point))
        
    def position_set_y(self, position, value_fixed_point):
        """
        (position_set_y, <position>, <value_fixed_point>),
        Set position Y coordinate.

		Args:
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_y(position, value_fixed_point)
        """
        return self.append((position_set_y, position, value_fixed_point))
        
    def position_set_z(self, position, value_fixed_point):
        """
        (position_set_z, <position>, <value_fixed_point>),
        Set position Z coordinate.

		Args:
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_z(position, value_fixed_point)
        """
        return self.append((position_set_z, position, value_fixed_point))
        
    def position_move_x(self, position, movement, value):
        """
        (position_move_x, <position>, <movement>, [value]),
        Moves position along X axis. Movement distance is in cms. Optional parameter determines whether the position is moved along the local (value=0) or global (value=1) X axis (i.e. whether the position will be moved to it's right/left, or to the global east/west).

		Args:
			position (str|int):
			movement (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_move_x(position, movement, value)
        """
        return self.append((position_move_x, position, movement, value))
        
    def position_move_y(self, position, movement, value):
        """
        (position_move_y, <position>, <movement>, [value]),
        Moves position along Y axis. Movement distance is in cms. Optional parameter determines whether the position is moved along the local (value=0) or global (value=1) Y axis (i.e. whether the position will be moved forward/backwards, or to the global north/south).

		Args:
			position (str|int):
			movement (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_move_y(position, movement, value)
        """
        return self.append((position_move_y, position, movement, value))
        
    def position_move_z(self, position, movement, value):
        """
        (position_move_z, <position>, <movement>, [value]),
        Moves position along Z axis. Movement distance is in cms. Optional parameter determines whether the position is moved along the local (value=0) or global (value=1) Z axis (i.e. whether the position will be moved to it's above/below, or to the global above/below - these directions will be different if the position is tilted).

		Args:
			position (str|int):
			movement (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_move_z(position, movement, value)
        """
        return self.append((position_move_z, position, movement, value))
        
    def position_set_z_to_ground_level(self, position):
        """
        (position_set_z_to_ground_level, <position>),
        This will bring the position Z coordinate so it rests on the ground level (i.e. an agent could stand on that position). This takes scene props with their collision meshes into account. Only works during a mission, so you can't measure global map height using this.

		Args:
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_z_to_ground_level(position)
        """
        return self.append((position_set_z_to_ground_level, position))
        
    def position_get_distance_to_terrain(self, destination, position):
        """
        (position_get_distance_to_terrain, <destination>, <position>),
        This will measure the distance between position and terrain below, ignoring all scene props and their collision meshes. Operation only works on the scenes and cannot be used on the global map.

		Args:
			destination (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_distance_to_terrain(destination, position)
        """
        return self.append((position_get_distance_to_terrain, destination, position))
        
    def position_get_distance_to_ground_level(self, destination, position):
        """
        (position_get_distance_to_ground_level, <destination>, <position>),
        This will measure the distance between position and the ground level, taking scene props and their collision meshes into account. Operation only works on the scenes and cannot be used on the global map.

		Args:
			destination (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_distance_to_ground_level(destination, position)
        """
        return self.append((position_get_distance_to_ground_level, destination, position))
        
    def position_get_rotation_around_x(self, destination, position):
        """
        (position_get_rotation_around_x, <destination>, <position>),
        Returns angle (in degrees) that the position is rotated around X axis (tilt forward/backwards).

		Args:
			destination (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_rotation_around_x(destination, position)
        """
        return self.append((position_get_rotation_around_x, destination, position))
        
    def position_get_rotation_around_y(self, destination, position):
        """
        (position_get_rotation_around_y, <destination>, <position>),
        Returns angle (in degrees) that the position is rotated around Y axis (tilt right/left).

		Args:
			destination (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_rotation_around_y(destination, position)
        """
        return self.append((position_get_rotation_around_y, destination, position))
        
    def position_get_rotation_around_z(self, destination, position):
        """
        (position_get_rotation_around_z, <destination>, <position>),
        Returns angle (in degrees) that the position is rotated around Z axis (turning right/left).

		Args:
			destination (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_rotation_around_z(destination, position)
        """
        return self.append((position_get_rotation_around_z, destination, position))
        
    def position_rotate_x(self, position, angle):
        """
        (position_rotate_x, <position>, <angle>),
        Rotates position around it's X axis (tilt forward/backwards).

		Args:
			position (str|int):
			angle (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_rotate_x(position, angle)
        """
        return self.append((position_rotate_x, position, angle))
        
    def position_rotate_y(self, position, angle):
        """
        (position_rotate_y, <position>, <angle>),
        Rotates position around Y axis (tilt right/left).

		Args:
			position (str|int):
			angle (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_rotate_y(position, angle)
        """
        return self.append((position_rotate_y, position, angle))
        
    def position_rotate_z(self, position, angle, use_global_z_axis):
        """
        (position_rotate_z, <position>, <angle>, [use_global_z_axis]),
        Rotates position around Z axis (rotate right/left). Pass 1 for use_global_z_axis to rotate the position around global axis instead.

		Args:
			position (str|int):
			angle (str|int):
			use_global_z_axis (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_rotate_z(position, angle, use_global_z_axis)
        """
        return self.append((position_rotate_z, position, angle, use_global_z_axis))
        
    def position_rotate_x_floating(self, position, angle_fixed_point):
        """
        (position_rotate_x_floating, <position>, <angle_fixed_point>),
        Same as (position_rotate_x), but takes fixed point value as parameter, allowing for more precise rotation.

		Args:
			position (str|int):
			angle_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_rotate_x_floating(position, angle_fixed_point)
        """
        return self.append((position_rotate_x_floating, position, angle_fixed_point))
        
    def position_rotate_y_floating(self, position, angle_fixed_point):
        """
        (position_rotate_y_floating, <position>, <angle_fixed_point>),
        Same as (position_rotate_y), but takes fixed point value as parameter, allowing for more precise rotation.

		Args:
			position (str|int):
			angle_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_rotate_y_floating(position, angle_fixed_point)
        """
        return self.append((position_rotate_y_floating, position, angle_fixed_point))
        
    def position_rotate_z_floating(self, position_no, angle_fixed_point):
        """
        (position_rotate_z_floating, <position_no>, <angle_fixed_point>),
        Version 1.161+. Same as (position_rotate_z), but takes fixed point value as parameter, allowing for more precise rotation.

		Args:
			position_no (str|int):
			angle_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_rotate_z_floating(position_no, angle_fixed_point)
        """
        return self.append((position_rotate_z_floating, position_no, angle_fixed_point))
        
    def position_get_scale_x(self, destination_fixed_point, position):
        """
        (position_get_scale_x, <destination_fixed_point>, <position>),
        Retrieves position scaling along X axis.

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_scale_x(destination_fixed_point, position)
        """
        return self.append((position_get_scale_x, destination_fixed_point, position))
        
    def position_get_scale_y(self, destination_fixed_point, position):
        """
        (position_get_scale_y, <destination_fixed_point>, <position>),
        Retrieves position scaling along Y axis.

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_scale_y(destination_fixed_point, position)
        """
        return self.append((position_get_scale_y, destination_fixed_point, position))
        
    def position_get_scale_z(self, destination_fixed_point, position):
        """
        (position_get_scale_z, <destination_fixed_point>, <position>),
        Retrieves position scaling along Z axis.

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_scale_z(destination_fixed_point, position)
        """
        return self.append((position_get_scale_z, destination_fixed_point, position))
        
    def position_set_scale_x(self, position, value_fixed_point):
        """
        (position_set_scale_x, <position>, <value_fixed_point>),
        Sets position scaling along X axis.

		Args:
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_scale_x(position, value_fixed_point)
        """
        return self.append((position_set_scale_x, position, value_fixed_point))
        
    def position_set_scale_y(self, position, value_fixed_point):
        """
        (position_set_scale_y, <position>, <value_fixed_point>),
        Sets position scaling along Y axis.

		Args:
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_scale_y(position, value_fixed_point)
        """
        return self.append((position_set_scale_y, position, value_fixed_point))
        
    def position_set_scale_z(self, position, value_fixed_point):
        """
        (position_set_scale_z, <position>, <value_fixed_point>),
        Sets position scaling along Z axis.

		Args:
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_set_scale_z(position, value_fixed_point)
        """
        return self.append((position_set_scale_z, position, value_fixed_point))
        
    def get_angle_between_positions(self, destination_fixed_point, position_no_1, position_no_2):
        """
        (get_angle_between_positions, <destination_fixed_point>, <position_no_1>, <position_no_2>),
        Calculates angle between positions, using positions as vectors. Only rotation around Z axis is used. In other words, the function returns the difference between Z rotations of both positions.

		Args:
			destination_fixed_point (str|int):
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_angle_between_positions(destination_fixed_point, position_no_1, position_no_2)
        """
        return self.append((get_angle_between_positions, destination_fixed_point, position_no_1, position_no_2))
        
    def position_has_line_of_sight_to_position(self, position_no_1, position_no_2):
        """
        (position_has_line_of_sight_to_position, <position_no_1>, <position_no_2>),
        Checks that you can see one position from another. This obviously implies that both positions must be in global space. Note this is computationally expensive, so try to keep number of these to a minimum.

		Args:
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_has_line_of_sight_to_position(position_no_1, position_no_2)
        """
        return self.append((position_has_line_of_sight_to_position, position_no_1, position_no_2))
        
    def get_distance_between_positions(self, destination, position_no_1, position_no_2):
        """
        (get_distance_between_positions, <destination>, <position_no_1>, <position_no_2>),
        Returns distance between positions in centimeters.

		Args:
			destination (str|int):
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_distance_between_positions(destination, position_no_1, position_no_2)
        """
        return self.append((get_distance_between_positions, destination, position_no_1, position_no_2))
        
    def get_distance_between_positions_in_meters(self, destination, position_no_1, position_no_2):
        """
        (get_distance_between_positions_in_meters, <destination>, <position_no_1>, <position_no_2>),
        Returns distance between positions in meters.

		Args:
			destination (str|int):
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_distance_between_positions_in_meters(destination, position_no_1, position_no_2)
        """
        return self.append((get_distance_between_positions_in_meters, destination, position_no_1, position_no_2))
        
    def get_sq_distance_between_positions(self, destination, position_no_1, position_no_2):
        """
        (get_sq_distance_between_positions, <destination>, <position_no_1>, <position_no_2>),
        Returns squared distance between two positions in centimeters.

		Args:
			destination (str|int):
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_sq_distance_between_positions(destination, position_no_1, position_no_2)
        """
        return self.append((get_sq_distance_between_positions, destination, position_no_1, position_no_2))
        
    def get_sq_distance_between_positions_in_meters(self, destination, position_no_1, position_no_2):
        """
        (get_sq_distance_between_positions_in_meters, <destination>, <position_no_1>, <position_no_2>),
        Returns squared distance between two positions in meters.

		Args:
			destination (str|int):
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_sq_distance_between_positions_in_meters(destination, position_no_1, position_no_2)
        """
        return self.append((get_sq_distance_between_positions_in_meters, destination, position_no_1, position_no_2))
        
    def position_is_behind_position(self, position_base, position_to_check):
        """
        (position_is_behind_position, <position_base>, <position_to_check>),
        Checks if the second position is behind the first.

		Args:
			position_base (str|int):
			position_to_check (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_is_behind_position(position_base, position_to_check)
        """
        return self.append((position_is_behind_position, position_base, position_to_check))
        
    def get_sq_distance_between_position_heights(self, destination, position_no_1, position_no_2):
        """
        (get_sq_distance_between_position_heights, <destination>, <position_no_1>, <position_no_2>),
        Returns squared distance between position *heights* in centimeters.

		Args:
			destination (str|int):
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_sq_distance_between_position_heights(destination, position_no_1, position_no_2)
        """
        return self.append((get_sq_distance_between_position_heights, destination, position_no_1, position_no_2))
        
    def position_normalize_origin(self, destination_fixed_point, position):
        """
        (position_normalize_origin, <destination_fixed_point>, <position>),
        What this operation seems to do is calculate the distance between the zero point [0,0,0] and the point with position's coordinates. Can be used to quickly calculate distance to relative positions.

		Args:
			destination_fixed_point (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_normalize_origin(destination_fixed_point, position)
        """
        return self.append((position_normalize_origin, destination_fixed_point, position))
        
    def position_get_screen_projection(self, position_screen, position_world):
        """
        (position_get_screen_projection, <position_screen>, <position_world>),
        Calculates the screen coordinates of the position and stores it as position_screen's X and Y coordinates.

		Args:
			position_screen (str|int):
			position_world (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> position_get_screen_projection(position_screen, position_world)
        """
        return self.append((position_get_screen_projection, position_screen, position_world))
        
    def map_get_random_position_around_position(self, dest_position_no, source_position_no, radius):
        """
        (map_get_random_position_around_position, <dest_position_no>, <source_position_no>, <radius>),
        Returns a random position on the global map in the vicinity of the source_position.

		Args:
			dest_position_no (str|int):
			source_position_no (str|int):
			radius (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> map_get_random_position_around_position(dest_position_no, source_position_no, radius)
        """
        return self.append((map_get_random_position_around_position, dest_position_no, source_position_no, radius))
        
    def map_get_land_position_around_position(self, dest_position_no, source_position_no, radius):
        """
        (map_get_land_position_around_position, <dest_position_no>, <source_position_no>, <radius>),
        Returns a random position on the global map in the vicinity of the source_position. Will always return a land position (i.e. some place you can walk to).

		Args:
			dest_position_no (str|int):
			source_position_no (str|int):
			radius (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> map_get_land_position_around_position(dest_position_no, source_position_no, radius)
        """
        return self.append((map_get_land_position_around_position, dest_position_no, source_position_no, radius))
        
    def map_get_water_position_around_position(self, dest_position_no, source_position_no, radius):
        """
        (map_get_water_position_around_position, <dest_position_no>, <source_position_no>, <radius>),
        Returns a random position on the global map in the vicinity of the source_position. Will always return a water position (i.e. sea, lake or river).

		Args:
			dest_position_no (str|int):
			source_position_no (str|int):
			radius (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> map_get_water_position_around_position(dest_position_no, source_position_no, radius)
        """
        return self.append((map_get_water_position_around_position, dest_position_no, source_position_no, radius))
        
    def troop_set_note_available(self, troop_id, value):
        """
        (troop_set_note_available, <troop_id>, <value>),
        Enables (value = 1) or disables (value = 0) troop's page in the Notes / Characters section.

		Args:
			troop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> troop_set_note_available(troop_id, value)
        """
        return self.append((troop_set_note_available, troop_id, value))
        
    def add_troop_note_tableau_mesh(self, troop_id, tableau_material_id):
        """
        (add_troop_note_tableau_mesh, <troop_id>, <tableau_material_id>),
        Adds graphical elements to the troop's information page (usually banner and portrait).

		Args:
			troop_id (str|int):
			tableau_material_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_troop_note_tableau_mesh(troop_id, tableau_material_id)
        """
        return self.append((add_troop_note_tableau_mesh, troop_id, tableau_material_id))
        
    def add_troop_note_from_dialog(self, troop_id, note_slot_no, expires_with_time):
        """
        (add_troop_note_from_dialog, <troop_id>, <note_slot_no>, <expires_with_time>),
        Adds current dialog text to troop notes. Each troop has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			troop_id (str|int):
			note_slot_no (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_troop_note_from_dialog(troop_id, note_slot_no, expires_with_time)
        """
        return self.append((add_troop_note_from_dialog, troop_id, note_slot_no, expires_with_time))
        
    def add_troop_note_from_sreg(self, troop_id, note_slot_no, string_id, expires_with_time):
        """
        (add_troop_note_from_sreg, <troop_id>, <note_slot_no>, <string_id>, <expires_with_time>),
        Adds any text stored in string register to troop notes. Each troop has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			troop_id (str|int):
			note_slot_no (str|int):
			string_id (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_troop_note_from_sreg(troop_id, note_slot_no, string_id, expires_with_time)
        """
        return self.append((add_troop_note_from_sreg, troop_id, note_slot_no, string_id, expires_with_time))
        
    def faction_set_note_available(self, faction_id, value):
        """
        (faction_set_note_available, <faction_id>, <value>),
        1 = available, 0 = not available
		Enables (value = 1) or disables (value = 0) faction's page in the Notes / Characters section.

		Args:
			faction_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> faction_set_note_available(faction_id, value)
        """
        return self.append((faction_set_note_available, faction_id, value))
        
    def add_faction_note_tableau_mesh(self, faction_id, tableau_material_id):
        """
        (add_faction_note_tableau_mesh, <faction_id>, <tableau_material_id>),
        Adds graphical elements to the faction's information page (usually graphical collage).

		Args:
			faction_id (str|int):
			tableau_material_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_faction_note_tableau_mesh(faction_id, tableau_material_id)
        """
        return self.append((add_faction_note_tableau_mesh, faction_id, tableau_material_id))
        
    def add_faction_note_from_dialog(self, faction_id, note_slot_no, expires_with_time):
        """
        (add_faction_note_from_dialog, <faction_id>, <note_slot_no>, <expires_with_time>),
        Adds current dialog text to faction notes. Each faction has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			faction_id (str|int):
			note_slot_no (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_faction_note_from_dialog(faction_id, note_slot_no, expires_with_time)
        """
        return self.append((add_faction_note_from_dialog, faction_id, note_slot_no, expires_with_time))
        
    def add_faction_note_from_sreg(self, faction_id, note_slot_no, string_id, expires_with_time):
        """
        (add_faction_note_from_sreg, <faction_id>, <note_slot_no>, <string_id>, <expires_with_time>),
        Adds any text stored in string register to faction notes. Each faction has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			faction_id (str|int):
			note_slot_no (str|int):
			string_id (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_faction_note_from_sreg(faction_id, note_slot_no, string_id, expires_with_time)
        """
        return self.append((add_faction_note_from_sreg, faction_id, note_slot_no, string_id, expires_with_time))
        
    def party_set_note_available(self, party_id, value):
        """
        (party_set_note_available, <party_id>, <value>),
        1 = available, 0 = not available
		Enables (value = 1) or disables (value = 0) party's page in the Notes / Characters section.

		Args:
			party_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> party_set_note_available(party_id, value)
        """
        return self.append((party_set_note_available, party_id, value))
        
    def add_party_note_tableau_mesh(self, party_id, tableau_material_id):
        """
        (add_party_note_tableau_mesh, <party_id>, <tableau_material_id>),
        Adds graphical elements to the party's information page (usually map icon).

		Args:
			party_id (str|int):
			tableau_material_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_party_note_tableau_mesh(party_id, tableau_material_id)
        """
        return self.append((add_party_note_tableau_mesh, party_id, tableau_material_id))
        
    def add_party_note_from_dialog(self, party_id, note_slot_no, expires_with_time):
        """
        (add_party_note_from_dialog, <party_id>, <note_slot_no>, <expires_with_time>),
        Adds current dialog text to party notes. Each party has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			party_id (str|int):
			note_slot_no (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_party_note_from_dialog(party_id, note_slot_no, expires_with_time)
        """
        return self.append((add_party_note_from_dialog, party_id, note_slot_no, expires_with_time))
        
    def add_party_note_from_sreg(self, party_id, note_slot_no, string_id, expires_with_time):
        """
        (add_party_note_from_sreg, <party_id>, <note_slot_no>, <string_id>, <expires_with_time>),
        Adds any text stored in string register to party notes. Each party has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			party_id (str|int):
			note_slot_no (str|int):
			string_id (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_party_note_from_sreg(party_id, note_slot_no, string_id, expires_with_time)
        """
        return self.append((add_party_note_from_sreg, party_id, note_slot_no, string_id, expires_with_time))
        
    def quest_set_note_available(self, quest_id, value):
        """
        (quest_set_note_available, <quest_id>, <value>),
        1 = available, 0 = not available
		Enables (value = 1) or disables (value = 0) quest's page in the Notes / Characters section.

		Args:
			quest_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> quest_set_note_available(quest_id, value)
        """
        return self.append((quest_set_note_available, quest_id, value))
        
    def add_quest_note_tableau_mesh(self, quest_id, tableau_material_id):
        """
        (add_quest_note_tableau_mesh, <quest_id>, <tableau_material_id>),
        Adds graphical elements to the quest's information page (not used in Native).

		Args:
			quest_id (str|int):
			tableau_material_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_quest_note_tableau_mesh(quest_id, tableau_material_id)
        """
        return self.append((add_quest_note_tableau_mesh, quest_id, tableau_material_id))
        
    def add_quest_note_from_dialog(self, quest_id, note_slot_no, expires_with_time):
        """
        (add_quest_note_from_dialog, <quest_id>, <note_slot_no>, <expires_with_time>),
        Adds current dialog text to quest notes. Each quest has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			quest_id (str|int):
			note_slot_no (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_quest_note_from_dialog(quest_id, note_slot_no, expires_with_time)
        """
        return self.append((add_quest_note_from_dialog, quest_id, note_slot_no, expires_with_time))
        
    def add_quest_note_from_sreg(self, quest_id, note_slot_no, string_id, expires_with_time):
        """
        (add_quest_note_from_sreg, <quest_id>, <note_slot_no>, <string_id>, <expires_with_time>),
        Adds any text stored in string register to quest notes. Each quest has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			quest_id (str|int):
			note_slot_no (str|int):
			string_id (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_quest_note_from_sreg(quest_id, note_slot_no, string_id, expires_with_time)
        """
        return self.append((add_quest_note_from_sreg, quest_id, note_slot_no, string_id, expires_with_time))
        
    def add_info_page_note_tableau_mesh(self, info_page_id, tableau_material_id):
        """
        (add_info_page_note_tableau_mesh, <info_page_id>, <tableau_material_id>),
        Adds graphical elements to the info page (not used in Native).

		Args:
			info_page_id (str|int):
			tableau_material_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_info_page_note_tableau_mesh(info_page_id, tableau_material_id)
        """
        return self.append((add_info_page_note_tableau_mesh, info_page_id, tableau_material_id))
        
    def add_info_page_note_from_dialog(self, info_page_id, note_slot_no, expires_with_time):
        """
        (add_info_page_note_from_dialog, <info_page_id>, <note_slot_no>, <expires_with_time>),
        Adds current dialog text to info page notes. Each info page has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			info_page_id (str|int):
			note_slot_no (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_info_page_note_from_dialog(info_page_id, note_slot_no, expires_with_time)
        """
        return self.append((add_info_page_note_from_dialog, info_page_id, note_slot_no, expires_with_time))
        
    def add_info_page_note_from_sreg(self, info_page_id, note_slot_no, string_id, expires_with_time):
        """
        (add_info_page_note_from_sreg, <info_page_id>, <note_slot_no>, <string_id>, <expires_with_time>),
        Adds any text stored in string register to info page notes. Each info page has 16 note slots. Last parameter is used to mark the note as time-dependent, if it's value is 1, then the note will be marked ("Report is current") and will be updated appropriately as the game progresses ("Report is X days old").

		Args:
			info_page_id (str|int):
			note_slot_no (str|int):
			string_id (str|int):
			expires_with_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_info_page_note_from_sreg(info_page_id, note_slot_no, string_id, expires_with_time)
        """
        return self.append((add_info_page_note_from_sreg, info_page_id, note_slot_no, string_id, expires_with_time))
        
    def cur_item_set_tableau_material(self, tableau_material_id, instance_code):
        """
        (cur_item_set_tableau_material, <tableau_material_id>, <instance_code>),
        Can only be used inside ti_on_init_item trigger in module_items.py. Assigns tableau to the item instance. Value of <instance_code> will be passed to tableau code. Commonly used for heraldic armors and shields.

		Args:
			tableau_material_id (str|int):
			instance_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_item_set_tableau_material(tableau_material_id, instance_code)
        """
        return self.append((cur_item_set_tableau_material, tableau_material_id, instance_code))
        
    def cur_scene_prop_set_tableau_material(self, tableau_material_id, instance_code):
        """
        (cur_scene_prop_set_tableau_material, <tableau_material_id>, <instance_code>),
        Can only be used inside ti_on_init_scene_prop trigger in module_scene_props.py. Assigns tableau to the scene prop instance. Value of <instance_code> will be passed to tableau code. Commonly used for static banners.

		Args:
			tableau_material_id (str|int):
			instance_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_scene_prop_set_tableau_material(tableau_material_id, instance_code)
        """
        return self.append((cur_scene_prop_set_tableau_material, tableau_material_id, instance_code))
        
    def cur_map_icon_set_tableau_material(self, tableau_material_id, instance_code):
        """
        (cur_map_icon_set_tableau_material, <tableau_material_id>, <instance_code>),
        Can only be used inside ti_on_init_map_icon trigger in module_map_icons.py. Assigns tableau to the icon prop instance. Value of <instance_code> will be passed to tableau code. Commonly used for player/lord party banners.

		Args:
			tableau_material_id (str|int):
			instance_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_map_icon_set_tableau_material(tableau_material_id, instance_code)
        """
        return self.append((cur_map_icon_set_tableau_material, tableau_material_id, instance_code))
        
    def cur_agent_set_banner_tableau_material(self):
        """
        (cur_agent_set_banner_tableau_material),
        Can only be used inside ti_on_agent_spawn trigger in module_mission_templates. Assigns heraldry .

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_agent_set_banner_tableau_material(tableau_material_id, instance_code)
        """
        return self.append((cur_agent_set_banner_tableau_material))
        
    def cur_tableau_add_tableau_mesh(self, tableau_material_id, value, position_register_no):
        """
        (cur_tableau_add_tableau_mesh, <tableau_material_id>, <value>, <position_register_no>),
        Used in module_tableau_materials.py to add one tableau to another. Value parameter is passed to tableau_material as is.

		Args:
			tableau_material_id (str|int):
			value (str|int):
			position_register_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_tableau_mesh(tableau_material_id, value, position_register_no)
        """
        return self.append((cur_tableau_add_tableau_mesh, tableau_material_id, value, position_register_no))
        
    def cur_tableau_render_as_alpha_mask(self):
        """
        (cur_tableau_render_as_alpha_mask),
        Tells the engine to treat the tableau as an alpha (transparency) mask.

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_render_as_alpha_mask(tableau_material_id, value, position_register_no)
        """
        return self.append((cur_tableau_render_as_alpha_mask))
        
    def cur_tableau_set_background_color(self, value):
        """
        (cur_tableau_set_background_color, <value>),
        Defines solid background color for the current tableau.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_set_background_color(value)
        """
        return self.append((cur_tableau_set_background_color, value))
        
    def cur_tableau_set_ambient_light(self, red_fixed_point, green_fixed_point, blue_fixed_point):
        """
        (cur_tableau_set_ambient_light, <red_fixed_point>, <green_fixed_point>, <blue_fixed_point>),
        Not documented. Used for tableaus rendered from 3D objects to provide uniform tinted lighting.

		Args:
			red_fixed_point (str|int):
			green_fixed_point (str|int):
			blue_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_set_ambient_light(red_fixed_point, green_fixed_point, blue_fixed_point)
        """
        return self.append((cur_tableau_set_ambient_light, red_fixed_point, green_fixed_point, blue_fixed_point))
        
    def cur_tableau_set_camera_position(self, position):
        """
        (cur_tableau_set_camera_position, <position>),
        Not documented. Used for tableaus rendered from 3D objects to position camera as necessary (usually with a perspective camera).

		Args:
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_set_camera_position(position)
        """
        return self.append((cur_tableau_set_camera_position, position))
        
    def cur_tableau_set_camera_parameters(self, is_perspective, camera_width_times_1000, camera_height_times_1000, camera_near_times_1000, camera_far_times_1000):
        """
        (cur_tableau_set_camera_parameters, <is_perspective>, <camera_width_times_1000>, <camera_height_times_1000>, <camera_near_times_1000>, <camera_far_times_1000>),
        Not documented. Used to define camera parameters for tableau rendering. Perspective camera is generally used to render 3D objects for tableaus, while non-perspective camera is used to modify tableau texture meshes.

		Args:
			is_perspective (str|int):
			camera_width_times_1000 (str|int):
			camera_height_times_1000 (str|int):
			camera_near_times_1000 (str|int):
			camera_far_times_1000 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_set_camera_parameters(is_perspective, camera_width_times_1000, camera_height_times_1000, camera_near_times_1000, camera_far_times_1000)
        """
        return self.append((cur_tableau_set_camera_parameters, is_perspective, camera_width_times_1000, camera_height_times_1000, camera_near_times_1000, camera_far_times_1000))
        
    def cur_tableau_add_point_light(self, position, red_fixed_point, green_fixed_point, blue_fixed_point):
        """
        (cur_tableau_add_point_light, <position>, <red_fixed_point>, <green_fixed_point>, <blue_fixed_point>),
        Not documented. Typically used for tableaus rendered from 3D objects to add a point light source.

		Args:
			position (str|int):
			red_fixed_point (str|int):
			green_fixed_point (str|int):
			blue_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_point_light(position, red_fixed_point, green_fixed_point, blue_fixed_point)
        """
        return self.append((cur_tableau_add_point_light, position, red_fixed_point, green_fixed_point, blue_fixed_point))
        
    def cur_tableau_add_sun_light(self, position, red_fixed_point, green_fixed_point, blue_fixed_point):
        """
        (cur_tableau_add_sun_light, <position>, <red_fixed_point>, <green_fixed_point>, <blue_fixed_point>),
        Not documented. Typically used for tableaus rendered from 3D objects to add a directional light source. Note that position coordinates do not matter, only rotation (i.e. light rays direction) does.

		Args:
			position (str|int):
			red_fixed_point (str|int):
			green_fixed_point (str|int):
			blue_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_sun_light(position, red_fixed_point, green_fixed_point, blue_fixed_point)
        """
        return self.append((cur_tableau_add_sun_light, position, red_fixed_point, green_fixed_point, blue_fixed_point))
        
    def cur_tableau_add_mesh(self, value_fixed_point1, value_fixed_point2):
        """
        (cur_tableau_add_mesh, <mesh_id>, <position>, <value_fixed_point>, <value_fixed_point>),
        Adds a static mesh to the tableau with specified offset, scale and alpha. First value fixed point is the scale factor, second value fixed point is alpha. use 0 for default values.

		Args:
			value_fixed_point1 (str|int):
			value_fixed_point2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_mesh(value_fixed_point1, value_fixed_point2)
        """
        return self.append((cur_tableau_add_mesh, value_fixed_point1, value_fixed_point2))
        
    def cur_tableau_add_mesh_with_vertex_color(self, value_fixed_point1, value_fixed_point2):
        """
        (cur_tableau_add_mesh_with_vertex_color, <mesh_id>, <position>, <value_fixed_point>, <value_fixed_point>, <value>),
        Adds a static mesh to the tableau with specified offset, scale, alpha and vertex color. First value fixed point is the scale factor, second value fixed point is alpha. Value is vertex color.

		Args:
			value_fixed_point1 (str|int):
			value_fixed_point2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_mesh_with_vertex_color(value_fixed_point1, value_fixed_point2)
        """
        return self.append((cur_tableau_add_mesh_with_vertex_color, value_fixed_point1, value_fixed_point2))
        
    def cur_tableau_add_mesh_with_scale_and_vertex_color(self, mesh_id, position, scale_position, value_fixed_point, value):
        """
        (cur_tableau_add_mesh_with_scale_and_vertex_color, <mesh_id>, <position>, <scale_position>, <value_fixed_point>, <value>),
        Similar to (cur_tableau_add_mesh_with_vertex_color), but allows non-uniform scaling. Scale factors are stored as (x,y,z) position properties with fixed point values.

		Args:
			mesh_id (str|int):
			position (str|int):
			scale_position (str|int):
			value_fixed_point (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_mesh_with_scale_and_vertex_color(mesh_id, position, scale_position, value_fixed_point, value)
        """
        return self.append((cur_tableau_add_mesh_with_scale_and_vertex_color, mesh_id, position, scale_position, value_fixed_point, value))
        
    def cur_tableau_add_map_icon(self, map_icon_id, position, value_fixed_point):
        """
        (cur_tableau_add_map_icon, <map_icon_id>, <position>, <value_fixed_point>),
        Adds a rendered image of a map icon to current tableau. Last parameter is the scale factor for the model.

		Args:
			map_icon_id (str|int):
			position (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_map_icon(map_icon_id, position, value_fixed_point)
        """
        return self.append((cur_tableau_add_map_icon, map_icon_id, position, value_fixed_point))
        
    def cur_tableau_add_troop(self, troop_id, position, animation_id, instance_no):
        """
        (cur_tableau_add_troop, <troop_id>, <position>, <animation_id>, <instance_no>),
        Adds a rendered image of the troop in a specified animation to current tableau. If instance_no is 0 or less, then the face is not generated randomly (important for heroes).

		Args:
			troop_id (str|int):
			position (str|int):
			animation_id (str|int):
			instance_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_troop(troop_id, position, animation_id, instance_no)
        """
        return self.append((cur_tableau_add_troop, troop_id, position, animation_id, instance_no))
        
    def cur_tableau_add_horse(self, item_id, position, animation_id):
        """
        (cur_tableau_add_horse, <item_id>, <position>, <animation_id>),
        Adds a rendered image of a horse in a specified animation to current tableau.

		Args:
			item_id (str|int):
			position (str|int):
			animation_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_horse(item_id, position, animation_id)
        """
        return self.append((cur_tableau_add_horse, item_id, position, animation_id))
        
    def cur_tableau_set_override_flags(self, value):
        """
        (cur_tableau_set_override_flags, <value>),
        When creating a troop image for current tableau, this operation allows to override troop's inventory partially or completely. See af_* flags in header_mission_templates.py for reference.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_set_override_flags(value)
        """
        return self.append((cur_tableau_set_override_flags, value))
        
    def cur_tableau_clear_override_items(self):
        """
        (cur_tableau_clear_override_items),
        Removes and previously defined equipment overrides for the troop, allowing to start from scratch.

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_clear_override_items(value)
        """
        return self.append((cur_tableau_clear_override_items))
        
    def cur_tableau_add_override_item(self, item_kind_id):
        """
        (cur_tableau_add_override_item, <item_kind_id>),
        When creating a troop image for current tableau, the operation will add a new item to troop's equipment.

		Args:
			item_kind_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cur_tableau_add_override_item(item_kind_id)
        """
        return self.append((cur_tableau_add_override_item, item_kind_id))
        
    def str_is_empty(self, string_register):
        """
        (str_is_empty, <string_register>),
        Checks that referenced string register is empty.

		Args:
			string_register (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_is_empty(string_register)
        """
        return self.append((str_is_empty, string_register))
        
    def str_clear(self):
        """
        (str_clear),
        Clears the contents of the referenced string register.

        Returns:
            TupleBuilder: self

        Example:
            >>> str_clear(string_register)
        """
        return self.append((str_clear))
        
    def str_store_string(self, string_register, string_id):
        """
        (str_store_string, <string_register>, <string_id>),
        Stores a string value in the referenced string register. Only string constants and quick strings can be stored this way.

		Args:
			string_register (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_string(string_register, string_id)
        """
        return self.append((str_store_string, string_register, string_id))
        
    def str_store_string_reg(self, string_register, string_no):
        """
        (str_store_string_reg, <string_register>, <string_no>),
        Copies the contents of one string register from another.

		Args:
			string_register (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_string_reg(string_register, string_no)
        """
        return self.append((str_store_string_reg, string_register, string_no))
        
    def str_store_troop_name(self, string_register, troop_id):
        """
        (str_store_troop_name, <string_register>, <troop_id>),
        Stores singular troop name in referenced string register.

		Args:
			string_register (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_troop_name(string_register, troop_id)
        """
        return self.append((str_store_troop_name, string_register, troop_id))
        
    def str_store_troop_name_plural(self, string_register, troop_id):
        """
        (str_store_troop_name_plural, <string_register>, <troop_id>),
        Stores plural troop name in referenced string register.

		Args:
			string_register (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_troop_name_plural(string_register, troop_id)
        """
        return self.append((str_store_troop_name_plural, string_register, troop_id))
        
    def str_store_troop_name_by_count(self, string_register, troop_id, number):
        """
        (str_store_troop_name_by_count, <string_register>, <troop_id>, <number>),
        Stores singular or plural troop name with number of troops ("29 Archers", "1 Bandit").

		Args:
			string_register (str|int):
			troop_id (str|int):
			number (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_troop_name_by_count(string_register, troop_id, number)
        """
        return self.append((str_store_troop_name_by_count, string_register, troop_id, number))
        
    def str_store_item_name(self, string_register, item_id):
        """
        (str_store_item_name, <string_register>, <item_id>),
        Stores singular item name in referenced string register.

		Args:
			string_register (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_item_name(string_register, item_id)
        """
        return self.append((str_store_item_name, string_register, item_id))
        
    def str_store_item_name_plural(self, string_register, item_id):
        """
        (str_store_item_name_plural, <string_register>, <item_id>),
        Stores plural item name in referenced string register.

		Args:
			string_register (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_item_name_plural(string_register, item_id)
        """
        return self.append((str_store_item_name_plural, string_register, item_id))
        
    def str_store_item_name_by_count(self, string_register, item_id):
        """
        (str_store_item_name_by_count, <string_register>, <item_id>),
        Stores singular or plural item name with number of items ("11 Swords", "1 Bottle of Wine").

		Args:
			string_register (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_item_name_by_count(string_register, item_id)
        """
        return self.append((str_store_item_name_by_count, string_register, item_id))
        
    def str_store_party_name(self, string_register, party_id):
        """
        (str_store_party_name, <string_register>, <party_id>),
        Stores party name in referenced string register.

		Args:
			string_register (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_party_name(string_register, party_id)
        """
        return self.append((str_store_party_name, string_register, party_id))
        
    def str_store_agent_name(self, string_register, agent_id):
        """
        (str_store_agent_name, <string_register>, <agent_id>),
        Stores agent name in referenced string register.

		Args:
			string_register (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_agent_name(string_register, agent_id)
        """
        return self.append((str_store_agent_name, string_register, agent_id))
        
    def str_store_faction_name(self, string_register, faction_id):
        """
        (str_store_faction_name, <string_register>, <faction_id>),
        Stores faction name in referenced string register.

		Args:
			string_register (str|int):
			faction_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_faction_name(string_register, faction_id)
        """
        return self.append((str_store_faction_name, string_register, faction_id))
        
    def str_store_quest_name(self, string_register, quest_id):
        """
        (str_store_quest_name, <string_register>, <quest_id>),
        Stores quest name (as defined in module_quests.py) in referenced string register.

		Args:
			string_register (str|int):
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_quest_name(string_register, quest_id)
        """
        return self.append((str_store_quest_name, string_register, quest_id))
        
    def str_store_info_page_name(self, string_register, info_page_id):
        """
        (str_store_info_page_name, <string_register>, <info_page_id>),
        Stores info page title (as defined in module_info_pages.py) in referenced string register.

		Args:
			string_register (str|int):
			info_page_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_info_page_name(string_register, info_page_id)
        """
        return self.append((str_store_info_page_name, string_register, info_page_id))
        
    def str_store_date(self, string_register, number_of_hours_to_add_to_the_current_date):
        """
        (str_store_date, <string_register>, <number_of_hours_to_add_to_the_current_date>),
        Stores formatted date string, using the number of hours since start of the game (can be retrieved by a call to store_current_hours).

		Args:
			string_register (str|int):
			number_of_hours_to_add_to_the_current_date (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_date(string_register, number_of_hours_to_add_to_the_current_date)
        """
        return self.append((str_store_date, string_register, number_of_hours_to_add_to_the_current_date))
        
    def str_store_troop_name_link(self, string_register, troop_id):
        """
        (str_store_troop_name_link, <string_register>, <troop_id>),
        Stores troop name as an internal game link. Resulting string can be used in game notes, will be highlighted, and clicking on it will redirect the player to the details page of the referenced troop.

		Args:
			string_register (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_troop_name_link(string_register, troop_id)
        """
        return self.append((str_store_troop_name_link, string_register, troop_id))
        
    def str_store_party_name_link(self, string_register, party_id):
        """
        (str_store_party_name_link, <string_register>, <party_id>),
        Stores party name as an internal game link. Resulting string can be used in game notes, will be highlighted, and clicking on it will redirect the player to the details page of the referenced party.

		Args:
			string_register (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_party_name_link(string_register, party_id)
        """
        return self.append((str_store_party_name_link, string_register, party_id))
        
    def str_store_faction_name_link(self, string_register, faction_id):
        """
        (str_store_faction_name_link, <string_register>, <faction_id>),
        Stores faction name as an internal game link. Resulting string can be used in game notes, will be highlighted, and clicking on it will redirect the player to the details page of the referenced faction.

		Args:
			string_register (str|int):
			faction_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_faction_name_link(string_register, faction_id)
        """
        return self.append((str_store_faction_name_link, string_register, faction_id))
        
    def str_store_quest_name_link(self, string_register, quest_id):
        """
        (str_store_quest_name_link, <string_register>, <quest_id>),
        Stores quest name as an internal game link. Resulting string can be used in game notes, will be highlighted, and clicking on it will redirect the player to the details page of the referenced quest.

		Args:
			string_register (str|int):
			quest_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_quest_name_link(string_register, quest_id)
        """
        return self.append((str_store_quest_name_link, string_register, quest_id))
        
    def str_store_info_page_name_link(self, string_register, info_page_id):
        """
        (str_store_info_page_name_link, <string_register>, <info_page_id>),
        Stores info page title as an internal game link. Resulting string can be used in game notes, will be highlighted, and clicking on it will redirect the player to the details page of the referenced info page.

		Args:
			string_register (str|int):
			info_page_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_info_page_name_link(string_register, info_page_id)
        """
        return self.append((str_store_info_page_name_link, string_register, info_page_id))
        
    def str_store_class_name(self, stribg_register, class_id):
        """
        (str_store_class_name, <stribg_register>, <class_id>),
        Stores name of the selected troop class (Infantry, Archers, Cavalry or any of the custom class names) in referenced string register.

		Args:
			stribg_register (str|int):
			class_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_class_name(stribg_register, class_id)
        """
        return self.append((str_store_class_name, stribg_register, class_id))
        
    def game_key_get_mapped_key_name(self, string_register, game_key):
        """
        (game_key_get_mapped_key_name, <string_register>, <game_key>),
        Version 1.161+. Stores human-readable key name that's currently assigned to the provided game key. May store "unknown" and "No key assigned" strings (the latter is defined in languages/en/ui.csv, the former seems to be hardcoded).

		Args:
			string_register (str|int):
			game_key (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> game_key_get_mapped_key_name(string_register, game_key)
        """
        return self.append((game_key_get_mapped_key_name, string_register, game_key))
        
    def str_store_player_username(self, string_register, player_id):
        """
        (str_store_player_username, <string_register>, <player_id>),
        Stores player's multiplayer username in referenced string register. Can be used in multiplayer mode only.

		Args:
			string_register (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_player_username(string_register, player_id)
        """
        return self.append((str_store_player_username, string_register, player_id))
        
    def str_store_server_password(self, string_register):
        """
        (str_store_server_password, <string_register>),
        Stores server's password in referenced string register.

		Args:
			string_register (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_server_password(string_register)
        """
        return self.append((str_store_server_password, string_register))
        
    def str_store_server_name(self, string_register):
        """
        (str_store_server_name, <string_register>),
        Stores server's name (as displayed to clients in server's list window) in referenced string register.

		Args:
			string_register (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_server_name(string_register)
        """
        return self.append((str_store_server_name, string_register))
        
    def str_store_welcome_message(self, string_register):
        """
        (str_store_welcome_message, <string_register>),
        Stores server's welcome message in referenced string register.

		Args:
			string_register (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_store_welcome_message(string_register)
        """
        return self.append((str_store_welcome_message, string_register))
        
    def str_encode_url(self, string_register):
        """
        (str_encode_url, <string_register>),
        This operation will "sanitize" a string to be used as part of network URL, replacing any non-standard characters with their '%'-codes.

		Args:
			string_register (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> str_encode_url(string_register)
        """
        return self.append((str_encode_url, string_register))
        
    def display_debug_message(self, string_id, hex_colour_code):
        """
        (display_debug_message, <string_id>, [hex_colour_code]),
        Displays a string message, but only in debug mode, using provided color (hex-coded 0xRRGGBB). The message is additionally written to rgl_log.txt file in both release and debug modes when edit mode is enabled.

		Args:
			string_id (str|int):
			hex_colour_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> display_debug_message(string_id, hex_colour_code)
        """
        return self.append((display_debug_message, string_id, hex_colour_code))
        
    def display_log_message(self, string_id, hex_colour_code):
        """
        (display_log_message, <string_id>, [hex_colour_code]),
        Display a string message using provided color (hex-coded 0xRRGGBB). The message will also be written to game log (accessible through Notes / Game Log), and will persist between sessions (i.e. it will be stored as part of the savegame).

		Args:
			string_id (str|int):
			hex_colour_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> display_log_message(string_id, hex_colour_code)
        """
        return self.append((display_log_message, string_id, hex_colour_code))
        
    def display_message(self, string_id, hex_colour_code):
        """
        (display_message, <string_id>, [hex_colour_code]),
        Display a string message using provided color (hex-coded 0xRRGGBB).

		Args:
			string_id (str|int):
			hex_colour_code (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> display_message(string_id, hex_colour_code)
        """
        return self.append((display_message, string_id, hex_colour_code))
        
    def set_show_messages(self, value):
        """
        (set_show_messages, <value>),
        Suppresses (value = 0) or enables (value = 1) game messages, including those generated by the game engine.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_show_messages(value)
        """
        return self.append((set_show_messages, value))
        
    def tutorial_box(self, string_id1, string_id2):
        """
        (tutorial_box, <string_id>, <string_id>),
        This operation is deprecated but is still used in Native.

		Args:
			string_id1 (str|int):
			string_id2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> tutorial_box(string_id1, string_id2)
        """
        return self.append((tutorial_box, string_id1, string_id2))
        
    def dialog_box(self, text_string_id, title_string_id):
        """
        (dialog_box, <text_string_id>, [title_string_id]),
        Displays a popup window with the text message and an optional caption.

		Args:
			text_string_id (str|int):
			title_string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> dialog_box(text_string_id, title_string_id)
        """
        return self.append((dialog_box, text_string_id, title_string_id))
        
    def question_box(self, string_id, yes_string_id, no_string_id):
        """
        (question_box, <string_id>, [<yes_string_id>], [<no_string_id>]),
        Displays a popup window with the text of the question and two buttons (Yes and No by default, but can be overridden). When the player selects one of possible responses, a ti_on_question_answered trigger will be executed.

		Args:
			string_id (str|int):
			yes_string_id (str|int):
			no_string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> question_box(string_id, yes_string_id, no_string_id)
        """
        return self.append((question_box, string_id, yes_string_id, no_string_id))
        
    def tutorial_message(self, string_id, color, auto_close_time):
        """
        (tutorial_message, <string_id>, [color], [auto_close_time]),
        Displays a popup window with tutorial text stored in referenced string or string register. Use -1 to close any currently open tutorial box. Optional parameters allow you to define text color and time period after which the tutorial box will close automatically.

		Args:
			string_id (str|int):
			color (str|int):
			auto_close_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> tutorial_message(string_id, color, auto_close_time)
        """
        return self.append((tutorial_message, string_id, color, auto_close_time))
        
    def tutorial_message_set_position(self, position_x, position_y):
        """
        (tutorial_message_set_position, <position_x>, <position_y>),
        Defines screen position for the tutorial box. Assumes screen size is 1000*750.

		Args:
			position_x (str|int):
			position_y (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> tutorial_message_set_position(position_x, position_y)
        """
        return self.append((tutorial_message_set_position, position_x, position_y))
        
    def tutorial_message_set_size(self, size_x, size_y):
        """
        (tutorial_message_set_size, <size_x>, <size_y>),
        Defines size of the tutorial box. Assumes screen size is 1000*750.

		Args:
			size_x (str|int):
			size_y (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> tutorial_message_set_size(size_x, size_y)
        """
        return self.append((tutorial_message_set_size, size_x, size_y))
        
    def tutorial_message_set_center_justify(self, val):
        """
        (tutorial_message_set_center_justify, <val>),
        Sets tutorial box to be center justified (value = 1), or use positioning dictated by tutorial_message_set_position (value = 0).

		Args:
			val (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> tutorial_message_set_center_justify(val)
        """
        return self.append((tutorial_message_set_center_justify, val))
        
    def tutorial_message_set_background(self, value):
        """
        (tutorial_message_set_background, <value>),
        Defines whether the tutorial box will have a background or not (1 or 0). Default is off.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> tutorial_message_set_background(value)
        """
        return self.append((tutorial_message_set_background, value))
        
    def entering_town(self, town_id):
        """
        (entering_town, <town_id>),
        Apparently deprecated.

		Args:
			town_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> entering_town(town_id)
        """
        return self.append((entering_town, town_id))
        
    def encountered_party_is_attacker(self):
        """
        (encountered_party_is_attacker),
        Checks that the party encountered on the world map was following player (i.e. either player was trying to run away or at the very least this is a head-on clash).

        Returns:
            TupleBuilder: self

        Example:
            >>> encountered_party_is_attacker(town_id)
        """
        return self.append((encountered_party_is_attacker))
        
    def conversation_screen_is_active(self):
        """
        (conversation_screen_is_active),
        Checks that the player is currently in dialogue with some agent. Can only be used in triggers of module_mission_templates.py file.

        Returns:
            TupleBuilder: self

        Example:
            >>> conversation_screen_is_active(town_id)
        """
        return self.append((conversation_screen_is_active))
        
    def in_meta_mission(self):
        """
        (in_meta_mission),
        Deprecated, do not use.

        Returns:
            TupleBuilder: self

        Example:
            >>> in_meta_mission(town_id)
        """
        return self.append((in_meta_mission))
        
    def change_screen_return(self):
        """
        (change_screen_return),
        Closes any current screen and returns the player to worldmap (to scene?). 4research how it behaves in missions.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_return(town_id)
        """
        return self.append((change_screen_return))
        
    def change_screen_loot(self, troop_id):
        """
        (change_screen_loot, <troop_id>),
        Opens the Looting interface, using the provided troop as loot storage. Player has full access to troop inventory.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_loot(troop_id)
        """
        return self.append((change_screen_loot, troop_id))
        
    def change_screen_trade(self, troop_id):
        """
        (change_screen_trade, [troop_id]),
        Opens the Trade screen, using the provided troop as the trading partner. When called from module_dialogs, troop_id is optional and defaults to current dialogue partner.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_trade(troop_id)
        """
        return self.append((change_screen_trade, troop_id))
        
    def change_screen_exchange_members(self, exchange_leader, party_id):
        """
        (change_screen_exchange_members, [exchange_leader], [party_id]),
        Opens the Exchange Members With Party interface, using the specified party_id. If called during an encounter, party_id is optional and defaults to the encountered party. Second parameter determines whether the party leader is exchangeable (useful when managing the castle garrison).

		Args:
			exchange_leader (str|int):
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_exchange_members(exchange_leader, party_id)
        """
        return self.append((change_screen_exchange_members, exchange_leader, party_id))
        
    def change_screen_trade_prisoners(self):
        """
        (change_screen_trade_prisoners),
        Opens the Sell Prisoners interface. Script "script_game_get_prisoner_price" will be used to determine prisoner price.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_trade_prisoners(exchange_leader, party_id)
        """
        return self.append((change_screen_trade_prisoners))
        
    def change_screen_buy_mercenaries(self):
        """
        (change_screen_buy_mercenaries),
        Opens the Buy Mercenaries interface, where player can hire troops from the party specified with (set_mercenary_source_party) operation. Only works from the dialog.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_buy_mercenaries(exchange_leader, party_id)
        """
        return self.append((change_screen_buy_mercenaries))
        
    def change_screen_view_character(self):
        """
        (change_screen_view_character),
        Opens the character screen of another troop. Can only be used in dialogs.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_view_character(exchange_leader, party_id)
        """
        return self.append((change_screen_view_character))
        
    def change_screen_training(self):
        """
        (change_screen_training),
        Opens the character screen for the troop that player is currently talking to. Only works in dialogs. Deprecated, use (change_screen_view_character) instead.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_training(exchange_leader, party_id)
        """
        return self.append((change_screen_training))
        
    def change_screen_mission(self):
        """
        (change_screen_mission),
        Starts the mission, using previously defined scene and mission template.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_mission(exchange_leader, party_id)
        """
        return self.append((change_screen_mission))
        
    def change_screen_map_conversation(self, troop_id):
        """
        (change_screen_map_conversation, <troop_id>),
        Starts the mission, same as (change_screen_mission). However once the mission starts, player will get into dialog with the specified troop, and once the dialog ends, the mission will automatically end.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_map_conversation(troop_id)
        """
        return self.append((change_screen_map_conversation, troop_id))
        
    def change_screen_exchange_with_party(self, party_id):
        """
        (change_screen_exchange_with_party, <party_id>),
        Effectively duplicates (change_screen_exchange_members), but party_id parameter is obligatory and the operation doesn't have an option to prevent party leader from being exchanged.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_exchange_with_party(party_id)
        """
        return self.append((change_screen_exchange_with_party, party_id))
        
    def change_screen_equip_other(self, troop_id):
        """
        (change_screen_equip_other, [troop_id]),
        Opens the Equip Companion interface. When calling from a dialog, it is not necessary to specify troop_id.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_equip_other(troop_id)
        """
        return self.append((change_screen_equip_other, troop_id))
        
    def change_screen_map(self):
        """
        (change_screen_map),
        Changes the screen to global map, closing any currently running game menu, dialog or mission.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_map(troop_id)
        """
        return self.append((change_screen_map))
        
    def change_screen_notes(self, note_type, object_id):
        """
        (change_screen_notes, <note_type>, <object_id>),
        Opens the Notes screen, in the selected category (note_type: 1=troops, 2=factions, 3=parties, 4=quests, 5=info_pages) and for the specified object in that category.

		Args:
			note_type (str|int):
			object_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_notes(note_type, object_id)
        """
        return self.append((change_screen_notes, note_type, object_id))
        
    def change_screen_quit(self):
        """
        (change_screen_quit),
        Quits the game to the main menu.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_quit(note_type, object_id)
        """
        return self.append((change_screen_quit))
        
    def change_screen_give_members(self, party_id):
        """
        (change_screen_give_members, [party_id]),
        Opens the Give Troops to Another Party interface. Party_id parameter is optional during an encounter and will use encountered party as default value.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_give_members(party_id)
        """
        return self.append((change_screen_give_members, party_id))
        
    def change_screen_controls(self):
        """
        (change_screen_controls),
        Opens the standard Configure Controls screen, pausing the game.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_controls(party_id)
        """
        return self.append((change_screen_controls))
        
    def change_screen_options(self):
        """
        (change_screen_options),
        Opens the standard Game Options screen, pausing the game.

        Returns:
            TupleBuilder: self

        Example:
            >>> change_screen_options(party_id)
        """
        return self.append((change_screen_options))
        
    def set_mercenary_source_party(self, party_id):
        """
        (set_mercenary_source_party, <party_id>),
        Defines the party from which the player will buy mercenaries with (change_screen_buy_mercenaries).

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_mercenary_source_party(party_id)
        """
        return self.append((set_mercenary_source_party, party_id))
        
    def start_map_conversation(self, troop_id, troop_dna):
        """
        (start_map_conversation, <troop_id>, [troop_dna]),
        Starts a conversation with the selected troop. Can be called directly from global map or game menus. Troop DNA parameter allows you to randomize non-hero troop appearances.

		Args:
			troop_id (str|int):
			troop_dna (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_map_conversation(troop_id, troop_dna)
        """
        return self.append((start_map_conversation, troop_id, troop_dna))
        
    def set_background_mesh(self, mesh_id):
        """
        (set_background_mesh, <mesh_id>),
        Sets the specified mesh as the background for the current menu. Possibly can be used for dialogs or presentations, but was not tested.

		Args:
			mesh_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_background_mesh(mesh_id)
        """
        return self.append((set_background_mesh, mesh_id))
        
    def set_game_menu_tableau_mesh(self, tableau_material_id, value, position_register_no):
        """
        (set_game_menu_tableau_mesh, <tableau_material_id>, <value>, <position_register_no>),
        Adds a tableau to the current game menu screen. Position (X,Y) coordinates define mesh position, Z coordinate defines scaling. Parameter <value> will be passed as tableau_material script parameter.

		Args:
			tableau_material_id (str|int):
			value (str|int):
			position_register_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_game_menu_tableau_mesh(tableau_material_id, value, position_register_no)
        """
        return self.append((set_game_menu_tableau_mesh, tableau_material_id, value, position_register_no))
        
    def jump_to_menu(self, menu_id):
        """
        (jump_to_menu, <menu_id>),
        Opens the specified game menu. Note this only happens after the current block of code completes execution.

		Args:
			menu_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> jump_to_menu(menu_id)
        """
        return self.append((jump_to_menu, menu_id))
        
    def disable_menu_option(self):
        """
        (disable_menu_option),
        Never used in native. Apparently deprecated as menu options have prerequisite code blocks now.

        Returns:
            TupleBuilder: self

        Example:
            >>> disable_menu_option(menu_id)
        """
        return self.append((disable_menu_option))
        
    def set_party_battle_mode(self):
        """
        (set_party_battle_mode),
        Used before or during the mission to start battle mode (and apparently make agents use appropriate AI).

        Returns:
            TupleBuilder: self

        Example:
            >>> set_party_battle_mode(menu_id)
        """
        return self.append((set_party_battle_mode))
        
    def finish_party_battle_mode(self):
        """
        (finish_party_battle_mode),
        Used during the mission to stop battle mode.

        Returns:
            TupleBuilder: self

        Example:
            >>> finish_party_battle_mode(menu_id)
        """
        return self.append((finish_party_battle_mode))
        
    def start_encounter(self, party_id):
        """
        (start_encounter, <party_id>),
        Forces the player party to initiate encounter with the specified party. Distance does not matter in this situation.

		Args:
			party_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_encounter(party_id)
        """
        return self.append((start_encounter, party_id))
        
    def leave_encounter(self):
        """
        (leave_encounter),
        Leaves encounter mode.

        Returns:
            TupleBuilder: self

        Example:
            >>> leave_encounter(party_id)
        """
        return self.append((leave_encounter))
        
    def encounter_attack(self):
        """
        (encounter_attack),
        Apparently starts the standard battle with the encountered party. 4research.

        Returns:
            TupleBuilder: self

        Example:
            >>> encounter_attack(party_id)
        """
        return self.append((encounter_attack))
        
    def select_enemy(self, value):
        """
        (select_enemy, <value>),
        When joining a battle, this determines what side player will be helping. Defending party is always 0, and attacking party is always 1. Player can support either attackers (value = 0, i.e. defenders are the enemy) or defenders (value = 1).

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> select_enemy(value)
        """
        return self.append((select_enemy, value))
        
    def set_passage_menu(self, value):
        """
        (set_passage_menu, <value>),
        When setting up a mission, this allows you to determine what game menu will be used for that mission passages instead of "mnu_town". Passage menu item number will determine what menu option (in sequential order, starting from 0) will be executed when the player activates that passage on the scene. Note that menu option condition code block will be ignored.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_passage_menu(value)
        """
        return self.append((set_passage_menu, value))
        
    def start_mission_conversation(self, troop_id):
        """
        (start_mission_conversation, <troop_id>),
        During the mission, initiates the dialog with specified troop.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_mission_conversation(troop_id)
        """
        return self.append((start_mission_conversation, troop_id))
        
    def set_conversation_speaker_troop(self, troop_id):
        """
        (set_conversation_speaker_troop, <troop_id>),
        Allows to dynamically switch speaking troops during the dialog when developer doesn't know in advance who will be doing the speaking. Should be placed in post-talk code section of dialog entry.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_conversation_speaker_troop(troop_id)
        """
        return self.append((set_conversation_speaker_troop, troop_id))
        
    def set_conversation_speaker_agent(self, agent_id):
        """
        (set_conversation_speaker_agent, <agent_id>),
        Allows to dynamically switch speaking agents during the dialog when developer doesn't know in advance who will be doing the speaking. Should be placed in post-talk code section of dialog entry.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_conversation_speaker_agent(agent_id)
        """
        return self.append((set_conversation_speaker_agent, agent_id))
        
    def store_conversation_agent(self, destination):
        """
        (store_conversation_agent, <destination>),
        Stores identifier of agent who is currently speaking.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_conversation_agent(destination)
        """
        return self.append((store_conversation_agent, destination))
        
    def store_conversation_troop(self, destination):
        """
        (store_conversation_troop, <destination>),
        Stores identifier of troop who is currently speaking.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_conversation_troop(destination)
        """
        return self.append((store_conversation_troop, destination))
        
    def store_partner_faction(self, destination):
        """
        (store_partner_faction, <destination>),
        Stores faction of the troop player is speaking to.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_partner_faction(destination)
        """
        return self.append((store_partner_faction, destination))
        
    def store_encountered_party(self, destination):
        """
        (store_encountered_party, <destination>),
        Stores identifier of the encountered party.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_encountered_party(destination)
        """
        return self.append((store_encountered_party, destination))
        
    def store_encountered_party2(self, destination):
        """
        (store_encountered_party2, <destination>),
        Stores the identifier of the second encountered party (when first party is in battle, this one will return it's battle opponent).

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_encountered_party2(destination)
        """
        return self.append((store_encountered_party2, destination))
        
    def set_encountered_party(self, party_no):
        """
        (set_encountered_party, <party_no>),
        Sets the specified party as encountered by player, but does not run the entire encounter routine. Used in Native during chargen to set up the starting town and then immediately throw the player into street fight without showing him the town menu.

		Args:
			party_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_encountered_party(party_no)
        """
        return self.append((set_encountered_party, party_no))
        
    def end_current_battle(self):
        """
        (end_current_battle),
        Apparently ends the battle between player's party and it's opponent. Exact effects not clear. 4research.

        Returns:
            TupleBuilder: self

        Example:
            >>> end_current_battle(party_no)
        """
        return self.append((end_current_battle))
        
    def store_repeat_object(self, destination):
        """
        (store_repeat_object, <destination>),
        Used in the dialogs code in combination with repeat_for_* dialog parameters, when creating dynamical player responses. Stores the value for the current iteration (i.e. a faction ID when repeat_for_factions is used, etc).

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_repeat_object(destination)
        """
        return self.append((store_repeat_object, destination))
        
    def talk_info_show(self, hide_or_show):
        """
        (talk_info_show, <hide_or_show>),
        Used in the dialogs code to display relations bar on opponent's portrait when mouse is hovering over it (value = 1) or disable this functionality (value = 0)

		Args:
			hide_or_show (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> talk_info_show(hide_or_show)
        """
        return self.append((talk_info_show, hide_or_show))
        
    def talk_info_set_relation_bar(self, value):
        """
        (talk_info_set_relation_bar, <value>),
        Sets the relations value for relationship bar in the dialog. Value should be in range -100..100.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> talk_info_set_relation_bar(value)
        """
        return self.append((talk_info_set_relation_bar, value))
        
    def talk_info_set_line(self, line_no, string_no):
        """
        (talk_info_set_line, <line_no>, <string_no>),
        Sets the additional text information (usually troop name) to be displayed together with the relations bar.

		Args:
			line_no (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> talk_info_set_line(line_no, string_no)
        """
        return self.append((talk_info_set_line, line_no, string_no))
        
    def all_enemies_defeated(self, team_id):
        """
        (all_enemies_defeated, [team_id]),
        Checks if all agents from the specified team are defeated. When team_id is omitted default enemy team is checked.

		Args:
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> all_enemies_defeated(team_id)
        """
        return self.append((all_enemies_defeated, team_id))
        
    def race_completed_by_player(self):
        """
        (race_completed_by_player),
        Not documented. Not used in Native. Apparently deprecated.

        Returns:
            TupleBuilder: self

        Example:
            >>> race_completed_by_player(team_id)
        """
        return self.append((race_completed_by_player))
        
    def num_active_teams_le(self, value):
        """
        (num_active_teams_le, <value>),
        Checks that the number of active teams (i.e. teams with at least one active agent) is less than or equal to given value.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> num_active_teams_le(value)
        """
        return self.append((num_active_teams_le, value))
        
    def main_hero_fallen(self):
        """
        (main_hero_fallen),
        Checks that the player has been knocked out.

        Returns:
            TupleBuilder: self

        Example:
            >>> main_hero_fallen(value)
        """
        return self.append((main_hero_fallen))
        
    def scene_allows_mounted_units(self):
        """
        (scene_allows_mounted_units),
        Not documented. Used in multiplayer, but it's not clear where horses could be disallowed in the first place. 4research.

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_allows_mounted_units(value)
        """
        return self.append((scene_allows_mounted_units))
        
    def is_zoom_disabled(self):
        """
        (is_zoom_disabled),
        Version 1.153+. Checks that the zoom is currently disabled in the game.

        Returns:
            TupleBuilder: self

        Example:
            >>> is_zoom_disabled(value)
        """
        return self.append((is_zoom_disabled))
        
    def scene_set_slot(self, scene_id, slot_no, value):
        """
        (scene_set_slot, <scene_id>, <slot_no>, <value>),
        

		Args:
			scene_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_set_slot(scene_id, slot_no, value)
        """
        return self.append((scene_set_slot, scene_id, slot_no, value))
        
    def scene_get_slot(self, destination, scene_id, slot_no):
        """
        (scene_get_slot, <destination>, <scene_id>, <slot_no>),
        

		Args:
			destination (str|int):
			scene_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_get_slot(destination, scene_id, slot_no)
        """
        return self.append((scene_get_slot, destination, scene_id, slot_no))
        
    def scene_slot_eq(self, scene_id, slot_no, value):
        """
        (scene_slot_eq, <scene_id>, <slot_no>, <value>),
        

		Args:
			scene_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_slot_eq(scene_id, slot_no, value)
        """
        return self.append((scene_slot_eq, scene_id, slot_no, value))
        
    def scene_slot_ge(self, scene_id, slot_no, value):
        """
        (scene_slot_ge, <scene_id>, <slot_no>, <value>),
        

		Args:
			scene_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_slot_ge(scene_id, slot_no, value)
        """
        return self.append((scene_slot_ge, scene_id, slot_no, value))
        
    def add_troop_to_site(self, troop_id, scene_id, entry_no):
        """
        (add_troop_to_site, <troop_id>, <scene_id>, <entry_no>),
        Set troop's position in the world to the specified scene and entry point. Entry point must have mtef_scene_source type. Agent will always appear at that entry when entering that scene. No longer used in Native.

		Args:
			troop_id (str|int):
			scene_id (str|int):
			entry_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_troop_to_site(troop_id, scene_id, entry_no)
        """
        return self.append((add_troop_to_site, troop_id, scene_id, entry_no))
        
    def remove_troop_from_site(self, troop_id, scene_id):
        """
        (remove_troop_from_site, <troop_id>, <scene_id>),
        Removes the troop from the specified scene. No longer used in Native.

		Args:
			troop_id (str|int):
			scene_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_troop_from_site(troop_id, scene_id)
        """
        return self.append((remove_troop_from_site, troop_id, scene_id))
        
    def modify_visitors_at_site(self, scene_id):
        """
        (modify_visitors_at_site, <scene_id>),
        Declares the scene which visitors will be modified from that moment on.

		Args:
			scene_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> modify_visitors_at_site(scene_id)
        """
        return self.append((modify_visitors_at_site, scene_id))
        
    def reset_visitors(self):
        """
        (reset_visitors),
        Resets all visitors to the scene.

        Returns:
            TupleBuilder: self

        Example:
            >>> reset_visitors(scene_id)
        """
        return self.append((reset_visitors))
        
    def set_visitor(self, entry_no, troop_id, dna):
        """
        (set_visitor, <entry_no>, <troop_id>, [<dna>]),
        Adds the specified troop as the visitor to the entry point of the scene defined with (modify_visitors_at_site). Entry point must have mtef_visitor_source type. Optional DNA parameter allows for randomization of agent looks (only applies to non-hero troops).

		Args:
			entry_no (str|int):
			troop_id (str|int):
			dna (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_visitor(entry_no, troop_id, dna)
        """
        return self.append((set_visitor, entry_no, troop_id, dna))
        
    def set_visitors(self, entry_no, troop_id, number_of_troops):
        """
        (set_visitors, <entry_no>, <troop_id>, <number_of_troops>),
        Save as (set_visitors), but spawns an entire group of some troop type.

		Args:
			entry_no (str|int):
			troop_id (str|int):
			number_of_troops (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_visitors(entry_no, troop_id, number_of_troops)
        """
        return self.append((set_visitors, entry_no, troop_id, number_of_troops))
        
    def add_visitors_to_current_scene(self, entry_no, troop_id, number_of_troops, team_no, group_no):
        """
        (add_visitors_to_current_scene, <entry_no>, <troop_id>, <number_of_troops>, <team_no>, <group_no>),
        Adds a number of troops to the specified entry point when the scene is already loaded. Team and group parameters are used in multiplayer mode only, singleplayer mode uses team settings for selected entry point as defined in module_mission_templates.py.

		Args:
			entry_no (str|int):
			troop_id (str|int):
			number_of_troops (str|int):
			team_no (str|int):
			group_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_visitors_to_current_scene(entry_no, troop_id, number_of_troops, team_no, group_no)
        """
        return self.append((add_visitors_to_current_scene, entry_no, troop_id, number_of_troops, team_no, group_no))
        
    def mission_tpl_entry_set_override_flags(self, mission_template_id, entry_no, value):
        """
        (mission_tpl_entry_set_override_flags, <mission_template_id>, <entry_no>, <value>),
        Allows modder to use a different set of equipment override flags (see af_* constants in header_mission_templates.py) for the selected entry point.

		Args:
			mission_template_id (str|int):
			entry_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_tpl_entry_set_override_flags(mission_template_id, entry_no, value)
        """
        return self.append((mission_tpl_entry_set_override_flags, mission_template_id, entry_no, value))
        
    def mission_tpl_entry_clear_override_items(self, mission_template_id, entry_no):
        """
        (mission_tpl_entry_clear_override_items, <mission_template_id>, <entry_no>),
        Clears the list of override equipment provided by the entry point definition in module_mission_templates.py.

		Args:
			mission_template_id (str|int):
			entry_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_tpl_entry_clear_override_items(mission_template_id, entry_no)
        """
        return self.append((mission_tpl_entry_clear_override_items, mission_template_id, entry_no))
        
    def mission_tpl_entry_add_override_item(self, mission_template_id, entry_no, item_kind_id):
        """
        (mission_tpl_entry_add_override_item, <mission_template_id>, <entry_no>, <item_kind_id>),
        Specified item will be added to any agent spawning on specified entry point.

		Args:
			mission_template_id (str|int):
			entry_no (str|int):
			item_kind_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_tpl_entry_add_override_item(mission_template_id, entry_no, item_kind_id)
        """
        return self.append((mission_tpl_entry_add_override_item, mission_template_id, entry_no, item_kind_id))
        
    def set_mission_result(self, value):
        """
        (set_mission_result, <value>),
        Sets the result of the current mission (1 for victory, -1 for defeat).

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_mission_result(value)
        """
        return self.append((set_mission_result, value))
        
    def finish_mission(self, delay_in_seconds):
        """
        (finish_mission, <delay_in_seconds>),
        Exits the scene after the specified delay.

		Args:
			delay_in_seconds (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> finish_mission(delay_in_seconds)
        """
        return self.append((finish_mission, delay_in_seconds))
        
    def set_jump_mission(self, mission_template_id):
        """
        (set_jump_mission, <mission_template_id>),
        Tells the game to use the specified mission template for the next mission. Apparently should precede the call to (jump_to_scene).

		Args:
			mission_template_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_jump_mission(mission_template_id)
        """
        return self.append((set_jump_mission, mission_template_id))
        
    def jump_to_scene(self, scene_id, entry_no):
        """
        (jump_to_scene, <scene_id>, [entry_no]),
        Tells the game to use the specified scene for the next mission. Usually followed by (change_screen_mission) call. Parameter entry_no does not seem to have any effect.

		Args:
			scene_id (str|int):
			entry_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> jump_to_scene(scene_id, entry_no)
        """
        return self.append((jump_to_scene, scene_id, entry_no))
        
    def set_jump_entry(self, entry_no):
        """
        (set_jump_entry, <entry_no>),
        Defines what entry point the player will appear at when the mission starts.

		Args:
			entry_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_jump_entry(entry_no)
        """
        return self.append((set_jump_entry, entry_no))
        
    def store_current_scene(self, destination):
        """
        (store_current_scene, <destination>),
        Retrieves the identifier of the current scene. Note that the operation will return the scene id even after the mission is completed and the player is already on global map.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_current_scene(destination)
        """
        return self.append((store_current_scene, destination))
        
    def close_order_menu(self):
        """
        (close_order_menu),
        Version 1.161+. If orders menu is currently open, it will be closed.

        Returns:
            TupleBuilder: self

        Example:
            >>> close_order_menu(destination)
        """
        return self.append((close_order_menu))
        
    def entry_point_get_position(self, position, entry_no):
        """
        (entry_point_get_position, <position>, <entry_no>),
        Retrieves the position of the entry point on the scene.

		Args:
			position (str|int):
			entry_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> entry_point_get_position(position, entry_no)
        """
        return self.append((entry_point_get_position, position, entry_no))
        
    def entry_point_set_position(self, entry_no, position):
        """
        (entry_point_set_position, <entry_no>, <position>),
        Moves the entry point to the specified position on the scene.

		Args:
			entry_no (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> entry_point_set_position(entry_no, position)
        """
        return self.append((entry_point_set_position, entry_no, position))
        
    def entry_point_is_auto_generated(self, entry_no):
        """
        (entry_point_is_auto_generated, <entry_no>),
        Checks that the entry point is auto-generated (in other words, there was no such entry point placed in the scene file).

		Args:
			entry_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> entry_point_is_auto_generated(entry_no)
        """
        return self.append((entry_point_is_auto_generated, entry_no))
        
    def scene_set_day_time(self, value):
        """
        (scene_set_day_time, <value>),
        Defines the time for the scene to force the engine to select a different skybox than the one dictated by current game time. Must be called within ti_before_mission_start trigger in module_mission_templates.py. Value should be in range 0..23.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_set_day_time(value)
        """
        return self.append((scene_set_day_time, value))
        
    def set_rain(self, rain_type, strength):
        """
        (set_rain, <rain_type>, <strength>),
        Sets a new weather for the mission. Rain_type values: 0 = clear, 1 = rain, 2 = snow. Strength is in range 0..100.

		Args:
			rain_type (str|int):
			strength (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_rain(rain_type, strength)
        """
        return self.append((set_rain, rain_type, strength))
        
    def set_fog_distance(self, distance_in_meters, fog_color):
        """
        (set_fog_distance, <distance_in_meters>, [fog_color]),
        Sets the density (and optionally color) of the fog for the mission.

		Args:
			distance_in_meters (str|int):
			fog_color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_fog_distance(distance_in_meters, fog_color)
        """
        return self.append((set_fog_distance, distance_in_meters, fog_color))
        
    def set_skybox(self, non_hdr_skybox_index, hdr_skybox_index):
        """
        (set_skybox, <non_hdr_skybox_index>, <hdr_skybox_index>),
        Version 1.153+. Forces the scene to be rendered with specified skybox. Index of -1 will disable.

		Args:
			non_hdr_skybox_index (str|int):
			hdr_skybox_index (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_skybox(non_hdr_skybox_index, hdr_skybox_index)
        """
        return self.append((set_skybox, non_hdr_skybox_index, hdr_skybox_index))
        
    def set_startup_sun_light(self, r, g, b):
        """
        (set_startup_sun_light, <r>, <g>, <b>),
        Version 1.153+. Defines the sunlight color for the scene.

		Args:
			r (str|int):
			g (str|int):
			b (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_startup_sun_light(r, g, b)
        """
        return self.append((set_startup_sun_light, r, g, b))
        
    def set_startup_ambient_light(self, r, g, b):
        """
        (set_startup_ambient_light, <r>, <g>, <b>),
        Version 1.153+. Defines the ambient light color for the scene.

		Args:
			r (str|int):
			g (str|int):
			b (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_startup_ambient_light(r, g, b)
        """
        return self.append((set_startup_ambient_light, r, g, b))
        
    def set_startup_ground_ambient_light(self, r, g, b):
        """
        (set_startup_ground_ambient_light, <r>, <g>, <b>),
        Version 1.153+. Defines the ambient light color for the ground.

		Args:
			r (str|int):
			g (str|int):
			b (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_startup_ground_ambient_light(r, g, b)
        """
        return self.append((set_startup_ground_ambient_light, r, g, b))
        
    def get_startup_sun_light(self, position_no):
        """
        (get_startup_sun_light, <position_no>),
        Version 1.165+. Returns startup sunlight color in (x, y, z) coordinates of position register.

		Args:
			position_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_startup_sun_light(position_no)
        """
        return self.append((get_startup_sun_light, position_no))
        
    def get_startup_ambient_light(self, position_no):
        """
        (get_startup_ambient_light, <position_no>),
        Version 1.165+. Returns startup ambient light color in (x, y, z) coordinates of position register.

		Args:
			position_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_startup_ambient_light(position_no)
        """
        return self.append((get_startup_ambient_light, position_no))
        
    def get_startup_ground_ambient_light(self, position_no):
        """
        (get_startup_ground_ambient_light, <position_no>),
        Version 1.165+. Returns startup ambient ground lighting color in (x, y, z) coordinates of position register.

		Args:
			position_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_startup_ground_ambient_light(position_no)
        """
        return self.append((get_startup_ground_ambient_light, position_no))
        
    def get_battle_advantage(self, destination):
        """
        (get_battle_advantage, <destination>),
        Retrieves the calculated battle advantage.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_battle_advantage(destination)
        """
        return self.append((get_battle_advantage, destination))
        
    def set_battle_advantage(self, value):
        """
        (set_battle_advantage, <value>),
        Sets a new value for battle advantage.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_battle_advantage(value)
        """
        return self.append((set_battle_advantage, value))
        
    def get_scene_boundaries(self, position_min, position_max):
        """
        (get_scene_boundaries, <position_min>, <position_max>),
        Retrieves the coordinates of the top-left and bottom-right corner of the scene to the provided position registers.

		Args:
			position_min (str|int):
			position_max (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_scene_boundaries(position_min, position_max)
        """
        return self.append((get_scene_boundaries, position_min, position_max))
        
    def mission_enable_talk(self):
        """
        (mission_enable_talk),
        Allows dialogue with agents on the scene.

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_enable_talk(position_min, position_max)
        """
        return self.append((mission_enable_talk))
        
    def mission_disable_talk(self):
        """
        (mission_disable_talk),
        Disables dialogue with agents on the scene.

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_disable_talk(position_min, position_max)
        """
        return self.append((mission_disable_talk))
        
    def mission_get_time_speed(self, destination_fixed_point):
        """
        (mission_get_time_speed, <destination_fixed_point>),
        Retrieves current time speed factor for the mission.

		Args:
			destination_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_get_time_speed(destination_fixed_point)
        """
        return self.append((mission_get_time_speed, destination_fixed_point))
        
    def mission_set_time_speed(self, value_fixed_point):
        """
        (mission_set_time_speed, <value_fixed_point>),
        Instantly changes the speed of time during the mission. Speed of time cannot be set to zero or below. Operation only works when cheat mode is enabled.

		Args:
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_set_time_speed(value_fixed_point)
        """
        return self.append((mission_set_time_speed, value_fixed_point))
        
    def mission_time_speed_move_to_value(self, value_fixed_point, duration_in_one_per_thousand_sec):
        """
        (mission_time_speed_move_to_value, <value_fixed_point>, <duration_in_one_per_thousand_sec>),
        Changes the speed of time during the mission gradually, within the specified duration period. Speed of time cannot be set to zero or below. Operation only works when cheat mode is enabled.

		Args:
			value_fixed_point (str|int):
			duration_in_one_per_thousand_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_time_speed_move_to_value(value_fixed_point, duration_in_one_per_thousand_sec)
        """
        return self.append((mission_time_speed_move_to_value, value_fixed_point, duration_in_one_per_thousand_sec))
        
    def mission_set_duel_mode(self, value):
        """
        (mission_set_duel_mode, <value>),
        Sets duel mode for the multiplayer mission. Values: 0 = off, 1 = on.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_set_duel_mode(value)
        """
        return self.append((mission_set_duel_mode, value))
        
    def store_zoom_amount(self, destination_fixed_point):
        """
        (store_zoom_amount, <destination_fixed_point>),
        Version 1.153+. Stores current zoom rate.

		Args:
			destination_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_zoom_amount(destination_fixed_point)
        """
        return self.append((store_zoom_amount, destination_fixed_point))
        
    def set_zoom_amount(self, value_fixed_point):
        """
        (set_zoom_amount, <value_fixed_point>),
        Version 1.153+. Sets new zoom rate.

		Args:
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_zoom_amount(value_fixed_point)
        """
        return self.append((set_zoom_amount, value_fixed_point))
        
    def reset_mission_timer_a(self):
        """
        (reset_mission_timer_a),
        Resets the value of first mission timer and starts it from zero.

        Returns:
            TupleBuilder: self

        Example:
            >>> reset_mission_timer_a(value_fixed_point)
        """
        return self.append((reset_mission_timer_a))
        
    def reset_mission_timer_b(self):
        """
        (reset_mission_timer_b),
        Resets the value of second mission timer and starts it from zero.

        Returns:
            TupleBuilder: self

        Example:
            >>> reset_mission_timer_b(value_fixed_point)
        """
        return self.append((reset_mission_timer_b))
        
    def reset_mission_timer_c(self):
        """
        (reset_mission_timer_c),
        Resets the value of third mission timer and starts it from zero.

        Returns:
            TupleBuilder: self

        Example:
            >>> reset_mission_timer_c(value_fixed_point)
        """
        return self.append((reset_mission_timer_c))
        
    def store_mission_timer_a(self, destination):
        """
        (store_mission_timer_a, <destination>),
        Retrieves current value of first mission timer, in seconds.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mission_timer_a(destination)
        """
        return self.append((store_mission_timer_a, destination))
        
    def store_mission_timer_b(self, destination):
        """
        (store_mission_timer_b, <destination>),
        Retrieves current value of second mission timer, in seconds.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mission_timer_b(destination)
        """
        return self.append((store_mission_timer_b, destination))
        
    def store_mission_timer_c(self, destination):
        """
        (store_mission_timer_c, <destination>),
        Retrieves current value of third mission timer, in seconds.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mission_timer_c(destination)
        """
        return self.append((store_mission_timer_c, destination))
        
    def store_mission_timer_a_msec(self, destination):
        """
        (store_mission_timer_a_msec, <destination>),
        Retrieves current value of first mission timer, in milliseconds.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mission_timer_a_msec(destination)
        """
        return self.append((store_mission_timer_a_msec, destination))
        
    def store_mission_timer_b_msec(self, destination):
        """
        (store_mission_timer_b_msec, <destination>),
        Retrieves current value of second mission timer, in milliseconds.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mission_timer_b_msec(destination)
        """
        return self.append((store_mission_timer_b_msec, destination))
        
    def store_mission_timer_c_msec(self, destination):
        """
        (store_mission_timer_c_msec, <destination>),
        Retrieves current value of third mission timer, in milliseconds.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_mission_timer_c_msec(destination)
        """
        return self.append((store_mission_timer_c_msec, destination))
        
    def mission_cam_set_mode(self, mission_cam_mode, duration_in_one_per_thousand_sec, value):
        """
        (mission_cam_set_mode, <mission_cam_mode>, <duration_in_one_per_thousand_sec>, <value>),
        Not documented. Changes main camera mode. Camera mode is 0 for automatic and 1 for manual (controlled by code). Duration parameter is used when switching from manual to auto, to determine how long will camera move to it's new position. Third parameter is not documented.

		Args:
			mission_cam_mode (str|int):
			duration_in_one_per_thousand_sec (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_set_mode(mission_cam_mode, duration_in_one_per_thousand_sec, value)
        """
        return self.append((mission_cam_set_mode, mission_cam_mode, duration_in_one_per_thousand_sec, value))
        
    def mission_cam_set_screen_color(self, value):
        """
        (mission_cam_set_screen_color, <value>),
        Not documented. Paints the screen with solid color. Parameter <value> contains color code with alpha component. Can be used to block screen entirely, add tint etc.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_set_screen_color(value)
        """
        return self.append((mission_cam_set_screen_color, value))
        
    def mission_cam_animate_to_screen_color(self, value, duration_in_one_per_thousand_sec):
        """
        (mission_cam_animate_to_screen_color, <value>, <duration_in_one_per_thousand_sec>),
        Not documented. Same as above, but color change is gradual. Used in Native to fill the screen with white before the end of marriage scene.

		Args:
			value (str|int):
			duration_in_one_per_thousand_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_animate_to_screen_color(value, duration_in_one_per_thousand_sec)
        """
        return self.append((mission_cam_animate_to_screen_color, value, duration_in_one_per_thousand_sec))
        
    def mission_cam_get_position(self):
        """
        (mission_cam_get_position),
        Retrieves the current position of camera during the mission (i.e. the point from which the player is observing the game).

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_get_position(value, duration_in_one_per_thousand_sec)
        """
        return self.append((mission_cam_get_position))
        
    def mission_cam_set_position(self):
        """
        (mission_cam_set_position),
        Moves the camera to the specified position during the mission.

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_set_position(value, duration_in_one_per_thousand_sec)
        """
        return self.append((mission_cam_set_position))
        
    def mission_cam_animate_to_position(self, position_register_no, duration_in_one_per_thousand_sec, value):
        """
        (mission_cam_animate_to_position, <position_register_no>, <duration_in_one_per_thousand_sec>, <value>),
        Moves the camera to the specified position smoothly. Second parameter determines how long it will take camera to move to destination, third parameter determines whether camera velocity will be linear (value = 0) or non-linear (value = 1).

		Args:
			position_register_no (str|int):
			duration_in_one_per_thousand_sec (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_animate_to_position(position_register_no, duration_in_one_per_thousand_sec, value)
        """
        return self.append((mission_cam_animate_to_position, position_register_no, duration_in_one_per_thousand_sec, value))
        
    def mission_cam_get_aperture(self):
        """
        (mission_cam_get_aperture),
        Not documented. View angle?

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_get_aperture(position_register_no, duration_in_one_per_thousand_sec, value)
        """
        return self.append((mission_cam_get_aperture))
        
    def mission_cam_set_aperture(self):
        """
        (mission_cam_set_aperture),
        Not documented.

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_set_aperture(position_register_no, duration_in_one_per_thousand_sec, value)
        """
        return self.append((mission_cam_set_aperture))
        
    def mission_cam_animate_to_aperture(self, value1, value2):
        """
        (mission_cam_animate_to_aperture, <value>, <duration_in_one_per_thousand_sec>, <value>),
        Not documented. if value = 0, then camera velocity will be linear. else it will be non-linear

		Args:
			value1 (str|int):
			value2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_animate_to_aperture(value1, value2)
        """
        return self.append((mission_cam_animate_to_aperture, value1, value2))
        
    def mission_cam_animate_to_position_and_aperture(self, value1, value2):
        """
        (mission_cam_animate_to_position_and_aperture, <position_register_no>, <value>, <duration_in_one_per_thousand_sec>, <value>),
        Not documented. if value = 0, then camera velocity will be linear. else it will be non-linear

		Args:
			value1 (str|int):
			value2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_animate_to_position_and_aperture(value1, value2)
        """
        return self.append((mission_cam_animate_to_position_and_aperture, value1, value2))
        
    def mission_cam_set_target_agent(self, agent_id, value):
        """
        (mission_cam_set_target_agent, <agent_id>, <value>),
        Not documented. if value = 0 then do not use agent's rotation, else use agent's rotation

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_set_target_agent(agent_id, value)
        """
        return self.append((mission_cam_set_target_agent, agent_id, value))
        
    def mission_cam_clear_target_agent(self):
        """
        (mission_cam_clear_target_agent),
        Not documented.

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_clear_target_agent(agent_id, value)
        """
        return self.append((mission_cam_clear_target_agent))
        
    def mission_cam_set_animation(self, anim_id):
        """
        (mission_cam_set_animation, <anim_id>),
        Not documented.

		Args:
			anim_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mission_cam_set_animation(anim_id)
        """
        return self.append((mission_cam_set_animation, anim_id))
        
    def mouse_get_world_projection(self, position_no_1, position_no_2):
        """
        (mouse_get_world_projection, <position_no_1>, <position_no_2>),
        Version 1.161+. Returns current camera coordinates (first position) and mouse projection to the back of the world (second position). Rotation data of resulting positions seems unreliable.

		Args:
			position_no_1 (str|int):
			position_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> mouse_get_world_projection(position_no_1, position_no_2)
        """
        return self.append((mouse_get_world_projection, position_no_1, position_no_2))
        
    def cast_ray(self, destination, hit_position_register, ray_position_register, ray_length_fixed_point):
        """
        (cast_ray, <destination>, <hit_position_register>, <ray_position_register>, [<ray_length_fixed_point>]),
        Version 1.161+. Casts a ray starting from <ray_position_register> and stores the closest hit position into <hit_position_register> (fails if no hits). If the body hit is a scene prop, its instance id will be stored into <destination>, otherwise it will be -1. Optional <ray_length> parameter seems to have no effect.

		Args:
			destination (str|int):
			hit_position_register (str|int):
			ray_position_register (str|int):
			ray_length_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> cast_ray(destination, hit_position_register, ray_position_register, ray_length_fixed_point)
        """
        return self.append((cast_ray, destination, hit_position_register, ray_position_register, ray_length_fixed_point))
        
    def set_postfx(self):
        """
        (set_postfx),
        This operation is not documented nor any examples of it's use could be found. Parameters are unknown.

        Returns:
            TupleBuilder: self

        Example:
            >>> set_postfx(destination, hit_position_register, ray_position_register, ray_length_fixed_point)
        """
        return self.append((set_postfx))
        
    def set_river_shader_to_mud(self):
        """
        (set_river_shader_to_mud),
        Changes river material for muddy env. This operation is not documented nor any examples of it's use could be found. Parameters are unknown.

        Returns:
            TupleBuilder: self

        Example:
            >>> set_river_shader_to_mud(destination, hit_position_register, ray_position_register, ray_length_fixed_point)
        """
        return self.append((set_river_shader_to_mud))
        
    def rebuild_shadow_map(self):
        """
        (rebuild_shadow_map),
        Version 1.153+. UNTESTED. Effects unknown. Rebuilds shadow map for the current scene. Apparently useful after heavy manipulation with scene props.

        Returns:
            TupleBuilder: self

        Example:
            >>> rebuild_shadow_map(destination, hit_position_register, ray_position_register, ray_length_fixed_point)
        """
        return self.append((rebuild_shadow_map))
        
    def set_shader_param_int(self, parameter_name, value):
        """
        (set_shader_param_int, <parameter_name>, <value>),
        Sets the int shader parameter <parameter_name> to <value>
		Version 1.153+. UNTESTED. Allows direct manupulation of shader parameters. Operation scope is unknown, possibly global. Parameter is an int value.

		Args:
			parameter_name (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_shader_param_int(parameter_name, value)
        """
        return self.append((set_shader_param_int, parameter_name, value))
        
    def set_shader_param_float(self, parameter_name, value_fixed_point):
        """
        (set_shader_param_float, <parameter_name>, <value_fixed_point>),
        Version 1.153+. Allows direct manupulation of shader parameters. Operation scope is unknown, possibly global. Parameter is a float value.

		Args:
			parameter_name (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_shader_param_float(parameter_name, value_fixed_point)
        """
        return self.append((set_shader_param_float, parameter_name, value_fixed_point))
        
    def set_shader_param_float4(self, parameter_name, valuex, valuey, valuez, valuew):
        """
        (set_shader_param_float4, <parameter_name>, <valuex>, <valuey>, <valuez>, <valuew>),
        Version 1.153+. Allows direct manupulation of shader parameters. Operation scope is unknown, possibly global. Parameter is a set of 4 float values.

		Args:
			parameter_name (str|int):
			valuex (str|int):
			valuey (str|int):
			valuez (str|int):
			valuew (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_shader_param_float4(parameter_name, valuex, valuey, valuez, valuew)
        """
        return self.append((set_shader_param_float4, parameter_name, valuex, valuey, valuez, valuew))
        
    def set_shader_param_float4x4(self, parameter_name, *args):
        """
        (set_shader_param_float4x4, <parameter_name>, [0][0], [0][1], [0][2], [1][0], [1][1], [1][2], [2][0], [2][1], [2][2], [3][0], [3][1], [3][2]),
        Version 1.153+. Allows direct manupulation of shader parameters. Operation scope is unknown, possibly global. Parameter is a set of 4x4 float values.

		Args:
			parameter_name (str|int):
			args (str|int): params

        Returns:
            TupleBuilder: self

        Example:
            >>> set_shader_param_float4x4("@user_value_float4x4", 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120)
        """
        operation = (set_shader_param_float4x4, parameter_name, args)
        flattened_operation = tuple(j for i in operation for j in (i if type(i) is tuple else (i,)))

        return self.append(flattened_operation)
        
    def prop_instance_is_valid(self, scene_prop_instance_id):
        """
        (prop_instance_is_valid, <scene_prop_instance_id>),
        Checks that the reference to a scene prop instance is valid (i.e. it was not removed).

		Args:
			scene_prop_instance_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_is_valid(scene_prop_instance_id)
        """
        return self.append((prop_instance_is_valid, scene_prop_instance_id))
        
    def prop_instance_is_animating(self, destination, scene_prop_id):
        """
        (prop_instance_is_animating, <destination>, <scene_prop_id>),
        Checks that the scene prop instance is currently animating.

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_is_animating(destination, scene_prop_id)
        """
        return self.append((prop_instance_is_animating, destination, scene_prop_id))
        
    def prop_instance_intersects_with_prop_instance(self, checked_scene_prop_id, scene_prop_id):
        """
        (prop_instance_intersects_with_prop_instance, <checked_scene_prop_id>, <scene_prop_id>),
        Checks if two scene props are intersecting (i.e. collided). Useful when animating scene props movement. Pass -1 for second parameter to check the prop against all other props on the scene.

		Args:
			checked_scene_prop_id (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_intersects_with_prop_instance(checked_scene_prop_id, scene_prop_id)
        """
        return self.append((prop_instance_intersects_with_prop_instance, checked_scene_prop_id, scene_prop_id))
        
    def scene_prop_has_agent_on_it(self, scene_prop_instance_id, agent_id):
        """
        (scene_prop_has_agent_on_it, <scene_prop_instance_id>, <agent_id>),
        Checks that the specified agent is standing on the scene prop instance.

		Args:
			scene_prop_instance_id (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_has_agent_on_it(scene_prop_instance_id, agent_id)
        """
        return self.append((scene_prop_has_agent_on_it, scene_prop_instance_id, agent_id))
        
    def scene_prop_set_slot(self, scene_prop_instance_id, slot_no, value):
        """
        (scene_prop_set_slot, <scene_prop_instance_id>, <slot_no>, <value>),
        

		Args:
			scene_prop_instance_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_set_slot(scene_prop_instance_id, slot_no, value)
        """
        return self.append((scene_prop_set_slot, scene_prop_instance_id, slot_no, value))
        
    def scene_prop_get_slot(self, destination, scene_prop_instance_id, slot_no):
        """
        (scene_prop_get_slot, <destination>, <scene_prop_instance_id>, <slot_no>),
        

		Args:
			destination (str|int):
			scene_prop_instance_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_slot(destination, scene_prop_instance_id, slot_no)
        """
        return self.append((scene_prop_get_slot, destination, scene_prop_instance_id, slot_no))
        
    def scene_prop_slot_eq(self, scene_prop_instance_id, slot_no, value):
        """
        (scene_prop_slot_eq, <scene_prop_instance_id>, <slot_no>, <value>),
        

		Args:
			scene_prop_instance_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_slot_eq(scene_prop_instance_id, slot_no, value)
        """
        return self.append((scene_prop_slot_eq, scene_prop_instance_id, slot_no, value))
        
    def scene_prop_slot_ge(self, scene_prop_instance_id, slot_no, value):
        """
        (scene_prop_slot_ge, <scene_prop_instance_id>, <slot_no>, <value>),
        

		Args:
			scene_prop_instance_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_slot_ge(scene_prop_instance_id, slot_no, value)
        """
        return self.append((scene_prop_slot_ge, scene_prop_instance_id, slot_no, value))
        
    def prop_instance_get_scene_prop_kind(self, destination, scene_prop_id):
        """
        (prop_instance_get_scene_prop_kind, <destination>, <scene_prop_id>),
        Retrieves the scene prop for the specified prop instance.

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_scene_prop_kind(destination, scene_prop_id)
        """
        return self.append((prop_instance_get_scene_prop_kind, destination, scene_prop_id))
        
    def scene_prop_get_num_instances(self, destination, scene_prop_id):
        """
        (scene_prop_get_num_instances, <destination>, <scene_prop_id>),
        Retrieves the total number of instances of a specified scene prop on the current scene.

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_num_instances(destination, scene_prop_id)
        """
        return self.append((scene_prop_get_num_instances, destination, scene_prop_id))
        
    def scene_prop_get_instance(self, destination, scene_prop_id, instance_no):
        """
        (scene_prop_get_instance, <destination>, <scene_prop_id>, <instance_no>),
        Retrieves the reference to a scene prop instance by it's number.

		Args:
			destination (str|int):
			scene_prop_id (str|int):
			instance_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_instance(destination, scene_prop_id, instance_no)
        """
        return self.append((scene_prop_get_instance, destination, scene_prop_id, instance_no))
        
    def scene_prop_enable_after_time(self, scene_prop_id, time_period):
        """
        (scene_prop_enable_after_time, <scene_prop_id>, <time_period>),
        Prevents usable scene prop from being used for the specified time period in 1/100th of second. Commonly used to implement "cooldown" periods.

		Args:
			scene_prop_id (str|int):
			time_period (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_enable_after_time(scene_prop_id, time_period)
        """
        return self.append((scene_prop_enable_after_time, scene_prop_id, time_period))
        
    def set_spawn_position(self, position):
        """
        (set_spawn_position, <position>),
        Defines the position which will later be used by (spawn_scene_prop), (spawn_scene_item), (spawn_agent) and (spawn_horse) operations.

		Args:
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_spawn_position(position)
        """
        return self.append((set_spawn_position, position))
        
    def spawn_scene_prop(self, scene_prop_id):
        """
        (spawn_scene_prop, <scene_prop_id>),
        Spawns a new scene prop instance of the specified type at the position defined by the last call to (set_spawn_position). Operation was supposed to store the prop_instance_id of the spawned position in reg0, but does not do this at the moment.

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> spawn_scene_prop(scene_prop_id)
        """
        return self.append((spawn_scene_prop, scene_prop_id))
        
    def prop_instance_get_variation_id(self, destination, scene_prop_id):
        """
        (prop_instance_get_variation_id, <destination>, <scene_prop_id>),
        Retrieves the first variation ID number for the specified scene prop instance.

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_variation_id(destination, scene_prop_id)
        """
        return self.append((prop_instance_get_variation_id, destination, scene_prop_id))
        
    def prop_instance_get_variation_id_2(self, destination, scene_prop_id):
        """
        (prop_instance_get_variation_id_2, <destination>, <scene_prop_id>),
        Retrieves the second variation ID number for the specified scene prop instance.

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_variation_id_2(destination, scene_prop_id)
        """
        return self.append((prop_instance_get_variation_id_2, destination, scene_prop_id))
        
    def replace_prop_instance(self, scene_prop_id, new_scene_prop_id):
        """
        (replace_prop_instance, <scene_prop_id>, <new_scene_prop_id>),
        Replaces a single scene prop instance with an instance of another scene prop (usually with the same dimensions, but not necessarily so). Can only be called in ti_before_mission_start trigger in module_mission_templates.py.

		Args:
			scene_prop_id (str|int):
			new_scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> replace_prop_instance(scene_prop_id, new_scene_prop_id)
        """
        return self.append((replace_prop_instance, scene_prop_id, new_scene_prop_id))
        
    def replace_scene_props(self, old_scene_prop_id, new_scene_prop_id):
        """
        (replace_scene_props, <old_scene_prop_id>, <new_scene_prop_id>),
        Replaces all instances of specified scene prop type with another scene prop type. Commonly used to replace damaged walls with their intact versions during normal visits to castle scenes. Can only be called in ti_before_mission_start trigger in module_mission_templates.py.

		Args:
			old_scene_prop_id (str|int):
			new_scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> replace_scene_props(old_scene_prop_id, new_scene_prop_id)
        """
        return self.append((replace_scene_props, old_scene_prop_id, new_scene_prop_id))
        
    def scene_prop_fade_out(self, scene_prop_id, fade_out_time):
        """
        (scene_prop_fade_out, <scene_prop_id>, <fade_out_time>),
        Version 1.153+. Makes the scene prop instance disappear within specified time.

		Args:
			scene_prop_id (str|int):
			fade_out_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_fade_out(scene_prop_id, fade_out_time)
        """
        return self.append((scene_prop_fade_out, scene_prop_id, fade_out_time))
        
    def scene_prop_fade_in(self, scene_prop_id, fade_in_time):
        """
        (scene_prop_fade_in, <scene_prop_id>, <fade_in_time>),
        Version 1.153+. Makes the scene prop instance reappear within specified time.

		Args:
			scene_prop_id (str|int):
			fade_in_time (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_fade_in(scene_prop_id, fade_in_time)
        """
        return self.append((scene_prop_fade_in, scene_prop_id, fade_in_time))
        
    def prop_instance_set_material(self, prop_instance_no, sub_mesh_no, string_register):
        """
        (prop_instance_set_material, <prop_instance_no>, <sub_mesh_no>, <string_register>),
        Version 1.161+. 4research. give sub mesh as -1 to change all meshes' materials.

		Args:
			prop_instance_no (str|int):
			sub_mesh_no (str|int):
			string_register (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_set_material(prop_instance_no, sub_mesh_no, string_register)
        """
        return self.append((prop_instance_set_material, prop_instance_no, sub_mesh_no, string_register))
        
    def scene_prop_get_visibility(self, destination, scene_prop_id):
        """
        (scene_prop_get_visibility, <destination>, <scene_prop_id>),
        Retrieves the current visibility state of the scene prop instance (1 = visible, 0 = invisible).

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_visibility(destination, scene_prop_id)
        """
        return self.append((scene_prop_get_visibility, destination, scene_prop_id))
        
    def scene_prop_set_visibility(self, scene_prop_id, value):
        """
        (scene_prop_set_visibility, <scene_prop_id>, <value>),
        Shows (value = 1) or hides (value = 0) the scene prop instance. What does it do with collision? 4research.

		Args:
			scene_prop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_set_visibility(scene_prop_id, value)
        """
        return self.append((scene_prop_set_visibility, scene_prop_id, value))
        
    def scene_prop_get_hit_points(self, destination, scene_prop_id):
        """
        (scene_prop_get_hit_points, <destination>, <scene_prop_id>),
        Retrieves current number of hit points that the scene prop instance has.

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_hit_points(destination, scene_prop_id)
        """
        return self.append((scene_prop_get_hit_points, destination, scene_prop_id))
        
    def scene_prop_get_max_hit_points(self, destination, scene_prop_id):
        """
        (scene_prop_get_max_hit_points, <destination>, <scene_prop_id>),
        Retrieves the maximum number of hit points that the scene prop instance has (useful to calculate the percent of damage).

		Args:
			destination (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_max_hit_points(destination, scene_prop_id)
        """
        return self.append((scene_prop_get_max_hit_points, destination, scene_prop_id))
        
    def scene_prop_set_hit_points(self, scene_prop_id, value):
        """
        (scene_prop_set_hit_points, <scene_prop_id>, <value>),
        Sets the number of hit points that the scene prop has. Both current and max hit points are affected. Only makes sense for sokf_destructible scene props.

		Args:
			scene_prop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_set_hit_points(scene_prop_id, value)
        """
        return self.append((scene_prop_set_hit_points, scene_prop_id, value))
        
    def scene_prop_set_cur_hit_points(self, scene_prop_id, value):
        """
        (scene_prop_set_cur_hit_points, <scene_prop_id>, <value>),
        Version 1.153+. Sets current HP amount for scene prop.

		Args:
			scene_prop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_set_cur_hit_points(scene_prop_id, value)
        """
        return self.append((scene_prop_set_cur_hit_points, scene_prop_id, value))
        
    def prop_instance_receive_damage(self, scene_prop_id, agent_id, damage_value):
        """
        (prop_instance_receive_damage, <scene_prop_id>, <agent_id>, <damage_value>),
        Makes scene prop instance receive specified amount of damage from any arbitrary agent. Agent reference is apparently necessary to properly initialize ti_on_scene_prop_hit trigger parameters.

		Args:
			scene_prop_id (str|int):
			agent_id (str|int):
			damage_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_receive_damage(scene_prop_id, agent_id, damage_value)
        """
        return self.append((prop_instance_receive_damage, scene_prop_id, agent_id, damage_value))
        
    def prop_instance_refill_hit_points(self, scene_prop_id):
        """
        (prop_instance_refill_hit_points, <scene_prop_id>),
        Restores hit points of a scene prop instance to their maximum value.

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_refill_hit_points(scene_prop_id)
        """
        return self.append((prop_instance_refill_hit_points, scene_prop_id))
        
    def scene_prop_get_team(self, value, scene_prop_id):
        """
        (scene_prop_get_team, <value>, <scene_prop_id>),
        Retrieves the team controlling the scene prop instance.

		Args:
			value (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_get_team(value, scene_prop_id)
        """
        return self.append((scene_prop_get_team, value, scene_prop_id))
        
    def scene_prop_set_team(self, scene_prop_id, value):
        """
        (scene_prop_set_team, <scene_prop_id>, <value>),
        Assigns the scene prop instance to a certain team.

		Args:
			scene_prop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_set_team(scene_prop_id, value)
        """
        return self.append((scene_prop_set_team, scene_prop_id, value))
        
    def scene_prop_set_prune_time(self, scene_prop_id, value):
        """
        (scene_prop_set_prune_time, <scene_prop_id>, <value>),
        Not documented. Not used in Native. Taleworlds comment: Prune time can only be set to objects that are already on the prune queue. Static objects are not affected by this operation.

		Args:
			scene_prop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_prop_set_prune_time(scene_prop_id, value)
        """
        return self.append((scene_prop_set_prune_time, scene_prop_id, value))
        
    def prop_instance_get_position(self, position, scene_prop_id):
        """
        (prop_instance_get_position, <position>, <scene_prop_id>),
        Retrieves the prop instance current position on the scene.

		Args:
			position (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_position(position, scene_prop_id)
        """
        return self.append((prop_instance_get_position, position, scene_prop_id))
        
    def prop_instance_get_starting_position(self, position, scene_prop_id):
        """
        (prop_instance_get_starting_position, <position>, <scene_prop_id>),
        Retrieves the prop instance starting position on the scene (i.e. the place where it was positioned when initialized).

		Args:
			position (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_starting_position(position, scene_prop_id)
        """
        return self.append((prop_instance_get_starting_position, position, scene_prop_id))
        
    def prop_instance_set_position(self, scene_prop_id, position, dont_send_to_clients):
        """
        (prop_instance_set_position, <scene_prop_id>, <position>, [dont_send_to_clients]),
        Teleports prop instance to another position. Optional flag dont_send_to_clients can be used on the server to prevent position change from being replicated to client machines (useful when doing some calculations which require to move the prop temporarily to another place).

		Args:
			scene_prop_id (str|int):
			position (str|int):
			dont_send_to_clients (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_set_position(scene_prop_id, position, dont_send_to_clients)
        """
        return self.append((prop_instance_set_position, scene_prop_id, position, dont_send_to_clients))
        
    def prop_instance_animate_to_position(self, scene_prop_id, position, duration_in_one_per_hundred_sec):
        """
        (prop_instance_animate_to_position, <scene_prop_id>, position, <duration_in_one_per_hundred_sec>),
        Moves prop instance to another position during the specified time frame (i.e. animates). Time is specified in 1/100th of second.

		Args:
			scene_prop_id (str|int):
			position (str|int):
			duration_in_one_per_hundred_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_animate_to_position(scene_prop_id, position, duration_in_one_per_hundred_sec)
        """
        return self.append((prop_instance_animate_to_position, scene_prop_id, position, duration_in_one_per_hundred_sec))
        
    def prop_instance_get_animation_target_position(self, pos, scene_prop_id):
        """
        (prop_instance_get_animation_target_position, <pos>, <scene_prop_id>),
        Retrieves the position that the prop instance is currently animating to.

		Args:
			pos (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_animation_target_position(pos, scene_prop_id)
        """
        return self.append((prop_instance_get_animation_target_position, pos, scene_prop_id))
        
    def prop_instance_stop_animating(self, scene_prop_id):
        """
        (prop_instance_stop_animating, <scene_prop_id>),
        Stops animating of the prop instance in the current position.

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_stop_animating(scene_prop_id)
        """
        return self.append((prop_instance_stop_animating, scene_prop_id))
        
    def prop_instance_get_scale(self, position, scene_prop_id):
        """
        (prop_instance_get_scale, <position>, <scene_prop_id>),
        Retrieves the current scaling factors of the prop instance.

		Args:
			position (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_scale(position, scene_prop_id)
        """
        return self.append((prop_instance_get_scale, position, scene_prop_id))
        
    def prop_instance_set_scale(self, scene_prop_id, value_x_fixed_point, value_y_fixed_point, value_z_fixed_point):
        """
        (prop_instance_set_scale, <scene_prop_id>, <value_x_fixed_point>, <value_y_fixed_point>, <value_z_fixed_point>),
        Sets new scaling factors for the scene prop.

		Args:
			scene_prop_id (str|int):
			value_x_fixed_point (str|int):
			value_y_fixed_point (str|int):
			value_z_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_set_scale(scene_prop_id, value_x_fixed_point, value_y_fixed_point, value_z_fixed_point)
        """
        return self.append((prop_instance_set_scale, scene_prop_id, value_x_fixed_point, value_y_fixed_point, value_z_fixed_point))
        
    def prop_instance_enable_physics(self, scene_prop_id, value):
        """
        (prop_instance_enable_physics, <scene_prop_id>, <value>),
        Enables (value = 1) or disables (value = 0) physics calculation (gravity, collision checks) for the scene prop instance.

		Args:
			scene_prop_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_enable_physics(scene_prop_id, value)
        """
        return self.append((prop_instance_enable_physics, scene_prop_id, value))
        
    def prop_instance_initialize_rotation_angles(self, scene_prop_id):
        """
        (prop_instance_initialize_rotation_angles, <scene_prop_id>),
        Should be called to initialize the scene prop instance prior to any calls to (prop_instance_rotate_to_position).

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_initialize_rotation_angles(scene_prop_id)
        """
        return self.append((prop_instance_initialize_rotation_angles, scene_prop_id))
        
    def prop_instance_rotate_to_position(self, scene_prop_id, position, duration_in_one_per_hundred_sec, total_rotate_angle_fixed_point):
        """
        (prop_instance_rotate_to_position, <scene_prop_id>, <position>, <duration_in_one_per_hundred_sec>, <total_rotate_angle_fixed_point>),
        Specified prop instance will move to the target position within the specified duration of time, and within the same time it will rotate for the specified angle. Used in Native code to simulate behavior of belfry wheels and rotating winches.

		Args:
			scene_prop_id (str|int):
			position (str|int):
			duration_in_one_per_hundred_sec (str|int):
			total_rotate_angle_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_rotate_to_position(scene_prop_id, position, duration_in_one_per_hundred_sec, total_rotate_angle_fixed_point)
        """
        return self.append((prop_instance_rotate_to_position, scene_prop_id, position, duration_in_one_per_hundred_sec, total_rotate_angle_fixed_point))
        
    def prop_instance_clear_attached_missiles(self, scene_prop_id):
        """
        (prop_instance_clear_attached_missiles, <scene_prop_id>),
        Version 1.153+. Removes all missiles currently attached to the scene prop. Only works with dynamic scene props.

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_clear_attached_missiles(scene_prop_id)
        """
        return self.append((prop_instance_clear_attached_missiles, scene_prop_id))
        
    def prop_instance_dynamics_set_properties(self, scene_prop_id, position):
        """
        (prop_instance_dynamics_set_properties, <scene_prop_id>, <position>),
        Initializes physical parameters of a scene prop. Position (X,Y) coordinates are used to store object's mass and friction coefficient. Coordinate Z is reserved (set it to zero just in case). Scene prop must be defined as sokf_moveable|sokf_dynamic_physics, and a call to (prop_instance_enable_physics) must be previously made.

		Args:
			scene_prop_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_dynamics_set_properties(scene_prop_id, position)
        """
        return self.append((prop_instance_dynamics_set_properties, scene_prop_id, position))
        
    def prop_instance_dynamics_set_velocity(self, scene_prop_id, position):
        """
        (prop_instance_dynamics_set_velocity, <scene_prop_id>, <position>),
        Sets current movement speed for a scene prop. Position's coordinates define velocity along corresponding axis. Same comments as for (prop_instance_dynamics_set_properties).

		Args:
			scene_prop_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_dynamics_set_velocity(scene_prop_id, position)
        """
        return self.append((prop_instance_dynamics_set_velocity, scene_prop_id, position))
        
    def prop_instance_dynamics_set_omega(self, scene_prop_id, position):
        """
        (prop_instance_dynamics_set_omega, <scene_prop_id>, <position>),
        Sets current rotation speed for a scene prop. Position's coordinates define rotational speed around corresponding axis. Same comments as for (prop_instance_dynamics_set_properties).

		Args:
			scene_prop_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_dynamics_set_omega(scene_prop_id, position)
        """
        return self.append((prop_instance_dynamics_set_omega, scene_prop_id, position))
        
    def prop_instance_dynamics_apply_impulse(self, scene_prop_id, position):
        """
        (prop_instance_dynamics_apply_impulse, <scene_prop_id>, <position>),
        Applies an impulse of specified scale to the scene prop. Position's coordinates define instant change in movement speed along corresponding axis. Same comments as for (prop_instance_dynamics_set_properties).

		Args:
			scene_prop_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_dynamics_apply_impulse(scene_prop_id, position)
        """
        return self.append((prop_instance_dynamics_apply_impulse, scene_prop_id, position))
        
    def prop_instance_deform_to_time(self, prop_instance_no, value):
        """
        (prop_instance_deform_to_time, <prop_instance_no>, <value>),
        Version 1.161+. Deforms a vertex-animated scene prop to specified vertex time. If you open the mesh in OpenBrf, right one of "Time of frame" boxes contains the relevant value.

		Args:
			prop_instance_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_deform_to_time(prop_instance_no, value)
        """
        return self.append((prop_instance_deform_to_time, prop_instance_no, value))
        
    def prop_instance_deform_in_range(self, prop_instance_no, start_frame, end_frame, duration_in_one_per_thousand_sec):
        """
        (prop_instance_deform_in_range, <prop_instance_no>, <start_frame>, <end_frame>, <duration_in_one_per_thousand_sec>),
        Version 1.161+. Animate vertex-animated scene prop from start frame to end frame within the specified time period (in milliseconds). If you open the mesh in OpenBrf, right one of "Time of frame" boxes contains the relevant values for frame parameters.

		Args:
			prop_instance_no (str|int):
			start_frame (str|int):
			end_frame (str|int):
			duration_in_one_per_thousand_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_deform_in_range(prop_instance_no, start_frame, end_frame, duration_in_one_per_thousand_sec)
        """
        return self.append((prop_instance_deform_in_range, prop_instance_no, start_frame, end_frame, duration_in_one_per_thousand_sec))
        
    def prop_instance_deform_in_cycle_loop(self, prop_instance_no, start_frame, end_frame, duration_in_one_per_thousand_sec):
        """
        (prop_instance_deform_in_cycle_loop, <prop_instance_no>, <start_frame>, <end_frame>, <duration_in_one_per_thousand_sec>),
        Version 1.161+. Performs looping animation of vertex-animated scene prop within the specified vertex frame ranges and within specified time (in milliseconds). If you open the mesh in OpenBrf, right one of "Time of frame" boxes contains the relevant values for frame parameters.

		Args:
			prop_instance_no (str|int):
			start_frame (str|int):
			end_frame (str|int):
			duration_in_one_per_thousand_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_deform_in_cycle_loop(prop_instance_no, start_frame, end_frame, duration_in_one_per_thousand_sec)
        """
        return self.append((prop_instance_deform_in_cycle_loop, prop_instance_no, start_frame, end_frame, duration_in_one_per_thousand_sec))
        
    def prop_instance_get_current_deform_progress(self, destination, prop_instance_no):
        """
        (prop_instance_get_current_deform_progress, <destination>, <prop_instance_no>),
        Version 1.161+. Returns a percentage value between 0 and 100 if animation is still in progress. Returns 100 otherwise.

		Args:
			destination (str|int):
			prop_instance_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_current_deform_progress(destination, prop_instance_no)
        """
        return self.append((prop_instance_get_current_deform_progress, destination, prop_instance_no))
        
    def prop_instance_get_current_deform_frame(self, destination, prop_instance_no):
        """
        (prop_instance_get_current_deform_frame, <destination>, <prop_instance_no>),
        Version 1.161+. Returns current frame of a vertex-animated scene prop, rounded to nearest integer value.

		Args:
			destination (str|int):
			prop_instance_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_get_current_deform_frame(destination, prop_instance_no)
        """
        return self.append((prop_instance_get_current_deform_frame, destination, prop_instance_no))
        
    def prop_instance_play_sound(self, scene_prop_id, sound_id, flags):
        """
        (prop_instance_play_sound, <scene_prop_id>, <sound_id>, [flags]),
        Version 1.153+. Makes the scene prop play a specified sound. See sf_* flags in header_sounds.py for reference on possible options.

		Args:
			scene_prop_id (str|int):
			sound_id (str|int):
			flags (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_play_sound(scene_prop_id, sound_id, flags)
        """
        return self.append((prop_instance_play_sound, scene_prop_id, sound_id, flags))
        
    def prop_instance_stop_sound(self, scene_prop_id):
        """
        (prop_instance_stop_sound, <scene_prop_id>),
        Version 1.153+. Stops any sound currently played by the scene prop instance.

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_stop_sound(scene_prop_id)
        """
        return self.append((prop_instance_stop_sound, scene_prop_id))
        
    def scene_item_get_num_instances(self, destination, item_id):
        """
        (scene_item_get_num_instances, <destination>, <item_id>),
        Gets the number of specified scene items present on the scene. Scene items behave exactly like scene props (i.e. cannot be picked).

		Args:
			destination (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_item_get_num_instances(destination, item_id)
        """
        return self.append((scene_item_get_num_instances, destination, item_id))
        
    def scene_item_get_instance(self, destination, item_id, instance_no):
        """
        (scene_item_get_instance, <destination>, <item_id>, <instance_no>),
        Retrieves the reference to a single instance of a scene item by it's sequential number.

		Args:
			destination (str|int):
			item_id (str|int):
			instance_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_item_get_instance(destination, item_id, instance_no)
        """
        return self.append((scene_item_get_instance, destination, item_id, instance_no))
        
    def scene_spawned_item_get_num_instances(self, destination, item_id):
        """
        (scene_spawned_item_get_num_instances, <destination>, <item_id>),
        Retrieves the number of specified spawned items present on the scene. Spawned items are actual items, i.e. they can be picked by player.

		Args:
			destination (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_spawned_item_get_num_instances(destination, item_id)
        """
        return self.append((scene_spawned_item_get_num_instances, destination, item_id))
        
    def scene_spawned_item_get_instance(self, destination, item_id, instance_no):
        """
        (scene_spawned_item_get_instance, <destination>, <item_id>, <instance_no>),
        Retrieves the reference to a single instance of a spawned item by it's sequential number.

		Args:
			destination (str|int):
			item_id (str|int):
			instance_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> scene_spawned_item_get_instance(destination, item_id, instance_no)
        """
        return self.append((scene_spawned_item_get_instance, destination, item_id, instance_no))
        
    def replace_scene_items_with_scene_props(self, old_item_id, new_scene_prop_id):
        """
        (replace_scene_items_with_scene_props, <old_item_id>, <new_scene_prop_id>),
        Replaces all instances of specified scene item with scene props. Can only be called in ti_before_mission_start trigger in module_mission_templates.py.

		Args:
			old_item_id (str|int):
			new_scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> replace_scene_items_with_scene_props(old_item_id, new_scene_prop_id)
        """
        return self.append((replace_scene_items_with_scene_props, old_item_id, new_scene_prop_id))
        
    def set_spawn_position(self, position):
        """
        (set_spawn_position, <position>),
        # DUPLICATE ENTRY
		Defines the position which will later be used by (spawn_scene_prop), (spawn_scene_item), (spawn_agent) and (spawn_horse) operations.

		Args:
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_spawn_position(position)
        """
        return self.append((set_spawn_position, position))
        
    def spawn_item(self, item_kind_id, item_modifier, seconds_before_pruning):
        """
        (spawn_item, <item_kind_id>, <item_modifier>, [seconds_before_pruning]),
        Spawns a new item, possibly with modifier, on the scene in the position specified by previous call to (set_spawn_position). Optional parameter determines time period (in second) after which the item will disappear. Using 0 will prevent the item from disappearing.

		Args:
			item_kind_id (str|int):
			item_modifier (str|int):
			seconds_before_pruning (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> spawn_item(item_kind_id, item_modifier, seconds_before_pruning)
        """
        return self.append((spawn_item, item_kind_id, item_modifier, seconds_before_pruning))
        
    def spawn_item_without_refill(self, item_kind_id, item_modifier, seconds_before_pruning):
        """
        (spawn_item_without_refill, <item_kind_id>, <item_modifier>, [seconds_before_pruning]),
        Version 1.153+. UNTESTED. It is unclear how this is different from standard (spawn_item).

		Args:
			item_kind_id (str|int):
			item_modifier (str|int):
			seconds_before_pruning (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> spawn_item_without_refill(item_kind_id, item_modifier, seconds_before_pruning)
        """
        return self.append((spawn_item_without_refill, item_kind_id, item_modifier, seconds_before_pruning))
        
    def set_current_color(self, red_value, green_value, blue_value):
        """
        (set_current_color, <red_value>, <green_value>, <blue_value>),
        Sets color for subsequent calls to (add_point_light) etc. Color component ranges are 0..255.

		Args:
			red_value (str|int):
			green_value (str|int):
			blue_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_current_color(red_value, green_value, blue_value)
        """
        return self.append((set_current_color, red_value, green_value, blue_value))
        
    def set_position_delta(self, value1, value2, value3):
        """
        (set_position_delta, <value>, <value>, <value>),
        Can only be called inside item or scene prop triggers. Sets (X,Y,Z) offsets from the item/prop current position for subsequent calls to (add_point_light) etc. Offsets are apparently in centimeters.

		Args:
			value1 (str|int):
			value2 (str|int):
			value3 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_position_delta(value1, value2, value3)
        """
        return self.append((set_position_delta, value1, value2, value3))
        
    def add_point_light(self, flicker_magnitude, flicker_interval):
        """
        (add_point_light, [flicker_magnitude], [flicker_interval]),
        Adds a point light source to an object with optional flickering magnitude (range 0..100) and flickering interval (in 1/100th of second). Uses position offset and color provided to previous calls to (set_position_delta) and (set_current_color). Can only be used in item triggers.

		Args:
			flicker_magnitude (str|int):
			flicker_interval (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_point_light(flicker_magnitude, flicker_interval)
        """
        return self.append((add_point_light, flicker_magnitude, flicker_interval))
        
    def add_point_light_to_entity(self, flicker_magnitude, flicker_interval):
        """
        (add_point_light_to_entity, [flicker_magnitude], [flicker_interval]),
        Adds a point light source to an object with optional flickering magnitude (range 0..100) and flickering interval (in 1/100th of second). Uses position offset and color provided to previous calls to (set_position_delta) and (set_current_color). Can only be used in scene prop triggers.

		Args:
			flicker_magnitude (str|int):
			flicker_interval (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_point_light_to_entity(flicker_magnitude, flicker_interval)
        """
        return self.append((add_point_light_to_entity, flicker_magnitude, flicker_interval))
        
    def particle_system_add_new(self, par_sys_id, position):
        """
        (particle_system_add_new, <par_sys_id>, [position]),
        Adds a new particle system to an object. Uses position offset and color provided to previous calls to (set_position_delta) and (set_current_color). Can only be used in item/prop triggers.

		Args:
			par_sys_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> particle_system_add_new(par_sys_id, position)
        """
        return self.append((particle_system_add_new, par_sys_id, position))
        
    def particle_system_emit(self, par_sys_id, value_num_particles, value_period):
        """
        (particle_system_emit, <par_sys_id>, <value_num_particles>, <value_period>),
        Adds a particle system in some fancy way. Uses position offset and color provided to previous calls to (set_position_delta) and (set_current_color). Can only be used in item/prop triggers.

		Args:
			par_sys_id (str|int):
			value_num_particles (str|int):
			value_period (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> particle_system_emit(par_sys_id, value_num_particles, value_period)
        """
        return self.append((particle_system_emit, par_sys_id, value_num_particles, value_period))
        
    def particle_system_burst(self, par_sys_id, position, percentage_burst_strength):
        """
        (particle_system_burst, <par_sys_id>, <position>, [percentage_burst_strength]),
        Bursts a particle system in specified position.

		Args:
			par_sys_id (str|int):
			position (str|int):
			percentage_burst_strength (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> particle_system_burst(par_sys_id, position, percentage_burst_strength)
        """
        return self.append((particle_system_burst, par_sys_id, position, percentage_burst_strength))
        
    def particle_system_burst_no_sync(self, par_sys_id, position_no, percentage_burst_strength):
        """
        (particle_system_burst_no_sync, <par_sys_id>, <position_no>, [percentage_burst_strength]),
        Version 1.153+. Same as above, but apparently does not synchronize this between server and client.

		Args:
			par_sys_id (str|int):
			position_no (str|int):
			percentage_burst_strength (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> particle_system_burst_no_sync(par_sys_id, position_no, percentage_burst_strength)
        """
        return self.append((particle_system_burst_no_sync, par_sys_id, position_no, percentage_burst_strength))
        
    def prop_instance_add_particle_system(self, scene_prop_id, par_sys_id, position_no):
        """
        (prop_instance_add_particle_system, <scene_prop_id>, <par_sys_id>, <position_no>),
        Version 1.153+. Adds a new particle system to the scene prop. Note that <position_no> is local, i.e. in relation to scene prop's coordinates and rotation.

		Args:
			scene_prop_id (str|int):
			par_sys_id (str|int):
			position_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_add_particle_system(scene_prop_id, par_sys_id, position_no)
        """
        return self.append((prop_instance_add_particle_system, scene_prop_id, par_sys_id, position_no))
        
    def prop_instance_stop_all_particle_systems(self, scene_prop_id):
        """
        (prop_instance_stop_all_particle_systems, <scene_prop_id>),
        Version 1.153+. Removes all particle systems currently associated with scene prop instance.

		Args:
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> prop_instance_stop_all_particle_systems(scene_prop_id)
        """
        return self.append((prop_instance_stop_all_particle_systems, scene_prop_id))
        
    def agent_is_in_special_mode(self, agent_id):
        """
        (agent_is_in_special_mode, <agent_id>),
        Checks that the agent is currently in scripted mode.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_in_special_mode(agent_id)
        """
        return self.append((agent_is_in_special_mode, agent_id))
        
    def agent_is_routed(self, agent_id):
        """
        (agent_is_routed, <agent_id>),
        Checks that the agent has fled from the map (i.e. reached the edge of the map in fleeing mode and then faded).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_routed(agent_id)
        """
        return self.append((agent_is_routed, agent_id))
        
    def agent_is_alive(self, agent_id):
        """
        (agent_is_alive, <agent_id>),
        Checks that the agent is alive.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_alive(agent_id)
        """
        return self.append((agent_is_alive, agent_id))
        
    def agent_is_wounded(self, agent_id):
        """
        (agent_is_wounded, <agent_id>),
        Checks that the agent has been knocked unconscious.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_wounded(agent_id)
        """
        return self.append((agent_is_wounded, agent_id))
        
    def agent_is_human(self, agent_id):
        """
        (agent_is_human, <agent_id>),
        Checks that the agent is human (i.e. not horse).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_human(agent_id)
        """
        return self.append((agent_is_human, agent_id))
        
    def agent_is_ally(self, agent_id):
        """
        (agent_is_ally, <agent_id>),
        Checks that the agent is allied to the player (belongs to player's party or allied party in current encounter).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_ally(agent_id)
        """
        return self.append((agent_is_ally, agent_id))
        
    def agent_is_non_player(self, agent_id):
        """
        (agent_is_non_player, <agent_id>),
        Checks that the agent is not a player.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_non_player(agent_id)
        """
        return self.append((agent_is_non_player, agent_id))
        
    def agent_is_defender(self, agent_id):
        """
        (agent_is_defender, <agent_id>),
        Checks that the agent belongs to the defending side (see encounter operations for details).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_defender(agent_id)
        """
        return self.append((agent_is_defender, agent_id))
        
    def agent_is_active(self, agent_id):
        """
        (agent_is_active, <agent_id>),
        Checks that the agent reference is active. This will succeed for dead or routed agents, for as long as the agent reference itself is valid.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_active(agent_id)
        """
        return self.append((agent_is_active, agent_id))
        
    def agent_has_item_equipped(self, agent_id, item_id):
        """
        (agent_has_item_equipped, <agent_id>, <item_id>),
        Checks that the agent has a specific item equipped.

		Args:
			agent_id (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_has_item_equipped(agent_id, item_id)
        """
        return self.append((agent_has_item_equipped, agent_id, item_id))
        
    def agent_is_in_parried_animation(self, agent_id):
        """
        (agent_is_in_parried_animation, <agent_id>),
        Checks that the agent is currently in parrying animation (defending from some attack).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_in_parried_animation(agent_id)
        """
        return self.append((agent_is_in_parried_animation, agent_id))
        
    def agent_is_alarmed(self, agent_id):
        """
        (agent_is_alarmed, <agent_id>),
        Checks that the agent is alarmed (in combat mode with weapon drawn).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_alarmed(agent_id)
        """
        return self.append((agent_is_alarmed, agent_id))
        
    def class_is_listening_order(self, team_no, sub_class):
        """
        (class_is_listening_order, <team_no>, <sub_class>),
        Checks that the specified group of specified team is listening to player's orders.

		Args:
			team_no (str|int):
			sub_class (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> class_is_listening_order(team_no, sub_class)
        """
        return self.append((class_is_listening_order, team_no, sub_class))
        
    def teams_are_enemies(self, team_no, team_no_2):
        """
        (teams_are_enemies, <team_no>, <team_no_2>),
        Checks that the two teams are hostile to each other.

		Args:
			team_no (str|int):
			team_no_2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> teams_are_enemies(team_no, team_no_2)
        """
        return self.append((teams_are_enemies, team_no, team_no_2))
        
    def agent_is_in_line_of_sight(self, agent_id, position_no):
        """
        (agent_is_in_line_of_sight, <agent_id>, <position_no>),
        Version 1.153+. Checks that the agent can be seen from specified position. Rotation of position register is not used (i.e. agent will be seen even if position is "looking" the other way).

		Args:
			agent_id (str|int):
			position_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_is_in_line_of_sight(agent_id, position_no)
        """
        return self.append((agent_is_in_line_of_sight, agent_id, position_no))
        
    def team_set_slot(self, team_id, slot_no, value):
        """
        (team_set_slot, <team_id>, <slot_no>, <value>),
        

		Args:
			team_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_slot(team_id, slot_no, value)
        """
        return self.append((team_set_slot, team_id, slot_no, value))
        
    def team_get_slot(self, destination, player_id, slot_no):
        """
        (team_get_slot, <destination>, <player_id>, <slot_no>),
        

		Args:
			destination (str|int):
			player_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_slot(destination, player_id, slot_no)
        """
        return self.append((team_get_slot, destination, player_id, slot_no))
        
    def team_slot_eq(self, team_id, slot_no, value):
        """
        (team_slot_eq, <team_id>, <slot_no>, <value>),
        

		Args:
			team_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_slot_eq(team_id, slot_no, value)
        """
        return self.append((team_slot_eq, team_id, slot_no, value))
        
    def team_slot_ge(self, team_id, slot_no, value):
        """
        (team_slot_ge, <team_id>, <slot_no>, <value>),
        

		Args:
			team_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_slot_ge(team_id, slot_no, value)
        """
        return self.append((team_slot_ge, team_id, slot_no, value))
        
    def agent_set_slot(self, agent_id, slot_no, value):
        """
        (agent_set_slot, <agent_id>, <slot_no>, <value>),
        

		Args:
			agent_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_slot(agent_id, slot_no, value)
        """
        return self.append((agent_set_slot, agent_id, slot_no, value))
        
    def agent_get_slot(self, destination, agent_id, slot_no):
        """
        (agent_get_slot, <destination>, <agent_id>, <slot_no>),
        

		Args:
			destination (str|int):
			agent_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_slot(destination, agent_id, slot_no)
        """
        return self.append((agent_get_slot, destination, agent_id, slot_no))
        
    def agent_slot_eq(self, agent_id, slot_no, value):
        """
        (agent_slot_eq, <agent_id>, <slot_no>, <value>),
        

		Args:
			agent_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_slot_eq(agent_id, slot_no, value)
        """
        return self.append((agent_slot_eq, agent_id, slot_no, value))
        
    def agent_slot_ge(self, agent_id, slot_no, value):
        """
        (agent_slot_ge, <agent_id>, <slot_no>, <value>),
        

		Args:
			agent_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_slot_ge(agent_id, slot_no, value)
        """
        return self.append((agent_slot_ge, agent_id, slot_no, value))
        
    def add_reinforcements_to_entry(self, mission_template_entry_no, wave_size):
        """
        (add_reinforcements_to_entry, <mission_template_entry_no>, <wave_size>),
        For battle missions, adds reinforcement wave to the specified entry point. Additional parameter determines relative wave size. Agents in reinforcement wave are taken from all parties of the side that the entry point belongs to due to mtef_team_* flags.

		Args:
			mission_template_entry_no (str|int):
			wave_size (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_reinforcements_to_entry(mission_template_entry_no, wave_size)
        """
        return self.append((add_reinforcements_to_entry, mission_template_entry_no, wave_size))
        
    def set_spawn_position(self):
        """
        (set_spawn_position),
        # DUPLICATE ENTRY
		Defines the position which will later be used by (spawn_scene_prop), (spawn_scene_item), (spawn_agent) and (spawn_horse) operations.

        Returns:
            TupleBuilder: self

        Example:
            >>> set_spawn_position(mission_template_entry_no, wave_size)
        """
        return self.append((set_spawn_position))
        
    def spawn_agent(self, troop_id):
        """
        (spawn_agent, <troop_id>),
        Spawns a new troop in the specified position and saves the reference to the new agent in reg0.

		Args:
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> spawn_agent(troop_id)
        """
        return self.append((spawn_agent, troop_id))
        
    def spawn_horse(self, item_kind_id, item_modifier):
        """
        (spawn_horse, <item_kind_id>, <item_modifier>),
        Spawns a new horse (with any modifier) in the specified position and saves the reference to the new agent in reg0.

		Args:
			item_kind_id (str|int):
			item_modifier (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> spawn_horse(item_kind_id, item_modifier)
        """
        return self.append((spawn_horse, item_kind_id, item_modifier))
        
    def remove_agent(self, agent_id):
        """
        (remove_agent, <agent_id>),
        Immediately removes the agent from the scene.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> remove_agent(agent_id)
        """
        return self.append((remove_agent, agent_id))
        
    def agent_fade_out(self, agent_id):
        """
        (agent_fade_out, <agent_id>),
        Fades out the agent from the scene (same effect as fleeing enemies when they get to the edge of map).

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_fade_out(agent_id)
        """
        return self.append((agent_fade_out, agent_id))
        
    def agent_play_sound(self, agent_id, sound_id):
        """
        (agent_play_sound, <agent_id>, <sound_id>),
        Makes the agent emit the specified sound.

		Args:
			agent_id (str|int):
			sound_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_play_sound(agent_id, sound_id)
        """
        return self.append((agent_play_sound, agent_id, sound_id))
        
    def agent_stop_sound(self, agent_id):
        """
        (agent_stop_sound, <agent_id>),
        Stops whatever sound agent is currently performing.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_stop_sound(agent_id)
        """
        return self.append((agent_stop_sound, agent_id))
        
    def agent_set_visibility(self, agent_id, value):
        """
        (agent_set_visibility, <agent_id>, <value>),
        Version 1.153+. Sets agent visibility. 0 for invisible, 1 for visible.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_visibility(agent_id, value)
        """
        return self.append((agent_set_visibility, agent_id, value))
        
    def get_player_agent_no(self, destination):
        """
        (get_player_agent_no, <destination>),
        Retrieves the reference to the player-controlled agent. Singleplayer mode only.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_player_agent_no(destination)
        """
        return self.append((get_player_agent_no, destination))
        
    def agent_get_kill_count(self, destination, agent_id, get_wounded):
        """
        (agent_get_kill_count, <destination>, <agent_id>, [get_wounded]),
        Retrieves the total number of kills by the specified agent during this battle. Call with non-zero <get_wounded> parameter to retrieve the total number of enemies the agent has knocked down.

		Args:
			destination (str|int):
			agent_id (str|int):
			get_wounded (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_kill_count(destination, agent_id, get_wounded)
        """
        return self.append((agent_get_kill_count, destination, agent_id, get_wounded))
        
    def agent_get_position(self, position, agent_id):
        """
        (agent_get_position, <position>, <agent_id>),
        Retrieves the position of the specified agent on the scene.

		Args:
			position (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_position(position, agent_id)
        """
        return self.append((agent_get_position, position, agent_id))
        
    def agent_set_position(self, agent_id, position):
        """
        (agent_set_position, <agent_id>, <position>),
        Teleports the agent to specified position on the scene. Be careful with riders - you must teleport the horse, not the rider for the operation to work correctly!

		Args:
			agent_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_position(agent_id, position)
        """
        return self.append((agent_set_position, agent_id, position))
        
    def agent_get_horse(self, destination, agent_id):
        """
        (agent_get_horse, <destination>, <agent_id>),
        Retrieves the reference to the horse agent that the specified agent is riding, or -1 if he's not riding a horse (or is a horse himself).

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_horse(destination, agent_id)
        """
        return self.append((agent_get_horse, destination, agent_id))
        
    def agent_get_rider(self, destination, horse_agent_id):
        """
        (agent_get_rider, <destination>, <horse_agent_id>),
        Retrieves the reference to the rider agent who is riding the specified horse, or -1 if there's no rider or the specified agent is not a horse.

		Args:
			destination (str|int):
			horse_agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_rider(destination, horse_agent_id)
        """
        return self.append((agent_get_rider, destination, horse_agent_id))
        
    def agent_get_party_id(self, destination, agent_id):
        """
        (agent_get_party_id, <destination>, <agent_id>),
        Retrieves the party that the specified agent belongs to (supposedly should only work in battle missions for agents spawned as starting/reinforcement waves).

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_party_id(destination, agent_id)
        """
        return self.append((agent_get_party_id, destination, agent_id))
        
    def agent_get_entry_no(self, destination, agent_id):
        """
        (agent_get_entry_no, <destination>, <agent_id>),
        Retrieves the entry point number where this agent has spawned. What does this return for agents spawned with (spawn_agent)? 4research.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_entry_no(destination, agent_id)
        """
        return self.append((agent_get_entry_no, destination, agent_id))
        
    def agent_get_troop_id(self, destination, agent_id):
        """
        (agent_get_troop_id, <destination>, <agent_id>),
        Retrieves the troop type of the specified agent. Returns -1 for horses (because horses are items, not troops).

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_troop_id(destination, agent_id)
        """
        return self.append((agent_get_troop_id, destination, agent_id))
        
    def agent_get_item_id(self, destination, horse_agent_id):
        """
        (agent_get_item_id, <destination>, <horse_agent_id>),
        Retrieves the item type of the specified horse agent. Returns -1 for humans.

		Args:
			destination (str|int):
			horse_agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_item_id(destination, horse_agent_id)
        """
        return self.append((agent_get_item_id, destination, horse_agent_id))
        
    def store_agent_hit_points(self, destination, agent_id, absolute):
        """
        (store_agent_hit_points, <destination>, <agent_id>, [absolute]),
        Retrieves current agent health. Optional last parameter determines whether actual health (absolute = 1) or relative percentile health (absolute = 0) is returned. Default is relative.

		Args:
			destination (str|int):
			agent_id (str|int):
			absolute (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_agent_hit_points(destination, agent_id, absolute)
        """
        return self.append((store_agent_hit_points, destination, agent_id, absolute))
        
    def agent_set_hit_points(self, agent_id, value, absolute):
        """
        (agent_set_hit_points, <agent_id>, <value>, [absolute]),
        Sets new value for agent health. Optional last parameter determines whether the value is interpreted as actual health (absolute = 1) or relative percentile health (absolute = 0). Default is relative.

		Args:
			agent_id (str|int):
			value (str|int):
			absolute (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_hit_points(agent_id, value, absolute)
        """
        return self.append((agent_set_hit_points, agent_id, value, absolute))
        
    def agent_set_max_hit_points(self, agent_id, value, absolute):
        """
        (agent_set_max_hit_points, <agent_id>, <value>, [absolute]),
        Version 1.153+. Changes agent's max hit points. Optional flag [absolute] determines if <value> is an absolute number of his points, or relative percentage (0..1000) of default value. Treated as percentage by default.

		Args:
			agent_id (str|int):
			value (str|int):
			absolute (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_max_hit_points(agent_id, value, absolute)
        """
        return self.append((agent_set_max_hit_points, agent_id, value, absolute))
        
    def agent_deliver_damage_to_agent(self, agent_id_deliverer, agent_id, damage_amount, weapon_item_id):
        """
        (agent_deliver_damage_to_agent, <agent_id_deliverer>, <agent_id>, [damage_amount], [weapon_item_id]),
        Makes one agent deal damage to another. Parameter damage_amount is optional, if it is skipped or <= 0, then damage will be calculated using attacker's weapon item and stats (like a normal weapon attack). Optional parameter weapon_item_id was added in 1.153 and will force the game the calculate the damage using this weapon.

		Args:
			agent_id_deliverer (str|int):
			agent_id (str|int):
			damage_amount (str|int):
			weapon_item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_deliver_damage_to_agent(agent_id_deliverer, agent_id, damage_amount, weapon_item_id)
        """
        return self.append((agent_deliver_damage_to_agent, agent_id_deliverer, agent_id, damage_amount, weapon_item_id))
        
    def agent_deliver_damage_to_agent_advanced(self, destination, attacker_agent_id, agent_id, value, weapon_item_id):
        """
        (agent_deliver_damage_to_agent_advanced, <destination>, <attacker_agent_id>, <agent_id>, <value>, [weapon_item_id]),
        Version 1.153+. Same as (agent_deliver_damage_to_agent), but resulting damage is returned. Also operation takes relations between agents into account, which may result in no damage, or even damage to attacker due to friendly fire rules.

		Args:
			destination (str|int):
			attacker_agent_id (str|int):
			agent_id (str|int):
			value (str|int):
			weapon_item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_deliver_damage_to_agent_advanced(destination, attacker_agent_id, agent_id, value, weapon_item_id)
        """
        return self.append((agent_deliver_damage_to_agent_advanced, destination, attacker_agent_id, agent_id, value, weapon_item_id))
        
    def add_missile(self, agent_id, starting_position, starting_speed_fixed_point, weapon_item_id, weapon_item_modifier, missile_item_id, missile_item_modifier):
        """
        (add_missile, <agent_id>, <starting_position>, <starting_speed_fixed_point>, <weapon_item_id>, <weapon_item_modifier>, <missile_item_id>, <missile_item_modifier>),
        Version 1.153+. Creates a missile with specified parameters. Note that <starting_position> parameter also determines the direction in which missile flies.

		Args:
			agent_id (str|int):
			starting_position (str|int):
			starting_speed_fixed_point (str|int):
			weapon_item_id (str|int):
			weapon_item_modifier (str|int):
			missile_item_id (str|int):
			missile_item_modifier (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> add_missile(agent_id, starting_position, starting_speed_fixed_point, weapon_item_id, weapon_item_modifier, missile_item_id, missile_item_modifier)
        """
        return self.append((add_missile, agent_id, starting_position, starting_speed_fixed_point, weapon_item_id, weapon_item_modifier, missile_item_id, missile_item_modifier))
        
    def agent_get_speed(self, position, agent_id):
        """
        (agent_get_speed, <position>, <agent_id>),
        Retrieves agent speed to (X,Y) coordinates of the position register. What do these mean - speed by world axis?

		Args:
			position (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_speed(position, agent_id)
        """
        return self.append((agent_get_speed, position, agent_id))
        
    def agent_set_no_death_knock_down_only(self, agent_id, value):
        """
        (agent_set_no_death_knock_down_only, <agent_id>, <value>),
        Sets the agent as unkillable (value = 1) or normal (value = 0). Unkillable agents will drop on the ground instead of dying and will stand up afterwards.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_no_death_knock_down_only(agent_id, value)
        """
        return self.append((agent_set_no_death_knock_down_only, agent_id, value))
        
    def agent_set_horse_speed_factor(self, agent_id, speed_multiplier_in_one_per_hundred):
        """
        (agent_set_horse_speed_factor, <agent_id>, <speed_multiplier_in_one_per_hundred>),
        Multiplies agent's horse speed (and maneuverability?) by the specified percentile value (using 100 will make the horse). Note that this is called on the rider, not on the horse! Supposedly will persist even if the agent changes horses. 4research.

		Args:
			agent_id (str|int):
			speed_multiplier_in_one_per_hundred (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_horse_speed_factor(agent_id, speed_multiplier_in_one_per_hundred)
        """
        return self.append((agent_set_horse_speed_factor, agent_id, speed_multiplier_in_one_per_hundred))
        
    def agent_set_speed_limit(self, agent_id, speed_limitkilometers_per_hour):
        """
        (agent_set_speed_limit, <agent_id>, <speed_limitkilometers_per_hour>),
        Limits agent speed by the specified value in kph. Use 5 for average walking speed. Affects only AI agents.

		Args:
			agent_id (str|int):
			speed_limitkilometers_per_hour (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_speed_limit(agent_id, speed_limitkilometers_per_hour)
        """
        return self.append((agent_set_speed_limit, agent_id, speed_limitkilometers_per_hour))
        
    def agent_set_damage_modifier(self, agent_id, value):
        """
        (agent_set_damage_modifier, <agent_id>, <value>),
        Version 1.153+. Changes the damage delivered by this agent. Value is in percentage, 100 is default, 1000 is max possible value.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_damage_modifier(agent_id, value)
        """
        return self.append((agent_set_damage_modifier, agent_id, value))
        
    def agent_set_accuracy_modifier(self, agent_id, value):
        """
        (agent_set_accuracy_modifier, <agent_id>, <value>),
        Version 1.153+. Changes agent's accuracy (with ranged weapons?). Value is in percentage, 100 is default, value can be between [0..1000]

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_accuracy_modifier(agent_id, value)
        """
        return self.append((agent_set_accuracy_modifier, agent_id, value))
        
    def agent_set_speed_modifier(self, agent_id, value):
        """
        (agent_set_speed_modifier, <agent_id>, <value>),
        Version 1.153+. Changes agent's speed. Value is in percentage, 100 is default, value can be between [0..1000]

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_speed_modifier(agent_id, value)
        """
        return self.append((agent_set_speed_modifier, agent_id, value))
        
    def agent_set_reload_speed_modifier(self, agent_id, value):
        """
        (agent_set_reload_speed_modifier, <agent_id>, <value>),
        Version 1.153+. Changes agent's reload speed. Value is in percentage, 100 is default, value can be between [0..1000]

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_reload_speed_modifier(agent_id, value)
        """
        return self.append((agent_set_reload_speed_modifier, agent_id, value))
        
    def agent_set_use_speed_modifier(self, agent_id, value):
        """
        (agent_set_use_speed_modifier, <agent_id>, <value>),
        Version 1.153+. Changes agent's speed with using various scene props. Value is in percentage, 100 is default, value can be between [0..1000]

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_use_speed_modifier(agent_id, value)
        """
        return self.append((agent_set_use_speed_modifier, agent_id, value))
        
    def agent_set_ranged_damage_modifier(self, agent_id, value):
        """
        (agent_set_ranged_damage_modifier, <agent_id>, <value>),
        Version 1.157+. Changes agent's damage with ranged weapons. Value is in percentage, 100 is default, value can be between [0..1000]

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_ranged_damage_modifier(agent_id, value)
        """
        return self.append((agent_set_ranged_damage_modifier, agent_id, value))
        
    def agent_get_time_elapsed_since_removed(self, destination, agent_id):
        """
        (agent_get_time_elapsed_since_removed, <destination>, <agent_id>),
        Retrieves the number of seconds that have passed since agent's death. Native uses this only for multiplayer to track player's respawns. Can it be used in singleplayer too? 4research.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_time_elapsed_since_removed(destination, agent_id)
        """
        return self.append((agent_get_time_elapsed_since_removed, destination, agent_id))
        
    def agent_refill_wielded_shield_hit_points(self, agent_id):
        """
        (agent_refill_wielded_shield_hit_points, <agent_id>),
        Restores all hit points for the shield the agent is currently wielding.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_refill_wielded_shield_hit_points(agent_id)
        """
        return self.append((agent_refill_wielded_shield_hit_points, agent_id))
        
    def agent_set_invulnerable_shield(self, agent_id, value):
        """
        (agent_set_invulnerable_shield, <agent_id>, <value>),
        Makes the agent invulnerable to any damage (value = 1) or makes him vulnerable again (value = 0).

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_invulnerable_shield(agent_id, value)
        """
        return self.append((agent_set_invulnerable_shield, agent_id, value))
        
    def agent_get_wielded_item(self, destination, agent_id, hand_no):
        """
        (agent_get_wielded_item, <destination>, <agent_id>, <hand_no>),
        Retrieves the item reference that the agent is currently wielding in his right hand (hand_no = 0) or left hand (hand_no = 1). Note that weapons are always wielded in right hand, and shield in left hand. When wielding a two-handed weapon (including bows and crossbows), this operation will return -1 for left hand.

		Args:
			destination (str|int):
			agent_id (str|int):
			hand_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_wielded_item(destination, agent_id, hand_no)
        """
        return self.append((agent_get_wielded_item, destination, agent_id, hand_no))
        
    def agent_get_ammo(self, destination, agent_id, value):
        """
        (agent_get_ammo, <destination>, <agent_id>, <value>),
        Retrieves the current ammo amount agent has for his wielded item (value = 1) or all his items (value = 0).

		Args:
			destination (str|int):
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_ammo(destination, agent_id, value)
        """
        return self.append((agent_get_ammo, destination, agent_id, value))
        
    def agent_get_item_cur_ammo(self, destination, agent_id, slot_no):
        """
        (agent_get_item_cur_ammo, <destination>, <agent_id>, <slot_no>),
        Version 1.153+. Returns remaining ammo for specified agent's item.

		Args:
			destination (str|int):
			agent_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_item_cur_ammo(destination, agent_id, slot_no)
        """
        return self.append((agent_get_item_cur_ammo, destination, agent_id, slot_no))
        
    def agent_refill_ammo(self, agent_id):
        """
        (agent_refill_ammo, <agent_id>),
        Refills all ammo and throwing weapon stacks that the agent has in his equipment.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_refill_ammo(agent_id)
        """
        return self.append((agent_refill_ammo, agent_id))
        
    def agent_set_wielded_item(self, agent_id, item_id):
        """
        (agent_set_wielded_item, <agent_id>, <item_id>),
        Forces the agent to wield the specified item. Agent must have that item in his equipment for this to work. Use item_id = -1 to unwield any currently wielded item.

		Args:
			agent_id (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_wielded_item(agent_id, item_id)
        """
        return self.append((agent_set_wielded_item, agent_id, item_id))
        
    def agent_equip_item(self, agent_id, item_id, weapon_slot_no):
        """
        (agent_equip_item, <agent_id>, <item_id>, [weapon_slot_no]),
        Adds the specified item to agent and forces him to equip it. Optional weapon_slot_no parameter is only used with weapons and will put the newly added item to that slot (range 1..4). If it is omitted with a weapon item, then the agent must have an empty weapon slot for the operation to succeed.

		Args:
			agent_id (str|int):
			item_id (str|int):
			weapon_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_equip_item(agent_id, item_id, weapon_slot_no)
        """
        return self.append((agent_equip_item, agent_id, item_id, weapon_slot_no))
        
    def agent_unequip_item(self, agent_id, item_id, weapon_slot_no):
        """
        (agent_unequip_item, <agent_id>, <item_id>, [weapon_slot_no]),
        Removes the specified item from the agent. Optional parameter weapon_slot_no is in range 1..4 and determines what weapon slot to remove (item_id must still be set correctly).

		Args:
			agent_id (str|int):
			item_id (str|int):
			weapon_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_unequip_item(agent_id, item_id, weapon_slot_no)
        """
        return self.append((agent_unequip_item, agent_id, item_id, weapon_slot_no))
        
    def agent_set_ammo(self, agent_id, item_id, value):
        """
        (agent_set_ammo, <agent_id>, <item_id>, <value>),
        Sets current agent ammo amount to the specified value between 0 and maximum ammo. Not clear what item_id means - weapon item or ammo item? 4research.

		Args:
			agent_id (str|int):
			item_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_ammo(agent_id, item_id, value)
        """
        return self.append((agent_set_ammo, agent_id, item_id, value))
        
    def agent_get_item_slot(self, destination, agent_id, value):
        """
        (agent_get_item_slot, <destination>, <agent_id>, <value>),
        Retrieves item_id for specified agent's slot Possible slot values range in 0..7, order is weapon1, weapon2, weapon3, weapon4, head_armor, body_armor, leg_armor, hand_armor.

		Args:
			destination (str|int):
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_item_slot(destination, agent_id, value)
        """
        return self.append((agent_get_item_slot, destination, agent_id, value))
        
    def agent_get_ammo_for_slot(self, destination, agent_id, slot_no):
        """
        (agent_get_ammo_for_slot, <destination>, <agent_id>, <slot_no>),
        Retrieves the amount of ammo agent has in the referenced slot (range 0..3).

		Args:
			destination (str|int):
			agent_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_ammo_for_slot(destination, agent_id, slot_no)
        """
        return self.append((agent_get_ammo_for_slot, destination, agent_id, slot_no))
        
    def agent_set_no_dynamics(self, agent_id, value):
        """
        (agent_set_no_dynamics, <agent_id>, <value>),
        Makes the agent stand on the spot (value = 1) or move normally (value = 0). When frozen on the spot the agent can still turn around and fight if necessary. Used in Native for the wedding scene.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_no_dynamics(agent_id, value)
        """
        return self.append((agent_set_no_dynamics, agent_id, value))
        
    def agent_get_animation(self, destination, agent_id, body_part):
        """
        (agent_get_animation, <destination>, <agent_id>, <body_part),
        Retrieves current agent animation for specified body part (0 = lower, 1 = upper).

		Args:
			destination (str|int):
			agent_id (str|int):
			body_part (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_animation(destination, agent_id, body_part)
        """
        return self.append((agent_get_animation, destination, agent_id, body_part))
        
    def agent_set_animation(self, agent_id, anim_id, channel_no):
        """
        (agent_set_animation, <agent_id>, <anim_id>, [channel_no]),
        Forces the agent to perform the specified animation. Optional channel_no parameter determines whether upper body (value = 1) or lower body (value = 0, default) is affected by animation.

		Args:
			agent_id (str|int):
			anim_id (str|int):
			channel_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_animation(agent_id, anim_id, channel_no)
        """
        return self.append((agent_set_animation, agent_id, anim_id, channel_no))
        
    def agent_set_stand_animation(self, agent_id, anim_id):
        """
        (agent_set_stand_animation, <agent_id>, <anim_id>),
        Defines the animation that this agent will use when standing still. Does not force the agent into actually doing this animation.

		Args:
			agent_id (str|int):
			anim_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_stand_animation(agent_id, anim_id)
        """
        return self.append((agent_set_stand_animation, agent_id, anim_id))
        
    def agent_set_walk_forward_animation(self, agent_id, anim_id):
        """
        (agent_set_walk_forward_animation, <agent_id>, <anim_id>),
        Defines the animation that this agent will use when walking forward. Only works for NPC agents.

		Args:
			agent_id (str|int):
			anim_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_walk_forward_animation(agent_id, anim_id)
        """
        return self.append((agent_set_walk_forward_animation, agent_id, anim_id))
        
    def agent_set_animation_progress(self, agent_id, value_fixed_point):
        """
        (agent_set_animation_progress, <agent_id>, <value_fixed_point>),
        Allows to skip the agent to a certain point in the animation cycle, as specified by the fixed point value (0..fixed_point_multiplier).

		Args:
			agent_id (str|int):
			value_fixed_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_animation_progress(agent_id, value_fixed_point)
        """
        return self.append((agent_set_animation_progress, agent_id, value_fixed_point))
        
    def agent_ai_set_can_crouch(self, agent_id, value):
        """
        (agent_ai_set_can_crouch, <agent_id>, <value>),
        Version 1.153+. Allows or forbids the agent to crouch. 0 to forbid, 1 to allow.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_set_can_crouch(agent_id, value)
        """
        return self.append((agent_ai_set_can_crouch, agent_id, value))
        
    def agent_get_crouch_mode(self, destination, agent_id):
        """
        (agent_get_crouch_mode, <destination>, <agent_id>),
        Version 1.153+. Retrieves agent's crouch status (1 = crouching, 0 = standing).

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_crouch_mode(destination, agent_id)
        """
        return self.append((agent_get_crouch_mode, destination, agent_id))
        
    def agent_set_crouch_mode(self, agent_id, value):
        """
        (agent_set_crouch_mode, <agent_id>, <value>),
        Version 1.153+. Sets agent's crouch status (1 = crouch, 0 = stand up).

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_crouch_mode(agent_id, value)
        """
        return self.append((agent_set_crouch_mode, agent_id, value))
        
    def agent_get_attached_scene_prop(self, destination, agent_id):
        """
        (agent_get_attached_scene_prop, <destination>, <agent_id>),
        Retrieves the reference to scene prop instance which is attached to the agent, or -1 if there isn't any.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_attached_scene_prop(destination, agent_id)
        """
        return self.append((agent_get_attached_scene_prop, destination, agent_id))
        
    def agent_set_attached_scene_prop(self, agent_id, scene_prop_id):
        """
        (agent_set_attached_scene_prop, <agent_id>, <scene_prop_id>),
        Attaches the specified prop instance to the agent. Used in multiplayer CTF missions to attach flags to players.

		Args:
			agent_id (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_attached_scene_prop(agent_id, scene_prop_id)
        """
        return self.append((agent_set_attached_scene_prop, agent_id, scene_prop_id))
        
    def agent_set_attached_scene_prop_x(self, agent_id, value):
        """
        (agent_set_attached_scene_prop_x, <agent_id>, <value>),
        Offsets the position of the attached scene prop in relation to agent, in centimeters, along the X axis (left/right).

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_attached_scene_prop_x(agent_id, value)
        """
        return self.append((agent_set_attached_scene_prop_x, agent_id, value))
        
    def agent_set_attached_scene_prop_y(self, agent_id, value):
        """
        (agent_set_attached_scene_prop_y, <agent_id>, <value>),
        Offsets the position of the attached scene prop in relation to agent, in centimeters, along the Y axis (backwards/forward).

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_attached_scene_prop_y(agent_id, value)
        """
        return self.append((agent_set_attached_scene_prop_y, agent_id, value))
        
    def agent_set_attached_scene_prop_z(self, agent_id, value):
        """
        (agent_set_attached_scene_prop_z, <agent_id>, <value>),
        Offsets the position of the attached scene prop in relation to agent, in centimeters, along the Z axis (down/up).

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_attached_scene_prop_z(agent_id, value)
        """
        return self.append((agent_set_attached_scene_prop_z, agent_id, value))
        
    def agent_get_bone_position(self, position_no, agent_no, bone_no, local_or_global):
        """
        (agent_get_bone_position, <position_no>, <agent_no>, <bone_no>, [<local_or_global>]),
        Version 1.161+. Returns current position for agent's bone (examine skeleton in openBrf to learn bone numbers). Pass 1 as optional <local_or_global> parameter to retrieve global bone coordinates.

		Args:
			position_no (str|int):
			agent_no (str|int):
			bone_no (str|int):
			local_or_global (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_bone_position(position_no, agent_no, bone_no, local_or_global)
        """
        return self.append((agent_get_bone_position, position_no, agent_no, bone_no, local_or_global))
        
    def agent_ai_set_interact_with_player(self, agent_no, value):
        """
        (agent_ai_set_interact_with_player, <agent_no>, <value>),
        Version 1.165+. Enables or disables agent AI interation with player. Dialog? Combat? 4research.

		Args:
			agent_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_set_interact_with_player(agent_no, value)
        """
        return self.append((agent_ai_set_interact_with_player, agent_no, value))
        
    def agent_set_is_alarmed(self, agent_id, value):
        """
        (agent_set_is_alarmed, <agent_id>, <value>),
        Sets agent's status as alarmed (value = 1) or peaceful (value = 0).

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_is_alarmed(agent_id, value)
        """
        return self.append((agent_set_is_alarmed, agent_id, value))
        
    def agent_clear_relations_with_agents(self, agent_id):
        """
        (agent_clear_relations_with_agents, <agent_id>),
        Clears any agent-to-agent relations for specified agent.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_clear_relations_with_agents(agent_id)
        """
        return self.append((agent_clear_relations_with_agents, agent_id))
        
    def agent_add_relation_with_agent(self, agent_id1, agent_id2):
        """
        (agent_add_relation_with_agent, <agent_id>, <agent_id>, <value>),
        Changes relations between two agents on the scene to enemy (value = -1), neutral (value = 0), ally (value = 1). Note that neutral agents are immune to friendly fire.

		Args:
			agent_id1 (str|int):
			agent_id2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_add_relation_with_agent(agent_id1, agent_id2)
        """
        return self.append((agent_add_relation_with_agent, agent_id1, agent_id2))
        
    def agent_get_number_of_enemies_following(self, destination, agent_id):
        """
        (agent_get_number_of_enemies_following, <destination>, <agent_id>),
        Retrieves the total number of enemies who are currently attacking the specified agents. May be used for AI decision-making.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_number_of_enemies_following(destination, agent_id)
        """
        return self.append((agent_get_number_of_enemies_following, destination, agent_id))
        
    def agent_ai_get_num_cached_enemies(self, destination, agent_no):
        """
        (agent_ai_get_num_cached_enemies, <destination>, <agent_no>),
        Version 1.165+. Returns total number of nearby enemies as has been cached by agent AI. Enemies are numbered from nearest to farthest.

		Args:
			destination (str|int):
			agent_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_get_num_cached_enemies(destination, agent_no)
        """
        return self.append((agent_ai_get_num_cached_enemies, destination, agent_no))
        
    def agent_ai_get_cached_enemy(self, destination, agent_no, cache_index):
        """
        (agent_ai_get_cached_enemy, <destination>, <agent_no>, <cache_index>),
        Version 1.165+. Return agent reference from AI's list of cached enemies, from nearest to farthest. Returns -1 if the cached enemy is not active anymore.

		Args:
			destination (str|int):
			agent_no (str|int):
			cache_index (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_get_cached_enemy(destination, agent_no, cache_index)
        """
        return self.append((agent_ai_get_cached_enemy, destination, agent_no, cache_index))
        
    def agent_get_attack_action(self, destination, agent_id):
        """
        (agent_get_attack_action, <destination>, <agent_id>),
        Retrieves agent's current attack action. Possible values: free = 0, readying_attack = 1, releasing_attack = 2, completing_attack_after_hit = 3, attack_parried = 4, reloading = 5, after_release = 6, cancelling_attack = 7.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_attack_action(destination, agent_id)
        """
        return self.append((agent_get_attack_action, destination, agent_id))
        
    def agent_get_defend_action(self, destination, agent_id):
        """
        (agent_get_defend_action, <destination>, <agent_id>),
        Retrieves agent's current defend action. Possible values: free = 0, parrying = 1, blocking = 2.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_defend_action(destination, agent_id)
        """
        return self.append((agent_get_defend_action, destination, agent_id))
        
    def agent_get_action_dir(self, destination, agent_id):
        """
        (agent_get_action_dir, <destination>, <agent_id>),
        Retrieves the direction of current agent's action. Possible values: invalid = -1, down = 0, right = 1, left = 2, up = 3.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_action_dir(destination, agent_id)
        """
        return self.append((agent_get_action_dir, destination, agent_id))
        
    def agent_set_attack_action(self, agent_id, direction_value, action_value):
        """
        (agent_set_attack_action, <agent_id>, <direction_value>, <action_value>),
        Forces the agent to perform an attack action. Direction value: -2 = cancel any action (1.153+), 0 = thrust, 1 = slashright, 2 = slashleft, 3 = overswing. Action value: 0 = ready and release, 1 = ready and hold.

		Args:
			agent_id (str|int):
			direction_value (str|int):
			action_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_attack_action(agent_id, direction_value, action_value)
        """
        return self.append((agent_set_attack_action, agent_id, direction_value, action_value))
        
    def agent_set_defend_action(self, agent_id, value, duration_in_one_per_thousand_sec):
        """
        (agent_set_defend_action, <agent_id>, <value>, <duration_in_one_per_thousand_sec>),
        Forces the agent to perform a defend action. Possible values: -2 = cancel any action (1.153+), 0 = defend_down, 1 = defend_right, 2 = defend_left, 3 = defend_up. Does time value determine delay, speed or duration? 4research.

		Args:
			agent_id (str|int):
			value (str|int):
			duration_in_one_per_thousand_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_defend_action(agent_id, value, duration_in_one_per_thousand_sec)
        """
        return self.append((agent_set_defend_action, agent_id, value, duration_in_one_per_thousand_sec))
        
    def agent_set_scripted_destination(self, agent_id, position, auto_set_z_to_ground_level, no_rethink):
        """
        (agent_set_scripted_destination, <agent_id>, <position>, [auto_set_z_to_ground_level], [no_rethink]),
        Forces the agent to travel to specified position and stay there until new behavior is set or scripted mode cleared. First optional parameter determines whether the position Z coordinate will be automatically set to ground level (value = 1) or not (value = 0). Second optional parameter added in 1.165 patch, set it to 1 to save resources.

		Args:
			agent_id (str|int):
			position (str|int):
			auto_set_z_to_ground_level (str|int):
			no_rethink (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_scripted_destination(agent_id, position, auto_set_z_to_ground_level, no_rethink)
        """
        return self.append((agent_set_scripted_destination, agent_id, position, auto_set_z_to_ground_level, no_rethink))
        
    def agent_set_scripted_destination_no_attack(self, agent_id, position, auto_set_z_to_ground_level):
        """
        (agent_set_scripted_destination_no_attack, <agent_id>, <position>, <auto_set_z_to_ground_level>),
        Same as above, but the agent will not attack his enemies.

		Args:
			agent_id (str|int):
			position (str|int):
			auto_set_z_to_ground_level (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_scripted_destination_no_attack(agent_id, position, auto_set_z_to_ground_level)
        """
        return self.append((agent_set_scripted_destination_no_attack, agent_id, position, auto_set_z_to_ground_level))
        
    def agent_get_scripted_destination(self, position, agent_id):
        """
        (agent_get_scripted_destination, <position>, <agent_id>),
        Retrieves the position which is defined as agent's scripted destination, if any.

		Args:
			position (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_scripted_destination(position, agent_id)
        """
        return self.append((agent_get_scripted_destination, position, agent_id))
        
    def agent_force_rethink(self, agent_id):
        """
        (agent_force_rethink, <agent_id>),
        Forces the agent to recalculate his current actions after setting him a new scripted destination or changing other factors affecting his behavior.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_force_rethink(agent_id)
        """
        return self.append((agent_force_rethink, agent_id))
        
    def agent_clear_scripted_mode(self, agent_id):
        """
        (agent_clear_scripted_mode, <agent_id>),
        Clears scripting mode from the agent, making him behave as usual again.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_clear_scripted_mode(agent_id)
        """
        return self.append((agent_clear_scripted_mode, agent_id))
        
    def agent_ai_set_always_attack_in_melee(self, agent_id, value):
        """
        (agent_ai_set_always_attack_in_melee, <agent_id>, <value>),
        Forces the agent to continuously attack in melee combat, instead of defending. Used in Native to prevent stalling at the top of the siege ladder. Use value = 0 to clear this mode.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_set_always_attack_in_melee(agent_id, value)
        """
        return self.append((agent_ai_set_always_attack_in_melee, agent_id, value))
        
    def agent_get_simple_behavior(self, destination, agent_id):
        """
        (agent_get_simple_behavior, <destination>, <agent_id>),
        Retrieves agent's current simple behavior (see aisb_* constants in header_mission_templates.py for details).

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_simple_behavior(destination, agent_id)
        """
        return self.append((agent_get_simple_behavior, destination, agent_id))
        
    def agent_ai_get_behavior_target(self, destination, agent_id):
        """
        (agent_ai_get_behavior_target, <destination>, <agent_id>),
        Version 1.153+. UNTESTED. Supposedly returns agent_id which is the target of current agent's behavior.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_get_behavior_target(destination, agent_id)
        """
        return self.append((agent_ai_get_behavior_target, destination, agent_id))
        
    def agent_get_combat_state(self, destination, agent_id):
        """
        (agent_get_combat_state, <destination>, <agent_id>),
        Retrieves agent's current combat state: (please check original one, there's more)

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_combat_state(destination, agent_id)
        """
        return self.append((agent_get_combat_state, destination, agent_id))
        
    def agent_ai_get_move_target(self, destination, agent_id):
        """
        (agent_ai_get_move_target, <destination>, <agent_id>),
        Version 1.153+. UNTESTED. Supposedly returns the enemy agent to whom the agent is currently moving to.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_get_move_target(destination, agent_id)
        """
        return self.append((agent_ai_get_move_target, destination, agent_id))
        
    def agent_get_look_position(self, position, agent_id):
        """
        (agent_get_look_position, <position>, <agent_id>),
        Retrieves the position that the agent is currently looking at.

		Args:
			position (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_look_position(position, agent_id)
        """
        return self.append((agent_get_look_position, position, agent_id))
        
    def agent_set_look_target_position(self, agent_id, position):
        """
        (agent_set_look_target_position, <agent_id>, <position>),
        Forces the agent to look at specified position (turn his head as necessary). Alarmed agents will ignore this.

		Args:
			agent_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_look_target_position(agent_id, position)
        """
        return self.append((agent_set_look_target_position, agent_id, position))
        
    def agent_ai_get_look_target(self, destination, agent_id):
        """
        (agent_ai_get_look_target, <destination>, <agent_id>),
        Version 1.153+. UNTESTED. Supposedly returns agent_id that the agent is currently looking at.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_get_look_target(destination, agent_id)
        """
        return self.append((agent_ai_get_look_target, destination, agent_id))
        
    def agent_set_look_target_agent(self, watcher_agent_id, observed_agent_id):
        """
        (agent_set_look_target_agent, <watcher_agent_id>, <observed_agent_id>),
        Forces the agent to look at specified agent (track his movements). Alarmed agents will ignore this.

		Args:
			watcher_agent_id (str|int):
			observed_agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_look_target_agent(watcher_agent_id, observed_agent_id)
        """
        return self.append((agent_set_look_target_agent, watcher_agent_id, observed_agent_id))
        
    def agent_start_running_away(self, agent_id, position_no):
        """
        (agent_start_running_away, <agent_id>, [<position_no>]),
        Makes the agent flee the battlefield, ignoring everything else and not attacking. If the agent reaches the edge of map in this mode, he will fade out. Optional position_no parameter added in 1.153 and will make the agent flee to specified position instead (pos0 is not allowed and will be ignored).

		Args:
			agent_id (str|int):
			position_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_start_running_away(agent_id, position_no)
        """
        return self.append((agent_start_running_away, agent_id, position_no))
        
    def agent_stop_running_away(self, agent_id):
        """
        (agent_stop_running_away, <agent_id>),
        Cancels fleeing behavior for the agent, turning him back to combat state.

		Args:
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_stop_running_away(agent_id)
        """
        return self.append((agent_stop_running_away, agent_id))
        
    def agent_ai_set_aggressiveness(self, agent_id, value):
        """
        (agent_ai_set_aggressiveness, <agent_id>, <value>),
        Sets the aggressiveness parameter for agent AI to use. Default value is 100. Higher values make agent more aggressive. Actual game effects are not obvious, apparently used to speed up mob aggravation when previously neutral.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_ai_set_aggressiveness(agent_id, value)
        """
        return self.append((agent_ai_set_aggressiveness, agent_id, value))
        
    def agent_set_kick_allowed(self, agent_id, value):
        """
        (agent_set_kick_allowed, <agent_id>, <value>),
        Enables (value = 1) or disables (value = 0) kicking for the specified agent. Only makes sense for player-controlled agents as bots don't know how to kick anyway.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_kick_allowed(agent_id, value)
        """
        return self.append((agent_set_kick_allowed, agent_id, value))
        
    def set_cheer_at_no_enemy(self, value):
        """
        (set_cheer_at_no_enemy, <value>),
        Version 1.153+. Determines whether the agents will cheer when no enemy remain on the map. 0 = do not cheer, 1 = cheer.

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_cheer_at_no_enemy(value)
        """
        return self.append((set_cheer_at_no_enemy, value))
        
    def agent_add_offer_with_timeout(self, agent_id, offerer_agent_id, duration_in_one_per_thousand_sec):
        """
        (agent_add_offer_with_timeout, <agent_id>, <offerer_agent_id>, <duration_in_one_per_thousand_sec>),
        Esoteric stuff. Used in multiplayer duels. Second agent_id is offerer, 0 value for duration is an infinite offer.

		Args:
			agent_id (str|int):
			offerer_agent_id (str|int):
			duration_in_one_per_thousand_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_add_offer_with_timeout(agent_id, offerer_agent_id, duration_in_one_per_thousand_sec)
        """
        return self.append((agent_add_offer_with_timeout, agent_id, offerer_agent_id, duration_in_one_per_thousand_sec))
        
    def agent_check_offer_from_agent(self, agent_id, offerer_agent_id):
        """
        (agent_check_offer_from_agent, <agent_id>, <offerer_agent_id>),
        second agent_id is offerer
		Esoteric stuff. Used in multiplayer duels. Second agent_id is offerer.

		Args:
			agent_id (str|int):
			offerer_agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_check_offer_from_agent(agent_id, offerer_agent_id)
        """
        return self.append((agent_check_offer_from_agent, agent_id, offerer_agent_id))
        
    def agent_get_group(self, destination, agent_id):
        """
        (agent_get_group, <destination>, <agent_id>),
        Retrieves reference to player who is currently the leader of specified bot agent. Only works in multiplayer.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_group(destination, agent_id)
        """
        return self.append((agent_get_group, destination, agent_id))
        
    def agent_set_group(self, agent_id, player_leader_id):
        """
        (agent_set_group, <agent_id>, <player_leader_id>),
        Puts the bot agent under command of specified player. Only works in multiplayer.

		Args:
			agent_id (str|int):
			player_leader_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_group(agent_id, player_leader_id)
        """
        return self.append((agent_set_group, agent_id, player_leader_id))
        
    def agent_get_team(self, destination, agent_id):
        """
        (agent_get_team, <destination>, <agent_id>),
        Retrieves the team that the agent belongs to.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_team(destination, agent_id)
        """
        return self.append((agent_get_team, destination, agent_id))
        
    def agent_set_team(self, agent_id, value):
        """
        (agent_set_team, <agent_id>, <value>),
        Puts the agent to specified team number.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_team(agent_id, value)
        """
        return self.append((agent_set_team, agent_id, value))
        
    def agent_get_class(self, destination, agent_id):
        """
        (agent_get_class, <destination>, <agent_id>),
        Retrieves the agent class (see grc_* constants in header_mission_templates.py for reference). Note this operation returns the troop class that the game divines from troop equipment and flags, ignoring any custom troop class settings.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_class(destination, agent_id)
        """
        return self.append((agent_get_class, destination, agent_id))
        
    def agent_get_division(self, destination, agent_id):
        """
        (agent_get_division, <destination>, <agent_id>),
        Retrieves the agent division (custom troop class number in 0..8 range).

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_division(destination, agent_id)
        """
        return self.append((agent_get_division, destination, agent_id))
        
    def agent_set_division(self, agent_id, value):
        """
        (agent_set_division, <agent_id>, <value>),
        Puts the agent into the specified division. This does not affect agent's troop class. Note that there's a bug in Warband: if an order is issued to agent's original division, the agent will immediately switch back to it's original division number. Therefore, if you want to manipulate agent divisions dynamically during the battle, you need to implement some workarounds for this bug.

		Args:
			agent_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_set_division(agent_id, value)
        """
        return self.append((agent_set_division, agent_id, value))
        
    def team_get_hold_fire_order(self, destination, team_no, division):
        """
        (team_get_hold_fire_order, <destination>, <team_no>, <division>),
        Retrieves current status of hold fire order for specified team/division (see aordr_* constants in header_mission_templates.py for reference).

		Args:
			destination (str|int):
			team_no (str|int):
			division (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_hold_fire_order(destination, team_no, division)
        """
        return self.append((team_get_hold_fire_order, destination, team_no, division))
        
    def team_get_movement_order(self, destination, team_no, division):
        """
        (team_get_movement_order, <destination>, <team_no>, <division>),
        Retrieves current movement orders for specified team/division (see mordr_* constants in header_mission_templates.py for reference).

		Args:
			destination (str|int):
			team_no (str|int):
			division (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_movement_order(destination, team_no, division)
        """
        return self.append((team_get_movement_order, destination, team_no, division))
        
    def team_get_riding_order(self, destination, team_no, division):
        """
        (team_get_riding_order, <destination>, <team_no>, <division>),
        Retrieves current status of riding order for specified team/division (see rordr_* constants in header_mission_templates.py for reference).

		Args:
			destination (str|int):
			team_no (str|int):
			division (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_riding_order(destination, team_no, division)
        """
        return self.append((team_get_riding_order, destination, team_no, division))
        
    def team_get_weapon_usage_order(self, destination, team_no, division):
        """
        (team_get_weapon_usage_order, <destination>, <team_no>, <division>),
        Retrieves current status of weapon usage order for specified team/division (see wordr_* constants in header_mission_templates.py for reference).

		Args:
			destination (str|int):
			team_no (str|int):
			division (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_weapon_usage_order(destination, team_no, division)
        """
        return self.append((team_get_weapon_usage_order, destination, team_no, division))
        
    def team_give_order(self, team_no, division, order_id):
        """
        (team_give_order, <team_no>, <division>, <order_id>),
        Issues an order to specified team/division.

		Args:
			team_no (str|int):
			division (str|int):
			order_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_give_order(team_no, division, order_id)
        """
        return self.append((team_give_order, team_no, division, order_id))
        
    def team_set_order_position(self, team_no, division, position):
        """
        (team_set_order_position, <team_no>, <division>, <position>),
        Defines the position for specified team/division when currently issued order requires one.

		Args:
			team_no (str|int):
			division (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_order_position(team_no, division, position)
        """
        return self.append((team_set_order_position, team_no, division, position))
        
    def team_get_leader(self, destination, team_no):
        """
        (team_get_leader, <destination>, <team_no>),
        Retrieves the reference to the agent who is the leader of specified team.

		Args:
			destination (str|int):
			team_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_leader(destination, team_no)
        """
        return self.append((team_get_leader, destination, team_no))
        
    def team_set_leader(self, team_no, new_leader_agent_id):
        """
        (team_set_leader, <team_no>, <new_leader_agent_id>),
        Sets the agent as the new leader of specified team.

		Args:
			team_no (str|int):
			new_leader_agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_leader(team_no, new_leader_agent_id)
        """
        return self.append((team_set_leader, team_no, new_leader_agent_id))
        
    def team_get_order_position(self, position, team_no, division):
        """
        (team_get_order_position, <position>, <team_no>, <division>),
        Retrieves position which is used for specified team/division current orders.

		Args:
			position (str|int):
			team_no (str|int):
			division (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_order_position(position, team_no, division)
        """
        return self.append((team_get_order_position, position, team_no, division))
        
    def team_set_order_listener(self, team_no, division, add_to_listeners):
        """
        (team_set_order_listener, <team_no>, <division>, [add_to_listeners]),
        Set the specified division as the one which will be following orders issued by the player (assuming the player is on the same team). If optional parameter add_to_listeners is greater than 0, then the operation will instead *add* specified division to order listeners. If division number is -1, then list of order listeners is cleared. If division number is 9, then all divisions will listen to player's orders.

		Args:
			team_no (str|int):
			division (str|int):
			add_to_listeners (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_order_listener(team_no, division, add_to_listeners)
        """
        return self.append((team_set_order_listener, team_no, division, add_to_listeners))
        
    def team_set_relation(self, team_no, team_no_2, value):
        """
        (team_set_relation, <team_no>, <team_no_2>, <value>),
        Sets relations between two teams. Possible values: enemy (-1), neutral (0) and friendly (1).

		Args:
			team_no (str|int):
			team_no_2 (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_relation(team_no, team_no_2, value)
        """
        return self.append((team_set_relation, team_no, team_no_2, value))
        
    def store_remaining_team_no(self, destination):
        """
        (store_remaining_team_no, <destination>),
        Retrieves the number of the last remaining team. Currently not used in Native, possibly deprecated.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_remaining_team_no(destination)
        """
        return self.append((store_remaining_team_no, destination))
        
    def team_get_gap_distance(self, destination, team_no, sub_class):
        """
        (team_get_gap_distance, <destination>, <team_no>, <sub_class>),
        Version 1.153+. UNTESTED. Supposedly returns average gap between troops of a specified team/class (depends on how many Stand Closer/Spread Out orders were given).

		Args:
			destination (str|int):
			team_no (str|int):
			sub_class (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_gap_distance(destination, team_no, sub_class)
        """
        return self.append((team_get_gap_distance, destination, team_no, sub_class))
        
    def store_enemy_count(self, destination):
        """
        (store_enemy_count, <destination>),
        No longer used in Native. Apparently stores total number of active enemy agents. Possibly deprecated. 4research.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_enemy_count(destination)
        """
        return self.append((store_enemy_count, destination))
        
    def store_friend_count(self, destination):
        """
        (store_friend_count, <destination>),
        No longer used in Native. Apparently stores total number of active friendly agents. Possibly deprecated. 4research.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_friend_count(destination)
        """
        return self.append((store_friend_count, destination))
        
    def store_ally_count(self, destination):
        """
        (store_ally_count, <destination>),
        No longer used in Native. Apparently stores total number of active allied agents (how is it different from friends?). Possibly deprecated. 4research.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_ally_count(destination)
        """
        return self.append((store_ally_count, destination))
        
    def store_defender_count(self, destination):
        """
        (store_defender_count, <destination>),
        No longer used in Native. Apparently stores total number of active agents on defender's side. Possibly deprecated. 4research.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_defender_count(destination)
        """
        return self.append((store_defender_count, destination))
        
    def store_attacker_count(self, destination):
        """
        (store_attacker_count, <destination>),
        No longer used in Native. Apparently stores total number of active agents on attacker's side. Possibly deprecated. 4research.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_attacker_count(destination)
        """
        return self.append((store_attacker_count, destination))
        
    def store_normalized_team_count(self, destination, team_no):
        """
        (store_normalized_team_count, <destination>, <team_no>),
        Stores the number of agents belonging to specified team, normalized according to battle_size and advantage. Commonly used to calculate advantage and possibly reinforcement wave sizes.

		Args:
			destination (str|int):
			team_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> store_normalized_team_count(destination, team_no)
        """
        return self.append((store_normalized_team_count, destination, team_no))
        
    def is_presentation_active(self, presentation_id):
        """
        (is_presentation_active, <presentation_id),
        Checks that the specified presentation is currently running.

		Args:
			presentation_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> is_presentation_active(presentation_id)
        """
        return self.append((is_presentation_active, presentation_id))
        
    def start_presentation(self, presentation_id):
        """
        (start_presentation, <presentation_id>),
        Starts the specified presentation.

		Args:
			presentation_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_presentation(presentation_id)
        """
        return self.append((start_presentation, presentation_id))
        
    def start_background_presentation(self, presentation_id):
        """
        (start_background_presentation, <presentation_id>),
        Apparently allows you to start a presentation in background but stay in the menu. 4research.

		Args:
			presentation_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_background_presentation(presentation_id)
        """
        return self.append((start_background_presentation, presentation_id))
        
    def presentation_set_duration(self, duration_in_one_per_hundred_sec):
        """
        (presentation_set_duration, <duration_in_one_per_hundred_sec>),
        Sets presentation duration time, in 1/100th of second. Must be called when a presentation is active. If several presentations are active, duration will be set for all of them.

		Args:
			duration_in_one_per_hundred_sec (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> presentation_set_duration(duration_in_one_per_hundred_sec)
        """
        return self.append((presentation_set_duration, duration_in_one_per_hundred_sec))
        
    def create_text_overlay(self, destination, string_id):
        """
        (create_text_overlay, <destination>, <string_id>),
        Creates a text label overlay and returns it's overlay_id.

		Args:
			destination (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_text_overlay(destination, string_id)
        """
        return self.append((create_text_overlay, destination, string_id))
        
    def create_mesh_overlay(self, destination, mesh_id):
        """
        (create_mesh_overlay, <destination>, <mesh_id>),
        Creates a mesh overlay and returns it's overlay_id.

		Args:
			destination (str|int):
			mesh_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_mesh_overlay(destination, mesh_id)
        """
        return self.append((create_mesh_overlay, destination, mesh_id))
        
    def create_mesh_overlay_with_item_id(self, destination, item_id):
        """
        (create_mesh_overlay_with_item_id, <destination>, <item_id>),
        Creates a mesh overlay, using the specified item mesh. Returns overlay_id.

		Args:
			destination (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_mesh_overlay_with_item_id(destination, item_id)
        """
        return self.append((create_mesh_overlay_with_item_id, destination, item_id))
        
    def create_mesh_overlay_with_tableau_material(self, destination, mesh_id, tableau_material_id, value):
        """
        (create_mesh_overlay_with_tableau_material, <destination>, <mesh_id>, <tableau_material_id>, <value>),
        Creates a mesh overlay, using the specified tableau_material. When mesh_id = -1, it is generated automatically. Value is passed as the parameter for tableau_material script. Returns overlay_id.

		Args:
			destination (str|int):
			mesh_id (str|int):
			tableau_material_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_mesh_overlay_with_tableau_material(destination, mesh_id, tableau_material_id, value)
        """
        return self.append((create_mesh_overlay_with_tableau_material, destination, mesh_id, tableau_material_id, value))
        
    def create_button_overlay(self, destination, string_id):
        """
        (create_button_overlay, <destination>, <string_id>),
        Creates a generic button overlay and returns it's overlay_id. The only difference between this and subsequent two operations is that they use different button meshes.

		Args:
			destination (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_button_overlay(destination, string_id)
        """
        return self.append((create_button_overlay, destination, string_id))
        
    def create_game_button_overlay(self, destination, string_id):
        """
        (create_game_button_overlay, <destination>, <string_id>),
        Creates a game button overlay and returns it's overlay_id.

		Args:
			destination (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_game_button_overlay(destination, string_id)
        """
        return self.append((create_game_button_overlay, destination, string_id))
        
    def create_in_game_button_overlay(self, destination, string_id):
        """
        (create_in_game_button_overlay, <destination>, <string_id>),
        Creates an in-game button overlay and returns it's overlay_id.

		Args:
			destination (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_in_game_button_overlay(destination, string_id)
        """
        return self.append((create_in_game_button_overlay, destination, string_id))
        
    def create_image_button_overlay(self, mesh_id1, mesh_id2):
        """
        (create_image_button_overlay, <destination>, <mesh_id>, <mesh_id>),
        Creates an image button, using two meshes for normal (1st mesh) and pressed (2nd mesh) status. Button does not have a textual label. Returns button overlay_id.

		Args:
			mesh_id1 (str|int):
			mesh_id2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_image_button_overlay(mesh_id1, mesh_id2)
        """
        return self.append((create_image_button_overlay, mesh_id1, mesh_id2))
        
    def create_image_button_overlay_with_tableau_material(self, destination, mesh_id, tableau_material_id, value):
        """
        (create_image_button_overlay_with_tableau_material, <destination>, <mesh_id>, <tableau_material_id>, <value>),
        Creates an image button from the specified mesh, using tableau_material as the image. When mesh = -1, it is generated automatically. Value is passed as the parameter to the tableau_material script. Returns overlay_id.

		Args:
			destination (str|int):
			mesh_id (str|int):
			tableau_material_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_image_button_overlay_with_tableau_material(destination, mesh_id, tableau_material_id, value)
        """
        return self.append((create_image_button_overlay_with_tableau_material, destination, mesh_id, tableau_material_id, value))
        
    def create_slider_overlay(self, destination, min_value, max_value):
        """
        (create_slider_overlay, <destination>, <min_value>, <max_value>),
        Creates horizontal slider overlay, with positions of the slider varying between min and max values. Current value of the slider can be changed with (overlay_set_val). Returns slider's overlay_id.

		Args:
			destination (str|int):
			min_value (str|int):
			max_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_slider_overlay(destination, min_value, max_value)
        """
        return self.append((create_slider_overlay, destination, min_value, max_value))
        
    def create_progress_overlay(self, destination, min_value, max_value):
        """
        (create_progress_overlay, <destination>, <min_value>, <max_value>),
        Creates progress bar overlay, with positions of the bar varying between min and max values. Current value of the progress bar can be changed with (overlay_set_val). Returns bar's overlay_id.

		Args:
			destination (str|int):
			min_value (str|int):
			max_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_progress_overlay(destination, min_value, max_value)
        """
        return self.append((create_progress_overlay, destination, min_value, max_value))
        
    def create_number_box_overlay(self, destination, min_value, max_value):
        """
        (create_number_box_overlay, <destination>, <min_value>, <max_value>),
        Creates a number box overlay (a small field for numeric value and small increase/decrease buttons to the right) with specified min and max values. Returns number box overlay_id.

		Args:
			destination (str|int):
			min_value (str|int):
			max_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_number_box_overlay(destination, min_value, max_value)
        """
        return self.append((create_number_box_overlay, destination, min_value, max_value))
        
    def create_text_box_overlay(self, destination):
        """
        (create_text_box_overlay, <destination>),
        Apparently deprecated. No longer used in Native.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_text_box_overlay(destination)
        """
        return self.append((create_text_box_overlay, destination))
        
    def create_simple_text_box_overlay(self, destination):
        """
        (create_simple_text_box_overlay, <destination>),
        Creates a text field overlay, where user can enter any text. Returns text field's overlay_id. Text contents of the field can be retrieved from s0 trigger in ti_on_presentation_event_state_change event for the text field.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_simple_text_box_overlay(destination)
        """
        return self.append((create_simple_text_box_overlay, destination))
        
    def create_check_box_overlay(self, destination, checkbox_off_mesh, checkbox_on_mesh):
        """
        (create_check_box_overlay, <destination>, <checkbox_off_mesh>, <checkbox_on_mesh>),
        Creates a checkbox overlay. Returns checkbox overlay_id.

		Args:
			destination (str|int):
			checkbox_off_mesh (str|int):
			checkbox_on_mesh (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_check_box_overlay(destination, checkbox_off_mesh, checkbox_on_mesh)
        """
        return self.append((create_check_box_overlay, destination, checkbox_off_mesh, checkbox_on_mesh))
        
    def create_listbox_overlay(self, destination, string, value):
        """
        (create_listbox_overlay, <destination>, <string>, <value>),
        Creates a listbox overlay. Individual items can be added with (overlay_add_item) and index of currently selected item can be set with (overlay_set_val). Returns listbox overlay_id. Importance of later two parameters unclear (default text&value?). 4research.

		Args:
			destination (str|int):
			string (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_listbox_overlay(destination, string, value)
        """
        return self.append((create_listbox_overlay, destination, string, value))
        
    def create_combo_label_overlay(self, destination):
        """
        (create_combo_label_overlay, <destination>),
        Creates a combo label overlay. Looks like plain text label. Individual items can be added with (overlay_add_item) and currently selected item can be set with (overlay_set_val). Returns combo block's overlay_id.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_combo_label_overlay(destination)
        """
        return self.append((create_combo_label_overlay, destination))
        
    def create_combo_button_overlay(self, destination):
        """
        (create_combo_button_overlay, <destination>),
        Creates a combo button overlay. For example see "Screen Resolution" dropdown in Settings menu. Individual items can be added with (overlay_add_item) and currently selected item can be set with (overlay_set_val). Returns combo block's overlay_id.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> create_combo_button_overlay(destination)
        """
        return self.append((create_combo_button_overlay, destination))
        
    def overlay_add_item(self, overlay_id, string_id):
        """
        (overlay_add_item, <overlay_id>, <string_id>),
        Adds an item to the listbox or combobox. Items are indexed from 0. Note the order in which items appear in the dropdown is reverse to the order in which they're added.

		Args:
			overlay_id (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_add_item(overlay_id, string_id)
        """
        return self.append((overlay_add_item, overlay_id, string_id))
        
    def set_container_overlay(self, overlay_id):
        """
        (set_container_overlay, <overlay_id>),
        Defines the specified overlay as the container. All subsequently created overlays will be placed inside the container, and their coordinates will be based on container's position. All containers with their contents will be displayed *above* any non-container overlays. Use -1 to stop placing overlays to current container and resume normal behavior.

		Args:
			overlay_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_container_overlay(overlay_id)
        """
        return self.append((set_container_overlay, overlay_id))
        
    def overlay_set_container_overlay(self, overlay_id, container_overlay_id):
        """
        (overlay_set_container_overlay, <overlay_id>, <container_overlay_id>),
        Allows you to put one overlay into a container, or remove it from container (if container_overlay_id = -1) without setting current overlay. May be unreliable.

		Args:
			overlay_id (str|int):
			container_overlay_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_container_overlay(overlay_id, container_overlay_id)
        """
        return self.append((overlay_set_container_overlay, overlay_id, container_overlay_id))
        
    def overlay_get_position(self, position, overlay_id):
        """
        (overlay_get_position, <position>, <overlay_id>),
        Retrieves overlay current position to specified position trigger, using position's X and Y coordinates. Note that the screen size in Warband is (1.00,0.75), further modified by fixed point multiplier.

		Args:
			position (str|int):
			overlay_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_get_position(position, overlay_id)
        """
        return self.append((overlay_get_position, position, overlay_id))
        
    def overlay_set_val(self, overlay_id, value):
        """
        (overlay_set_val, <overlay_id>, <value>),
        Sets the value of the overlays which have numeric values.

		Args:
			overlay_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_val(overlay_id, value)
        """
        return self.append((overlay_set_val, overlay_id, value))
        
    def overlay_set_text(self, overlay_id, string_id):
        """
        (overlay_set_text, <overlay_id>, <string_id>),
        Changes the overlay text (if it has any). Works for labels, text fields, buttons with text labels...

		Args:
			overlay_id (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_text(overlay_id, string_id)
        """
        return self.append((overlay_set_text, overlay_id, string_id))
        
    def overlay_set_boundaries(self, overlay_id, min_value, max_value):
        """
        (overlay_set_boundaries, <overlay_id>, <min_value>, <max_value>),
        Changes the value boundaries for the overlays that have them.

		Args:
			overlay_id (str|int):
			min_value (str|int):
			max_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_boundaries(overlay_id, min_value, max_value)
        """
        return self.append((overlay_set_boundaries, overlay_id, min_value, max_value))
        
    def overlay_set_position(self, overlay_id, position):
        """
        (overlay_set_position, <overlay_id>, <position>),
        Sets the overlay position on the screen, using position's X and Y coordinates. Note that the screen size in Warband is (1.00,0.75), further modified by fixed point multiplier.

		Args:
			overlay_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_position(overlay_id, position)
        """
        return self.append((overlay_set_position, overlay_id, position))
        
    def overlay_set_size(self, overlay_id, position):
        """
        (overlay_set_size, <overlay_id>, <position>),
        Sets the overlay size, using position's X and Y coordinates. Note that the screen size in Warband is (1.00,0.75), further modified by fixed point multiplier. Also see (overlay_set_area_size).

		Args:
			overlay_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_size(overlay_id, position)
        """
        return self.append((overlay_set_size, overlay_id, position))
        
    def overlay_set_area_size(self, overlay_id, position):
        """
        (overlay_set_area_size, <overlay_id>, <position>),
        Defines the actual area on the screen used to display the overlay. If it's size is greater than area size, it will create a scrollable area with appropriate scrollbars. Can be used to create scrollable areas for large text, or scrollable containers with many children elements (see Host Game screen for a typical example).

		Args:
			overlay_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_area_size(overlay_id, position)
        """
        return self.append((overlay_set_area_size, overlay_id, position))
        
    def overlay_set_additional_render_height(self, overlay_id, height_adder):
        """
        (overlay_set_additional_render_height, <overlay_id>, <height_adder>),
        Version 1.153+. Effects uncertain. 4research.

		Args:
			overlay_id (str|int):
			height_adder (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_additional_render_height(overlay_id, height_adder)
        """
        return self.append((overlay_set_additional_render_height, overlay_id, height_adder))
        
    def overlay_animate_to_position(self, overlay_id, duration_in_one_per_thousand_sec, position):
        """
        (overlay_animate_to_position, <overlay_id>, <duration_in_one_per_thousand_sec>, <position>),
        Moves overlay to specified position during a specified timeframe, specified in 1/1000th of second.

		Args:
			overlay_id (str|int):
			duration_in_one_per_thousand_sec (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_animate_to_position(overlay_id, duration_in_one_per_thousand_sec, position)
        """
        return self.append((overlay_animate_to_position, overlay_id, duration_in_one_per_thousand_sec, position))
        
    def overlay_animate_to_size(self, overlay_id, duration_in_one_per_thousand_sec, position):
        """
        (overlay_animate_to_size, <overlay_id>, <duration_in_one_per_thousand_sec>, <position>),
        Changes overlay size to specified value during a specified timeframe, specified in 1/1000th of second.

		Args:
			overlay_id (str|int):
			duration_in_one_per_thousand_sec (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_animate_to_size(overlay_id, duration_in_one_per_thousand_sec, position)
        """
        return self.append((overlay_animate_to_size, overlay_id, duration_in_one_per_thousand_sec, position))
        
    def overlay_set_mesh_rotation(self, overlay_id, position):
        """
        (overlay_set_mesh_rotation, <overlay_id>, <position>),
        Despite the name, works with any overlay, allowing you to put it on the screen in rotated position. To determine the angles, position's rotation values are used (not coordinates!). Usually you will want to only use rotation around Z axis (which results in clockwise or anti-clockwise rotation as seen by user). Note that rotating overlays which are placed inside a container may cause strange results, so some trial and error will be necessary in such situation.

		Args:
			overlay_id (str|int):
			position (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_mesh_rotation(overlay_id, position)
        """
        return self.append((overlay_set_mesh_rotation, overlay_id, position))
        
    def overlay_set_material(self, overlay_id, string_no):
        """
        (overlay_set_material, <overlay_id>, <string_no>),
        Version 1.161+. Replaces the material used for rendering specified overlay.

		Args:
			overlay_id (str|int):
			string_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_material(overlay_id, string_no)
        """
        return self.append((overlay_set_material, overlay_id, string_no))
        
    def overlay_set_color(self, overlay_id, color):
        """
        (overlay_set_color, <overlay_id>, <color>),
        Changes the overlay color (hexadecimal value 0xRRGGBB). May not work with some overlay types.

		Args:
			overlay_id (str|int):
			color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_color(overlay_id, color)
        """
        return self.append((overlay_set_color, overlay_id, color))
        
    def overlay_set_alpha(self, overlay_id, alpha):
        """
        (overlay_set_alpha, <overlay_id>, <alpha>),
        Changes the overlay alpha (hexadecimal value in 0x00..0xFF range). May not work with some overlay types.

		Args:
			overlay_id (str|int):
			alpha (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_alpha(overlay_id, alpha)
        """
        return self.append((overlay_set_alpha, overlay_id, alpha))
        
    def overlay_set_hilight_color(self, overlay_id, color):
        """
        (overlay_set_hilight_color, <overlay_id>, <color>),
        Highlights the overlay with specified color. May not work with some overlay types.

		Args:
			overlay_id (str|int):
			color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_hilight_color(overlay_id, color)
        """
        return self.append((overlay_set_hilight_color, overlay_id, color))
        
    def overlay_set_hilight_alpha(self, overlay_id, alpha):
        """
        (overlay_set_hilight_alpha, <overlay_id>, <alpha>),
        Highlights the overlay with specified alpha. May not work with some overlay types.

		Args:
			overlay_id (str|int):
			alpha (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_hilight_alpha(overlay_id, alpha)
        """
        return self.append((overlay_set_hilight_alpha, overlay_id, alpha))
        
    def overlay_animate_to_color(self, overlay_id, duration_in_one_per_thousand_sec, color):
        """
        (overlay_animate_to_color, <overlay_id>, <duration_in_one_per_thousand_sec>, <color>),
        Changes overlay's color during a specified timeframe, specified in 1/000th of second.

		Args:
			overlay_id (str|int):
			duration_in_one_per_thousand_sec (str|int):
			color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_animate_to_color(overlay_id, duration_in_one_per_thousand_sec, color)
        """
        return self.append((overlay_animate_to_color, overlay_id, duration_in_one_per_thousand_sec, color))
        
    def overlay_animate_to_alpha(self, overlay_id, duration_in_one_per_thousand_sec, color):
        """
        (overlay_animate_to_alpha, <overlay_id>, <duration_in_one_per_thousand_sec>, <color>),
        Changes overlay's alpha during a specified timeframe, specified in 1/000th of second.

		Args:
			overlay_id (str|int):
			duration_in_one_per_thousand_sec (str|int):
			color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_animate_to_alpha(overlay_id, duration_in_one_per_thousand_sec, color)
        """
        return self.append((overlay_animate_to_alpha, overlay_id, duration_in_one_per_thousand_sec, color))
        
    def overlay_animate_to_highlight_color(self, overlay_id, duration_in_one_per_thousand_sec, color):
        """
        (overlay_animate_to_highlight_color, <overlay_id>, <duration_in_one_per_thousand_sec>, <color>),
        Highlights overlay to specified color during a specified timeframe, specified in 1/000th of second.

		Args:
			overlay_id (str|int):
			duration_in_one_per_thousand_sec (str|int):
			color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_animate_to_highlight_color(overlay_id, duration_in_one_per_thousand_sec, color)
        """
        return self.append((overlay_animate_to_highlight_color, overlay_id, duration_in_one_per_thousand_sec, color))
        
    def overlay_animate_to_highlight_alpha(self, overlay_id, duration_in_one_per_thousand_sec, color):
        """
        (overlay_animate_to_highlight_alpha, <overlay_id>, <duration_in_one_per_thousand_sec>, <color>),
        Highlights overlay to specified alpha during a specified timeframe, specified in 1/000th of second.

		Args:
			overlay_id (str|int):
			duration_in_one_per_thousand_sec (str|int):
			color (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_animate_to_highlight_alpha(overlay_id, duration_in_one_per_thousand_sec, color)
        """
        return self.append((overlay_animate_to_highlight_alpha, overlay_id, duration_in_one_per_thousand_sec, color))
        
    def overlay_set_display(self, overlay_id, value):
        """
        (overlay_set_display, <overlay_id>, <value>),
        Shows (value = 1) or hides (value = 0) the specified overlay.

		Args:
			overlay_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_display(overlay_id, value)
        """
        return self.append((overlay_set_display, overlay_id, value))
        
    def overlay_obtain_focus(self, overlay_id):
        """
        (overlay_obtain_focus, <overlay_id>),
        Makes the specified overlay obtain input focus. Only works for text fields.

		Args:
			overlay_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_obtain_focus(overlay_id)
        """
        return self.append((overlay_obtain_focus, overlay_id))
        
    def overlay_set_tooltip(self, overlay_id, string_id):
        """
        (overlay_set_tooltip, <overlay_id>, <string_id>),
        Defines a text which will be displayed as a tooltip when mouse pointer will hover over the specified overlay. Unreliable, always test how it works.

		Args:
			overlay_id (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> overlay_set_tooltip(overlay_id, string_id)
        """
        return self.append((overlay_set_tooltip, overlay_id, string_id))
        
    def show_item_details(self, item_id, position, price_multiplier_percentile):
        """
        (show_item_details, <item_id>, <position>, <price_multiplier_percentile>),
        Shows a popup box at the specified position, containing standard game information for the specified item. Last parameter determines price percentile multiplier. Multiplier value of 100 will display item standard price, value of 0 will display "Default Item" instead of price (used in multiplayer equipment selection presentation).

		Args:
			item_id (str|int):
			position (str|int):
			price_multiplier_percentile (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> show_item_details(item_id, position, price_multiplier_percentile)
        """
        return self.append((show_item_details, item_id, position, price_multiplier_percentile))
        
    def show_item_details_with_modifier(self, item_id, item_modifier, position, price_multiplier_percentile):
        """
        (show_item_details_with_modifier, <item_id>, <item_modifier>, <position>, <price_multiplier_percentile>),
        Same as above, but displays stats and price information for an item with a modifier.

		Args:
			item_id (str|int):
			item_modifier (str|int):
			position (str|int):
			price_multiplier_percentile (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> show_item_details_with_modifier(item_id, item_modifier, position, price_multiplier_percentile)
        """
        return self.append((show_item_details_with_modifier, item_id, item_modifier, position, price_multiplier_percentile))
        
    def close_item_details(self):
        """
        (close_item_details),
        Closes the item details popup box.

        Returns:
            TupleBuilder: self

        Example:
            >>> close_item_details(item_id, item_modifier, position, price_multiplier_percentile)
        """
        return self.append((close_item_details))
        
    def show_troop_details(self, troop_id, position, troop_price):
        """
        (show_troop_details, <troop_id>, <position>, <troop_price>),
        Version 1.153+. Supposedly displays a popup with troop information at specified place. 4research.

		Args:
			troop_id (str|int):
			position (str|int):
			troop_price (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> show_troop_details(troop_id, position, troop_price)
        """
        return self.append((show_troop_details, troop_id, position, troop_price))
        
    def player_is_active(self, player_id):
        """
        (player_is_active, <player_id>),
        Checks that the specified player is active (i.e. connected to server).

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_is_active(player_id)
        """
        return self.append((player_is_active, player_id))
        
    def multiplayer_is_server(self):
        """
        (multiplayer_is_server),
        Checks that the code is running on multiplayer server. Operation will fail on client machines or in singleplayer mode.

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_is_server(player_id)
        """
        return self.append((multiplayer_is_server))
        
    def multiplayer_is_dedicated_server(self):
        """
        (multiplayer_is_dedicated_server),
        Checks that the code is running on dedicated multiplayer server machine.

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_is_dedicated_server(player_id)
        """
        return self.append((multiplayer_is_dedicated_server))
        
    def game_in_multiplayer_mode(self):
        """
        (game_in_multiplayer_mode),
        Checks that the game is running in multiplayer mode.

        Returns:
            TupleBuilder: self

        Example:
            >>> game_in_multiplayer_mode(player_id)
        """
        return self.append((game_in_multiplayer_mode))
        
    def player_is_admin(self, player_id):
        """
        (player_is_admin, <player_id>),
        Checks that the specified player has administrative rights.

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_is_admin(player_id)
        """
        return self.append((player_is_admin, player_id))
        
    def player_is_busy_with_menus(self, player_id):
        """
        (player_is_busy_with_menus, <player_id>),
        Undocumented. Educated guess is it's true when player is running a presentation without prsntf_read_only flag.

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_is_busy_with_menus(player_id)
        """
        return self.append((player_is_busy_with_menus, player_id))
        
    def player_item_slot_is_picked_up(self, player_id, item_slot_no):
        """
        (player_item_slot_is_picked_up, <player_id>, <item_slot_no>),
        Checks that the specified player's equipment slot contains an item that the player has picked up from ground.

		Args:
			player_id (str|int):
			item_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_item_slot_is_picked_up(player_id, item_slot_no)
        """
        return self.append((player_item_slot_is_picked_up, player_id, item_slot_no))
        
    def player_set_slot(self, player_id, slot_no, value):
        """
        (player_set_slot, <player_id>, <slot_no>, <value>),
        

		Args:
			player_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_slot(player_id, slot_no, value)
        """
        return self.append((player_set_slot, player_id, slot_no, value))
        
    def player_get_slot(self, destination, player_id, slot_no):
        """
        (player_get_slot, <destination>, <player_id>, <slot_no>),
        

		Args:
			destination (str|int):
			player_id (str|int):
			slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_slot(destination, player_id, slot_no)
        """
        return self.append((player_get_slot, destination, player_id, slot_no))
        
    def player_slot_eq(self, player_id, slot_no, value):
        """
        (player_slot_eq, <player_id>, <slot_no>, <value>),
        

		Args:
			player_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_slot_eq(player_id, slot_no, value)
        """
        return self.append((player_slot_eq, player_id, slot_no, value))
        
    def player_slot_ge(self, player_id, slot_no, value):
        """
        (player_slot_ge, <player_id>, <slot_no>, <value>),
        

		Args:
			player_id (str|int):
			slot_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_slot_ge(player_id, slot_no, value)
        """
        return self.append((player_slot_ge, player_id, slot_no, value))
        
    def send_message_to_url(self, string_id, encode_url):
        """
        (send_message_to_url, <string_id>, <encode_url>),
        Sends an HTTP request. Response from that URL will be returned to "script_game_receive_url_response". Parameter <encode_url> is optional and effects are unclear. Supposedly it's equivalent of calling (str_encode_url) on the first parameter which doesn't make sense for me.

		Args:
			string_id (str|int):
			encode_url (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> send_message_to_url(string_id, encode_url)
        """
        return self.append((send_message_to_url, string_id, encode_url))
        
    def multiplayer_send_message_to_server(self, message_type):
        """
        (multiplayer_send_message_to_server, <message_type>),
        Multiplayer client operation. Send a simple message (only message code, no data) to game server.

		Args:
			message_type (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_message_to_server(message_type)
        """
        return self.append((multiplayer_send_message_to_server, message_type))
        
    def multiplayer_send_int_to_server(self, message_type, value):
        """
        (multiplayer_send_int_to_server, <message_type>, <value>),
        Multiplayer client operation. Send a message with a single extra integer value to game server.

		Args:
			message_type (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_int_to_server(message_type, value)
        """
        return self.append((multiplayer_send_int_to_server, message_type, value))
        
    def multiplayer_send_2_int_to_server(self, value1, value2):
        """
        (multiplayer_send_2_int_to_server, <message_type>, <value>, <value>),
        Same as (multiplayer_send_int_to_server), but two integer values are sent.

		Args:
			value1 (str|int):
			value2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_2_int_to_server(value1, value2)
        """
        return self.append((multiplayer_send_2_int_to_server, value1, value2))
        
    def multiplayer_send_3_int_to_server(self, value1, value2, value3):
        """
        (multiplayer_send_3_int_to_server, <message_type>, <value>, <value>, <value>),
        Same as (multiplayer_send_int_to_server), but three integer values are sent.

		Args:
			value1 (str|int):
			value2 (str|int):
			value3 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_3_int_to_server(value1, value2, value3)
        """
        return self.append((multiplayer_send_3_int_to_server, value1, value2, value3))
        
    def multiplayer_send_4_int_to_server(self, value1, value2, value3, value4):
        """
        (multiplayer_send_4_int_to_server, <message_type>, <value>, <value>, <value>, <value>),
        Same as (multiplayer_send_int_to_server), but four integer values are sent.

		Args:
			value1 (str|int):
			value2 (str|int):
			value3 (str|int):
			value4 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_4_int_to_server(value1, value2, value3, value4)
        """
        return self.append((multiplayer_send_4_int_to_server, value1, value2, value3, value4))
        
    def multiplayer_send_string_to_server(self, message_type, string_id):
        """
        (multiplayer_send_string_to_server, <message_type>, <string_id>),
        Multiplayer client operation. Send a message with a string value to game server.

		Args:
			message_type (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_string_to_server(message_type, string_id)
        """
        return self.append((multiplayer_send_string_to_server, message_type, string_id))
        
    def multiplayer_send_message_to_player(self, player_id, message_type):
        """
        (multiplayer_send_message_to_player, <player_id>, <message_type>),
        Multiplayer server operation. Send a simple message (only message code, no data) to one of connected players.

		Args:
			player_id (str|int):
			message_type (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_message_to_player(player_id, message_type)
        """
        return self.append((multiplayer_send_message_to_player, player_id, message_type))
        
    def multiplayer_send_int_to_player(self, player_id, message_type, value):
        """
        (multiplayer_send_int_to_player, <player_id>, <message_type>, <value>),
        Multiplayer server operation. Send a message with a single extra integer value to one of connected players.

		Args:
			player_id (str|int):
			message_type (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_int_to_player(player_id, message_type, value)
        """
        return self.append((multiplayer_send_int_to_player, player_id, message_type, value))
        
    def multiplayer_send_2_int_to_player(self, value1, value2):
        """
        (multiplayer_send_2_int_to_player, <player_id>, <message_type>, <value>, <value>),
        Same as (multiplayer_send_int_to_player), but two integer values are sent.

		Args:
			value1 (str|int):
			value2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_2_int_to_player(value1, value2)
        """
        return self.append((multiplayer_send_2_int_to_player, value1, value2))
        
    def multiplayer_send_3_int_to_player(self, value1, value2, value3):
        """
        (multiplayer_send_3_int_to_player, <player_id>, <message_type>, <value>, <value>, <value>),
        Same as (multiplayer_send_int_to_player), but three integer values are sent.

		Args:
			value1 (str|int):
			value2 (str|int):
			value3 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_3_int_to_player(value1, value2, value3)
        """
        return self.append((multiplayer_send_3_int_to_player, value1, value2, value3))
        
    def multiplayer_send_4_int_to_player(self, value1, value2, value3, value4):
        """
        (multiplayer_send_4_int_to_player, <player_id>, <message_type>, <value>, <value>, <value>, <value>),
        Same as (multiplayer_send_int_to_player), but four integer values are sent.

		Args:
			value1 (str|int):
			value2 (str|int):
			value3 (str|int):
			value4 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_4_int_to_player(value1, value2, value3, value4)
        """
        return self.append((multiplayer_send_4_int_to_player, value1, value2, value3, value4))
        
    def multiplayer_send_string_to_player(self, player_id, message_type, string_id):
        """
        (multiplayer_send_string_to_player, <player_id>, <message_type>, <string_id>),
        Multiplayer server operation. Send a message with a string value to one of connected players.

		Args:
			player_id (str|int):
			message_type (str|int):
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_send_string_to_player(player_id, message_type, string_id)
        """
        return self.append((multiplayer_send_string_to_player, player_id, message_type, string_id))
        
    def get_max_players(self, destination):
        """
        (get_max_players, <destination>),
        Returns maximum possible number of connected players. Apparently always returns a constant value, however it's return value can change as maximum increases with new patches.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> get_max_players(destination)
        """
        return self.append((get_max_players, destination))
        
    def player_get_team_no(self, destination, player_id):
        """
        (player_get_team_no, <destination>, <player_id>),
        Retrieves player's selected team.

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_team_no(destination, player_id)
        """
        return self.append((player_get_team_no, destination, player_id))
        
    def player_set_team_no(self, player_id, team_id):
        """
        (player_set_team_no, <player_id>, <team_id>),
        Assigns a player to the specified team.

		Args:
			player_id (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_team_no(player_id, team_id)
        """
        return self.append((player_set_team_no, player_id, team_id))
        
    def player_get_troop_id(self, destination, player_id):
        """
        (player_get_troop_id, <destination>, <player_id>),
        Retrieves player's selected troop reference.

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_troop_id(destination, player_id)
        """
        return self.append((player_get_troop_id, destination, player_id))
        
    def player_set_troop_id(self, player_id, troop_id):
        """
        (player_set_troop_id, <player_id>, <troop_id>),
        Assigns the selected troop reference to a player.

		Args:
			player_id (str|int):
			troop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_troop_id(player_id, troop_id)
        """
        return self.append((player_set_troop_id, player_id, troop_id))
        
    def player_get_agent_id(self, destination, player_id):
        """
        (player_get_agent_id, <destination>, <player_id>),
        Retrieves player's current agent reference. Returns a negative value if player has no agent.

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_agent_id(destination, player_id)
        """
        return self.append((player_get_agent_id, destination, player_id))
        
    def agent_get_player_id(self, destination, agent_id):
        """
        (agent_get_player_id, <destination>, <agent_id>),
        Retrieves player reference that is currently controlling the specified agent.

		Args:
			destination (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> agent_get_player_id(destination, agent_id)
        """
        return self.append((agent_get_player_id, destination, agent_id))
        
    def player_get_gold(self, destination, player_id):
        """
        (player_get_gold, <destination>, <player_id>),
        Retrieves player's current gold amount.

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_gold(destination, player_id)
        """
        return self.append((player_get_gold, destination, player_id))
        
    def player_set_gold(self, player_id, value, max_value):
        """
        (player_set_gold, <player_id>, <value>, <max_value>),
        Sets player's new gold amount and maximum allowed gold amount. Use 0 for <max_value> to remove gold limit.

		Args:
			player_id (str|int):
			value (str|int):
			max_value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_gold(player_id, value, max_value)
        """
        return self.append((player_set_gold, player_id, value, max_value))
        
    def player_spawn_new_agent(self, player_id, entry_point):
        """
        (player_spawn_new_agent, <player_id>, <entry_point>),
        Spawns a new agent for the specified player. Essentially a combination of (spawn_agent) and (player_control_agent) operations.

		Args:
			player_id (str|int):
			entry_point (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_spawn_new_agent(player_id, entry_point)
        """
        return self.append((player_spawn_new_agent, player_id, entry_point))
        
    def player_add_spawn_item(self, player_id, item_slot_no, item_id):
        """
        (player_add_spawn_item, <player_id>, <item_slot_no>, <item_id>),
        

		Args:
			player_id (str|int):
			item_slot_no (str|int):
			item_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_add_spawn_item(player_id, item_slot_no, item_id)
        """
        return self.append((player_add_spawn_item, player_id, item_slot_no, item_id))
        
    def multiplayer_get_my_team(self, destination):
        """
        (multiplayer_get_my_team, <destination>),
        Client operation. Retrieves player's currently selected team.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_get_my_team(destination)
        """
        return self.append((multiplayer_get_my_team, destination))
        
    def multiplayer_get_my_troop(self, destination):
        """
        (multiplayer_get_my_troop, <destination>),
        Client operation. Retrieves player's currently selected troop.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_get_my_troop(destination)
        """
        return self.append((multiplayer_get_my_troop, destination))
        
    def multiplayer_set_my_troop(self, destination):
        """
        (multiplayer_set_my_troop, <destination>),
        Client operation. Selects a new troop for the player.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_set_my_troop(destination)
        """
        return self.append((multiplayer_set_my_troop, destination))
        
    def multiplayer_get_my_gold(self, destination):
        """
        (multiplayer_get_my_gold, <destination>),
        Client operation. Retrieves current player's gold amount.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_get_my_gold(destination)
        """
        return self.append((multiplayer_get_my_gold, destination))
        
    def multiplayer_get_my_player(self, destination):
        """
        (multiplayer_get_my_player, <destination>),
        Client operation. Retrieves current player's player_id reference.

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_get_my_player(destination)
        """
        return self.append((multiplayer_get_my_player, destination))
        
    def multiplayer_make_everyone_enemy(self):
        """
        (multiplayer_make_everyone_enemy),
        Used in deathmatch mode to make everyone hostile to all other agents.

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_make_everyone_enemy(destination)
        """
        return self.append((multiplayer_make_everyone_enemy))
        
    def player_control_agent(self, player_id, agent_id):
        """
        (player_control_agent, <player_id>, <agent_id>),
        Server operation. Puts the agent under specified player's control. Operation will change agent's face code and banner to those of player.

		Args:
			player_id (str|int):
			agent_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_control_agent(player_id, agent_id)
        """
        return self.append((player_control_agent, player_id, agent_id))
        
    def player_get_item_id(self, destination, player_id, item_slot_no):
        """
        (player_get_item_id, <destination>, <player_id>, <item_slot_no>),
        Server operation. Retrieves item that's currently equipped by specified player in <item_slot_no> equipment slot.

		Args:
			destination (str|int):
			player_id (str|int):
			item_slot_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_item_id(destination, player_id, item_slot_no)
        """
        return self.append((player_get_item_id, destination, player_id, item_slot_no))
        
    def player_get_banner_id(self, destination, player_id):
        """
        (player_get_banner_id, <destination>, <player_id>),
        Server operation. Retrieves banner_id reference used by the specified player. Note that in MP banners are enumerated starting from 0 (unlike single-player where they're enumeration depends on scene prop banners' reference range).

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_banner_id(destination, player_id)
        """
        return self.append((player_get_banner_id, destination, player_id))
        
    def player_set_is_admin(self, player_id, value):
        """
        (player_set_is_admin, <player_id>, <value>),
        Server operation. Set the current player as admin (value = 1) or not (value = 0).

		Args:
			player_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_is_admin(player_id, value)
        """
        return self.append((player_set_is_admin, player_id, value))
        
    def player_get_score(self, destination, player_id):
        """
        (player_get_score, <destination>, <player_id>),
        

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_score(destination, player_id)
        """
        return self.append((player_get_score, destination, player_id))
        
    def player_set_score(self, player_id, value):
        """
        (player_set_score, <player_id>, <value>),
        

		Args:
			player_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_score(player_id, value)
        """
        return self.append((player_set_score, player_id, value))
        
    def player_get_kill_count(self, destination, player_id):
        """
        (player_get_kill_count, <destination>, <player_id>),
        

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_kill_count(destination, player_id)
        """
        return self.append((player_get_kill_count, destination, player_id))
        
    def player_set_kill_count(self, player_id, value):
        """
        (player_set_kill_count, <player_id>, <value>),
        

		Args:
			player_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_kill_count(player_id, value)
        """
        return self.append((player_set_kill_count, player_id, value))
        
    def player_get_death_count(self, destination, player_id):
        """
        (player_get_death_count, <destination>, <player_id>),
        

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_death_count(destination, player_id)
        """
        return self.append((player_get_death_count, destination, player_id))
        
    def player_set_death_count(self, player_id, value):
        """
        (player_set_death_count, <player_id>, <value>),
        

		Args:
			player_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_death_count(player_id, value)
        """
        return self.append((player_set_death_count, player_id, value))
        
    def player_get_ping(self, destination, player_id):
        """
        (player_get_ping, <destination>, <player_id>),
        

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_ping(destination, player_id)
        """
        return self.append((player_get_ping, destination, player_id))
        
    def player_get_is_muted(self, destination, player_id):
        """
        (player_get_is_muted, <destination>, <player_id>),
        

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_is_muted(destination, player_id)
        """
        return self.append((player_get_is_muted, destination, player_id))
        
    def player_set_is_muted(self, player_id, value, mute_for_everyone):
        """
        (player_set_is_muted, <player_id>, <value>, [mute_for_everyone]),
        mute_for_everyone optional parameter should be set to 1 if player is muted for everyone (this works only on server).
		

		Args:
			player_id (str|int):
			value (str|int):
			mute_for_everyone (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_set_is_muted(player_id, value, mute_for_everyone)
        """
        return self.append((player_set_is_muted, player_id, value, mute_for_everyone))
        
    def player_get_unique_id(self, destination, player_id):
        """
        (player_get_unique_id, <destination>, <player_id>),
        can only bew used on server side
		Server operation. Retrieves player's unique identifier which is determined by player's game license code. This number is supposed to be unique for each license, allowing reliable player identification across servers.

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_unique_id(destination, player_id)
        """
        return self.append((player_get_unique_id, destination, player_id))
        
    def player_get_gender(self, destination, player_id):
        """
        (player_get_gender, <destination>, <player_id>),
        

		Args:
			destination (str|int):
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_gender(destination, player_id)
        """
        return self.append((player_get_gender, destination, player_id))
        
    def player_save_picked_up_items_for_next_spawn(self, player_id):
        """
        (player_save_picked_up_items_for_next_spawn, <player_id>),
        

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_save_picked_up_items_for_next_spawn(player_id)
        """
        return self.append((player_save_picked_up_items_for_next_spawn, player_id))
        
    def player_get_value_of_original_items(self, player_id):
        """
        (player_get_value_of_original_items, <player_id>),
        Undocumented. Official docs: this operation returns values of the items, but default troop items will be counted as zero (except horse)

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> player_get_value_of_original_items(player_id)
        """
        return self.append((player_get_value_of_original_items, player_id))
        
    def profile_get_banner_id(self, destination):
        """
        (profile_get_banner_id, <destination>),
        Client operation. Retrieves banner_id reference used by the game for multiplayer. Note that in MP banners are enumerated starting from 0 (unlike single-player where they're enumeration depends on scene prop banners' reference range).

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> profile_get_banner_id(destination)
        """
        return self.append((profile_get_banner_id, destination))
        
    def profile_set_banner_id(self, value):
        """
        (profile_set_banner_id, <value>),
        Client operation. Assigns a new banner_id to be used for multiplayer. Note that in MP banners are enumerated starting from 0 (unlike single-player where they're enumeration depends on scene prop banners' reference range).

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> profile_set_banner_id(value)
        """
        return self.append((profile_set_banner_id, value))
        
    def team_get_bot_kill_count(self, destination, team_id):
        """
        (team_get_bot_kill_count, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_bot_kill_count(destination, team_id)
        """
        return self.append((team_get_bot_kill_count, destination, team_id))
        
    def team_set_bot_kill_count(self, destination, team_id):
        """
        (team_set_bot_kill_count, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_bot_kill_count(destination, team_id)
        """
        return self.append((team_set_bot_kill_count, destination, team_id))
        
    def team_get_bot_death_count(self, destination, team_id):
        """
        (team_get_bot_death_count, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_bot_death_count(destination, team_id)
        """
        return self.append((team_get_bot_death_count, destination, team_id))
        
    def team_set_bot_death_count(self, destination, team_id):
        """
        (team_set_bot_death_count, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_bot_death_count(destination, team_id)
        """
        return self.append((team_set_bot_death_count, destination, team_id))
        
    def team_get_kill_count(self, destination, team_id):
        """
        (team_get_kill_count, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_kill_count(destination, team_id)
        """
        return self.append((team_get_kill_count, destination, team_id))
        
    def team_get_score(self, destination, team_id):
        """
        (team_get_score, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_score(destination, team_id)
        """
        return self.append((team_get_score, destination, team_id))
        
    def team_set_score(self, team_id, value):
        """
        (team_set_score, <team_id>, <value>),
        

		Args:
			team_id (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_score(team_id, value)
        """
        return self.append((team_set_score, team_id, value))
        
    def team_set_faction(self, team_id, faction_id):
        """
        (team_set_faction, <team_id>, <faction_id>),
        

		Args:
			team_id (str|int):
			faction_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_set_faction(team_id, faction_id)
        """
        return self.append((team_set_faction, team_id, faction_id))
        
    def team_get_faction(self, destination, team_id):
        """
        (team_get_faction, <destination>, <team_id>),
        

		Args:
			destination (str|int):
			team_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> team_get_faction(destination, team_id)
        """
        return self.append((team_get_faction, destination, team_id))
        
    def multiplayer_clear_scene(self):
        """
        (multiplayer_clear_scene),
        

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_clear_scene(destination, team_id)
        """
        return self.append((multiplayer_clear_scene))
        
    def multiplayer_find_spawn_point(self, destination, team_no, examine_all_spawn_points, is_horseman):
        """
        (multiplayer_find_spawn_point, <destination>, <team_no>, <examine_all_spawn_points>, <is_horseman>),
        

		Args:
			destination (str|int):
			team_no (str|int):
			examine_all_spawn_points (str|int):
			is_horseman (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> multiplayer_find_spawn_point(destination, team_no, examine_all_spawn_points, is_horseman)
        """
        return self.append((multiplayer_find_spawn_point, destination, team_no, examine_all_spawn_points, is_horseman))
        
    def set_spawn_effector_scene_prop_kind(self, team_no, scene_prop_kind_no):
        """
        (set_spawn_effector_scene_prop_kind, <team_no>, <scene_prop_kind_no>),
        Specifies some scene prop kind as one of the teams' spawn effector, making players of that team more likely to spawn closer to the specified effector prop instances. Use -1 to disable spawn effector for a team.

		Args:
			team_no (str|int):
			scene_prop_kind_no (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_spawn_effector_scene_prop_kind(team_no, scene_prop_kind_no)
        """
        return self.append((set_spawn_effector_scene_prop_kind, team_no, scene_prop_kind_no))
        
    def set_spawn_effector_scene_prop_id(self, team_no, scene_prop_id):
        """
        (set_spawn_effector_scene_prop_id, <team_no>, <scene_prop_id>),
        Specifies a single prop instance as a team's spawn effector. Different from (set_spawn_effector_scene_prop_kind) as other instances of the same scene prop will not affect player spawning.

		Args:
			team_no (str|int):
			scene_prop_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_spawn_effector_scene_prop_id(team_no, scene_prop_id)
        """
        return self.append((set_spawn_effector_scene_prop_id, team_no, scene_prop_id))
        
    def start_multiplayer_mission(self, mission_template_id, scene_id, started_manually):
        """
        (start_multiplayer_mission, <mission_template_id>, <scene_id>, <started_manually>),
        

		Args:
			mission_template_id (str|int):
			scene_id (str|int):
			started_manually (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> start_multiplayer_mission(mission_template_id, scene_id, started_manually)
        """
        return self.append((start_multiplayer_mission, mission_template_id, scene_id, started_manually))
        
    def kick_player(self, player_id):
        """
        (kick_player, <player_id>),
        

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> kick_player(player_id)
        """
        return self.append((kick_player, player_id))
        
    def ban_player(self, player_id1, player_id2):
        """
        (ban_player, <player_id>, <value>, <player_id>),
        Official docs: set value = 1 for banning temporarily, assign 2nd player id as the administrator player id if banning is permanent

		Args:
			player_id1 (str|int):
			player_id2 (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> ban_player(player_id1, player_id2)
        """
        return self.append((ban_player, player_id1, player_id2))
        
    def save_ban_info_of_player(self, player_id):
        """
        (save_ban_info_of_player, <player_id>),
        

		Args:
			player_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> save_ban_info_of_player(player_id)
        """
        return self.append((save_ban_info_of_player, player_id))
        
    def ban_player_using_saved_ban_info(self):
        """
        (ban_player_using_saved_ban_info),
        

        Returns:
            TupleBuilder: self

        Example:
            >>> ban_player_using_saved_ban_info(player_id)
        """
        return self.append((ban_player_using_saved_ban_info))
        
    def server_add_message_to_log(self, string_id):
        """
        (server_add_message_to_log, <string_id>),
        

		Args:
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_add_message_to_log(string_id)
        """
        return self.append((server_add_message_to_log, string_id))
        
    def server_get_renaming_server_allowed(self, destination):
        """
        (server_get_renaming_server_allowed, <destination>),
        Official docs: 0-1

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_renaming_server_allowed(destination)
        """
        return self.append((server_get_renaming_server_allowed, destination))
        
    def server_get_changing_game_type_allowed(self, destination):
        """
        (server_get_changing_game_type_allowed, <destination>),
        Official docs: 0-1

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_changing_game_type_allowed(destination)
        """
        return self.append((server_get_changing_game_type_allowed, destination))
        
    def server_get_combat_speed(self, destination):
        """
        (server_get_combat_speed, <destination>),
        Official docs: 0-2

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_combat_speed(destination)
        """
        return self.append((server_get_combat_speed, destination))
        
    def server_set_combat_speed(self, value):
        """
        (server_set_combat_speed, <value>),
        Official docs: 0-2

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_combat_speed(value)
        """
        return self.append((server_set_combat_speed, value))
        
    def server_get_friendly_fire(self, destination):
        """
        (server_get_friendly_fire, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_friendly_fire(destination)
        """
        return self.append((server_get_friendly_fire, destination))
        
    def server_set_friendly_fire(self, value):
        """
        (server_set_friendly_fire, <value>),
        Official docs: 0 = off, 1 = on

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_friendly_fire(value)
        """
        return self.append((server_set_friendly_fire, value))
        
    def server_get_control_block_dir(self, destination):
        """
        (server_get_control_block_dir, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_control_block_dir(destination)
        """
        return self.append((server_get_control_block_dir, destination))
        
    def server_set_control_block_dir(self, value):
        """
        (server_set_control_block_dir, <value>),
        Official docs: 0 = automatic, 1 = by mouse movement

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_control_block_dir(value)
        """
        return self.append((server_set_control_block_dir, value))
        
    def server_set_password(self, string_id):
        """
        (server_set_password, <string_id>),
        

		Args:
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_password(string_id)
        """
        return self.append((server_set_password, string_id))
        
    def server_get_add_to_game_servers_list(self, destination):
        """
        (server_get_add_to_game_servers_list, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_add_to_game_servers_list(destination)
        """
        return self.append((server_get_add_to_game_servers_list, destination))
        
    def server_set_add_to_game_servers_list(self, value):
        """
        (server_set_add_to_game_servers_list, <value>),
        

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_add_to_game_servers_list(value)
        """
        return self.append((server_set_add_to_game_servers_list, value))
        
    def server_get_ghost_mode(self, destination):
        """
        (server_get_ghost_mode, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_ghost_mode(destination)
        """
        return self.append((server_get_ghost_mode, destination))
        
    def server_set_ghost_mode(self, value):
        """
        (server_set_ghost_mode, <value>),
        

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_ghost_mode(value)
        """
        return self.append((server_set_ghost_mode, value))
        
    def server_set_name(self, string_id):
        """
        (server_set_name, <string_id>),
        

		Args:
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_name(string_id)
        """
        return self.append((server_set_name, string_id))
        
    def server_get_max_num_players(self, destination):
        """
        (server_get_max_num_players, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_max_num_players(destination)
        """
        return self.append((server_get_max_num_players, destination))
        
    def server_set_max_num_players(self, value):
        """
        (server_set_max_num_players, <value>),
        

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_max_num_players(value)
        """
        return self.append((server_set_max_num_players, value))
        
    def server_set_welcome_message(self, string_id):
        """
        (server_set_welcome_message, <string_id>),
        

		Args:
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_welcome_message(string_id)
        """
        return self.append((server_set_welcome_message, string_id))
        
    def server_get_melee_friendly_fire(self, destination):
        """
        (server_get_melee_friendly_fire, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_melee_friendly_fire(destination)
        """
        return self.append((server_get_melee_friendly_fire, destination))
        
    def server_set_melee_friendly_fire(self, value):
        """
        (server_set_melee_friendly_fire, <value>),
        Official docs: 0 = off, 1 = on

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_melee_friendly_fire(value)
        """
        return self.append((server_set_melee_friendly_fire, value))
        
    def server_get_friendly_fire_damage_self_ratio(self, destination):
        """
        (server_get_friendly_fire_damage_self_ratio, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_friendly_fire_damage_self_ratio(destination)
        """
        return self.append((server_get_friendly_fire_damage_self_ratio, destination))
        
    def server_set_friendly_fire_damage_self_ratio(self, value):
        """
        (server_set_friendly_fire_damage_self_ratio, <value>),
        Official docs: 0-100

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_friendly_fire_damage_self_ratio(value)
        """
        return self.append((server_set_friendly_fire_damage_self_ratio, value))
        
    def server_get_friendly_fire_damage_friend_ratio(self, destination):
        """
        (server_get_friendly_fire_damage_friend_ratio, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_friendly_fire_damage_friend_ratio(destination)
        """
        return self.append((server_get_friendly_fire_damage_friend_ratio, destination))
        
    def server_set_friendly_fire_damage_friend_ratio(self, value):
        """
        (server_set_friendly_fire_damage_friend_ratio, <value>),
        Official docs: 0-100

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_friendly_fire_damage_friend_ratio(value)
        """
        return self.append((server_set_friendly_fire_damage_friend_ratio, value))
        
    def server_get_anti_cheat(self, destination):
        """
        (server_get_anti_cheat, <destination>),
        

		Args:
			destination (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_get_anti_cheat(destination)
        """
        return self.append((server_get_anti_cheat, destination))
        
    def server_set_anti_cheat(self, value):
        """
        (server_set_anti_cheat, <value>),
        Official docs: 0 = off, 1 = on

		Args:
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> server_set_anti_cheat(value)
        """
        return self.append((server_set_anti_cheat, value))
        
    def set_tooltip_text(self, string_id):
        """
        (set_tooltip_text, <string_id>),
        

		Args:
			string_id (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> set_tooltip_text(string_id)
        """
        return self.append((set_tooltip_text, string_id))
        
    def ai_mesh_face_group_show_hide(self, group_no, value):
        """
        (ai_mesh_face_group_show_hide, <group_no>, <value>),
        1 for enable, 0 for disable

		Args:
			group_no (str|int):
			value (str|int):

        Returns:
            TupleBuilder: self

        Example:
            >>> ai_mesh_face_group_show_hide(group_no, value)
        """
        return self.append((ai_mesh_face_group_show_hide, group_no, value))

    def auto_set_meta_mission_at_end_commited(self):
        """
        (auto_set_meta_mission_at_end_commited)
        Not documented. Not used in Native. Was (simulate_battle, <value>) before

        Returns:
            TupleBuilder: self

        Example:
            >>> auto_set_meta_mission_at_end_commited(":screening_party_score")
        """
        return self.append((auto_set_meta_mission_at_end_commited))