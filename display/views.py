import pandas as pd
from django.shortcuts import render

def fetch_seat_data():
    try:
        url = 'http://admission.gptcpalakkad.ac.in/'
        tables = pd.read_html(url)

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
                
                if not categories:
                    categories.append({'name': 'N/A', 'availability': 'No seats available'})

                branches.append({'name': branch_name, 'categories': categories})

            data.append({'college': collegename, 'branches': branches})

        return data

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return []

def home_view(request):
    data = fetch_seat_data()
    colleges = [{'name': college['college']} for college in data]
    branches = {branch['name'] for college in data for branch in college['branches']}
    return render(request, 'home.html', {'colleges': colleges, 'branches': branches})

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

def branch_view(request, branch_name):
    data = fetch_seat_data()
    branch_data = [
        {
            'college': college['college'],
            'categories': next((branch['categories'] for branch in college['branches'] if branch['name'] == branch_name), [])
        }
        for college in data if any(branch['name'] == branch_name for branch in college['branches'])
    ]
    
    if not branch_data:
        return render(request, '404.html', {'message': 'Branch not found'})

    return render(request, 'branch_seat_availability.html', {
        'branch': branch_name,
        'colleges': branch_data
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
