from ArabicOcr import arabicocr
from flask import Flask, request, Response, jsonify
import os
import time
import json
from PIL import Image

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello'

@app.route('/ocr', methods=['POST'])
def run_ocr():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
		    return "File not found"
		file = request.files['file']
		if file and allowed_file(file.filename):
			# get the file input
			millisec = time.time() * 1000
			filename = 'sample_' + str(millisec) + '.jpg'
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			out_image = 'out_' + str(millisec) + '.jpg'

			# convert to grayscale
			img = Image.open(filename)
			imgGray = img.convert('L')
			imgGray.save(filename)

			# perform OCR
			results = arabicocr.arabic_ocr(filename, out_image)
			# format response
			words=[]
			for i in range(len(results)):
				word=results[i][1]
				if word:
					words.append(word)
			# cleanup					
			os.remove(filename)
			os.remove(out_image)
			# return
			return app.response_class(response=json.dumps(words),
                                  status=200,
                                  mimetype='application/json')

	error = {}
	error["message"] = "Bad request"
	return app.response_class(response=json.dumps(error),
                              status=400,
                              mimetype='application/json')			

