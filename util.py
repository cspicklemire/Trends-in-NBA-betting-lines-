import pandas as pd
import numpy as np

def ml_to_pct(ml):
    
    if (ml > 0):
        pct = 100/(100 + ml)
    if (ml < 0):
        pct = ml/(ml - 100)
    return pct
    
    
def updateRecords(gameDict, teamRecords):
    #Updates each team's record after the game
    #Result of game not included in the table since we care about forecasting
    if gameDict['HF'] > gameDict['AF']:
        teamRecords[str(gameDict['Home'])]['wins'] += 1
        teamRecords[str(gameDict['Away'])]['losses'] += 1
    else:
        teamRecords[str(gameDict['Home'])]['losses'] += 1
        teamRecords[str(gameDict['Away'])]['wins'] += 1
    
def readEvenRow(row, gameDict, gameCounter, dataDict, seasonString):
    theCount = gameCounter.get(row.Date,0)
    theCount += 1
    gameCounter[row.Date] = theCount
    gameID = seasonString + str(row.Date).zfill(4) + str(theCount).zfill(3)
    gameDict['gameID'] = gameID
    gameDict['Date'] = row['Date']
    gameDict['Away'] = row['Team']
    gameDict['A1'] = row['1st']
    gameDict['A2'] = row['2nd']
    gameDict['A3'] = row['3rd']
    gameDict['A4'] = row['4th']
    gameDict['AF'] = row['Final']
    gameDict['AwayML'] = row['ML']

    #The spreadsheet is not consistent with which row has the spread and which row has the over/under,
    #the following code determines which row is which
    opening = float(row['Open'])
    if (opening > 100):
        gameDict['OpenOU'] = opening
    elif (opening < 100):
        gameDict['OpenSpread'] = opening
    closing = float(row['Close'] )         
    if (closing > 100):
        gameDict['CloseOU'] = closing
    elif (closing < 100):
        gameDict['CloseSpread'] = closing

    secondHalf = row['2H']
    if (str(secondHalf).lower() == 'pk'):
        gameDict['2HSpread'] = 100
    elif secondHalf > 50:
        gameDict['2HOU'] = row['2H']
    elif secondHalf < 50:
        gameDict['2HSpread'] = row['2H']
    else:
        print ('Error: data does not match template', secondHalf)

    dataDict[gameID] = gameDict   


def readOddRow(row, gameDict, dataDict, teamRecords):
    if (row['Date'] != gameDict['Date']):
        print ('Error: data does not match template', row)
        
    gameDict['Home'] = row['Team']
    gameDict['H1'] = row['1st']
    gameDict['H2'] = row['2nd']
    gameDict['H3'] = row['3rd']
    gameDict['H4'] = row['4th']
    gameDict['HF'] = row['Final']
    gameDict['HomeML'] = row['ML']
    
    #The spreadsheet is not consistent with which row has the spread and which row has the over/under,
    #the following code determines which row is which
    opening = float(row['Open'])
    if (opening > 100):
        gameDict['OpenOU'] = opening
    elif (opening < 100):
        gameDict['OpenSpread'] = opening
    closing = float(row['Close'] )         
    if (closing > 100):
        gameDict['CloseOU'] = closing
    elif (closing < 100):
        gameDict['CloseSpread'] = closing


    
    secondHalf = float(row['2H'])
    if secondHalf > 50:
        gameDict['2HOU'] = row['2H']
    elif secondHalf < 50:
        gameDict['2HSpread'] = row['2H']

    if int(gameDict['HomeML']) < int(gameDict['AwayML']):
        gameDict['Favorite'] = gameDict['Home']
        gameDict['Underdog'] = gameDict['Away']
    else:
        gameDict['Favorite'] = gameDict['Away']
        gameDict['Underdog'] = gameDict['Home']

    total = int(gameDict['HF']) + int(gameDict['AF'])

    if (total < float(gameDict['CloseOU'])):
        gameDict['OUResult'] = 'Under'
    elif (total > float(gameDict['CloseOU'])):
        gameDict['OUResult'] = 'Over'
    elif (total == float(gameDict['CloseOU'])):
        gameDict['OUResult'] = 'Push'
        
    gameDict['Winner'] = gameDict['HF']>gameDict['AF'] and gameDict['Home'] or gameDict['Away']
    
    if gameDict['Favorite'] == gameDict['Winner']:
        gameDict['Upset?'] = 'No'
    else:
        gameDict['Upset?'] = 'Yes'

    favScore = (gameDict['Favorite'] == gameDict['Home']) and gameDict['HF'] or gameDict['AF']
    dogScore = (gameDict['Favorite'] == gameDict['Home']) and gameDict['AF'] or gameDict['HF']
    margin = favScore - dogScore
    line = gameDict['CloseSpread']
    if (margin > line): #Did the favorite cover the spread?
        gameDict['Cover?'] = 'Yes'
    elif (margin < line):
        gameDict['Cover?'] = 'No'
    elif (margin == line):
        gameDict['Cover?'] = 'Push'

    gameDict['HomeMLPct'] = ml_to_pct(gameDict['HomeML'])
    gameDict['AwayMLPct'] = ml_to_pct(gameDict['AwayML'])
    gameDict['TotalMLPct'] = gameDict['HomeMLPct'] + gameDict['AwayMLPct']

    gameDict['HomeWins'] = teamRecords[gameDict['Home']]['wins']
    gameDict['HomeLosses'] = teamRecords[gameDict['Home']]['losses']
    if (gameDict['HomeWins']+gameDict['HomeLosses'] == 0): #handling divide by zero exception for Wpct of the first game
        gameDict['HomeWpct'] = round(0,3)
    else:
        gameDict['HomeWpct'] = round(gameDict['HomeWins']/(gameDict['HomeWins']+gameDict['HomeLosses']),3)

    gameDict['AwayWins'] = teamRecords[gameDict['Away']]['wins']
    gameDict['AwayLosses'] = teamRecords[gameDict['Away']]['losses']
    if (gameDict['AwayWins']+gameDict['AwayLosses'] == 0):
        gameDict['AwayWpct'] = round(0,3)
    else:
        gameDict['AwayWpct'] = round(gameDict['AwayWins']/(gameDict['AwayWins']+gameDict['AwayLosses']),3)
        
    updateRecords(gameDict, teamRecords)
    

def populateDataFrame(url):   
    teamList = ['Atlanta','Boston','Brooklyn','Charlotte','Chicago','Cleveland','Dallas',
                'Denver','Detroit','GoldenState','Houston','Indiana','LAClippers', 'LALakers',
                'Memphis','Miami','Milwaukee','Minnesota','NewOrleans','NewYork','OklahomaCity',
                'Orlando','Philadelphia','Phoenix','Portland','Sacramento','SanAntonio',
                'Toronto','Utah','Washington']
    
    teamRecords = {x:{'wins':0, 'losses':0} for x in teamList}
    
    #Since "pick'em" odds are functionally equivalent to a zero point spread since it's 50/50, 
    #this just makes the "pk" entries into
    df = pd.read_excel(url)
    df.Open = np.where(df.Open.str.lower() == 'pk',0,df.Open.values)
    df.Close = np.where(df.Close.str.lower() == 'pk',0,df.Close.values)
    df['2H'] = np.where(df['2H'].str.lower() == 'pk',0,df['2H'].values) 
       
    dataDict = {}
    seasonString = '201819' #TOFIX for other years
    gameCounter = {} # counts how many games happen on each date so that each game is assigned a unique gameID
    gameID = ''
    i = 0
    for ix, row in df.iterrows():
        if (i%2 == 0):
            gameDict = {}
            readEvenRow(row, gameDict, gameCounter, dataDict, seasonString)
        else:
            readOddRow(row, gameDict, dataDict, teamRecords)  
        i += 1
    
    myOrder = ['gameID', 'Date','Home','Away','HomeWpct','AwayWpct','Favorite','Underdog',
               'Winner','Upset?','H1', 'H2', 'H3','H4', 'HF','A1', 'A2', 'A3', 'A4', 'AF',
               'HomeML', 'AwayML', 'HomeMLPct', 'AwayMLPct', 'TotalMLPct','OpenOU','CloseOU',
               'OUResult', 'OpenSpread', 'CloseSpread','Cover?', '2HOU', '2HSpread']

    newData = []
    
    for key in dataDict.keys():
        gameDict = dataDict[key]
        newDict = {}
        for gk in myOrder: #This loop reorders the columns to format more nicely
            newDict[gk]= gameDict[gk]
        newData.append(newDict)

    dfNew = pd.DataFrame(newData)
    return dfNew
    
if __name__=='__main__':
    #import pdb; pdb.set_trace()
    print(len(populateDataFrame('https://sportsbookreviewsonline.com/scoresoddsarchives/nba/nba%20odds%202018-19.xlsx')))
    
    