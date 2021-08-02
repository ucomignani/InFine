# InFine

## Coverage
Scripts used to compute coverage are provided in ./coverage/ directory. To compute the coverage, variables SG_FILES and SPJ_FILES in Coverage_script.sh must point to the directory containing base files and query result files, respectively.

## Datasets
Due to space limitations, all open datasets (PTC,TPC-H and PTE) used in the experiments are available on the following link:
[Datasets used in InFine experiments](https://drive.google.com/drive/folders/1wGparB08BihNU4J0TQOJvujt74KFy5jo?usp=sharing)

MIMIC-3 can be obtained on [MIMIC-3](https://physionet.org/content/mimiciii/1.4/)

## Reproducibility and repeatability 
### Running InFine
InFine runs on Windows and Linux OS. The Linux version of infine can be found in ./exec/linux.
The Windows version of infine with the necessary libraries (g++ compiler mingw32) can be found in ./exec/windows.

The file allResultsInFine.txt in ./exec/ contains our statistical results.

**Remark:** Due to the double compatibility of OS, it is possible that some text files have to be re-encoding (unix2dos or dos2unix).

### Run experiments
We provide all files we used in our experiments for PTE (works_PTE.txt), PTC (works_PTC.txt), and TPC-H (works_TPCH.txt) databases. Each works file is located in the corresponding datasets folder (for example, works_PTE.txt in datasets PTE folder, cf. [Datasets used in InFine experiments](https://drive.google.com/drive/folders/1wGparB08BihNU4J0TQOJvujt74KFy5jo?usp=sharing)).

The command line to launch *InFine* prototype consists of either 1 parameter (name of file containing a jobs list) or 9 parameters (the description of a single job).

A job is described by *DBName*, *TableORquery*, *dataInput1.csv*, *attrJoinId1*, *fdsInput1.txt*, *dataInput2.csv*, *attrJoinId2*, *fdsInput2.txt*, *nbRuns* where:
* *DBname*: the database which corresponds to the set of data sets (information)
* *TableORquery*: name of join table or a query (information). Due to some special characters, one needs to enclose by "
* *dataInput1.csv attrJoinId1 fdsInput1.txt*: the **LEFT** data for the join operation following by the id of the join attribute and the valid FDs
* *dataInput2.csv attrJoinId2 fdsInput2.txt*: the **RIGHT** data for the join operation following by the id of the join attribute and the valid FDs
* *nbRuns*: number of runs with these parameters. It uses for statistics.

For instance: PTE "pte_atm|X|pte_drug" pte_atm.csv 0 pte_atm_nulleq_efd.txt pte_drug.csv 0 pte_drug_nulleq_efd.txt 10
pte_atm.csv and pte_drug.csv coming from the database PTE. The ids 0 and 0 correspond respectively to the id of the join attribute of pte_atm.csv and pte_drug.csv. pte_atm_nulleq_efd.txt and pte_drug_nulleq_efd.txt contain respectively the valid FDs of pte_atm.csv and pte_drug.csv . These settings are executed 10 times.

A jobs file is a text file that contains jobs description. Empty lines or lines starting by '#' are ignore.
For example, the following file contains only one job description.

	# InFine for PTE

	# "pte_atm|X|pte_drug"
	PTE "pte_atm|X|pte_drug" pte_atm.csv    0 pte_atm_nulleq_efd.txt    pte_drug.csv   0 pte_drug_nulleq_efd.txt 10

Infine's results are store in two types of files:
1. a file named *DBname*_**results.txt** (PTE_results.txt for example) for statistics usage, one line is appended per run
2. a file named *DBname_TableORquery*_**provFDs.txt** (PTE_pte_atm_JOIN_pte_drug_provFDs.txt, "|X|" are replaced by "_JOIN_" due to '|' character) for the provenance identification of valid FDs (only once for all runs).

   Due to possible duplication of attribute names in datasets, infine rename all attributes by adding prefix: **L_** and **R_** for **LEFT** and **RIGHT** datasets respectively. The prefix **JA_** identified the join attribute.

