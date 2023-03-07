#!/usr/bin/env python3

import rospy 
from listen import Listen 
from execute import Execute 
from respond import Respond
import sys
import signal

rospy.init_node("main")

s_idle = "IDLE"
s_listen = "LISTEN"
s_execute = "EXECUTE"
s_respond = "RESPOND"
s_exit = "EXIT"

STATE = s_idle

speech_rec = Listen()

speech_rec.calibrate_mic()
commander = Execute()
speaker = Respond()

result = ""
speak = ""
complete_speaking = False 

def shutdown(sig):
    speaker.speak("Exiting the program. Have a good day.")
    rospy.loginfo("[MAIN] Exiting program...")
    sys.exit(0)

while not rospy.is_shutdown():
    
    if STATE == s_exit: 
        shutdown(signal.SIGINT)
    # just initialized the program would have IDLE state which would quickly switch to LISTEN state 
    # to start listening for commands
    elif STATE == s_idle:
        STATE = s_listen

    # LISTEN state would listen for speech 
    elif STATE == s_listen:
        # if there is a result, then move to EXECUTE state
        if result: 
            rospy.loginfo(f"[MAIN] Received command <{result}> from [LISTEN] node and changing STATE to {s_execute}")
            STATE = s_execute
        # else keep listening 
        else: 
            result = speech_rec.listen() 
            STATE = s_listen

    # EXECUTE state will execute the command if it is found
    elif STATE == s_execute:
        speak = commander.execute_command(result) 
        if speak == -1: 
            STATE = s_exit
        else: 
            STATE = s_respond

    # RESPOND state will respond with something related to the command
    elif STATE == s_respond:
        speaker.speak(speak) 
        result = ""
        speak = ""
        STATE = s_idle

    signal.signal(signal.SIGINT, shutdown)
        

    
    
