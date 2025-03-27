from algopy import ARC4Contract, Account, Application, UInt64, op, subroutine
from algopy.arc4 import abimethod


class getAlgoPriceContract(ARC4Contract):
    def __init__(self) -> None:
        self.usdc_pool_address = Account('UDFWT5DW3X5RZQYXKQEMZ6MRWAEYHWYP7YUAPZKPW6WJK3JH3OZPL7PO2Y')
        self.tinyman_router = Application(148607000)

    @abimethod
    def callGetScaledAlgoPrice(
        self
    ) -> UInt64:
        
        USDC_reserve = op.AppLocal.get_ex_uint64(self.usdc_pool_address, self.tinyman_router, b'asset_1_reserves')[0]
        ALGO_reserve = op.AppLocal.get_ex_uint64(self.usdc_pool_address, self.tinyman_router, b'asset_2_reserves')[0]

        SCALE_FACTOR = UInt64(1_000_000)

        return USDC_reserve * SCALE_FACTOR // ALGO_reserve
    

    @subroutine
    def getScaledAlgoPrice(
        self
    ) -> UInt64:
        
        USDC_reserve = op.AppLocal.get_ex_uint64(self.usdc_pool_address, self.tinyman_router, b'asset_1_reserves')[0]
        ALGO_reserve = op.AppLocal.get_ex_uint64(self.usdc_pool_address, self.tinyman_router, b'asset_2_reserves')[0]

        SCALE_FACTOR = UInt64(10_000)

        return USDC_reserve * SCALE_FACTOR // ALGO_reserve
    

    @abimethod
    def getTargetUSDCAmountInAlgo(
        self,
        target_usdc: UInt64
    ) -> UInt64:
        
        scaled_algo_price = self.getScaledAlgoPrice()

        SCALE_FACTOR = UInt64(1_000_000)

        amount_in_algo = target_usdc * SCALE_FACTOR // scaled_algo_price

        return amount_in_algo
