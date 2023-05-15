import pandas as pd

# Create an empty DataFrame with the desired columns
columns = ['code', 'description', 'price', 'benefits', 'duration', 'img']
df = pd.DataFrame(columns=columns)

# Write the DataFrame to a CSV file
df.to_csv('products.csv', index=False)