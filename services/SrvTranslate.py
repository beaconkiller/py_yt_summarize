from faster_whisper import WhisperModel
from services.SrvHelper import SrvHelper
from services.SrvYtDownload import SrvYtDownload
import os
import json
import math
import asyncio

class SrvTranslate:


    def run_translate_batch(self):
        files = self.getFiles()

        i = 0
        for audio in files:
            print(i)
            self.translateAudio(audio)
            i +=1 






    def runTest(self):
        files = self.getFiles()
        
        obj_processed = []
        for file in files : 
            
            vid_name = file.split("\\")[-1].split("(__)")[1]
            vid_url = f"https://www.youtube.com/watch?v={file.split("\\")[-1].split("(__)")[0]}"
            
            obj = {
                "vid_name":vid_name,
                "vid_url":vid_url,
                "result": None,
            }
            
            # audio_res = self.getFullStringFromAudio(file)
                        
            # ====== DEBUG ======
            full_string = self.readFromTextTmp() 
            # ===================
            
            arr_obj_items = self.processFullString(full_string)            
            arr_obj_items = self.getSentencesByMappedWords(full_string,arr_obj_items)

            obj["result"] = arr_obj_items
            
            self.cleanArrObjItems(obj)

            obj_processed.append(obj)
            
        self.saveJson(obj_processed)






    def processVideo(self, arr_url, arr_to_search):
        
        sess_id = SrvHelper.createSessId()
        
        asyncio.run(SrvYtDownload.getAudioBatchWithSessId(
            arr_url, 
            sess_id
        ))
        
        
        files = self.getFilesBySessionId(sess_id)
        obj_processed = []
        for file in files : 
            
            vid_name = file.split("\\")[-1].split("(__)")[1]
            vid_url = f"https://www.youtube.com/watch?v={file.split("\\")[-1].split("(__)")[0]}"
            
            obj = {
                "vid_name":vid_name,
                "vid_url":vid_url,
                "result": None,
            }
            
            audio_res = self.getFullStringFromAudio(file)
            
            full_string = audio_res.strip()
            print(full_string)
            
            # ====== DEBUG ======
            # full_string = self.readFromTextTmp() 
            # ===================
            
            arr_obj_items = self.processFullString(full_string, arr_to_search)            
            arr_obj_items = self.getSentencesByMappedWords(full_string, arr_obj_items)
            
            obj["result"] = arr_obj_items
            
            self.cleanArrObjItems(obj)

            obj_processed.append(obj)
            
        self.saveJsonToSessResult(obj_processed, sess_id)
            

        


        

        

    def processFullString(
        self, 
        full_string,
        arr_to_search
    ):
        mapped_words = self.findWordsIndex(full_string, arr_to_search)
        return mapped_words






    def getFullStringFromAudio(self, file_path):
        audio_res = self.translateAudio(file_path)
        return audio_res






    def getFilesBySessionId(self,sess_id):
        curDir = os.getcwd()
        fileStorage = os.path.join(curDir, 'file_storage', 'session_result', sess_id)
        files = os.listdir(fileStorage)

        arr = []
        for el in files:
            if(el == '.gitkeep') : continue
            arr.append(os.path.join(curDir, 'file_storage', 'session_result', sess_id, el))

        return arr






    def getFiles(self):
        curDir = os.getcwd()
        fileStorage = os.path.join(curDir, 'file_storage', 'audio_result')
        files = os.listdir(fileStorage)

        arr = []
        for el in files:
            if(el == '.gitkeep') : continue
            arr.append(os.path.join(curDir, 'file_storage', 'audio_result', el))

        return arr






    def translateAudio(self, filePath):
        print(filePath)

        model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        segments,info = model.transcribe(
            filePath,
            beam_size=5
        )

        words = ""
        for segment in segments:
            print(segment.start, segment.end, segment.text)
            words += segment.text
        return words
        
        
        
        
        
        
    def getSentencesByMappedWords(
        self, 
        full_string, 
        arr_obj_items,
    ):    
        arr_full_string = full_string.split(" ")

        offset = 20
        
        arr_result = []
        for obj in arr_obj_items:
            indexes = obj["place"]
            # print(indexes)
            
            for index in indexes:
                sentence = ""
                start_index = arr_full_string[index]
                
                for i in range(index - offset, index + offset):
                    word = arr_full_string[i]
                    sentence += " " + word
                    
                obj["key_sentences"].append(sentence)
                
        return arr_obj_items
                
                
                
                
                

    def getMappedInterestWords(self, arr_to_search):
        mapped_interest = []
        for word in arr_to_search:
            obj = {
                "string":word,
                "place":[],
                "key_sentences":[]
            }
            mapped_interest.append(obj)

        return mapped_interest






    def findWordsIndex(self, full_string, arr_to_search):
        full_string = full_string.lower()
        arr_obj_find = self.getMappedInterestWords(arr_to_search)
        arr_string = full_string.split(" ")
        
        i = 0
        for word in arr_string:
            for obj_find in arr_obj_find:
                str_word = obj_find["string"]
                if(str_word == word):
                    obj_find["place"].append(i)
            i+=1

        return arr_obj_find
        # print(words)






    def readFromTextTmp(self):
        dir_path = os.getcwd()
        file_path = os.path.join(dir_path, "file_storage", "test_files", "tmp.txt")
        print(file_path)

        with open(file_path) as file:
            sentence = file.read()
            return sentence
        
        
        
        
        
    def cleanArrObjItems(self,obj_item):
        for item in obj_item["result"]:
            self.removeDuplicates(item)
            
        self.removeEmpty(obj_item)

        return obj_item
    
    
    
    
    
    
    def removeDuplicates(self,arr_obj_item):
        arr_key_sentences = arr_obj_item["key_sentences"]
        arr_cleaned_sentences = []
        for i in range(0,len(arr_key_sentences)):
            sentence_to_find = self.getSubstractedSentence(arr_key_sentences[i].strip())

            dupe = 0
            for sentence in arr_key_sentences:
                if sentence_to_find in sentence:
                    dupe += 1
                    
            if dupe < 3 :
                arr_cleaned_sentences.append(arr_key_sentences[i].strip())
        
        arr_obj_item["key_sentences"] = arr_cleaned_sentences
        
        
        
        
        
        
    def removeEmpty(self,obj_item):
        new_arr = []
        for result in obj_item["result"]:
            if len(result["place"]) > 0:
                new_arr.append(result)

        obj_item["result"] = new_arr
        
            
            
            
            
            
            
    def getSubstractedSentence(self, sentence):
        arr_words = sentence.split(" ") 
        mid_point = math.floor(len(arr_words)/2)
        arr_new_words = []
        for i in range(mid_point-5, mid_point+5):
            arr_new_words.append(arr_words[i])
                
        substracted_string = " ".join(arr_new_words)
        
        return substracted_string
        
        
        
        
        
        
    def saveJsonToSessResult(self, arr_obj_items,sess_id):
        dir_path = os.path.join("file_storage", "session_result", sess_id, "result.json")
        with open(dir_path,"w") as file:
            json.dump(arr_obj_items,file,indent=4)
        
        
        
        
        
        
    def saveJson(self, arr_obj_items):
        dir_path = os.path.join("file_storage","json_dump","saved10.json")
        with open(dir_path,"w") as file:
            json.dump(arr_obj_items,file)
        
        




SrvTranslate = SrvTranslate()

