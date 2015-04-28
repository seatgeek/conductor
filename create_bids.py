import csv
import datetime

parameters = []
ad_group_id = []
keyword_id = []
keyword_cpc = []
hour = str(datetime.datetime.now().time().hour)
multiple = []


def multipliers():
    roi_goal = 2
    # Comment out line above and uncomment line before if you have a CPA goal
    # cpa_goal = 20
    spend_rows = []
    trans_rows = []

    with open('report.csv', 'rb') as spendcsvfile:
        reportreader = csv.reader(spendcsvfile)
        for row in reportreader:
            if row[0] == hour:
                spend_rows.append(float(row[1])/1000000)

    with open('hourly_transactions.csv', 'rb') as transcsvfile:
        transreportreader = csv.reader(transcsvfile, delimiter=' ')
        for row in transreportreader:
            if row[0] == hour:
                trans_rows.append(float(row[1]))

    # Create the bid multiplier
    z = trans_rows[0]/(roi_goal*spend_rows[0])
    # Comment out line above and uncomment line below if you have a CPA goal
    # z = (cpa_goal*trans_rows[0])/spend_rows[0]
    print "Bid multiplier ="+str(z)
    multiple.append(z)
    return multiple


# Parsing the keywords report into ad_group_ids, keyword_ids, and keyword_cpcs for later use in the changebids() function
def batch_parameters():
    with open('keywords.csv', 'rb') as keywordscsv:
        keywordsreader = csv.reader(keywordscsv)
        parameters = list(keywordsreader)
    for i in xrange(len(parameters)):
        if parameters[i][0] != 'Ad group ID':
            ad_group_id.append(parameters[i][0])
            keyword_id.append(parameters[i][1])
            keyword_cpc.append(parameters[i][2])
    return ad_group_id, keyword_id, keyword_cpc
