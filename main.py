from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

def schedule_meetings(data):
    schedule = []
    buffer_time = timedelta(minutes=5)
    available_slots = {}

    for row in data:
        school_id = row['School ID']
        preferences = [row['OPT 1'], row['OPT 2'], row['OPT 3']]
        duration = timedelta(minutes=row['Duration'])

        assigned = False
        for pref in preferences:
            slot_start = datetime.strptime(pref, '%Y-%m-%d %H:%M')
            slot_end = slot_start + duration + buffer_time

            if slot_start not in available_slots or available_slots[slot_start] <= slot_start:
                available_slots[slot_start] = slot_end
                schedule.append({
                    'title': f'School {school_id}',
                    'start': slot_start.isoformat(),
                    'end': slot_end.isoformat(),
                })
                assigned = True
                break

        if not assigned:
            # Handle conflicts (basic fallback)
            pass

    return schedule

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    schedule = schedule_meetings(data)
    return jsonify(schedule)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)