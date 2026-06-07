import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host     = 'localhost',
    user     = 'root',           # your MySQL username
    password = 'vardhan',  # your MySQL password
    database = 'ola_db'
)

cursor = conn.cursor()

# Drop table if exists and recreate
cursor.execute("DROP TABLE IF EXISTS ola_rides")

cursor.execute("""
CREATE TABLE ola_rides (
    Date                        TEXT,
    Time                        TEXT,
    Booking_ID                  TEXT,
    Booking_Status              TEXT,
    Customer_ID                 TEXT,
    Vehicle_Type                TEXT,
    Pickup_Location             TEXT,
    Drop_Location               TEXT,
    V_TAT                       INT,
    C_TAT                       INT,
    Canceled_Rides_by_Customer  TEXT,
    Canceled_Rides_by_Driver    TEXT,
    Incomplete_Rides            TEXT,
    Incomplete_Rides_Reason     TEXT,
    Booking_Value               INT,
    Payment_Method              TEXT,
    Ride_Distance               INT,
    Driver_Ratings              INT,
    Customer_Rating             INT,
    Day                         INT,
    Month                       INT,
    DayOfWeek                   TEXT,
    Hour                        INT
)
""")
print("Table created ✅")

# Load CSV
df = pd.read_csv('OLA_Cleaned.csv')
print(f"CSV loaded: {len(df):,} rows")

# Insert rows in batches
batch_size = 1000
rows = [tuple(row) for row in df.values]
cols = ', '.join(df.columns.tolist())
placeholders = ', '.join(['%s'] * len(df.columns))

for i in range(0, len(rows), batch_size):
    cursor.executemany(
        f"INSERT INTO ola_rides ({cols}) VALUES ({placeholders})",
        rows[i:i+batch_size]
    )
    conn.commit()
    print(f"Inserted {min(i+batch_size, len(rows)):,} / {len(rows):,} rows...", end='\r')

print("\nAll rows inserted ✅")
cursor.execute("SELECT COUNT(*) FROM ola_rides")
print(f"Total rows in MySQL: {cursor.fetchone()[0]:,}")

cursor.close()
conn.close()
print("\nDone! Your data is now in MySQL ola_db → ola_rides table 🎉")