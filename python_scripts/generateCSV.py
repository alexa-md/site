"""
    generateCSV.py

    Makes csv files in the correct format
    for Watson API.
"""


import pickle


savedData = open('pickle/saveData.pickle', 'rb')
data = pickle.load(savedData)
savedData.close()

savedSymptomData = open('pickle/saveSymptomData.pickle', 'rb')
symptoms = pickle.load(savedSymptomData)
savedSymptomData.close()


def filterIncompleteData():
    newData = []

    for entry in data:
        if len(entry['symptoms']) <= 1:
            continue

        entry['symptoms'] = list(filter(lambda x: len(x) > 2, entry['symptoms']))

        newData.append(entry)

    return newData


def filterSampleSet():
    fileHandle = open('csv/sample.csv', 'r')
    fileWrite = open('csv/data.csv', 'w')
    sampleSet = set()
    newData = []

    for line in fileHandle:
        line = line.strip('\n')

        sampleSet.add(line)

    for entry in filterIncompleteData():
        if entry['title'] not in sampleSet:
            continue
        newData.append(entry)

    return newData

def generate():
    file_handle = open('csv/dataFull.csv', 'w')
    symptomSet = set()

    for entry in filterIncompleteData():
        title = entry['title']
        symptoms = entry['symptoms']

        if not title or not symptoms or len(symptoms) < 2:
            continue

        for symptom in symptoms:
            if len(symptom) >= 1024:
                continue

            if symptom in symptomSet:
                continue

            symptomSet.add(symptom)
            symptom = symptom.replace('"', '').lstrip()
            file_handle.write('"' + symptom + '",' + title + '\n')


def generateSymptoms():
    file_handle = open('csv/symptoms.csv', 'w')

    for entry in symptoms:
            file_handle.write(entry + '\n')


def generateSample():
    file_handle = open('csv/data2.csv', 'w')
    symptomSet = set()

    for entry in filterSampleSet():
        title = entry['title']
        symptoms = entry['symptoms']

        if not title or not symptoms or len(symptoms) < 2:
            continue

        for symptom in symptoms:
            if len(symptom) >= 1024:
                continue

            if symptom in symptomSet:
                continue

            symptomSet.add(symptom)
            symptom = symptom.replace('"', '').lstrip()
            file_handle.write('"' + symptom + '",' + title + '\n')


generateSample()
