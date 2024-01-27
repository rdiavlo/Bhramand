
def main_handler(sql_query_list, sql_query_names):
    try:
        with return_connection_object() as connection:
            with connection.cursor() as cursor:

                def shout_if_src_rows_gets_updated():
                    pass

                print("\nThe counts being fetched are : ", end="")
                sql_query = """ select src_rows from (
                         select * from ejc.diy_master
                        where target_table like 'MT_RSTD_GL_REV_MEASURE'
                        and start_Time > current_date - 1
                        and ingestion_type = 'JCT'
                        order by start_time desc)
                        where rownum = 1"""
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        print(round(row[0]/1000000, 2), " Million\n")

                # run query every 1 minutes polling for output
                time_interval_between_runs = 60

                run_state = True
                while run_state:
                    for sql_query_name in sql_query_names:
                        cursor.execute(sql_query_list[sql_query_name])
                        rows = cursor.fetchall()
                        if rows:
                            print(time.strftime("%H:%M:%S", time.localtime()), end=", Status: ")
                            t_run_state = False
                            for row in rows:
                                print(row[0], " ", sql_query_name)

                                if row[0] != 'Success':
                                    t_run_state = True
                                    break

                            if not t_run_state:
                                run_state = False
                                play_sound(speech_text="The run has completed Sire", file_name="assets/sound_file.mp3")
                                messagebox.showinfo("Table", "The run has completed signore!!!")

                    print("-------------------------------------"*2)
                    time.sleep(time_interval_between_runs + random.randint(5, 12))

    except cx_Oracle.Error as error:
        print(error)