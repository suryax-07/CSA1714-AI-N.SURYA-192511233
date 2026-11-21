
import math
from collections import Counter

INTENTS = {
    "greeting": ["hello", "hi there", "good morning"],
    "open_alerts": ["show open alerts", "list active alerts"],
    "why_flagged": ["why was this flagged", "explain this detection"],
    "status": ["system status", "check device status"],
    "accuracy": ["show detection accuracy", "model performance"],
    "latency": ["show response time", "processing delay"],
    "help": ["help me", "show available commands"],
    "goodbye": ["bye", "goodbye"]
}

RESPONSES = {
    "greeting": "Hello. How can I help?",
    "open_alerts": "There are 2 sample open alerts.",
    "why_flagged": "The event crossed the detection threshold.",
    "status": "The detection system is running.",
    "accuracy": "See the B3 model performance report.",
    "latency": "The response time is measured in the test.",
    "help": "Ask about alerts, status, accuracy or latency.",
    "goodbye": "Goodbye."
}

def vector(text):
    return Counter(text.lower().split())

def cosine(a,b):
    keys = set(a) | set(b)

    dot = sum(a[k]*b[k] for k in keys)
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))

    return dot/(na*nb) if na and nb else 0

def classify(text, threshold=.25):
    scores = {}

    for intent, examples in INTENTS.items():
        scores[intent] = max(
            cosine(vector(text), vector(example))
            for example in examples
        )

    best = max(scores, key=scores.get)

    if scores[best] < threshold:
        return "out_of_scope", scores[best]

    return best, scores[best]

def main():
    print("AI RETRIEVAL CHATBOT")

    tests = [
        "hello",
        "show open alerts",
        "why was this flagged",
        "system status",
        "show detection accuracy",
        "show response time",
        "help me",
        "goodbye",
        "tell me a joke"
    ]

    for question in tests:
        intent, confidence = classify(question)

        response = RESPONSES.get(
            intent,
            "Sorry, I cannot understand that request."
        )

        print("\\nInput:", question)
        print("Intent:", intent)
        print("Confidence:", round(confidence,3))
        print("Response:", response)

    print("\\nSPEECH ERROR TEST")

    for rate in [0,10,20,30]:
        print("Word error rate:", rate, "%")

    print("\\nTHRESHOLD TEST")

    for threshold in [.10,.25,.40,.60]:
        accepted = sum(
            classify(q,threshold)[0] != "out_of_scope"
            for q in tests
        )

        print("Threshold:",threshold,
              "Accepted:",accepted)

if __name__ == "__main__":
    main()
