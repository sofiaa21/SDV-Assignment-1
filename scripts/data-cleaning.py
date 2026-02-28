import pandas as pd

# --- STEP 1: LOAD DATA ---
print("--- Loading Datasets ---")
pre2018_data = pd.read_csv('data/raw-data/Police_Department_Incident_Reports__Historical_2003_to_May_2018_20260227.csv')
post2018_data = pd.read_csv('data/raw-data/Police_Department_Incident_Reports__2018_to_Present_20260227.csv')

print(f"Pre-2018 Data loaded: {pre2018_data.shape[0]} rows")
print(f"Post-2018 Data loaded: {post2018_data.shape[0]} rows")

# --- STEP 2: CLEAN PRE-2018 DATA ---
print("\n--- Processing Pre-2018 Data ---")

# Combine Date and Time into a single Pandas Datetime object
pre2018_data['Incident Datetime'] = pd.to_datetime(pre2018_data['Date'] + ' ' + pre2018_data['Time'])
print("Converted 'Date' and 'Time' strings to unified Datetime objects.")

# Standardize column names to match the modern format
# Mapping: X -> Longitude, Y -> Latitude
pre_rename_map = {
    'IncidntNum': 'Incident Number',
    'Category': 'Incident Category',
    'Descript': 'Incident Description',
    'PdDistrict': 'Police District',
    'X': 'Longitude',
    'Y': 'Latitude',
    'DayOfWeek' : 'Incident Day of Week'
}
pre2018_data = pre2018_data.rename(columns=pre_rename_map)

# Define the final schema we want to keep
shared_cols = [
    'Incident Number', 'Incident Datetime', 'Incident Category', 
    'Incident Description', 'Police District', 'Resolution', 
    'Latitude', 'Longitude', 'Incident Day of Week'
]

pre_clean = pre2018_data[shared_cols].copy()
print(f"Pre-2018 columns aligned. Sample coordinates: Lat {pre_clean['Latitude'].iloc[0]}, Long {pre_clean['Longitude'].iloc[0]}")

# --- FILTER OUT 2018 FROM HISTORICAL DATA ---
print("\n--- Filtering out 2018 from Historical Data ---")
pre_clean = pre_clean[pd.to_datetime(pre_clean['Incident Datetime']).dt.year < 2018]
print(f"Pre-2018 data after removing 2018: {len(pre_clean)} rows")

# --- STEP 3: CLEAN POST-2018 DATA ---
print("\n--- Processing Post-2018 Data ---")

# Convert the modern datetime column
# Specifying format: Year/Month/Day Hour(12-hr):Minute:Second AM/PM
post2018_data['Incident Datetime'] = pd.to_datetime(
    post2018_data['Incident Datetime'], 
    format='%Y/%m/%d %I:%M:%S %p'
)

# Slice only the columns we need (names already align with our shared_cols)
post_clean = post2018_data[shared_cols].copy()
print(f"Post-2018 columns aligned. {len(post_clean.columns)} columns retained.")

# --- STEP 4: MERGE DATASETS ---
print("\n--- Merging Datasets ---")
sf_crime_combined = pd.concat([pre_clean, post_clean], ignore_index=True)
print(f"Combined Dataframe Shape: {sf_crime_combined.shape}")

# --- STEP 5: STANDARDIZE DISTRICT NAMES ---
print("\n--- Standardizing Police Districts ---")
before_districts = sf_crime_combined['Police District'].unique()[:5]
print(f"Example district names before: {before_districts}")

# Convert 'MISSION' or 'mission' to 'Mission'
sf_crime_combined['Police District'] = sf_crime_combined['Police District'].str.title()

after_districts = sf_crime_combined['Police District'].unique()
print(f"Example district names after: {after_districts}")
print(f"Number of retained districts: {len(after_districts)}")

# --- STEP 6: FILTER FOR COMPLETE YEARS ---
print("\n--- Filtering Years ---")
sf_crime_combined['Year'] = sf_crime_combined['Incident Datetime'].dt.year

# Drop the current year (2026) because it is incomplete
# And drop any rows with missing essential data
initial_count = len(sf_crime_combined)
df_final = sf_crime_combined[sf_crime_combined['Year'] < 2026].dropna(subset=['Incident Category', 'Police District'])

rows_dropped = initial_count - len(df_final)
print(f"Dropped {rows_dropped} rows (incomplete years or null values).")
print(f"Dataset now spans years: {sorted(df_final['Year'].unique())}")

# --- STEP 7: EXPORT CLEANED DATA ---
print("\n--- Exporting Data ---")

# Define the output path
output_path = 'data/clean-data/sf_clean_data.csv'

# Save to CSV, ignoring the dataframe's index
df_final.to_csv(output_path, index=False)

print(f"Success! Cleaned data saved to: {output_path}")
print("--- SCRIPT COMPLETE ---")