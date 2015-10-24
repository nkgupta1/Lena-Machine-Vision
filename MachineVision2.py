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
GAUSSIAN = [[1,2,1], [2,4,2], [1,2,1]]

def main():
    #pull image data from ppm graphics file into a list of string-type numbers (nums)
    file1 = open('grayScale.ppm', 'r')
    stng  = file1.readline().strip()
    print (stng)
    nums  = file1.read().split()
    print (nums[:10])
    file1.close()

    #Create list of gray-values from the file nubmber (cast from strings to ints)
    image = []
    for pos in range(3, len(nums)):
        image.append(int(nums[pos]))

    for i in range(NUMBER_OF_TIMES_TO_SMOOTH_IMAGE):
        image = blur(image)

    # Write gray-values blurred to file
    file1 = open('grayScaleBlurred.ppm', 'w')
    file1.write('P2\n512 512\n255\n')
    for elt in image:
        file1.write(str(elt) + ' ' )
    printElapsedTime('saved file numbers')
    file1.close()

    #Display grayScale files as an iamge.
    displayImageInWindow(image)

    root.mainloop()

def blur(image):
    #print(len(image))
    image2 = [0] * WIDTH * HEIGHT
    for row in range(1, HEIGHT - 1):
        for col in range(1, WIDTH - 1):
            val = 0
            for r in range(-1, 2):
                for c in range(-1, 2):

                    # print((row+r)*WIDTH + col + c)
                    val += image[(row+r)*WIDTH + col + c] * GAUSSIAN[r + 1][c + 1]
            val = int(val / 16)
            image2[row*WIDTH + col] = val
    return image2

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
