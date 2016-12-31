"""
Card game made only with Tkinter in Python, by Tiago Taquelim Aug/2016;
"""


from tkinter import *
import tkinter.messagebox
import vars as var
import cards as Deck
import sys, random


class Window(object):
    def __init__(self):

        
        self.root = Tk()
        self.root.geometry(("800x600"))
        self.root.title("Card game")
        try:
            self.root.wm_iconbitmap("icon.ico")
        except:
            pass

        self.root.bind("<Escape>" , sys.exit)

        # Creating a menu
        mainMenu = Menu(self.root)
        self.root.config(menu = mainMenu)

        subMenu = Menu(mainMenu, tearoff = 0)
        mainMenu.add_cascade(label = "Rules", command = self.gameRules)
        mainMenu.add_cascade(label = "Help", menu = subMenu)

        subMenu.add_command(label = "Known bugs", command = self.knownBugs)
        subMenu.add_command(label = "Report a bug", command = self.reportBug)
        subMenu.add_separator()
        subMenu.add_command(label = "How to play?", command = self.howToPlay)

        self.root.resizable(False,False)
        self.root['bg'] = var.BACKGROUND

        #Starts the game rules screen...

        self.gameRulesScreen()

        # PRE LOADED FRAMES
        self.frameMenuBar = Frame(self.root, bg = "blue")

        self.frameGame = Frame(self.root)
            #canvas for the game
        self.gameScreen = Canvas(self.frameGame,width=800,height=600,bg="green")




        # Field list (Field is where the cards are played)
        self.field = ["0","0"] # Each for player, and this is the last crad played.


        self.root.mainloop()


    #""" Menu functions """#


    def knownBugs(self):

        newWindow = Toplevel()
        
        newWindow.wm_title("Known bugs")
        text = Label(newWindow, text="""These are the known bugs:
                                > Clicking on the name of the cards to play them don't work.
                                > If play all the cards too fast the bot can't keep up and will not draw.""")
        text.pack(side="top", fill="both", expand=True, padx=100, pady=100)


    def reportBug(self):

        newWindow = Toplevel()
        newWindow.wm_title("Report a bug")

        text = Label(newWindow, text = "Reporting bugs helps the developers to improve the game.")
        self.reportEntry = Entry(newWindow)
        ok = Button(newWindow, text = "Send", command = self.getReport)
        

        text.pack()
        self.reportEntry.pack()
        ok.pack()
        
        
    def getReport(self):
        #Idealy i wanted the player to send this to a online database not to the game folder;
        
        print(">",self.reportEntry.get())
        file = open("report.txt","a")
        file.write("\n" + self.reportEntry.get())

        file.close()
    def howToPlay(self):
        #TODO
        print("Work in progress...")

    def gameRules(self):
        #TODO
        print("Work in progress...")


    def mainMenu(self):
        self.frameRules.destroy()


        self.frameTitle = Frame(self.root, bg = var.BACKGROUND)
        self.frameTitle.pack()
        
        self.start_but = Button(self.frameTitle,text="Start Game",
                                pady= 10,
                                command = self.play,
                                padx = 15,fg='darkblue', bg='ghostwhite', relief=GROOVE)
        self.options_but = Button(self.frameTitle,
                                  text="Options",
                                  command = self.options,
                                  pady= 10,padx = 21,fg='darkblue', bg='ghostwhite', relief=GROOVE)
        self.exit_but = Button(self.frameTitle,
                               text="Exit game",
                               command = self.exit,
                               pady= 10,padx = 17,fg='darkblue', bg='ghostwhite', relief=GROOVE)

        self.developer = Label(self.frameTitle,
                               text = "Made by Tiago Taquelim")


        self.start_but.pack()
        self.options_but.pack()
        self.exit_but.pack()
        self.developer.pack(side = BOTTOM)


    #"""    Game functions     """#


    def status(self):
        #Display cards on deck
        self.cards_on_deck = len(Deck.deck)
        self.gameScreen.create_text((80,520),text = ("Cards left: %i"%self.cards_on_deck,),fill="white",tag="gameStats")
        self.gameScreen.create_text((650,10),text = ("Player %i - %i Computer"%(self.player_points,self.bot_points)),fill="white",tag="gameStats")
        
    def update(self):
        if self.gameRun:
            self.gameScreen.delete("gameStats","pts")
            self.status()
            self.botAI()
            
            if len(Deck.deck) <= 0:
                self.winner()
                self.win = "OVER"

            self.root.after(200, self.update) #increasing this might cause a bug, but increases FPS. (10 is fine)
        else:
            pass
        
    def play(self):
        #This will start the game and some variables.
        
        #Vars
        self.bot_hand = []
        self.player_hand= []
        
        self.player_points = 0
        self.bot_points = 0
        
        self.gameRun = True
        #
        #delete menus
        self.frameTitle.destroy()
        self.frameGame.pack()
        self.gameScreen.pack()
        
        
        #creating scenario
        self.status()
        self.startingCards()
        self.update()

        #binds
        self.gameScreen.tag_bind('card0',"<Button-1>",self.placeCard)
        self.gameScreen.tag_bind('card1',"<Button-1>",self.placeCard)
        self.gameScreen.tag_bind('card2',"<Button-1>",self.placeCard)


    def drawCard(self):

        if len(Deck.deck) <= 3 :
            return

        self.cardDrawn = random.choice(Deck.deck)


        if var.playerDraw:
            self.b = self.player_hand[0] == 0
            self.c = self.player_hand[1] == 0
            self.d = self.player_hand[2] == 0
            if self.b:
                #Card get removed from deck and its added to the hand.
                self.player_hand[0] = self.cardDrawn
                Deck.deck.remove(self.cardDrawn)

                #Drawing card on screen with text for position 0.
                self.gameScreen.create_rectangle((345,420),(445,580),fill="blue",tag="card0",outline="darkblue")
                self.cardText = self.gameScreen.create_text((395,500),text = ("%s"%self.cardDrawn),fill="white",tag="cardText0")

                return

            elif self.c:
                self.player_hand[1] = self.cardDrawn
                Deck.deck.remove(self.cardDrawn)

                #Drawing card on screen with text for position 1.
                self.gameScreen.create_rectangle((345+150,420),(445+150,580),
                                                 fill="blue",tag="card1",outline="darkblue")
                self.cardText = self.gameScreen.create_text((395+150,500),
                                                 text = ("%s"%self.cardDrawn),fill="white",tag="cardText1")

                return


            elif self.d:
                self.player_hand[2] = self.cardDrawn
                Deck.deck.remove(self.cardDrawn)

                #Drawing card on screen with text for position 2.
                self.gameScreen.create_rectangle((345+300,420),(445+300,580),
                                                 fill="blue",tag="card2",outline="darkblue")
                self.cardText = self.gameScreen.create_text((395+300,500),
                                                            text = ("%s"%self.cardDrawn),fill="white",tag="cardText2")

                return


    def botDraw(self):

        if len(Deck.deck) <= 0 :
            return

        else:
            self.cardDrawn0 = random.choice(Deck.deck)
            Deck.deck.remove(self.cardDrawn0)
            if len(Deck.deck) <= 0 :
                return

            self.cardDrawn1 = random.choice(Deck.deck)

            Deck.deck.remove(self.cardDrawn1)
            if len(Deck.deck) <= 0 :
                return

            self.cardDrawn2 = random.choice(Deck.deck)
            Deck.deck.remove(self.cardDrawn2)

            self.bot_hand[0] = self.cardDrawn0

            self.gameScreen.create_rectangle((20+50,5),(120+50,155),
                                             fill="red",tag="cardBOT0",outline="darkred")


            self.bot_hand[1] = self.cardDrawn1
            self.gameScreen.create_rectangle((20+200,5),(120+200,5+150),
                                             fill="red",tag="cardBOT1",outline="darkred")

            self.bot_hand[2] = self.cardDrawn2
            self.gameScreen.create_rectangle((20+350,5),(120+350,5+150),
                                             fill="red",tag="cardBOT2",outline="darkred")

            self.bot_hand.reverse()


    def botAI(self):
        #TODO
        #The simplest AI possible :)

        if self.bot_hand[2] != 0:
            self.botPlay = self.bot_hand[2]
            return
        elif self.bot_hand[1] != 0:
            self.botPlay = self.bot_hand[1]
            return
        elif self.bot_hand[0] != 0:
            self.botPlay = self.bot_hand[0]
            return
        else:
            self.botDraw()


        
    def placeCard(self,event):
        
        #Player's move
        if (event.y >= 420 and event.y <= 580):
            #To make it more dynamic
            desv = random.randint(-20,20)

            #card left
            if (event.x >= 345 and event.x <= 445):
                self.gameScreen.delete("card0","cardText0")
                
                self.card = self.gameScreen.create_rectangle((400+desv,250+desv),(500+desv,390+desv),
                                                             fill = "blue",
                                                             tag="card_on_field",
                                                             outline="darkblue")
                self.cardText = self.gameScreen.create_text((450+desv,320+desv),
                                                            fill="white",
                                                            tag="cardText_on_field",
                                                            text= self.player_hand[0])

                #remove from status and...
                #place on the field , index 0 for player
                #then to compare with index 1 wich is the bot played card.
                self.field[0] = self.player_hand[0]
                self.player_hand[0] = 0
               
                

            
            elif (event.x >= 495 and event.x <= 595):
            #card middle
                self.gameScreen.delete("card1","cardText1")
                
                self.card = self.gameScreen.create_rectangle((400+desv,250+desv),(500+desv,390+desv),
                                                             fill = "blue",
                                                             tag="card_on_field",
                                                             outline="darkblue")
                self.cardText = self.gameScreen.create_text((450+desv,320+desv),
                                                            fill="white",
                                                            tag="cardText_on_field",
                                                            text= self.player_hand[1])

                #remove from status
                self.field[0] = self.player_hand[1]
                self.player_hand[1] = 0
                
 
            elif (event.x >= 645 and event.x <= 745):
            #card right
                self.gameScreen.delete("card2","cardText2")
                
                self.cardField = self.gameScreen.create_rectangle((400+desv,250+desv),(500+desv,390+desv),
                                                                  fill = "blue",
                                                                  tag="card_on_field",
                                                                  outline="darkblue")
                self.cardTextField = self.gameScreen.create_text((450+desv,320+desv),
                                                                 fill="white",
                                                                 tag="cardText2",
                                                                 text= self.player_hand[2])

                #remove from status
                self.field[0] = self.player_hand[2]
                self.player_hand[2] = 0
                

            else:
                print("Player: not in that x")

            #Draws 3 cards automaticly if there is no cards in your hand
            if self.player_hand == [0,0,0]:
                for i in range(3):
                    self.drawCard()

        #Bot's moves when player moves first.
        if self.field[0] != 0:

            desv = random.randint(-20,20)

            #card left
            if self.botPlay == self.bot_hand[0]:
                self.gameScreen.delete("cardBOT0")
                
                self.card = self.gameScreen.create_rectangle((250+desv,250+desv),(350+desv,390+desv),
                                                             fill = "red",
                                                             tag="card_on_field",
                                                             outline="darkblue")
                self.cardText = self.gameScreen.create_text((300+desv,320+desv),
                                                            fill="white",
                                                            tag="cardText_on_field",
                                                            text= self.bot_hand[0])

                #remove from status
                self.field[1] = self.bot_hand[0]
                self.bot_hand[0] = 0

                

            
            elif self.botPlay == self.bot_hand[1]:
            #card middle
                self.gameScreen.delete("cardBOT1")
                
                self.card = self.gameScreen.create_rectangle((250+desv,250+desv),(350+desv,390+desv),
                                                             fill = "red",
                                                             tag="card_on_field",
                                                             outline="darkblue")
                self.cardText = self.gameScreen.create_text((300+desv,320+desv),
                                                            fill="white",
                                                            tag="cardText_on_field",
                                                            text= self.bot_hand[1])

                #remove from status
                self.field[1] = self.bot_hand[1]
                self.bot_hand[1] = 0

 
            elif self.botPlay == self.bot_hand[2]:
            #card right
                self.gameScreen.delete("cardBOT2")
                
                self.cardField = self.gameScreen.create_rectangle((250+desv,250+desv),(350+desv,390+desv),
                                                                  fill = "red",
                                                                  tag="card_on_field",
                                                                  outline="darkblue")
                self.cardTextField = self.gameScreen.create_text((300+desv,320+desv),
                                                                 fill="white",
                                                                 tag="cardText2",
                                                                 text= self.bot_hand[2])

                #remove from status
                self.field[1] = self.bot_hand[2]
                self.bot_hand[2] = 0
        
        self.cardFight()
        

        
    def startingCards(self):

        a = 295
        #Draw player hand
        for i in range(3):
            deckCard = random.choice(Deck.deck)
            print(deckCard)
            #Drawing cards on hand
            self.card = self.gameScreen.create_rectangle((50 + a,120 + 300),(150 + a,150 + 430),
                                                         fill="blue",
                                                         tag="card%i"%i,
                                                         outline="darkblue")
            self.cardText = self.gameScreen.create_text((100 + a,200 + 300),
                                                        text = ("%s"%deckCard),
                                                        tag = "cardText%i"%i,
                                                        fill="white")
            #

            #Sending to status
            self.player_hand.append(deckCard)
            Deck.deck.remove(deckCard)
            
            a += 150
            
        #Draw bot hand
        a = 50
        for i in range(3):
            deckCard = random.choice(Deck.deck)
            print(deckCard)
            #
            self.card1 = self.gameScreen.create_rectangle((20 + a,5 + 0),(120 + a,5 + 150),
                                                          fill="red",
                                                          tag="cardBOT%i"%i,
                                                          )
            #
            a += 150
            self.bot_hand.append(deckCard)
            Deck.deck.remove(deckCard)
        self.bot_hand.reverse()

        #Deck on screen
        for i in range(5):
            self.gameScreen.create_rectangle((10+5*i,450),(110+ 5*i,590),fill="brown",tag="deck",outline="darkred")



    def cardFight(self):

        #Comparing and searching for the value on the string
        self.player_card = self.field[0]
        self.bot_card = self.field[1]
        #
        if True:
            if self.player_card in var.cardValues:
                cardValue_player = var.cardValues.get(self.player_card)


            else:
                for i in self.player_card:
                    if i.isnumeric():
                        num = i
                        num = int(num)

                        if num <= 7 and num >= 0:
                            cardValue_player = 1
                        elif num > 7 and num <= 10:
                            cardValue_player = 2
        #
        if True:
            if self.bot_card in var.cardValues:
                cardValue_bot = var.cardValues.get(self.bot_card)
                
                                                   

            else:
                for i in self.bot_card:
                    if i.isnumeric():
                        num = i
                        num = int(num)

                        if num >= 0 and num <= 7 :
                            cardValue_bot = 1
                        elif num > 7 and num <= 10:
                            cardValue_bot = 2

        
        #Add points
        if cardValue_player > cardValue_bot:

            self.player_points += cardValue_player
            self.gameScreen.create_text((700,300),text=("+" + str(cardValue_player)),fill="blue",tag="pts",font=("Verdana","15","bold"))

        elif cardValue_player == cardValue_bot:

            self.player_points += cardValue_player
            self.bot_points += cardValue_bot

            self.gameScreen.create_text((700,300), text=("+" + str(cardValue_player)),fill="blue",tag="pts",font=("Verdana","15","bold"))
            self.gameScreen.create_text((700,400), text=("+" + str(cardValue_bot)),fill="red",tag="pts",font=("Verdana","15","bold"))

        else:

            self.bot_points += cardValue_bot
            self.gameScreen.create_text((700,400), text=("+" + str(cardValue_bot)), fill="red", tag="pts", font=("Verdana","15","bold"))


    def gameRulesScreen(self):
        self.frameRules = Frame(self.root,bg = "black")
        self.frameRules.pack()
        
        self.ok_but = Button(self.frameRules,
                               text="Ok!",
                               command = self.mainMenu,
                               pady= 10,padx = 17,fg='darkblue', bg='ghostwhite', relief=GROOVE)

        self.rules = Label(self.frameRules,bd = 1, relief = SUNKEN,
                           pady = 250, padx = 250,
                               text="The rules are too simple: Each player starts with 3 cards in hand "
                           "\n wich you can click with the left mouse button to play them on the field, the computer will also play "
                           "\n a card on the field and the higher one wins that 'round' and so on until the deck run out of cards."
                           "\n Card values are in Vars.py , check them out for more information.",
                               fg="ghostwhite",bg="black",font=("Verdana",10))

        self.rules.pack()
        self.ok_but.pack()


    def winner(self):

        self.win = self.player_points > self.bot_points

        if self.win:
            self.textAlert("You are the winner!",650,300)
            tkinter.messagebox.showinfo("Well done!","You are the winner!\n\nDouble Press ESC to QUIT")


            game_run = False

        if self.win ==  "OVER":
            print("game end...")

        elif self.win ==  False:
            self.textAlert("Bot is the winner!",100,300)
            tkinter.messagebox.showinfo("You still played well....","Bot is the winner!\n\nDouble Press ESC to QUIT")

            game_run = False


    #""" game settings functions """#


    def options(self):
        self.frameTitle.destroy()
        
        self.frameOptions = Frame(self.root,bg = var.BACKGROUND)
        self.frameOptions.pack()

        self.bg_var = False
        self.bg_but = Button(self.frameOptions, text="Nocturne Mode", command = self.nocturneMode)
        self.mainmenu_but = Button(self.frameOptions,
                                   text="Return to main menu",
                                   command = self.changeMenu,
                                   fg="white",bg="darkgrey",font=("Verdana","15","bold"))
        
        self.bg_but.pack()
        self.mainmenu_but.pack(side=BOTTOM)
        
    def changeMenu(self):
        self.frameOptions.destroy()
        self.mainMenu()

    def textAlert(self,text,x,y,color="red"):
        self.text = self.gameScreen.create_text((x,y),text=text,fill=color,font=("Verdana","15","bold"))
        
    def nocturneMode(self):

        self.bg_var = not self.bg_var

        if self.bg_var:
            self.root['bg'] = 'black'
            self.frameOptions['bg'] = 'black'
            self.gameScreen['bg'] = 'darkgreen'

            var.BACKGROUND = "black"
        else:
            self.root['bg'] = 'lightgrey'
            self.frameOptions['bg'] = 'lightgrey'
            self.gameScreen['bg'] = 'green'

            var.BACKGROUND = "lightgrey"

    def exit(self):
        quit()


    #"""                """#


if __name__ == "__main__":

    Deck.makeDeck()
    Window()
