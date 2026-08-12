# model_based_agent.py
"""Model‑Based Agent that keeps a memory of visited percept states.
It updates its internal state each turn and uses IF‑THEN rules that consult
that memory. The agent is stateless with respect to the environment – it only
stores what it has observed.
"""

class ModelBasedAgent:
    """Agent with an internal memory (visited percept states).

    The environment provides a *local* percept dictionary containing:
        - ``wall_ahead`` (bool)
        - ``food_here``  (bool)
    The agent also receives the action it chose on the previous step via
    ``self.last_action`` so it can update its internal direction estimate.
    """

    def __init__(self):
        # Set of tuples that uniquely identify a percept state the agent has seen.
        # We include the direction the agent is currently facing so that the same
        # wall/food pattern observed from a different heading is treated as a
        # distinct state.
        self.visited_states = set()
        # Remember the last action to keep a simple internal direction model.
        self.last_action = None
        self.direction = "Up"  # default facing direction

    def _update_direction(self, action: str):
        """Update the internal facing direction based on the action taken.
        The environment only moves the agent forward; turning is modelled by
        choosing a different movement direction. For simplicity we treat the
        action itself as the new direction.
        """
        if action in {"Up", "Down", "Left", "Right"}:
            self.direction = action
        # store the action for the next step
        self.last_action = action

    def sense_and_act(self, percept: dict) -> str:
        """Choose an action using IF‑THEN rules that query the memory.

        Rule set (strict IF‑THEN logic):
        1. IF ``food_here`` THEN move forward (``Up`` – the default forward).
        2. IF ``wall_ahead`` AND the *current* percept state has been visited
           BEFORE THEN turn right (``Right``).
        3. IF ``wall_ahead`` THEN turn left (``Left``).
        4. ELSE move forward (``Up``).
        """
        # Record the current state *before* deciding on an action.
        state_id = (self.direction, percept.get('wall_ahead'), percept.get('food_here'))
        self.visited_states.add(state_id)

        # Rule 1: food ahead → forward
        if percept.get('food_here', False):
            action = 'Up'
            self._update_direction(action)
            return action

        # Rule 2: wall ahead and we have seen this exact state before → turn right
        if percept.get('wall_ahead', False) and state_id in self.visited_states:
            action = 'Right'
            self._update_direction(action)
            return action

        # Rule 3: wall ahead → turn left
        if percept.get('wall_ahead', False):
            action = 'Left'
            self._update_direction(action)
            return action

        # Rule 4: default forward move
        action = 'Up'
        self._update_direction(action)
        return action
