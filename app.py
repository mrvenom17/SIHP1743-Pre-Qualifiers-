from flask import Flask, render_template, request, redirect
from SIHTOOL import investigate_profile  # Import your function here

app = Flask(__name__)

# Route to serve the index.html file
@app.route('./index.html')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/investigate', methods=['POST'])
def investigate():
    platform = request.form['platform']
    profile_url = request.form['profile_url']

    # Call your scraping function with the platform and profile URL
    investigate_profile(platform, profile_url)

    # After investigation, redirect back to the home page or a results page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
