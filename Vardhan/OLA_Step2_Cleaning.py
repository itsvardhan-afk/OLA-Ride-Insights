# ============================================================
#   OLA RIDE INSIGHTS — STEP 2: DATA CLEANING & PREPROCESSING
# ============================================================
# HOW TO RUN:
#   1. Make sure OLA_DataSet.xlsx is in the same folder
#   2. Open terminal in VS Code
#   3. Run: python OLA_Step2_Cleaning.py
#   4. It will create a new file: OLA_Cleaned.csv
#      (This cleaned file is what you use for SQL in Step 3)
# ============================================================

import pandas as pd

# ============================================================
# SECTION 1 — LOAD THE RAW DATA
# ============================================================

print("=" * 55)
print("LOADING RAW DATA...")
print("=" * 55)

df = pd.read_excel('OLA_DataSet.xlsx')

print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")
print(f"Nulls before cleaning : {df.isnull().sum().sum():,}")
print()


# ============================================================
# SECTION 2 — FIX DATE & TIME COLUMNS
# ============================================================

print("=" * 55)
print("SECTION 2: FIXING DATE & TIME")
print("=" * 55)

# Make sure Date is in proper datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract useful columns from Date
df['Day']        = df['Date'].dt.day
df['Month']      = df['Date'].dt.month
df['DayOfWeek']  = df['Date'].dt.day_name()   # Monday, Tuesday etc.
df['Hour']       = pd.to_datetime(df['Time'].astype(str),
                                   format='%H:%M:%S', errors='coerce').dt.hour

print("Date column fixed ✅")
print("New columns added: Day, Month, DayOfWeek, Hour")
print(df[['Date', 'Day', 'Month', 'DayOfWeek', 'Hour']].head(3))
print()


# ============================================================
# SECTION 3 — FIX MISSING VALUES
# ============================================================

print("=" * 55)
print("SECTION 3: FIXING MISSING VALUES")
print("=" * 55)

# --- Text columns: fill with 'Not Applicable' ---
# Why? Cancelled rides have no cancellation reason — we label it clearly
df['Canceled_Rides_by_Customer'] = df['Canceled_Rides_by_Customer'].fillna('Not Applicable')
df['Canceled_Rides_by_Driver']   = df['Canceled_Rides_by_Driver'].fillna('Not Applicable')
df['Incomplete_Rides_Reason']    = df['Incomplete_Rides_Reason'].fillna('Not Applicable')
df['Payment_Method']             = df['Payment_Method'].fillna('Not Applicable')
print("Text nulls filled with 'Not Applicable' ✅")

# --- Incomplete_Rides: fill with 'No' ---
# Why? If it's null, the ride wasn't marked incomplete → it's 'No'
df['Incomplete_Rides'] = df['Incomplete_Rides'].fillna('No')
print("Incomplete_Rides nulls filled with 'No' ✅")

# --- Ratings: fill with 0 ---
# Why? Cancelled rides have no rating — 0 means 'no rating given'
df['Driver_Ratings']  = df['Driver_Ratings'].fillna(0)
df['Customer_Rating'] = df['Customer_Rating'].fillna(0)
print("Driver_Ratings & Customer_Rating nulls filled with 0 ✅")

# --- V_TAT & C_TAT: fill with 0 ---
# Why? Cancelled rides have no wait time recorded
df['V_TAT'] = df['V_TAT'].fillna(0)
df['C_TAT']  = df['C_TAT'].fillna(0)
print("V_TAT & C_TAT nulls filled with 0 ✅")
print()


# ============================================================
# SECTION 4 — FIX DATA TYPES
# ============================================================

print("=" * 55)
print("SECTION 4: FIXING DATA TYPES")
print("=" * 55)

# Convert ratings to int (no need for decimals like 4.0 → 4)
df['Driver_Ratings']  = df['Driver_Ratings'].astype(int)
df['Customer_Rating'] = df['Customer_Rating'].astype(int)
df['V_TAT']           = df['V_TAT'].astype(int)
df['C_TAT']           = df['C_TAT'].astype(int)

print("Driver_Ratings  → int ✅")
print("Customer_Rating → int ✅")
print("V_TAT, C_TAT    → int ✅")
print()


# ============================================================
# SECTION 5 — REMOVE UNWANTED COLUMNS
# ============================================================

print("=" * 55)
print("SECTION 5: REMOVING UNWANTED COLUMNS")
print("=" * 55)

# 'Vehicle Images' column has image URLs — not useful for analysis
df.drop(columns=['Vehicle Images'], inplace=True)
print("Dropped 'Vehicle Images' column ✅")
print()


# ============================================================
# SECTION 6 — VERIFY CLEANING
# ============================================================

print("=" * 55)
print("SECTION 6: VERIFICATION")
print("=" * 55)

print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")
print(f"Nulls after cleaning : {df.isnull().sum().sum()}")
print()
print("Null count per column:")
print(df.isnull().sum())
print()
print("Data types after cleaning:")
print(df.dtypes)
print()
print("Sample cleaned row (a cancelled ride):")
sample = df[df['Booking_Status'] == 'Canceled by Driver'].iloc[0]
print(sample[['Booking_Status', 'Payment_Method',
              'Driver_Ratings', 'Canceled_Rides_by_Driver']])
print()


# ============================================================
# SECTION 7 — SAVE CLEANED DATA
# ============================================================

print("=" * 55)
print("SECTION 7: SAVING CLEANED FILE")
print("=" * 55)

df.to_csv('OLA_Cleaned.csv', index=False)
print("Saved as: OLA_Cleaned.csv ✅")
print()
print("=" * 55)
print("STEP 2 COMPLETE!")
print("=" * 55)
print()
print("Summary of what was cleaned:")
print("  • Date column   → converted to proper datetime")
print("  • New columns   → Day, Month, DayOfWeek, Hour added")
print("  • Text nulls    → filled with 'Not Applicable'")
print("  • Rating nulls  → filled with 0 (no rating given)")
print("  • TAT nulls     → filled with 0")
print("  • Image URLs    → removed (not needed)")
print(f"  • Final shape   → {df.shape[0]:,} rows × {df.shape[1]} columns")
print()
print("Next step → Load OLA_Cleaned.csv into MySQL for SQL queries!")
