raw = """gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_INV_ITEM_COST_FSCL_QTR_TV_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_INV_ITEM_COST_FSCL_QTR_TV_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_INV_ITEM_TCOST_FSCL_QTR_TV_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_INV_ITEM_TCOST_FSCL_QTR_TV_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_TMS_PORT_TYPE_COUNT_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_TMS_PORT_TYPE_COUNT_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRTNR_CNTCT_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRTNR_CNTCT_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRTNR_CNTCT_SITE_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRTNR_CNTCT_SITE_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRTNR_CNTCT_QUALIFICATN_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRTNR_CNTCT_QUALIFICATN_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_INVENTORY_ITEM_HISTORY_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_INVENTORY_ITEM_HISTORY_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_CS_DEAL_SVC_FIN_HIER_ME_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_CS_DEAL_SVC_FIN_HIER_ME_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_SLS_ACCT_GROUP_SAV_PARTY_FUTR_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_SLS_ACCT_GROUP_SAV_PARTY_FUTR_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_CX_PID_COMPONENT_HIERARCHY_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_CX_PID_COMPONENT_HIERARCHY_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_CX_COMPONENT_HIERARCHY_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_CX_COMPONENT_HIERARCHY_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_CX_COMPONENT_HIERARCHY_DEL_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_CX_COMPONENT_HIERARCHY_DEL_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRDT_FAMILY_SBE_ALLOCATION_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRDT_FAMILY_SBE_ALLOCATION_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_TMS_SLS_ALOC_PRD_ALOC_FUTR_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_TMS_SLS_ALOC_PRD_ALOC_FUTR_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_PARTNER_HIERARCHY_MONTH_WITH_RAND_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_PARTNER_HIERARCHY_MONTH_WITH_RAND_BQDELS"""
a = raw.split("\n")
a = [i.split("\t") for i in a]


# step - 1: get src counts
schema_map = {}
acc = ""
counter = 1
for i in a:
    src_db, src_schema, src_table = i[0], i[1], i[2]
    acc += f"\tselect {counter}, count(*) from `{src_db}.{src_schema}.{src_table}` UNION ALL\n"
    counter += 1
# print(acc[:-10])


# step - 2: generate param file
for i in a:
    src_db, src_schema, src_table = i[0], i[1], i[2]
    tgt_db, tgt_schema, tgt_table = i[4], i[5], i[6]
    template = f"PRD~BQ2TD_PAR~BIGQUERY~{src_db}~{src_schema}~{src_table}~{tgt_db}~{tgt_schema}~{tgt_table}~TD_BQ_EXTRACT~~"
    print(template)
print("=" * 80)


details = """

mkdir /users/edwadm/param/25_01_2024
vim /users/edwadm/param/25_01_2024/tbl.param

-- add param file now

cd /apps/edwgcpdata/python/bq2td_scripts/;
nohup ./BQ2TD.py -i db -f /users/edwadm/param/25_01_2024/tbl.param -a rnayakm@cisco.com -e PRD   &

"""
print(details)





# step - 3: monitor run
table_list = [i[6] for i in a]
sql = f"""   	SELECT * FROM BQ_DIY_MASTER 
WHERE target_table in ({table_list})"""
sql = sql.replace("[", "")
sql = sql.replace("]", "")
print(sql)



tables = """N_INVENTORY_ITEM_COST_BQDELS
N_INVENTORY_ITEM_TCOST_BQDELS
N_CX_CUST_BU_TO_PRTY_LNK_BQDELS
N_GROUP_PARTY_BQDELS
N_DIR_FULFIL_CMPNT_ITM_CST_BQDELS
N_CX_CUST_BUSI_UNIT_BQDELS
N_CX_CUSTOMER_BQDELS
R_SALES_HIERARCHY_BQDELS
N_SALES_TERRITORY_BQDELS
N_OFFER_TYPE_PRDT_ALLC_BQDELS
MT_INV_ITEM_COST_FSCL_QTR_TV_BQDELS
MT_INV_ITEM_TCOST_FSCL_QTR_TV_BQDELS
N_TMS_PORT_TYPE_COUNT_BQDELS
R_SALES_HIERARCHY_ME_BQDELS
MT_CS_DEAL_SVC_FIN_HIER_ME_BQDELS
MT_CX_PID_COMPONENT_HIERARCHY_BQDELS
MT_CX_COMPONENT_HIERARCHY_BQDELS
MT_CX_COMPONENT_HIERARCHY_DEL_BQDELS
N_PRDT_FAMILY_SBE_ALLOCATION_BQDELS
MT_TMS_SLS_ALOC_PRD_ALOC_FUTR_BQDELS
MT_PARTNER_HIERARCHY_MONTH_WITH_RAND_BQDELS"""
table_list = tables.split("\n")


#  adhoc step: assign jobs of normal tables to del tables in JCT
for table in table_list:
    sql = f"""
        SELECT * FROM ejc.BQ_JOB_STREAMS bjs
        WHERE target_table_name in ('{table.replace("_BQDELS", "")}', '{table}')
        and job_stream_id LIKE '%_TD'
        and active_ind = 'Y';"""
    # print(sql)





# valdz
for table in table_list:
    sql = f"""       
            SELECT * FROM ejc.BQ_JOB_STREAMS bjs
            WHERE target_table_name in  ('{table.replace("_BQDELS", "")}', '{table}')
            and job_stream_id LIKE '%_TD'
            and active_ind = 'Y';

    """
    print(sql)

# get counts
raw = """gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRTNR_CNTCT_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRTNR_CNTCT_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRTNR_CNTCT_SITE_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRTNR_CNTCT_SITE_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_PRTNR_CNTCT_QUALIFICATN_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_PRTNR_CNTCT_QUALIFICATN_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	N_INVENTORY_ITEM_HISTORY_BQDELS	Teradata	TDPROD	COMREFDB_BQ	N_INVENTORY_ITEM_HISTORY_BQDELS
gcp-edwprddata-prd-33200	BR_REFERENCEDB	MT_SLS_ACCT_GROUP_SAV_PARTY_FUTR_BQDELS	Teradata	TDPROD	COMREFDB_BQ	MT_SLS_ACCT_GROUP_SAV_PARTY_FUTR_BQDELS"""
a = raw.split("\n")
assert len(a) == 5
a = [i.split("\t") for i in a]
for i in a:
    src_db, src_schema, src_table = i[0], i[1], i[2]

    sql_1 = f"\tselect {counter}, count(*) from `{src_db}.{src_schema}.{src_table}` UNION ALL\n"
    # print(sql_1)

for i in a:
    tgt_db, tgt_schema, tgt_table = i[4], i[5], i[6]

    sql_1 = f"\tselect {counter}, count(*) from {tgt_schema}.{tgt_table} UNION ALL\n"
    # print(sql_1)