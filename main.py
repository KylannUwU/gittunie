from flask import Flask, request

app = Flask(__name__)

plans = []  # Lista dinámica de planes

# Ruta para agregar un plan
@app.route("/addplan")
def add_plan():
    new_plan = request.args.get("plan", "")  # Obtiene el nuevo plan
    if new_plan:
        plans.append(new_plan)  # Lo agrega al final de la lista
    return "Plan añadido."

# Ruta para remover el último plan
@app.route("/removeplan")
def remove_plan():
    if plans:
        removed = plans.pop()  # Elimina el último plan
        return f"Plan removido: {removed}"
    return "No hay planes para remover."

# Ruta para resetear los planes
@app.route("/resetplan")
def reset_plan():
    plans.clear()  # Limpia la lista de planes
    return "Plan reiniciado."

# Ruta para obtener los planes y mostrar el formato adecuado
@app.route("/plan")
def get_plan():
    user = request.args.get("user", "alguien")  # Nombre del usuario, por defecto es "alguien"

    parts = []  # Lista para almacenar las partes del mensaje de los planes

    # Añadir los planes anteriores con la palomita [ ✔️ ]
    if len(plans) > 1:
        for plan in plans[:-1]:  # Excluye el último plan
            parts.append(f"{plan} [ ✔️  ]")
    
    # Añadir el último plan con [En pantalla]
    if len(plans) > 0:
        parts.append(f"{plans[-1]} [En pantalla ]")

    # Crear la parte dinámica del mensaje
    dynamic_part = " ➜ ".join(parts) + " ➜ " if parts else ""
    return f" nephuPats Plan nephuUwu  [ Plan de Hoy ] ➜ {dynamic_part}Mucho Más! nephuPls  @{user}"

# Inicia Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
