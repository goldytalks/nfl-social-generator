"""
NFL Social Content Generator - Main Flask Application
Phase 1: MVP with manual context input
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd

from modules import CSVProcessor, MoversAnalyzer, TweetGenerator
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

# Ensure upload and export folders exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.EXPORT_FOLDER, exist_ok=True)

# Global variables to store session data
current_data = {
    'df': None,
    'movers': None,
    'results': None,
    'filename': None
}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV files allowed'}), 400

    try:
        filename = secure_filename(file.filename)

        # Process CSV directly from memory (no disk write needed)
        # This works in serverless environments like Vercel
        processor = CSVProcessor(file_object=file)
        if not processor.process():
            errors = processor.get_errors()
            return jsonify({'error': f'CSV processing failed: {", ".join(errors)}'}), 400

        # Store data globally
        current_data['df'] = processor.get_data()
        current_data['filename'] = filename

        # Get summary
        summary = processor.get_summary()

        return jsonify({
            'success': True,
            'filename': filename,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_movers():
    """Analyze data to find biggest movers"""
    if current_data['df'] is None:
        return jsonify({'error': 'No data loaded. Please upload CSV first.'}), 400

    try:
        # Get configuration from request or use defaults
        data = request.get_json() or {}
        threshold = data.get('threshold', config.MOVEMENT_THRESHOLD)
        top_n = data.get('top_n', config.TOP_N_MOVERS)

        # Create config dict
        analyzer_config = {
            'movement_threshold': threshold,
            'top_n_movers': top_n
        }

        # Analyze movers
        analyzer = MoversAnalyzer(current_data['df'], analyzer_config)
        movers = analyzer.identify_movers()

        # Store movers
        current_data['movers'] = movers

        # Get summary
        summary = analyzer.get_movers_summary()

        # Convert movers to list of dicts for JSON
        movers_list = movers.to_dict('records')

        # Format for display
        for mover in movers_list:
            mover['last_week_american'] = format_american_odds(mover['last_week_american'])
            mover['this_week_american'] = format_american_odds(mover['this_week_american'])

        return jsonify({
            'success': True,
            'movers': movers_list,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/generate', methods=['POST'])
def generate_tweets():
    """Generate tweet drafts for movers"""
    if current_data['movers'] is None:
        return jsonify({'error': 'No movers analyzed. Please analyze data first.'}), 400

    try:
        # Get contexts from request (optional)
        data = request.get_json() or {}
        contexts = data.get('contexts', {})

        # Get config
        generator_config = config.get_config()

        # Generate tweets
        generator = TweetGenerator(generator_config)
        results = generator.generate_batch(current_data['movers'], contexts)

        # Store results
        current_data['results'] = results

        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        return jsonify({'error': f'Tweet generation failed: {str(e)}'}), 500


@app.route('/api/export', methods=['POST'])
def export_results():
    """Export generated tweets to JSON (returns data directly for serverless compatibility)"""
    if current_data['results'] is None:
        return jsonify({'error': 'No results to export. Please generate tweets first.'}), 400

    try:
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tweets_{timestamp}.json'

        # Prepare export data
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'source_file': current_data['filename'],
            'config': config.get_config(),
            'results': current_data['results']
        }

        # In serverless environments (Vercel), return data directly
        # User can save the JSON from the response
        return jsonify({
            'success': True,
            'filename': filename,
            'data': export_data
        })

    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download exported file"""
    try:
        filepath = os.path.join(config.EXPORT_FOLDER, secure_filename(filename))
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 404


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify(config.get_config())


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration (for session only)"""
    # This would update config for current session
    # Not implementing persistent config changes in MVP
    return jsonify({'message': 'Config update not implemented in MVP'})


def format_american_odds(odds):
    """Format American odds with +/- sign"""
    try:
        odds_int = int(float(odds))
        return f'+{odds_int}' if odds_int > 0 else str(odds_int)
    except:
        return str(odds)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
