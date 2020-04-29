import numpy as np


def my_print(strings):
    print()
    for string in strings:
        print(string)
    print()


def my_round(number):
    return round(number, 4)


class Asset:
    # Notice that the way this works might not be extremely straightforward.
    # The returns are expected to be in % while the weights are not.
    # Will fix this in the next iteration.
    def __init__(self, portfolio_weight, benchmark_weight, portfolio_return, benchmark_return):
        self.portfolio_weight = portfolio_weight
        self.benchmark_weight = benchmark_weight
        self.portfolio_return = portfolio_return
        self.benchmark_return = benchmark_return

    def get_allocation(self, _benchmark_total_return):
        return (self.portfolio_weight - self.benchmark_weight) * (self.benchmark_return - _benchmark_total_return)

    def get_selection(self):
        return self.benchmark_weight * (self.portfolio_return - self.benchmark_return)

    def get_interaction(self):
        return (self.portfolio_weight - self.benchmark_weight) * (self.portfolio_return - self.benchmark_return)

    def get_top_down_allocation(self, _benchmark_total_return):
        return self.get_allocation(_benchmark_total_return)

    def get_bottom_up_allocation(self, _benchmark_total_return):
        return (self.portfolio_weight - self.benchmark_weight) * (self.portfolio_return - _benchmark_total_return)

    def get_top_down_selection(self):
        return self.portfolio_weight * (self.portfolio_return - self.benchmark_return)

    def get_bottom_up_selection(self):
        return self.get_selection()

# Q4.
# Asset class   Portfolio weight    Benchmark weight    Portfolio return    Benchmark return
# Equity                60                  60                  5.95                5.42
# Fixed Income          35                  40                  –0.58               –0.55
# Cash                  5                   0                   0.10                0.10


equity = Asset(0.6, 0.6, 5.95, 5.42)
fixed_income = Asset(0.35, 0.4, -0.58, -0.55)
cash = Asset(0.05, 0, 0.1, 0.1)
assets = np.array([equity, fixed_income, cash])
benchmark_total_return = sum(map(lambda asset: asset.benchmark_weight * asset.benchmark_return, assets))

# Calculate the performance attribution effects for the month:
# a. Original form of allocation, selection, and interaction effects.
original_allocations = list(map(lambda asset: my_round(asset.get_allocation(benchmark_total_return)), assets))
original_selections = list(map(lambda asset: my_round(asset.get_selection()), assets))
original_interactions = list(map(lambda asset: my_round(asset.get_interaction()), assets))
my_print(['Q4. (a)',
          f'Original Allocation:    {original_allocations}',
          f'Original Selection:     {original_selections}',
          f'Original Interaction:   {original_interactions}'])

# b. Top-down form of allocation and selection effects,
top_down_allocations = list(map(lambda asset: my_round(asset.get_top_down_allocation(benchmark_total_return)), assets))
top_down_selections = list(map(lambda asset: my_round(asset.get_top_down_selection()), assets))

my_print(['(b)',
          f'Top-down Allocation:    {top_down_allocations}',
          f'Top-down Selection:     {top_down_selections}'])

# c. Bottom-up form of allocation and selection effects.
bottom_up_allocations = list(map(lambda asset: my_round(asset.get_bottom_up_allocation(benchmark_total_return)), assets))
bottom_up_selections = list(map(lambda asset: my_round(asset.get_bottom_up_selection()), assets))

my_print(['(c)',
          f'Bottom-up Allocation:    {bottom_up_allocations}',
          f'Bottom-up Selection:     {bottom_up_selections}'])


# Which form strikes you as most informative? Why? There is no “right” answer – the intent of the question
# is to give you an opportunity to think about the different forms.
