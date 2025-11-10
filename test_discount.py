from db import query_one, execute

# Update users to have paid status for testing
execute("UPDATE users SET membership_payment_status='paid' WHERE id=1")  # Silver
execute("UPDATE users SET membership_payment_status='paid' WHERE id=2")  # Basic

# Verify updates
user1 = query_one("SELECT membership, membership_payment_status FROM users WHERE id=1")
user2 = query_one("SELECT membership, membership_payment_status FROM users WHERE id=2")
user3 = query_one("SELECT membership, membership_payment_status FROM users WHERE id=3")

print("User 1 (Silver):", user1)
print("User 2 (Basic):", user2)
print("User 3 (None):", user3)

# Test discount calculation logic
def calculate_discount(user, total_price):
    discount = 0.0
    if user and user['membership'] and user['membership_payment_status'] == 'paid':
        if user['membership'] == 'Basic':
            discount = 0.05  # 5% welcome discount
        elif user['membership'] == 'Silver':
            discount = 0.10  # 10% birthday discount
        elif user['membership'] == 'Gold':
            discount = 0.10  # 10% birthday discount
        elif user['membership'] == 'Platinum':
            discount = 0.20  # 20% store-wide discount
    discounted_price = total_price * (1 - discount)
    return discounted_price, discount

# Test with product price 6788.00
product_price = 6788.00

discounted1, disc1 = calculate_discount(user1, product_price)
discounted2, disc2 = calculate_discount(user2, product_price)
discounted3, disc3 = calculate_discount(user3, product_price)

print(f"\nProduct price: ₱{product_price}")
print(f"Silver membership (10%): ₱{discounted1:.2f} (saved ₱{product_price * disc1:.2f})")
print(f"Basic membership (5%): ₱{discounted2:.2f} (saved ₱{product_price * disc2:.2f})")
print(f"No membership: ₱{discounted3:.2f} (saved ₱{product_price * disc3:.2f})")
