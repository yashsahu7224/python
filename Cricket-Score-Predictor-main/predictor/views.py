from django.shortcuts import render
from django import forms
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import csv
import sys
sys.path.append('/predictor')
from predictorR import predictRuns

class Newinput(forms.Form):
    teams=(
        ("",""),
        ("Mumbai Indians","Mumbai Indians"),
        ("Punjab Kings","Punjab Kings"),
        ("Chennai Super Kings","Chennai Super Kings"),
        ("Royal Challengers Bangalore","Royal Challengers Bangalore"),
        ("Rajasthan Royals","Rajasthan Royals"),
        ("Delhi Capitals","Delhi Capitals"),
        ("Sunrisers Hyderabad","Sunrisers Hyderabad"),
        ("Kolkata Knight Riders","Kolkata Knight Riders")
    )
    venues=(
        ("",""),
        ("Wankhede Stadium","Wankhede Stadium, Mumbai"),
        ("MA Chidambaram Stadium","MA Chidambaram Stadium, Chennai"),
        ("M Chinnaswamy Stadium","M Chinnaswamy Stadium, Bangalore"),
        ("Arun Jaitley Stadium","Arun Jaitley Stadium, Delhi"),
        ("Narendra Modi Stadium","Narendra Modi Stadium, Ahmedabad"),
        ("Eden Garden","Eden Garden, Kolkata")
    )
    venue=forms.ChoiceField(choices=venues,initial="")
    innings=forms.IntegerField(max_value=2,min_value=1,label="Innings")
    batting_team=forms.ChoiceField(choices=teams,initial="")
    bowling_team=forms.ChoiceField(choices=teams,initial="")
    batsmen=forms.CharField(label="Batsmen (csv format):")
    bowler=forms.CharField(label="Bowler (csv format):")

# Create your views here.
def index(request):
    if request.method == "POST":
        form=Newinput(request.POST)
        if form.is_valid():
            bat_team=form.cleaned_data['batting_team']
            bowl_team=form.cleaned_data['bowling_team']
            venue=form.cleaned_data['venue']
            innings=form.cleaned_data['innings']
            batsmen=form.cleaned_data['batsmen']
            bowler=form.cleaned_data['bowler']
            content=f"venue,innings,batting_team,bowling_team,batsmen,bowlers\n{venue},{innings},{bat_team},{bowl_team},\"{batsmen}\",\"{bowler}\""
            print(content)
            with open('inputFile.csv', mode='w') as infile:
                fwriter = csv.writer(infile, delimiter=',')
                fwriter.writerow(['venue','innings','batting_team','bowling_team','batsmen','bowlers'])
                fwriter.writerow([venue,innings,bat_team,bowl_team,f"{batsmen}",f"{bowler}"])
            runs = predictRuns('inputFile.csv')
            request.method="GET"
            return render(request,'predictor/index.html',{
                "form":Newinput(),
                "runs":runs
            })
    return render(request,'predictor/index.html',{
        "form":Newinput()
    })
