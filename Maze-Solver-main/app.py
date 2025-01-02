from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from utils.image_processing import preprocess_image, process_image_in_bins
from utils.maze_solver import find_start_and_end, a_star_algorithm_animated
from utils.visualization import create_animation
import logging

# Initialize Flask app
app = Flask(__name__, static_folder='static_files')
CORS(app)

# Ensure required directories exist
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')


@app.route('/solve_maze', methods=['POST'])
def solve_maze():
    """Handle maze solving."""
    try:
        # Validate and retrieve uploaded file
        file = request.files.get('mazeImage')
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        logging.info(f"File uploaded and saved to {file_path}")

        # Preprocess the image
        binary_img = preprocess_image(file_path, bin_size=(1,1), scale_percent=30)
        processed_img = process_image_in_bins(binary_img, bin_size=(1,1))
        logging.info("Image preprocessing complete")

        # Solve the maze
        start, end = find_start_and_end(processed_img)
        path, frames, _ = a_star_algorithm_animated(processed_img, start, end)
        if not path:
            return jsonify({"error": "No path found in the maze"}), 400
        logging.info("Maze solving complete")

        # Create and save the animation
        output_filename = f"{os.path.splitext(file.filename)[0]}_solution.gif"
        output_path = os.path.join(STATIC_FOLDER, output_filename)
        create_animation(frames, output_path)
        logging.info(f"Animation saved to {output_path}")

        # Return the URL of the generated GIF
        return jsonify({"gifUrl": f"/static_files/{output_filename}"})
    
    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
        return jsonify({"error": f"Value Error: {str(ve)}"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/static_files')
def serve_static(filename):
    """Serve static files (GIFs)."""
    return send_from_directory(STATIC_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    