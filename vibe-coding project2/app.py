from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import requests
import json
from datetime import datetime, timedelta
import random
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Dummy user data (in a real app, this would be in a database)
users = {
    'demo_user': {
        'habits': {
            'exercise': [
                {'date': '2024-01-15', 'amount': 30, 'minutes': 30},
                {'date': '2024-01-16', 'amount': 45, 'minutes': 45},
                {'date': '2024-01-17', 'amount': 20, 'minutes': 20},
                {'date': '2024-01-18', 'amount': 35, 'minutes': 35},
                {'date': '2024-01-19', 'amount': 25, 'minutes': 25},
                {'date': '2024-01-20', 'amount': 40, 'minutes': 40},
                {'date': '2024-01-21', 'amount': 15, 'minutes': 15}
            ],
            'meditation': [
                {'date': '2024-01-15', 'amount': 10, 'minutes': 10},
                {'date': '2024-01-16', 'amount': 15, 'minutes': 15},
                {'date': '2024-01-17', 'amount': 5, 'minutes': 5},
                {'date': '2024-01-18', 'amount': 20, 'minutes': 20},
                {'date': '2024-01-19', 'amount': 10, 'minutes': 10},
                {'date': '2024-01-20', 'amount': 15, 'minutes': 15},
                {'date': '2024-01-21', 'amount': 8, 'minutes': 8}
            ],
            'water_intake': [
                {'date': '2024-01-15', 'amount': 6, 'minutes': None},
                {'date': '2024-01-16', 'amount': 8, 'minutes': None},
                {'date': '2024-01-17', 'amount': 5, 'minutes': None},
                {'date': '2024-01-18', 'amount': 7, 'minutes': None},
                {'date': '2024-01-19', 'amount': 9, 'minutes': None},
                {'date': '2024-01-20', 'amount': 6, 'minutes': None},
                {'date': '2024-01-21', 'amount': 4, 'minutes': None}
            ],
            'sleep_hours': [
                {'date': '2024-01-15', 'amount': 7.5, 'minutes': None},
                {'date': '2024-01-16', 'amount': 8, 'minutes': None},
                {'date': '2024-01-17', 'amount': 6.5, 'minutes': None},
                {'date': '2024-01-18', 'amount': 7, 'minutes': None},
                {'date': '2024-01-19', 'amount': 8.5, 'minutes': None},
                {'date': '2024-01-20', 'amount': 7, 'minutes': None},
                {'date': '2024-01-21', 'amount': 6, 'minutes': None}
            ]
        },
        'nutrition_logs': [
            {
                'date': '2024-01-15',
                'meals': [
                    {
                        'name': 'Oatmeal with berries',
                        'calories': 320,
                        'protein': 12,
                        'carbs': 55,
                        'fat': 8,
                        'fiber': 8,
                        'sugar': 15,
                        'time': '08:00',
                        'meal_type': 'breakfast'
                    },
                    {
                        'name': 'Grilled chicken salad',
                        'calories': 450,
                        'protein': 35,
                        'carbs': 25,
                        'fat': 22,
                        'fiber': 6,
                        'sugar': 8,
                        'time': '12:30',
                        'meal_type': 'lunch'
                    },
                    {
                        'name': 'Salmon with vegetables',
                        'calories': 580,
                        'protein': 42,
                        'carbs': 30,
                        'fat': 28,
                        'fiber': 8,
                        'sugar': 12,
                        'time': '19:00',
                        'meal_type': 'dinner'
                    }
                ]
            },
            {
                'date': '2024-01-16',
                'meals': [
                    {
                        'name': 'Greek yogurt with granola',
                        'calories': 280,
                        'protein': 18,
                        'carbs': 35,
                        'fat': 10,
                        'fiber': 4,
                        'sugar': 20,
                        'time': '07:30',
                        'meal_type': 'breakfast'
                    },
                    {
                        'name': 'Turkey sandwich',
                        'calories': 380,
                        'protein': 28,
                        'carbs': 40,
                        'fat': 15,
                        'fiber': 3,
                        'sugar': 5,
                        'time': '12:00',
                        'meal_type': 'lunch'
                    }
                ]
            }
        ],
        'mood_logs': [
            {'mood': '😊', 'notes': 'Had a great workout and felt energized all day!', 'date': '2024-01-15 08:30'},
            {'mood': '😐', 'notes': 'Regular day, nothing special but feeling okay', 'date': '2024-01-16 09:15'},
            {'mood': '😔', 'notes': 'Feeling a bit down today, maybe need more sleep', 'date': '2024-01-17 10:00'},
            {'mood': '😤', 'notes': 'Work is stressful, need to take a break', 'date': '2024-01-18 14:30'},
            {'mood': '😊', 'notes': 'Went for a walk and felt much better', 'date': '2024-01-19 16:45'},
            {'mood': '😴', 'notes': 'Tired but accomplished a lot today', 'date': '2024-01-20 20:00'},
            {'mood': '😊', 'notes': 'Spent time with family, feeling grateful', 'date': '2024-01-21 19:30'}
        ],
        'goals': {
            'daily_water': 8,
            'daily_exercise': 30,
            'daily_meditation': 15,
            'sleep_hours': 8,
            'daily_calories': 2000,
            'daily_protein': 150,
            'daily_carbs': 250,
            'daily_fat': 65
        }
    }
}

# API Keys (you'll need to get these from respective services)
WEATHER_API_KEY = "your_openweathermap_api_key"  # Get from openweathermap.org
QUOTES_API_URL = "https://api.quotable.io/random"
NUTRITION_API_URL = "https://api.edamam.com/api/nutrition-data"
NUTRITION_API_KEY = "your_edamam_api_key"  # Get from edamam.com
NUTRITION_APP_ID = "your_edamam_app_id"  # Get from edamam.com

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            session['user_id'] = 'demo_user'
        return f(*args, **kwargs)
    return decorated_function

def get_weather_data(city="New York"):
    """Get weather data from OpenWeatherMap API"""
    try:
        # For demo purposes, return dummy weather data
        weather_data = {
            'main': {'temp': 22, 'humidity': 65},
            'weather': [{'main': 'Clear', 'description': 'clear sky'}],
            'name': city
        }
        return weather_data
    except Exception as e:
        print(f"Weather API error: {e}")
        return None

def get_motivational_quote():
    """Get motivational quote from API"""
    try:
        response = requests.get(QUOTES_API_URL, params={'tags': 'motivation,health'})
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'content': 'Your health is an investment, not an expense.',
                'author': 'Anonymous'
            }
    except Exception as e:
        print(f"Quotes API error: {e}")
        return {
            'content': 'Every day is a new beginning. Take a deep breath and start again.',
            'author': 'Anonymous'
        }

def get_nutrition_data(food_item):
    """Get nutrition data from Edamam API"""
    try:
        if NUTRITION_API_KEY == "your_edamam_api_key" or NUTRITION_APP_ID == "your_edamam_app_id":
            # Return dummy data for demo
            return get_dummy_nutrition_data(food_item)
        
        url = f"{NUTRITION_API_URL}"
        params = {
            'app_id': NUTRITION_APP_ID,
            'app_key': NUTRITION_API_KEY,
            'ingr': food_item
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'calories': data.get('calories', 0),
                'protein': data.get('totalNutrients', {}).get('PROCNT', {}).get('quantity', 0),
                'carbs': data.get('totalNutrients', {}).get('CHOCDF', {}).get('quantity', 0),
                'fat': data.get('totalNutrients', {}).get('FAT', {}).get('quantity', 0),
                'fiber': data.get('totalNutrients', {}).get('FIBTG', {}).get('quantity', 0),
                'sugar': data.get('totalNutrients', {}).get('SUGAR', {}).get('quantity', 0)
            }
        else:
            return get_dummy_nutrition_data(food_item)
    except Exception as e:
        print(f"Nutrition API error: {e}")
        return get_dummy_nutrition_data(food_item)

def get_dummy_nutrition_data(food_item):
    """Get dummy nutrition data for demo purposes"""
    # Common food items with their nutritional values
    nutrition_db = {
        'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4, 'sugar': 19},
        'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'fiber': 3, 'sugar': 14},
        'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sugar': 0},
        'salmon': {'calories': 208, 'protein': 25, 'carbs': 0, 'fat': 12, 'fiber': 0, 'sugar': 0},
        'oatmeal': {'calories': 150, 'protein': 6, 'carbs': 27, 'fat': 3, 'fiber': 4, 'sugar': 1},
        'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4, 'sugar': 0.1},
        'broccoli': {'calories': 55, 'protein': 3.7, 'carbs': 11, 'fat': 0.6, 'fiber': 5, 'sugar': 2.6},
        'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'sugar': 0.4},
        'eggs': {'calories': 70, 'protein': 6, 'carbs': 0.6, 'fat': 5, 'fiber': 0, 'sugar': 0.4},
        'milk': {'calories': 103, 'protein': 8, 'carbs': 12, 'fat': 2.4, 'fiber': 0, 'sugar': 12},
        'bread': {'calories': 79, 'protein': 3.1, 'carbs': 15, 'fat': 1, 'fiber': 1.2, 'sugar': 1.3},
        'pasta': {'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'fiber': 1.8, 'sugar': 0.8},
        'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'sugar': 3.2},
        'cheese': {'calories': 113, 'protein': 7, 'carbs': 0.4, 'fat': 9, 'fiber': 0, 'sugar': 0.1},
        'nuts': {'calories': 607, 'protein': 20, 'carbs': 21, 'fat': 54, 'fiber': 7, 'sugar': 4.3}
    }
    
    # Try to find exact match or partial match
    food_lower = food_item.lower()
    for key, value in nutrition_db.items():
        if key in food_lower or food_lower in key:
            return value
    
    # Default values if no match found
    return {'calories': 100, 'protein': 5, 'carbs': 15, 'fat': 3, 'fiber': 2, 'sugar': 5}

def get_nutrition_tips(water_intake, exercise_minutes, calories_consumed=0, calories_goal=2000):
    """Get nutrition tips based on user's habits and nutrition data"""
    tips = []
    
    if water_intake < 6:
        tips.append("You're below your daily water goal. Try drinking a glass now!")
    
    if exercise_minutes < 20:
        tips.append("Consider a 10-minute walk to boost your daily activity.")
    
    if exercise_minutes > 45:
        tips.append("Great job on exercise! Remember to stay hydrated.")
    
    # Nutrition-specific tips
    if calories_consumed > 0:
        if calories_consumed < calories_goal * 0.7:
            tips.append("You're eating below your calorie goal. Consider adding a healthy snack!")
        elif calories_consumed > calories_goal * 1.3:
            tips.append("You're above your calorie goal. Try lighter meal options for dinner.")
    
    return tips

def get_personalized_suggestions(user_data, weather_data):
    """Generate personalized wellness suggestions"""
    suggestions = []
    
    # Weather-based suggestions
    if weather_data and weather_data.get('weather'):
        weather_main = weather_data['weather'][0]['main'].lower()
        temp = weather_data['main']['temp']
        
        if 'rain' in weather_main or 'snow' in weather_main:
            suggestions.append("It's raining - perfect for indoor yoga or meditation!")
        elif 'clear' in weather_main and temp > 20:
            suggestions.append("Beautiful weather! Great day for outdoor exercise.")
        elif temp < 10:
            suggestions.append("It's chilly - consider indoor workouts or warm-up exercises.")
    
    # Habit-based suggestions
    today = datetime.now().strftime('%Y-%m-%d')
    user_habits = user_data['habits']
    
    if not any(entry['date'] == today for entry in user_habits.get('water_intake', [])):
        suggestions.append("Don't forget to log your water intake today!")
    
    if not any(entry['date'] == today for entry in user_habits.get('exercise', [])):
        suggestions.append("Time for some physical activity - even 10 minutes helps!")
    
    if not any(entry['date'] == today for entry in user_habits.get('meditation', [])):
        suggestions.append("Take a moment to meditate and center yourself.")
    
    # Mood-based suggestions
    if user_data['mood_logs']:
        recent_moods = user_data['mood_logs'][-3:]  # Check last 3 mood entries
        negative_moods = ['😔', '😤', '😴']
        negative_count = sum(1 for mood_log in recent_moods if mood_log['mood'] in negative_moods)
        
        if negative_count >= 2:  # If 2 or more recent moods are negative
            suggestions.append("Feeling down? Try our mood-boosting mini-game!")
    
    return suggestions

@app.route('/')
@login_required
def dashboard():
    user_id = session['user_id']
    user_data = users[user_id]
    
    # Get external data
    weather_data = get_weather_data()
    quote = get_motivational_quote()
    suggestions = get_personalized_suggestions(user_data, weather_data)
    
    # Calculate today's progress
    today = datetime.now().strftime('%Y-%m-%d')
    today_water = sum(entry['amount'] for entry in user_data['habits']['water_intake'] 
                     if entry['date'] == today)
    today_exercise = sum(entry['minutes'] for entry in user_data['habits']['exercise'] 
                        if entry['date'] == today)
    today_meditation = sum(entry['minutes'] for entry in user_data['habits']['meditation'] 
                          if entry['date'] == today)
    
    # Calculate today's nutrition
    today_calories = 0
    today_protein = 0
    today_carbs = 0
    today_fat = 0
    
    for log in user_data.get('nutrition_logs', []):
        if log['date'] == today:
            for meal in log['meals']:
                today_calories += meal['calories']
                today_protein += meal['protein']
                today_carbs += meal['carbs']
                today_fat += meal['fat']
    
    # Get mood trend
    recent_moods = user_data['mood_logs'][-7:] if user_data['mood_logs'] else []
    
    return render_template('dashboard.html',
                         user_data=user_data,
                         weather_data=weather_data,
                         quote=quote,
                         suggestions=suggestions,
                         today_water=today_water,
                         today_exercise=today_exercise,
                         today_meditation=today_meditation,
                         today_calories=today_calories,
                         today_protein=today_protein,
                         today_carbs=today_carbs,
                         today_fat=today_fat,
                         recent_moods=recent_moods,
                         now=datetime.now())

@app.route('/habits')
@login_required
def habits():
    user_id = session['user_id']
    user_data = users[user_id]
    return render_template('habits.html', user_data=user_data, now=datetime.now())

@app.route('/log_habit', methods=['POST'])
@login_required
def log_habit():
    user_id = session['user_id']
    habit_type = request.form['habit_type']
    amount = float(request.form['amount'])
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if habit_type not in users[user_id]['habits']:
        return jsonify({'error': 'Invalid habit type'}), 400
    
    entry = {
        'date': date,
        'amount': amount,
        'minutes': amount if habit_type in ['exercise', 'meditation'] else None
    }
    
    users[user_id]['habits'][habit_type].append(entry)
    
    return jsonify({'success': True, 'message': f'{habit_type.title()} logged successfully!'})

@app.route('/tips')
@login_required
def tips():
    user_id = session['user_id']
    user_data = users[user_id]
    weather_data = get_weather_data()
    quote = get_motivational_quote()
    
    # Calculate nutrition tips
    today = datetime.now().strftime('%Y-%m-%d')
    today_water = sum(entry['amount'] for entry in user_data['habits']['water_intake'] 
                     if entry['date'] == today)
    today_exercise = sum(entry['minutes'] for entry in user_data['habits']['exercise'] 
                        if entry['date'] == today)
    
    # Calculate today's calories
    today_calories = 0
    for log in user_data.get('nutrition_logs', []):
        if log['date'] == today:
            for meal in log['meals']:
                today_calories += meal['calories']
    
    nutrition_tips = get_nutrition_tips(today_water, today_exercise, today_calories, user_data['goals']['daily_calories'])
    
    return render_template('tips.html',
                         user_data=user_data,
                         weather_data=weather_data,
                         quote=quote,
                         nutrition_tips=nutrition_tips,
                         now=datetime.now())

@app.route('/nutrition')
@login_required
def nutrition():
    user_id = session['user_id']
    user_data = users[user_id]
    
    # Calculate today's nutrition totals
    today = datetime.now().strftime('%Y-%m-%d')
    today_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0}
    
    for log in user_data.get('nutrition_logs', []):
        if log['date'] == today:
            for meal in log['meals']:
                today_nutrition['calories'] += meal['calories']
                today_nutrition['protein'] += meal['protein']
                today_nutrition['carbs'] += meal['carbs']
                today_nutrition['fat'] += meal['fat']
                today_nutrition['fiber'] += meal['fiber']
                today_nutrition['sugar'] += meal['sugar']
    
    return render_template('nutrition.html', 
                         user_data=user_data, 
                         today_nutrition=today_nutrition,
                         now=datetime.now())

@app.route('/log_nutrition', methods=['POST'])
@login_required
def log_nutrition():
    user_id = session['user_id']
    food_name = request.form['food_name']
    meal_type = request.form['meal_type']
    time = request.form.get('time', datetime.now().strftime('%H:%M'))
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Get nutrition data from API
    nutrition_data = get_nutrition_data(food_name)
    
    meal_entry = {
        'name': food_name,
        'calories': nutrition_data['calories'],
        'protein': nutrition_data['protein'],
        'carbs': nutrition_data['carbs'],
        'fat': nutrition_data['fat'],
        'fiber': nutrition_data['fiber'],
        'sugar': nutrition_data['sugar'],
        'time': time,
        'meal_type': meal_type
    }
    
    # Find or create today's nutrition log
    today_log = None
    for log in users[user_id].get('nutrition_logs', []):
        if log['date'] == date:
            today_log = log
            break
    
    if today_log is None:
        today_log = {'date': date, 'meals': []}
        if 'nutrition_logs' not in users[user_id]:
            users[user_id]['nutrition_logs'] = []
        users[user_id]['nutrition_logs'].append(today_log)
    
    today_log['meals'].append(meal_entry)
    
    return jsonify({
        'success': True, 
        'message': f'{food_name} logged successfully!',
        'nutrition_data': nutrition_data
    })

@app.route('/mood')
@login_required
def mood():
    user_id = session['user_id']
    user_data = users[user_id]
    return render_template('mood.html', user_data=user_data, now=datetime.now())

@app.route('/log_mood', methods=['POST'])
@login_required
def log_mood():
    user_id = session['user_id']
    mood = request.form['mood']
    notes = request.form.get('notes', '')
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    entry = {
        'mood': mood,
        'notes': notes,
        'date': date
    }
    
    users[user_id]['mood_logs'].append(entry)
    
    return jsonify({'success': True, 'message': 'Mood logged successfully!'})

@app.route('/api/chart_data')
@login_required
def chart_data():
    user_id = session['user_id']
    user_data = users[user_id]
    
    # Generate data for the last 7 days
    dates = []
    water_data = []
    exercise_data = []
    meditation_data = []
    
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dates.insert(0, date)
        
        # Calculate data for each habit
        water_amount = sum(entry['amount'] for entry in user_data['habits']['water_intake'] 
                          if entry['date'] == date)
        exercise_minutes = sum(entry['minutes'] for entry in user_data['habits']['exercise'] 
                              if entry['date'] == date)
        meditation_minutes = sum(entry['minutes'] for entry in user_data['habits']['meditation'] 
                                if entry['date'] == date)
        
        water_data.insert(0, water_amount)
        exercise_data.insert(0, exercise_minutes)
        meditation_data.insert(0, meditation_minutes)
    
    return jsonify({
        'dates': dates,
        'water': water_data,
        'exercise': exercise_data,
        'meditation': meditation_data
    })

@app.route('/api/mood_data')
@login_required
def mood_data():
    user_id = session['user_id']
    user_data = users[user_id]
    
    # Get mood data for the last 7 days
    mood_counts = {'😊': 0, '😐': 0, '😔': 0, '😤': 0, '😴': 0}
    
    for mood_log in user_data['mood_logs'][-7:]:
        mood = mood_log['mood']
        if mood in mood_counts:
            mood_counts[mood] += 1
    
    return jsonify(mood_counts)

@app.route('/api/nutrition_data')
@login_required
def nutrition_data():
    user_id = session['user_id']
    user_data = users[user_id]
    
    # Get nutrition data for the last 7 days
    dates = []
    calories_data = []
    protein_data = []
    carbs_data = []
    fat_data = []
    
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dates.insert(0, date)
        
        # Calculate daily totals
        daily_calories = 0
        daily_protein = 0
        daily_carbs = 0
        daily_fat = 0
        
        for log in user_data.get('nutrition_logs', []):
            if log['date'] == date:
                for meal in log['meals']:
                    daily_calories += meal['calories']
                    daily_protein += meal['protein']
                    daily_carbs += meal['carbs']
                    daily_fat += meal['fat']
        
        calories_data.insert(0, daily_calories)
        protein_data.insert(0, daily_protein)
        carbs_data.insert(0, daily_carbs)
        fat_data.insert(0, daily_fat)
    
    return jsonify({
        'dates': dates,
        'calories': calories_data,
        'protein': protein_data,
        'carbs': carbs_data,
        'fat': fat_data
    })

@app.route('/mood-game')
@login_required
def mood_game():
    user_id = session['user_id']
    user_data = users[user_id]
    return render_template('mood_game.html', user_data=user_data, now=datetime.now())

@app.route('/api/game-score', methods=['POST'])
@login_required
def save_game_score():
    user_id = session['user_id']
    score = request.json.get('score', 0)
    
    # In a real app, you'd save this to a database
    # For now, we'll just return a success message
    return jsonify({
        'success': True,
        'message': f'Great job! You scored {score} points!',
        'encouragement': get_encouragement_message(score)
    })

def get_encouragement_message(score):
    """Get encouraging message based on game score"""
    if score >= 100:
        return "Amazing! You're absolutely crushing it! 🌟"
    elif score >= 75:
        return "Fantastic work! You're doing great! 🎉"
    elif score >= 50:
        return "Good job! Every point counts! 👍"
    elif score >= 25:
        return "Nice effort! Keep going! 💪"
    else:
        return "You tried! That's what matters most! ❤️"

if __name__ == '__main__':
    app.run(debug=True)
