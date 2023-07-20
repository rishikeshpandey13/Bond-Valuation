import datetime

class Bond:
    def __init__(self, coupon_rate, face_value, maturity_date, coupon_frequency):
        self.coupon_rate = coupon_rate
        self.face_value = face_value
        self.maturity_date = maturity_date
        self.coupon_frequency = coupon_frequency

    def calculate_present_value(self, discount_rate):
        cash_flows = self.calculate_cash_flows()
        present_value = sum(c / (1 + discount_rate) ** (i + 1) for i, c in enumerate(cash_flows))
        return present_value

    def calculate_yield_to_maturity(self, present_value):
        guess = 0.05  # Initial guess for yield
        max_iterations = 1000
        tolerance = 0.0001
        i = 0

        while i < max_iterations:
            price = self.calculate_present_value(guess)
            error = price - present_value

            if abs(error) < tolerance:
                return guess

            derivative = (self.calculate_present_value(guess + tolerance) - price) / tolerance
            guess = guess - error / derivative
            i += 1

        raise Exception("Yield to maturity calculation did not converge.")

    def calculate_coupon_payment(self):
        return self.face_value * self.coupon_rate / self.coupon_frequency

    def calculate_cash_flows(self):
        cash_flows = []
        coupon_payment = self.calculate_coupon_payment()
        maturity_date = datetime.datetime.strptime(self.maturity_date, "%Y-%m-%d").date()

        current_date = datetime.date.today()
        while current_date < maturity_date:
            cash_flows.append(coupon_payment)
            current_date += datetime.timedelta(days=365 / self.coupon_frequency)

        cash_flows.append(coupon_payment + self.face_value)
        return cash_flows

    def is_matured(self):
        maturity_date = datetime.datetime.strptime(self.maturity_date, "%Y-%m-%d").date()
        return datetime.date.today() >= maturity_date

    def days_to_maturity(self):
        maturity_date = datetime.datetime.strptime(self.maturity_date, "%Y-%m-%d").date()
        return (maturity_date - datetime.date.today()).days


# Example usage
bond = Bond(coupon_rate=0., face_value=1000, maturity_date="2025-12-31", coupon_frequency=2)

discount_rate = 0.06
present_value = bond.calculate_present_value(discount_rate)
yield_to_maturity = bond.calculate_yield_to_maturity(present_value)

print("Present Value: ", present_value)
print("Yield to Maturity: ", yield_to_maturity)
