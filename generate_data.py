import csv
import random
from datetime import date, timedelta

random.seed(42)  # same data every time you run it

operators = ["Jio", "Airtel", "Vi", "BSNL"]
# Make BSNL a bit less reliable and Jio a bit more reliable, so patterns exist
operator_weights = [0.28, 0.28, 0.20, 0.24]

cities = ["Solapur", "Pune", "Mumbai", "Nagpur", "Nashik", "Hyderabad", "Bengaluru", "Delhi"]
causes = ["Power failure", "Fiber cut", "Tower fault", "Maintenance", "Heavy rain", "Congestion"]
cause_weights = [0.25, 0.20, 0.20, 0.15, 0.12, 0.08]

start = date(2026, 1, 1)
days = 300
rows = []

for _ in range(1000):
    op = random.choices(operators, operator_weights)[0]
    city = random.choice(cities)
    cause = random.choices(causes, cause_weights)[0]
    d = start + timedelta(days=random.randint(0, days - 1))
    hour = random.choices(range(24), weights=[2]*6 + [3]*6 + [4]*6 + [6]*6)[0]

    base = {"Power failure": 90, "Fiber cut": 150, "Tower fault": 60,
            "Maintenance": 45, "Heavy rain": 100, "Congestion": 25}[cause]
    duration = max(5, int(random.gauss(base, base * 0.4)))
    if op == "BSNL":
        duration = int(duration * 1.3)

    rows.append([d.isoformat(), hour, op, city, duration, cause])

rows.sort(key=lambda r: r[0])

with open("outages.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "hour", "operator", "city", "duration_minutes", "cause"])
    writer.writerows(rows)

print("Created outages.csv with", len(rows), "rows")