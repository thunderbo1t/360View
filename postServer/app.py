import os
import cv2
from flask import Flask, render_template, request
from flask_json import *
import imagehash
import numpy as np
from PIL import Image
from scipy.signal import savgol_filter


app = Flask(__name__)
json = FlaskJSON(app)

@app.route('/')
def hello_world():    
	l = os.listdir("./")
	for I in ["app.py","app.pyc","music","src","templates","var","Readme.html","Readme.md"]:
		l.remove(I)
	return render_template("home.html",items=l)

@app.route("/test")
def Test():
	return render_template("test.html")

@app.route("/getPage",methods=["POST"])
def getPage():
	page = request.form['button']
	return render_template(page+"/"+page+".html")

@app.route('/upload', methods=['POST','GET'])
def upload_file():
	file = request.files["video"]
	if file.filename not in os.listdir("."):
		f = os.path.join(".", file.filename)
	else:
		f = "./"+file.filename
	file.save(f)
	extract(f,file.filename.split(".")[0])
	return json_response(success="success")
	return json_response(success="Failed")



def avgHash(img1,img2):
	hash1 = imagehash.average_hash(img1)
	hash2 = imagehash.average_hash(img2)
	return hash1-hash2

def cut_redundant(folder,num,window=51,order=3):
	if (window % 2==0):
		window += 1
	start = Image.open("./"+folder+"/img/"+folder+"0.png")
	hist = []
	for I in range(num):
		path = "./"+folder+"/img/"+folder+I.__str__()+".png"
		img = Image.open(path)
		hist.append(avgHash(start,img))
	final_hist = savgol_filter(hist, window, order)
	min_Hist= 9999
	min_ind= num
	minFound = False
	for I in range(num-3,num - (num//4),-1):
		if ( final_hist[I] < min_Hist ):
			min_Hist = final_hist[I]
			min_ind = I
			minFound = True 
	return min_ind


def extract(vid,folder):
	cap = cv2.VideoCapture(vid)
	i = 0
	j=0
	os.makedirs("./"+folder+'/img')
	while(cap.isOpened()):
		ret, frame = cap.read()
		if i% 5   == 0 and ret:
			f = cv2.resize(frame, (1000, 500))
			cv2.imwrite('./'+folder+'/img/'+folder+j.__str__()+'.png',f)
			j=j+1
		i= i+1
		if ret == False:
			break
	print (folder)
	j = cut_redundant(folder,j,j//4)
	print "image written"
	cap.release()
	os.remove(vid)
	createHTML(j,folder)


def createHTML(totalFrames,file):
	temp = '''<html>
		<head>

		<link rel='stylesheet' href='../../src/threesixty.css'>
		<script src='../src/jquery.js'></script>
		<script src='../src/threesixty.js'></script>
		<script type='text/javascript'>
		window.onload = init;

		var product1;
		function init(){

				product1 = $('.product1').ThreeSixty({
					totalFrames: TOTALCOUNT_OF_FRAMES,
					endFrame: ENDFRAME,
					currentFrame: 0,

					imgList: '.threesixty_images',
					progress: '.spinner',
					imagePath:'img/',
					filePrefix: 'FILE_PREFIX',
					ext: '.png',
					height: 350,
					width: 700,
									navigation: true,
					disableSpin: true
			});


			$('.custom_previous').bind('click', function(e) {
			  product1.previous();
			});

			$('.custom_next').bind('click', function(e) {
			  product1.next();
			});

		}
	</script>
	</head>
	<body>

	<div class='threesixty car product1'>
		<div class='spinner'>
			<span>0%</span>
		</div>
		<ol class='threesixty_images'></ol>
	</div>
	<div style="padding: 10px;">
	<CENTER>
		<button class="button custom_next" style="vertical-align:middle"><span>next</span></button>	
		<button class="button custom_previous" style="vertical-align:middle"><span>Previous</span></button>
	</CENTER>
	</div>
		 <audio autoplay>
		 <source src="../music/happy.mp3" type="audio/mpeg">
		 <audio>
			 Your browser does not support the audio element.
		 </audio>
	</body>
	</html>'''

	temp = temp.replace('TOTALCOUNT_OF_FRAMES',str(totalFrames-1))
	temp = temp.replace('ENDFRAME',str(totalFrames-1))
	temp = temp.replace('FILE_PREFIX',file)
	with open('./'+file+'/'+file+'.html','w') as outputHTML:
		outputHTML.write(temp)




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
