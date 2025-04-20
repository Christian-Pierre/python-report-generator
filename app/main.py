import tempfile
from flask import Flask, request, send_file, jsonify
from weasyprint import HTML
from utils import multiplos_json_para_html, aula_para_html

app = Flask(__name__)

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
            return send_file(pdf_file.name, as_attachment=True, download_name="relatorios.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/relatorio-aula', methods=['POST'])
def gerar_relatorio_aula():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Arquivo não enviado"}), 400

    try:
        data = file.read().decode('utf-8')
        html = aula_para_html(data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=html).write_pdf(pdf_file.name)
            return send_file(pdf_file.name, as_attachment=True, download_name="relatorio_aula.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Sempre mantenha esse bloco por último
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
