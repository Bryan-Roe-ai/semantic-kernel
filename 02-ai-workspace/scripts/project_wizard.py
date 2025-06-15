#!/usr/bin/env python3
"""
🧙‍♂️ Project Wizard - Create AI projects with magical ease!
Interactive project creation with templates and guidance.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

class ProjectWizard:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.projects_dir = Path("~/ai-projects").expanduser()
        self.projects_dir.mkdir(exist_ok=True)
    
    def print_welcome(self):
        """Print magical welcome message."""
        print("\n" + "🌟" * 25)
        print("🧙‍♂️ Welcome to the AI Project Wizard!")
        print("   Let's create something amazing together...")
        print("🌟" * 25)
        time.sleep(1)
    
    def show_project_types(self):
        """Show available project types."""
        projects = {
            "1": {
                "name": "🤖 Smart Chatbot",
                "description": "Conversational AI that can chat about any topic",
                "difficulty": "Beginner",
                "time": "30 minutes",
                "tech": "Python, Natural Language Processing"
            },
            "2": {
                "name": "📸 Image Classifier", 
                "description": "AI that can identify objects in photos",
                "difficulty": "Intermediate",
                "time": "1 hour",
                "tech": "Python, Computer Vision, TensorFlow"
            },
            "3": {
                "name": "📊 Prediction Engine",
                "description": "Predict future values from historical data",
                "difficulty": "Beginner",
                "time": "45 minutes", 
                "tech": "Python, Machine Learning, Pandas"
            },
            "4": {
                "name": "🎵 Music Recommendation System",
                "description": "Suggest music based on listening habits",
                "difficulty": "Intermediate",
                "time": "1.5 hours",
                "tech": "Python, Collaborative Filtering"
            },
            "5": {
                "name": "🌐 Web Scraper + AI Analyzer",
                "description": "Scrape websites and analyze content with AI",
                "difficulty": "Intermediate",
                "time": "1 hour",
                "tech": "Python, Web Scraping, NLP"
            },
            "6": {
                "name": "🎮 Game AI Agent",
                "description": "AI that learns to play games",
                "difficulty": "Advanced",
                "time": "2+ hours",
                "tech": "Python, Reinforcement Learning"
            },
            "7": {
                "name": "⚛️ Quantum-Enhanced Optimizer",
                "description": "Use quantum computing for optimization",
                "difficulty": "Advanced", 
                "time": "2+ hours",
                "tech": "Python, Qiskit, Quantum Computing"
            },
            "8": {
                "name": "🐝 Swarm Intelligence Solver",
                "description": "Multiple AI agents solving problems together",
                "difficulty": "Advanced",
                "time": "2+ hours", 
                "tech": "Python, Multi-Agent Systems"
            }
        }
        
        print("\n🎯 Choose Your AI Project Adventure:")
        print("-" * 50)
        
        for key, project in projects.items():
            print(f"\n{key}. {project['name']}")
            print(f"   📝 {project['description']}")
            print(f"   🎯 Difficulty: {project['difficulty']}")
            print(f"   ⏱️ Time: {project['time']}")
            print(f"   🛠️ Tech: {project['tech']}")
        
        return projects
    
    def get_project_details(self):
        """Get project details from user."""
        print("\n" + "💫" * 20)
        print("✨ Project Configuration Wizard")
        print("💫" * 20)
        
        details = {}
        
        # Project name
        while True:
            name = input("\n🏷️ What should we call your project? ").strip()
            if name:
                details['name'] = name.lower().replace(' ', '-')
                details['display_name'] = name
                break
            print("❌ Please enter a project name!")
        
        # Description
        description = input("\n📝 Brief description (optional): ").strip()
        details['description'] = description or f"An amazing AI project called {details['display_name']}"
        
        # Author
        author = input("\n👤 Your name (optional): ").strip()
        details['author'] = author or "AI Developer"
        
        return details
    
    def create_chatbot_project(self, details):
        """Create a smart chatbot project."""
        project_path = self.projects_dir / details['name']
        project_path.mkdir(exist_ok=True)
        
        # Main chatbot code
        main_code = f'''#!/usr/bin/env python3
"""
🤖 {details['display_name']} - Smart Chatbot
{details['description']}

Created by: {details['author']}
Created on: {datetime.now().strftime("%Y-%m-%d")}
"""

import re
import random
from datetime import datetime

class SmartChatbot:
    def __init__(self, name="{details['display_name']}"):
        self.name = name
        self.conversation_history = []
        self.user_preferences = {{}}
        
        # Response patterns
        self.patterns = [
            (r"hi|hello|hey", self.greet),
            (r"how are you", self.status_check),
            (r"what.*your.*name", self.introduce),
            (r"help|assist", self.offer_help),
            (r"time|date", self.tell_time),
            (r"joke|funny", self.tell_joke),
            (r"bye|goodbye|exit", self.say_goodbye),
            (r".*", self.default_response)
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer a joke about UDP... but I'm not sure if it got it.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem."
        ]
    
    def greet(self, message):
        greetings = [
            f"Hello! I'm {{self.name}}, your AI assistant! 🤖",
            f"Hi there! {{self.name}} here, ready to chat! ✨",
            f"Hey! Great to meet you! I'm {{self.name}} 👋"
        ]
        return random.choice(greetings)
    
    def status_check(self, message):
        responses = [
            "I'm doing great! My circuits are buzzing with excitement! ⚡",
            "Fantastic! I'm learning something new every second! 🧠",
            "Wonderful! Ready to help you with anything! 🚀"
        ]
        return random.choice(responses)
    
    def introduce(self, message):
        return f"I'm {{self.name}}, an AI chatbot created to help and chat with you! I can answer questions, tell jokes, and have conversations. What would you like to talk about? 🤖✨"
    
    def offer_help(self, message):
        return "I'm here to help! I can:\\n• Answer questions\\n• Tell jokes\\n• Chat about various topics\\n• Help with basic tasks\\n• Provide information\\n\\nWhat do you need help with? 💡"
    
    def tell_time(self, message):
        now = datetime.now()
        return f"It's {{now.strftime('%I:%M %p')}} on {{now.strftime('%A, %B %d, %Y')}} 🕐"
    
    def tell_joke(self, message):
        return f"Here's a joke for you:\\n\\n{{random.choice(self.jokes)}} 😄"
    
    def say_goodbye(self, message):
        farewells = [
            "Goodbye! It was great chatting with you! 👋",
            "See you later! Thanks for the conversation! ✨",
            "Bye! Come back anytime for more chat! 🌟"
        ]
        return random.choice(farewells)
    
    def default_response(self, message):
        responses = [
            "That's interesting! Tell me more about that. 🤔",
            "I see! Can you elaborate on that? 💭", 
            "Fascinating! I'd love to learn more. 📚",
            "Cool! What else would you like to discuss? 💫",
            "That's a great point! What are your thoughts on that? 🎯"
        ]
        return random.choice(responses)
    
    def chat(self, user_message):
        """Process user message and return response."""
        user_message = user_message.lower().strip()
        self.conversation_history.append(("user", user_message))
        
        # Find matching pattern
        for pattern, handler in self.patterns:
            if re.search(pattern, user_message):
                response = handler(user_message)
                self.conversation_history.append(("bot", response))
                return response
        
        # Should never reach here due to catch-all pattern
        return self.default_response(user_message)

def main():
    """Main chat loop."""
    print("🤖 Welcome to {details['display_name']}!")
    print("💬 Start chatting! (Type 'exit' to quit)")
    print("-" * 40)
    
    bot = SmartChatbot()
    
    while True:
        try:
            user_input = input("\\n👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"\\n🤖 {{bot.name}}: {{bot.say_goodbye(user_input)}}")
                break
            
            response = bot.chat(user_input)
            print(f"\\n🤖 {{bot.name}}: {{response}}")
            
        except KeyboardInterrupt:
            print(f"\\n\\n🤖 {{bot.name}}: Thanks for chatting! Goodbye! 👋")
            break
        except Exception as e:
            print(f"\\n❌ Error: {{e}}")
            print("Let's keep chatting! 💪")

if __name__ == "__main__":
    main()
'''
        
        with open(project_path / "main.py", 'w') as f:
            f.write(main_code)
        
        # Create README
        readme_content = f'''# 🤖 {details['display_name']}

{details['description']}

## 🚀 Quick Start

```bash
python main.py
```

## 🎯 Features

- 💬 Natural conversation
- 🕐 Time and date information
- 😄 Jokes and entertainment
- 🤖 Friendly AI personality
- 📚 Learning capabilities

## 🛠️ How to Enhance

1. **Add more patterns**: Edit the `patterns` list in `SmartChatbot`
2. **Improve responses**: Enhance the response methods
3. **Add memory**: Store user preferences and context
4. **Connect APIs**: Add weather, news, or other data sources
5. **Train on data**: Use machine learning for better responses

## 💡 Ideas for Expansion

- Web interface using Flask
- Voice recognition and speech
- Integration with external APIs
- Personality customization
- Multi-language support

Created by: {details['author']}
Created on: {datetime.now().strftime("%Y-%m-%d")}
'''
        
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)
        
        # Create requirements.txt
        requirements = '''# Basic requirements for the chatbot
# Add more packages as you enhance your bot

# For advanced NLP (optional):
# nltk>=3.8
# spacy>=3.5
# transformers>=4.20

# For web interface (optional):
# flask>=2.3
# requests>=2.28

# For voice capabilities (optional):
# speech_recognition>=3.10
# pyttsx3>=2.90
'''
        
        with open(project_path / "requirements.txt", 'w') as f:
            f.write(requirements)
        
        return project_path
    
    def create_image_classifier_project(self, details):
        """Create an image classifier project."""
        project_path = self.projects_dir / details['name']
        project_path.mkdir(exist_ok=True)
        
        # Main classifier code
        main_code = f'''#!/usr/bin/env python3
"""
📸 {details['display_name']} - Image Classifier
{details['description']}

Created by: {details['author']}
Created on: {datetime.now().strftime("%Y-%m-%d")}
"""

import os
import sys
from pathlib import Path

try:
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
    from tensorflow.keras.preprocessing import image
    import numpy as np
    from PIL import Image
except ImportError:
    print("❌ Required packages not installed!")
    print("📦 Install them with: pip install tensorflow pillow numpy")
    sys.exit(1)

class ImageClassifier:
    def __init__(self):
        print("🔄 Loading AI model... (this may take a moment)")
        self.model = MobileNetV2(weights='imagenet')
        print("✅ Model loaded successfully!")
    
    def classify_image(self, image_path):
        """Classify an image and return predictions."""
        try:
            # Load and preprocess image
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            # Make prediction
            predictions = self.model.predict(img_array)
            decoded_predictions = decode_predictions(predictions, top=5)[0]
            
            return decoded_predictions
            
        except Exception as e:
            print(f"❌ Error processing image: {{e}}")
            return None
    
    def classify_from_path(self, image_path):
        """Classify image and display results."""
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {{image_path}}")
            return
        
        print(f"\\n🔍 Analyzing: {{Path(image_path).name}}")
        print("-" * 40)
        
        predictions = self.classify_image(image_path)
        
        if predictions:
            print("🎯 Top 5 Predictions:")
            for i, (class_id, class_name, confidence) in enumerate(predictions, 1):
                confidence_percent = confidence * 100
                print(f"   {{i}}. {{class_name.title()}} - {{confidence_percent:.1f}}% confident")
        else:
            print("❌ Could not classify this image")

def main():
    """Main application."""
    print("📸 Welcome to {details['display_name']}!")
    print("🤖 AI-powered image classification")
    print("=" * 50)
    
    # Initialize classifier
    classifier = ImageClassifier()
    
    while True:
        print("\\n🎯 What would you like to do?")
        print("1. 📁 Classify an image file")
        print("2. 📂 Classify all images in a folder")  
        print("3. ❓ Help")
        print("4. 👋 Exit")
        
        choice = input("\\n🤔 Your choice (1-4): ").strip()
        
        if choice == "1":
            image_path = input("\\n📁 Enter image path: ").strip()
            classifier.classify_from_path(image_path)
            
        elif choice == "2":
            folder_path = input("\\n📂 Enter folder path: ").strip()
            if os.path.exists(folder_path):
                image_extensions = {{'.jpg', '.jpeg', '.png', '.bmp', '.gif'}}
                image_files = [f for f in os.listdir(folder_path) 
                             if Path(f).suffix.lower() in image_extensions]
                
                if image_files:
                    print(f"\\n🔍 Found {{len(image_files)}} images to classify...")
                    for img_file in image_files[:5]:  # Limit to 5 for demo
                        img_path = os.path.join(folder_path, img_file)
                        classifier.classify_from_path(img_path)
                        print()
                else:
                    print("❌ No image files found in this folder")
            else:
                print("❌ Folder not found")
                
        elif choice == "3":
            print("\\n💡 Help:")
            print("• This AI can identify 1000+ different objects")
            print("• Supported formats: JPG, PNG, BMP, GIF")
            print("• For best results, use clear, well-lit photos")
            print("• The AI shows its top 5 guesses with confidence levels")
            
        elif choice == "4":
            print("\\n👋 Thanks for using the image classifier!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
'''
        
        with open(project_path / "main.py", 'w') as f:
            f.write(main_code)
        
        # Create example images directory
        examples_dir = project_path / "example_images"
        examples_dir.mkdir(exist_ok=True)
        
        # Create README
        readme_content = f'''# 📸 {details['display_name']}

{details['description']}

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the classifier:**
   ```bash
   python main.py
   ```

3. **Add some images to classify:**
   - Put images in the `example_images/` folder
   - Or point to images anywhere on your computer

## 🎯 Features

- 🤖 Identifies 1000+ different objects
- 📊 Shows confidence levels for predictions
- 📁 Can process single images or entire folders
- 🖼️ Supports JPG, PNG, BMP, GIF formats
- ⚡ Uses state-of-the-art MobileNetV2 model

## 🛠️ How to Enhance

1. **Train on custom data**: Replace MobileNetV2 with your own model
2. **Add web interface**: Use Flask to create a web app
3. **Real-time camera**: Add webcam support for live classification
4. **Batch processing**: Add support for processing hundreds of images
5. **Custom categories**: Train the model on your specific objects

## 💡 Project Ideas

- Security camera object detection
- Medical image analysis
- Quality control for manufacturing
- Wildlife monitoring system
- Art style classification

## 📦 Requirements

- Python 3.7+
- TensorFlow 2.x
- PIL (Pillow)
- NumPy

Created by: {details['author']}
Created on: {datetime.now().strftime("%Y-%m-%d")}
'''
        
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)
        
        # Create requirements.txt
        requirements = '''tensorflow>=2.10.0
Pillow>=9.0.0
numpy>=1.21.0

# Optional enhancements:
# opencv-python>=4.6.0  # For advanced image processing
# matplotlib>=3.5.0     # For visualization
# flask>=2.3.0          # For web interface
'''
        
        with open(project_path / "requirements.txt", 'w') as f:
            f.write(requirements)
        
        return project_path
    
    def create_prediction_engine_project(self, details):
        """Create a prediction engine project."""
        project_path = self.projects_dir / details['name']
        project_path.mkdir(exist_ok=True)
        
        # Main prediction code
        main_code = f'''#!/usr/bin/env python3
"""
📊 {details['display_name']} - Prediction Engine
{details['description']}

Created by: {details['author']}
Created on: {datetime.now().strftime("%Y-%m-%d")}
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

class PredictionEngine:
    def __init__(self):
        self.model = None
        self.data = None
        self.feature_columns = []
        self.target_column = None
        
    def load_sample_data(self):
        """Generate sample sales data for demonstration."""
        print("📊 Generating sample sales data...")
        
        # Create sample data
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        np.random.seed(42)  # For reproducible results
        
        data = []
        base_sales = 1000
        for i, date in enumerate(dates):
            # Simulate realistic sales patterns
            trend = i * 2  # Growing trend
            seasonal = 200 * np.sin(2 * np.pi * i / 365)  # Yearly pattern
            weekly = 100 * np.sin(2 * np.pi * i / 7)      # Weekly pattern
            noise = np.random.normal(0, 50)               # Random variation
            
            marketing_spend = 200 + np.random.normal(0, 50)
            temperature = 70 + 20 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 5)
            
            sales = base_sales + trend + seasonal + weekly + noise + 0.5 * marketing_spend
            sales = max(sales, 0)  # No negative sales
            
            data.append({{
                'date': date,
                'sales': sales,
                'marketing_spend': marketing_spend,
                'temperature': temperature,
                'day_of_week': date.weekday(),
                'month': date.month
            }})
        
        self.data = pd.DataFrame(data)
        print(f"✅ Created {{len(self.data)}} days of sample data")
        return self.data
    
    def load_csv_data(self, file_path):
        """Load data from CSV file."""
        try:
            self.data = pd.read_csv(file_path)
            print(f"✅ Loaded {{len(self.data)}} rows from {{file_path}}")
            return self.data
        except Exception as e:
            print(f"❌ Error loading data: {{e}}")
            return None
    
    def explore_data(self):
        """Explore the dataset."""
        if self.data is None:
            print("❌ No data loaded!")
            return
            
        print("\\n🔍 Data Exploration:")
        print("-" * 30)
        print(f"📊 Dataset shape: {{self.data.shape}}")
        print(f"📋 Columns: {{list(self.data.columns)}}")
        
        print("\\n📈 Statistical Summary:")
        print(self.data.describe())
        
        print("\\n🔍 Sample rows:")
        print(self.data.head())
    
    def prepare_features(self, target_column, feature_columns=None):
        """Prepare features for training."""
        if self.data is None:
            print("❌ No data loaded!")
            return False
            
        self.target_column = target_column
        
        if feature_columns is None:
            # Auto-select numeric columns (except target)
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            self.feature_columns = [col for col in numeric_columns if col != target_column]
        else:
            self.feature_columns = feature_columns
        
        print(f"🎯 Target: {{self.target_column}}")
        print(f"🔧 Features: {{self.feature_columns}}")
        return True
    
    def train_model(self):
        """Train the prediction model."""
        if not self.feature_columns or not self.target_column:
            print("❌ Features not prepared! Call prepare_features() first.")
            return False
        
        # Prepare data
        X = self.data[self.feature_columns]
        y = self.data[self.target_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        print("🏋️ Training prediction model...")
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✅ Model trained successfully!")
        print(f"📊 R² Score: {{r2:.3f}} ({{r2*100:.1f}}% of variance explained)")
        print(f"📏 Mean Squared Error: {{mse:.2f}}")
        
        return True
    
    def make_predictions(self, input_data=None):
        """Make predictions with the trained model."""
        if self.model is None:
            print("❌ No trained model! Call train_model() first.")
            return None
        
        if input_data is None:
            # Use the last few rows for prediction
            input_data = self.data[self.feature_columns].tail(5)
            print("🔮 Making predictions on recent data:")
        
        predictions = self.model.predict(input_data)
        
        print("\\n🎯 Predictions:")
        for i, pred in enumerate(predictions):
            print(f"   Sample {{i+1}}: {{pred:.2f}}")
        
        return predictions
    
    def visualize_predictions(self):
        """Create visualizations of predictions."""
        if self.model is None or self.data is None:
            print("❌ Need trained model and data for visualization!")
            return
        
        # Create predictions for the entire dataset
        X = self.data[self.feature_columns]
        predictions = self.model.predict(X)
        
        # Plot actual vs predicted
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.scatter(self.data[self.target_column], predictions, alpha=0.6)
        plt.plot([self.data[self.target_column].min(), self.data[self.target_column].max()], 
                 [self.data[self.target_column].min(), self.data[self.target_column].max()], 'r--')
        plt.xlabel(f'Actual {{self.target_column}}')
        plt.ylabel(f'Predicted {{self.target_column}}')
        plt.title('Actual vs Predicted')
        
        plt.subplot(1, 2, 2)
        if 'date' in self.data.columns:
            plt.plot(self.data['date'], self.data[self.target_column], label='Actual', alpha=0.7)
            plt.plot(self.data['date'], predictions, label='Predicted', alpha=0.7)
            plt.xticks(rotation=45)
        else:
            plt.plot(self.data[self.target_column], label='Actual', alpha=0.7)
            plt.plot(predictions, label='Predicted', alpha=0.7)
        
        plt.xlabel('Time')
        plt.ylabel(self.target_column)
        plt.title('Time Series: Actual vs Predicted')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('predictions_chart.png', dpi=150, bbox_inches='tight')
        print("📈 Visualization saved as 'predictions_chart.png'")
        plt.show()

def main():
    """Main application."""
    print("📊 Welcome to {details['display_name']}!")
    print("🔮 AI-powered prediction engine")
    print("=" * 50)
    
    engine = PredictionEngine()
    
    while True:
        print("\\n🎯 What would you like to do?")
        print("1. 📊 Use sample sales data")
        print("2. 📁 Load your own CSV data")
        print("3. 🔍 Explore current data")
        print("4. 🏋️ Train prediction model")
        print("5. 🔮 Make predictions")
        print("6. 📈 Visualize results")
        print("7. ❓ Help")
        print("8. 👋 Exit")
        
        choice = input("\\n🤔 Your choice (1-8): ").strip()
        
        if choice == "1":
            engine.load_sample_data()
            engine.prepare_features('sales')
            
        elif choice == "2":
            file_path = input("\\n📁 Enter CSV file path: ").strip()
            if engine.load_csv_data(file_path):
                print("\\n📋 Available columns:", list(engine.data.columns))
                target = input("🎯 Which column to predict? ").strip()
                if target in engine.data.columns:
                    engine.prepare_features(target)
                else:
                    print("❌ Column not found!")
            
        elif choice == "3":
            engine.explore_data()
            
        elif choice == "4":
            if engine.train_model():
                print("🎉 Ready to make predictions!")
                
        elif choice == "5":
            engine.make_predictions()
            
        elif choice == "6":
            engine.visualize_predictions()
            
        elif choice == "7":
            print("\\n💡 Help:")
            print("• Load data (CSV or use samples)")
            print("• Choose what you want to predict") 
            print("• Train the AI model")
            print("• Make predictions on new data")
            print("• The AI finds patterns in your data automatically!")
            
        elif choice == "8":
            print("\\n👋 Thanks for using the prediction engine!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
'''
        
        with open(project_path / "main.py", 'w') as f:
            f.write(main_code)
        
        # Create README
        readme_content = f'''# 📊 {details['display_name']}

{details['description']}

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the prediction engine:**
   ```bash
   python main.py
   ```

3. **Try the sample data or load your own CSV file**

## 🎯 Features

- 📊 Automatic pattern detection in data
- 🔮 Future value predictions
- 📈 Visual charts and graphs
- 📁 CSV file support
- 🎯 Easy-to-use interface
- 📊 Model performance metrics

## 💡 What Can You Predict?

- 💰 Sales forecasting
- 📈 Stock prices
- 🌡️ Weather patterns  
- 👥 Customer behavior
- 📊 Business metrics
- 🏠 House prices

## 🛠️ How to Enhance

1. **Advanced models**: Add Random Forest, Neural Networks
2. **Time series**: Implement ARIMA, LSTM for time-based data
3. **Feature engineering**: Create better input features
4. **Web interface**: Build a web app with Flask/Django
5. **Real-time predictions**: Connect to live data streams

## 📦 Requirements

- Python 3.7+
- pandas, numpy, scikit-learn
- matplotlib for visualizations

Created by: {details['author']}
Created on: {datetime.now().strftime("%Y-%m-%d")}
'''
        
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)
        
        # Create requirements.txt
        requirements = '''pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.2.0
matplotlib>=3.5.0

# Optional enhancements:
# tensorflow>=2.10.0     # For neural networks
# xgboost>=1.7.0         # For gradient boosting
# plotly>=5.11.0         # For interactive charts
# streamlit>=1.25.0      # For web interface
'''
        
        with open(project_path / "requirements.txt", 'w') as f:
            f.write(requirements)
        
        return project_path
    
    def create_project(self, project_type, details):
        """Create the selected project type."""
        creators = {
            "1": self.create_chatbot_project,
            "2": self.create_image_classifier_project,
            "3": self.create_prediction_engine_project,
            # Add more project types here
        }
        
        if project_type in creators:
            return creators[project_type](details)
        else:
            print(f"❌ Project type {{project_type}} not implemented yet!")
            return None
    
    def run(self):
        """Main wizard loop."""
        self.print_welcome()
        
        # Show project types
        projects = self.show_project_types()
        
        # Get user choice
        while True:
            choice = input("\\n🧙‍♂️ Which project sparks your interest? (1-8): ").strip()
            if choice in projects:
                break
            print("❌ Invalid choice. Please try again!")
        
        # Get project details
        details = self.get_project_details()
        
        # Create the project
        print(f"\\n🪄 Creating your {{projects[choice]['name']}} project...")
        print("✨ Weaving magic into code...")
        time.sleep(2)
        
        project_path = self.create_project(choice, details)
        
        if project_path:
            print(f"\\n🎉 Success! Your project is ready!")
            print(f"📂 Location: {{project_path}}")
            print(f"\\n🚀 Next steps:")
            print(f"   cd {{project_path}}")
            print(f"   pip install -r requirements.txt")
            print(f"   python main.py")
            print(f"\\n📚 Don't forget to read the README.md for more details!")
            print(f"\\n✨ Happy coding! Your AI adventure awaits! ✨")
        else:
            print("❌ Something went wrong. Please try again!")

def main():
    """Entry point."""
    wizard = ProjectWizard()
    wizard.run()

if __name__ == "__main__":
    main()
