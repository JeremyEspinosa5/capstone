#!/usr/bin/python3
#Project GlaDos
#Filename: capstone.py
#ITSC-310 System Security Capstone
#Author: Jeremy Espinosa & Kenny Truong

#Progam collects images of the desired target from the internet and only retains those that match with the original photo of the target in question

from google_images_search import GoogleImagesSearch
import face_recognition
import os
import datetime

#API and CX keys used to run google image search
gis = GoogleImagesSearch('API', 'CX')

#Deletes images that do not match the face of the target
def deleteImg(knownFace, wrongImages):

	print("Deleting unusable images!")
	for pics in wrongImages:
		try:
			os.remove(f"{knownFace}/{pics}")
		except:
			pass

#Compares a photo of the target with the collected photos from the internet
def facialRec(knownFace, fileName):
	pictureList = []
	wrongImages = []

	#Stores file names of collected images in a list 
	for root, dirs, files in os.walk(knownFace):
		for fileList in files:
			pictureList.append(fileList)
	#Iterates through collected images
	for pics in pictureList:
		print(f"Scanning {pics}!")
		known_image = face_recognition.load_image_file(fileName)
		try:
			unknown_image = face_recognition.load_image_file(f"{knownFace}/{pics}")
		#Used to skip when a blank .jpg is downloaded
		except:
			pass

		#Get the face encodings for each face in each image file
		#Removes any files that do not have a face
		try:
			known_face_encoding = face_recognition.face_encodings(known_image)[0]    	
			unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
		except IndexError:
			print("I wasn't able to locate any faces in at least one of the images. Deleting the image files.")
			wrongImages.append(pics)

		known_faces = [
   			known_face_encoding
		]

		#Results is an array of True/False telling if the unknown face matched anyone in the known_faces array
		results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
		if not results[0]:
			print("Not the person you are looking for! File will be deleted!")
			wrongImages.append(pics)

	deleteImg(knownFace, wrongImages)

#Asks user for original image location
def originalPic():
	print("\nPlease ensure a pic of the person you want to search for exists within the current folder")
	namePic = input("Please enter the name of the picture to be compared by the program: ")
	#Original image must contain the proper extensions 
	if namePic.endswith(('.jpg', '.png', '.gif')):
		return namePic
	else:
		print("File is not supported must be a .gif/.jpg/.png file! Exiting!")
		exit()

#Asks user for the search parameters
def setParameters():
	print("Please input desired parameters for the following fields:\n(Only query and number of images must be filled. Leave fields blank if specification is not needed.) ")
	query = input("Query (name of person you want to collect data on): ")
	if query == '':
		print("Query cannot be blank! Exiting!")
		exit()
	searchNum = input("Number of images to be collected in google images: ")
	if searchNum == '':
		print("Number of images cannot be blank! Exiting!")
		exit()
	elif not searchNum.isdigit() :
		print("Number of images must be a number! Exiting!")
		exit()
	fileType = input("Type of file to be collected (jpg/gif/png): ")
	if fileType not in ['jpg','png','gif','']:
		print("Type of file must be jpg/gif/png or blank! Exiting!")
		exit() 
	imageType = input("Type of image to be collected (clipart/face/lineart/news/photo): ")
	if imageType not in ['clipart','face','lineart','news','photo','']:
		print("Type of image must be clipart/face/lineart/news/photo or blank! Exiting!")
		exit()
	imageSize = input("Size of images to be collected (huge/icon/large/medium/small/xlarge/xxlarge): ")
	if imageSize not in ['huge','icon','large','medium','small','xlarge','xxlarge','']:
		print("Image size must be huge/icon/large/medium/small/xlarge/xxlarge or blank! Exiting!")
		exit()
	print("Downloading Images...")
	return query, searchNum, fileType, imageType, imageSize

#Header
def startUp():
	dateCurrent = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print(f'''
	______          _           _     _____  _          ______ _____ _____ 
	| ___ \        (_)         | |   |  __ \| |         |  _  \  _  /  ___|
	| |_/ / __ ___  _  ___  ___| |_  | |  \/| |     __ _| | | | | | \ `--. 
	|  __/ '__/ _ \| |/ _ \/ __| __| | | __ | |    / _` | | | | | | |`--. |
	| |  | | | (_) | |  __/ (__| |_  | |_\ \| |___| (_| | |/ /\ \_/ /\__/ /
	\_|  |_|  \___/| |\___|\___|\__|  \____/\_____/\__,_|___/  \___/\____/ 
	              _/ |                                                     
	             |__/                                                      
                                                                          
	***********************************************************************
	*                                                                     *
	*              Created By: Jeremy Espinosa & Kenny Truong             *
	*                                                                     *
	*                         Course: ITSC-310                            *
	*                                                                     *
	*                        {dateCurrent}                          *
	*                                                                     * 
	***********************************************************************
																		  ''')
											   
def main():
	startUp()
	option = setParameters()
	# define search params:
	_search_params = {
	    'q': option[0],
	    'num': int(option[1]),
	    'fileType': option[2],
	    'imgType': option[3],
	    'imgSize': option[4],
	}

	# this will search and download:
	gis.search(search_params=_search_params, path_to_dir=option[0])

	fileName = originalPic()

	facialRec(option[0], fileName)

	print("All usable images successfully downloaded! Terminating program!")

if __name__ == "__main__":
	main()
