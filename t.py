# <editor-fold desc="This text is shown when collapsed">
print("hoohah")
# </editor-fold>

"""

Set config attributes:
    INGESTION_MODE --> full load/incremental
    INGESTION_FLOW --> BQ2TD
    ENV --> dev/stg/prd

Get source input
Check counts
Get target input
Create param file [2 TABLE TEST --> BATCHSIZE*NO_OF_BATCHES]
validate param file
Add param file
run tables
monitor: Get jct & diy [shout victory or blocker]
update sharepoint

"""

INGESTION_FLOW = "BQ2TD"
INGESTION_MODE = "FULL"
ENV = "PRD"


def bq2td():
    raw_inp_src = """gcp-edwprddata-prd-33200.WORK_SALESDB_PREPROD	N_SALES_ORDER_V1_TV_BQ_COPY_TD_EXPORT"""

    table_set_1 = """TDPROD	MGRE3NFDB	N_SALES_ORDER_V1_TV_BQ"""

    print("Step-1: Source parameters entered:")
    raw_inp_src = raw_inp_src.strip()

    inp_clean_src = raw_inp_src.split("\n")
    for i in range(len(inp_clean_src)):
        r_1 = inp_clean_src[i].split("\t")
        db, schema = r_1[0].split(".")
        table = r_1[1]
        db, schema, table = db.strip(), schema.strip(), table.strip()
        for val in [db, schema, table]:
            assert len(val) > 0
        inp_clean_src[i] = [db, schema, table]
    print("\t", inp_clean_src)
    print("=" * 50)
    assert len(inp_clean_src) == len(raw_inp_src.split("\n"));
    "The expected count of tables is not met"

    print("Step-2: Check source count pre-ingestion: ")
    for val in inp_clean_src:
        db, schema, table = val[0], val[1], val[2]
        acc = f"\tselect '{db}.{schema}.{table}', '{table}', count(*) from `{db}.{schema}.{table}` UNION ALL"
        print(acc)
    print("=" * 50)

    print("Step-3: Target parameters entered:")
    table_set_1 = table_set_1.split("\n")
    inp_clean_target = [i.split("	") for i in table_set_1]
    print("\t", inp_clean_target)
    print("=" * 50)
    assert len(inp_clean_src) == len(inp_clean_target);
    f"{inp_clean_src} != {len(inp_clean_target)}"

    print("Step-4: Creating param files")
    for i in range(len(inp_clean_src)):
        src_db, src_schema, src_table = inp_clean_src[i][0], inp_clean_src[i][1], inp_clean_src[i][2]
        tgt_db, tgt_schema, tgt_table = inp_clean_target[i][0], inp_clean_target[i][1], inp_clean_target[i][2]
        param_template = f"\tPRD~BQ2TD_PAR~BIGQUERY~{src_db}~{src_schema}~{src_table}~{tgt_db}~{tgt_schema}~{tgt_table}~TD_BQ_EXTRACT~EDW_UPDATE_DTM~"
        print(param_template)
        # print(target_table)
    print("=" * 50)

    print("Step-5: Reference steps")
    print("""\tserver: prd-07
    Choose a param file not in use:
    vim /users/edwadm/param/10_01_2024/param_1.param
    vim /users/edwadm/param/10_01_2024/param_2.param

    Add params and validate
    cat /users/edwadm/param/10_01_2024/param_2.param

    cd /apps/edwgcpdata/python/bq2td_scripts;
    nohup ./BQ2TD.py -i db -f /users/edwadm/param/10_01_2024/param_1.param -a rnayakm@cisco.com -e PRD   > /users/edwadm/param/10_01_2024/au_file.log &
    nohup ./BQ2TD.py -i db -f /users/edwadm/param/10_01_2024/param_2.param -a rnayakm@cisco.com -e PRD   > /users/edwadm/param/10_01_2024/au_file.log &""")
    print("=" * 50)

    print("Step-6: Monitor run: DIY & JCT")
    str_tbl_list = str([i[2] for i in inp_clean_target])[1:-1]
    sql = f"""\tSELECT * FROM EJC.BQ_DIY_MASTER
    WHERE target_table in ({str_tbl_list})
    and start_time > current_date - 1
    order by start_time desc;"""
    print(sql)
    print("=" * 50)

    counter = 1
    print("Step-7: Validate source &  target count after ingestion")

    for val in inp_clean_src:
        db, schema, table = val[0], val[1], val[2]
        acc = f"\tselect {counter}, count(*) from `{db}.{schema}.{table}` UNION ALL"
        print(acc)
        counter += 1
    counter = 1
    print("")
    for val in inp_clean_target:
        db, schema, table = val[0], val[1], val[2]
        sql = f"\tSELECT {counter}, count(*) from {schema}.{table} union all"
        print(sql)
        counter += 1
    print("=" * 50)


if (INGESTION_FLOW == "BQ2TD") and (INGESTION_MODE == "FULL") and (ENV == "PRD"):
    bq2td()