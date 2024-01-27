# This has ODSPROD connector
from configparser import ConfigParser


# Get the configparser object
config_object = ConfigParser()
# Read the contents of the `config.ini` file:
config_object.read('config.ini')


"""
1. SQL Query builder -> query repo file
2. Query executor
3. GUI Engine -> Minion models
    -- Min01: Run on thread to validate workflow & no error check [Pooled conn?]

Dataframes to hold data

"""
import oracledb
# from assets import config
from datetime import datetime
import tkinter as tk
import threading
import pandas as pd
from sqlalchemy import create_engine, text


import random
# from assets.shout import play_sound

# {"description": "SQL"}
all_sql_list = {
    "Au: Tables not in schedule":
        """"select TARGET_TABLE_NAME, job_group_id from ejc.edw_job_streams ejc
        where job_group_id in ('EDW_JIRA_FIX', 'EDW_DOWNTIME')
        and modified_by in :CECID
        and active_ind = 'Y'
        order by TARGET_TABLE_NAME""",

    "Mon: MT_RSTD_":
        """
        select current_phase from ejc.diy_master
        where target_table like 'MT_RSTD_INV_REV_MEASURE'
        and start_time > current_date - 1
        and rownum < 3
        order by start_time desc
        """,

    "Mon: MT_RSTD_GL_REV_MEASURE":
        """
        select current_phase from ejc.diy_master
        where target_table like 'MT_RSTD_GL_REV_MEASURE'
        and start_time > current_date - 1
        and rownum < 3
        order by start_time desc
        """
}


# TODO:
#  1. WARNING IF ANYTHING IN SQL BESIDES 'SELECT' -> DIALOG BOX
#  2. Get your attention [Mail]
#  3.

dummy = ["Mon: MT_SERVICES_BOOKINGS_CX"]
monitoring_list = ["Mon: MT_RSTD_GL_REV_MEASURE"]


def get_connection_engine():
    print("Connecting to oracle...")

    # Access values from the configuration file:
    p_host = config_object.get('Database', 'host')
    p_dns = config_object.get('Database', 'dns')
    p_port = config_object.get('Database', 'port')
    p_username = config_object.get('Database', 'username')
    p_password = config_object.get('Database', 'password')

    # dialect + driver: // username: password @ host:port / database
    engine = create_engine(f"oracle+oracledb://{p_username}:{p_password}@{p_host}:{p_port}/?service_name={p_dns}",
                           thick_mode=True)
    print("Connection to oracle sucessfull!")
    return engine


def execute_oracle_queries(conn_engine, query):
    curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    print(f"\n{curr_time} - Running query... \n", query)
    # TODO: sanitize the input
    bad_character_list = [";"]
    for bad_character in bad_character_list:
        query = query.replace(bad_character, "")

    # check for malicious user commands
    blacklist = ['DROP', 'CREATE', 'ALTER', 'DELETE', 'UPDATE', 'MERGE']
    query = query.upper()
    for bad_command in blacklist:
        if bad_command in query:
            print("Bad command found!!!")
            raise AssertionError

    # limit access to only specified objects in ODSPROD
    # query_tables_whitelisted = ["DIY_MASTER", "BQ_DIY_MASTER", "JOB_STREAMS", "BQ_JOB_STREAMS"]
    # get only 10 rows max
    MAX_RESULT_ROWS = 10
    return_val = None
    with conn_engine.connect() as conn:

        # mode = "Print everything"
        mode = "print and return data frame"
        if mode == "Print everything":
            text_val = text(query)
            rs = conn.execute(text_val).fetchmany(MAX_RESULT_ROWS)
            for row in rs:
                print("\t", row)

        elif mode == "print and return data frame":
            df = pd.read_sql(query, conn)
            print("\t", df)
            return_val = df

    print(f"{curr_time} - Query completed!\n")
    return return_val


def get_gui_wrapper_for_connection():
    root = tk.Tk()
    root.title('Command runner')

    # get ODSPROD connection engine
    conn = get_connection_engine()

    # make a text widget to get user query
    inputtxt = tk.Text(root, height=20, width=40)
    inputtxt.pack()

    def run_user_query():
        # TODO: run query for max 10 seconds
        query_provided_by_user = inputtxt.get("1.0", 'end-1c').strip().upper()
        try:
            # query = """select current_date from dual"""
            execute_oracle_queries(conn, query_provided_by_user)
        except Exception as e:
            print("Exception occurred!!!", e)

    # if button is pressed query entered in text box is run
    button = tk.Button(root, text='Run query', width=25, command=run_user_query)

    button.pack()
    root.mainloop()


def get_multi_threaded_gui():
    # x = threading.Thread(target=thread_function, args=(1,))
    # logging.info("Main    : before running thread")
    # x.start()
    pass


get_gui_wrapper_for_connection()


print("======================= END OF MAIN =======================")



# try:
#     main_handler(all_sql_list, monitoring_list)
# except:
#     messagebox.showinfo("Table", "The run has FAILED!!!")
# finally:
#     play_sound(speech_text="The monitoring program has ended..", file_name="assets/sound_file.mp3")
#


"""
Objective:
    I will provide an Excel sheet with chunks... Your mission is to run it to completion

Sequence:

    Vald JCT [Extract: ALL_DATA, Merge: APPEND, Where clause, Job_group_id, Run_status]
    Run Chunks [1 --> 2 --> 3 ...]
    Monitor:
        Valds [ETA]
        Success: Shout
        Failure: Shout

"""