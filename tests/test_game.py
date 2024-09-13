import pytest
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
