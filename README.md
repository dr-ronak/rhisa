# RHISA Healthcare Chatbot

Regional Health Insight & Support Agent (RHISA) is an AI-powered healthcare chatbot designed to provide healthcare information and support for Gujarat and Maharashtra regions in India. The system focuses on eye health and skin conditions while maintaining strict privacy through synthetic data usage.

## Features

### Core Capabilities
- **Multilingual Support**: English, Gujarati, and Marathi
- **Regional Focus**: Specialized for Gujarat and Maharashtra healthcare needs
- **Healthcare Domains**: Eye health and skin conditions
- **Synthetic Data**: Privacy-compliant synthetic patient data
- **Compliance Checking**: Validates against regional healthcare guidelines
- **Trend Analysis**: Regional health pattern analysis
- **Patient Education**: Culturally appropriate health education materials

### Specialized Agents
- **Knowledge Agent**: Information retrieval and patient education
- **Trend Analyzer**: Regional health trend analysis and reporting
- **Compliance Checker**: Healthcare guideline validation

### API Endpoints
- `/api/v1/chat` - Main chat interface
- `/api/v1/knowledge/search` - Knowledge base search
- `/api/v1/trends/<region>/<condition>` - Health trend analysis
- `/api/v1/compliance/check` - Compliance validation
- `/api/v1/patient-education` - Educational content generation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd rhisa-healthcare-chatbot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables (optional):
```bash
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
```

## Usage

### Running the Application
1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

### Using the Chat Interface
1. Select your region (Gujarat or Maharashtra)
2. Choose your preferred language (English, Gujarati, or Marathi)
3. Type your healthcare question or use quick action buttons
4. Receive AI-powered responses with regional context

### Example Queries
- "What are the symptoms of cataract?"
- "Show me skin health trends in Gujarat"
- "Eye care guidelines for diabetes patients"
- "How to prevent fungal infections during monsoon?"
- "Emergency eye care contacts in Maharashtra"

## API Usage

### Chat API
```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of glaucoma?",
    "region": "gujarat",
    "language": "en"
  }'
```

### Knowledge Search API
```bash
curl "http://localhost:5000/api/v1/knowledge/search?query=cataract&region=gujarat&language=en"
```

### Trends API
```bash
curl "http://localhost:5000/api/v1/trends/gujarat/cataract"
```

### Compliance Check API
```bash
curl -X POST http://localhost:5000/api/v1/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "case_data": {
      "conditions": ["cataract"],
      "treatments": ["surgery"],
      "medications": ["eye drops"]
    },
    "region": "gujarat"
  }'
```

## Architecture

### Components
- **Flask Application**: Main web server and API endpoints
- **Agents**: Specialized AI agents for different healthcare tasks
- **Data Layer**: Synthetic data generation and management
- **Utils**: Language processing and entity extraction utilities
- **Config**: Application configuration and settings

### Data Privacy
- **Synthetic Data Only**: No real patient data is used
- **Privacy by Design**: Built-in privacy protection mechanisms
- **Compliance**: Adheres to healthcare data privacy regulations
- **Audit Logging**: Comprehensive activity tracking

## Configuration

### Environment Variables
- `FLASK_ENV`: Application environment (development/production)
- `SECRET_KEY`: Flask secret key for session management
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

### Regional Configuration
The application supports region-specific configurations including:
- Healthcare guidelines and protocols
- Emergency contact numbers
- Local health department information
- Cultural and linguistic preferences

## Development

### Project Structure
```
rhisa-healthcare-chatbot/
├── app.py                 # Main Flask application
├── agents/               # Specialized AI agents
│   ├── knowledge_agent.py
│   ├── trend_analyzer.py
│   └── compliance_checker.py
├── config/               # Configuration files
│   └── settings.py
├── data/                 # Data generation utilities
│   └── synthetic_generator.py
├── utils/                # Utility functions
│   ├── language_processor.py
│   └── entity_extractor.py
├── templates/            # HTML templates
│   └── index.html
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Adding New Features
1. **New Agent**: Create a new agent class in the `agents/` directory
2. **New API Endpoint**: Add route handlers in `app.py`
3. **New Language**: Update language configurations in `utils/language_processor.py`
4. **New Region**: Add regional data in `config/settings.py`

### Testing
Run the application in development mode:
```bash
export FLASK_ENV=development
python app.py
```

## Deployment

### Production Deployment
1. Set production environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```

2. Use a production WSGI server:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## Disclaimer

This chatbot is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## Acknowledgments

- Built for Gujarat and Maharashtra healthcare systems
- Designed with privacy-first principles
- Supports multilingual healthcare communication
- Promotes accessible healthcare information"# rhisa" 
