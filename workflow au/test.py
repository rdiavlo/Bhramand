
raw = """gcp-edwprddata-prd-33200	WORK_SALESDB_PREPROD	MT_NEW_LOGO_XAAS_SUB_REF_PID_HIST_BQ_COPY_TD_EXPORT	Teradata	TDPROD	MGRE3NFDB	MT_NEW_LOGO_XAAS_SUB_REF_PID_HIST_BQ
gcp-edwprddata-prd-33200	WORK_SALESDB_PREPROD	MT_NEW_LOGO_XAAS_SUB_REF_PML_HIST_BQ_COPY_TD_EXPORT	Teradata	TDPROD	MGRE3NFDB	MT_NEW_LOGO_XAAS_SUB_REF_PML_HIST_BQ
gcp-edwprddata-prd-33200	WORK_SALESDB_PREPROD	MT_NEW_LOGO_XAAS_BKG_PML_HIST_BQ_COPY_TD_EXPORT	Teradata	TDPROD	MGRE3NFDB	MT_NEW_LOGO_XAAS_BKG_PML_HIST_BQ""".strip()
raw = raw.split("\n")
clean_inp = [i.split("\t") for i in raw]

for val in clean_inp:
    param_text = f"\tPRD~BQ2TD_PAR~BIGQUERY~{val[0]}~{val[1]}~{val[2]}~{val[4]}~{val[5]}~{val[6]}~TD_BQ_EXTRACT~~~BQ"
    print(param_text)


counter = 1
for val in clean_inp:
    target_table = val[2].strip()
    tgt_db, tgt_schema = val[0], val[1]
    # sql = f"""SELECT * FROM BQ_JOB_STREAMS bjs
    #     WHERE target_table_name in ('{target_table}');"""
    sql = f"""select {counter}, count(*) 
    from {tgt_db}.{tgt_schema}.{target_table} union all\n"""
    # print(sql)
    counter += 1