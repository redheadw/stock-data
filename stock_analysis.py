# Pandas is a programmable spreadsheet, with named columns of data and an index
import pandas as pd 
import matplotlib.pyplot as plt

# Load CSV files from the data folder
index_data = pd.read_csv('data/indexData.csv')
#index_info = pd.read_csv('data/indexInfo.csv')
index_Processed = pd.read_csv('data/indexProcessed.csv')

# check: Print the first few rows of on of the files
#print(index_data.head())

# Strip spaces from column names
index_data.columns = index_data.columns.str.strip()
index_Processed.columns = index_Processed.columns.str.strip()

# Convert columns to numeric
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Create a list for datasets
datasets = []

# Clean datasets
for name, df in [('index_data', index_data), ('index_info', index_Processed)]:
    print(f'\nProcessing {name}...')
    
    # Remove column names
    df.columns = df.columns.str.strip()
    
    # Show column names
    print(f'Columns: {df.columns.tolist()}')

    # Skip missing columns
    missing_cols =[col for col in numeric_cols if col not in df.columns]
    if missing_cols:
        print(f'Skipping {name}: Missing columns {missing_cols}') 
        continue

    # Convert columns to numeric
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Convert 'Date' to datetime and extract year
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date', 'Close'], inplace=True)
    df['Year'] = df['Date'].dt.year

    # Calculate volatility
    df['Volatility'] = df['High'] - df['Low']

    # Add to dataset list
    datasets.append((name, df))

# Plot both datasets if valid
if len(datasets) >= 2:
    (name1, df1), (name2, df2) = datasets 

    # 1. Compare Average Close Price
    avg_close_data = df1.groupby('Year')['Close'].mean()
    avg_close_Processed = df2.groupby('Year')['Close'].mean()

    plt.figure(figsize=(10, 5))
    avg_close_data.plot(label=name1, marker='o')
    avg_close_Processed.plot(label=name2, marker='x')
    plt.title('Average Closing Price Comparison by Year')
    plt.xlabel('Year')
    plt.ylabel('Avg Close Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Volume Trend Visualization
    volume_data = df1.groupby('Year')['Volume'].mean()
    volume_Processed = df2.groupby('Year')['Volume'].mean()

    plt.figure(figsize=(10, 5))
    volume_data.plot(label=name1, marker='o')
    volume_Processed.plot(label=name2, marker='x')
    plt.title('Average Volume Comparison by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Volume')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 3. Volatility Trend (High - Low Spread)
    volatility_data = df1.groupby('Year')['Volatility'].mean()
    volatility_Processed = df2.groupby('Year')['Volatility'].mean()

    plt.figure(figsize=(10, 5))
    volatility_data.plot(label=name1, marker='o')
    volatility_Processed.plot(label=name2, marker='x')
    plt.title('Average Volatility (High - Low) Comparison by Year')
    plt.xlabel('Year')
    plt.ylabel('Volatility')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print('\nNot enough valid data sets.')
    























