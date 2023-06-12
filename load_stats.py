from pathlib import Path
class LoadFile:
    def __init__(self, ai_game):
        self.stats = ai_game.stats
        self.path = Path('records/score.txt')
        if not self.path.exists():
            self.path.touch()

    def save_score(self):
        score_str = str(self.stats.high_score)
        self.path.write_text(score_str)

    def load_score(self):
        score = self.path.read_text()
        print(score)
        self.stats.high_score = float(score)
