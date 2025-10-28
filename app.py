"""
Simple Flask backend for Job Matcher API
Optimized for Render.com deployment
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

app = Flask(__name__)

# Configure CORS - allow your Vercel frontend
cors_origins = [
    "https://job-matcher-app-dusky.vercel.app",
    "http://localhost:3000",
    "https://localhost:3000"
]

CORS(app, origins=cors_origins)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Job Matcher API",
        "version": "1.0.0",
        "message": "Backend is running successfully"
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "Job Matcher API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "docs": "API accepts resume_text, job_title, description, requirements, benefits"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint with smart mock data"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['resume_text', 'job_title', 'description']
        missing = [field for field in required_fields if not data.get(field)]

        if missing:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        resume_text = data.get('resume_text', '')
        job_title = data.get('job_title', '').lower()
        description = data.get('description', '').lower()
        requirements = data.get('requirements', '').lower()
        benefits = data.get('benefits', '').lower()

        # Extract skills from resume (simple keyword matching)
        tech_skills = ['python', 'java', 'javascript', 'react', 'nodejs', 'docker', 'kubernetes',
                      'aws', 'azure', 'gcp', 'mongodb', 'postgresql', 'mysql', 'tensorflow',
                      'pytorch', 'machine learning', 'ai', 'devops', 'git', 'ci/cd']

        found_skills = [skill for skill in tech_skills if skill in resume_text.lower()]

        # Extract required skills from job requirements
        required_skills = [skill for skill in tech_skills if skill in requirements or skill in description]

        # Calculate match score
        if required_skills:
            matches = len([skill for skill in found_skills if skill in required_skills])
            match_score = min(0.95, 0.3 + (matches / len(required_skills)))
        else:
            match_score = min(0.85, 0.5 + (len(found_skills) * 0.1))

        # Predict salary based on job title and skills
        if 'intern' in job_title or 'fresher' in job_title:
            salary_range = "5-8 million VND"
        elif 'junior' in job_title or 'entry' in job_title:
            salary_range = "10-15 million VND"
        elif 'mid' in job_title or '2-3' in job_title or '3-5' in job_title:
            salary_range = "15-25 million VND"
        elif 'senior' in job_title or '5+' in job_title:
            salary_range = "25-35 million VND"
        elif 'lead' in job_title or 'principal' in job_title:
            salary_range = "30-45 million VND"
        elif 'manager' in job_title or 'head' in job_title or 'director' in job_title:
            salary_range = "40-60 million VND"
        else:
            salary_range = "15-25 million VND"

        # Determine missing skills
        missing_skills = list(set(required_skills) - set(found_skills))[:5]  # Top 5 missing

        # Extract years of experience
        exp_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        exp_matches = re.findall(exp_pattern, resume_text.lower())
        experience_years = int(exp_matches[0]) if exp_matches else 0

        # Parse resume info
        parsed_resume = {
            "experience_years": experience_years,
            "education": "Bachelor's Degree in Computer Science" if 'degree' in resume_text.lower() else "Not specified",
            "skills": found_skills[:10],  # Top 10 skills
            "skill_count": len(found_skills),
            "resume_length": len(resume_text),
            "certifications": ["AWS Certified"] if 'aws' in resume_text.lower() else [],
            "languages": ["Vietnamese", "English"]
        }

        response = {
            "predicted_salary": salary_range,
            "match_score": round(match_score, 2),
            "match_percentage": f"{int(match_score * 100)}%",
            "missing_skills": missing_skills,
            "found_skills": found_skills[:10],
            "parsed_resume": parsed_resume,
            "analysis": {
                "total_required_skills": len(required_skills),
                "matched_skills": len([s for s in found_skills if s in required_skills]),
                "relevance": "High" if match_score > 0.7 else "Medium" if match_score > 0.5 else "Low"
            },
            "note": "This is an enhanced mock prediction. The actual PhoBERT model will provide more accurate analysis."
        }

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error in predict: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)