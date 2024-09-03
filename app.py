from flask import Flask, redirect, url_for, render_template, request, session
import spotify

app = Flask(__name__)

@app.route("/")
def render_home():

   return render_template('home.html')
   # songs = render_template('my-form.html')
   # return redirect(url_for('get_songs'))

@app.route('/input_song', methods = ["GET", "POST"])
def render_input_songs():
   if request.method == "POST":
      # getting input with name = fname in HTML form
      song = request.form.get("song")
      # getting input with name = lname in HTML form 
      artist = request.form.get("artist") 
      #number
      number = request.form.get("number")
      session['song'] = song
      session['artist'] = artist
      session['number'] = number
      return redirect(url_for('/get_songs'))
   return render_template('input_song.html')

@app.route("/get_songs", methods = ["GET", "POST"])
def get_songs():
   song = session.get('song')
   artist = session.get('artist')
   number = session.get('number')
   tracks = spotify.get_tracks(song, artist, number)
   tracks_info = [(sng['name'], sng['external_urls']['preview_url']) for sng in tracks['items']]
   tracks_html = '<br>'.join([f'{name:} {url}' for name, url in tracks_info])

   return tracks_html
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)