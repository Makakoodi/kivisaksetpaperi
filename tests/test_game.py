import pytest
import random
from src.game import KiviSaksetPaperi


#Testataan pelaajan voittoa
def test_player_wins():
    game = KiviSaksetPaperi()
    result = game.get_winner('kivi', 'sakset')
    assert result == 'Pelaaja voitti!', "Pelaajan pitäisi voittaa kivi vastaab sakset tilanteessa"

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




#uusia testejä tekoälyn toimivuutta varten

#matriisin päivitys joka kierroksen jälkeen
def test_matrix_updated():
    game = KiviSaksetPaperi(degree=5)
    for _ in range(4):
        game.move_history.add_move('kivi')
    game.update_matrix(game.move_history, 'paperi')
    
    move_history_key = tuple(game.move_history.get_last_moves(5))
    assert 'paperi' in game.matrix[move_history_key], "Matriisin pitäisi päivittyä pelaajan viimeksi pelatulla valinnalla."
    assert game.matrix[move_history_key]['paperi'] > 1/3, "Paperin todennnäköisyys pitäisi nousta, kun pelaaja valitsee sen."

#testataan toimiiko tekoäly vaikka aste ei ole vielä 5, tätä testiä pitäisi vielä parantaa
def test_degree():
    game = KiviSaksetPaperi(degree=5)
    for _ in range(2):
        game.move_history.add_move('kivi')
    
    ai_choice = game.get_ai_choice()
    
    assert ai_choice in game.choices, "Tekoälyn pitäisi silti tehdä päätös, vaikka liikehistoria ei yllä asteisiin (5)."

#testataan reagoiko tekoäly jos pelaaja valitsee pelkästään kiveä
def test_repeat_kivi():
    game = KiviSaksetPaperi(degree=5)

    for _ in range(10):
        game.move_history.add_move('kivi')
        game.update_matrix(game.move_history, 'kivi')

    ai_choice = game.get_ai_choice()
    
    assert ai_choice == 'paperi', "Tekoälyn pitäisi valita paperi voittaakseen."

#testataan ettei tekoäly tee satunnaisia valintoja kun aste on saavutettu
def test_ai_random():
    game = KiviSaksetPaperi(degree=10)
    
    #simuloidaan satunnaisesti pelaajan liikkeitä
    for move in ['kivi', 'sakset', 'paperi', 'kivi', 'paperi']:
        game.move_history.add_move(move)
    game.update_matrix(game.move_history, 'sakset')
    
    ai_choice = game.get_ai_choice()

    assert ai_choice != random.choice(game.choices), "Tekoälyn ei pitäisi tehdä satunnaista valintaajos historia on riittämätön"