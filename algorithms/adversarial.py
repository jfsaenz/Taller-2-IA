from __future__ import annotations

import random
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

import algorithms.evaluation as evaluation
from world.game import Agent, Directions

if TYPE_CHECKING:
    from world.game_state import GameState


class MultiAgentSearchAgent(Agent, ABC):
    """
    Base class for multi-agent search agents (Minimax, AlphaBeta, Expectimax).
    """

    def __init__(self, depth: str = "2", _index: int = 0, prob: str = "0.0") -> None:
        self.index = 0  # Drone is always agent 0
        self.depth = int(depth)
        self.prob = float(
            prob
        )  # Probability that each hunter acts randomly (0=greedy, 1=random)
        self.evaluation_function = evaluation.evaluation_function

    @abstractmethod
    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone from the current GameState.
        """
        pass


class RandomAgent(MultiAgentSearchAgent):
    """
    Agent that chooses a legal action uniformly at random.
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Get a random legal action for the drone.
        """
        legal_actions = state.get_legal_actions(self.index)
        return random.choice(legal_actions) if legal_actions else None


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Minimax agent for the drone (MAX) vs hunters (MIN) game.
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using minimax.

        Tips:
        - The game tree alternates: drone (MAX) -> hunter1 (MIN) -> hunter2 (MIN) -> ... -> drone (MAX) -> ...
        - Use self.depth to control the search depth. depth=1 means the drone moves once and each hunter moves once.
        - Use state.get_legal_actions(agent_index) to get legal actions for a specific agent.
        - Use state.generate_successor(agent_index, action) to get the successor state after an action.
        - Use state.is_win() and state.is_lose() to check terminal states.
        - Use state.get_num_agents() to get the total number of agents.
        - Use self.evaluation_function(state) to evaluate leaf/terminal states.
        - The next agent is (agent_index + 1) % num_agents. Depth decreases after all agents have moved (full ply).
        - Return the ACTION (not the value) that maximizes the minimax value for the drone.
        """
        # Obtengo las acciones legales del drone
        legal_actions = state.get_legal_actions(self.index)
        if not legal_actions:
            return None
        
        # Inicializo variables para la mejor acción y valor
        best_action = None
        best_value = float('-inf')
        # Calculo el número de agentes una vez para pasarlo a minimax
        num_agents = state.get_num_agents()
        
        # Pruebo cada acción posible del drone
        for action in legal_actions:
            successor = state.generate_successor(self.index, action)
            # Llamo a minimax con el estado sucesor, empezando desde el agente 1 (primer hunter)
            value = self.minimax(successor, 1, self.depth, num_agents)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    
    def minimax(self, state, agent_index, depth, num_agents):
        # Si llego a profundidad 0 o estado terminal, evaluo el estado
        if depth == 0 or state.is_win() or state.is_lose():
            return self.evaluation_function(state)
        
        # Calculo el siguiente agente y ajusto la profundidad si es un nuevo ply
        next_agent = (agent_index + 1) % num_agents
        next_depth = depth if next_agent != 0 else depth - 1
        
        # Si es el turno del drone (MAX), maximizo
        if agent_index == 0:
            value = float('-inf')
            for action in state.get_legal_actions(agent_index):
                successor = state.generate_successor(agent_index, action)
                value = max(value, self.minimax(successor, next_agent, next_depth, num_agents))
            return value
        # Si es turno de un hunter (MIN), minimizo
        else:
            value = float('inf')
            for action in state.get_legal_actions(agent_index):
                successor = state.generate_successor(agent_index, action)
                value = min(value, self.minimax(successor, next_agent, next_depth, num_agents))
            return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Alpha-Beta pruning agent. Same as Minimax but with alpha-beta pruning.
    MAX node: prune when value > beta (strict).
    MIN node: prune when value < alpha (strict).
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using alpha-beta pruning.

        Tips:
        - Same structure as MinimaxAgent, but with alpha-beta pruning.
        - Alpha: best value MAX can guarantee (initially -inf).
        - Beta: best value MIN can guarantee (initially +inf).
        - MAX node: prune when value > beta (strict inequality, do NOT prune on equality).
        - MIN node: prune when value < alpha (strict inequality, do NOT prune on equality).
        - Update alpha at MAX nodes: alpha = max(alpha, value).
        - Update beta at MIN nodes: beta = min(beta, value).
        - Pass alpha and beta through the recursive calls.
        """
        # Obtengo las acciones legales del drone
        legal_actions = state.get_legal_actions(self.index)
        if not legal_actions:
            return None
        
        # Inicializo variables para la mejor acción y valor
        best_action = None
        best_value = float('-inf')
        # Calculo el número de agentes una vez
        num_agents = state.get_num_agents()
        # Alpha y beta iniciales
        alpha = float('-inf')
        beta = float('inf')
        
        # Pruebo cada acción posible del drone
        for action in legal_actions:
            successor = state.generate_successor(self.index, action)
            # Llamo a alphabeta con el estado sucesor, empezando desde el agente 1
            value = self.alphabeta(successor, 1, self.depth, num_agents, alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
            # Actualizo alpha para poda
            alpha = max(alpha, value)
        
        return best_action
    
    def alphabeta(self, state, agent_index, depth, num_agents, alpha, beta):
        # Si llego a profundidad 0 o estado terminal, evaluo el estado
        if depth == 0 or state.is_win() or state.is_lose():
            return self.evaluation_function(state)
        
        # Calculo el siguiente agente y ajusto la profundidad si es un nuevo ply
        next_agent = (agent_index + 1) % num_agents
        next_depth = depth if next_agent != 0 else depth - 1
        
        # Si es el turno del drone (MAX), maximizo con alpha-beta
        if agent_index == 0:
            value = float('-inf')
            for action in state.get_legal_actions(agent_index):
                successor = state.generate_successor(agent_index, action)
                value = max(value, self.alphabeta(successor, next_agent, next_depth, num_agents, alpha, beta))
                # Actualizo alpha
                alpha = max(alpha, value)
                # No uso break para poda, exploro todas
            return value
        # Si es turno de un hunter (MIN), minimizo con alpha-beta
        else:
            value = float('inf')
            for action in state.get_legal_actions(agent_index):
                successor = state.generate_successor(agent_index, action)
                value = min(value, self.alphabeta(successor, next_agent, next_depth, num_agents, alpha, beta))
                # Actualizo beta
                beta = min(beta, value)
                # No uso break para poda, exploro todas
            return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Expectimax agent with a mixed hunter model.

    Each hunter acts randomly with probability self.prob and greedily
    (worst-case / MIN) with probability 1 - self.prob.

    * When prob = 0:  behaves like Minimax (hunters always play optimally).
    * When prob = 1:  pure expectimax (hunters always play uniformly at random).
    * When 0 < prob < 1: weighted combination that correctly models the
      actual MixedHunterAgent used at game-play time.

    Chance node formula:
        value = (1 - p) * min(child_values) + p * mean(child_values)
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using expectimax with mixed hunter model.

        Tips:
        - Drone nodes are MAX (same as Minimax).
        - Hunter nodes are CHANCE with mixed model: the hunter acts greedily with
          probability (1 - self.prob) and uniformly at random with probability self.prob.
        - Mixed expected value = (1-p) * min(child_values) + p * mean(child_values).
        - When p=0 this reduces to Minimax; when p=1 it is pure uniform expectimax.
        - Do NOT prune in expectimax (unlike alpha-beta).
        - self.prob is set via the constructor argument prob.
        """

        def expectimax(current_state, depth, agent_index):
            if depth == self.depth or current_state.is_win() or current_state.is_lose():
                return self.evaluation_function(current_state)

            legal_actions = current_state.get_legal_actions(agent_index)
            if not legal_actions:
                return self.evaluation_function(current_state)

            num_agents = current_state.get_num_agents()
            next_agent = (agent_index + 1) % num_agents
            next_depth = depth + 1 if next_agent == 0 else depth

            if agent_index == 0:
                best_value = float("-inf")

                for action in legal_actions:
                    successor = current_state.generate_successor(agent_index, action)
                    value = expectimax(successor, next_depth, next_agent)

                    if value > best_value:
                        best_value = value

                return best_value

            values = []

            for action in legal_actions:
                successor = current_state.generate_successor(agent_index, action)
                values.append(expectimax(successor, next_depth, next_agent))

            min_value = min(values)
            avg_value = sum(values) / len(values)

            return (1 - self.prob) * min_value + self.prob * avg_value

        legal_actions = state.get_legal_actions(self.index)

        if not legal_actions:
            return None

        best_action = None
        best_value = float("-inf")

        for action in legal_actions:
            successor = state.generate_successor(self.index, action)
            value = expectimax(successor, 0, 1)

            if value > best_value:
                best_value = value
                best_action = action

        return best_action