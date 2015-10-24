#Nikhil Gupta
#Machine Vision

#GLOBALS

from tkinter  import *
from time     import clock, sleep

root      = Tk()
START     = clock()
WIDTH     = 512
HEIGHT    = 512
COLORFLAG = False
HIGH      = 45
LOW       = 10
NUMBER_OF_TIMES_TO_SMOOTH_IMAGE = 6

def main():
    #pull image data from ppm graphics file into a list of string-type numbers (nums)
    file1 = open('lena_rgb_p3.ppm', 'r')
    stng  = file1.readline().strip()
    print (stng)
    nums  = file1.read().split()
    print (nums[:10])
    file1.close()

    #Create list of gray-values from the file nubmer (cast from strings to ints)
    image = []
    for pos in range(10, len(nums), 3):
        RGB = [int(nums[pos]), int(nums[pos+1]), int(nums[pos+2]),]
        image.append(int(.3*RGB[0] + .59*RGB[1] +.11*RGB[2]))
    printElapsedTime('Gray numbers are now created.')

    #Write gray-values to file
    file1 = open('grayScale.ppm', 'w')
    file1.write('P2\n512 512\n255\n')
    for elt in image:
        file1.write(str(elt) + ' ' )
    printElapsedTime('saved file numbers')
    file1.close()

    #Display grayScale files as an iamge.
    displayImageInWindow(image)

    root.mainloop()

class ImageFrame:
    def __init__(self, image):
        self.img = PhotoImage(width = WIDTH, height = HEIGHT)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                num = image[row*WIDTH + col]
                if COLORFLAG == True:
                    kolor = '#%02x%02x%02x' % (num[0], num[1], num[2]) #color
                else:
                    kolor = '#%02x%02x%02x' % (num, num, num)
                self.img.put(kolor, (col, row))
        c = Canvas(root, width = WIDTH, height = HEIGHT); c.pack()
        c.create_image(0,0, image = self.img, anchor = NW)
        printElapsedTime('displayed image')

def printElapsedTime(msg = 'time'):
    length = 30
    msg = msg [:length]
    tab = '.'*(length-len(msg)) #msg length truncated at 30 chars
    print('--' + msg.upper() + tab + ' ', end = '')
    time = round(clock() - START, 1)    #START is global constant
    print('%2d'%int(time/60), ' min : ', '%4.1f'%round(time%60, 1), ' sec', sep = '')

def displayImageInWindow(image):
    global x
    x = ImageFrame(image)

if __name__ == '__main__': main()