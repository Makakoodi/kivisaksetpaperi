import random

class KiviSaksetPaperi:
    def __init__(self):
        #Konstruktori
        self.choices = ['kivi', 'paperi', 'sakset']
        self.player_score = 0
        self.ai_score = 0

    def get_ai_choice(self):
        #placeholder tekoäly joka palauttaa satunnaisen vastauksen
        return random.choice(self.choices)

    def get_winner(self, player, ai):
        #Voittajan määrittelylogiikka
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
        #Pääfunktio pelille
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

if __name__ == "__main__":
    game = KiviSaksetPaperi()
    game.play()