"""
Flask web API for RTO AI Enrollment System
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from .agents import EnrollmentManager

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
CORS(app)

# Global manager instance
global_manager = None

def get_manager():
    """Get or create the global enrollment manager"""
    global global_manager
    if global_manager is None:
        global_manager = EnrollmentManager()
    return global_manager

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint - returns pong"""
    return jsonify({'status': 'pong', 'message': 'Server is running'}), 200

@app.route('/rto', methods=['GET'])
def rto():
    """Route to home screen"""
    return redirect(url_for('index'))

@app.route('/api/new_inquiry', methods=['POST'])
def api_new_inquiry():
    """API endpoint for new student inquiry"""
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    program = data.get('program', '').strip()

    if not all([name, email, phone, program]):
        return jsonify({'error': 'All fields are required'}), 400

    manager = get_manager()
    student_id, message = manager.new_inquiry(name, email, phone, program)

    return jsonify({
        'student_id': student_id,
        'message': message,
        'success': True
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for student conversation"""
    data = request.get_json()
    student_id = data.get('student_id', '').strip()
    user_message = data.get('message', '').strip()

    if not student_id or not user_message:
        return jsonify({'error': 'Student ID and message are required'}), 400

    manager = get_manager()
    response = manager.process_response(student_id, user_message)

    if 'error' in response:
        return jsonify({'error': response['error']}), 400

    return jsonify({
        'message': response['message'],
        'qualification_score': response.get('qualification_score'),
        'recommendation': response.get('recommendation'),
        'action': response.get('action'),
        'success': True
    })

@app.route('/api/followup/<student_id>', methods=['GET'])
def api_followup(student_id):
    """API endpoint for generating follow-up messages"""
    manager = get_manager()
    followup = manager.generate_followup_message(student_id)

    if 'error' in followup:
        return jsonify({'error': followup['error']}), 404

    return jsonify({
        'followup_message': followup['followup_message'],
        'recommended_channel': followup['recommended_channel'],
        'success': True
    })

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """API endpoint for dashboard data"""
    manager = get_manager()
    dashboard = manager.get_dashboard()
    return jsonify(dashboard)

@app.route('/api/export', methods=['GET'])
def api_export():
    """API endpoint for exporting student data"""
    manager = get_manager()
    export_data = manager.export_students()
    return jsonify(export_data)

@app.route('/api/students', methods=['GET'])
def api_students():
    """API endpoint for getting all students"""
    manager = get_manager()
    students = manager.db.list_all()
    students_data = [s.to_dict() for s in students]
    return jsonify({'students': students_data})


def run_web_server():
    """Run the Flask web server on port 5008"""
    port = 5008
    print(f"Starting web server on port {port}...")
    print(f"Open http://localhost:{port} in your browser")
    app.run(debug=True, host='0.0.0.0', port=port)

