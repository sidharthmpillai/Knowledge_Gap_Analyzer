def analyze_gap(user_skills, target_role, role_skills):
    required_skills = role_skills.get(target_role, [])

    user_skills_set = set(skill.lower() for skill in user_skills)
    required_skills_set = set(skill.lower() for skill in required_skills)

    missing_skills = required_skills_set - user_skills_set
    matched_skills = user_skills_set & required_skills_set

    readiness_score = (len(matched_skills) / len(required_skills_set)) * 100

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "readiness_score": round(readiness_score, 2)
    }
