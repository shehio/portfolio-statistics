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

        self.portfolio_weights = portfolio_weights
        self.benchmark_weights = benchmark_weights
        self.portfolio_returns = portfolio_returns
        self.benchmark_returns = benchmark_returns

        self.benchmark_total_return = 0
        for asset_weight, asset_return in zip(self.benchmark_weights, self.benchmark_returns):
            self.benchmark_total_return += asset_weight * asset_return

    def get_allocations(self):
        allocations = np.array([])
        for portfolio_weight, benchmark_weight, benchmark_return in \
                zip(self.portfolio_weights, self.benchmark_weights, self.benchmark_returns):
            allocations = np.append(
                allocations,
                (portfolio_weight - benchmark_weight) * (benchmark_return - self.benchmark_total_return))

        return allocations

    def get_selections(self):
        selections = np.array([])
        for portfolio_return, benchmark_weight, benchmark_return in \
                zip(self.portfolio_returns, self.benchmark_weights, self.benchmark_returns):
            selections = np.append(
                selections,
                benchmark_weight * (portfolio_return - benchmark_return))

        return selections

    def get_interactions(self):
        interactions = np.array([])
        for benchmark_weight, benchmark_return, portfolio_weight, portfolio_return in \
                zip(self.benchmark_weights, self.benchmark_returns, self.benchmark_weights, self.portfolio_returns):
            interactions = np.append(
                interactions,
                (portfolio_weight - benchmark_weight) * (portfolio_return - benchmark_return))

        return interactions
