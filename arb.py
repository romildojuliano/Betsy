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

    def __init__(self, odd_a: float, odd_b: float, odd_draw: float) -> None:
        self.odd_a = odd_a
        self.odd_b = odd_b
        self.odd_draw = odd_draw
        self.tip = (1 / self.odd_a + 1 / self.odd_b + 1 / self.odd_draw)
        self.profit = (1 - self.tip)
        print(f'total implied probability: {self.tip*100:.2f}%')

    def calculate_bets(self) -> None:
        if self.profit > 0:
            print('----------------------------------')
            self.total_bet = float(input('total bet: '))
            print(f'profit margin: {self.profit*100:.2f}%')
            print(f'expected profit: R$ {self.total_bet*self.profit:.2f}')
            self.bet_a = (self.total_bet * (1 / self.odd_a)) / self.tip
            self.bet_b = (self.total_bet * (1 / self.odd_b)) / self.tip
            self.bet_draw = (self.total_bet * (1 / self.odd_draw)) / self.tip
            print('----------------------------------')
            print(f'bet on outcome A: R$ {self.bet_a:.2f}')
            print(f'bet on outcome B: R$ {self.bet_b:.2f}')
            print(f'bet on draw: R$ {self.bet_draw:.2f}')
        else:
            print(
                "Can't guarantee profit with total implied probability greater than 100%")


if __name__ == '__main__':
    odd_a = float(input('odd for outcome A: '))
    odd_b = float(input('odd for outcome B: '))
    odd_draw = float(input('odd for draw: '))
    arb = Arbitrage(odd_a, odd_b, odd_draw)
    arb.calculate_bets()
