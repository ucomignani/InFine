#!/bin/bash

OUTPUT_FILE="./coverageQueries.csv"

if [ ! -f $OUTPUT_FILE ]; then
    echo "$OUTPUT_FILE does not exist. It will be created..."
    echo "inst1,inst2,joinIdInst1,joinIdInst2,joinType,coverage,LEFT_dist_without-join,RIGHT_dist_without-join,JOIN_tot,LEFT_tot,LEFT_distinct,RIGHT_tot,RIGHT_distinct,nbIdOccurMoreThanOnce" > $OUTPUT_FILE
fi

SG_FILES="./Coverage_TPCH/"
SPJ_FILES="./SPJ_query_results/"


################# TPCH ##################
# Q2
python3 computeCoverage.py $SPJ_FILES/Q2.csv $SG_FILES/Q2_L.csv $SG_FILES/Q2_R.csv "s_suppkey" "ps_suppkey" "s_suppkey" $OUTPUT_FILE

# Q3
python3 computeCoverage.py $SPJ_FILES/Q3.csv $SG_FILES/Q3_L.csv $SG_FILES/Q3_R.csv "l_orderkey" "l_orderkey" "o_orderkey" $OUTPUT_FILE


# Q4
python3 computeCoverage.py $SPJ_FILES/Q4.csv $SG_FILES/Q4_L.csv $SG_FILES/Q4_R.csv "o_orderkey" "l_orderkey" "o_orderkey" $OUTPUT_FILE


# Q7
python3 computeCoverage.py $SPJ_FILES/Q7.csv $SG_FILES/Q7_L.csv $SG_FILES/Q7_R.csv "l_orderkey" "l_orderkey" "o_orderkey" $OUTPUT_FILE



# Q9
python3 computeCoverage.py $SPJ_FILES/Q9.csv $SG_FILES/Q9_L.csv $SG_FILES/Q9_R.csv "s_nationkey" "n_nationkey" "s_nationkey" $OUTPUT_FILE

# Q10
python3 computeCoverage.py $SPJ_FILES/Q10.csv $SG_FILES/Q10_L.csv $SG_FILES/Q10_R.csv "n_nationkey" "c_nationkey" "n_nationkey" $OUTPUT_FILE

# Q11
python3 computeCoverage.py $SPJ_FILES/Q11.csv $SG_FILES/Q11_L.csv $SG_FILES/Q11_R.csv "ps_suppkey" "s_suppkey" "ps_suppkey" $OUTPUT_FILE

# Q14
python3 computeCoverage.py $SPJ_FILES/Q14.csv $SG_FILES/Q14_L.csv $SG_FILES/Q14_R.csv "l_partkey" "p_partkey" "l_partkey" $OUTPUT_FILE

# new MIMIC-3
# this dataset is not provided as it is not in open data
# python3 computeCoverage.py New_MIMIC3/MIMIC_Q1_patients_admissions_New_subquery.csv New_MIMIC3/MIMIC_Q1_L.csv New_MIMIC3/MIMIC_Q1_R.csv "subject_id" "subject_id" "subject_id" $OUTPUT_FILE
