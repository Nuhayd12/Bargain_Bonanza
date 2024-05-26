from time import sleep, time

class BiddingSystem:
    def _init_(self):
        self.products = {}

    def add_product(self, product_id, min_price, max_price, auction_duration):
        self.products[product_id] = {
            'min_price': min_price,
            'max_price': max_price,
            'auction_duration': auction_duration,
            'start_time': 0,
            'bids': {}
        }

    def place_bid(self, product_id, user_id, bid_amount):
        product = self.products.get(product_id)
        if not product:
            print("Product not found")
            return
        if bid_amount < product['min_price']:
            print("Bid amount is below the minimum price")
            return
        if bid_amount > product['max_price']:
            print("Bid amount exceeds the maximum price")
            return
        if product['start_time'] == 0:
            product['start_time'] = time()
            product['end_time'] = product['start_time'] + product['auction_duration']
        if time() > product['end_time']:
            print("Bidding time has ended")
            return
        
        # Check if there's a tie in the bid
        if self.check_bid_tie(product_id, bid_amount):
            return
        
        product['bids'][user_id] = bid_amount
        print(f"Bid of {bid_amount} placed on product {product_id} by user {user_id}")

    def start_auction(self, product_id):
        self.products[product_id]['start_time'] = time()
        self.products[product_id]['end_time'] = self.products[product_id]['start_time'] + self.products[product_id]['auction_duration']
        print(f"Auction for product {product_id} has started")

    def get_highest_bidder(self, product_id):
        product = self.products.get(product_id)
        if not product['bids']:
            return None
        highest_bidder = max(product['bids'], key=product['bids'].get)
        return highest_bidder

    def get_current_bid(self, product_id):
        product = self.products.get(product_id)
        if not product['bids']:
            return None
        return product['bids'][self.get_highest_bidder(product_id)]

    def check_bid_tie(self, product_id, current_bid):
        product = self.products.get(product_id)
        for user, bid in product['bids'].items():
            if bid == current_bid and user != self.get_highest_bidder(product_id):
                decision = input(f"User {user}, there is a tie with the current highest bid. Do you want to increase your bid? (1 for yes, 0 for no): ")
                if decision == '1':
                    new_bid = int(input(f"Enter your new bid amount: "))
                    if new_bid > current_bid:
                        product['bids'][user] = new_bid
                        print(f"New bid of {new_bid} placed on product {product_id} by user {user}")
                    else:
                        print("New bid amount must be higher than the current highest bid.")
                        continue
                else:
                    print(f"User {user} chose not to increase the bid.")
        return False


# Test the bidding system with immediate timer start and fixed time limit
bidding_system = BiddingSystem()
bidding_system.add_product(1, 100, 500, auction_duration=60)

# Start the auction and place bids for users
bidding_system.start_auction(1)  # Start auction
start_time = time()  # Record the time when the first input is received
user_counter = 1  # Counter to keep track of users
while time() < start_time + 60:
    user_id = input(f"Enter user ID {user_counter}: ")
    bid_amount = int(input(f"Enter bid amount for user {user_counter}: "))
    bidding_system.place_bid(1, user_id, bid_amount)
    user_counter += 1

# Get the winning bidder and the winning bid amount
winning_bidder = bidding_system.get_highest_bidder(1)
winning_bid_amount = bidding_system.get_current_bid(1)

# Print the winning bidder and winning bid amount
if winning_bidder:
    print(f"The winning bidder is {winning_bidder} with a bid of {winning_bid_amount}.")
else:
    print("No valid bids were placed for this product.")