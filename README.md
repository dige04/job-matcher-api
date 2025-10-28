# Job Matcher API

Simple Flask backend for the Job Matcher application.

## Features

- Resume and job matching analysis
- Salary prediction based on job title and skills
- Skill extraction and gap analysis
- CORS enabled for frontend integration

## Deploy to Render

1. Push this repository to GitHub
2. Go to [render.com](https://render.com)
3. Click "New Web Service"
4. Connect your GitHub repository
5. Use the following settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

## Environment Variables

No environment variables required for basic functionality.

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Analyze resume-job match

### Predict Request Format

```json
{
  "resume_text": "Your resume text here...",
  "job_title": "Software Engineer",
  "description": "Job description...",
  "requirements": "Job requirements...",
  "benefits": "Benefits..."
}
```