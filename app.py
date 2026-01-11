#!/usr/bin/env python3
"""
Flask web interface for the AI Agent application.
"""
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import os
from datetime import datetime

from src.agent import Agent
from src.tools import CalculatorTool, WeatherTool, WebSearchTool

app = Flask(__name__)
CORS(app)

# Global agent instance
agent = None


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/init', methods=['POST'])
def init_agent():
    """Initialize the agent with specified configuration."""
    global agent
    
    data = request.json
    provider = data.get('provider', 'ollama')
    model = data.get('model', 'llama3')
    use_tools = data.get('use_tools', True)
    api_key = data.get('api_key')
    
    try:
        tools = None
        if use_tools:
            tools = [CalculatorTool(), WeatherTool(), WebSearchTool()]
        
        kwargs = {}
        if api_key:
            kwargs['api_key'] = api_key
        
        agent = Agent(
            provider=provider,
            model=model,
            tools=tools,
            **kwargs
        )
        
        return jsonify({
            'success': True,
            'info': agent.get_info()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to the agent."""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 400
    
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = agent.chat(message)
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Stream chat response."""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 400
    
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    def generate():
        try:
            for chunk in agent.chat(message, stream=True):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history."""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 400
    
    agent.clear_history()
    return jsonify({'success': True})


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get agent information."""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 400
    
    return jsonify(agent.get_info())


@app.route('/api/save', methods=['POST'])
def save_conversation():
    """Save conversation to file."""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 400c
    
    filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs('conversations', exist_ok=True)
    filepath = os.path.join('conversations', filename)
    
    agent.save_conversation(filepath)
    return jsonify({
        'success': True,
        'filepath': filepath
    })


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🤖 Free AI Agent Web Interface")
    print("="*50)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
