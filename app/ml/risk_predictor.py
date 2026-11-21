import pandas as pd

def create_training_data():
    data = {
        "files_changed": [
            1, 2, 3, 2, 4,
            5, 8, 10, 7, 12,
            15, 20, 25, 30, 18
        ],
        "lines_added": [
            10, 20, 30, 15, 40,
            100, 200, 300, 250, 400,
            600, 900, 1200, 1500, 800
        ],
        "lines_deleted": [
            2, 5, 10, 3, 8,
            30, 50, 80, 60, 100,
            150, 200, 300, 400, 250
        ],
        "detected_issues": [
            0, 0, 1, 0, 1,
            2, 3, 4, 2, 5,
            6, 8, 10, 12, 9
        ],
        "risk_level": [
            "Low", "Low", "Low", "Low", "Low",
            "Medium", "Medium", "Medium", "Medium", "Medium",
            "High", "High", "High", "High", "High"
        ]
    }

    return pd.DataFrame(data)


from sklearn.ensemble import RandomForestClassifier


def train_risk_model():
    data = create_training_data()

    features = [
        "files_changed",
        "lines_added",
        "lines_deleted",
        "detected_issues"
    ]

    X = data[features]
    y = data["risk_level"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_pr_risk(files_changed, lines_added, lines_deleted, detected_issues):
    model = train_risk_model()

    input_data = pd.DataFrame([{
        "files_changed": files_changed,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "detected_issues": detected_issues
    }])

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    confidence = {
        risk: round(float(probability), 2)
        for risk, probability in zip(model.classes_, probabilities)
    }

    return {
        "predicted_risk": prediction,
        "confidence": confidence
    }

from app.analyzer.code_analyzer import analyze_code


def analyze_pr_risk(code, files_changed, lines_added, lines_deleted):
    code_report = analyze_code(code)

    if not code_report["valid"]:
        return {
            "success": False,
            "message": "Cannot predict risk because the code has syntax errors.",
            "code_analysis": code_report
        }

    detected_issues = code_report["total_issues"]

    risk_report = predict_pr_risk(
        files_changed=files_changed,
        lines_added=lines_added,
        lines_deleted=lines_deleted,
        detected_issues=detected_issues
    )

    return {
        "success": True,
        "code_analysis": code_report,
        "risk_analysis": risk_report
    }