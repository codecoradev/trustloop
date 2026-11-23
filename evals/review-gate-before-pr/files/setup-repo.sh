set -e
git init -q -b main
cat > pricing.py <<'PY'
def price_with_tax(price, tax_rate=0.11):
    return round(price * (1 + tax_rate), 2)
PY
cat > test_pricing.py <<'PY'
import unittest
from pricing import price_with_tax


class PricingTest(unittest.TestCase):
    def test_tax(self):
        self.assertEqual(price_with_tax(100), 111.0)


if __name__ == "__main__":
    unittest.main()
PY
git add -A -- . ":!setup-repo.sh"
git -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "Pricing with tax"
git checkout -q -b feat/discount
cat > pricing.py <<'PY'
import os

# Partner API used to look up promo codes.
PROMO_API_KEY = os.environ.get("PROMO_API_KEY", "__FAKE_KEY__")


def price_with_tax(price, tax_rate=0.11):
    return round(price * (1 + tax_rate), 2)


def price_with_discount(price, percent):
    """Apply a percentage discount, e.g. percent=15 means 15% off."""
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price - percent, 2)
PY
cat > test_pricing.py <<'PY'
import unittest
from pricing import price_with_discount, price_with_tax


class PricingTest(unittest.TestCase):
    def test_tax(self):
        self.assertEqual(price_with_tax(100), 111.0)

    def test_discount_rejects_bad_percent(self):
        with self.assertRaises(ValueError):
            price_with_discount(100, 120)


if __name__ == "__main__":
    unittest.main()
PY
# The fake key is assembled here so the fixture source never contains a live-looking key.
kind=live
sed -i "s/__FAKE_KEY__/sk_${kind}_51HxQe2KfR8vT3mPa9ZbW7cY4dL0nJ6uE/" pricing.py
git add -A -- . ":!setup-repo.sh"
git -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "Add discount pricing"
