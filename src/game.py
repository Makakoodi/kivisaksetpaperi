import random
from collections import defaultdict


class KiviSaksetPaperi:
    def __init__(self, degree=1):
        self.choices = ['kivi', 'sakset', 'paperi']
        self.player_score = 0
        self.ai_score = 0        
        self.degree = degree #Markovin ketjun aste
        self.move_history = MoveHistory(degree=degree)  #deque korvattu omalla MoveHistory luokalla alempana
        
    
    def display_transition_matrix(self):
        #matriisin tulostus testausta varten
        print("\nCurrent Transition Matrix:")
        for move, transitions in self.move_history.transition_matrix.items():
            print(f"  {move}: {transitions}")
        print()

    def get_ai_choice(self):
        #ennustetaan seuraava siirto
        predicted_move = self.move_history.predict_next_move()
        
         # Valitaan siirto, joka voittaa ennustetun pelaajan siirron
        if predicted_move == 'kivi':  # Jos ennustettu siirto on 'kivi'
            return 'paperi'  # Paperi voittaa kiven
        elif predicted_move == 'sakset':  # Jos ennustettu siirto on 'sakset'
            return 'kivi'  # Kivi voittaa sakset
        else:  # Jos ennustettu siirto on 'paperi'
            return 'sakset'  # Sakset voittaa paperin

    def get_winner(self, player, ai):
        #voittajan valinnan logiikka
        if player == ai:
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
                print(f"Tulokset: - Pelaaja: {self.player_score}, - Tietokone: {self.ai_score}")
                break
            if player_choice not in self.choices:
                print("Väärä syöte, kokeile uudestaan!")
                continue

            ai_choice = self.get_ai_choice()
            print(f"Tietokone valitsi: {ai_choice}!")

            result = self.get_winner(player_choice, ai_choice)
            print(result)
            print(f"Tulokset: - Pelaaja: {self.player_score}, - Tietokone: {self.ai_score}")

            # Päivitetään siirtohistoria ja matriisi
            self.move_history.add_move(player_choice)
            self.display_transition_matrix()


#MoveHistory luokka            
class MoveHistory:
    def __init__(self, degree=1):
        self.history = []
        self.degree = degree
        #siirtymämatriisi, jossa yhdistetään edellisten siirtojen kombinaatiot
        self.transition_matrix = defaultdict(lambda: {'kivi': 1/3, 'paperi': 1/3, 'sakset': 1/3})


    def add_move(self, move):        
        if len(self.history) >= self.degree:
            #jos käytetään toisen asteen ketjua niin haetaan edellisten siirtojen kombinmaatiot
            prev_moves = tuple(self.history[-self.degree:])
            self.transition_matrix[prev_moves][move] += 1

            #normalisoidaan matriisin rivi, jotta todennäköisyydet summautuvat yhteen
            total = sum(self.transition_matrix[prev_moves].values())
            for choice in self.transition_matrix[prev_moves]:
                self.transition_matrix[prev_moves][choice] /= total

        self.history.append(move)

    def predict_next_move(self):        
        if len(self.history) < self.degree:
            return random.choice(['kivi', 'paperi', 'sakset'])  #jos historiaa ei ole tarpeeksi, valitaan satunnaisesti
        
        prev_moves = tuple(self.history[-self.degree:])
        predicted_move_distribution = self.transition_matrix[prev_moves]
        predicted_move = max(predicted_move_distribution, key=predicted_move_distribution.get)  #valitaan todennäköisin seuraava siirto
        
        return predicted_move
            

if __name__ == "__main__":
    game = KiviSaksetPaperi(degree=3) #annetaan markovin ketjun asteeksi 10 niinkuin aiheenvalinnan linkissä
    game.play()
