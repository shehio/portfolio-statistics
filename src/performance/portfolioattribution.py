from src.performance.assetattribution import AssetAttribution

import numpy as np


class PortfolioAttribution:
    def __init__(
            self,
            portfolio_weights: np.array,
            benchmark_weights: np.array,
            portfolio_returns: np.array,
            benchmark_returns: np.array):

        length = len(portfolio_weights)
        assert length == len(benchmark_weights)
        assert length == len(portfolio_returns)
        assert length == len(benchmark_returns)

        self.benchmark_total_return = 0
        for asset_weight, asset_return in zip(benchmark_weights, benchmark_returns):
            self.benchmark_total_return += asset_weight * asset_return

        self.asset_attributions = np.array([], dtype=AssetAttribution)

        for portfolio_weight, benchmark_weight, portfolio_return, benchmark_return in \
                zip(portfolio_weights, benchmark_weights, portfolio_returns, benchmark_returns):
            self.asset_attributions = np.append(
                self.asset_attributions,
                AssetAttribution(portfolio_weight, benchmark_weight, portfolio_return, benchmark_return))

    def get_allocations(self):
        allocations = np.array([])
        for asset_attribution in self.asset_attributions:
            allocations = np.append(allocations, asset_attribution.get_allocation(self.benchmark_total_return))

        return allocations

    def get_selections(self):
        selections = np.array([])
        for asset_attribution in self.asset_attributions:
            selections = np.append(selections, asset_attribution.get_selection())

        return selections

    def get_interactions(self):
        interactions = np.array([])
        for asset_attribution in self.asset_attributions:
            interactions = np.append(interactions, asset_attribution.get_interaction())

        return interactions

    def get_total_attribution(self):
        total_attributions = np.array([])
        for asset_attribution in self.asset_attributions:
            total_attribution = asset_attribution.get_interaction() + \
                                asset_attribution.get_selection() + \
                                asset_attribution.get_interaction()
            total_attributions = np.append(total_attributions, total_attribution)

        return total_attributions
