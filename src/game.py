import random
from collections import deque

class KiviSaksetPaperi:
    def __init__(self, degree=4):
        self.choices = ['kivi', 'paperi', 'sakset']
        self.player_score = 0
        self.ai_score = 0
        self.last_player_move = None
        self.degree = degree #Markovin ketjun aste
        self.move_history = MoveHistory(self.degree)  #deque korvattu omalla MoveHistory luokalla alempana
        self.matrix = {}

    def update_matrix(self, move_history, current_move):
        #Päivitetään matriisin todennäköisyydet, jotka perustuu aikaisempiin valintoihin
        move_history_key = tuple(move_history.get_last_moves(self.degree))
        if move_history_key not in self.matrix:
            self.matrix[move_history_key] = {choice: 1/3 for choice in self.choices}
        for move in self.choices:
            self.matrix[move_history_key][move] *= 0.7
        #Ylempää ja alempaa arvoa muuttamalla tietokone valitsaa agressiivisemmin
        self.matrix[move_history_key][current_move] += 0.3

    def get_ai_choice(self):
        #Tietokone valitsee todennäköisyyksiin perustuvan vaihtoehdon
        #atm_degree on apuna, kun peliä ei ole pelattu tarpeeksi monta kierrosta
        atm_degree = self.degree

        while atm_degree > 0:
            move_history_key = tuple(self.move_history.get_last_moves(atm_degree))
            if move_history_key in self.matrix:
                print(f"Aste tällä hetkellä: {atm_degree}")
                next_move_probs = self.matrix[move_history_key]
                total = sum(next_move_probs.values())
                normalized_probs = [prob / total for prob in next_move_probs.values()]
                predicted_player_move = random.choices(list(next_move_probs.keys()), normalized_probs)[0]

                #Tekoäly valitsee järkevän vaihtoehdon perustuen ennustettuun pelaajan valintaan
                if predicted_player_move == 'kivi':
                    return 'paperi'     #Paperi voittaa kiven
                elif predicted_player_move == 'paperi':
                    return 'sakset'     #Sakset voittaa paperin
                else:
                    return 'kivi'       #Kivi voittaa sakset
            atm_degree -= 1

        print("Satunnainen valinta") #testausta varten jos tekoäly valitsee satunnaisesti
        return random.choice(self.choices)

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

            #päivitetään historia ja matriisi
            self.move_history.add_move(player_choice)
            if len(self.move_history) == self.degree:
                self.update_matrix(self.move_history, player_choice)



#MoveHistory luokka            
class MoveHistory:
    def __init__(self, length):
        #length on maximi määrä historiassa säilytettäviä liikkeitä, eli käytännössä Markovin ketjun aste
        self.length = length  
        self.history = []

    def add_move(self, move):
        #jos historia ylittää asteen niin poistetaan vanhin liike ja lisätään uusi
        if len(self.history) >= self.length:
            self.history.pop(0)  

        self.history.append(move)


    def get_last_moves(self, x):
        #palauttaa x määrän liikkeitä historiasta
        if x > len(self.history):
            return self.history  #palauttaa koko historian jos x arvo on isompi kuin historia
        return self.history[-x:]

    def __len__(self):
        return len(self.history)
            

if __name__ == "__main__":
    game = KiviSaksetPaperi(degree=4) #annetaan markovin ketjun asteeksi 10 niinkuin aiheenvalinnan linkissä
    game.play()
