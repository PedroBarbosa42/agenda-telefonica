import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
ARQUIVO = Path(__file__).parent / "contatos.json"


def carregar():
    if not ARQUIVO.exists():
        return []
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def salvar(contatos):
    ARQUIVO.write_text(
        json.dumps(contatos, indent=2, ensure_ascii=False), encoding="utf-8"
    )


@app.route("/")
def listar():
    return render_template("listar.html", contatos=carregar())


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        contatos = carregar()
        novo_id = max((c["id"] for c in contatos), default=0) + 1
        contatos.append({
            "id": novo_id,
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form.get("email", ""),
        })
        salvar(contatos)
        return redirect(url_for("listar"))
    return render_template("cadastrar.html")


@app.route("/contato/<int:contato_id>")
def consultar(contato_id):
    contato = next((c for c in carregar() if c["id"] == contato_id), None)
    if contato is None:
        abort(404)
    return render_template("consultar.html", contato=contato)


if __name__ == "__main__":
    app.run(debug=True)