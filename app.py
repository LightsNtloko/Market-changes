#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Set the secrete key for the app
app.secrete_key = 'eb3b6ec9686b0fe3246532bfd854261b'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-data', methods=['POST'])
def submit_data():
    # Retrieve form data
    company_name = request.form.get('company_name')
    company_email = request.form.get('company_email')
    company_socials = request.form.get('company_socials')
    day_to_day_operations = request.form.get('day_to_day_operations')
    product_name = request.form.get('product_name')
    research_type = request.form.get('research_type')

    # Based on research type, get selected techniques
    primary_techniques = []
    secondary_techniques = []

    if research_type == "primary":
        primary_techniques = request.form.getlist('primary_techniques')
    elif research_type == "secondary":
        secondary_techniques = request.form.getlist('secondary_techniques')

    # Logging or further processing of form data
    print(f"Company Name: {company_name}")
    print(f"Company Email: {company_email}")
    print(f"Company Socials: {company_socials}")
    print(f"Day-to-Day Operations: {day_to_day_operations}")
    print(f"Product Name: {product_name}")
    print(f"Research Type: {research_type}")
    if primary_techniques:
        print(f"Primary Research Techniques: {primary_techniques}")
    if secondary_techniques:
        print(f"Secondary Research Techniques: {secondary_techniques}")

    # Saving the submitted data on Database
    with open('submitted_data.txt', 'a') as file:
        file.write(f"Company Name: {company_name}\n")
        file.write(f"Company Email: {company_email}\n")
        file.write(f"Company Socials: {company_socials}\n")
        file.write(f"Day-to-Day Operations: {day_to_day_operations}\n")
        file.write(f"Product Name: {product_name}\n")
        file.write(f"Research Type: {research_type}\n")
    
    if primary_techniques:
        file.write(f"Primary Research Techniques: {primary_techniques}\n")
    if secondary_techniques:
        file.write(f"Secondary Research Techniques: {secondary_techniques}\n")
    file.write("\n")

    # Flash a success message
    flash('Data submited successfully!')

    # Redirect or process the data as required
    return redirect(url_for('index'))

@app.route('/view-data')
def view_data():
    try:
        with open('submitted_data.txt', 'r') as file:
            data = file.read()
    except FileNotFoundError:
        data = 'No data found.'
    return render_template('view_data.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
