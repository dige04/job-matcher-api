# Job Matcher API for Lovable Integration

Lightweight Flask API for resume-job matching analysis, optimized for DigitalOcean deployment.

## Features

- **Smart Resume Analysis**: Extracts skills, experience, and education from resumes
- **Job Matching**: Calculates match scores between resumes and job postings
- **Salary Prediction**: Estimates salary ranges based on job title and skills
- **CORS Enabled**: Configured for Lovable domains
- **OpenAPI Documentation**: Full API documentation at `/docs`

## API Endpoints

### Health Check
```
GET /health
```

### Root Endpoint
```
GET /
```

### Prediction (Main Endpoint)
```
POST /predict
Content-Type: application/json

{
  "resume_text": "Your resume text here...",
  "job_title": "Senior Software Engineer",
  "description": "Job description...",
  "requirements": "Python, React, AWS...",
  "benefits": "Health insurance, 401k..."
}
```

### API Documentation
```
GET /docs
```

## Deployment to DigitalOcean

### Option 1: Using DigitalOcean Dashboard (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create DigitalOcean App**:
   - Go to https://cloud.digitalocean.com/apps/new
   - Select "GitHub" as source
   - Choose this repository
   - Use the following settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Run Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
     - **HTTP Port**: `8080`
     - **Instance Size**: Basic XXS (free tier eligible)

3. **Environment Variables** (optional):
   - `ALLOWED_ORIGINS`: `https://app.lovable.dev,https://app.lovable.co`
   - `PORT`: `8080`

### Option 2: Using doctl CLI

1. **Install doctl**:
   ```bash
   brew install doctl
   ```

2. **Authenticate**:
   ```bash
   doctl auth init
   ```

3. **Deploy**:
   ```bash
   ./deploy_do.sh
   ```

## Integration with Lovable

Once deployed, your API endpoint will be:
```
https://your-app-name.ondigitalocean.app
```

Use this URL in your Lovable frontend to make API calls:

```javascript
const response = await fetch('https://your-app-name.ondigitalocean.app/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    resume_text: resume,
    job_title: jobTitle,
    description: jobDesc,
    requirements: jobReq,
    benefits: jobBen
  })
});
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python3 app.py

# Test the API
curl -X GET http://localhost:8080/health
```

## Example Response

```json
{
  "status": "success",
  "predicted_salary": "25-35 million VND",
  "match_score": 0.85,
  "match_percentage": "85%",
  "missing_skills": ["kubernetes", "graphql"],
  "found_skills": ["python", "react", "aws", "docker"],
  "parsed_resume": {
    "experience_years": 5,
    "education": "Bachelor's Degree",
    "skills": ["python", "react", "aws", "docker"],
    "skill_count": 4
  },
  "analysis": {
    "total_required_skills": 6,
    "matched_skills": 4,
    "relevance": "High",
    "experience_level": "Senior"
  }
}
```
