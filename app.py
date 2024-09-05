from flask import Flask, redirect, url_for, render_template, request
import spotify
import bs4

app = Flask(__name__)
song = ""
artist = ""
number = 0  
@app.route("/")
def render_home():

   return render_template('home.html')
   # songs = render_template('my-form.html')
   # return redirect(url_for('get_songs'))

@app.route('/input_song', methods = ["GET", "POST"])
def render_input_songs():
   if request.method == "POST":
      song = request.form["song"]
      artist = request.form['artist']
      number = int(request.form['number'])
      model = request.form['model']

   
      tracks = spotify.get_tracks(song, artist, number, model)
      urls = []
      names = []
      ids = []


      for element in tracks:
         #print(element)
         #print (element.keys())
         #print(element.get('external_urls'))
         ids.append(element.get('id'))
         urls.append(element.get('external_urls'))
         


      #print(urls)
      # tracks_info = [(sng['name'], sng['external_urls']['preview_url']) for sng in tracks['items']]
      # print(tracks_info)
      urls = [d['spotify'] for d in urls ]


      with open("templates/input_song.html") as inf:
         txt = inf.read()
         soup = bs4.BeautifulSoup(txt, features='html.parser')


      content_block = soup.find(id="content")
      print("Found content block:", content_block)  # Debug: Check if the block is found
      content_block.clear()
      if content_block:
         for i in range(len(urls)):
            src1 = ("https://open.spotify.com/embed/track/" + ids[i])
            new_link = soup.new_tag("iframe", style="border-radius:12px",src=src1, width ="100%", height="352", frameBorder="0", allowfullscreen="", allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture", loading="lazy")
         
            content_block.append(new_link)
            content_block.append(soup.new_tag("br"))  # Adds a line break after each link


            print(soup)
         with open("templates/input_song.html", "w") as outf:
            outf.write(str(soup))


         print("Links added successfully!")
      else:
         print("Content block not found. No links were added.")
   else:
      with open("templates/input_song.html") as inf:
         txt = inf.read()
         soup = bs4.BeautifulSoup(txt, features='html.parser')
      content_block = soup.find(id="content")
      print("Found content block:", content_block)  # Debug: Check if the block is found
      content_block.clear()
     
   return render_template('input_song.html')


@app.route("/display_songs")
def display_songs():
   print("test4")
   # song = session['song']
   # artist = session['artist']
   # number = session['number']
   song = request.args["song"]
   artist = request.args['artist']
   number = int(request.args['number'])
   model = request.args['model']

   
   tracks = spotify.get_tracks(song, artist, number, model)
   urls = []
   names = []
   ids = []

   for element in tracks:
      #print(element)
      #print (element.keys())
      #print(element.get('external_urls'))
      ids.append(element.get('id'))
      urls.append(element.get('external_urls'))
      

   #print(urls)
   # tracks_info = [(sng['name'], sng['external_urls']['preview_url']) for sng in tracks['items']]
   # print(tracks_info)
   urls = [d['spotify'] for d in urls ]

   with open("templates/display_songs.html") as inf:
      txt = inf.read()
      soup = bs4.BeautifulSoup(txt, features='html.parser')

   content_block = soup.find(id="content")
   print("Found content block:", content_block)  # Debug: Check if the block is found
   content_block.clear()
   if content_block:
      for i in range(len(urls)):
        src1 = ("https://open.spotify.com/embed/track/" + ids[i])
        new_link = soup.new_tag("iframe", style="border-radius:12px",src=src1, width ="100%", height="352", frameBorder="0", allowfullscreen="", allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture", loading="lazy")
   
        content_block.append(new_link)
        content_block.append(soup.new_tag("br"))  # Adds a line break after each link

      print(soup)
      with open("templates/display_songs.html", "w") as outf:
        outf.write(str(soup))

      print("Links added successfully!")
   else:
      print("Content block not found. No links were added.")
   return render_template('display_songs.html')
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
