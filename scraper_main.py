#Author: Connor Larson

from ocean_scraper import *
from scada_scraper import *
from utils import move_files

#delte the old files
delete_folder_contents('/Users/connor/dev/hackArizona/Biosphere-Ocean-Data')

#gets the new files
scrape_the_ocean()
scrape_the_scada()

#move them into the data folder
move_files()