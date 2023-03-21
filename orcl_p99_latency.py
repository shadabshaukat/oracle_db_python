import argparse
import oracledb
import datetime
import time
import csv
import os
import numpy as np

query_times = []

un = 'admin'
pw = '***'
cs = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=**.eu-frankfurt-1.oraclecloud.com))(connect_data=(service_name=i*****_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))' # Autonomous
#cs = 'orcl11g-scan.s*****.oraclevcn.com:1521/orcl11g_mel1wc.***.oraclevcn.com' # Non-Autonomous


def oneping(interval, csvfile):
    # Establish a new database connection
    conn = oracledb.connect(user=un, password=pw, dsn=cs)

    # Get cursor object
    cursor = conn.cursor()

    # Get session information
    cursor.execute("select sys_context('USERENV','SID'), sys_context('USERENV','INSTANCE') from dual")
    sid, instance = cursor.fetchone()

    # Execute the query and time it
    t0 = time.perf_counter()
    cursor.execute("select 1 from dual")
    cursor.fetchall()
    t1 = time.perf_counter()

    # Calculate the timings
    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    # Write the timings to the CSV file
    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time, sid, instance])

    # Close the cursor and the connection
    cursor.close()
    conn.close()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Connect and run a query.")
parser.add_argument("--interval", type=float, help="interval between each query, default 1", default=1)
parser.add_argument("--period", type=int, help="runtime in seconds; default 60", default=60)
parser.add_argument("--csvoutput", help="write timings to the named CSV file")
args = parser.parse_args()

# Open the CSV file if specified
if args.csvoutput is not None:
    csvfile = open(args.csvoutput, "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Query time (ms)", "SID", "Instance"])
else:
    csvfile = None

# Calculate the start time and the end time
start_time = time.perf_counter()
end_time = start_time + args.period

# Run the main loop
while time.perf_counter() < end_time:
    oneping(args.interval, csvfile)

# Close the CSV file if it was opened
if csvfile is not None:
    csvfile.close()

# Calculate the P99 latency
"""
Explanation of p99 latency in the context of the script and output in CSV file:

The p99 latency is the 99th percentile of the query times, which represents the time it takes for the query to be completed
for 99% of the requests. In other words, it's the maximum time it takes for a query to be completed for the majority of the requests.

In the context of this script, the query time is measured for each query executed, and the results are written to a CSV file.
After the script is finished running, the p99 latency can be calculated by reading the query times from the CSV file and
calculating the 99th percentile. This provides a useful metric for measuring the performance of the database for the given
query over the duration of the script.
"""

if len(query_times) > 0:
    p99_latency = np.percentile(query_times, 99)
    print("P99 latency: {:.2f} ms".format(p99_latency))
else:
    print("No queries were executed.")
