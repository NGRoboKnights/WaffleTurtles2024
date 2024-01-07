#########################################################################
#Welcome to python!
#This code was made by the Waffle Turtles
#This code will run the robot in a square using a loop
#On the right side of your screen ---> is the API Modules. Open this tab and browse for more lines of code to play with. HOWEVER,  
#Everything you need for a square is already coded for you
#Feel free to  play around with it!
#Main code starts on line 59 :D
#########################################################################
import app
from hub import port, light_matrix
import runloop
import motor_pair, motor
import sys
import time
import distance_sensor

#this is the circumference of the wheels that are used
#it is a global variable. 27.6 is big wheel, 17.6 is small wheel
circumference = 27.6

#########################################################################
# run_motors
#this function can make both motors go
#for whatever reason, you need to unpair the motors and re-pair them
#########################################s###############################
async def run_motors(centimeters):
    angle = ((centimeters / circumference) * 360)
    motor_pair.unpair(motor_pair.PAIR_1)
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    # the arguments are the pair, angle and speed
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, int(angle), 0, velocity=2000, deceleration=500, acceleration=1000, stop=motor.SMART_BRAKE)
#########################################################################
# this function turns the robot a number of degrees
# positive numbers are right, negative are left
#########################################################################
async def stopped_turn(angle):
    angle = int(angle * 2 * 0.82) #times two because each motor turning in opposite directions does half -- and a fudge factor
    motor_pair.unpair(motor_pair.PAIR_1)
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, angle, 150, -150, stop=motor.SMART_BRAKE)
#########################################################################
#distance detect
#drives forward until a certain distance from an object, with sensor in front of robot
#argument is in centimeters
#########################################################################
async def distance_detect_forward(stop_distance):
    distance_sensor_illuminate()
    stop_distance = (stop_distance * 10)
    motor_pair.unpair(motor_pair.PAIR_1)
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    while True:
        if distance_sensor.distance(port.B)>stop_distance or distance_sensor.distance(port.B) == -1: motor_pair.move(motor_pair.PAIR_1,0)
        else:
            motor_pair.stop(motor_pair.PAIR_1)
            break
    distance_sensor.clear(port.B)
    motor_pair.stop(motor_pair.PAIR_1)

######################################################################
#Turn on the distance sensor lights
#takes no arguments
######################################################################
def distance_sensor_illuminate():
    distance_sensor.set_pixel(port.B, 0, 0, 100)
    distance_sensor.set_pixel(port.B, 0, 1, 100)
    distance_sensor.set_pixel(port.B, 1, 0, 100)
    distance_sensor.set_pixel(port.B, 1, 1, 100)


#########################################################################
#this is the 'main' program -- this is where everything starts
# for i in range(times of loops): is a loop function. Make sure code under the loop is tabbed out
#########################################################################
async def main():
    for i in range(2):#this is a loop. The orange number is how many times you want the loop to happen. The code you want repeted has to be indented
        await stopped_turn(90) #This makes the robot turn 90 degrees, or a right angle, to the right
        await run_motors(20) #this makes the robot move forward 25cm
        #Now lets reverse
    for i in range(2):#another loop
            await stopped_turn(-90) # a negative value for a stopped_turn command will make it turn left
            await run_motors(-20) # a negative argument for run_motors command will make it run backward

    #let's drive forward now until we are within 5 cm of a wall, then stop and light up the sensor.
    await distance_detect_forward(5)
    await distance_sensor_illuminate



    sys.exit(0)

runloop.run(main())
