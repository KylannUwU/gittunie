from flask import Flask, request
import os

app = Flask(__name__)

plans = []  # Lista dinámica de planes
current_plan_index = -1  # Índice del plan actual "En pantalla"
call_participants = []  # Lista para almacenar los participantes de la llamada (pares de nombre y emote)
DEFAULT_CALL = {"name": "Solita", "emote": "nephuLurk"}  # Valor predeterminado para la llamada

@app.route("/addplan")
def add_plan():
    global plans
    new_plans = request.args.get("plan", "").strip()
    if new_plans:
        items = [item.strip() for item in new_plans.split(",") if item.strip()]
        plans.extend(items)
    return "Planes añadidos nephuJammies"


# Ruta para establecer un plan como "En pantalla"
@app.route("/setplan")
def set_plan():
    global current_plan_index
    plan_to_set = request.args.get("plan", "").strip().lower()
    for i, plan in enumerate(plans):
        if plan.lower() == plan_to_set:
            current_plan_index = i
            return f"'{plans[i]}' En pantalla nephuo7"
    return "Plan no encontrado nephuThink"


# Ruta para resetear todos los planes
@app.route("/resetplan")
def reset_plan():
    global plans, current_plan_index
    plans.clear()
    current_plan_index = -1
    return "Planes reiniciados nephuComfy"
    
# Ruta para eliminar un plan específico por nombre
@app.route("/removeplan")
def remove_specific_plans():
    global current_plan_index

    plans_to_remove_raw = request.args.get("plan", "")
    if not plans_to_remove_raw:
        return "No se especificaron planes para remover."

    plans_to_remove = [p.strip().lower() for p in plans_to_remove_raw.split(",") if p.strip()]
    removed_plans = []

    # Iteramos sobre una copia para evitar problemas al modificar la lista mientras iteramos
    i = 0
    while i < len(plans):
        plan_lower = plans[i].lower()
        if plan_lower in plans_to_remove:
            removed = plans.pop(i)
            removed_plans.append(removed)
            # Ajustar índice actual si es necesario
            if current_plan_index == i:
                current_plan_index = -1
            elif current_plan_index > i:
                current_plan_index -= 1
            # No incrementamos i porque la lista se achicó
        else:
            i += 1

    if removed_plans:
        return f"Planes removidos: {', '.join(removed_plans)}"
    else:
        return "Plan no existente nephuThink"



# Ruta para obtener el mensaje de los planes en formato bonito
@app.route("/plan")
def get_plan():
    user = request.args.get("user", "alguien")
    parts = []

    for i, plan in enumerate(plans):
        if i < current_plan_index:
            parts.append(f"{plan} [✓]")
        elif i == current_plan_index:
            parts.append(f"{plan} [En pantalla ]")
        else:
            parts.append(plan)

    dynamic_part = " ➜ ".join(parts) + " ➜ " if parts else ""
    return f"nephuPats Plan nephuUwu  [ Plan de Hoy ] ➜ {dynamic_part}Mucho Más! nephuPls @{user}"

@app.route("/addcall", methods=['GET'])
def add_call():
    entries = request.args.get("entries", "").split()  # Separar por espacios
    if len(entries) % 2 != 0:
        return "Numero incorrecto de elementos, recuerda enviar siempre un Nombre sin espacios y un Emote por participante nephuDerp"

    for i in range(0, len(entries), 2):
        name = entries[i]
        emote = entries[i + 1]
        call_participants.append({"name": name , "emote": emote})
    
    return f"Participantes añadidos: {' , '.join([f'{name} {emote}' for name, emote in zip(entries[::2], entries[1::2])])}"


@app.route("/removecall", methods=['GET'])
def remove_call():
    names = request.args.get("entries", "").split()  # Separar por espacios (solo nombres)
    removed = []
    
    # Convertir los nombres a minúsculas para comparar sin importar mayúsculas/minúsculas
    names = [name.lower() for name in names]
    
    for name in names:
        # Buscar y remover los participantes que coincidan solo con el nombre (ignorando mayúsculas/minúsculas)
        for participant in call_participants[:]:
            if participant['name'].lower() == name:
                call_participants.remove(participant)
                removed.append(f"{name} {participant['emote']}")
    
    # Si no quedan participantes, agregar el valor predeterminado
    if not call_participants:
        return f"{DEFAULT_CALL['name']} {DEFAULT_CALL['emote']} " 
    
    if removed:
        return f"Participantes removidos: {' , ' .join(removed)} "
    else:
        return "No se encontraron participantes para remover."





# Ruta para resetear la llamada
@app.route("/resetcall", methods=['GET'])
def reset_call():
    call_participants.clear()
    return f"!call reiniciado nephuComfy"

# Ruta para obtener la información de la llamada
@app.route("/call", methods=['GET'])
def get_call():
    if not call_participants:
        return f"{DEFAULT_CALL['name']} {DEFAULT_CALL['emote']}"
    
    call_info = " ".join([f"{p['name']} {p['emote']}" for p in call_participants])
    return call_info



# Inicia Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
