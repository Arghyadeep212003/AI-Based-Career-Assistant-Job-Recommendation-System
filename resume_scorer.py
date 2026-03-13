import re

class ResumeScorer:

    def __init__(self):

        self.skills = [
            "python","java","sql","machine learning","deep learning",
            "data science","django","flask","react",
            "html","css","javascript","git"
        ]

        self.education = [
            "bachelor","master","b.tech","m.tech",
            "degree","university","college"
        ]

        self.experience = [
            "experience","internship","project",
            "developed","worked","designed"
        ]

        self.certifications = [
            "certificate","certification","coursera",
            "udemy","aws","google"
        ]

    def count(self, text, words):
        return sum(1 for w in words if w in text)

    def score_resume(self, text):

        text = text.lower()

        score = (
            self.count(text, self.skills) * 4 +
            self.count(text, self.education) * 5 +
            self.count(text, self.experience) * 5 +
            self.count(text, self.certifications) * 3
        )

        return min(score, 100)
