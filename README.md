# InFine

## Coverage
Scripts used to compute coverage are provided in ./coverage/ directory. To compute the coverage, variables SG_FILES and SPJ_FILES in Coverage_script.sh must point to the directory containing base files and query result files, respectively.

## Datasets
Due to space limitations, all open datasets (PTC,TPC-H and PTE) used in the experiments are available on the following link:
[Datasets used in InFine experiments](https://drive.google.com/drive/folders/1wGparB08BihNU4J0TQOJvujt74KFy5jo?usp=sharing)

MIMIC-3 can be obtained on [MIMIC-3](https://physionet.org/content/mimiciii/1.4/)

## works file
The command line to launch InFine prototype consists of either 1 parameter (name of file containing a jobs list) or 9 parameters (the description of a single job).

A job is described by DBName, TableORquery, dataInput1.csv attrJoinId1 fdsInput1.txt dataInput2.csv attrJoinId2 fdsInput2.txt nbRuns where:
	DBname: the database which corresponds to the set of data sets (information)
	TableORquery: name of join table or a query (human information). Due to some special characters, one needs to enclose with "
	dataInput1.csv attrJoinId1 fdsInput1.txt: the LEFT data for the join operation following by the id of the join attribute and the valid FDs
	dataInput2.csv attrJoinId2 fdsInput2.txt: the RIGHT data for the join operation following by the id of the join attribute and the valid FDs
	nbRuns: number of runs with these parameters. It uses for statistics.

For instance: PTE "pte_atm|X|pte_drug" pte_atm.csv 0 pte_atm_nulleq_efd.txt pte_drug.csv 0 pte_drug_nulleq_efd.txt 10
pte_atm.csv and pte_drug.csv coming from the database PTE. The ids 0 and 0 correspond respectively to the id of the join attribute of pte_atm.csv and pte_drug.csv. pte_atm_nulleq_efd.txt and pte_drug_nulleq_efd.txt contain respectively the valid FDs of pte_atm.csv and pte_drug.csv . These settings are executed 10 times.

A jobs file is a text file that contains jobs description. Empty lines or lines starting by '#' are ignore.
For example, the following file contains only one job description.

	# InFine for PTE

	# "pte_atm|X|pte_drug"
	PTE "pte_atm|X|pte_drug" pte_atm.csv    0 pte_atm_nulleq_efd.txt    pte_drug.csv   0 pte_drug_nulleq_efd.txt 10


Infine's results are store in two types of files
	a file named <DBname>_results.txt (PTE_results.txt for example) for statistics usage, one line is appended per run
	a file named <DBname>_<TableORquery>_provFDs.txt (PTE_pte_atm_JOIN_pte_drugprovFDs.txt, "|X|" are replaced by "_JOIN_" due to '|' character) for the provenance identification of valid FDs (only once for all runs).
