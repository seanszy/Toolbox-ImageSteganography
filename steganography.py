"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    red_loaded = red_channel.load()
    encoded_image.show()

    #for loop runs through each pixel in the x and y
    for y in range( y_size):
        for x in range( x_size):
            #uses the find_LSB function to find the LSB of each red part of
            #each pixel
            decode_pixel = find_LSB(red_loaded[x,y])
            decode_pixel = int(decode_pixel)
            #sets to black if 0 and white if 1
            if decode_pixel == 0:
                decode_pixel = (0, 0, 0)
            if decode_pixel == 1:
                 decode_pixel = (255, 255, 255)
            #puts the new pixel value into the matrix
            pixels[x, y] = decode_pixel
    #saves and displays it
    decoded_image.save("images/decoded_image.png")
    decoded_image.show()

def find_LSB(int_number):
    """This method takes the red part of each pixel and finds the LSB of it"""
    #convert to binary
    binary_number = bin(int_number)
    #convert binary to string
    binary_string = str(binary_number)
    #find and return the last number of the binary sequence
    LSB = binary_string[-1]
    return(LSB)

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)
    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_LSB(R_value, LSB):
    """This method takes in a LSB from a black and white text that is used
    to encode the message. It also takes in the Red channel from the pixel that
    it should code the LSB on to"""
    #finds the string in binary
    binary_number = bin(R_value)
    binary_string = str(binary_number)
    length = len(binary_string)
    #makes the old LSB the new LSB from the black and white image
    binary_string = binary_string[0: length-1] + str(LSB)
    #converts it back to integers
    New_R_Value = int(binary_string, 2)
    return New_R_Value

def encode_image(text_to_encode, template_image="images/encode2.png"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    unencoded_image = Image.open(template_image)
    #sets up the image so it can be edited
    unencoded_image_2 = unencoded_image.load()
    red_channel = unencoded_image.split()[0]
    #sets up red channel so it can be edited
    red_channel_unencoded = red_channel.load()
    x_size = unencoded_image.size[0]
    y_size = unencoded_image.size[1]
    #finds the image matrix of an image with the secret text
    pixels = write_text(text_to_encode, unencoded_image.size)
    red_channel_pixels = pixels.split()[0]
    pixels_red = red_channel_pixels.load()

    #loop to encode values into image
    for y in range(y_size):
        for x in range( x_size):
            #uses find_LSB from above to find what LSB values should be
            #encoded into the image
            LSB = find_LSB(pixels_red[x,y])
            #finds the red channel of each pixel
            R_value = red_channel_unencoded[x, y]
            #finds the new red pixel after encoding it
            temporary_red = encode_LSB(R_value, LSB)
            #finds the current red and blue pixel channels
            temp_pixel = unencoded_image_2[x, y]
            temp_blue = temp_pixel[1]
            temp_green = temp_pixel[2]
            #puts red, green, and blue together to make the new pixel
            new_pixel = (temporary_red, temp_blue, temp_green)
            #sets the new pixel in the matrix
            unencoded_image_2[x, y] = new_pixel
    #saves and shows it
    unencoded_image.save("images/encoded_image_sean.png")
    unencoded_image.show()

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()
    print("Encoding the image...")
    encode_image("I can encode messages")
    print("Decoding the image I encoded...")
    decode_image("images/encoded_image_sean.png")
