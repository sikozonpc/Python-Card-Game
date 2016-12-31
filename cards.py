#Deck
deck = []

def makeDeck():

    suits = ["Spades","Diamonds","Hearths","Clubs"]
    
    for suit in suits:
        for value in range(2,14):
            if value == 11:
                a = "Jacks"
                deck.append(suit +" of "+a)
            elif value == 12:
                a = "Queens"
                deck.append(suit +" of "+a)
            elif value == 13:
                a = "Kings"
                deck.append(suit +" of "+a)
            else:
                deck.append(str(value) +" of "+ suit )
    deck.append("Ace")
    deck.append("Ace")
    





