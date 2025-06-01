#!/usr/bin/env python3
"""
Dummy Flask Application
A simple web app example that follows the app_setup.py structure
"""

import os
from flask import Flask, render_template_string

# Create Flask app
app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dummy App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        ul { line-height: 1.6; }
        .port { font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Dummy Flask Application</h1>
        
        <div class="success">
            <strong>✅ Success!</strong> Your application is running correctly.
        </div>
        
        <div class="info">
            <h3>📋 Application Info:</h3>
            <ul>
                <li><strong>Port:</strong> <span class="port">{{ port }}</span></li>
                <li><strong>Host:</strong> {{ host }}</li>
                <li><strong>Environment:</strong> {{ env_info }}</li>
                <li><strong>Template Directory:</strong> {{ template_dir }}</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🎯 What this demonstrates:</h3>
            <ul>
                <li>Flask web application setup</li>
                <li>Environment variable configuration (CDSW_READONLY_PORT)</li>
                <li>Template directory usage</li>
                <li>Basic routing and templating</li>
                <li>Integration with app_setup.py launcher</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🔧 How to use:</h3>
            <ul>
                <li>Run <code>python app_setup.py</code> to automatically setup and start</li>
                <li>Or run <code>python app.py</code> directly</li>
                <li>Access the app at: <a href="http://{{ host }}:{{ port }}">http://{{ host }}:{{ port }}</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page of the dummy app"""
    port = os.getenv('CDSW_READONLY_PORT', '8090')
    host = '127.0.0.1'
    template_dir = os.environ.get("TEMPLATE_DIR", "template")
    
    return render_template_string(HTML_TEMPLATE, 
                                port=port, 
                                host=host,
                                env_info="Development" if app.debug else "Production",
                                template_dir=template_dir)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "port": os.getenv('CDSW_READONLY_PORT', '8090'),
        "template_dir": os.environ.get("TEMPLATE_DIR", "template")
    }

@app.route('/api/test')
def api_test():
    """Simple API endpoint for testing"""
    return {
        "message": "Hello from the dummy app!",
        "status": "success",
        "data": {
            "app_name": "Dummy Flask App",
            "version": "1.0.0",
            "port": os.getenv('CDSW_READONLY_PORT', '8090')
        }
    }

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Get port from environment variable (following app_setup.py instructions)
    PORT = os.getenv('CDSW_READONLY_PORT', '8090')
    
    print(f"🚀 Starting Dummy Flask App on http://127.0.0.1:{PORT}")
    print(f"📁 Template directory: {os.environ.get('TEMPLATE_DIR', 'template')}")
    print("🛑 Press Ctrl+C to stop")
    
    # Run the app (following the pattern from app_setup.py comments)
    app.run(host="127.0.0.1", port=int(PORT))
    # Alternative for development: app.run(debug=True, host='0.0.0.0', port=5000) 