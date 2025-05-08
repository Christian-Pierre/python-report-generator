import tempfile
import logging
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from weasyprint import HTML
from utils import multiplos_json_para_html, aula_pratica_para_html, aula_teorica_para_html

app = Flask(__name__)
CORS(app)  # Libera CORS para todas as origens

logging.basicConfig(level=logging.INFO)

@app.route('/generate-multi', methods=['POST'])
def generate_multi_pdf():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    try:
        data = file.read().decode('utf-8')
        html = multiplos_json_para_html(data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=html).write_pdf(pdf_file.name)
            return send_file(
                pdf_file.name,
                as_attachment=True,
                download_name="relatorios.pdf",
                mimetype="application/pdf"
            )

    except Exception as e:
        app.logger.exception("Erro ao gerar PDF múltiplo:")
        return jsonify({"error": "Erro interno no servidor"}), 500


@app.route('/relatorio-aula-pratica', methods=['POST'])
def gerar_relatorio_aula_pratica():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Arquivo não enviado"}), 400

    try:
        data = file.read().decode('utf-8')
        html = aula_pratica_para_html(data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=html).write_pdf(pdf_file.name)
            return send_file(
                pdf_file.name,
                as_attachment=True,
                download_name="relatorio_aula.pdf",
                mimetype="application/pdf"
            )

    except Exception as e:
        app.logger.exception("Erro ao gerar relatório de aula:")
        return jsonify({"error": "Erro interno no servidor"}), 500

@app.route('/relatorio-aula-teorica', methods=['POST'])
def gerar_relatorio_aula_teorica():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Arquivo não enviado"}), 400

    try:
        data = file.read().decode('utf-8')
        html = aula_teorica_para_html(data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=html).write_pdf(pdf_file.name)
            return send_file(
                pdf_file.name,
                as_attachment=True,
                download_name="relatorio_aula.pdf",
                mimetype="application/pdf"
            )

    except Exception as e:
        app.logger.exception("Erro ao gerar relatório de aula:")
        return jsonify({"error": "Erro interno no servidor"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


# Sempre mantenha esse bloco por último
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
