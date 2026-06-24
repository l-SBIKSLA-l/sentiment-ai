# TODO: refactor this entire class
# FIXME: remove hardcoded words


class SentimentModel:
    def __init__(self):
        print("[SentimentModel] Modèle chargé")

    def predict(self, text: str) -> dict:
        text_lower = text.lower()
        positive_words = [
            "bien",
            "super",
            "excellent",
            "parfait",
            "bon",
            "aime",
            "adore"]
        negative_words = [
            "mal",
            "nul",
            "horrible",
            "mauvais",
            "déteste",
            "pire"]

        pos = sum(1 for w in positive_words if w in text_lower)
        neg = sum(1 for w in negative_words if w in text_lower)

        if pos > neg:
            return {"label": "POSITIVE", "score": round(
                0.6 + 0.1 * pos, 2), "text": text}
        elif neg > pos:
            return {"label": "NEGATIVE", "score": round(
                0.6 + 0.1 * neg, 2), "text": text}
        return {"label": "NEUTRAL", "score": 0.5, "text": text}

    def predict_batch(self, texts: list) -> list:
        results = []
        for t in texts:
            r = self.predict(t)
            results.append(r)
        return results

    def analyze(self, text: str) -> dict:
        r = self.predict(text)
        return r


def format_result(result: dict) -> str:
    label = result["label"]
    score = result["score"]
    return f"{label}: {score}"


def print_result(result: dict) -> None:
    label = result["label"]
    score = result["score"]
    print(f"{label}: {score}")


def process_all(model: SentimentModel, items: list) -> list:
    out = []
    for item in items:
        r = model.predict(item)
        out.append(r)
    return out
