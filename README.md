# 📄 python-report-generator

Gere relatórios em PDF a partir de arquivos JSON com **Flask + WeasyPrint**.  
Este serviço transforma dados como registros de biometrias e aulas em documentos PDF formatados automaticamente.

---

## 🐳 Instalação com Docker

### 🔧 Build da imagem Docker

```bash
docker build -t pdf-generator .
```

### 📦 Salvar e carregar a imagem (opcional)

```bash
docker save pdf-generator -o pdf-generator.tar
docker load -i pdf-generator.tar
```

### 🚀 Rodar o container

```bash
docker run -p 5000:5000 pdf-generator
```

---

## 📤 Como usar a API

### 🔁 Gerar múltiplos relatórios em um único PDF

```bash
curl -X POST http://localhost:5000/generate-multi \
  -F "file=@multi.json" \
  --output relatorios.pdf
```

### 📚 Gerar relatório de aula

```bash
curl -X POST http://localhost:5000/relatorio-aula \
  -F "file=@aula.json" \
  --output relatorio_aula.pdf
```

---

