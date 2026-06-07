-- ============================================================
--   OLA RIDE INSIGHTS — STEP 3: SQL QUERIES
-- ============================================================
-- HOW TO RUN:
--   1. Open MySQL Workbench
--   2. Connect to your local server
--   3. Make sure ola_db is selected (USE ola_db;)
--   4. Run each query one by one
--   5. Take a screenshot of each result
-- ============================================================

USE ola_db;

-- ============================================================
-- QUERY 1: Retrieve all successful bookings
-- ============================================================

SELECT *
FROM ola_rides
WHERE Booking_Status = 'Success';

-- Result: 63,967 rows — all rides that completed successfully


-- ============================================================
-- QUERY 2: Find the average ride distance for each vehicle type
-- ============================================================

SELECT
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Avg_Ride_Distance_km
FROM ola_rides
WHERE Booking_Status = 'Success'   -- only count completed rides
GROUP BY Vehicle_Type
ORDER BY Avg_Ride_Distance_km DESC;

-- Result: Prime Sedan has highest avg distance ~15.76 km


-- ============================================================
-- QUERY 3: Get the total number of cancelled rides by customers
-- ============================================================

SELECT
    COUNT(*) AS Total_Cancelled_By_Customer
FROM ola_rides
WHERE Booking_Status = 'Canceled by Customer';

-- Result: 10,499 rides cancelled by customers


-- ============================================================
-- QUERY 4: List the top 5 customers who booked the highest number of rides
-- ============================================================

SELECT
    Customer_ID,
    COUNT(*) AS Total_Bookings
FROM ola_rides
GROUP BY Customer_ID
ORDER BY Total_Bookings DESC
LIMIT 5;

-- Result: Top 5 customers with most bookings


-- ============================================================
-- QUERY 5: Get the number of rides cancelled by drivers
--          due to personal and car-related issues
-- ============================================================

SELECT
    COUNT(*) AS Cancelled_Due_To_Personal_Car_Issues
FROM ola_rides
WHERE Booking_Status = 'Canceled by Driver'
  AND Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Result: 6,542 rides cancelled due to personal & car issues


-- ============================================================
-- QUERY 6: Find the maximum and minimum driver ratings
--          for Prime Sedan bookings
-- ============================================================

SELECT
    MAX(Driver_Ratings) AS Max_Driver_Rating,
    MIN(Driver_Ratings) AS Min_Driver_Rating
FROM ola_rides
WHERE Vehicle_Type = 'Prime Sedan'
  AND Booking_Status = 'Success'   -- only rated rides (not cancelled)
  AND Driver_Ratings > 0;

-- Result: Max = 5, Min = 3


-- ============================================================
-- QUERY 7: Retrieve all rides where payment was made using UPI
-- ============================================================

SELECT *
FROM ola_rides
WHERE Payment_Method = 'UPI';

-- Result: 25,881 rides paid via UPI


-- ============================================================
-- QUERY 8: Find the average customer rating per vehicle type
-- ============================================================

SELECT
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating
FROM ola_rides
WHERE Booking_Status = 'Success'
  AND Customer_Rating > 0           -- exclude unrated (cancelled) rides
GROUP BY Vehicle_Type
ORDER BY Avg_Customer_Rating DESC;

-- Result: Average customer rating per vehicle type


-- ============================================================
-- QUERY 9: Calculate the total booking value of rides
--          completed successfully
-- ============================================================

SELECT
    SUM(Booking_Value) AS Total_Revenue_INR
FROM ola_rides
WHERE Booking_Status = 'Success';

-- Result: Total revenue from all successful rides


-- ============================================================
-- QUERY 10: List all incomplete rides along with the reason
-- ============================================================

SELECT
    Booking_ID,
    Customer_ID,
    Vehicle_Type,
    Booking_Status,
    Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides = 'Yes';

-- Result: 3,926 incomplete rides with their reasons


-- ============================================================
-- BONUS QUERIES (extra marks!)
-- ============================================================

-- BONUS 1: Revenue by payment method
SELECT
    Payment_Method,
    COUNT(*)            AS Total_Rides,
    SUM(Booking_Value)  AS Total_Revenue
FROM ola_rides
WHERE Booking_Status = 'Success'
GROUP BY Payment_Method
ORDER BY Total_Revenue DESC;

-- BONUS 2: Peak booking hours
SELECT
    Hour,
    COUNT(*) AS Total_Bookings
FROM ola_rides
GROUP BY Hour
ORDER BY Total_Bookings DESC
LIMIT 5;

-- BONUS 3: Most common pickup locations
SELECT
    Pickup_Location,
    COUNT(*) AS Total_Pickups
FROM ola_rides
WHERE Booking_Status = 'Success'
GROUP BY Pickup_Location
ORDER BY Total_Pickups DESC
LIMIT 10;

-- BONUS 4: Cancellation rate by vehicle type
SELECT
    Vehicle_Type,
    COUNT(*)                                              AS Total_Rides,
    SUM(CASE WHEN Booking_Status LIKE 'Canceled%' THEN 1 ELSE 0 END) AS Cancelled,
    ROUND(
        SUM(CASE WHEN Booking_Status LIKE 'Canceled%' THEN 1 ELSE 0 END)
        / COUNT(*) * 100, 2
    )                                                     AS Cancellation_Rate_Pct
FROM ola_rides
GROUP BY Vehicle_Type
ORDER BY Cancellation_Rate_Pct DESC;
