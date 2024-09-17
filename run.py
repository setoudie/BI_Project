from download_script import *

input_choice = input('Tapez:  \n 1 --> format .xml\n  others --> format .csv')

download_data(drv=driver, choice=input_choice)