import pandas as pd
import numpy as np
import joblib

def predictRuns(testInput):
    with open('RandomForestRegressor_model.joblib','rb') as f:
        lin = joblib.load(f)

    test_case = pd.read_csv(testInput)
    innings = test_case['innings']

    batsmen_list = test_case['batsmen'].to_list()
    listToStr = ' '.join([str(elem) for elem in batsmen_list])
    x = listToStr.split(", ")
    mean_df = pd.read_csv("mean_striker.csv")
    mean_of_batsmen = mean_df['mean'].mean()
    actual = list()
    for i in range(len(x)):
        found = False
        for j in range(len(mean_df)):
            if x[i] == mean_df['batsmen'][j]:
                actual.append(mean_df['mean'][j])
                found = True
                break
        if not found:
            actual.append(mean_of_batsmen)
    final_mean = 0
    for i in range(len(actual)):
        final_mean += actual[i]
    final_mean /= len(actual)

    bowler_list = test_case['bowlers'].to_list()
    listToStr = ' '.join([str(elem) for elem in bowler_list])
    x = listToStr.split(", ")
    mean_df = pd.read_csv("mean_bowler.csv")
    mean_of_bowler = mean_df['mean'].mean()
    actual = list()
    for i in range(len(x)):
        found = False
        for j in range(len(mean_df)):
            if x[i] == mean_df['bowler'][j]:
                actual.append(mean_df['mean'][j])
                found = True
                break
        if not found:
            actual.append(mean_of_bowler)
    final_bowler_mean = 0
    for i in range(len(actual)):
        final_bowler_mean += actual[i]
    final_bowler_mean /= len(actual)


    temp_array = list()
    csk = [0, 0, 0, 0, 0, 0, 0]
    dd = [1, 0, 0, 0, 0, 0, 0]
    kxip = [0, 1, 0, 0, 0, 0, 0]
    kkr = [0, 0, 1, 0, 0, 0, 0]
    mi = [0, 0, 0, 1, 0, 0, 0]
    rr = [0, 0, 0, 0, 1, 0, 0]
    rcb = [0, 0, 0, 0, 0, 1, 0]
    srh = [0, 0, 0, 0, 0, 0, 1]
    if (test_case['batting_team'] == 'Chennai Super Kings').bool():
        temp_array = temp_array + csk
    elif (test_case['batting_team'] == 'Delhi Capitals').bool():
        temp_array = temp_array + dd
    elif (test_case['batting_team'] == 'Punjab Kings').bool():
        temp_array = temp_array + kxip
    elif (test_case['batting_team'] == 'Kolkata Knight Riders').bool():
        temp_array = temp_array + kkr
    elif (test_case['batting_team'] == 'Mumbai Indians').bool():
        temp_array = temp_array + mi
    elif (test_case['batting_team'] == 'Rajasthan Royals').bool():
        temp_array = temp_array + rr
    elif (test_case['batting_team'] == 'Royal Challengers Bangalore').bool():
        temp_array = temp_array + rcb
    elif (test_case['batting_team'] == 'Sunrisers Hyderabad').bool():
        temp_array = temp_array + srh

    if (test_case.bowling_team == 'Chennai Super Kings').bool():
        temp_array = temp_array + csk
    elif (test_case.bowling_team == 'Delhi Capitals').bool():
        temp_array = temp_array + dd
    elif (test_case.bowling_team == 'Punjab Kings').bool():
        temp_array = temp_array + kxip
    elif (test_case.bowling_team == 'Kolkata Knight Riders').bool():
        temp_array = temp_array + kkr
    elif (test_case.bowling_team == 'Mumbai Indians').bool():
        temp_array = temp_array + mi
    elif (test_case.bowling_team == 'Rajasthan Royals').bool():
        temp_array = temp_array + rr
    elif (test_case.bowling_team == 'Royal Challengers Bangalore').bool():
        temp_array = temp_array + rcb
    elif (test_case.bowling_team == 'Sunrisers Hyderabad').bool():
        temp_array = temp_array + srh

    venue_array = list()
    aj = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    eden = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mchin = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    machid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    modi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    wankhede = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    if (test_case.venue == 'Wankhede Stadium').bool():
        venue_array = venue_array + wankhede
    elif (test_case.venue == 'MA Chidambaram Stadium').bool():
        venue_array = venue_array + machid
    elif (test_case.venue == 'M Chinnaswamy Stadium').bool() or (test_case.venue == 'M.Chinnaswamy Stadium').bool():
        venue_array = venue_array + mchin
    elif (test_case.venue == 'Arun Jaitley Stadium').bool():
        venue_array = venue_array + aj
    elif (test_case.venue == 'Narendra Modi Stadium').bool():
        venue_array = venue_array + modi
    elif (test_case.venue == 'Eden Garden').bool():
        venue_array = venue_array + eden


    output = []
    output.append(innings)
    output.append(final_mean)
    output.append(final_bowler_mean)

    for i in range(14):
        output.append(temp_array[i])
    for i in range(20):
        output.append(venue_array[i])

    final_output = []
    final_output = [output, ]

    return int(lin.predict(final_output))
