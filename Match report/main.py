############### libraries ############################################
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import os
from mplsoccer import VerticalPitch, FontManager
from mplsoccer import Pitch
from scipy.ndimage import gaussian_filter
from PIL import Image
import time
import numpy as np
import matplotlib
from matplotlib.colors import to_rgba
from matplotlib.colors import Normalize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import clipboard
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import functions as fcn
import requests
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")


################## parameters ###############################################
matplotlib.rcParams['figure.dpi'] = 300

name_h = 'Home'
name_a = 'Away'

URL = 'https://github.com/ricardoandreom/Data/blob/main/GoogleFonts/Bree_Serif/BreeSerif-Regular.ttf?raw=true'
fprop = FontManager(URL).prop

chrome_driver_loc = "C:/Users/Admin/chromedriver"
data_download_loc = "C:/Users/Admin/Downloads"

#### parameters mandatory to change
end_color_a = '#2861D4'
end_color_h = 'C33333'
kitline_h = '#a8d0f5'
kitline_a = '#f29aba'

match = 'SL Benfica 1 - 0 FC Porto'  #'FC Porto 5-0 SL Benfica'
url = 'https://www.whoscored.com/Matches/1748463/Live/Portugal-Liga-Portugal-2023-2024-Benfica-FC-Porto'
#https://www.whoscored.com/Matches/1748628/Live/Portugal-Liga-Portugal-2023-2024-FC-Porto-Benfica

teamId_a = 297
teamId_h = 299
team_a='FC Porto'
team_h='SL Benfica'

lg='Liga Portugal'
date=  'Sep 29 09'  #'Mar 03 2023'
sig='@ricardoandreom'

facecolor = 'white'
linecolor = 'black'
fontcolor = 'black'

home_img = 'https://raw.githubusercontent.com/ricardoandreom/Data/main/Images/Liga%20Portugal%20Teams/Porto.png'
away_img = 'https://raw.githubusercontent.com/ricardoandreom/Data/main/Images/Liga%20Portugal%20Teams/Sport%20Lisboa%20e%20Benfica.png'

# get data
scraped_data = fcn.get_data(url, match) #pd.read_csv("C:/Users/Admin/Desktop/result FC Porto 5-0 SL Benfica.csv")
# generate basis
df_base = fcn.preprocess_df_base(scraped_data, teamId_h, teamId_a)
# preprocess data
df = fcn.create_df_stats(df_base)

# generate vizzes
fcn.build_control_index(df_base, end_color_h, end_color_a,teamId_h, teamId_a)

fcn.home_xt_start_zone(df, end_color_h, teamId_h, teamId_a)
fcn.home_xt_end_zone(df,end_color_h, teamId_h, teamId_a)

fcn.away_xt_start_zone(df,end_color_a, teamId_h, teamId_a)
fcn.away_xt_end_zone(df, end_color_a, teamId_h, teamId_a)

fcn.home_passes_finalthird(df_base, teamId_h, teamId_a)
fcn.away_passes_finalthird(df_base, teamId_h, teamId_a)

fcn.home_penalty_passes(df_base, teamId_h, teamId_a)
fcn.away_penalty_passes(df_base, teamId_h, teamId_a)

fcn.home_passes_finalthird_v(df_base, teamId_h, teamId_a)
fcn.away_passes_finalthird_v(df_base, teamId_h, teamId_a)

fcn.home_pass_network(df_base, end_color_h, team_h, teamId_h, teamId_a)
fcn.away_pass_network(df_base, end_color_a, team_a, teamId_h, teamId_a)

fcn.shots(df_base,  end_color_h, end_color_a,teamId_h, teamId_a)

fcn.build_table_stats(df_base, team_a, team_h,teamId_h, teamId_a)

fcn.home_gk_distribution(df_base,369877,teamId_h, teamId_a)
fcn.away_gk_distribution(df_base,373842,teamId_h, teamId_a)

fcn.voronoi_game(df_base, end_color_h, end_color_a,teamId_h, teamId_a)

fcn.build_footer_team_badges(home_img, away_img, match, lg, date, sig)

############ Build report


# report images
file16 = f'{data_download_loc}/Match Report Team Pics.png'
file13 = f'{data_download_loc}/Match Report Lineup.png'
file9 = f'{data_download_loc}/Home xT By Zone Start.png'
file11 = f'{data_download_loc}/Home Passes In Final Third.png'
file4 = f'{data_download_loc}/Home Final Third Passes.png'
file5 = f'{data_download_loc}/Away Final Third Passes.png'
file10 = f'{data_download_loc}/Away xT By Zone Start.png'
file12 = f'{data_download_loc}/Away Passes In Final Third.png'
file1 = f'{data_download_loc}/Home Heatmap.png'
file2 = f'{data_download_loc}/Away Heatmap.png'
file3 = f'{data_download_loc}/Match Report Shots.png'
file14 = f'{data_download_loc}/Home Gk distribution.png'                     #Home Penalty Passes.png
file15 = f'{data_download_loc}/Away Gk distribution.png'                         #Away Penalty Passes.png
footer = f'{data_download_loc}/Match Report Footer.png'
file17 = f'{data_download_loc}/Match Report Pressure.png'
file18 = f'{data_download_loc}/voronoi.png'

# merging images
output=fcn.merge_4images(file1, file2, file3, file4, file5, file9,
              file10, file11,file12,file13,file14,file15,file16,file17, footer)

output.save(f'{match}.png')
im = Image.open(f'{match}.png')
size = int(round(im.size[0]/3.25,0)), int(round(im.size[1]/3.25,0))
im_resized = im.resize(size, Image.Resampling.LANCZOS)
im_resized.save(f'{data_download_loc}/{match}.png')

