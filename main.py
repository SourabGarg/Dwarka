from flask import Flask, render_template, request
import pymongo
import folium
from folium import plugins

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Temple"]
collection = db["Kangra"]

app = Flask(__name__)

data_list = list(collection.find())


def get_map(name):
    map_data = []
    for document in data_list:
        if name == document['Type'] or name == 'all':
            map_data.append({
                "name": document['Name'],
                "type": document['Type'],
                "coordinates": document['Coordinates'],
                "latitude": float(document['Coordinates'].split(",")[0]),
                "longitude": float(document['Coordinates'].split(",")[1]),
                "image": document['Images'],
                "about": document['About'],
                "who": document['Who'],
                "where": document['Where'],
                "history": document['History'],
                "facts": document['Facts']
            })
    m = folium.Map(location=[32.0824141, 76.4320124], zoom_start=11)
    minimap = plugins.MiniMap()
    m.add_child(minimap)

    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)

    for n in map_data:
        popup_data = f"<div class='popup' style='opacity: 0.8; position: relative; display: flex; flex-direction: column; align-items: center; text-align: center;'>"
        popup_data += f"<h3><b>{n['name']}</b></h3>"
        popup_data += f"<img src='static/{n['image']}/main.jpg' style='height: 200px; width: 100%; margin-top:10px; object-fit: cover; border-radius:5%;' alt='Image'>"
        popup_data += f"<form method='post' action='/detail' target='_blank'>"
        popup_data += f"<input type='hidden' name='value' value='{n['name']}'>"
        popup_data += f"<button type='submit' style='background-color:#0d6efd; border-radius:30px; color:white; border:0; margin: 10px; margin-top:20px; padding: 10px; font-size: 16px;'>Show More</button>"
        popup_data += "</form>"
        popup_data += "</div>"

        folium.Marker(
            location=[n['latitude'], n['longitude']],
            popup=folium.Popup(popup_data, max_width=300),
            icon=folium.Icon(color='blue')
        ).add_to(m)

    folium.LayerControl(position='bottomleft').add_to(m)

    m.save('templates/temple_map.html')

    return map_data


def get_one_data(value):
    data = []
    for document in data_list:
        if value == document['Name']:
            data.append({
                "name": document['Name'],
                "type": document['Type'],
                "coordinates": document['Coordinates'],
                "latitude": float(document['Coordinates'].split(",")[0]),
                "longitude": float(document['Coordinates'].split(",")[1]),
                "image": document['Images'],
                "about": document['About'],
                "who": document['Who'],
                "where": document['Where'],
                "history": document['History'],
                "facts": document['Facts']
            })
    return data


@app.route('/')
def get_home():
    return render_template('home.html')


@app.route('/about')
def get_about():
    return render_template('about.html')


@app.route('/map')
def use_map():
    return render_template('temple_map.html')


@app.route('/map_page', methods=['POST'])
def display_map():
    value = request.form.get('value')
    get_map(value)
    return render_template('map.html')


@app.route('/show_all')
def show_all():
    value = 'all'
    get_map(value)
    return render_template('map.html')


@app.route('/detail', methods=['POST'])
def process_data():
    value = request.form.get('value')
    temple_data = get_one_data(value)
    send_name = temple_data[0]['name'][:-7]
    return render_template('data.html', temple_data=temple_data, send_name=send_name)


if __name__ == '__main__':
    app.run(debug=True)
