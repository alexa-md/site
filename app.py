""""
    Alexa MD

    Submitted to HackPrinceton 2017.

    Integrates IBM Watson API and Alexa API to
    provide diagnoses from a voice command input
    of their symptoms.
"""

from flask import Flask, render_template, request
from python_scripts import watson


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']

    print(query)

    # Input tags
    tags = query.split(',')
    inputTags = ''
    for t in tags:
        inputTags += '<span>' + t + '</span>'

    # Results
    results = watson.get_illness(query)

    resultDesc = ''
    animations = ''

    # Generates HTML text, needs to be converted to
    # Jinja later
    count = 0;
    for r in results:
        resultDesc += '<div class="result">' + r['class_name'] + ' <span>' + str(int(r['confidence'] * 100)) + '%</span>' + '<div id="progressbar'+ str(count) +'"><div></div></div></div>'
        animations += '#progressbar' + str(count) + ' { background-color: #545454; border-radius: 0px; padding: 1px; width: 400px; display: inline-block; float: right;}'
        animations += '#progressbar' + str(count) +' div{background-color: #6aaf6a;height: 10px;width:0%;border-radius: 0px;-webkit-animation:loadbar'+str(count)+' 2s;-webkit-animation-fill-mode: forwards;animation-fill-mode: forwards;}'
        animations += '@-webkit-keyframes loadbar'+str(count)+' {0% {width: 0%;}100% {width: '+str(int(r['confidence'] * 100))+'%;}}'
        animations += '@keyframes loadbar'+str(count)+' {0% {width: 0%;}100% {width: '+str(int(r['confidence'] * 100))+'%;}}'
        count += 1

    diagnosisName = results[0]['class_name'].title()
    diagnosisConfidence = str(int(results[0]['confidence'] * 100))

    return render_template('search.html',
                           inputTags=inputTags,
                           diagnosisName=diagnosisName,
                           diagnosisConfidence=diagnosisConfidence,
                           resultDesc=resultDesc,
                           animations=animations)


if __name__ == "__main__":
    app.run(debug=True)
