import random

class KiviSaksetPaperi:
    def __init__(self):
        #Konstruktori
        self.choices = ['kivi', 'paperi', 'sakset']
        self.player_score = 0
        self.ai_score = 0
        self.last_player_move = None 


        #Luodaan 3x3 matriisi missä kaikilla vastauksilla on sama todennäköisyys
        self.matrix = {
            'kivi': {'kivi': 1/3, 'paperi': 1/3, 'sakset': 1/3},
            'paperi': {'kivi': 1/3, 'paperi': 1/3, 'sakset': 1/3},
            'sakset': {'kivi': 1/3, 'paperi': 1/3, 'sakset': 1/3}
        }


    def update_matrix(self, prev_move, current_move):        
        #Päivitetään matriisin todennäköisyydet, jotka perustuu aikaisempiin valintoihin
        for move in self.choices:
            self.matrix[prev_move][move] *= 0.9
        #Ylempää ja alempaa arvoa muuttamalla tietokone valitsaa agressiivisemmin
        self.matrix[prev_move][current_move] += 0.1

    

    def get_ai_choice(self):
        #Tietokone valitsee todennäköisyyksiin perustuvan vaihtoehdon
        #Aluksi valinta on satunnainen koska matriisi on koskematon
        if self.last_player_move is None:            
            return random.choice(self.choices)
        else:
            #Ennustetaan matriisin perusteella pelaajan seuraava valinta
            next_move_probs = self.matrix[self.last_player_move]
            
            
            total = sum(next_move_probs.values())
            normalized_probs = [prob / total for prob in next_move_probs.values()]
            predicted_player_move = random.choices(list(next_move_probs.keys()), normalized_probs)

            #Tekoäly valitsee järkevän vaihtoehdon perustuen pelaajan ennustettuun valintaan
            if predicted_player_move == 'kivi':
                return 'paperi'  #Paperi voittaa kiven
            elif predicted_player_move == 'paperi':
                return 'sakset'  #Sakset voittaa paperin
            else:
                return 'kivi'  #Kivi voittaa sakset


    def get_winner(self, player, ai):
        #Voittajan valinta
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


    def display_matrix(self):
        #testi käyttöön jotta voi nähdä matriisin sen hetkisen tilanteen todennäköisyyksille
        print("\nMatriisi tällä hetkellä: ")
        for move, transitions in self.matrix.items():
            print(f"  {move}: {transitions}")
        print()    


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
            
            #matriisin päivitys
            if self.last_player_move is not None:
                self.update_matrix(self.last_player_move, player_choice)
            
            #Testausta varten matriisin tulostus ruudulle
            self.display_matrix()
            
            self.last_player_move = player_choice

if __name__ == "__main__":
    game = KiviSaksetPaperi()
    game.play()
