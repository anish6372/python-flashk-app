#!/usr/bin/env python3
"""
Simple Flask Web Application for AWS CI/CD Demo
"""
from flask import Flask, jsonify, render_template_string
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AWS CI/CD Demo App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { color: #232F3E; text-align: center; }
        .info { background-color: #E7F3FF; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .button { background-color: #FF9900; color: white; padding: 10px 20px; border: none; border-radius: 4px; text-decoration: none; display: inline-block; margin: 10px 5px; }
        .button:hover { background-color: #E68900; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🚀 AWS CI/CD Pipeline Demo</h1>
        <div class="info">
            <h3>Application Status: ✅ Running</h3>
            <p><strong>Environment:</strong> {{ env }}</p>
            <p><strong>Version:</strong> 1.0.0</p>
            <p><strong>Build:</strong> {{ build_id }}</p>
        </div>
        
        <h2>Available Endpoints:</h2>
        <ul>
            <li><a href="/" class="button">Home</a> - This page</li>
            <li><a href="/health" class="button">Health Check</a> - API health status</li>
            <li><a href="/info" class="button">App Info</a> - Application information</li>
        </ul>
        
        <div class="info">
            <h3>📋 CI/CD Pipeline Features:</h3>
            <ul>
                <li>✅ Automated builds with AWS CodeBuild</li>
                <li>✅ GitHub integration for source control</li>
                <li>✅ Automated testing and deployment</li>
                <li>✅ Docker containerization support</li>
                <li>✅ Health monitoring endpoints</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with application information"""
    env = os.getenv('ENVIRONMENT', 'development')
    build_id = os.getenv('CODEBUILD_BUILD_ID', 'local-build')
    
    return render_template_string(HOME_TEMPLATE, env=env, build_id=build_id)

@app.route('/health')
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Perform basic health checks here
        response = {
            'status': 'healthy',
            'timestamp': str(os.environ.get('REQUEST_TIME', 'N/A')),
            'environment': os.getenv('ENVIRONMENT', 'development'),
            'version': '1.0.0',
            'checks': {
                'database': 'ok',  # Add actual DB check if needed
                'memory': 'ok',
                'disk': 'ok'
            }
        }
        logger.info("Health check passed")
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

@app.route('/info')
def app_info():
    """Application information endpoint"""
    info = {
        'name': 'AWS CI/CD Demo Application',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'build_id': os.getenv('CODEBUILD_BUILD_ID', 'local-build'),
        'python_version': os.environ.get('PYTHON_VERSION', 'Unknown'),
        'aws_region': os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Home page'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/info', 'method': 'GET', 'description': 'Application info'}
        ]
    }
    return jsonify(info)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)