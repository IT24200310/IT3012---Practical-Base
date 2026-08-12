# simulator.py
from visual_grid_game import VisualGridHuntGame
from simple_reflex_agent import SimpleReflexAgent
from model_based_agent import ModelBasedAgent
from grid_game import GridHuntGame


def run_simple_reflex():
    """Run the VisualGridHuntGame with the SimpleReflexAgent.
    Demonstrates failure in a partially observable world.
    """
    env = VisualGridHuntGame()
    agent = SimpleReflexAgent()

    print("=== Simple Reflex Agent Simulation Started ===")
    while not env.is_done():
        percept = env.get_percept()
        action = agent.sense_and_act(percept)
        env.execute_action(action)
        # Show a concise status line
        print(f"Action: {action} | WallAhead: {percept.get('wall_ahead')} | FoodHere: {percept.get('food_here')} | Score: {percept['score']}")
    print(f"\nSimple Reflex Simulation Over! Final Score: {env.score} after {env.steps} steps.")
from agent import GreedyGridAgent


def run_model_based():
    """Run the VisualGridHuntGame with the ModelBasedAgent.
    Demonstrates memory‑based behavior that can break out of loops.
    """
    env = VisualGridHuntGame()
    agent = ModelBasedAgent()
    print("=== Model‑Based Agent Simulation Started ===")
    while not env.is_done():
        percept = env.get_percept()
        action = agent.sense_and_act(percept)
        env.execute_action(action)
        print(f"Action: {action} | WallAhead: {percept.get('wall_ahead')} | FoodHere: {percept.get('food_here')} | Score: {percept['score']}")
    print(f"\nModel‑Based Simulation Over! Final Score: {env.score} after {env.steps} steps.")


def run_grid_hunt():
    env = GridHuntGame()
    agent = GreedyGridAgent()

    print("=== UC Berkeley Style Small Grid Hunt Started ===")
    while not env.is_done():
        percept = env.get_percept(agent)
        action = agent.sense_and_act(percept)
        env.execute_action(agent, action)
        print(f"Pos: {percept['agent_pos']} | Food Left: {percept['remaining_food']} | Score: {percept['score']}")

    print(f"\nGame Over! Final Score: {env.score} after {env.steps} steps.")

if __name__ == "__main__":
    run_grid_hunt()