# simple_reflex_agent.py
"""Implementation of a stateless Simple Reflex Agent.
The agent decides an action solely from the current percept using
IF‑THEN rules. No history or __init__ state is stored.
"""

class SimpleReflexAgent:
    """Stateless reflex agent.

    Expected percept dictionary (produced by VisualGridHuntGame.get_percept):
        - ``wall_ahead`` (bool): True if the cell directly ahead is a wall or out of bounds.
        - ``food_here``  (bool): True if food is in the cell directly ahead.
    The agent returns one of the movement actions understood by the environment:
        'Up', 'Down', 'Left', 'Right'.
    """

    def sense_and_act(self, percept: dict) -> str:
        """Choose an action based on the current percept.

        Rule set (strict IF‑THEN logic):
        1. IF ``food_here`` THEN move forward (chosen as ``Up`` – the default forward direction).
        2. IF ``wall_ahead`` THEN turn left (implemented as moving ``Left``).
        3. ELSE move forward (again ``Up``).
        """
        # Rule 1: food ahead → go forward
        if percept.get('food_here', False):
            return 'Up'
        # Rule 2: wall ahead → turn left (move left)
        if percept.get('wall_ahead', False):
            return 'Left'
        # Rule 3: default action – move forward
        return 'Up'
