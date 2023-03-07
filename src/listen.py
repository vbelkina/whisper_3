import rospy 
import speech_recognition as sr 
import signal 
import sys

class Listen():

    def __init__(self):
        self.node_name = "[LISTEN]"
        self.state = "LISTEN"
        self.r = sr.Recognizer()
        self.r.dynamic_energy_threshold = False
        self.r.energy_threshold = 400
        
    def calibrate_mic(self):
        """
        calibrate the mic with some ambient noise
        """
        with sr.Microphone() as source:  
            rospy.loginfo(f"{self.node_name} Please wait. Calibrating microphone...")  
            # listen for 5 seconds and create the ambient noise energy level  
            self.r.adjust_for_ambient_noise(source, duration=5)  
    
    def listen(self):
        result = ""

        with sr.Microphone() as source:
            rospy.loginfo(f"{self.node_name} listening...")
            audio = self.r.listen(source)

        try:
            
            result = self.r.recognize_google(audio)
            result = result.lower()
            
            rospy.loginfo(f"{self.node_name} RESULT: {result}")

            if result: 
                return result
            else: 
                return ""

        except sr.UnknownValueError: 
            rospy.loginfo(f"{self.node_name} could not understand...")
        except sr.RequestError as e:  
            print(f"{self.node_name} whisper error; {0}".format(e)) 