import rospy 
import json 
from geometry_msgs.msg import Twist
import sys 
import signal

class Execute():

    def __init__(self):
        self.node_name = "[EXECUTE]"
        self.cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

        with open('/home/nika/catkin_ws/src/whisper_3/commands.json') as file:
            self.parsed_json = json.load(file)
    
    def process_command(self, text):
        return text.lower().strip().split()

    def execute_command(self, text):
        rospy.loginfo(f"{self.node_name} received command <{text}>")
        twist = Twist()
        command = self.process_command(text)

        if command[0] == "stop":
            self.cmd_vel.publish(twist)
            return "Stopping now"
        elif command[0] == "exit" or command[0] == "shutdown":
            self.cmd_vel.publish(twist)
            return -1
        elif command[0] in self.parsed_json:
            if command[1] in self.parsed_json[command[0]]:
                twist.linear.x = self.parsed_json[command[0]][command[1]]["linear.x"]
                twist.linear.y = self.parsed_json[command[0]][command[1]]["linear.y"]
                twist.linear.z = self.parsed_json[command[0]][command[1]]["linear.z"]
                twist.angular.x = self.parsed_json[command[0]][command[1]]["angular.x"]
                twist.angular.y = self.parsed_json[command[0]][command[1]]["angular.y"]
                twist.angular.z = self.parsed_json[command[0]][command[1]]["angular.z"]

                self.cmd_vel.publish(twist)

                return f"Executing command {command}"
            else: 
                return f"I don't know the command {command}."
        else: 
            return f"I don't know the command {command}."
