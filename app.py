import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

load_dotenv(override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

print(f"DEBUG: GROQ_API_KEY loaded: {GROQ_API_KEY[:10] if GROQ_API_KEY else 'None'}...")
print("🔐 Loaded GROQ_API_KEY:", "Yes" if GROQ_API_KEY else "No")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return value
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat

llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a travel assistant. Generate a detailed {days}-day trip itinerary for {group_type} traveling to {city}, interested in {interests}, 
using {transport} as transportation, with a {budget} budget. 

IMPORTANT: Format your response EXACTLY as follows:

SUMMARY
[Brief overview of the trip]

DAILY ITINERARY
Day 1:
- Morning: [Activity] (Duration: X hours, Cost: ₹X)
- Afternoon: [Activity] (Duration: X hours, Cost: ₹X)
- Evening: [Activity] (Duration: X hours, Cost: ₹X)

Day 2:
[Same structure...]

FOOD RECOMMENDATIONS
1. [Dish Name]: [Description] (Type: [Food Type])
2. [Another Dish]

HIDDEN GEMS
1. [Place Name]: [Description] (Why Visit: [Reason])
2. [Another Place]

ESTIMATED COSTS
Total estimated cost: ₹XXX
Breakdown:
- Accommodation: ₹XXX
- Food: ₹XXX
- Activities: ₹XXX
- Transportation: ₹XXX""")
])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("index.html", active='home')

@app.route('/generate', methods=['GET', 'POST'])
def generate_trip():
    if request.method == 'POST':
        try:
            trip_data = {
                'city': request.form['city'],
                'days': int(request.form['days']),
                'interests': ", ".join([x.strip() for x in request.form['interests'].split(',')]),
                'transport': request.form['transport'],
                'budget': request.form['budget'],
                'group_type': request.form['group_type'],
                'photos': []
            }

            if 'photos' in request.files:
                for file in request.files.getlist('photos'):
                    if file and allowed_file(file.filename):
                        filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        trip_data['photos'].append(filename)

            print("⏳ Generating itinerary with LLM...")
            response = llm.invoke(itinerary_prompt.format_messages(**trip_data))
            print("✅ LLM Response Received")

            trip_data['itinerary'] = response.content
            trip_data['created_at'] = datetime.now().isoformat()
            session['current_trip'] = trip_data
            session.modified = True

            return render_template("result.html", trip=trip_data)

        except Exception as e:
            print(f"❌ Error generating itinerary: {e}")
            flash(f"Error generating itinerary: {str(e)}", "error")
            return redirect(url_for('generate_trip'))

    return render_template("generate.html", active='generate')

@app.route('/save', methods=['POST'])
def save_trip():
    if 'current_trip' not in session:
        flash('No trip to save', 'error')
        return redirect(url_for('generate_trip'))

    if 'saved_trips' not in session:
        session['saved_trips'] = []
    trip_data = session['current_trip'].copy()
    trip_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    session['saved_trips'].append(trip_data)
    session.modified = True
    flash('Trip saved successfully!', 'success')
    return redirect(url_for('my_trips'))

@app.route('/my-trips')
def my_trips():
    trips = session.get('saved_trips', [])
    return render_template("my_trips.html", trips=trips, active='trips')

@app.route('/edit-trip/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trips = session.get('saved_trips', [])
    if trip_id < 0 or trip_id >= len(trips):
        flash('Trip not found', 'error')
        return redirect(url_for('my_trips'))

    if request.method == 'POST':
        trips[trip_id] = {
            **trips[trip_id],
            'city': request.form['city'],
            'days': int(request.form['days']),
            'interests': [x.strip() for x in request.form['interests'].split(',')],
            'transport': request.form['transport'],
            'budget': request.form['budget'],
            'group_type': request.form['group_type'],
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        session['saved_trips'] = trips
        session.modified = True
        flash('Trip updated successfully!', 'success')
        return redirect(url_for('view_trip', trip_id=trip_id))

    return render_template("edit_trip.html", trip=trips[trip_id], trip_id=trip_id)

@app.route('/trip/<int:trip_id>')
def view_trip(trip_id):
    trips = session.get('saved_trips', [])
    if trip_id < 0 or trip_id >= len(trips):
        flash('Trip not found', 'error')
        return redirect(url_for('my_trips'))
    return render_template("trip_detail.html", trip=trips[trip_id], trip_id=trip_id)

@app.route('/delete-trip/<int:trip_id>')
def delete_trip(trip_id):
    trips = session.get('saved_trips', [])
    if trip_id < 0 or trip_id >= len(trips):
        flash('Trip not found', 'error')
    else:
        del trips[trip_id]
        session['saved_trips'] = trips
        session.modified = True
        flash('Trip deleted successfully', 'success')
    return redirect(url_for('my_trips'))

@app.route('/about')
def about():
    return render_template("about.html", active='about')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template("contact.html", active='contact')

if __name__ == '__main__':
    app.run(debug=True)
