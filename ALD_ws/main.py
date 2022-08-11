
import logging

from flask import Flask, jsonify, request
import os

import torch
from predict import Predictor, profanityDetectionClassifier

model_path='./best_model_state.bin'

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.debug = True

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = profanityDetectionClassifier()
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model = model.to(device)

predictor = Predictor(model)


"""
predictor.predict('senin beynini kuşlara taksak kuşlar geri geri uçar')
"""

@app.route('/profanity_check', methods=['POST'])
def profanity_check():
    text = request.json.get("text")
    access_key=request.json.get("key")
    if access_key=="2167476":
    	app.logger.error("Text %s", str(text))
    	predicted = predictor.predict(text)
        # result = {category: int(prob) for category, prob in  predicted.items()}
    	return jsonify(result)
    return jsonify("You are anauthorized!")

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

port = os.getenv('PORT', '80')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))

