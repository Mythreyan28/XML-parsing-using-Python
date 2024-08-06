# XML-parsing-using-Python:

-> Need to prioritize Hindi language over Bengali language.

-> That is, If Bengali audio language comes first in sequence and Hindi after that, we need to switch their adaptation_set completely. 

-> No need to make any changes to video adaptation_set. 

-> Also, while changing the adaptation_set the id also need to be changes.
 
Eg: Bengali id is '0' if it available first, Hindi id will be '1'. So, during adaptation_set swap we need to change the id also for Hindi id should be Bengali language's id = 0 and for Bengali id shoud change to Hindi id = 1.

-> So your script's input should be  'file_dash_orig.mpd' and expected output should be 'file_dash.mpd'..
