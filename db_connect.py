import csv
import os
import psycopg2
import psycopg2.extras


def get_transactions(campaign_id):
    query = """SELECT
    --Our DB is in UTC but Adwords will give you reports in your account's timezone. Conversions may be necessary
    extract(hour from convert_timezone('UTC', 'EST', created_at)) as "hour",
    CASE WHEN sum(margin) IS NULL THEN '1' ELSE sum(margin) END as margin
    FROM transactions
    WHERE created_at BETWEEN current_date - interval '14 day' AND current_date
    AND campaign_id = """+campaign_id+"""GROUP BY "hour"ORDER BY "hour" ASC;"""

    params = {
        'database': os.getenv('DATABASE_DATABASE'),
        'user': os.getenv('DATABASE_USER'),
        'password': os.getenv('DATABASE_PASSWORD'),
        'host': os.getenv('DATABASE_HOST'),
        'port': os.getenv('DATABASE_PORT'),
    }

    try:
        conn = psycopg2.connect(**params)
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    spent_rows = cur.fetchall()

    with open('hourly_transactions.csv', 'wb') as csvfile:
        transaction_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        transaction_writer.writerows(spent_rows)
