import os
import cv2
from flask import Flask, render_template, request
from flask_json import *

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
    #fileList = request.files.getlist("image")
    #for file in fileList:
    file = request.files["video"]
    if file.filename not in os.listdir("."):
        f = os.path.join(".", file.filename)
	file.save(f)
	extract(f,"./"+file.filename.split(".")[0])
	return json_response(success="success")
    return json_response(success="Failed")


def writeFile(val):
    with open('var','w') as inp:
        inp.write(val)

def extract(vid,folder):
    val = None
    print os.listdir("./")
    if ("var" not in os.listdir('./')):
        writeFile(str(0))
        val = 0
    else:
        with open('var','r') as inp:
            val = int(inp.read())
            val += 1
        writeFile(str(val))
    cap = cv2.VideoCapture(vid)
    i = 0
    j=0
    folder = folder + val.__str__()
    os.makedirs(folder+'/img')
    while(cap.isOpened()):
        ret, frame = cap.read()
        if i% 5   == 0 and ret:
            f = cv2.resize(frame, (1000, 500))
            cv2.imwrite('./'+folder+'/img/'+folder+j.__str__()+'.png',f)
            j=j+1
        i= i+1
        if ret == False:
            break
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
