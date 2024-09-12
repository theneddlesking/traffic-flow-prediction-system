# data eg.

# input

# SITE_NUMBER,LOCATION,CD_MELWAY,NB_LATITUDE,NB_LONGITUDE,HF_VICROADS_INTERNAL,VR_INTERNAL_STAT,VR_INTERNAL_LOCATION,NB_TYPE_SURVEY,DATE,V00,V01,V02,V03,V04,V05,V06,V07,V08,V09,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,V29,V30,V31,V32,V33,V34,V35,V36,V37,V38,V39,V40,V41,V42,V43,V44,V45,V46,V47,V48,V49,V50,V51,V52,V53,V54,V55,V56,V57,V58,V59,V60,V61,V62,V63,V64,V65,V66,V67,V68,V69,V70,V71,V72,V73,V74,V75,V76,V77,V78,V79,V80,V81,V82,V83,V84,V85,V86,V87,V88,V89,V90,V91,V92,V93,V94,V95
# 0970,WARRIGAL_RD N of HIGH STREET_RD,060 G10,-37.86703,145.09159,249,182,1,1,10/1/06,86,83,52,58,59,44,31,37,30,24,16,24,25,25,15,6,21,17,15,15,16,21,27,21,25,32,61,48,56,66,77,79,67,93,103,130,154,149,210,229,250,246,266,254,300,275,322,292,315,314,308,280,357,298,281,289,345,297,233,227,273,225,265,257,233,244,259,264,265,253,243,210,216,202,177,169,167,136,131,128,118,121,87,113,142,112,114,97,97,66,81,50,59,47,29,34
# 0970,WARRIGAL_RD N of HIGH STREET_RD,060 G10,-37.86703,145.09159,249,182,1,1,10/2/06,32,28,17,11,7,11,6,15,11,12,6,9,1,4,11,9,11,16,22,14,28,26,57,57,70,136,221,196,239,366,355,400,401,400,395,367,315,308,302,306,245,286,279,275,227,234,236,239,320,254,242,261,251,290,254,256,283,226,276,271,281,285,306,301,327,340,294,326,277,382,320,377,259,298,218,190,186,172,161,158,134,141,119,142,103,108,111,102,107,114,80,60,62,48,44,26
# 0970,WARRIGAL_RD N of HIGH STREET_RD,060 G10,-37.86703,145.09159,249,182,1,1,10/3/06,26,32,21,14,10,12,13,10,9,7,8,5,5,6,11,12,8,11,13,10,23,37,64,95,90,183,219,251,302,307,410,351,411,408,405,372,330,366,360,317,312,289,293,299,293,273,264,264,290,260,286,272,274,270,259,313,281,347,280,266,347,277,328,318,357,347,381,288,358,338,365,369,296,335,269,232,211,198,176,163,155,140,135,129,139,146,130,132,114,86,93,90,73,57,29,40
# 0970,WARRIGAL_RD N of HIGH STREET_RD,060 G10,-37.86703,145.09159,249,182,1,1,10/4/06,32,22,28,13,16,8,14,10,8,8,7,6,8,2,7,10,8,14,16,12,24,37,62,84,82,166,230,235,256,336,316,392,374,392,417,380,376,328,324,338,282,272,290,340,301,288,258,272,319,315,251,281,294,301,300,288,282,260,247,252,320,300,264,329,359,345,270,338,308,340,377,335,352,290,258,281,237,203,167,165,133,163,135,141,137,158,115,113,132,101,113,90,78,66,52,44
# 0970,WARRIGAL_RD N of HIGH STREET_RD,060 G10,-37.86703,145.09159,249,182,1,1,10/5/06,40,39,21,11,16,9,15,15,9,6,9,4,4,1,11,9,17,13,16,15,23,35,58,79,81,139,238,235,235,328,344,315,359,434,375,365,356,362,328,330,327,276,311,281,303,324,285,301,331,296,302,299,290,281,308,294,303,296,265,306,312,322,343,317,397,385,388,324,348,361,372,396,315,334,309,271,251,262,228,196,176,152,146,167,122,150,171,120,116,113,99,91,61,55,49,36

# output
# site number, date time every 5 minutes, flow

import math
import pandas as pd
import argparse


DAYS_IN_OCTOBER = 31

NUMBER_OF_DAYS = math.ceil(DAYS_IN_OCTOBER * 0.7)

NUMBER_OF_15_MINUTES_PER_DAY = 96

NUMBER_OF_PERIODS = NUMBER_OF_DAYS * NUMBER_OF_15_MINUTES_PER_DAY


def create_test_train_from_location(location):

    csv = "./data/vic/ScatsOctober2006.csv"

    df = pd.read_csv(csv, encoding="utf-8")

    # output df

    def convert_15_minute_index_to_str(i):
        hours = i // 4
        minutes = (i % 4) * 15

        # pad 0s to make it 2 digits
        hours_str = str(hours).zfill(2)
        minutes_str = str(minutes).zfill(2)

        return f"{hours_str}:{minutes_str}"

    # select only certain location
    df = df[df["LOCATION"] == location]

    output_df = []

    # iter each row
    for index, row in df.iterrows():

        # get flow
        flow = row["V00":"V95"]

        date = row["DATE"]

        # get 15 minutes
        for i in range(0, 96, 1):

            output_df.append(
                {
                    "15 Minutes": date + " " + convert_15_minute_index_to_str(i),
                    "Lane 1 Flow (Veh/5 Minutes)": flow[i],
                    "# Lane Points": 1,
                    "% Observed": 100,
                },
            )

    # convert to df

    output_df = pd.DataFrame(output_df)

    # 70% to 30% ratio
    train_df = output_df.iloc[:NUMBER_OF_PERIODS]

    # rest use as test data
    test_df = output_df.iloc[NUMBER_OF_PERIODS:]

    # save to csv based on location name
    train_df.to_csv(
        "./data/vic_test_train/train_" + location + ".csv",
        encoding="utf-8",
        index=False,
    )

    test_df.to_csv(
        "./data/vic_test_train/test_" + location + ".csv", encoding="utf-8", index=False
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--location",
        type=str,
        help="Location to extract data from",
    )

    args = parser.parse_args()

    # check if location is provided
    if not args.location:
        raise ValueError("Location is required")

    create_test_train_from_location(args.location)
