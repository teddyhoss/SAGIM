import psycopg2
import pandas as pd
import glob
import os

# Database connection parameters
DB_HOST = 'localhost'
DB_PORT = 9999
DB_NAME = 'data24'
DB_USER = 'data24'
DB_PASS = 'data24'

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def import_csv_files():
    # Get list of CSV files in current directory
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    for csv_file in csv_files:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        print("Importing {} into table {}...".format(csv_file, table_name))

        # Read CSV file into DataFrame
        df = pd.read_csv(csv_file)

        # Replace spaces and special characters in column names
        df.columns = [col.strip().replace(' ', '_').replace('-', '_') for col in df.columns]

        # Generate SQL to create table
        columns = df.columns
        # Infer data types
        data_types = []
        for col in columns:
            if pd.api.types.is_integer_dtype(df[col]):
                data_types.append('"{0}" INTEGER'.format(col))
            elif pd.api.types.is_float_dtype(df[col]):
                data_types.append('"{0}" FLOAT'.format(col))
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                data_types.append('"{0}" TIMESTAMP'.format(col))
            else:
                data_types.append('"{0}" TEXT'.format(col))
        columns_with_types = ', '.join(data_types)
        create_table_query = 'CREATE TABLE IF NOT EXISTS "{0}" ({1});'.format(table_name, columns_with_types)
        cursor.execute(create_table_query)
        conn.commit()

        # Prepare insert query
        placeholders = ', '.join(['%s'] * len(columns))
        columns_formatted = ', '.join(['"{0}"'.format(col) for col in columns])
        insert_query = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table_name, columns_formatted, placeholders)

        # Insert data
        for row in df.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)
        conn.commit()
        print("Successfully imported {} into table {}.".format(csv_file, table_name))

    cursor.close()
    conn.close()
    print("All CSV files have been imported successfully.")

if __name__ == '__main__':
    import_csv_files()
