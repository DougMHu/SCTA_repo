import SCTA_context
from SCTA.System import Transponder
from SCTA.Instrumentation import BTC, SLG
from SCTA.DataLogging import DataLogger
from ..utils.fileparse import csv2dict, dict2csv, importCSV
import pandas as pd

import logging


def calibrateDDSS(scenario=1):



	# IP addresses and port numbers
FSW_IP="192.168.88.243"
SLG1_IP="192.168.88.2"
SLG2_IP="192.168.88.3"
SLG3_IP="192.168.88.4"
SLG_port=5025
#BTC_IP="192.168.10.11"
# Initialize Equipment

fsw = FSW(type="IP", port=FSW_IP, window="Spectrum")
slg1= SLG(ip=SLG1_IP, port=SLG_port, numMods=1)
slg2= SLG(ip=SLG2_IP, port=SLG_port, numMods=1)
slg3= SLG(ip=SLG3_IP, port=SLG_port, numMods=1)
#btc = BTC(type="IP", port=BTC_IP)

#initialize SLG Setup


slg1.loadConfigFile("DSWM\SLG1_DSWM_US_23CH_2B_20MS.cfg")
slg2.loadConfigFile("DSWM\SLG2_DSWM_US_23CH_2B_20MS.cfg")
slg3.loadConfigFile("DSWM\SLG3_DSWM_US_23CH_2B_20MS.cfg")

slg=[slg1, slg2, slg3]
mod1=list(range(1,10))
mod2=list(range(1,7))
mod3=list(range(1,9))
mods=mod1+mod2+mod3
powers=[]

spec = pd.read_csv('C:\\Users\\labuser\\Documents\\SCTA_repo\\src\\SCTA\\Specs\\raw\\DSWM23_Scen2.csv')

victim = spec[""]

