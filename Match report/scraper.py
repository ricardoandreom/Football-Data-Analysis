import pandas as pd
import os
import time
import numpy as np
import warnings
warnings.filterwarnings("ignore")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import clipboard
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


################## parameters
url = 'https://www.whoscored.com/Matches/1735525/Live/Belgium-Jupiler-Pro-League-2023-2024-Union-St-Gilloise-Eupen'
match = 'Union St. Gilloise 4-1 Eupen'

name_h = 'Home'
name_a = 'Away'

teamId_a = 2166
teamId_h = 2647

match='Union St. Gilloise 4-1 Eupen'

team_h='Union St. Gilloise'
team_a='Eupen'

# Location of your Chromedriver
chrome_driver_loc = "C:/Users/Admin/chromedriver"
# Where you want the data to download to
data_download_loc = "C:/Users/Admin/Downloads"

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": data_download_loc}
options.add_argument(prefs)

s = Service(chrome_driver_loc)
driver = webdriver.Chrome(service=s)
driver.get(url)

t = driver.page_source

start = t.find("matchCentreData")+len('matchCentreData')+2
end = t[t.find("matchCentreData"):].find('matchCentreEventTypeJson') + start - 30

output = t[start:end]
driver.close()

#     driver = webdriver.Chrome(chrome_driver_loc)
s = Service(chrome_driver_loc)
driver = webdriver.Chrome(service=s)
driver.get("https://konklone.io/json")
input_css = 'body > section.json > div.areas > textarea'

# Connecting to it with our driver
input_area = driver.find_element(by=By.CSS_SELECTOR, value=input_css)

# Set the sentence into the clipboard
clipboard.copy(output)
# Making sure that there is no previous text
input_area.clear()
# Pasting the copied sentence into the input_area
input_area.send_keys(Keys.SHIFT, Keys.INSERT)

# CSS of the download button
click_css = 'body > section.csv > p > span.rendered > a.download'

# Click it
driver.find_element(by=By.CSS_SELECTOR, value=click_css).click()
time.sleep(3)
driver.close()

os.chdir(data_download_loc)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
df_base = pd.read_csv(f'{data_download_loc}/{files[-1]}')
os.rename(f'{data_download_loc}/{files[-1]}', f'result {match}.csv')

df_base = df_base[df_base['period/displayName']!='PenaltyShootout'].reset_index(drop=True)

type_cols = [col for col in df_base.columns if '/type/displayName' in col]


df_base['endX'] = 0.0
df_base['endY'] = 0.0
for i in range(len(df_base)):
    df1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df1[type_cols[j]].values[0]
        if col == 'PassEndX':
            endx = df1.loc[:,'qualifiers/%i/value' %j].values[0]
            df_base['endX'][i] = float(endx)
        else:
            j +=1
    k = 0
    for k in range(len(type_cols)):
        col = df1[type_cols[k]].values[0]
        if col == 'PassEndY':
            endy = df1.loc[:,'qualifiers/%i/value' %k].values[0]
            df_base['endY'][i] = float(endy)
        else:
            k +=1

df_base['Cross'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'Cross':
            df_base['Cross'][i] = 1
        else:
            j +=1

df_base['Corner'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'CornerTaken':
            df_base['Corner'][i] = 1
        else:
            j +=1

df_base['KeyPass'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'KeyPass':
            df_base['KeyPass'][i] = 1
        else:
            j +=1

df_base['ShotAssist'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'ShotAssist':
            df_base['ShotAssist'][i] = 1
        else:
            j +=1

df_base['FK'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'FreeKickTaken':
            df_base['FK'][i] = 1
        else:
            j +=1
df_base['IFK'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'IndirectFreeKickTaken':
            df_base['IFK'][i] = 1
        else:
            j +=1
df_base['GK'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'GoalKick':
            df_base['GK'][i] = 1
        else:
            j +=1
df_base['ThrowIn'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'ThrowIn':
            df_base['ThrowIn'][i] = 1
        else:
            j +=1

df_base['GoalMouthY'] = 0.0
df_base['GoalMouthZ'] = 0.0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col == 'GoalMouthY':
            mouthy = df_base1.loc[:,'qualifiers/%i/value' %j].values[0]
            df_base['GoalMouthY'][i] = mouthy
        else:
            j +=1
    k = 0
    for k in range(len(type_cols)):
        col = df_base1[type_cols[k]].values[0]
        if col == 'GoalMouthZ':
            mouthz = df_base1.loc[:,'qualifiers/%i/value' %k].values[0]
            df_base['GoalMouthZ'][i] = mouthz
        else:
            k +=1
try:
    for i in range(len(df_base)):
        tid = df_base.teamId[i]
        if df_base.isOwnGoal[i] == True:
            if tid == teamId_h:
                df_base.teamId[i] = teamId_a
                df_base.x[i] = 100-df_base.x[i]
                df_base.y[i] = 100-df_base.y[i]
            elif tid == teamId_a:
                df_base.teamId[i] = teamId_h
except:
    pass
#####################

df_base['RedCard'] = 0
for i in range(len(df_base)):
    df_base1 = df_base.iloc[i:i+1,:]
    j = 0
    for j in range(len(type_cols)):
        col = df_base1[type_cols[j]].values[0]
        if col in ['SecondYellow','Red']:
            df_base['RedCard'][i] = 1
        else:
            j +=1

####################################################################################################
####################################################################################################
####################################################################################################

df = df_base.copy()
df = df[(df['Corner']==0) & (df['FK']==0) & (df['IFK']==0) & (df['GK']==0) & (df['ThrowIn']==0)]
df = df[(df['type/displayName']=='Pass') & (df['outcomeType/value']==1)]

xT = pd.read_csv('https://raw.githubusercontent.com/mckayjohns/youtube-videos/main/data/xT_Grid.csv', header=None)
xT = np.array(xT)
xT_rows, xT_cols = xT.shape

df['x1_bin_xT'] = pd.cut(df['x'], bins=xT_cols, labels=False)
df['y1_bin_xT'] = pd.cut(df['y'], bins=xT_rows, labels=False)
df['x2_bin_xT'] = pd.cut(df['endX'], bins=xT_cols, labels=False)
df['y2_bin_xT'] = pd.cut(df['endY'], bins=xT_rows, labels=False)

df['start_zone_value_xT'] = df[['x1_bin_xT', 'y1_bin_xT']].apply(lambda x: xT[x[1]][x[0]], axis=1)
df['end_zone_value_xT'] = df[['x2_bin_xT', 'y2_bin_xT']].apply(lambda x: xT[x[1]][x[0]], axis=1)

df['xT'] = df['end_zone_value_xT'] - df['start_zone_value_xT']

