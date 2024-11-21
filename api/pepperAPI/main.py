"""CSC_5RO11_TA, AI for Robotics."""

# import sys
# print "\n".join(sys.path)   # uncomment for debug

import pepper_api




def main():
    pepper = pepper_api.PepperAPI('192.168.2.133')
    print(pepper.battery_charge)

    pepper.show_url('http://doc.aldebaran.com/2-4/naoqi/core/altabletservice-api.html#altabletservice-api')


    # Infinite loop.
    while True:
        pass

    # pepper.rest()
    # pepper.set_eyes_color("off")




if __name__ == '__main__':
    main()
