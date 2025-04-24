import random
import time
from datetime import datetime, timedelta

class IntradayStockSimulator:
    def __init__(self):
        self.balance = 0.0
        self.positions = []
        self.history = []
        self.start_time = datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
        self.current_time = self.start_time

    def invest(self, amount, stock, entry_price):
        quantity = amount / entry_price
        position = {
            'stock': stock,
            'entry_price': entry_price,
            'quantity': quantity,
            'invested': amount,
            'time': self.current_time
        }
        self.positions.append(position)
        self.balance -= amount
        self.history.append((self.current_time, f"Invested ₹{amount:.2f} in {stock} at ₹{entry_price:.2f}"))

    def withdraw(self, stock, current_price):
        new_positions = []
        for pos in self.positions:
            if pos['stock'] == stock:
                proceeds = pos['quantity'] * current_price
                pnl = proceeds - pos['invested']
                self.balance += proceeds
                self.history.append((self.current_time, f"Withdrew ₹{proceeds:.2f} from {stock} at ₹{current_price:.2f}. PnL: ₹{pnl:.2f}"))
            else:
                new_positions.append(pos)
        self.positions = new_positions

    def advance_time(self, minutes=1):
        self.current_time += timedelta(minutes=minutes)

    def simulate_market_movement(self, stock, base_price):
        return round(base_price + random.uniform(-1.5, 1.5), 2)

    def summary(self):
        print("\n[Simulation Summary as of", self.current_time.strftime('%H:%M'), "]")
        for log in self.history:
            print(log[0].strftime('%H:%M'), ":", log[1])
        print("Current Balance: ₹{:.2f}".format(self.balance))
        for pos in self.positions:
            print(f"Holding {pos['stock']} - Qty: {pos['quantity']:.2f}, Entry Price: ₹{pos['entry_price']:.2f}")


# Example usage:
sim = IntradayStockSimulator()
sim.invest(10000, 'INFY', 1550.25)
sim.advance_time(5)
price = sim.simulate_market_movement('INFY', 1550.25)
sim.withdraw('INFY', price)
sim.invest(30000, 'SUZLON', 46.85)  # Simulated entry price

# Extended real-time simulation
base_price = 46.85
for _ in range(60):  # Simulate 60 minutes of trading
    sim.advance_time(1)
    price = sim.simulate_market_movement('SUZLON', base_price)
    sim.history.append((sim.current_time, f"Current SUZLON price: ₹{price:.2f}"))
    time.sleep(1)  # Simulate 1-second wait per minute for demo purposes

sim.summary()
