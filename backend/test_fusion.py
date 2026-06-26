from core.fusion_engine import FusionEngine

prophet_result = {

    "prediction": 1720000,

    "confidence": 94,

    "mae": 24000

}

xgb_result = {

    "prediction": 1695000,

    "confidence": 91,

    "mae": 18000

}

lstm_result = {

    "prediction": 1713000,

    "confidence": 89,

    "mae": 21000

}

engine = FusionEngine()

result = engine.combine(

    prophet_result,

    xgb_result,

    lstm_result,

    "Stable"

)

print(result)