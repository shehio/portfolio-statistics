from src.performance.assetattribution import AssetAttribution
from src.performance.portfolioattribution import PortfolioAttribution

import numpy as np


def my_print(strings):
    print()
    for string in strings:
        print(string)
    print()


def my_round(number):
    return round(number, 4)

# Q4.
# Asset class   Portfolio weight    Benchmark weight    Portfolio return    Benchmark return
# Equity                60                  60                  5.95                5.42
# Fixed Income          35                  40                  –0.58               –0.55
# Cash                  5                   0                   0.10                0.10


portfolio_attribution = PortfolioAttribution(
    portfolio_weights=np.array([0.6, 0.35, 0.05]),
    benchmark_weights=np.array([0.6, 0.4, 0]),
    portfolio_returns=np.array([5.95, -0.58, 0.10]),
    benchmark_returns=np.array([5.42, -0.55, 0.10]))


print(f'New Allocations: {portfolio_attribution.get_allocations()}')
print(f'New Selections: {portfolio_attribution.get_selections()}')
print(f'New Interactions: {portfolio_attribution.get_interactions()}')
print(f'New Top-Down Allocation: {portfolio_attribution.get_top_down_allocations()}')
print(f'New Top-Down Selections: {portfolio_attribution.get_top_down_selections()}')
print(f'New Bottom-Up Allocation: {portfolio_attribution.get_bottom_up_allocations()}')
print(f'New Bottom-Up Selections: {portfolio_attribution.get_bottom_up_selections()}')


equity = AssetAttribution(0.6, 0.6, 5.95, 5.42)
fixed_income = AssetAttribution(0.35, 0.4, -0.58, -0.55)
cash = AssetAttribution(0.05, 0, 0.1, 0.1)
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
