import pandas as pd
import numpy as np

def ml_to_pct(ml):
    
    if (ml > 0):
        pct = 100/(100 + ml)
    if (ml < 0):
        pct = ml/(ml - 100)
    return pct
    
    
def populateDataFrame(url):   
    teamrecords = {
    'Atlanta': {
        'wins' : 0,
        'losses' : 0
    },
    'Boston': {
        'wins' : 0,
        'losses' : 0
    },
    'Brooklyn': {
        'wins' : 0,
        'losses' : 0
    },
    'Charlotte': {
        'wins' : 0,
        'losses' : 0
    },
    'Chicago': {
        'wins' : 0,
        'losses' : 0
    },
    'Cleveland': {
        'wins' : 0,
        'losses' : 0
    },
    'Dallas': {
        'wins' : 0,
        'losses' : 0
    },
    'Denver': {
        'wins' : 0,
        'losses' : 0
    },
    'Detroit': {
        'wins' : 0,
        'losses' : 0
    },
    'GoldenState': {
        'wins' : 0,
        'losses' : 0
    },
    'Houston': {
        'wins' : 0,
        'losses' : 0
    },
    'Indiana': {
        'wins' : 0,
        'losses' : 0
    },
    'LAClippers': {
        'wins' : 0,
        'losses' : 0
    },
    'LALakers': {
        'wins' : 0,
        'losses' : 0
    },
    'Memphis': {
        'wins' : 0,
        'losses' : 0
    },
    'Miami': {
        'wins' : 0,
        'losses' : 0
    },
    'Milwaukee': {
        'wins' : 0,
        'losses' : 0
    },
    'Minnesota': {
        'wins' : 0,
        'losses' : 0
    },
    'NewOrleans': {
        'wins' : 0,
        'losses' : 0
    },
    'NewYork': {
        'wins' : 0,
        'losses' : 0
    },
    'OklahomaCity': {
        'wins' : 0,
        'losses' : 0
    },
    'Orlando': {
        'wins' : 0,
        'losses' : 0
    },
    'Philadelphia': {
        'wins' : 0,
        'losses' : 0
    },
    'Phoenix': {
        'wins' : 0,
        'losses' : 0
    },
    'Portland': {
        'wins' : 0,
        'losses' : 0
    },
    'Sacramento': {
        'wins' : 0,
        'losses' : 0
    },
    'SanAntonio': {
        'wins' : 0,
        'losses' : 0
    },
    'Toronto': {
        'wins' : 0,
        'losses' : 0
    },
    'Utah': {
        'wins' : 0,
        'losses' : 0
    },
    'Washington': {
        'wins' : 0,
        'losses' : 0
    }
    
    }
    
    
    
    df = pd.read_excel(url)
    df.Open = np.where(df.Open.str.lower() == 'pk',0,df.Open.values)
    df.Close = np.where(df.Close.str.lower() == 'pk',0,df.Close.values)
    df['2H'] = np.where(df['2H'].str.lower() == 'pk',0,df['2H'].values)
    
    
    i = 0
    seasonString = '201819'
    gameID = ''
    dateDict = {}
    dataDict = {}
    gameCounter = {} # counters by date


    
    
    for ix, row in df.iterrows():
        if i%2:
            # odd row
            if (row['Date'] != gameDict['Date']):
                print ('Error: data does not match template', row)
            gameDict = dataDict.get(gameID,{})
            gameDict['Home'] = row['Team']
            gameDict['H1'] = row['1st']
            gameDict['H2'] = row['2nd']
            gameDict['H3'] = row['3rd']
            gameDict['H4'] = row['4th']
            gameDict['HF'] = row['Final']
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

            gameDict['HomeML'] = row['ML']
            secondHalf = float(row['2H'])
            if secondHalf > 50:
                gameDict['2HOU'] = row['2H']
            elif secondHalf < 50:
                gameDict['2HSpread'] = row['2H']

            if int(gameDict['HomeML']) < int(gameDict['AwayML']): #populates favorite and underdog based on ml
                gameDict['Favorite'] = gameDict['Home']
                gameDict['Underdog'] = gameDict['Away']
            else:
                gameDict['Favorite'] = gameDict['Away']
                gameDict['Underdog'] = gameDict['Home']

            total = int(gameDict['HF']) + int(gameDict['AF'])

            if (total < float(gameDict['CloseOU'])): #Did the game end up over or under?
                gameDict['OUResult'] = 'Under'
            elif (total > float(gameDict['CloseOU'])):
                gameDict['OUResult'] = 'Over'
            elif (total == float(gameDict['CloseOU'])):
                gameDict['OUResult'] = 'Push'
            gameDict['Winner'] = gameDict['HF']>gameDict['AF'] and gameDict['Home'] or gameDict['Away'] #Who won?
            if gameDict['Favorite'] == gameDict['Winner']:
                gameDict['Upset?'] = 'No'
            else:
                gameDict['Upset?'] = 'Yes'

            favScore = (gameDict['Favorite'] == gameDict['Home']) and gameDict['HF'] or gameDict['AF']
            dogScore = (gameDict['Favorite'] == gameDict['Home']) and gameDict['AF'] or gameDict['HF']
            margin = favScore - dogScore #Margin of victory - should be negative if upset
            gameDict['Margin'] = margin
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

            gameDict['HomeWins'] = teamrecords[gameDict['Home']]['wins']
            gameDict['HomeLosses'] = teamrecords[gameDict['Home']]['losses']
            if (gameDict['HomeWins']+gameDict['HomeLosses'] == 0): #handling divide by zero exception for Wpct of the first game
                 gameDict['HomeWpct'] = round(0,3)
            else:
                gameDict['HomeWpct'] = round(gameDict['HomeWins']/(gameDict['HomeWins']+gameDict['HomeLosses']),3)

            gameDict['AwayWins'] = teamrecords[gameDict['Away']]['wins']
            gameDict['AwayLosses'] = teamrecords[gameDict['Away']]['losses']
            if (gameDict['AwayWins']+gameDict['AwayLosses'] == 0):
                gameDict['AwayWpct'] = round(0,3)
            else:
                gameDict['AwayWpct'] = round(gameDict['AwayWins']/(gameDict['AwayWins']+gameDict['AwayLosses']),3)

            #Updates each team's record at this point in time - result of game not included in the table since we only care about #the information available before the game
            if gameDict['HF'] > gameDict['AF']:
                teamrecords[str(gameDict['Home'])]['wins'] += 1
                teamrecords[str(gameDict['Away'])]['losses'] += 1
            else:
                teamrecords[str(gameDict['Home'])]['losses'] += 1
                teamrecords[str(gameDict['Away'])]['wins'] += 1


        else:
            gameDict = {}
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

            gameDict['AwayML'] = row['ML']

            secondHalf = row['2H']
            if (str(secondHalf).lower() == 'pk'):
                gameDict['2HSpread'] = 100
            elif secondHalf > 50:
                gameDict['2HOU'] = row['2H']
            elif secondHalf < 50:
                gameDict['2HSpread'] = row['2H']
            else:
                print ('Error: data does not match template', secondHalf)
                break

            dataDict[gameID] = gameDict
        i += 1
    
    
    myOrder = ['gameID', 'Date','Home','Away','HomeWpct','AwayWpct','Favorite','Underdog','Winner','Upset?','H1', 'H2', 'H3',     'H4', 'HF','A1', 'A2', 'A3', 'A4', 'AF','HomeML', 'AwayML', 'HomeMLPct', 'AwayMLPct', 'TotalMLPct','OpenOU',                   'CloseOU','OUResult', 'OpenSpread', 'CloseSpread','Margin', 'Cover?', '2HOU', '2HSpread', ]


    newData = []
    for key in dataDict.keys():
        gDict = dataDict[key]
        newDict = {}
        for gk in myOrder:
            newDict[gk]= gDict[gk]
        newData.append(newDict)

    dfNew = pd.DataFrame(newData)
    




    return dfNew