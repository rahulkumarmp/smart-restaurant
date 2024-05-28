import pymysql
import psycopg2

# MySQL connection parameters
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = ''  # Using an empty password as specified
mysql_db = 'gnt_test'

# PostgreSQL connection parameters
pg_host = 'localhost'
pg_user = 'admin'
pg_password = ''  # Adjust if you have a password
pg_db = 'gnt_test'

# SQL to fetch data from MySQL
select_sql = "SELECT first_name, contact_number FROM tbl_member"  # Adjust 'member' if your table name is different

# SQL to insert data into PostgreSQL
insert_sql = "INSERT INTO testuser (name, mobile) VALUES (%s, %s)"  # Ensure 'testuser' matches your target table

try:
    # Connect to MySQL
    mysql_conn = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(host=pg_host,
                               dbname=pg_db,
                               user=pg_user,
                               password=pg_password)
    pg_cursor = pg_conn.cursor()

    with mysql_conn.cursor() as cursor:
        cursor.execute(select_sql)
        for row in cursor.fetchall():
            # Execute insert statement for each row
            pg_cursor.execute(insert_sql, (row['first_name'], row['contact_number']))

    # Commit changes to PostgreSQL and close connections
    pg_conn.commit()

    print("Data migration completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if mysql_conn:
        mysql_conn.close()
    if pg_conn:
        pg_conn.close()
