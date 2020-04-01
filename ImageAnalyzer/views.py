from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from . import settings
from . import models
import time
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

curl = settings.CURRENT_URL
media_url = settings.MEDIA_URL

def home(request):
	if request.method == "GET":
		return render(request, "home.html", {'curl':curl, 'output': ''})

	else:
		current_time = time.time()
		time_tuple = time.localtime(current_time)
		date = time.asctime(time_tuple)

		fs = FileSystemStorage()

		imgname = request.FILES['filename']
		filename = fs.save(imgname.name,imgname)
		# print("imgname = ", imgname)
		# print("filename = ", filename)

		testimg1 = request.FILES['testfile1']
		testfile1 = fs.save(testimg1.name,testimg1)
		# print("testimg1 = ", testimg1)
		# print("testfile1 = ", testfile1)

		testimg2 = request.FILES['testfile2']
		testfile2 = fs.save(testimg2.name,testimg2)
		# print("testimg2 = ", testimg2)
		# print("testfile2 = ", testfile2)

		testimg3 = request.FILES['testfile3']
		testfile3 = fs.save(testimg3.name,testimg3)
		# print("testimg3 = ", testimg3)
		# print("testfile3 = ", testfile3)

		# query = "insert into imagesinfo values(NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (imgname, filename, testimg1, testfile1, testimg2, testfile2, testimg3, testfile3, testimg4, testfile4, date)
		# query = "insert into imagesinfo values(NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NULL, NULL, '%s')" % (imgname, filename, testimg1, testfile1, testimg2, testfile2, testimg3, testfile3, date)
		# query = "insert into imagesinfo values(NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (imgname, filename, testimg1, testfile1, testimg2, testfile2, testimg3, testfile3, date)
		query = "insert into imageinfo values(NULL, '%s', '%s', '%s', '%s', '%s')" % (filename, testfile1, testfile2, testfile3, date)
		models.cursor.execute(query)
		models.db.commit()

		return render(request, "home.html", {'curl':curl, 'output':'------Uploaded Successfully------'})

def result(request):
	imageid = request.GET.get("imageid")

	print("imageid = ", imageid)

	query = "select * from imageinfo where imageid = '%s';" % (imageid)
	models.cursor.execute(query)
	imglist = models.cursor.fetchall()
	imgname = request.GET.get("imgname")

	print("imglist = ", imglist)

	c = []
	    
	def compare_images(imageA, imageB):
	    s = ssim(imageA, imageB)
	    c.append(s)

	print(settings.MEDIA_URL)


	
	# load the images
	media = "D:/imageanalyzer/media/"

	path = media + str(imglist[0][1])
	print(path)
	original = cv2.imread(path)

	path = media + str(imglist[0][2])
	print(path)
	edited1 = cv2.imread(path)

	path = media + str(imglist[0][3])
	print(path)
	edited2 = cv2.imread(path)

	path = media + str(imglist[0][4])
	print(path)
	edited3 = cv2.imread(path)

	# convert the images to grayscale
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	edited1 = cv2.cvtColor(edited1, cv2.COLOR_BGR2GRAY)
	edited2 = cv2.cvtColor(edited2, cv2.COLOR_BGR2GRAY)
	edited3 = cv2.cvtColor(edited3, cv2.COLOR_BGR2GRAY)

	compare_images(original, original)
	compare_images(original, edited1)
	compare_images(original, edited2)
	compare_images(original, edited3)

	print(c)
	

	if request.method == "GET":
		return render(request, "result.html", {'curl':curl, 'imglist': imglist, 'media_url': media_url, 'c': c})
		

def history(request):
	query = "select * from imageinfo;"
	models.cursor.execute(query)
	imglist = models.cursor.fetchall()
	
	imgname = request.POST.get("imgname")

	print("imglist = ", imglist)
	# print("imgname = ", imgname)

	# for x in imglist[0]:
		# print(x)
	

	count = 0
	
	if request.method == "GET":
		return render(request, "history.html", {'curl':curl, 'media_url': media_url, 'imglist': imglist, 'count':count})
