import pytest
import random
from src.game import KiviSaksetPaperi


""" UI testejä joita ei tarvinnutkaan loppujen lopuksi

#Testataan pelaajan voittoa
def test_player_wins():
    game = KiviSaksetPaperi()
    result = game.get_winner('kivi', 'sakset')
    assert result == 'Pelaaja voitti!', "Pelaajan pitäisi voittaa kivi vastaan sakset tilanteessa"

#Testataan tekoälyn voittoa
def test_ai_wins():
    game = KiviSaksetPaperi()
    result = game.get_winner('sakset', 'kivi')
    assert result == 'Tietokone voitti!', "Tietokoneen pitäisi voittaa sakset vastaan kivi tilanteessa"

#Testataan tasapeliä kivellä
def test_tie_kivi():
    game = KiviSaksetPaperi()
    result = game.get_winner('kivi', 'kivi')
    assert result == 'Tasapeli!', "Tuloksen pitäisi olla tasapeli jos molemmat valitsevat kiven"

#Testataan tasapeliä saksilla
def test_tie_sakset():
    game = KiviSaksetPaperi()
    result = game.get_winner('sakset', 'sakset')
    assert result == 'Tasapeli!', "Tuloksen pitäisi olla tasapeli jos molemmat valitsevat sakset"

#Testataan tasapeliä paperilla
def test_tie_paperi():
    game = KiviSaksetPaperi()
    result = game.get_winner('paperi', 'paperi')
    assert result == 'Tasapeli!', "Tuloksen pitäisi olla tasapeli jos molemmat valitsevat paperin"

#Testataan väärää syötettä
def test_invalid_input(monkeypatch):
    game = KiviSaksetPaperi()

    #Simuloidaan syötteet "asd" vääräksi syötteeksi ja sitten "lopeta", jotta ohjelma ei jää looppaamaan   
    monkeypatch.setattr('builtins.input', lambda _:'asd')
    monkeypatch.setattr('builtins.input', lambda _:'lopeta')    
    result = game.play()  
    assert result is None, "Pelin pitäisi käsitellä väärä syöte ja pysähtyä 'lopeta' komennon jälkeen"


#Testataan pelin lopetusta
def test_quit(monkeypatch):
    game = KiviSaksetPaperi()
    
    #Simuloidaan syötettä "lopeta"
    monkeypatch.setattr('builtins.input', lambda _: 'lopeta')    
    result = game.play()
    assert result is None, "Pelin pitäisi loppua 'lopeta' komennon jälkeen"


"""

#tekoälyn testaus


# Testataan, että aste vaihtuu testausvaiheen jälkeen oikein
def test_degree_testphase():
    game = KiviSaksetPaperi(max_degree=3)

    # Simuloidaan 15 kierrosta
    for i in range(15):
        game.move_history.add_move(random.choice(['kivi', 'paperi', 'sakset']))
        game.rounds_played += 1
        game.adjust_degree()

    # Testataan, että asteet on vaihtunu
    assert game.current_degree in [1, 2, 3], "Asteen pitäisi olla yksi sallituista 1, 2 tai 3."
    assert game.rounds_played == 15, "Kierroksia pitäisi olla 15 testausvaiheen jälkeen."

# Testataan, että tekoäly valitsee paperin jos pelaaja valitsee toistuvasti kiveä
def test_ai_repeat_kivi():
    game = KiviSaksetPaperi(max_degree=2)

    # Pelaaja valitsee jatkuvasti 'kivi'
    for _ in range(5):
        game.move_history.add_move('kivi')

    # Testataan, että tekoäly valitsee paperin
    ai_choice = game.get_ai_choice()
    assert ai_choice == 'paperi', "Tekoälyn pitäisi valita paperi voittaakseen pelaajan toistuvan kiven."


# Testataan, että aste vaihtuu oikein pelin aikana
def test_ai_degree_performance():
    game = KiviSaksetPaperi(max_degree=3)

    # Simuloidaan 15 kierrosta, jossa tekoäly voittaa vaihtelevasti
    for i in range(15):
        game.move_history.add_move(random.choice(['kivi', 'paperi', 'sakset']))
        game.rounds_played += 1

        if i % 5 == 0:  #Simuloidaan 5 kierroksen jaksoja
            if i < 10:  #Ensimmäiset 10 kierrosta 
                game.ai_score = 1  #Tekoäly voittaa kerran
            else:  
                game.ai_score = 4  #Tekoäly voittaa neljä kertaa

            game.adjust_degree()

    #Tarkistetaan, että nykyinen aste vastaa parhaan asteen suoritusta
    best_degree = max(game.degrees_performance, key=lambda d: (game.degrees_performance[d]['wins'] / max(1, game.degrees_performance[d]['rounds'])))

    assert game.current_degree == best_degree, f"Tekoälyn asteen pitäisi olla {best_degree}, koska sillä on paras winrate."

    #Varmistetaan, että nykyinen aste on yksi sallituista asteista
    assert game.current_degree in [1, 2, 3], "Tekoälyn asteen pitäisi olla 1, 2 tai 3 pelin edetessä."