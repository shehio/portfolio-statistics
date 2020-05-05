import numpy as np


class AttributionLinker:

    @staticmethod  # A property could be allocation, selection, or interaction.
    def link_attributions(
            benchmark_returns: np.array(),
            portfolio_returns: np.array(),
            portfolio_attributions: np.array()):

        assert len(benchmark_returns) == len(portfolio_returns)
        assert len(benchmark_returns) == len(portfolio_attributions)

        linked_property = 0
        for benchmark_return, portfolio_return, portfolio_attribution \
                in zip(benchmark_returns, portfolio_returns, portfolio_attributions):
            kt = AttributionLinker.__calculate_kt(portfolio_return, benchmark_return)
            linked_property += (kt * portfolio_attribution)

        return linked_property

    @staticmethod
    def __calculate_kt(benchmark_return, portfolio_return):
        num = np.log(1 + portfolio_return) - np.log(1 + benchmark_return)
        denum = portfolio_return - benchmark_return

        if denum == 0:
            kt = 1 / (1 + portfolio_return)
        else:
            kt = num / denum

        return kt