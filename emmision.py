import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# Parameters
initial_reward = 25            # Initial block reward
block_time_minutes = 1       # Block time in minutes
blocks_per_day = (24 * 60) / block_time_minutes
blocks_per_year = int(blocks_per_day * 365)
decay_rate = 0.071             # 7.1% decay every 6 months
decay_cycles_per_year = 2
years = 50

# Initialize
yearly_data = []
reward = initial_reward
cumulative_supply = 0

# Generate data
for year in range(1, years + 1):
    annual_reward = 0
    for cycle in range(decay_cycles_per_year):
        blocks_in_half_year = blocks_per_year // decay_cycles_per_year
        cycle_reward = reward * blocks_in_half_year
        annual_reward += cycle_reward
        reward *= (1 - decay_rate)

    cumulative_supply += annual_reward
    yearly_data.append({
        "Year": year,
        "Annual Issuance": round(annual_reward, 2),
        "Total Supply": round(cumulative_supply, 2)
    })

# Create DataFrame
df = pd.DataFrame(yearly_data)

# Print table to console
print(df.to_string(index=False))

# Save chart
plt.figure(figsize=(10, 5))
plt.plot(df["Year"], df["Total Supply"], label="Total Supply", color='blue')
plt.title("Yearly Total Coin Supply Over 50 Years")
plt.xlabel("Year")
plt.ylabel("Total Supply")
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.savefig("supply_curve.png")

# Save table as PNG
fig, ax = plt.subplots(figsize=(10, 12))
ax.axis('off')
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    loc='center',
    cellLoc='right',
    colLoc='right'
)
table.scale(1, 1.5)
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.tight_layout()
plt.savefig("supply_table.png", dpi=200)

print("\nSaved: supply_curve.png and supply_table.png")
