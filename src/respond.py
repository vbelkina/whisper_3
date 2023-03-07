import rospy 
from gtts import gTTS
import os
import sys 
import signal

class Respond():

    def __init__(self):
        self.node_name = "[RESPOND]"
        self.lang = "en"
    
    def speak(self, text):
        rospy.loginfo(f"{self.node_name} Going to say: {text}")
        speech = gTTS(text= text, lang=self.lang, slow=False)
  
        # Saving the converted audio in a mp3 file named
        speech.save("speak.mp3")
        
        # Playing the converted file
        os.system("mpg123 -q speak.mp3")

