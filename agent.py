# agent.py
import random
from collections import deque
import heapq

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent(GreedyGridAgent):
    def __init__(self):
        super().__init__()
        self.plan = []
        self.active_algo = 'BFS'
        self.pos = (0, 0)
        
    def _get_neighbors(self, state, percept):
        x, y = state
        w, h = percept['grid_size']
        walls = set(percept['walls'])
        for action, (dx, dy) in [('Up', (0,1)), ('Down', (0,-1)), ('Left', (-1,0)), ('Right', (1,0))]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in walls:
                yield action, (nx, ny)

    def bfs_search(self, start, goal, percept):
        frontier = deque([(start, [])])
        reached = {start}
        while frontier:
            curr, path = frontier.popleft()
            if curr == goal:
                return path
            for action, nxt in self._get_neighbors(curr, percept):
                if nxt not in reached:
                    reached.add(nxt)
                    frontier.append((nxt, path + [action]))
        return []

    def dfs_search(self, start, goal, percept):
        frontier = [(start, [])]
        reached = set()
        while frontier:
            curr, path = frontier.pop()
            if curr == goal:
                return path
            if curr not in reached:
                reached.add(curr)
                for action, nxt in self._get_neighbors(curr, percept):
                    if nxt not in reached:
                        frontier.append((nxt, path + [action]))
        return []

    def ucs_search(self, start, goal, percept):
        frontier = [(0, start, [])]
        reached = set()
        while frontier:
            cost, curr, path = heapq.heappop(frontier)
            if curr == goal:
                return path
            if curr not in reached:
                reached.add(curr)
                for action, nxt in self._get_neighbors(curr, percept):
                    if nxt not in reached:
                        heapq.heappush(frontier, (cost + 1, nxt, path + [action]))
        return []

    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:
            all_food = percept.get('all_food', [])
            if not all_food:
                return 'Stay'
            closest_food = min(all_food, key=lambda f: abs(f[0]-self.pos[0]) + abs(f[1]-self.pos[1]))
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(self.pos, closest_food, percept)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(self.pos, closest_food, percept)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(self.pos, closest_food, percept)
            if not self.plan:
                return 'Stay'
        
        action = self.plan.pop(0)
        x, y = self.pos
        if action == 'Up': self.pos = (x, y + 1)
        elif action == 'Down': self.pos = (x, y - 1)
        elif action == 'Left': self.pos = (x - 1, y)
        elif action == 'Right': self.pos = (x + 1, y)
        return action