import os
import sys

# Add project_root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5002)