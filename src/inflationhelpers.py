class InflationHelpers:
    @staticmethod
    def get_inflation(cpi_1: float, cpi_2: float):
        return (cpi_2 / cpi_1 - 1) * 100


