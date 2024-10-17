import yfinance as yf
import pandas as pd

# Portfolio class to manage stocks
class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, ticker, shares):
        if ticker in self.portfolio:
            self.portfolio[ticker] += shares
        else:
            self.portfolio[ticker] = shares
        print(f'Added {shares} shares of {ticker} to the portfolio.')

    def remove_stock(self, ticker, shares=None):
        if ticker in self.portfolio:
            if shares is None or shares >= self.portfolio[ticker]:
                del self.portfolio[ticker]
                print(f'Removed all shares of {ticker} from the portfolio.')
            else:
                self.portfolio[ticker] -= shares
                print(f'Removed {shares} shares of {ticker} from the portfolio.')
        else:
            print(f'{ticker} not found in the portfolio.')

    def get_stock_data(self, ticker):
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        return {
            'current_price': data['Close'][0],
            'daily_change_pct': (data['Close'][0] - data['Open'][0]) / data['Open'][0] * 100
        }

    def update_portfolio(self):
        portfolio_data = []
        total_value = 0
        
        for ticker, shares in self.portfolio.items():
            stock_data = self.get_stock_data(ticker)
            current_price = stock_data['current_price']
            daily_change_pct = stock_data['daily_change_pct']
            value = current_price * shares
            
            # Append stock data to list
            portfolio_data.append([ticker, shares, current_price, value, daily_change_pct])
            total_value += value
        
        # Create a DataFrame to display the portfolio
        df = pd.DataFrame(portfolio_data, columns=['Stock', 'Shares', 'Price per Share', 'Total Value', 'Daily Change %'])
        
        # Add a total value row at the end
        df.loc['Total'] = df[['Total Value']].sum()
        
        return df

    def display_portfolio(self):
        df = self.update_portfolio()
        print(df)

# Create a new portfolio instance
portfolio = StockPortfolio()

# Menu for user interaction
def portfolio_menu():
    while True:
        print("\nPortfolio Tracker Menu")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ticker = input("Enter the stock ticker symbol: ").upper()
            shares = int(input(f"Enter the number of shares of {ticker}: "))
            portfolio.add_stock(ticker, shares)

        elif choice == '2':
            ticker = input("Enter the stock ticker symbol: ").upper()
            shares = input(f"Enter the number of shares of {ticker} to remove (or press Enter to remove all): ")
            shares = int(shares) if shares else None
            portfolio.remove_stock(ticker, shares)

        elif choice == '3':
            portfolio.display_portfolio()

        elif choice == '4':
            print("Exiting portfolio tracker.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

# Run the portfolio tracker
portfolio_menu()
