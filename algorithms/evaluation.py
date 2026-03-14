from __future__ import annotations

from typing import TYPE_CHECKING
import algorithms.utils as utils

if TYPE_CHECKING:
    from world.game_state import GameState


def evaluation_function(state: GameState) -> float:
    """
    Evaluation function for non-terminal states of the drone vs. hunters game.

    A good evaluation function can consider multiple factors, such as:
      (a) BFS distance from drone to nearest delivery point (closer is better).
          Uses actual path distance so walls and terrain are respected.
      (b) BFS distance from each hunter to the drone, traversing only normal
          terrain ('.' / ' ').  Hunters blocked by mountains, fog, or storms
          are treated as unreachable (distance = inf) and pose no threat.
      (c) BFS distance to a "safe" position (i.e., a position that is not in the path of any hunter).
      (d) Number of pending deliveries (fewer is better).
      (e) Current score (higher is better).
      (f) Delivery urgency: reward the drone for being close to a delivery it can
          reach strictly before any hunter, so it commits to nearby pickups
          rather than oscillating in place out of excessive hunter fear.
      (g) Adding a revisit penalty can help prevent the drone from getting stuck in cycles.

    Returns a value in [-1000, +1000].

    Tips:
    - Use state.get_drone_position() to get the drone's current (x, y) position.
    - Use state.get_hunter_positions() to get the list of hunter (x, y) positions.
    - Use state.get_pending_deliveries() to get the set of pending delivery (x, y) positions.
    - Use state.get_score() to get the current game score.
    - Use state.get_layout() to get the current layout.
    - Use state.is_win() and state.is_lose() to check terminal states.
    - Use bfs_distance(layout, start, goal, hunter_restricted) from algorithms.utils
      for cached BFS distances. hunter_restricted=True for hunter-only terrain.
    - Use dijkstra(layout, start, goal) from algorithms.utils for cached
      terrain-weighted shortest paths, returning (cost, path).
    - Consider edge cases: no pending deliveries, no hunters nearby.
    - A good evaluation function balances delivery progress with hunter avoidance.
    """

    if state.is_win():
        return 1000.0

    if state.is_lose():
        return -1000.0

    drone_pos = state.get_drone_position()
    if drone_pos is None:
        return -1000.0

    hunters = state.get_hunter_positions()
    deliveries = state.get_pending_deliveries()
    layout = state.get_layout()
    score = float(state.get_score())

    value = score

    if not deliveries:
        return max(-1000.0, min(1000.0, value + 500.0))

    delivery_dists = []
    delivery_costs = []

    for delivery in deliveries:
        dist = utils.bfs_distance(
            layout,
            drone_pos,
            delivery,
            hunter_restricted=False,
        )
        cost, _ = utils.dijkstra(layout, drone_pos, delivery)

        if dist != float("inf"):
            delivery_dists.append(dist)

        if cost != float("inf"):
            delivery_costs.append(cost)

    if delivery_dists:
        nearest_delivery = min(delivery_dists)
        value += 80.0 / (nearest_delivery + 1)

    if delivery_costs:
        cheapest_delivery = min(delivery_costs)
        value += 120.0 / (cheapest_delivery + 1)

    value -= 120.0 * len(deliveries)

    hunter_dists = []
    for hunter in hunters:
        dist = utils.bfs_distance(
            layout,
            hunter,
            drone_pos,
            hunter_restricted=True,
        )
        if dist != float("inf"):
            hunter_dists.append(dist)

    if hunter_dists:
        closest_hunter = min(hunter_dists)

        if closest_hunter == 0:
            return -1000.0
        elif closest_hunter == 1:
            value -= 600.0
        elif closest_hunter == 2:
            value -= 250.0
        elif closest_hunter == 3:
            value -= 120.0
        else:
            value += min(120.0, 12.0 * closest_hunter)

        for dist in hunter_dists:
            value -= 35.0 / (dist + 1)

    safe_bonus = 0.0

    for delivery in deliveries:
        drone_steps = utils.bfs_distance(
            layout,
            drone_pos,
            delivery,
            hunter_restricted=False,
        )

        if drone_steps == float("inf"):
            continue

        hunter_best = float("inf")

        for hunter in hunters:
            hdist = utils.bfs_distance(
                layout,
                hunter,
                delivery,
                hunter_restricted=True,
            )
            hunter_best = min(hunter_best, hdist)

        if drone_steps < hunter_best:
            safe_bonus = max(safe_bonus, 140.0 / (drone_steps + 1))

    value += safe_bonus

    if len(deliveries) == 1 and delivery_dists:
        value += 100.0 / (min(delivery_dists) + 1)
    value = max(-1000.0,min(1000.0, value))
    return value