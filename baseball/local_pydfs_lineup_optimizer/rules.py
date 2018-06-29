from __future__ import division
from collections import defaultdict
from itertools import product, combinations
from random import getrandbits, uniform
from typing import Dict, Any
from pydfs_lineup_optimizer.solvers import Solver, SolverSign
from pydfs_lineup_optimizer.utils import list_intersection
from pydfs_lineup_optimizer.lineup import Lineup
from pydfs_lineup_optimizer.player import Player


class OptimizerRule(object):
    def __init__(self, optimizer, params):
        # type: ('LineupOptimizer', Dict[str, Any]) -> None
        self.params = params
        self.optimizer = optimizer

    def apply(self, solver, players_dict):
        # type: (Solver, Dict[Player, Any]) -> None
        pass

    def apply_for_iteration(self, solver, players_dict, result):
        # type: (Solver, Dict[Player, any], Lineup) -> None
        pass


class NormalObjective(OptimizerRule):
    def apply(self, solver, players_dict):
        variables = []
        coefficients = []
        for player, variable in players_dict.items():
            variables.append(variable)
            coefficients.append(player.fppg)
        solver.set_objective(variables, coefficients)

    def apply_for_iteration(self, solver, players_dict, result):
        if not result:
            return
        variables = []
        coefficients = []
        for player, variable in players_dict.items():
            variables.append(variable)
            coefficients.append(player.fppg)
        solver.add_constraint(variables, coefficients, SolverSign.LTE, result.fantasy_points_projection - 0.001)


class RandomObjective(OptimizerRule):
    def apply_for_iteration(self, solver, players_dict, result):
        variables = []
        coefficients = []
        for player, variable in players_dict.items():
            variables.append(variable)
            coefficients.append(player.fppg * (1 + (-1 if bool(getrandbits(1)) else 1) *
                                               uniform(*self.optimizer.get_deviation())))
        solver.set_objective(variables, coefficients)


class TotalPlayersRule(OptimizerRule):
    def apply(self, solver, players_dict):
        variables = players_dict.values()
        coefficients = [1] * len(variables)
        solver.add_constraint(variables, coefficients, SolverSign.EQ, self.optimizer.total_players)


class LineupBudgetRule(OptimizerRule):
    def apply(self, solver, players_dict):
        variables = []
        coefficients = []
        for player, variable in players_dict.items():
            variables.append(variable)
            coefficients.append(player.salary)
        solver.add_constraint(variables, coefficients, SolverSign.LTE, self.optimizer.budget)


class LockedPlayersRule(OptimizerRule):
    def __init__(self, optimizer, params):
        super(LockedPlayersRule, self).__init__(optimizer, params)
        self.used_players = defaultdict(int)

    def apply_for_iteration(self, solver, players_dict, result):
        if not result:
            # First iteration, locked players must have exposure > 0
            for player in self.optimizer.locked_players:
                solver.add_constraint([players_dict[player]], [1], SolverSign.EQ, 1)
            return
        for player in result.lineup:
            self.used_players[player] += 1
        removed_players = []
        for player, used in self.used_players.items():
            exposure = player.max_exposure if player.max_exposure is not None else self.params.get('max_exposure')
            if exposure is not None and exposure <= used / self.params.get('n'):
                removed_players.append(player)
                solver.add_constraint([players_dict[player]], [1], SolverSign.EQ, 0)
        for player in self.optimizer.locked_players:
            if player not in removed_players:
                solver.add_constraint([players_dict[player]], [1], SolverSign.EQ, 1)


class PositionsRule(OptimizerRule):
    def apply(self, solver, players_dict):
        extra_positions = self.optimizer.players_with_same_position
        positions = self.optimizer.get_positions_for_optimizer()
        for position, places in positions.items():
            extra = 0
            if len(position) == 1:
                extra = extra_positions.get(position[0], 0)
            players_with_position = [variable for player, variable in players_dict.items()
                                     if list_intersection(position, player.positions)]
            coefficients = [1] * len(players_with_position)
            solver.add_constraint(players_with_position, coefficients, SolverSign.GTE, places + extra)


class TeamMatesRule(OptimizerRule):
    def apply(self, solver, players_dict):
        for team, quantity in self.optimizer.players_from_one_team.items():
            players_from_same_team = [variable for player, variable in players_dict.items() if player.team == team]
            coefficients = [1] * len(players_from_same_team)
            solver.add_constraint(players_from_same_team, coefficients, SolverSign.EQ, quantity)


class MaxFromOneTeamRule(OptimizerRule):
    def apply(self, solver, players_dict):
        if not self.optimizer.max_from_one_team:
            return
        for team in self.optimizer.available_teams:
            players_from_team = [variable for player, variable in players_dict.items() if player.team == team]
            coefficients = [1] * len(players_from_team)
            solver.add_constraint(players_from_team, coefficients, SolverSign.LTE, self.optimizer.max_from_one_team)


class MinSalaryCapRule(OptimizerRule):
    def apply(self, solver, players_dict):
        variables = []
        coefficients = []
        for player, variable in players_dict.items():
            variables.append(variable)
            coefficients.append(player.salary)
        min_salary_cap = self.optimizer.min_salary_cap
        solver.add_constraint(variables, coefficients, SolverSign.GTE, min_salary_cap)


class FromSameTeamByPositionsRule(OptimizerRule):
    def apply(self, solver, players_dict):
        from_same_team = len(self.optimizer.positions_from_same_team)
        players_combinations = []
        # Create all possible combinations with specified position for each team
        for team in self.optimizer.available_teams:
            team_players = [player for player in players_dict.keys() if player.team == team]
            players_by_positions = []
            for position in self.optimizer.positions_from_same_team:
                players_by_positions.append([player for player in team_players if position in player.positions])
            for players_combination in product(*players_by_positions):
                # Remove combinations with duplicated players
                if len(set(players_combination)) != from_same_team:
                    continue
                players_combinations.append(tuple([player for player in players_combination]))
        combinations_variable = {combination: solver.add_variable(
            'combinations_%d' % i, 0, 1
        ) for i, combination in enumerate(players_combinations)}
        solver.add_constraint(combinations_variable.values(), [1] * len(combinations_variable), SolverSign.GTE, 1)
        for combination in players_combinations:
            variables = [players_dict[player] for player in combination]
            coefficients = [1] * len(variables)
            solver.add_constraint(variables, coefficients, SolverSign.GTE,
                                  from_same_team * combinations_variable[combination])


class RemoveInjuredRule(OptimizerRule):
    def apply(self, solver, players_dict):
        for player, variable in players_dict.items():
            if player.is_injured:
                solver.add_constraint([variable], [1], SolverSign.EQ, 0)


class MaxRepeatingPlayersRule(OptimizerRule):
    def __init__(self, optimizer, params):
        super(MaxRepeatingPlayersRule, self).__init__(optimizer, params)
        self.exclude_combinations = []

    def apply_for_iteration(self, solver, players_dict, result):
        max_repeating_players = self.optimizer.max_repeating_players
        if max_repeating_players is None or not result:
            return
        for players_combination in combinations(result.players, max_repeating_players + 1):
            self.exclude_combinations.append([players_dict[player] for player in players_combination])
        coefficients = [1] * (max_repeating_players + 1)
        for players_combination in self.exclude_combinations:
            solver.add_constraint(players_combination, coefficients, SolverSign.LTE, max_repeating_players)

