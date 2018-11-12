# Kyle Thomas
# Functions to perform stenography on images
# Encoding:
# $ python stenography.py -e <message file> <original image> <new encoded image>
# Decoding:
# $ python stenography.py -d <image with message> <message file>
# Only works with png image formats, messages should be a text file


from sys import argv
from graphics import Image, Point, color_rgb


# Purpose:  To convert an ascii string to a binary representation
#   Input:  A string
#  Output:  A string representing the input in binary
def convert_ascii_to_binary(ascii_txt):
    binary_txt = ""
    for char in ascii_txt:
        binary_char = "{0:07b}".format(ord(char))
        binary_txt += binary_char
    binary_txt += "1111111"  # terminating character
    return binary_txt


# Purpose: To convert a binary string into the ascii characters
#   Input: A binary string
#  Output: The string in ascii represenation
def convert_binary_to_ascii(binary_string):
    message = ""
    tmp_buffer = ""
    count = 0
    for bit in binary_string:
        tmp_buffer += bit
        count += 1
        if count == 7:
            count = 0
            if tmp_buffer == "1111111":
                break
            message += chr(int(tmp_buffer,2))
            tmp_buffer = ""

    return message


# Purpose: To decode an image
#   Input: An image object with a message encoded
#  Output: A message in binary ascii form
def decode_image(image):
    width = image.getWidth()
    height = image.getHeight()

    # Create binary string
    binary_string = ""
    for x_pixel in range(width):
        for y_pixel in range(height):
            currentPixel = image.getPixel(x_pixel,y_pixel)
            for value in currentPixel:
                if value % 2 == 0:
                    binary_string += "0"
                else:
                    binary_string += "1"            

    return binary_string


# Purpose: To encode text into a picture
#   Input: An image object and a binary message to encode
#  Output: An image object with the message encoded
def encode_image(image, binary_message):

    # make the message divisiable by 3
    while len(binary_message) % 3 != 0:
        binary_message += "0"

    message_length = len(binary_message)
    
    width = image.getWidth()
    height = image.getHeight()

    # Iterate through pixels and change RBG value based on binary value above
    # Checks to see if picture is large enough
    if (message_length / 3) <= (width * height):          
        for x_pixel in range(width):
            for y_pixel in range(height):
                if binary_message == "":
                    break
                red, green, blue = image.getPixel(x_pixel,y_pixel)

                # Red Value
                if int(binary_message[0]) == 0 and red % 2 != 0:
                    red += 1
                    if red > 126:
                        red -= 2
                elif int(binary_message[0]) == 1 and red % 2 == 0:
                    red += 1
                    if red > 126:
                        red -= 2

                # Green Value
                if int(binary_message[1]) == 0 and green % 2 != 0:
                    green += 1 
                    if green > 126:
                        green -= 2
                elif int(binary_message[1]) == 1 and green % 2 == 0:
                    green += 1
                    if green > 126:
                        green -= 2
                
                # Blue Value
                if int(binary_message[2]) == 0 and blue % 2 != 0:
                    blue += 1
                    if blue > 126:
                        blue -= 2
                elif int(binary_message[2]) == 1 and blue % 2 == 0:
                    blue += 1
                    if blue > 126:
                        blue -= 2

                # Set new RGB values
                image.setPixel(x_pixel, y_pixel, color_rgb(red, green, blue))
                binary_message = binary_message[3:]  # cut off first 3 values
    else:
        raise Exception("Picture is too small for message")

    return image


# Purpose: To open a file and return the contents
#   Input: A string that will be the file name
#  Output: The contents of the file
def read_file(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text


# Purpose: To write a string to a file
#   Input: The string to write the to file and the file name
#  Output: None
def write_to_file(contents, filename):
    f = open(filename, "w")
    print(contents, file=f)
    f.close()
    return


def main():
    if "-e" in argv[1]:  # encode
        image = Image(Point(0,0), argv[3])
        #h = image.getHeight()
        #w = image.getWidth()
        #image = Image(Point(w / 2, h / 2), argv[3])
        message = convert_ascii_to_binary(read_file(argv[2]))
        image = encode_image(image, message)
        image.save(argv[4])
    elif "-d" in argv[1]:  # decode
        image = Image(Point(0,0), argv[2])
        #h = image.getHeight()
        #w = image.getWidth()
        #image = Image(Point(w / 2, h / 2), argv[2])
        message = decode_image(image)

        write_to_file(convert_binary_to_ascii(message), argv[3])

    else:
        print("Please use the following format:")
        print("-e <message> <original image> <new image> for encoding")
        print("-d <image> <decoded message> for decoding")

    exit(0)


main()