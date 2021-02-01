# ASB #
import numpy as np
import cv2
import math

def ASB_randomGraveDigger (img_width,img_heigth,msg_length,key):					# Function for determination of steganography burial locations
	total = img_width*img_heigth
	matrix = [[0 for x in range(img_width)] for y in range(img_heigth)] 			# Creates a list containing int(heigth) lists, each of int(width) items, 
																						#all set to 0. its a virtual map for current image. 
																						#if an item is set to 0 this means pixel of image that holds these coordinates is free to bury a bit. 
																						#if its 1 then this pixel already holds a message bit. which means its full
	msg_matrix = [[0 for x in range(msg_length)] for y in range(2)]					# msg_matrix[pos_axis(0=X,1=Y):msg pixel coordinates][order number(0 to msg_length):msg bit order]
																						# msg_matrix[row][column] 
																						# msg_matrix[0][0]=X coordinates of first bit of msg ; msg_matrix[1][0]=Y coordinates of first bit of msg...
	
	counter = 0																		# A counter for operation loop count
	
	key = key + 458																	# ASB ;)
	while(counter < msg_length):
		x1 = (key**2)+(2*key)+1997													# Operations for a random generated number between 0 and "total" 
		x2 = x1 + int(math.log(key, 2))												# İncludes logarithmic and exponential equations for safety
		x3 = x2 + int(math.log(x2, 5))
		x4 = x3 + (key**2) 
		x5 = int(math.log(x4 ,10))
		x6 = (x4**2) + x5
		x7 = x6 + img_heigth + img_heigth
		y = int(x7) % total
		pixel_order = y																# Random number is used as pixel_order number. a pixel_order number can be any number from 0 to total
		
		pixel_positionY = int(pixel_order/img_width) 								# Pixel_order number is transformed into a X and Y coordinate value 
		pixel_positionX = int(pixel_order%img_width)  
		#print("\n[TEST]pixel_positionX=%d, pixel_positionY=%d, pixel_order=%d" %(pixel_positionX,pixel_positionY,pixel_order))	#TEST
		if (matrix[pixel_positionY][pixel_positionX] == 0):							# İf current coordinate (which represent a pixel of image) does not hold any buried bit,
			matrix[pixel_positionY][pixel_positionX] = 1
			msg_matrix[0][counter]=pixel_positionX									# Save coordinates of new pixel
			msg_matrix[1][counter]=pixel_positionY	
		else:
			while(1):
				pixel_order += 1
				pixel_order = pixel_order % total
				pixel_positionY = int(pixel_order/img_width) 
				pixel_positionX = pixel_order%img_width
				#print("[TEST]Cell Full. Iterating pixel_order number...")																#TEST
				#print("[TEST]pixel_positionX=%d, pixel_positionY=%d, pixel_order=%d" %(pixel_positionX,pixel_positionY,pixel_order))	#TEST
				if (matrix[pixel_positionY][pixel_positionX] == 0):
					matrix[pixel_positionY][pixel_positionX]=1
					msg_matrix[0][counter]=pixel_positionX
					msg_matrix[1][counter]=pixel_positionY
					break
		key = pixel_order + 1														# +1 for in case pixel_order is 0
		counter += 1
	
	return msg_matrix;
	
	
print("\n\n\n")
print("-------------------------------------------")
print("| ASB Random LSB Steganography [Receiver] |")
print("-------------------------------------------")	
																#***# STAGE 1 : Read Steganographic image, get key from text file.

encrytedImgFileName = input("Encrypted image file name to decrypt(full name with extension): ")	
# encrytedImgFileName = "lena512_lsbstego.bmp"
img = cv2.imread(encrytedImgFileName,0)								# read steganographic image	
height, width = img.shape 												# get size of image

keyFileName = input("Key file name (full name with extension): ")
# keyFileName = "key.txt"
file = open(keyFileName, "r") 											# Get key number from text file
key_file = file.read()
file.close() 
	
grave_number = int(key_file[3:])										# All other numbers except first 3 digit indicated grave_number. Which is total number of encrypted pixels				
key = int(key_file[0:3])												# First 3 digit of key_file is key 
#print("[TEST]key=%d,grave_number=%d"%(key,grave_number))				# TEST

graves = ASB_randomGraveDigger(width,height,grave_number,key)
#print("[TEST]graves=",graves)

																		
																#***# STAGE 2 : Read every pixel's value's lsb respecting to graves coordinates, store them as received_msg_bits

received_msg_bits = ""
for i in range(len(graves[0])):
	x = graves[0][i]												# Get X (Column) coordinates of next pixel location
	y = graves[1][i]												# Get Y (Row) coordinates of next pixel location
	pixel_value_decimal = img[y,x]       							# img[row,column] returns int pixel value 
	pixel_value_binary = bin(pixel_value_decimal)					# Cast decimal value to binary (variable type is string)
	lsb = int(pixel_value_binary[-1])								# Last character of binary string is lsb
	received_msg_bits += str(lsb)									# Add LSB's to received_msg_bits as string 
	
	
	
	
print("\nReceived message (bitwise) =",received_msg_bits)					# received message which collected from lsb of pixel values


																#***# STAGE 3 : split received_msg_bits into 7-bit each parts and convert these binary numbers to ascii characters,
																	# order them in received_msg_text string as result: received message
# representing ascii character with binary number example :																		
#		2^6		2^5		2^4		2^3		2^2		2^1		2^0      : digit_value
# 0b	1		1		1		1		1		1		1		 : 7-bit binary number

received_msg_text = ""
binary_value = 0b0000000												#going to change for every character through entire for loop
digit_value = 64														#in little endian order, 7th bit digit value is 2^6 = 64 so it starts processing msb to lsb 					
parse_count = 0															#when 7 bits from received_msg_bits are operated, that means operations for a character (which is represented with 7-bits) is completed.
for t in range (len(received_msg_bits)):
	current_msg_bit = int(received_msg_bits[t])							# currently parsed message bit
	binary_value += (digit_value*current_msg_bit)						# for example : 0b0000000 += (64*1) = 0b10000000  ... so it adds 1-bit to msb in this case
	digit_value = digit_value/2											# divide digit_value by 2 to proceed next lower significant digit number
	parse_count += 1
	if (parse_count >= 7):										
		character = chr(int(binary_value))								# decode binary value to character
		received_msg_text += character									# add character to received message string
		binary_value = 0b0000000										#reset loop variables
		digit_value = 64					
		parse_count=0
		
		
		
print("\nReceived message (string) =",received_msg_text)					# Received message





																	
	
	
	
	
	
	