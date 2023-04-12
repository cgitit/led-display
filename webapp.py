import os
from os import walk
import subprocess
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
quotes_file = os.path.join(basedir, 'static/quotes/quotes.txt')

# simplest example
# layout for ALL PAGES is in templates/base.html
# this route is in hello.html
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/movies/del/<movie>", methods=["POST"])
def delete_movie(movie=None):
	if movie is not None:
		try:
			movie = int(movie)-1
			movies = os.listdir("/home/pi/static/movies")
			filename = movies[movie]
			filepath = os.path.join("/home/pi/static/movies", filename)
			os.remove(filepath)
			return jsonify(success=True)
		except (ValueError, IndexError):
			return jsonify(err=True, message="Invalid movie index.")
		except Exception as e:
			return jsonify(error=True, message=str(e))
	else:
		return jsonify(error=True, message="Movie index not provided.")

@app.route("/movies", methods=["GET", "POST"])
def read_movies():
        if request.method == "POST":
                f = request.files['userMovie']
                f.save("/home/pi/static/movies/%s" % f.filename)
        movies = []
        for (dirpath, dirnames, filenames) in walk("/home/pi/static/movies"):
                movies.extend(filenames)
                break
        return render_template("movies.html", movies=movies)

@app.route("/images/del/<image>", methods=["POST"])
def delete_image(image=None):
	if image is not None:
		try:
			image = int(image) - 1
			images = os.listdir("/home/pi/static/images")
			filename = images[image]
			filepath = os.path.join("/home/pi/static/images", filename)
			os.remove(filepath)
			return jsonify(success=True)
		except (ValueError, IndexError):
			return jsonify(err=True, message="Invalid image index.")
		except Exception as e:
			return jsonify(error=True, message=str(e))
	else:
		return jsonify(error=True, message="Image index not provided.")

@app.route("/images", methods=["GET", "POST"])
def read_images():
	if request.method == "POST":
		f = request.files['userImage']
		f.save("/home/pi/static/images/%s" % f.filename)
	images = []
	for (dirpath, dirnames, filenames) in walk("/home/pi/static/images"):
		images.extend(filenames)
		break
	return render_template("images.html", images=images)

# this is an API route
# NOT a page, like above, which uses render_template()
# does NOT use base.html
# returns json instead with jsonify(DATA)
# it gets called by page using JavaScript
# not sure if this True/False actually does anything?
# should return {error: true} or {error:false}
# and then only remove quote from ui when true
@app.route("/quotes/<line>", methods=["POST"])
def delete_quote(line=None):
	if line is not None:
		cmd = "sed -i '" + line + "d' " + quotes_file
		# should use subprocess instead?
		os.system(cmd)
		return jsonify(error=False)
	return jsonify(error=True)

# multiple actions on one route (GET, POST)
# sometimes you want them separate but these show the same data
@app.route("/quotes", methods=["GET", "POST"])
def read_quotes():
	# echoing in the new quote only happens on a post
	if request.method == "POST":
		os.system("echo \"" + request.form["quote"]  + "\" >> " + quotes_file)

	# reading the file happens with every request
	# so on a POST the file is edited and then read
	# keeps code simple and data fresh
	quotes = []
	with open(quotes_file, "r") as file:
		for line in file.readlines():
			quotes.append(line.rstrip())
	return render_template("quotes.html", quotes=quotes)

@app.route("/lyrics/del/<lyric>", methods=["POST"])
def delete_lyrics(lyric=None):
	if lyric is not None:
		try:
			lyric = int(lyric) - 1
			lyrics = os.listdir("/home/pi/static/lyrics")
			filename = lyrics[lyric]
			filepath = os.path.join("/home/pi/static/lyrics", filename)
			os.remove(filepath)
			return jsonify(success=True)
		except (ValueError, IndexError):
			return jsonify(err=True, message="Invalid lyric index.")
		except Exception as e:
			return jsonify(error=True, message=str(e))
	else:
		return jsonify(error=True, message="Lyric index not provided.")

@app.route("/lyrics/dsp/<lyric>", methods=["GET"])
def get_lyrics(lyric=None):
	if lyric != None:
		#lyric = int(lyric)-1
		lyrics = []
		for (dirpath, dirnames, filenames) in walk("/home/pi/static/lyrics"):
			lyrics.extend(filenames)
		print(lyric)
		for each in lyrics:
			if lyric == each:
				with open('/home/pi/static/lyrics/%s' % lyric, 'r') as f:
					text = f.read()
					return render_template("lyric_template.html", lyricText=text, lyricTitle=lyric)
				return jsonify(error=False)
	return jsonify(error=True)

# echoing in the new quote only happens on a post
#if request.method == "POST":
#os.system(lyric_file)
# reading the file happens with every request
# so on a POST the file is edited and then read
# keeps code simple and data fresh

@app.route("/lyrics", methods=["GET", "POST"])
def read_lyrics():
	if request.method == "POST":
		artist = request.form['lyricArtist']
		title = request.form['lyricTitle']
		text = request.form['lyricText']
		fname1 = artist.replace(" ", "")
		fname2 = title.replace(" ", "")
		fname = fname1 + "_" + fname2
		with open("/home/pi/static/lyrics/%s" % fname, 'w') as f:
			f.write(text)
	lyrics = []
	for (dirpath, dirnames, filenames) in walk("/home/pi/static/lyrics/"):
		lyrics.extend(filenames)
		break
	return render_template("lyrics.html", lyrics=lyrics)

# just a list for now
@app.route("/wifi", methods=["POST", "GET"])
def list_wifi():
	try:
		# b_networks is a list of binary strings
		# map applies the function to each element in the list
		# and returns a new list
		b_networks = subprocess.check_output("sudo iw dev wlan0 scan | grep SSID | grep -v \"List\" | cut -c8- | sed '/^$/d'", shell=True).splitlines()
		networks = map(lambda x: x.decode('UTF-8'), b_networks)
		return render_template("wifi.html", networks=networks)
	except:
		return "This is for first run wifi setup only. Edit /etc/dhcpcd.conf to return to wifi setup."

#Get SSID Clicked and password from user
@app.route("/ssid/<network>", methods=['GET', "POST"])
def ssid(network=None):
	if request.method == 'POST':
		password = request.form['password']
		#writes to wpa_supplicant the wifi information
		cmd1 = '''network={\n\tssid=\"%s\"\n\tpsk=\"%s\"\n}''' % (network,password)
		with open("/home/pi/wpa_supplicant.conf","a") as f:
			f.write(cmd1)
		#runs setup.py
		os.system("python3 /home/pi/setup-wifi.py")
		return "Please REBOOT using the power switch."
		#then files are set to update on reboot
		#editing dhcpcd.conf will set mode to ad-hoc setup
		#wifi information is set in /etc/wpa_supplicant/wpa_supplicant.conf
#	return render_template("ssid.html", network=network, password=password)
	return render_template("ssid.html", network=network)

