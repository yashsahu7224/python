import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("all_matches.csv")
df = df[df['start_date']>="2013-01-01"]
df = df[df['ball']<6.0]
df = df[df['innings']<3]
df['total_runs'] = df['runs_off_bat'] + df['extras']

consistent_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Daredevils', 'Sunrisers Hyderabad']
df = df[(df['batting_team'].isin(consistent_teams)) & (df['bowling_team'].isin(consistent_teams))]

df.venue.replace("Punjab Cricket Association IS Bindra Stadium","Punjab Cricket Association IS Bindra Stadium, Mohali",inplace=True)
df.venue.replace("Punjab Cricket Association Stadium, Mohali","Punjab Cricket Association IS Bindra Stadium, Mohali",inplace = True)
df.venue.replace("Rajiv Gandhi International Stadium, Uppal","Rajiv Gandhi International Stadium",inplace = True)
df.venue.replace("Sardar Patel Stadium, Motera","Narendra Modi Stadium",inplace = True)
df.venue.replace("MA Chidambaram Stadium, Chepauk, Chennai","MA Chidambaram Stadium",inplace = True)
df.venue.replace("MA Chidambaram Stadium, Chepauk","MA Chidambaram Stadium",inplace = True)
df.venue.replace("M.Chinnaswamy Stadium","M Chinnaswamy Stadium",inplace = True)
df.batting_team.replace("Delhi Daredevils", "Delhi Capitals", inplace = True)
df.bowling_team.replace("Delhi Daredevils", "Delhi Capitals", inplace = True)
df.batting_team.replace("Kings XI Punjab", "Punjab Kings", inplace = True)
df.bowling_team.replace("Kings XI Punjab", "Punjab Kings", inplace = True)

batsman_grp = df.groupby(["match_id","innings", "batting_team", "striker"])
batsmen = batsman_grp["runs_off_bat"].sum().reset_index()
balls_faced = df[df["extras"] == 0]
balls_faced = balls_faced.groupby(["match_id", "innings", "striker"])["runs_off_bat"].count().reset_index()
balls_faced.columns = ["match_id", "innings", "striker", "balls_faced"]
batsmen = batsmen.merge(balls_faced, left_on=["match_id", "innings", "striker"],
                        right_on=["match_id", "innings", "striker"], how="left")
batsmen['SR'] = np.round(batsmen['runs_off_bat'] / batsmen['balls_faced'] * 100)
batsmen.drop(["runs_off_bat","balls_faced"],axis=1,inplace=True)

bowler_grp = df.groupby(["match_id", "innings", "bowling_team", "bowler", "ball"])
bowlers = bowler_grp["total_runs","wides", "byes", "legbyes", "noballs"].sum().reset_index()
bowlers["runs"] = bowlers["total_runs"] - (bowlers["byes"] + bowlers["legbyes"])
bowlers["extras"] = bowlers["wides"] + bowlers["noballs"]
bowlers.drop(["byes","legbyes","total_runs"],axis=1,inplace=True)
bowlers_over = bowlers.groupby(['match_id', 'innings', 'bowling_team', 'bowler'])['ball'].count().reset_index()
bowlers = bowlers.groupby(['match_id', 'innings', 'bowling_team', 'bowler']).sum().reset_index().drop('ball', 1)
bowlers = bowlers_over.merge(bowlers, on=["match_id", "innings", "bowling_team", "bowler"], how = 'left')
bowlers['Econ'] = np.round((bowlers['runs']*6) / bowlers['ball'] )
bowlers.drop(["wides","noballs","runs","extras","ball"],axis=1,inplace=True)

df_grp = df.groupby(["match_id","venue","innings"])
df_totalruns = df_grp["total_runs"].sum().reset_index()

df = df.merge(df_totalruns, left_on=['match_id','venue','innings'],
                        right_on=['match_id','venue','innings',], how="left")

df = df.merge(batsmen, left_on=["match_id", "innings", "batting_team", "striker"],
                        right_on=["match_id", "innings", "batting_team","striker"], how="left")

df = df.merge(bowlers,left_on=["match_id", "innings", "bowling_team", "bowler"],
                        right_on=["match_id", "innings", "bowling_team", "bowler"], how="left")


mean1 = df.groupby(['striker'])['SR'].mean().sort_values().to_dict()
df['striker'] = df.striker.map(mean1)
df['striker'].fillna(100, inplace=True)
dict = {'batsmen':mean1.keys(),'mean':mean1.values()}
mean_striker = pd.DataFrame(dict)
mean_striker.to_csv('mean_striker.csv',index=False)


mean2 = df.groupby(['bowler'])['Econ'].mean().sort_values().to_dict()
df['bowler'] = df.bowler.map(mean2)
dict1 = {'bowler':mean2.keys(),'mean':mean2.values()}
mean_bowler = pd.DataFrame(dict1)
mean_bowler.to_csv('mean_bowler.csv',index=False)

# Here
# consistent_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
#                     'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
#                     'Delhi Daredevils', 'Sunrisers Hyderabad']
# df = df[(df['batting_team'].isin(consistent_teams)) & (df['bowling_team'].isin(consistent_teams))]
# df.venue.replace("Punjab Cricket Association IS Bindra Stadium","Punjab Cricket Association IS Bindra Stadium, Mohali",inplace=True)
# df.venue.replace("Punjab Cricket Association Stadium, Mohali","Punjab Cricket Association IS Bindra Stadium, Mohali",inplace = True)
# df.venue.replace("Rajiv Gandhi International Stadium, Uppal","Rajiv Gandhi International Stadium",inplace = True)
# df.venue.replace("Sardar Patel Stadium, Motera","Narendra Modi Stadium",inplace = True)
# df.venue.replace("MA Chidambaram Stadium, Chepauk, Chennai","MA Chidambaram Stadium",inplace = True)
# df.venue.replace("MA Chidambaram Stadium, Chepauk","MA Chidambaram Stadium",inplace = True)
# df.venue.replace("M.Chinnaswamy Stadium","M Chinnaswamy Stadium",inplace = True)
# df.batting_team.replace("Delhi Daredevils", "Delhi Capitals", inplace = True)
# df.bowling_team.replace("Delhi Daredevils", "Delhi Capitals", inplace = True)
# df.batting_team.replace("Kings XI Punjab", "Punjab Kings", inplace = True)
# df.bowling_team.replace("Kings XI Punjab", "Punjab Kings", inplace = True)

df = pd.get_dummies(data=df, columns=['batting_team', 'bowling_team'],drop_first=True)
df = pd.get_dummies(data=df, columns=['venue'],drop_first=True)
df=df[['innings','striker','bowler',
       'batting_team_Delhi Capitals',
       'batting_team_Kolkata Knight Riders',
       'batting_team_Mumbai Indians', 'batting_team_Punjab Kings',
       'batting_team_Rajasthan Royals',
       'batting_team_Royal Challengers Bangalore',
       'batting_team_Sunrisers Hyderabad',
       'bowling_team_Delhi Capitals',
       'bowling_team_Kolkata Knight Riders',
       'bowling_team_Mumbai Indians', 'bowling_team_Punjab Kings',
       'bowling_team_Rajasthan Royals',
       'bowling_team_Royal Challengers Bangalore',
       'bowling_team_Sunrisers Hyderabad',
       'venue_Barabati Stadium',
       'venue_Brabourne Stadium',
       'venue_Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'venue_Dubai International Cricket Stadium',
       'venue_Eden Gardens',
       'venue_Feroz Shah Kotla',
       'venue_Himachal Pradesh Cricket Association Stadium',
       'venue_Holkar Cricket Stadium',
       'venue_JSCA International Stadium Complex',
       'venue_M Chinnaswamy Stadium', 'venue_MA Chidambaram Stadium',
       'venue_Maharashtra Cricket Association Stadium',
       'venue_Narendra Modi Stadium',
       'venue_Punjab Cricket Association IS Bindra Stadium, Mohali',
       'venue_Rajiv Gandhi International Stadium',
       'venue_Sawai Mansingh Stadium',
       'venue_Shaheed Veer Narayan Singh International Stadium',
       'venue_Sharjah Cricket Stadium', 'venue_Sheikh Zayed Stadium',
       'venue_Wankhede Stadium','total_runs_y']]

X = df.drop(columns = "total_runs_y")
y = df.total_runs_y

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state=0)


lin = RandomForestRegressor(n_estimators=100,max_features=None)
lin.fit(X_train,y_train)

joblib.dump(lin,'RandomForestRegressor_model.joblib')


print(lin.score(X_test,y_test))
