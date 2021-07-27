import pandas as pd
import csv
import sys
from pathlib import Path
from os import path


def readFile(filePath):
    # Define file extension from path

    # Read in file, determine whether a pkl or txt/csv
    try:

        # Detect delimiter
        sniffer = csv.Sniffer()
        sniffer.preferred = [',', '|', ';', ':', '~']
        csvFile = open(filePath, 'rt')
        row1 = []
        for row in csv.reader(csvFile, delimiter="\t"):
            row1 = row
            break
        csvFile.close()
        dialect = sniffer.sniff(str(row1))
        sepType = dialect.delimiter

        if sepType not in {",", "|", ";", ":", "~"}:
            print(
                "Impossible to detect a delimiter (this might occurs with single column datasets). By default, readFile will use ',' as delimiter.")
            df = pd.read_csv(filePath, sep=',', low_memory=False)
        else:
            # Read in pandas data frame from csv file
            df = pd.read_csv(filePath, sep=sepType, low_memory=False)
    except pd.errors.ParserError:
        print("Invalid file\n")
        sys.stdout.flush()
        return
    except IOError:
        print("\tFile not found: " + str(filePath) + "\n")
        sys.stdout.flush()
        return

    return df


def computePartialCoverage(joinedInstance, refInstance, idJoinedInstance, idRefInstance):
    nbUniqueIdsRef = refInstance[idRefInstance].nunique()
    uniqueIdsRef = set(refInstance[idRefInstance])

    sumResult = 0
    for id in uniqueIdsRef:
        if not pd.isna(id):
            isJoinId = joinedInstance[idJoinedInstance] == id
            isRefId = refInstance[idRefInstance] == id
            sumResult += joinedInstance[isJoinId].shape[0] / \
                refInstance[isRefId].shape[0]
        else:
            print("NaN")

    return sumResult / nbUniqueIdsRef


def nbRepeatedJoinIdsInJoinedInstance(dfJoin, idJoin):
    listIds=dfJoin[idJoin].tolist()
    occursMoreThanOnceList = [listIds.count(i) for i in set(listIds) if listIds.count(i) > 1]
    return sum(occursMoreThanOnceList)


def computeCoverage(outCsv, csv1, csv2,
                    idJoin, id1, id2,
                    joinType='inner', suffixes=None):
    print("\n\n******* Launch join coverage script between " +
          str(csv1) + " and " + str(csv2) + "; result set: " + str(outCsv) + " *******")
    # Read in pandas data frame from csv file
    df1 = readFile(csv1)  # pd.read_csv(csv1, sep=",", index_col=id1)
    df2 = readFile(csv2)
    dfJoin = readFile(outCsv)

    if df1 is None or df2 is None or dfJoin is None:
        print("\nMissing dataset")
        return

    uniqueJoinId = dfJoin[idJoin].nunique()
    # nbJoinId = dfJoin[idJoin].size
    if uniqueJoinId > 0:
        print("\nResult dataset not empty: computation of coverage.")
        coverage = (uniqueJoinId/df1[id1].nunique() + uniqueJoinId/df2[id2].nunique()) /2
        coverage = (computePartialCoverage(dfJoin, df1, idJoin, id1)
                    + computePartialCoverage(dfJoin, df2, idJoin, id2)) / 2
        nbRepeatedJoinIds = nbRepeatedJoinIdsInJoinedInstance(dfJoin, idJoin)
    else:  # case where dfJoin is empty
        print("\nJoin dataset empty: coverage and nb repeated join ids values are 0")
        coverage = 0
        nbRepeatedJoinIds = 0
    joinTot = dfJoin.shape[0]

    joinType = joinType.lower()
    print("\nCompute informations with joinType=" + str(joinType))
    if joinType == 'inner':
        LEFT_tot = joinTot
        LEFT_distinct = dfJoin[idJoin].nunique()
        RIGHT_tot = joinTot
        RIGHT_distinct = dfJoin[idJoin].nunique()
    elif joinType == 'left':
        LEFT_tot = joinTot
        LEFT_distinct = dfJoin[idJoin].nunique()
        RIGHT_tot = dfJoin[dfJoin[idJoin].isin(df2[id2])].shape[0]
        RIGHT_distinct = dfJoin[dfJoin[idJoin].isin(
            df2[id2])][idJoin].drop_duplicates().shape[0]
    elif joinType == 'right':
        LEFT_tot = dfJoin[dfJoin[idJoin].isin(df1[id1])].shape[0]
        LEFT_distinct = dfJoin[dfJoin[idJoin].isin(
            df1[id1])][idJoin].drop_duplicates().shape[0]
        RIGHT_tot = joinTot
        RIGHT_distinct = dfJoin[idJoin].nunique()
    else:
        print('WRONG TYPE OF JOIN')
        return

    return Path(csv1).stem + "," + Path(csv2).stem + "," \
        + id1 + "," + id2 + "," + str(joinType) + "," \
        + str(coverage) + "," \
        + str(df1[id1].nunique()) + "," \
        + str(df2[id2].nunique()) + "," \
        + str(joinTot) + "," \
        + str(LEFT_tot) + "," \
        + str(LEFT_distinct) + "," \
        + str(RIGHT_tot) + "," \
        + str(RIGHT_distinct) + "," \
        + str(nbRepeatedJoinIds)  \
        + "\n"


# le nombre de distinct pour la table LEFT (hors jointure): e.g.,  select count(distinct subject_id) from p_100;
# le nombre de distinct pour la table RIGHT (hors jointure) : e.g.,  select count(distinct subject_id) from a_1000;
# le nombre total de la jointure
# le nombre total de LEFT dans la jointure,
# le nombre de distint de LEFT dans la jointure
#  le nombre total de RIGHT dans la jointure,
# le nombre de distint de RIGHT dans la jointure

# open output file in order to rise an exception if this information is missing
f = open(sys.argv[7], "a+")

outputCsvBody = ""
outputCsvBody += computeCoverage(str(sys.argv[1]),
                                 str(sys.argv[2]),
                                 str(sys.argv[3]),
                                 str(sys.argv[4]),str(sys.argv[5]),str(sys.argv[6]))
f.write(outputCsvBody)
f.close()
