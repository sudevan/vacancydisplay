from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import random
import pandas as pd
from urllib.request import Request, urlopen
from django.shortcuts import render
from django.http import JsonResponse
import sys
def index(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
    else:
        request.session['counter'] += 1

    # Generate random data for demonstration
    data = {
        'number': random.randint(1, 100),
        'counter': request.session['counter']
    }

    return render(request, 'index.html', data)

import pandas as pd
from urllib.request import Request, urlopen
from django.shortcuts import render

def fetch_seat_data():
    try:
        url = 'http://admission.gptcpalakkad.ac.in/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = Request(url, headers=headers)
        response = urlopen(req)
        tables = pd.read_html(response)

        data = []
        for table in tables:
            collegename = table.iloc[2, 2]
            programs = table.iloc[3, 3:].to_list()
            quotacount = len(table) - 1

            branches = []
            for idx, program in enumerate(programs):
                branch_name = fulform(program)
                categories = []
                for i in range(4, quotacount + 1):
                    category_name = table.iloc[i, 2].upper()
                    availability = table.iloc[i, 3 + idx]
                    if pd.notna(availability):
                        categories.append({'name': category_name, 'availability': availability})
                branches.append({'name': branch_name, 'categories': categories})

            data.append({'college': collegename, 'branches': branches})

        return data

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return []

def home_view(request):
    data = fetch_seat_data()
    colleges = [{'name': college['college']} for college in data]
    return render(request, 'home.html', {'colleges': colleges})

def seat_availability_view(request):
    data = fetch_seat_data()

    current_index = request.session.get('current_college_index', 0)

    if current_index >= len(data):
        current_index = 0

    current_college_data = data[current_index]

    request.session['current_college_index'] = (current_index + 1) % len(data)

    return render(request, 'seat_availability.html', {
        'college': current_college_data['college'],
        'branches': current_college_data['branches']
    })

def college_view(request, college_name):
    data = fetch_seat_data()
    college_data = next((college for college in data if college['college'] == college_name), None)
    
    if college_data is None:
        return render(request, '404.html', {'message': 'College not found'})

    return render(request, 'college_seat_availability.html', {
        'college': college_data['college'],
        'branches': college_data['branches']
    })

def fulform(data):
    branch_dict = {
        "CM": "Computer Hardware Engineering",
        "EL": "Electronics Engineering",
        "ME": "Mechanical Engineering",
        "EE": "Electrical Electronics Engineering",
        "IE": "Instrumentation Engineering",
        "CE": "Civil Engineering",
        "CT": "Computer Engineering",
        "PT": "Printing Engineering",
        "AU": "Automobile Engineering",
        "AM": "Artificial Intelligence & Machine Learning"
    }
    return branch_dict.get(data, data)

def fetch_seat_data():
    data = []
    try:
        url = 'http://admission.gptcpalakkad.ac.in/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = Request(url, headers=headers)
        response = urlopen(req)
        tables = pd.read_html(response)
        
       
        for table in tables:
            collegename = table.iloc[2, 2]
            programs = table.iloc[3, 3:].to_list()
            quotacount = len(table) - 1
    
            branches = []
            for idx, program in enumerate(programs):
                branch_name = fulform(program)
                categories = []
                for i in range(4, quotacount + 1):
                    category_name = table.iloc[i, 2].upper()
                    availability = table.iloc[i, 3 + idx]
                    if pd.notna(availability):
                        categories.append({'name': category_name, 'availability': availability})
                branches.append({'name': branch_name, 'categories': categories})
    
            data.append({'college': collegename, 'branches': branches})
        
        return data
    except Exception as e:
         # Print exception information
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Exception Type: {exc_type.__name__}")
        print(f"Exception: {e}")
        print(f"Line Number: {exc_tb.tb_lineno}")
        return JsonResponse(data)

def seat_availability_view(request):
    # Fetch the data from the remote site
    data = fetch_seat_data()

    # Get the current college index from the session
    current_index = request.session.get('current_college_index', 0)

    # If the index is out of range, reset it to 0
    if current_index >= len(data):
        current_index = 0

    # Get the current college data
    current_college_data = data[current_index]

    # Update the session with the next index
    request.session['current_college_index'] = (current_index + 1) % 6

    return render(request, 'live.html', {
        'college': current_college_data['college'],
        'branches': current_college_data['branches']
    })

def fulform(data):
    branch_dict = {
        "CM": "Computer Hardware Engineering",
        "EL": "Electronics Engineering",
        "ME": "Mechanical Engineering",
        "EE": "Electrical Electronics Engineering",
        "IE": "Instrumentation Engineering",
        "CE": "Civil Engineering",
        "CT": "Computer Engineering",
        "PT": "Printing Engineering",
        "AU": "Automobile Engineering",
        "AM": "Artificial Intelligence & Machine Learning"
    }
    return branch_dict.get(data, data)
