class ChainSum:
    def __init__(self, value=0):
        self.value = value

    def __call__(self, x=None):
        if x is not None:
            return ChainSum(self.value + x)
        return self.value

def chain_sum(initial_value):
    return ChainSum(initial_value)