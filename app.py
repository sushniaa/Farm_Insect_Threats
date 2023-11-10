from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
#from tensorflow.keras.preprocessing.image import load_img
from keras.preprocessing.image import load_img
import numpy as np
import os
from PIL import Image
from flask import Flask, send_from_directory, current_app

app = Flask(__name__)


app = Flask(__name__, static_folder='static')
app.add_url_rule('/static/<filename>', 'static', build_only=True)
upload_folder = os.path.join("static", "uploads")
os.makedirs(upload_folder, exist_ok=True)

@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicons/favicon.ico')

dic = {0:'Africanized Honey Bees', 1:'Aphids', 2:'Armyworms', 3:'Brown Marmorated Stink Bugs', 4:'Cabbage Loopers', 5:'Citrus Canker', 6:'Colorado Potato Beetles', 7:'Corn Borers', 8:'Corn Earworms', 9:'Fall Armyworms', 10:'Spider Mites', 11:'Fruit Flies', 12:'Tomato Hornworms', 13:'Western Corn Rootworms', 14:'Thrips'}
insecticides = {
    'Africanized Honey Bees': 'Contact local beekeepers or pest control experts for handling bee infestations',
    'Aphids': 'Neem oil, insecticidal soap',
    'Armyworms': 'Bacillus thuringiensis (Bt)',
    'Brown Marmorated Stink Bugs': 'Pyrethroids, neonicotinoids',
    'Cabbage Loopers': 'Bacillus thuringiensis (Bt)',
    'Citrus Canker': 'Copper-based sprays, antibiotics for citrus trees',
    'Colorado Potato Beetles': 'Insecticides with active ingredients like neonicotinoids',
    'Corn Borers': 'Bacillus thuringiensis (Bt), neonicotinoids',
    'Corn Earworms': 'Bacillus thuringiensis (Bt)',
    'Fall Armyworms': 'Bacillus thuringiensis (Bt)',
    'Fruit Flies': 'Fruit fly traps, pyrethroids',
    'Spider Mites': 'Miticides, neem oil',
    'Thrips': 'Neem oil, insecticidal soap',
    'Tomato Hornworms': 'Bacillus thuringiensis (Bt)',
    'Western Corn Rootworms': 'Seed treatment with neonicotinoids'
}
model = load_model('insect.h5')

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    return render_template("prediction.html")

def get_insecticides_label(class_name):
    if class_name == 'Africanized Honey Bees (Killer Bees)':
        return 'Contact local beekeepers or pest control experts for handling bee infestations'
    else:
        return insecticides.get(class_name, 'No information available for recommended insecticides')


@app.route("/submit", methods=['POST'])
def get_prediction():
    if request.method == 'POST':
        img = request.files['images']

        if img:
            img_path = os.path.join("static", "uploads", img.filename)
            #img = Image.open(img_path)
            #img = img.resize((300, 300))
            img.save(img_path)

            label = predict_label(img_path)
            insecticides_label = get_insecticides_label(label)

            response = {
                "image_path": img_path,
                "label": label,
                "insecticides_label": insecticides_label,
            }

            return jsonify(response)

def predict_label(img_path):
    # Load and preprocess the image, then use the model to make predictions
    i = image.load_img(img_path, target_size=(300, 300))
    i = image.img_to_array(i)
    i = np.expand_dims(i, axis=0)
    predict_x = model.predict(i)
    classes_x = np.argmax(predict_x, axis=1)
    label = dic[classes_x[0]]
    return label

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
