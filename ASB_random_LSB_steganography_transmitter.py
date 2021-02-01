# ASB #
import numpy as np
import cv2
import math
import re

#***# DESCRİPTİON
# Characters that used in this steganography are represented with least 7 significant bits of their ascii codes:
# All ascii characters except extended characters has a 0 bit at (from left to right) 8th digit.
# Because of we wont use any extended ascii character in this steganography, the msb of ascii code is useless in this case, which is always 0. so we work on only l7sb 
# img[row,column]   : integer value of pixel which is positioned in specified row(y) and column(x) 

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
print("----------------------------------------------")
print("| ASB Random LSB Steganography [Transmitter] |")
print("----------------------------------------------")

																	#***# WRİTE STEGANO MESSAGES TO AN İMAGE
																	#***# STAGE 1 : Get message text, remove unwanted characters from input_text
print("Images with lossless formats must be used. Example: .bmp | .png")
targetImgFileName = input("Target image file name to encrypt (full name with extension): ")	
# targetImgFileName = "lena512.bmp"
img_before = cv2.imread(targetImgFileName,0)	
img = cv2.imread(targetImgFileName,0)									# Grayscale image
height, width = img.shape 												# Get size of image
max_chars = (math.floor((height*width)/7))								# Each character represented with 7 bits.each bit is buried into a pixels lsb 


while(1):
	print("\nPlease write yout text to bury into image.\nYour text must be shorter than image capacity and must not include extended character!")
	print("\nImage Capacity : Maximum %d characters"%(max_chars))
	input_text = input("\nEnter text (Special characters, numbers and spaces are not allowed): ")
	text = ''.join(filter(str.isalnum, input_text)) 					# Remove spaces and special characters
	text = re.sub(r'[ş|ç|ö|ü|ğ]',r'',text)								# Remove specific extended characters								
	if(len(text)<max_chars):
		break
	print("Please write less than %d characters"%(max_chars))
	
while(1):																# Get key value for decoding algorithm. Key value must only contain positive integers.
	input_key = input("\nEnter integer 3 digit key for decoding algorithm : ")		
	input_key = input_key.replace(" ", "") 
	if(len(input_key) == 3):
		try:
			key = int(input_key)
		except ValueError:
			print("Please only use positive integers for key value.")
			key=-1
		else:
			if(key>=0):													# İf everything is okay, break while loop
				break
			print("Please only use positive integers as key value.")
#print("[TEST]Key=",key)													# TEST



																	#***# STAGE 2 : Convert characters into binary numbers respecting to ascii table. Create bitwise message
	
bitwise_text = ""
for t in range (len(text)):
	decimal_value_of_current_char = ord(text[t])						# Characters decimal value in ascii table
	binary_value_of_current_char = bin(decimal_value_of_current_char)	# Binary representation of this decimal value (stored as string variable)
	l7sb = binary_value_of_current_char[2:9]							# Get least 7 significant bits of binary string
	
	bitwise_text += l7sb												# Add least 7 significant bits of character's binary ascii code to bitwise_text string, which is going to be buried into least significant bits of pixel values of image
print("[TEST]Text=",text)												# TEST	
print("[TEST]Bitwise_text=",bitwise_text)								# TEST	


keyFileName = input("Key file name (full name with extension): ")
#keyFileName = "key.txt"
file = open(keyFileName,"w") 											# Write key number to a text file which is required for ASB_randomGraveDigger
file.write(str(key)+str(len(bitwise_text)))								# key includes length of bitwise text
file.close() 

graves = ASB_randomGraveDigger(width,height,len(bitwise_text),key)		
#print("[TEST]graves = ",graves)										# TEST


parse_count = 0
for i in range(len(graves[0])):
	x =	graves[0][i] 													# Get X (Column) coordinates of next pixel location
	y =	graves[1][i]													# Get Y (Row) coordinates of next pixel location
	pixel_value_decimal = img[y,x] 										# img[row,column] returns int pixel value 
	pixel_value_binary = bin(pixel_value_decimal)						# Cast decimal value to binary (variable type is string)
	lsb = int(pixel_value_binary[-1])									# Last character of binary string is lsb
	selected_bit = int(bitwise_text[parse_count])						# Cast string bit to integer
	bit_difference = selected_bit - lsb									# for example : parsed_msg=0 and lsb=1 , then bit_difference=-1 . so if current pixel value is 0b00110011 ,lsb of this value need to be 0 
	img[y,x] = img[y,x] + (bit_difference)								# After summing with (-1) current pixel value becomes 0b00110010.  in this case , we turned lsb from 1 to 0 as we desired.	
	parse_count += 1
	if(parse_count >= len(bitwise_text)):								# When all bitwise_text string is parsed, break for loop
		break


			
encryptedImgFileName = input("Name for encrypted image file (full name with extension): ")
# encryptedImgFileName = "lena512_lsbstego.bmp"			
cv2.imwrite(encryptedImgFileName,img) 							# Write new stegano image with secret message buried inside linearly
img_after = img


print("\nYour message has been buried successfully to file: ",encryptedImgFileName)


#***# SHOW QUALITY PARAMETERS
# Read original image			
# Get size of image
# Read steganographic image	after steganography process	

MSE = 0																	# Calculate Mean Square Error (MSE) rate between before and after images
for y in range (height):
	for x in range (width):
		MSE += (int(img_before[y,x]) - int(img_after[y,x]))**2
	
MSE = MSE/(height*width)	
print("\nMean Square Error (MSE) =",MSE)

PSNR = 10*math.log10((255**2)/MSE)										# Calculate Peak Signal Noise Ratio (PSNR)
print("\nPeak Signal Noise Ratio (PSNR) =",PSNR)
	
																		
cv2.imshow("Before Steganography", img_before)							# Visual Difference Test
cv2.imshow("After Steganography", img_after)	
cv2.waitKey(0)		









