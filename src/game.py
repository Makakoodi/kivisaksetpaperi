import random
from collections import defaultdict


class KiviSaksetPaperi:
    def __init__(self, max_degree=3):
        self.choices = ['kivi', 'sakset', 'paperi']
        self.player_score = 0
        self.ai_score = 0   
        self.total_ai_score = 0
        self.tie = 0    
        self.max_degree = max_degree  #maksimi markovin ketju
        self.current_degree = 1  #markovin ketju alkaa 1 asteella
        self.move_history = MoveHistory(degree=self.current_degree)  #deque korvattu omalla MoveHistory luokalla alempana
        self.rounds_played = 0
        self.degrees_performance = {i: {'wins': 1, 'rounds': 2} for i in range(1, self.max_degree + 1)}
        

    def adjust_degree(self):
        #5 kierroksen välein tarkistus
        if self.rounds_played > 0 and self.rounds_played % 5 == 0:
            #lasketaan tekoälyn voittoprosentti viimeisten 5 kierroksen ajalta
            ai_win_rate = (self.ai_score / 5)
            print(f"DEBUG: AI winrate viimeisten 5 kierroksen aikana = {ai_win_rate:.2f}")
            
            #päivitetään nykyisen asteen winrate viimeisten 5 kierroksen tulosten mukaan
            self.degrees_performance[self.current_degree]['wins'] += self.ai_score
            self.degrees_performance[self.current_degree]['rounds'] += 5
            
            #päivitetään winrate suoraan
            self.degrees_performance[self.current_degree]['winrate'] = self.degrees_performance[self.current_degree]['wins'] / max(1, self.degrees_performance[self.current_degree]['rounds'])
            
            
            self.ai_score = 0
            
            #testausvaihe pelin alussa (15 kierrosta)
            if self.rounds_played <= 15:
                if self.rounds_played < 15:
                    next_degree = (self.current_degree % self.max_degree) + 1
                    print(f"\nDEBUG: Kokeillaan seuraavaa astetta: {next_degree}.\n")
                    self.current_degree = next_degree
                    self.move_history.degree = self.current_degree
                
            else:
                #parhaimman asteen arviointi
                best_degree = max(self.degrees_performance, key=lambda d: (self.degrees_performance[d]['wins'] / max(1, self.degrees_performance[d]['rounds'])))
                
                #asteen vaihto jos tarvitsee
                best_winrate = self.degrees_performance[best_degree]['wins'] / max(1, self.degrees_performance[best_degree]['rounds'])
                current_winrate = self.degrees_performance[self.current_degree]['wins'] / max(1, self.degrees_performance[self.current_degree]['rounds'])
                
                if best_degree != self.current_degree or current_winrate < best_winrate:
                    print(f"\nDEBUG: Paras aste löydetty: {best_degree} ({best_winrate:.2f} winrate), vaihdetaan siihen.\n")
                    self.current_degree = best_degree
                    self.move_history.degree = self.current_degree
                else:
                    print(f"DEBUG: Nykyinen aste {self.current_degree} pysyy käytössä, koska sen winrate ({current_winrate:.2f}) on yhtä hyvä tai parempi.")

        

    
    def display_transition_matrix(self):
        #matriisin tulostus testausta varten
        
        print("\nDEBUG: Current Transition Matrix:")
        for move, transitions in self.move_history.transition_matrix.items():
            print(f"  {move}: {transitions}")
        print()

    def get_ai_choice(self):
        #ennustetaan seuraava siirto
        predicted_move = self.move_history.predict_next_move()
        
         #valitaan siirto, joka voittaa ennustetun pelaajan siirron
        if predicted_move == 'kivi':  #jos ennustettu siirto on 'kivi'
            return 'paperi'  #paperi voittaa kiven
        elif predicted_move == 'sakset':  #jos ennustettu siirto on 'sakset'
            return 'kivi'  #kivi voittaa sakset
        else:  #jos ennustettu siirto on 'paperi'
            return 'sakset'  #sakset voittaa paperin

    def get_winner(self, player, ai):
        #voittajan valinnan logiikka
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
            self.total_ai_score += 1
            return 'Tietokone voitti!'

  

    def play(self):
        print("Tämä on kivi, sakset ja paperi!")
        while True:
            player_choice = input("Valitse kivi, paperi, tai sakset (Kirjoita 'lopeta' poistuaksesi ohjelmasta): ").lower()
            if player_choice == 'lopeta':
                print(f"Tulokset: - Pelaaja: {self.player_score}, - Tietokone: {self.total_ai_score}")
                break
            

            if player_choice not in self.choices:
                print("Väärä syöte, kokeile uudestaan!")
                continue

            ai_choice = self.get_ai_choice()
            print(f"Tietokone valitsi: {ai_choice}!")

            result = self.get_winner(player_choice, ai_choice)
            print(result)
            print(f"Tulokset: - Pelaaja: {self.player_score}, - Tietokone: {self.total_ai_score}, - Tasapelit: {self.tie}")

            #päivitetään siirtohistoria ja matriisi
            self.move_history.add_move(player_choice)
            self.display_transition_matrix()

            if result == 'Tietokone voitti!':
                self.degrees_performance[self.current_degree]['wins'] += 1
            
            self.degrees_performance[self.current_degree]['rounds'] += 1
            self.rounds_played += 1
            self.adjust_degree()

#MoveHistory luokka            
class MoveHistory:
    def __init__(self, degree=1):
        self.history = []
        self.degree = degree
        #siirtymämatriisi, jossa yhdistetään edellisten siirtojen kombinaatiot
        self.transition_matrix = defaultdict(lambda: {'kivi': 0, 'paperi': 0, 'sakset': 0})


    def add_move(self, move):        
        if len(self.history) >= self.degree:
            prev_moves = tuple(self.history[-self.degree:])
            self.transition_matrix[prev_moves][move] += 1

        self.history.append(move)

    def predict_next_move(self):   
        prev_moves = tuple(self.history[-self.degree:])
        matrix_weights = self.transition_matrix[prev_moves]
        weight_sum = sum(matrix_weights.values())

        if len(self.history) < self.degree:
            return random.choice(['kivi', 'paperi', 'sakset'])        
        if weight_sum == 0:
            #valitaan satunnaisesti ilman historiaa   
            return random.choice(['kivi', 'paperi', 'sakset'])  

        weights = {move: count / weight_sum for move, count in matrix_weights.items()}

        moves, probs = zip(*weights.items())
        """ eli käytännössä moves = ('kivi', 'paperi', 'sakset')
                            probs = (0.4, 0.3, 0.3) """
        return random.choices(moves, probs)[0]
            

if __name__ == "__main__":
    game = KiviSaksetPaperi(max_degree=3) #annetaan markovin ketjun maksimiasteeksi 3
    game.play()