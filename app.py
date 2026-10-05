from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='.')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:1.5b')

SYSTEM = '''You are AI Garden Buddy, a practical gardening assistant. Give simple, safe, beginner-friendly advice. Focus on outdoor actions. Do not claim certainty about plant diseases. When information is missing, state assumptions. Keep responses concise and actionable.'''

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.post('/api/garden-plan')
def garden_plan():
    data = request.get_json(force=True)
    city = data.get('city', 'Unknown')
    month = data.get('month', 'current month')
    space = data.get('space', 'balcony')
    sunlight = data.get('sunlight', 'partial sun')
    experience = data.get('experience', 'beginner')
    goal = data.get('goal', 'easy vegetables and herbs')
    prompt = f'''Create a garden plan for:
City/region: {city}
Month/season: {month}
Growing space: {space}
Sunlight: {sunlight}
Experience: {experience}
Goal: {goal}

Return exactly these sections:
1. PLANTS: 5 suitable beginner-friendly plants, each with a one-line reason.
2. THIS WEEK: 5 outdoor tasks with checkboxes.
3. WATERING: simple guidance.
4. SUNLIGHT: simple guidance.
5. TIPS: 3 practical tips.
6. WARNING: one short note about checking local frost/heat conditions and plant labels.
Use plain text, no markdown tables.'''
    try:
        r = requests.post(OLLAMA_URL, json={
            'model': MODEL,
            'system': SYSTEM,
            'prompt': prompt,
            'stream': False,
            'options': {'temperature': 0.4}
        }, timeout=90)
        r.raise_for_status()
        answer = r.json().get('response', '').strip()
        return jsonify({'ok': True, 'answer': answer, 'model': MODEL})
    except Exception as e:
        fallback = f'''PLANTS
1. Coriander — quick and beginner friendly.
2. Mint — grows well in containers; keep it contained.
3. Basil — useful for a sunny spot.
4. Radish — fast-growing and suitable for containers.
5. Spinach — a good cool-season leafy crop.

THIS WEEK
☐ Check the soil before watering.
☐ Remove dead or yellow leaves.
☐ Give plants the sunlight they need.
☐ Check the underside of leaves for pests.
☐ Spend 15 minutes observing and caring for your plants.

WATERING
Water when the top layer of soil feels dry; avoid keeping containers waterlogged.

SUNLIGHT
Use your available {sunlight} and place plants according to their light needs.

TIPS
1. Start small with 2–5 plants.
2. Use pots with drainage holes.
3. Label each plant with its sowing date.

WARNING
Local weather and frost dates vary, so confirm conditions for {city} before planting sensitive crops.

AI connection is unavailable right now. Start Ollama and try again for a personalized local-AI plan.'''
        return jsonify({'ok': False, 'answer': fallback, 'error': str(e)})

@app.post('/api/outdoor-mission')
def outdoor_mission():
    data = request.get_json(force=True)
    minutes = data.get('minutes', 20)
    prompt = f'''Create one outdoor gardening mission that takes about {minutes} minutes. Give a title, 3 to 5 actions, and one observation to record. The user should spend most of the time away from the screen.'''
    try:
        r = requests.post(OLLAMA_URL, json={'model': MODEL, 'system': SYSTEM, 'prompt': prompt, 'stream': False}, timeout=60)
        r.raise_for_status()
        return jsonify({'ok': True, 'answer': r.json().get('response','').strip(), 'model': MODEL})
    except Exception:
        return jsonify({'ok': False, 'answer': f'''TODAY'S OUTDOOR MISSION\n\nSpend {minutes} minutes outside.\n\n☐ Check soil moisture for your plants.\n☐ Remove one dead leaf or weed.\n☐ Observe one insect, bird, or new leaf.\n☐ Write down one thing you noticed.\n\nYour goal: spend less time on the screen and more time in the garden.'''} )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
