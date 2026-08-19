import asyncio
from datetime import datetime
import time
import math
import random
import string

class SrvHelper:   
    
    def getDateNowIso(self):
        return datetime.now().isoformat()






    def getDateString(self):
        now = datetime.now().isoformat()
        arr_date = now.split('T')[0].split('-')
        arr_time = now.split('T')[1].split(':')
        str = f"{arr_date[2]}{arr_date[2]}{arr_date[1]}_{arr_time[0]}{arr_time[1]}{arr_time[2].split('.')[0]}"
        return str
    





    async def delay(self, dur):
        if(dur > 0) : 
            dur = dur 
        else : dur = 2 
        await asyncio.sleep(dur)
        return
    
    
    
    
    
    
    def getRandomNum(self,lgt):
        res = ""
        for i in range(0, lgt):
            rand = str(random.randint(0,9)) 
            res += rand
        return res
    
    
    
    
    
    
    def getRandomStr(self,lgt):
        res = ""
        for i in range(0, lgt):
            rand = string.ascii_lowercase[random.randint(0,25)] 
            res += rand
        return res
        
    
    
    
    
    
    
    def createSessId(self):
        date = self.getDateNowIso().replace("T","_").replace(":","").split(".")[0]
        rand_num = self.getRandomNum(6)
        rand_string = self.getRandomStr(6)
        res = f"{rand_string}{rand_num}_{date}"
        return res
                
        


SrvHelper = SrvHelper()