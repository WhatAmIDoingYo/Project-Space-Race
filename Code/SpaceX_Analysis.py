import sqlite3
import pandas as pd

# Connect to SQLite database
con = sqlite3.connect("my_data1.db")
cur = con.cursor()

# Load the SpaceX dataset into the database
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")

# Drop the table if it exists and create a new table without blank rows
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE;")
cur.execute("CREATE TABLE SPACEXTABLE AS SELECT * FROM SPACEXTBL WHERE Date IS NOT NULL;")
con.commit()

# Task 1: Display the names of the unique launch sites
cur.execute('SELECT DISTINCT "Launch_Site" FROM SPACEXTABLE;')
print("Task 1 - Unique Launch Sites:")
for row in cur.fetchall():
    print(row)

# Task 2: Display 5 records where launch sites begin with 'CCA'
cur.execute('SELECT * FROM SPACEXTABLE WHERE "Launch_Site" LIKE "CCA%" LIMIT 5;')
print("\nTask 2 - Records with Launch Sites starting with 'CCA':")
for row in cur.fetchall():
    print(row)

# Task 3: Display the total payload mass carried by boosters launched by NASA (CRS)
cur.execute('SELECT SUM("PAYLOAD_MASS__KG_") FROM SPACEXTABLE WHERE "Customer" LIKE "%NASA (CRS)%";')
print("\nTask 3 - Total Payload Mass by NASA (CRS):")
print(cur.fetchone()[0])

# Task 4: Display average payload mass carried by booster version F9 v1.1
cur.execute('SELECT AVG("PAYLOAD_MASS__KG_") FROM SPACEXTABLE WHERE "Booster_Version" = "F9 v1.1";')
print("\nTask 4 - Average Payload Mass for F9 v1.1:")
print(cur.fetchone()[0])

# Task 5: List the date when the first successful landing outcome on ground pad was achieved
cur.execute('SELECT MIN("Date") FROM SPACEXTABLE WHERE "Landing_Outcome" = "Success (ground pad)";')
print("\nTask 5 - First Successful Ground Pad Landing Date:")
print(cur.fetchone()[0])

# Task 6: List the names of boosters with success on drone ship and payload mass between 4000 and 6000
cur.execute('SELECT "Booster_Version" FROM SPACEXTABLE WHERE "Landing_Outcome" = "Success (drone ship)" AND "PAYLOAD_MASS__KG_" > 4000 AND "PAYLOAD_MASS__KG_" < 6000;')
print("\nTask 6 - Boosters with Successful Drone Ship Landing and Payload Mass 4000-6000 kg:")
for row in cur.fetchall():
    print(row)

# Task 7: List the total number of successful and failure mission outcomes
cur.execute('SELECT "Mission_Outcome", COUNT(*) as count FROM SPACEXTABLE GROUP BY "Mission_Outcome";')
print("\nTask 7 - Mission Outcome Counts:")
for row in cur.fetchall():
    print(row)

# Task 8: List the names of booster versions that carried the maximum payload mass
cur.execute('SELECT "Booster_Version" FROM SPACEXTABLE WHERE "PAYLOAD_MASS__KG_" = (SELECT MAX("PAYLOAD_MASS__KG_") FROM SPACEXTABLE);')
print("\nTask 8 - Booster Versions with Maximum Payload Mass:")
for row in cur.fetchall():
    print(row)

# Task 9: List records with month names, failure landing outcomes on drone ship, booster versions, and launch site for 2015
cur.execute('SELECT substr("Date", 6, 2) as month, "Landing_Outcome", "Booster_Version", "Launch_Site" FROM SPACEXTABLE WHERE substr("Date", 0, 5) = "2015" AND "Landing_Outcome" LIKE "Failure (drone ship)";')
print("\nTask 9 - 2015 Drone Ship Failure Records:")
for row in cur.fetchall():
    print(row)

# Task 10: Rank the count of landing outcomes between 2010-06-04 and 2017-03-20 in descending order
cur.execute('SELECT "Landing_Outcome", COUNT(*) as count FROM SPACEXTABLE WHERE "Date" BETWEEN "2010-06-04" AND "2017-03-20" GROUP BY "Landing_Outcome" ORDER BY count DESC;')
print("\nTask 10 - Landing Outcome Counts (2010-06-04 to 2017-03-20):")
for row in cur.fetchall():
    print(row)

# Close the database connection
con.close()