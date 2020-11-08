from flask import Flask
from flask_cors import CORS
from keras.models import load_model
from plant_health_monitoring.recommender import Recommender

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


recomender = Recommender('plant_health_monitoring/ml_models/plan_soil.csv')
recomender.load('plant_health_monitoring/ml_models/Plant_recommender.npz')
print(recomender.recomend(['apple','aloe vera'],5))

models = {
    'Apple': [load_model("plant_health_monitoring/ml_models/Apple_dieases.h5"), ["Apple scab", "Planting disease resistant varieties is the best way to manage scab. Fungicides can be used to manage apple scab. Proper timing of sprays is needed for fungicides to control disease."], ["Black rot", "Captan and sulfur products are labeled for control of both scab and black rot. A scab spray program including these chemicals may help prevent the frog-eye leaf spot of black rot, as well as the infection of fruit. "], ["Cedar apple rust","In that case, you should focus on purging infected leaves and fruit from around your tree. Spraying apple trees with copper can be done to treat cedar apple rust and prevent other fungal infections."], ["Healthy",""]],
    'Cherry': [load_model("plant_health_monitoring/ml_models/Cherry_dieases.h5"), ["Powder Mildew","The most important spray timing for powdery mildew control is the first cover timing, i.e., the first spray application after shuck split. Prior to shuck split, chlorothalonil (Bravo and other generics) is the fungicide of choice in tart cherry orchards due to its excellent activity in cherry leaf spot control."], ["Healthy",'']],
    'Corn': [load_model("plant_health_monitoring/ml_models/Corn_dieases.h5"), ["Cercospora Leaf Spot Gray Leaf Spot","There are some fungicides available to help manage Cercospora leaf spot. Products containing chlorothalonil, myclobutanil or thiophanate-methyl are most effective when applied prior to or at the first sign of leaf spots"], ["Common Rust","Immediately spray with a fungicide. The fungicide is most effective when started at the first sign of infection."], ["Northern Leaf Blight","Treating northern corn leaf blight involves using fungicides. For most home gardeners this step isn't needed, but if you have a bad infection, you may want to try this chemical treatment."], ["Healthy",""]],
    'Grape': [load_model("plant_health_monitoring/ml_models/Grape_dieases.h5"), ["Black rot","The best time to treat black rot of grapes is between bud break until about four weeks after bloom; treating outside of this window is likely to end in frustration. "],["Esca (Black Measles)","No Cure"],["Leaf blight (Isariopsis Leaf Spot)","Spraying of the grapevines at 3-4 leaf stage with fungicides like Bordeaux mixture @ 0.8% or Copper Oxychloride @ 0.25% or Carbendazim @ 0.1% are effective against this disease"],["Healthy",""]],
    'Peach': [load_model("plant_health_monitoring/ml_models/Peach_dieases.h5"),["Bacterial Spot","Compounds available for use on peach and nectarine for bacterial spot include copper, oxytetracycline (Mycoshield and generic equivalents), and syllit+captan; however, repeated applications are typically necessary for even minimal disease control"],["Healthy",""]],
    'Pepper Bell': [load_model("plant_health_monitoring/ml_models/Pepper_bell_dieases.h5"),["Bacterial Spot","Purchase disease-free seed and transplants. Treat seeds by soaking them for 2 minutes in a 10% chlorine bleach solution (1 part bleach; 9 parts water). Thoroughly rinse seeds and dry them before planting."],["Healthy",""]],
    'Potato': [load_model("plant_health_monitoring/ml_models/Potato_dieases.h5"),["Early Blight","Treatment of early blight includes prevention by planting potato varieties that are resistant to the disease; late maturing are more resistant than early maturing varieties. Avoid overhead irrigation and allow for sufficient aeration between plants to allow the foliage to dry as quickly as possible."],["Late Blight","The severe late blight can be effectively managed with prophylactic spray of mancozeb at 0.25% followed by cymoxanil+mancozeb or dimethomorph+mancozeb at 0.3% at the onset of disease and one more spray of mancozeb at 0.25% seven days after application of systemic fungicides."],["Healthy",""]],
    'Strawberry': [load_model("plant_health_monitoring/ml_models/Strawberry_dieases.h5"),["Leaf Scorch","Since this fungal pathogen over winters on the fallen leaves of infect plants, proper garden sanitation is key. This includes the removal of infected garden debris from the strawberry patch, as well as the frequent establishment of new strawberry"],["Healthy",""]],

}

from plant_health_monitoring import routes