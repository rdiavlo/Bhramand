from datetime import datetime
import os


ingestion_flow_types = ["FORWARD", "REVERSE"]
source_types = ["TERADATA"]
env_types = ["PRD", "TS1", "TS3", "DV1", "DV3"]

INGESTION_FLOW = "FORWARD"
SOURCE = "TERADATA"
ENV = "PRD"
RE_INGESTION = False

ROOT_DIR = os.getcwd() + "\\"
curr_time = datetime.now().strftime('%Y-%m-%d')
LOG_FILE = ROOT_DIR + "logs/log-" + str(curr_time) + ".log"
print("Outputting the status to: ", LOG_FILE)

CODE_ERROR = None
WARNING = None


def read_file(file_path):
    """
    Read from a file and return its contents
    :param file_path: the file path where the file to be read is
    :return: the lines or None if file not found
    """
    try:
        with open(file_path + "ew", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None
    return lines


def write_to_file(file_path, msg):
    curr_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    # check if file exists, if it does overwrite it. else create new file
    # if os.path.isfile(file_path):
    #     file_open_mode = "w"
    # else:
    file_open_mode = "a"
    with open(file_path, file_open_mode) as file:
        file.write(curr_time + " - " + msg + "\n")
        file.flush()
        os.fsync(file.fileno())


def assert_proposition(boolean_proposition, file_assertion_error_msg, assertion_type="CRITICAL_ERROR"):
    assertion_success = exec("assert " + boolean_proposition)
    if not assertion_success:
        write_to_file(LOG_FILE, file_assertion_error_msg)
        if type == "CRITICAL_ERROR":
            raise AssertionError


RAW_DATA_FILE = """TDPROD	NRTSTGDB	WI_ORDER_LINES_EXT_NRT_CG1_BP	gcp-edwprddata-prd-33200	TDPROD_NRTSTGDB_STOCKPILE	WI_ORDER_LINES_EXT_NRT_CG1_BP
TDPROD	NRTSTGDB	WI_ORDER_LINES_EXT_NRT_CG1_OLP	gcp-edwprddata-prd-33200	TDPROD_NRTSTGDB_STOCKPILE	WI_ORDER_LINES_EXT_NRT_CG1_OLP
TDPROD	NRTSTGDB	WI_ORDER_LINES_EXT_NRT_CG1_PBL	gcp-edwprddata-prd-33200	TDPROD_NRTSTGDB_STOCKPILE	WI_ORDER_LINES_EXT_NRT_CG1_PBL
TDPROD	NRTSTGDB	WI_ORDER_LINES_EXT_NRT_CG1_SMC	gcp-edwprddata-prd-33200	TDPROD_NRTSTGDB_STOCKPILE	WI_ORDER_LINES_EXT_NRT_CG1_SMC
TDPROD	NRTSTGDB	WI_ORDER_LINES_EXT_NRT_CG1_CSD	gcp-edwprddata-prd-33200	TDPROD_NRTSTGDB_STOCKPILE	WI_ORDER_LINES_EXT_NRT_CG1_CSD
TDPROD	EXCEPDB	EX_WIPS_SER_POS_DTLS_MULTI_PUB	gcp-edwprddata-prd-33200	TDPROD_EXCEPDB_STOCKPILE	EX_WIPS_SER_POS_DTLS_MULTI_PUB"""
RAW_DATA_FILE = RAW_DATA_FILE.strip()
raw_file = RAW_DATA_FILE.split("\n")
clean_inp = [i.split("\t") for i in raw_file]
COUNT_OF_TABLES = len(clean_inp)

msg = f"\nThe ingestion params are: \nFlow: {INGESTION_FLOW}\nSource: {SOURCE}\n" \
      f"Environment: {ENV} \nCount of tables: {COUNT_OF_TABLES} \n Re-Ingestion: {RE_INGESTION}"
write_to_file(LOG_FILE, msg)


if INGESTION_FLOW == "FORWARD":
    if ENV == "PRD":
        if not RE_INGESTION:

            # Step-1: get input in clean format comprising 6 rows. ie: 3 source & 3 target
            assertion_check = list(filter(lambda x: len(x) != 6, clean_inp))

            boolean_proposition = """len(assertion_check) == 0"""
            CODE_ERROR = "ERROR: The format of raw input should be in the form src_db\tsrc_schema\tsrc_table" \
                         "\ttgt_db\ttgt_schema\t_tgt_table. THIS DOES NOT MATCH!"
            assert_proposition(boolean_proposition=boolean_proposition, file_assertion_error_msg=CODE_ERROR)

            msg = f"\nThis is the input provided: \n{raw_file}\n"
            msg += f"This is the cleaned input: \n{clean_inp}"
            write_to_file(LOG_FILE, msg)
            msg = "\n"

            # Step-2: Begin checks
            main_table_map_to_metadata = {}
            for val in clean_inp:
                target_table_name = val[5]
                metadata_list = val + [[], [], None, {}]   # Add [Tags, Comments, Status, Auxiliary Metadata..
                # Ex: src_count]
                main_table_map_to_metadata[target_table_name] = metadata_list

            # 0. Check if src objects are not in blacklist
            blacklist = []
            WARNING = "Warning: The schema provided is blacklisted!"
            try:
                for val in main_table_map_to_metadata:
                    schema = main_table_map_to_metadata[val][1]
                    if schema in blacklist:
                        tags, comments, status = ["schema is blacklisted"], ["The table is rejected as the base schema "
                                                                             "is blacklisted"], "REJECTED"
                        main_table_map_to_metadata[val][6], main_table_map_to_metadata[val][7], \
                            main_table_map_to_metadata[val][8] = tags, comments, status
                        raise AssertionError
            except AssertionError:
                write_to_file(LOG_FILE, WARNING)

            # 1. check if src objects are present
            td_unique_databases = set()
            for val in clean_inp:
                db = val[1]
                td_unique_databases.add(db)

            msg += "RUN THIS: Validate that these databases are present\n"
            for td_database in td_unique_databases:
                sql = f"""
                select *
                from dbc.tables
                where
                database_name = '{td_database}' UNION ALL\n"""
                msg += sql
            msg = msg[:-len(' UNION ALL')]

            msg += "\n\nRUN THIS: Validate that these tables are present\n"
            for val in clean_inp:
                db, table = val[1], val[2]
                sql = f"""
                select *
                from dbc.tables
                where
                database_name = '{db}' and TableName = '{table}' UNION ALL\n"""
                msg += sql
            msg = msg[:-len(' UNION ALL')]
            write_to_file(LOG_FILE, msg)
            msg = "\n"

            DATABASE_NOT_PRESENT_AT_SOURCE = input("Enter database objects not present at source: ").strip()
            TABLES_NOT_PRESENT_AT_SOURCE = input("Enter tables not present at source: ").strip()
            DATABASE_NOT_PRESENT_AT_SOURCE, TABLES_NOT_PRESENT_AT_SOURCE = DATABASE_NOT_PRESENT_AT_SOURCE.split("\n"), \
                TABLES_NOT_PRESENT_AT_SOURCE.split("\n")

            # add entries to metadata dict if db/table not present at source
            for val in main_table_map_to_metadata:
                db, table = main_table_map_to_metadata[val][1], main_table_map_to_metadata[val][2]
                if db in DATABASE_NOT_PRESENT_AT_SOURCE:
                    tags, comments, status = ["schema is not present at source"], \
                        ["The table is rejected as the base schema not present at source"], "REJECTED"
                    main_table_map_to_metadata[val][6], main_table_map_to_metadata[val][7], \
                        main_table_map_to_metadata[val][8] = tags, comments, status
                else:
                    if table in TABLES_NOT_PRESENT_AT_SOURCE:
                        tags, comments, status = ["Table is not present at source"], \
                            ["The table is rejected as the base table not present at source"], "REJECTED"
                        main_table_map_to_metadata[val][6], main_table_map_to_metadata[val][7], \
                            main_table_map_to_metadata[val][8] = tags, comments, status

            msg = f"""\n\tThese databases are not present at source: {DATABASE_NOT_PRESENT_AT_SOURCE}\n\
            These tables are not present at source: {TABLES_NOT_PRESENT_AT_SOURCE}"""
            write_to_file(LOG_FILE, msg)
            msg = "\n"

            # 2. check if src objects has count > 0
            switch_2 = True
            # if switch_2:
            #     # TODO: Connect to teradata here
            #     msg += "\nRUN THIS: Validate that these tables have counts > 0\n"
            #     for val in clean_inp:
            #         db, table = val[1], val[2]
            #         if db not in DATABASE_NOT_PRESENT_AT_SOURCE:
            #             if table not in TABLES_NOT_PRESENT_AT_SOURCE:
            #                 sql = f"\tselect cast(count(*) as BIGINT), '{table}' from {db}.{table} UNION ALL\n"
            #                 msg += sql
            #         else:
            #             pass
            #     msg = msg[:-len(' UNION ALL')]
            #     write_to_file(LOG_FILE, msg)
            #     msg = "\n"
            #
            #     # add src count to metadata dict
            #     table_to_src_count = """EL_BKGS_ALLOC_SL6_NL_DE_HIST_PG_1222	10""".strip()
            #     table_to_src_count = table_to_src_count.split("\n")
            #     table_to_src_count = [i.split("\t") for i in table_to_src_count]
            #     for val in table_to_src_count:
            #         table_name, src_count = val[0], val[1]
            #         status = main_table_map_to_metadata[table_name][7]
            #         if status != 'REJECTED':
            #             main_table_map_to_metadata[table_name][9]["src_count"] = src_count

            # 3. Check if they have already been ingested

            # check in DIY and JCT


            msg += "\nRUN THIS: Validate that these tables have counts > 0\n"
            sql = f"""   SELECT TARGET_TABLE_NAME, count(*) AS COUNT_OF_JCT_ENTRIES
                ,CASE
                WHEN count(*) > 2 THEN 'ANOMALY'
                WHEN count(*) = 2 THEN 'Ingestion attempted'
                WHEN count(*) = 1 THEN 'Ingestion attempted'
                WHEN count(*) = 0 THEN 'History load required, not ingested previously'
                ELSE 'The quantity is under 30'
            	END AS INGESTION_MODE
               from
               ("""
            for val in clean_inp:
                src_db, src_schema, src_table, tgt_db, tgt_schema, tgt_table = val[0], val[1], val[2], val[3], val[4], \
                    val[5]
                sql += f"""
                     SELECT * FROM EJC.BQ_JOB_STREAMS
                     WHERE 1=1
                     AND SOURCE_DB_NAME = '{src_db}'
                     AND SOURCE_SCHEMA = '{src_schema}'
                     AND SOURCE_TABLE_NAME = '{src_table}'
                     UNION ALL
                     SELECT * FROM EJC.BQ_JOB_STREAMS
                     WHERE 1=1
                     AND TARGET_DB_NAME = '{tgt_db}'
                     AND TARGET_SCHEMA = '{tgt_schema}'
                     AND TARGET_TABLE_NAME = '{tgt_table}' 
                    UNION ALL"""
            sql = sql[:-len(' UNION ALL')]
            sql += """)
                   GROUP BY TARGET_TABLE_NAME"""
            print(sql)

            for val in clean_inp:
                src_db, src_schema, src_table, tgt_db, tgt_schema, tgt_table = val[0], val[1], val[2], val[3], val[4], \
                    val[5]

                sql_2 = f"""                     SELECT * FROM EJC.BQ_DIY_MASTER
                         WHERE 1=1
                         AND INGESTION_TYPE IN ('JCT', 'DB')
                         AND SOURCE_DB_NAME = '{src_db}'
                         AND SOURCE_SCHEMA = '{src_schema}'
                         AND SOURCE_TABLE  = '{src_table}'
                         AND ENV_TYPE = '{ENV}'
                         UNION ALL
                         SELECT * FROM EJC.BQ_DIY_MASTER
                         WHERE 1=1
                         AND NOT INGESTION_TYPE IN ('JCT', 'DB')
                         AND TARGET_SCHEMA = '{tgt_schema}'
                         AND TARGET_TABLE = '{tgt_table}' 
                         AND ENV_TYPE = '{ENV}'
                         UNION ALL
                        """
                sql_2 = sql_2[:-len(' UNION ALL')]

                # print(sql_2)



            # separate into already ingested and not ingested
                # if already ingested check if run is success
                # if success: update JCT. If failed: Get DIY error

                # if not already ingested: run in param mode
            ALREADY_INGESTED_AND_FAILED_TABLES = input("Enter ingested & failed tables: ").strip()
            ALREADY_INGESTED_AND_SUCCEEDED_TABLES = input("Enter ingested & completed tables: ").strip()
            FIRST_TIME_INGESTION_TABLES = input("Enter not ingested tables: ").strip()
            ALREADY_INGESTED_AND_FAILED_TABLES, ALREADY_INGESTED_AND_SUCCEEDED_TABLES, FIRST_TIME_INGESTION_TABLES = \
                ALREADY_INGESTED_AND_FAILED_TABLES.split("\n"), ALREADY_INGESTED_AND_SUCCEEDED_TABLES.split("\n"), \
                FIRST_TIME_INGESTION_TABLES.split("\n")

            all_tables_list = [val[2] for val in clean_inp]

            boolean_proposition = """len(all_tables_list) == len(ALREADY_INGESTED_AND_FAILED_TABLES) \
                       + len(ALREADY_INGESTED_AND_SUCCEEDED_TABLES) \
                       + len(FIRST_TIME_INGESTION_TABLES)"""
            CODE_ERROR = "ERROR: The count of provided tables: Not Ingested + Ingested and completed + Ingested and " \
                         "failed is not consistent"
            assert_proposition(boolean_proposition=boolean_proposition, file_assertion_error_msg=CODE_ERROR)



        else:
            # this is re-ingestion mode
            pass



        pass
    elif ENV == "TS1" or ENV == "TS3":

        pass
    elif ENV == "DV1" or ENV == "DV3":

        pass



elif INGESTION_FLOW == "REVERSE":
    pass