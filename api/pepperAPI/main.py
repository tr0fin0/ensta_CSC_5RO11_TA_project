"""CSC_5RO11_TA, AI for Robotics."""

# import sys
# print "\n".join(sys.path)   # uncomment for debug

import naoqi



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
            speed (float) : movement speed. Default value is 1.0.
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


    def show_url(
        self,
        url = 'http://doc.aldebaran.com/2-4/naoqi/core/altabletservice-api.html#altabletservice-api'
    ):
        """
        Display an webpage URL address in Pepper's tablet.

        Args:
            url (str) : webpage URL address. Default value is Aldebaran's documentation.
        """
        self.tablet.loadUrl(url)
        self.tablet.showWebview


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





def main():
    pepper = PepperAPI('192.168.2.133')
    print(pepper.battery_charge)

    pepper.show_url('http://doc.aldebaran.com/2-4/naoqi/core/altabletservice-api.html#altabletservice-api')


    # Infinite loop.
    while True:
        pass

    # pepper.rest()
    # pepper.set_eyes_color("off")




if __name__ == '__main__':
    main()
