from flask import jsonify
from app import app
import teradatasql
from app.config import DATABASE_CONFIG

@app.route('/api/parents', methods=['GET'])
def get_parents():
    try:
        conn = teradatasql.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        # Obtenir les noms des colonnes à partir des métadonnées
        cursor.execute("HELP COLUMN Profiles.*")
        columns_info = cursor.fetchall()
        
        # Les noms des colonnes sont dans la première colonne des résultats
        column_names = [col_info[0] for col_info in columns_info]
        
        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()
        
        # Retourner les noms des colonnes
        return jsonify({
            'column_names': column_names
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_connection', methods=['GET'])
def check_connection():
    try:
        conn = teradatasql.connect(**DATABASE_CONFIG)
        conn.close()
        return jsonify({"message": "La connexion à Teradata est établie."}), 200
    except Exception as e:
        return jsonify({"error": "Impossible de se connecter à Teradata.", "details": str(e)}), 500
