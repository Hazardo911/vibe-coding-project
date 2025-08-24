# Smart Wellness Tracker

A comprehensive web application built with Python Flask that helps users track their daily wellness habits, mood, and provides personalized suggestions based on weather, nutrition, and user data.

## 🌟 Features

### Daily Habit Tracker
- **Exercise Tracking**: Log workout duration and type
- **Meditation**: Track mindfulness sessions
- **Water Intake**: Monitor daily hydration
- **Sleep Hours**: Record sleep patterns
- **Quick Logging**: One-click habit logging for common activities

### Progress Visualization
- **Interactive Charts**: Weekly progress tracking using Chart.js
- **Progress Bars**: Visual representation of daily goals
- **Streak Tracking**: Monitor consistency in habits
- **Trend Analysis**: View patterns over time

### Smart API Integrations
- **Quotes API**: Daily motivational quotes from quotable.io
- **Weather API**: Weather-based activity suggestions (OpenWeatherMap)
- **Nutrition Tips**: Personalized recommendations based on habits
- **Mood Tracking**: Emoji-based mood logging with insights

### Personalized Dashboard
- **Smart Suggestions**: Weather and habit-based recommendations
- **Daily Goals**: Track progress towards wellness targets
- **Recent Activity**: View latest habits and mood entries
- **Wellness Score**: Overall wellness assessment

### Responsive Design
- **Mobile-Friendly**: Works on all device sizes
- **Modern UI**: Beautiful gradient design with Bootstrap 5
- **Interactive Elements**: Hover effects and smooth animations
- **Accessible**: Easy navigation and clear visual hierarchy

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-wellness-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📱 Usage Guide

### Dashboard
- View daily progress towards wellness goals
- See personalized suggestions based on weather and habits
- Access quick actions for logging habits and mood
- View recent activity and motivational quotes

### Habits Page
- Log new habits with detailed forms
- Use quick-log buttons for common activities
- View habit history and progress
- Track daily goals with visual progress bars

### Tips Page
- Get personalized wellness suggestions
- View weather-based recommendations
- Access nutrition tips
- Participate in weekly wellness challenges

### Mood Tracker
- Log daily mood using emoji selection
- Add notes about your day
- View mood trends and insights
- Access mood-based wellness activities

## 🔧 Configuration

### API Keys (Optional)
For full functionality, you can add API keys in `app.py`:

```python
# Weather API (OpenWeatherMap)
WEATHER_API_KEY = "your_openweathermap_api_key"

# Get free API key from: https://openweathermap.org/api
```

### Customization
- Modify user goals in the `users` dictionary in `app.py`
- Add new habit types in the habits template
- Customize wellness suggestions in the tips functions
- Adjust the UI theme in `base.html`

## 🏗️ Project Structure

```
smart-wellness-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── dashboard.html    # Main dashboard page
    ├── habits.html       # Habit tracking page
    ├── tips.html         # Wellness tips page
    └── mood.html         # Mood tracking page
```

## 🎨 Features in Detail

### Smart Suggestions
The app provides personalized recommendations based on:
- **Weather Conditions**: Indoor/outdoor activity suggestions
- **Habit Patterns**: Reminders for missed daily activities
- **Mood Trends**: Wellness activities based on emotional state
- **Nutrition**: Hydration and exercise recommendations

### Data Visualization
- **Line Charts**: Weekly progress tracking
- **Doughnut Charts**: Mood distribution analysis
- **Progress Bars**: Goal completion visualization
- **Interactive Elements**: Hover effects and animations

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Clear menu structure
- **Real-time Updates**: Instant feedback on actions
- **Accessibility**: Keyboard navigation and screen reader support

## 🔮 Future Enhancements

- **Google Calendar Integration**: Sync wellness tasks
- **Social Features**: Share progress with friends
- **Advanced Analytics**: Detailed wellness insights
- **Mobile App**: Native iOS/Android applications
- **AI Recommendations**: Machine learning-based suggestions
- **Gamification**: Rewards and achievements system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Bootstrap**: For the responsive UI framework
- **Chart.js**: For beautiful data visualizations
- **Font Awesome**: For the icon library
- **Quotable.io**: For motivational quotes API
- **OpenWeatherMap**: For weather data API

## 📞 Support

If you have any questions or need help with the application, please:
- Check the documentation above
- Look for existing issues in the repository
- Create a new issue with detailed information

---

**Happy Wellness Tracking! 🌱✨**
