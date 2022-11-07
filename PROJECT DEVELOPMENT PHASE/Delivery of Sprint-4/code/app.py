
from flask import Flask,render_template,redirect, url_for,request
import requests

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
     if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("demo2"))
            arr.append(float(val))

        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "d2-3twnS_oRmh5yFAxs0aK7kpqJcN3_1qQy6IX3-P413"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
            })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr]
                            }]
                        }
        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/523f7b82-a7a0-4066-afab-c0f74dc8b976/predictions?version=2022-11-03',
            json=payload_scoring,
            headers=header
            ).json()
        result = response_scoring['predictions'][0]['values']
        if result[0][0] > 0.5:
            return redirect(url_for('chance', percent=result[0][0]*100))
        else:
            return redirect(url_for('no_chance', percent=result[0][0]*100)) 
     else:
        return redirect(url_for("demo2"))    

@app.route("/home")
def home():
    return render_template("demo2.html")
@app.route("/demo2")
def demo2():
    return render_template("demo2.html")
@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])
@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("demo2"))


if __name__=='__main__':
    app.run(debug=True)