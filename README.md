# Oracle DB Python Code Examples 

## orcl_p99_latency.py

This is a Python script that connects to an Oracle database and executes a simple query repeatedly for a given time interval. It measures the query response time and logs it in a CSV file. The script also calculates and prints the P99 latency at the end of the run.

The script imports the required modules like warnings, cryptography, argparse, oracledb, datetime, time, csv, os, and numpy (which is imported as np). It first disables a UserWarning related to implicit type casting when using older versions of the cryptography package.

The script then sets the database credentials (un, pw, and cs), which are used to connect to the Oracle database. The cs variable contains the connection string in TNS format.

The oneping() function is defined to execute a single query and measure its response time. It opens a new connection to the database using the credentials specified, gets a cursor object, and retrieves the session information (SID and instance) from the database. It then executes a query to select 1 from dual table (a special Oracle table used for selecting a constant value), fetches the results, calculates the query execution time in milliseconds, appends it to the query_times list, writes the query execution time, timestamp, SID, and instance to the CSV file (if specified), and closes the cursor and the database connection.

The script then parses the command-line arguments using the argparse module. It accepts the interval, period, and csvoutput options. If csvoutput is specified, the script opens the file in write mode and writes the header row to it. If it is not specified, the csvfile variable is set to None.

The script then runs a loop for the specified duration (period) with a sleep interval (interval) between queries. It calls the oneping() function to execute a single query and log the query execution time in the query_times list and the CSV file.

Finally, after the loop is complete, the script checks if any queries were executed by checking the length of the query_times list. If there were any queries executed, it calculates the P99 latency using the np.percentile() function and prints it to the console with two decimal places. If no queries were executed, it prints a message saying so.
