import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


env = Environment(loader=FileSystemLoader("app/templates"))

def multiplos_json_para_html(json_data):
    try:
        relatórios = json.loads(json_data)
        html_total = ""

        template = env.get_template("base.html")

        for relatorio in relatórios:
            titulo = relatorio.get("titulo", "Relatório")
            dados = relatorio.get("dados", [])

            if not isinstance(dados, list) or not dados:
                continue

            headers = list(dados[0].keys())
            rows = [[item.get(h, "") for h in headers] for item in dados]

            html = template.render(titulo=titulo, headers=headers, rows=rows)
            html_total += html + "<hr style='page-break-after: always;'>"

        return html_total

    except Exception as e:
        raise ValueError(f"Erro ao processar relatórios: {e}")

def aula_pratica_para_html(data):
    try:
        parsed = json.loads(data)
    except:
        parsed = {}

    # Dados mock para teste se JSON estiver vazio
    if not parsed:
        parsed = {
            "nome_aluno": "Aluno Teste",
            "data_hora_aula": datetime.now().isoformat(),
            "biometrias": [
                {
                    "autor": "aluno",
                    "tipo": "dedo polegar direito",
                    "hora": "10:00",
                    "imagem_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"  # Pequeno base64 válido
                },
                {
                    "autor": "aluno",
                    "tipo": "dedo indicador esquerdo",
                    "hora": "10:01",
                    "imagem_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
                },
                {
                    "autor": "instrutor",
                    "tipo": "dedo polegar esquerdo",
                    "hora": "10:02",
                    "imagem_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
                },
                {
                    "autor": "instrutor",
                    "tipo": "dedo indicador direito",
                    "hora": "10:03",
                    "imagem_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
                }
            ]
        }

    nome_aluno = parsed.get("nome_aluno", "Aluno Desconhecido")
    data_hora_aula = parsed.get("data_hora_aula", "")
    data_formatada = ""
    try:
        data_formatada = datetime.fromisoformat(data_hora_aula).strftime("%d/%m/%Y %H:%M")
    except:
        data_formatada = data_hora_aula

    biometrias = parsed.get("biometrias", [])

    # Normaliza base64
    for b in biometrias:
        img = b.get("imagem_base64", "")
        if not img.startswith("data:image"):
            b["imagem_base64"] = f"data:image/png;base64,{img.strip()}"

    template = env.get_template("aula_pratica.html")
    return template.render(
        titulo="Relatório de Aula Prática",
        nome_aluno=nome_aluno,
        data_hora=data_formatada,
        biometrias=biometrias
    )


def aula_teorica_para_html(data_json):
    template = env.get_template("aula_teorica.html")

    instrutor_nome = data_json.get("instrutorNome", "N/A")
    instrutor_cpf = data_json.get("cpfInstrutor", "N/A")
    lista_alunos = data_json.get("listaAlunos", [])

    htmls = []

    for aluno_data in lista_alunos:
        biometrias = aluno_data.get("biometrias", [])
        
        # Normaliza as imagens base64
        for b in biometrias:
            img = b.get("imagem_base64", "")
            if img and not img.startswith("data:image"):
                b["imagem_base64"] = f"data:image/png;base64,{img.strip()}"

        context = {
            "titulo": "Relatório de Aula Teórica",
            "instrutor_nome": instrutor_nome,
            "instrutor_cpf": instrutor_cpf,
            "aluno": {
                "nome": aluno_data.get("nome_aluno"),
                "cpf": aluno_data.get("cpf_aluno"),
                "data_hora_aula": aluno_data.get("data_hora_aula", "N/A"),
                "biometrias": biometrias
            }
        }
        html = template.render(context)
        htmls.append(html)

    return htmls
