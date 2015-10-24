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
Sy = [[1,2,1], [0,0,0], [-1,-2,-1]]
Sx = [[-1,0,1], [-2,0,2], [-1,0,1]]

def main():
    # pull image data from ppm graphics file into a list of string-type numbers (nums)
    file1 = open('grayScaleBlurred.ppm', 'r')
    stng  = file1.readline().strip()
    print (stng)
    nums  = file1.read().split()
    print (nums[:10])
    file1.close()

    image = []
    for pos in range(3, len(nums)):
        image.append(int(nums[pos]))


    image = sobel(image)

    #Determine boundary edge point
    image = boundary(image)

    #check with threshold
    image = threshold(image)


    #Display grayScale files as an iamge.
    displayImageInWindow(image)

    root.mainloop()

def threshold(image):
    for row in range(HEIGHT):
        for col in range(WIDTH):
            image[(row) * WIDTH + col][3] = 1 #been here
            if image[(row)*WIDTH + col][2] == 0: continue

            if image[(row)*WIDTH + col][0] > HIGH:
                image[(row)*WIDTH + col][4] = 1
                image = fixCellAt(image, row, col)
    return image

def fixCellAt(M, row, col):
    #base
    if M[(row) * WIDTH + col][3] == 1: return M

    M[(row) * WIDTH + col][3] = 1 #been here

    #fix above
    if (row > 0 and M[(row-1) * WIDTH + col][2] == 1 and M[(row-1) * WIDTH + col][0] > LOW):
        M[(row-1) * WIDTH + col][3] = 1  #been here
        M[(row-1) * WIDTH + col][4] = 1  #marked to be printed
        # M = fixCellAt(M, row-1, col)

    #fix below
    if (row < HEIGHT - 1 and M[(row+1) * WIDTH + col][2] == 1 and M[(row+1) * WIDTH + col][0] > LOW):
        M[(row+1) * WIDTH + col][3] = 1  #been here
        M[(row+1) * WIDTH + col][4] = 1  #marked to be printed
        # M = fixCellAt(M, row+1, col)

    #fix left
    if (col > 0 and M[(row) * WIDTH + col - 1][2] == 1 and M[(row) * WIDTH + col-1][0] > LOW):
        M[(row) * WIDTH + col - 1][3] = 1  #been here
        M[(row) * WIDTH + col - 1][4] = 1  #marked to be printed
        # M = fixCellAt(M, row, col - 1)

    #fix right
    if (col < WIDTH - 1 and M[(row) * WIDTH + col + 1][2] == 1 and M[(row) * WIDTH + col+1][0] > LOW):
        M[(row) * WIDTH + col + 1][3] = 1  #been here
        M[(row) * WIDTH + col + 1][4] = 1  #marked to be printed
        # M = fixCellAt(M, row, col + 1)

    return M


def boundary(image):
    for row in range(1, HEIGHT - 1):
        for col in range(1, WIDTH - 1):
            r1,c1, r2,c2 = 0,0, 0,0
            theta = image[(row)*WIDTH + col][1]
            if   theta == 0: r1,c1, r2,c2 = 0,-1,0,1
            elif theta == 1: r1,c1, r2,c2 = 1,-1,-1,1
            elif theta == 2: r1,c1, r2,c2 = -1,0,1,0
            elif theta == 3: r1,c1, r2,c2 = -1,-1,1,1

            val = image[(row)*WIDTH + col][0]
            image[(row)*WIDTH + col][2] = int((val > image[(row+r1)*WIDTH + col + c1][0])
                                          and (val > image[(row+r2)*WIDTH + col + c2][0]))

    return image

def sobel(image):
    image2 = [[0,0,0,0,0] for elt in range(HEIGHT * WIDTH)]
    for row in range(1, HEIGHT - 1):
        for col in range(1, WIDTH - 1):
            Gx, Gy = 0, 0
            for r in range(-1, 2):
                for c in range(-1, 2):

                    val = image[(row+r)*WIDTH + col + c]

                    Gx += val * Sx[r + 1][c + 1]
                    Gy += val * Sy[r + 1][c + 1]
            from math import sqrt
            M = sqrt(Gx*Gx + Gy*Gy)
            D = theta(Gx, Gy)
            image2[row*WIDTH + col] = [M, D, 0, 0, 0]
    return image2

def theta(Gx, Gy):
    from math import atan2, pi
    T = atan2(Gy, Gx) + (Gy < 0) * pi
    return int( (T + pi / 8) // (pi / 4)) % 4

class ImageFrame:
    def __init__(self, image):
        self.img = PhotoImage(width = WIDTH, height = HEIGHT)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                # print(row, col)
                num = 255 * image[row*WIDTH + col][2] * image[row*WIDTH + col][4]
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