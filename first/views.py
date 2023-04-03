from django.shortcuts import render
import json
def create_file():
    with open('example.json', 'r') as f:
        data = json.loads(f.read())
        for i in data['employees']['employee']:
            if i['id'] == '3':
                print(i['photo'])

# Create your views here.
