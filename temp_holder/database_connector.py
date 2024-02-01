import sqlite3
from random import randrange, random
from datetime import date

def execute_query_and_get_results(query_list):
    result = ""

    try:
        conn = sqlite3.connect('sql.db')
        cursor = conn.cursor()
        print('DB Initializing...')

        for query in query_list:

            # Write a query and execute it with cursor
            cursor.execute(query)

            # Fetch and output result
            result = cursor.fetchall()
            print(f'Query is running... {query} \n \tThe result of query execution: {result}')

        # Close the cursor
        cursor.close()

    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred!!! ', error)
        return ""

    # Close DB Connection irrespective of success
    # or failure
    finally:
        if conn:
            conn.commit()
            conn.close()
            print('DB Connection has been closed.')
            return result


class ProductsTableInterface():
    """
    1. Checks
        -- If link is proper
    """
    def __init__(self):
        self.table_name = "products"
        self.description = "Table that has product names and the links for web scraper to extract prices."

    def __str__(self):
        return self.description
    def insert_recs(self, recs_list):
        # TODO: Add dynamic record insertion functionality to tables

        print(f"\nInserting {len(recs_list)} records to Products table:")
        query_inp_list = []
        for i in range(5):
            insert_into_table_query = f"INSERT INTO products (PRODUCT_NAME, PRODUCT_LINK) " \
                                      f"VALUES ('dummy_product_{i}', 'dummy_link_{i}')"
            query_inp_list.append(insert_into_table_query)
        execute_query_and_get_results(query_inp_list)
        # for rec in recs_list:
        # pass

    def delete_recs(self, all_recs_delete=False):
        if all_recs_delete:
            print("\nDeleting all records from Products table:")
            # Delete all recs from DB
            query_del_all_recs = "delete from products"
            query_inp_list = [query_del_all_recs]

            execute_query_and_get_results(query_inp_list)
        else:
            # TODO: Add partial records deletion functionality to tables
            pass

    def view_recs(self):
        print("\nViewing all records from Products table:")
        query_del_all_recs = "select * from products"
        query_inp_list = [query_del_all_recs]

        res = execute_query_and_get_results(query_inp_list)
        return res




# Create table ProductsParametrHistory
# create_table_query = """CREATE TABLE products_parameter_history(
#    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
#    PRODUCT_KEY INTEGER NOT NULL,
#    PRICE  REAL,
#    CREATE_DATE TEXT NOT NULL,
#    FOREIGN KEY(PRODUCT_KEY) REFERENCES products(PRODUCT_ID)
# );"""
# query_inp_list = [create_table_query]
# execute_query_and_get_results(query_inp_list)


# Drop table ProductsParametrHistory
# drop_table_query = """DROP TABLE products_parameter_history;"""
# query_inp_list = [drop_table_query]
# execute_query_and_get_results(query_inp_list)



class ProductsParametrHistoryTableInterface():
    """
    1. Checks:
        -- Will not reinsert for a date if it already exists in the table
        -- If link is proper [TODO]
        --
    """
    def __init__(self):
        self.table_name = "products_parameter_history"
        self.description = "Table that maps the trends of table stats and attributes over time"

    def __str__(self):
        return self.description
    def insert_recs(self, recs_list):

        print(f"\nInserting {len(recs_list)} records to products_parameter_history table:")

        # check if record has no entries for that date
        check_dates_in_table_query = f"SELECT CREATE_DATE FROM products_parameter_history "
        table_date_list = execute_query_and_get_results([check_dates_in_table_query])
        table_date_list = [i[0] for i in table_date_list]

        query_inp_list = []
        for i in range(6, 11):

            inp_date = str(date.today())
            if inp_date not in table_date_list:

                insert_into_table_query = f"INSERT INTO products_parameter_history (PRODUCT_KEY, PRICE, CREATE_DATE) " \
                                          f"VALUES ({i}, {round(randrange(50, 90) + random(), 2)}, '{inp_date}')"
                print(insert_into_table_query)
                query_inp_list.append(insert_into_table_query)
            else:
                print(f"\tThe records for {inp_date} are already populated")
        execute_query_and_get_results(query_inp_list)
        # for rec in recs_list:
        # pass

    def delete_recs(self, all_recs_delete=False):
        if all_recs_delete:
            print("\nDeleting all records from products_parameter_history table:")
            # Delete all recs from DB
            query_del_all_recs = "delete from products_parameter_history"
            query_inp_list = [query_del_all_recs]

            execute_query_and_get_results(query_inp_list)
        else:
            pass

    def view_recs(self):
        print("\nViewing all records from products_parameter_history table:")
        query_del_all_recs = "select * from products_parameter_history"
        query_inp_list = [query_del_all_recs]

        res = execute_query_and_get_results(query_inp_list)
        return res


if __name__ == "__main__":
    def console_output_block_wrapper(inp_string):
        def wrapper():
            print("--" * 80)
            print(inp_string)
            print("--" * 80)
        return wrapper

    # Create 'Products' table interface object and view all records
    products_table_db_obj = ProductsTableInterface()
    t_str = "1. TABLE: Products:" + str(products_table_db_obj)
    console_output_block_wrapper(t_str)()
    products_table_db_obj.view_recs()

    # Create Products_Parameter_History table interface object and view all records
    products_param_hist_table_db_obj = ProductsParametrHistoryTableInterface()
    # products_param_hist_table_db_obj.delete_recs(all_recs_delete=True)
    # products_param_hist_table_db_obj.insert_recs([])
    t_str = "2. TABLE: Products_Parameter_History:" + str(products_param_hist_table_db_obj)
    console_output_block_wrapper(t_str)()
    products_param_hist_table_db_obj.view_recs()


