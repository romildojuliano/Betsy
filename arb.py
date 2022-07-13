import pandas as pd
import numpy as np

class Arbitrage:
    odd_a: float
    odd_b: float
    odd_draw: float
    tip: float
    profit: float
    total_bet: float
    bet_a: float
    bet_b: float
    bet_draw: float
    platform: str

    def __init__(self, odd_a: float, odd_b: float, odd_draw: float, platform: str, total_bet: float = np.NaN) -> None:
        self.odd_a = odd_a
        self.odd_b = odd_b
        self.odd_draw = odd_draw
        self.total_bet = total_bet
        self.platform = platform
        self.tip = (1 / self.odd_a + 1 / self.odd_b + 1 / self.odd_draw)
        self.profit = (1 - self.tip)
        print(f'Total implied probability: {self.tip*100:.2f}%')

    def calculate_bets(self, verbose: bool = False, user_input: bool = False) -> pd.DataFrame:
        """Insert docstring here

        Args:
            verbose (bool, optional): Shows detailed info about the process. Defaults to False.
            user_input (bool, optional): Determines if the value is given by input or parameter. Defaults to False.

        Returns:
            pd.DataFrame: Dataframe containing data about the bet
        """
        if user_input == True:
            self.total_bet = float(input('total bet: '))

        self.bet_a = (self.total_bet * (1 / self.odd_a)) / self.tip
        self.bet_b = (self.total_bet * (1 / self.odd_b)) / self.tip
        self.bet_draw = (self.total_bet * (1 / self.odd_draw)) / self.tip

        if verbose == True:
            print('----------------------------------')
            print(f'Profit margin: {self.profit*100:.2f}%')
            print(f'Expected profit: R$ {self.total_bet*self.profit:.2f}')
            print('----------------------------------')
            print(f'Bet on outcome A: R$ {self.bet_a:.2f}')
            print(f'Bet on outcome B: R$ {self.bet_b:.2f}')
            print(f'Bet on draw: R$ {self.bet_draw:.2f}')

            if self.profit < 0:
                print(
                    "Can't guarantee profit with total implied probability \
                    greater than 100%"
                )
        
        # Returns a pandas dataframe that can be used to store some bets
        # if you plan on storing multiple values, you may want to append
        # these values on some kind of main dataframe.
        return pd.DataFrame(
            data={
                "Odd a":            [self.odd_a],
                "Odd Draw":         [self.odd_draw],
                "Odd b":            [self.odd_b],
                "Bet a":            [self.bet_a],
                "Draw" :            [self.bet_draw],
                "Bet b":            [self.bet_b],
                "Profit Rate":      [self.profit],
                "Expected Profit":  [self.profit*self.total_bet]
            },
            index=[self.platform]
        )

if __name__ == '__main__':
    # Using user input
    '''
    odd_a = float(input('odd for outcome A: '))
    odd_b = float(input('odd for outcome B: '))
    odd_draw = float(input('odd for draw: '))
    arb = Arbitrage(odd_a, odd_b, odd_draw)
    df = arb.calculate_bets(verbose=True)
    print(df)
    '''
    
    # Using constructor itself
    generic_bet = Arbitrage(
        odd_a=1.34, 
        odd_b=8.86, 
        odd_draw=5.29, 
        total_bet=2500,
        platform="BETSY"
    ).calculate_bets()

    print(generic_bet)
