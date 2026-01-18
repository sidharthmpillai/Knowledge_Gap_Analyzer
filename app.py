from flask import Flask, request, jsonify
from skills_data import ROLE_SKILLS
from gap_analyzer import analyze_gap
from roadmap import generate_roadmap

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    user_skills = data.get("user_skills", [])
    target_role = data.get("target_role", "")

    result = analyze_gap(user_skills, target_role, ROLE_SKILLS)
    result["roadmap"] = generate_roadmap(result["missing_skills"])

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

from roadmap import ROADMAP

def generate_roadmap(missing_skills):
    roadmap = []
    for skill in missing_skills:
        if skill.lower() in ROADMAP:
            roadmap.append({
                "skill": skill,
                "suggestion": ROADMAP[skill.lower()]["suggestion"],
                "links": ROADMAP[skill.lower()]["links"]
            })
        else:
            roadmap.append({
                "skill": skill,
                "suggestion": "No specific suggestion available",
                "links": []
            })
    return roadmap
