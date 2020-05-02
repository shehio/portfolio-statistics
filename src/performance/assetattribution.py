class AssetAttribution:
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
