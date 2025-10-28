"""
Flask backend for Job Matcher API
Optimized for DigitalOcean App Platform deployment
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

app = Flask(__name__)

# Get the port from environment variable (DigitalOcean sets PORT to 8080)
port = int(os.environ.get('PORT', 8080))

# Configure CORS for Lovable and local development
cors_origins = [
    "https://app.lovable.dev",  # Lovable development
    "https://app.lovable.co",   # Lovable production
    "https://*.lovable.dev",    # Lovable subdomains
    "https://*.lovable.co",     # Lovable subdomains
    "https://job-matcher-app-dusky.vercel.app",  # Existing Vercel frontend
    "http://localhost:3000",
    "https://localhost:3000",
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000"
]

# Allow dynamic origins based on environment
if os.getenv('ALLOWED_ORIGINS'):
    cors_origins.extend(os.getenv('ALLOWED_ORIGINS').split(','))

CORS(app, origins=cors_origins, supports_credentials=True)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for DigitalOcean"""
    return jsonify({
        "status": "healthy",
        "service": "Job Matcher API",
        "version": "1.0.0",
        "message": "Backend is running successfully on DigitalOcean",
        "port": port,
        "provider": "DigitalOcean App Platform"
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "Job Matcher API is running",
        "version": "1.0.0",
        "provider": "DigitalOcean App Platform",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "docs": "/docs (POST - for OpenAPI specification)",
            "api_info": "API accepts resume_text, job_title, description, requirements, benefits"
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
                "error": f"Missing required fields: {', '.join(missing)}",
                "status": "error",
                "code": 400
            }), 400

        resume_text = data.get('resume_text', '')
        job_title = data.get('job_title', '').lower()
        description = data.get('description', '').lower()
        requirements = data.get('requirements', '').lower()
        benefits = data.get('benefits', '').lower()

        # Extract skills from resume (simple keyword matching)
        tech_skills = ['python', 'java', 'javascript', 'react', 'nodejs', 'node.js', 'docker', 'kubernetes',
                      'aws', 'azure', 'gcp', 'mongodb', 'postgresql', 'mysql', 'tensorflow',
                      'pytorch', 'machine learning', 'ml', 'ai', 'devops', 'git', 'ci/cd', 'typescript',
                      'vue', 'angular', 'flask', 'django', 'fastapi', 'rest api', 'graphql',
                      'sql', 'nosql', 'redis', 'elasticsearch', 'kafka', 'microservices',
                      'gitlab', 'bitbucket', 'jira', 'confluence', 'trello', 'slack', 'discord']

        found_skills = []
        for skill in tech_skills:
            if skill in resume_text.lower():
                found_skills.append(skill)

        # Extract required skills from job requirements
        required_skills = []
        for skill in tech_skills:
            if skill in requirements or skill in description:
                required_skills.append(skill)

        # Calculate match score
        if required_skills:
            matches = len([skill for skill in found_skills if skill in required_skills])
            match_score = min(0.95, 0.3 + (matches / len(required_skills)))
        else:
            match_score = min(0.85, 0.5 + (len(found_skills) * 0.05))

        # Predict salary based on job title, experience, and skills
        if 'intern' in job_title or 'fresher' in job_title or 'entry level' in job_title:
            salary_range = "5-8 million VND"
        elif 'junior' in job_title or 'entry' in job_title:
            salary_range = "10-15 million VND"
        elif 'mid' in job_title or '2-3' in job_title or '3-5' in job_title or 'associate' in job_title:
            salary_range = "15-25 million VND"
        elif 'senior' in job_title or '5+' in job_title or 'sr' in job_title:
            salary_range = "25-35 million VND"
        elif 'lead' in job_title or 'principal' in job_title or 'staff' in job_title:
            salary_range = "30-45 million VND"
        elif 'manager' in job_title or 'head' in job_title or 'director' in job_title:
            salary_range = "40-60 million VND"
        elif 'vp' in job_title or 'vice president' in job_title:
            salary_range = "70-100 million VND"
        elif 'cto' in job_title or 'c-level' in job_title:
            salary_range = "100-150 million VND"
        else:
            # Adjust based on skills
            if any(s in found_skills for s in ['python', 'machine learning', 'tensorflow', 'pytorch']):
                salary_range = "20-30 million VND"
            else:
                salary_range = "15-25 million VND"

        # Determine missing skills
        missing_skills = list(set(required_skills) - set(found_skills))[:5]  # Top 5 missing

        # Extract years of experience
        exp_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'experience\s*:?\s*(\d+)',
            r'(\d+)\s*-\s*\d+\s*(?:years?|yrs?)'
        ]

        experience_years = 0
        for pattern in exp_patterns:
            matches = re.findall(pattern, resume_text.lower())
            if matches:
                experience_years = int(matches[0])
                break

        # Parse resume info
        education_level = "Not specified"
        if any(degree in resume_text.lower() for degree in ['bachelor', 'bs', 'b.s.', 'beng']):
            education_level = "Bachelor's Degree"
        elif any(degree in resume_text.lower() for degree in ['master', 'ms', 'm.s.', 'meng']):
            education_level = "Master's Degree"
        elif any(degree in resume_text.lower() for degree in ['phd', 'ph.d', 'doctorate']):
            education_level = "PhD"

        parsed_resume = {
            "experience_years": experience_years,
            "education": education_level,
            "skills": found_skills[:15],  # Top 15 skills
            "skill_count": len(found_skills),
            "resume_length": len(resume_text),
            "certifications": [],
            "languages": ["Vietnamese", "English"],
            "has_github": 'github.com' in resume_text.lower(),
            "has_linkedin": 'linkedin.com' in resume_text.lower()
        }

        # Add certifications based on keywords
        if 'aws' in resume_text.lower():
            parsed_resume["certifications"].append("AWS Certified")
        if 'azure' in resume_text.lower():
            parsed_resume["certifications"].append("Azure Certified")
        if 'gcp' in resume_text.lower():
            parsed_resume["certifications"].append("Google Cloud Certified")

        response = {
            "status": "success",
            "predicted_salary": salary_range,
            "match_score": round(match_score, 2),
            "match_percentage": f"{int(match_score * 100)}%",
            "missing_skills": missing_skills,
            "found_skills": found_skills[:15],
            "parsed_resume": parsed_resume,
            "analysis": {
                "total_required_skills": len(required_skills),
                "matched_skills": len([s for s in found_skills if s in required_skills]),
                "relevance": "High" if match_score > 0.7 else "Medium" if match_score > 0.5 else "Low",
                "experience_level": "Senior" if experience_years > 5 else "Mid-level" if experience_years > 2 else "Junior"
            },
            "job_analysis": {
                "is_tech_role": any(tech in job_title for tech in ['engineer', 'developer', 'programmer', 'architect']),
                "is_management": any(mgmt in job_title for mgmt in ['manager', 'lead', 'head', 'director']),
                "estimated_level": "Senior" if any(sr in job_title for sr in ['senior', 'sr', 'principal', 'staff']) else "Junior" if any(jr in job_title for jr in ['junior', 'jr', 'entry']) else "Mid"
            },
            "note": "This is an enhanced mock prediction with intelligent parsing. The actual PhoBERT model will provide more accurate analysis."
        }

        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Error in predict: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}",
            "code": 500
        }), 500

@app.route('/docs', methods=['GET'])
def openapi_docs():
    """OpenAPI/Swagger documentation for Lovable"""
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Job Matcher API",
            "description": "API for matching resumes with job postings using AI analysis",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
                "email": "support@jobmatcher.com"
            }
        },
        "servers": [
            {
                "url": "https://your-job-matcher-api.ondigitalocean.app",
                "description": "Production server on DigitalOcean"
            },
            {
                "url": "http://localhost:8080",
                "description": "Development server"
            }
        ],
        "paths": {
            "/health": {
                "get": {
                    "summary": "Health check endpoint",
                    "description": "Check if the API is running",
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "service": {"type": "string"},
                                            "version": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/predict": {
                "post": {
                    "summary": "Analyze resume-job match",
                    "description": "Analyze a resume against a job posting to predict salary and match score",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["resume_text", "job_title", "description"],
                                    "properties": {
                                        "resume_text": {
                                            "type": "string",
                                            "description": "Complete resume text"
                                        },
                                        "job_title": {
                                            "type": "string",
                                            "description": "Job title"
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "Job description"
                                        },
                                        "requirements": {
                                            "type": "string",
                                            "description": "Job requirements (optional)"
                                        },
                                        "benefits": {
                                            "type": "string",
                                            "description": "Job benefits (optional)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful analysis",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "predicted_salary": {"type": "string"},
                                            "match_score": {"type": "number"},
                                            "match_percentage": {"type": "string"},
                                            "missing_skills": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "found_skills": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "parsed_resume": {
                                                "type": "object"
                                            },
                                            "analysis": {
                                                "type": "object"
                                            },
                                            "job_analysis": {
                                                "type": "object"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Bad request - missing required fields",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"},
                                            "status": {"type": "string"},
                                            "code": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Internal server error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"},
                                            "status": {"type": "string"},
                                            "code": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)