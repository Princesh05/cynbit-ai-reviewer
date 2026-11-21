from app.ml.risk_predictor import create_training_data
from app.ml.risk_predictor import analyze_pr_risk

def test_training_data():
    data = create_training_data()

    assert len(data) == 15
    assert "risk_level" in data.columns
    assert data["risk_level"].nunique() == 3


from app.ml.risk_predictor import train_risk_model


def test_model_training():
    model = train_risk_model()

    assert model is not None
    assert len(model.classes_) == 3


from app.ml.risk_predictor import predict_pr_risk


def test_pr_risk_prediction():
    result = predict_pr_risk(
        files_changed=20,
        lines_added=900,
        lines_deleted=200,
        detected_issues=8
    )

    assert result["predicted_risk"] in ["Low", "Medium", "High"]
    assert "confidence" in result
    assert len(result["confidence"]) == 3

    assert abs(sum(result["confidence"].values()) - 1.0) < 0.02


    from app.ml.risk_predictor import analyze_pr_risk


def test_analyzer_and_risk_integration():
    code = """
import os

price = 100
discount = 10

print(price)
"""

    result = analyze_pr_risk(
        code=code,
        files_changed=5,
        lines_added=50,
        lines_deleted=10
    )

    assert result["success"] is True
    assert result["code_analysis"]["total_issues"] == 2
    assert result["risk_analysis"]["predicted_risk"] in [
        "Low", "Medium", "High"
    ]