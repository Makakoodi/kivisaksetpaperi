import pytest
import random
from src.game import KiviSaksetPaperi


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




#tekoälyn testausta

#matriisin päivitys joka kierroksen jälkeen
def test_matrix_updated():
    game = KiviSaksetPaperi(degree=2)
    
    # Lisää siirtohistoria
    game.move_history.add_move('kivi')
    game.move_history.add_move('kivi')   
    game.move_history.add_move('paperi')
    game.move_history.add_move('paperi')
    game.move_history.add_move('sakset')
    game.move_history.add_move('paperi')
    game.move_history.add_move('sakset')

    
    move_history_key = tuple(game.move_history.history[-2:])
    
    assert 'paperi' in game.move_history.transition_matrix[move_history_key], "Matriisin pitäisi päivittyä pelaajan viimeksi pelatulla valinnalla."
    assert game.move_history.transition_matrix[move_history_key]['paperi'] > 1/3, "Paperin todennäköisyyden pitäisi nousta, kun pelaaja valitsee sen."

#testataan toimiiko tekoäly vaikka aste ei ole vielä 5, tätä testiä pitäisi vielä parantaa
def test_degree():
    game = KiviSaksetPaperi(degree=3)
    game.move_history.add_move('kivi')
    game.move_history.add_move('sakset')
    
    ai_choice = game.get_ai_choice()
    
    assert ai_choice in game.choices, "Tekoälyn pitäisi silti tehdä päätös, vaikka liikehistoria ei yllä asteisiin."

#testataan reagoiko tekoäly jos pelaaja valitsee pelkästään kiveä
def test_repeat_kivi():
    game = KiviSaksetPaperi(degree=5)
    for _ in range(10):
        game.move_history.add_move('kivi')
        
    ai_choice = game.get_ai_choice()    
    assert ai_choice == 'paperi', "Tekoälyn pitäisi valita paperi voittaakseen."

#testataan ettei tekoäly tee satunnaisia valintoja kun aste on saavutettu
def test_ai_not_random_when_history_sufficient():
    game = KiviSaksetPaperi(degree=2)
    
    # Simuloidaan pelaajan liikkeitä
    game.move_history.add_move('kivi')
    game.move_history.add_move('kivi')
    game.move_history.add_move('kivi')
    game.move_history.add_move('kivi')
    
    # Ennusta siirto
    ai_choice = game.get_ai_choice()
    
    assert ai_choice == 'paperi', "Tekoälyn pitäisi valita paperi voittaakseen kiven."

def test_high_degree_markov_chain():
    game = KiviSaksetPaperi(degree=3)
    
    #simuloidaan pelaajan valintoja
    moves = ['kivi', 'paperi', 'sakset', 'kivi', 'paperi', 'sakset']
    for move in moves:
        game.move_history.add_move(move)
    
    #ennusta seuraava siirto
    ai_choice = game.get_ai_choice()
    
    
    assert ai_choice in game.choices, "Tekoälyn valinnan tulee olla yksi validista vaihtoehdoista."
