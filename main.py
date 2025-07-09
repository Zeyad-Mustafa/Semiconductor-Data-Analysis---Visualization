import pandas as pd

# Read the CSV file
data = pd.read_csv('wafer_data.csv')

# Show the first few rows
print(data.head())

# Basic statistics
print("Average Yield:", data['Yield_Percentage'].mean())
print("Max Defect Count:", data['Defect_Count'].max())
import matplotlib.pyplot as plt

# Plot yield percentage for each wafer
plt.figure(figsize=(8, 4))
plt.bar(data['Wafer_ID'], data['Yield_Percentage'])
plt.xlabel('Wafer ID')
plt.ylabel('Yield Percentage')
plt.title('Yield Percentage per Wafer')
plt.show()

# Plot defect count over time
plt.figure(figsize=(8, 4))
plt.plot(data['Date'], data['Defect_Count'], marker='o')
plt.xlabel('Date')
plt.ylabel('Defect Count')
plt.title('Defect Count Over Time')
plt.show()

