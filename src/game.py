import random
from collections import defaultdict, deque

class KiviSaksetPaperi:
    def __init__(self, max_degree=3):
        self.choices = ['kivi', 'sakset', 'paperi']
        self.player_score = 0
        self.ai_score = 0
        self.tie = 0
        self.max_degree = max_degree
        self.move_history = MoveHistory(max_degree)

    def get_ai_choice(self):
        #ennustetaan seuraava liike kaikkien asteiden perusteella ja valitaan parhaan probabiliteetin omaava liike.
        
        predicted_move, best_degree, best_probability = self.move_history.predict_next_move()

        print(f"DEBUG: Paras aste: {best_degree}, ennustettu siirto: {predicted_move}, todennäköisyys: {best_probability:.2f}")
        
        if predicted_move == 'kivi':
            return 'paperi'
        elif predicted_move == 'sakset':
            return 'kivi'
        elif predicted_move == 'paperi':
            return 'sakset'

        return random.choice(self.choices)

    def get_winner(self, player, ai):
        if player == ai:
            self.tie += 1
            return "Tasapeli!"
        elif (player == 'kivi' and ai == 'sakset') or \
             (player == 'sakset' and ai == 'paperi') or \
             (player == 'paperi' and ai == 'kivi'):
            self.player_score += 1
            return 'Pelaaja voitti!'
        else:
            self.ai_score += 1
            return 'Tietokone voitti!'

    def play(self):
        print("Tämä on kivi, sakset ja paperi!")
        while True:
            player_choice = input("Valitse kivi, paperi, tai sakset (Kirjoita 'lopeta' poistuaksesi ohjelmasta): ").lower()
            if player_choice == 'lopeta':
                print(f"Tulokset: - Pelaaja: {self.player_score}, - Tietokone: {self.ai_score}, - Tasapelit: {self.tie}")
                break

            if player_choice not in self.choices:
                print("Väärä syöte, kokeile uudestaan!")
                continue

            ai_choice = self.get_ai_choice()
            print(f"Tietokone valitsi: {ai_choice}!")

            result = self.get_winner(player_choice, ai_choice)
            print(result)

            self.move_history.add_move(player_choice)
            self.move_history.display_transition_matrices()  #DEBUG matriisin näyttö

class MoveHistory:
    def __init__(self, max_degree):
        self.max_degree = max_degree
        self.history = deque(maxlen=max_degree)
        self.transition_matrices = {
            degree: defaultdict(lambda: defaultdict(int)) for degree in range(1, max_degree + 1)
        }

    def add_move(self, move):
        #lisätään uusi liike matriiseihin
        self.history.append(move)
        for degree in range(1, self.max_degree + 1):
            if len(self.history) >= degree:
                sequence = tuple(self.history)[-degree:]
                if degree == 1:
                    # 1-asteinen tallentaa yksittäisen siirron
                    self.transition_matrices[degree][sequence[0]][move] += 1
                else:
                    # Muut asteet tallentavat sekvenssejä
                    self.transition_matrices[degree][tuple(sequence[:-1])][sequence[-1]] += 1

    def predict_next_move(self):
        #ennustetaan seuraava liike tarkistamalla kaikki asteet ja valitsemalla paras probabiliteetti
        
        best_move = None
        best_probability = 0
        best_degree = None

        for degree in range(1, self.max_degree + 1):
            if len(self.history) < degree:
                continue  #skipataan asteet ilman riittävää historiaa

            sequence = tuple(self.history)[-degree:]     #haetaan pelaajan viimeiset siirrot asteen mukaisesti
            matrix = self.transition_matrices[degree]   #haetaan nykyiselle asteelle siirtomatriisi

            if degree == 1:
                key = sequence[0]
            else:
                key = sequence[:-1]

            if key not in matrix:
                continue  #skipataan jos sekvenssiä ei ole tallennettu

            transitions = matrix[key]
            total = sum(transitions.values())
            probabilities = {move: count / total for move, count in transitions.items()}

            #valitaan korkein todennäköisyys
            most_likely_move, probability = max(probabilities.items(), key=lambda item: item[1])
            if probability > best_probability:
                best_probability = probability
                best_move = most_likely_move
                best_degree = degree

        if best_move:
            return best_move, best_degree, best_probability
        
        return random.choice(['kivi', 'paperi', 'sakset']), None, 0.0
    
    def display_transition_matrices(self):
        #DEBUG näyttää matriisin joka kierroksen jälkeen jotta nähdään päivittyykö uudet parit
        print("\nDEBUG: Transition Matrices:")
        for degree, matrix in self.transition_matrices.items():
            print(f" Degree {degree}:")
            for key, transitions in matrix.items():
                print(f"   {key} -> {dict(transitions)}")

if __name__ == "__main__":
    game = KiviSaksetPaperi(max_degree=3)
    game.play()
