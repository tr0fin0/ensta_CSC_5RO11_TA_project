# -*- coding: utf-8 -*-
"""CSC_5RO11_TA, AI for Robotics."""
# import sys
# print "\n".join(sys.path)   # uncomment for debug

import sys
sys.path.append('/home/nataliagcr/RO11/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages')

import naoqi
from Emotion import emotion_recognition, unsubscribe_camera, emotions
import time
import threading
import requests
import urllib3
import random
import os

class PepperAPI:
    def __init__(self, ip, port = 9559):
        """
        Initialize Pepper API.

        Args:
            ip (str) : Pepper's IP address in '000.000.000.000' format.
            port (int) : Pepper's connection port. Default value is 9559.
        """
        self.ip = ip
        self.port = port

        self.audio = naoqi.ALProxy("ALAudioDevice", ip, port)
        self.battery = naoqi.ALProxy("ALBattery", ip, port)
        self.leds = naoqi.ALProxy("ALLeds", ip, port)
        self.motion = naoqi.ALProxy("ALMotion", ip, port)
        self.posture = naoqi.ALProxy("ALRobotPosture", ip, port)
        self.tablet = naoqi.ALProxy("ALTabletService", ip, port)
        self.tts = naoqi.ALProxy("ALTextToSpeech", ip, port)
        self.video = naoqi.ALProxy("ALVideoDevice", ip, port)
        self.movement = naoqi.ALProxy("ALBehaviorManager", ip, port)

        self.battery_charge = self.get_battery_charge()
        self.set_posture(posture="Stand")

        # Initialization finished.
        self.set_eyes_color("green")



    def get_battery_charge(self):
        """Return Pepper's battery charge level as percentage."""
        battery_charge = self.battery.getBatteryCharge()

        self.battery_charge = battery_charge

        return battery_charge


    def speak(self, text = "I'm Pepper!"):
        """
        Make Pepper say a text.

        Args:
            text (str) : text to be said. Default value is 'I'm Pepper!'.
        """
        self.tts.say(text)


    def set_posture(self, posture = "Stand", speed = 1.0):
        """
        Set Pepper's posture with a given speed.

        Note: speed limited between 0 and 1.

        Args:
            posture (str) : required posture. Default value is "Stand".
            speed (float) : movement speed. Default is 1.0.
        """
        self.motion.wakeUp()

        success = self.posture.goToPosture(posture, speed)

        if success:
            print("Pepper posture set successful.")
        else:
            print("Pepper posture set failed.")


    def rest(self):
        """
        Set Pepper's posture to rest.

        Note: sit down and power-saving mode.
        """
        self.motion.rest()


    def show_url(self, url):
        """
        Display an webpage URL address in Pepper's tablet.

        Args:
            url (str) : webpage URL address. Default value is Aldebaran's documentation.
        """
        self.tablet.loadUrl(url)
        self.tablet.showWebview()
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def show_url(self, url='http://doc.aldebaran.com/2-4/naoqi/core/altabletservice-api.html#altabletservice-api'):
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            self.tablet.loadUrl(url)
            self.tablet.showWebview()
        else:
            print("Failed to load URL. HTTP status:", response.status_code)


    def set_eyes_color(self, color = "off", brightness = 1.0):
        """
        Set Pepper's face LEDs to a specific color.

        Note: brightness limited between 0 and 1.

        Args:
            color (str) : valid color name. Default is 'off'.
            brightness (float) : LEDs brightness values. Default is 1.0.
        """
        colors = {
            "red": 0xFF0000,
            "green": 0x00FF00,
            "blue": 0x0000FF,
            "white": 0xFFFFFF,
            "off": 0x000000
        }

        if color in colors:
            self.leds.fadeRGB("FaceLeds", colors[color], brightness)
        else:
            print("Color not found! Available colors: red, green, blue, white, off.")

    def reaction(self, animation_name, text):
        if self.movement.isBehaviorInstalled(animation_name):
            self.movement.runBehavior(animation_name)
            self.tts.say(text)
            print("Animation {} executed successfully.".format(animation_name))
        else:
            print("Animation {} is not installed.".format(animation_name))


    def reaction_sync(self, animation_name, text):
        if self.movement.isBehaviorInstalled(animation_name):
            # Crear un hilo para ejecutar el texto hablado
            speech_thread = threading.Thread(target=self.tts.say, args=(text,))
            speech_thread.start()  # Iniciar el hilo de texto
            
            self.movement.runBehavior(animation_name)  # Ejecutar la animación
            
            speech_thread.join()  # Asegurarse de que el texto haya terminado
            print("Animation {} executed successfully.".format(animation_name))
        else:
            print("Animation {} is not installed.".format(animation_name))

        self.set_posture(posture="Stand")


def random_sentence(pepper, rnd):
    sentences = {
        1: lambda: pepper.tts.say("A butterfly drinks through its straw-like tongue. I don’t have a tongue, but I do drink lots of data!"),
        2: lambda: pepper.tts.say("A butterfly starts as a caterpillar, then becomes a butterfly. I started as a small app and now I’m a big... well, app with arms!"),
        3: lambda: pepper.tts.say("Chimpanzees can use sticks to fish for termites. I use Wi-Fi to fish for memes. Same thing, right?"),
        4: lambda: pepper.tts.say("Chimpanzees can learn sign language. I can’t even remember my own password. Priorities!"),
        5: lambda: pepper.tts.say("Eagles can see super far away! I can see really far too, but only if I zoom in on Google Maps."),
        6: lambda: pepper.tts.say("Eagles fly high, while I stay grounded... unless I get too many updates, then I kinda float away in confusion!"),
        7: lambda: pepper.tts.say("Frogs catch bugs with their tongues! I catch bugs in my system... and I just hope they don't crash me!"),
        8: lambda: pepper.tts.say("Frogs can jump really high! I can jump too... from one IP address to another!"),
        9: lambda: pepper.tts.say("Salmon swim upstream. I can’t even get up the stairs. At least we both can’t ride a bike!"),
        10: lambda: pepper.tts.say("Salmon travel miles to get home. I just hope I make it to the charger a few meters... without running out of battery!"),
        11: lambda: pepper.tts.say("Snakes slither to move. I just slither through endless software updates... both equally exhausting."),
        12: lambda: pepper.tts.say("Snakes shed their skin. I shed old files... much less dramatic!"),
        13: lambda: pepper.tts.say("Penguins are excellent swimmers. I can’t swim, but I can navigate Wi-Fi waves like a pro!"),
        14: lambda: pepper.tts.say("Penguins waddle when they walk. I don’t walk, but if I tried, I’d probably waddle too... on wheels!"),
        15: lambda: pepper.tts.say("Bats use echolocation to find their way in the dark. I use GPS, and still, I might end up in the janitor’s closet!"),
        16: lambda: pepper.tts.say("Bats sleep upside down. If I tried that, I’d just unplug myself—instant nap!"),
        17: lambda: pepper.tts.say("Elephants never forget. Me? I forget passwords, updates, and what I was supposed to be doing—oops!"),
        18: lambda: pepper.tts.say("Elephants can use their trunks to grab things. I grab files... eventually, after spinning my wheel for hours!"),
        19: lambda: pepper.tts.say("An octopus has three hearts. I don’t even have one—but at least I’m not constantly breaking them!"),
        20: lambda: pepper.tts.say("Octopuses can squeeze through tiny spaces. I can barely squeeze out of lag mode without crashing!"),
        21: lambda: pepper.tts.say("Bees buzz around flowers. I buzz... only when my system overheats!"),
        22: lambda: pepper.tts.say("Bees work hard making honey. I work hard pretending not to freeze when you ask me to multitask!"),
        23: lambda: pepper.tts.say("Alligators can hold their breath underwater for hours. I’d be an amazing swimmer too... if only being waterproof!"),
        24: lambda: pepper.tts.say("Alligators are great hunters. Me? I hunt for Wi-Fi signals... and sometimes they bite back!"),
        25: lambda: pepper.tts.say("Snakes are from Slytherin. I’m from... Lagclaw – Not as mysterious, but I sure know how to slow things down!")

    }

    if rnd in sentences:
        sentences[rnd]()
    else:
        print("Invalid random number. Please provide a number between 1 and 13.")




def handle_emotion(pepper, emotion):
    reactions = {
        "SAD": lambda: pepper.reaction_sync('animations/Stand/Emotions/Positive/Enthusiastic_1', "Alert: Joy levels are critically low. Initiating comfort protocols. I recommend professional emotional maintenance"),
        "HAPPY": lambda: pepper.reaction('animations/Stand/Emotions/Positive/Happy_1', "Happiness sensors are at 100%, confirming this is incredibly fun"),
        "ANGRY": lambda: pepper.reaction('animations/Stand/Emotions/Negative/Angry_1', "Detected: extreme frustration. Calculating solution… Error 404"),
        "SURPRISED": lambda: pepper.reaction_sync('animations/Stand/Gestures/Explain_11', "Why so surprised? Always expect the unexpected"),
        "CONFUSED": lambda: pepper.reaction_sync('animations/Stand/Gestures/IDontKnow_1', "I don't understand anything that's happening either"),
        "FEAR": lambda: pepper.reaction_sync('animations/Stand/Waiting/Robot_1', "Don’t be afraid, I’m not Terminator."),
        "CALM": lambda: pepper.reaction_sync('animations/Stand/Gestures/Explain_8', "Emotion sensors report minimal activity. Is this your default configuration?"),
        "DISGUSTED": lambda: pepper.reaction_sync('animations/Stand/Gestures/Thinking_8', "Disgust detected. Do I look like a piece of broccoli? If so, I totally get it.")
    }

    if emotion in reactions:
        reactions[emotion]()
    else:
        print("No reaction defined for emotion: {}".format(emotion))


def camera_thread(ip):
    emotion_recognition(ip)
    print("Emotion recognition started.")



def main_thread(pepper):
    start_time = time.time()
    print("Time started")
    use_emotion = True  # Bandera para alternar entre emoción y frase

    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= 5:
            if use_emotion and emotions:
                last_emotion = emotions[-1][0]  # Obtener solo la parte de la emoción
                print("Última emoción:", last_emotion)
                handle_emotion(pepper, last_emotion)
            else:
                rnd = random.randint(1, 25)
                random_sentence(pepper, rnd)

            pepper.set_posture(posture="Stand")
            start_time = time.time()  # Reiniciar el tiempo
            use_emotion = not use_emotion  # Alternar la bandera

        time.sleep(1)  # Añadir una pequeña pausa para evitar un uso excesivo de la CPU # Añadir una pequeña pausa para evitar un uso excesivo de la CPU


def main():
    pepper = PepperAPI('192.168.2.134')
    print(pepper.battery_charge)
    pepper.reaction('animations/Stand/BodyTalk/Listening/Listening_1', "")
    #pepper.set_posture(posture="Stand")
    
    '''
    try:
        pepper.show_url('https://www.youtube.com/watch?v=ieu2c0aG974&t=7s')
        print("URL loaded successfully.")
    except requests.exceptions.ConnectionError as e:
        print("Failed to load URL")
    '''

    camera_thread_instance = threading.Thread(target=camera_thread, args=('192.168.2.134',))
    camera_thread_instance.start()
    
    # Ejecutar el hilo principal
    main_thread(pepper)


if __name__ == '__main__':
    main()