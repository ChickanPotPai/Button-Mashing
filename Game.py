from Tkinter import *
from random import *

canvasWidth = 1000
canvasHeight = 700
settingsHeight = 500
settingsWidth = 300

class Avatar():
    global enemy
    
    def __init__(self, canvas, picture, cheats, varTag):
        self.avatarX = 100
        self.avatarY = 450
        self.cheats = cheats
        self.tag = varTag
        self.healthTag = 'HP'
        self.chargeTag = 'charge'
        self.projectileTag = 'projectile'
        self.avatarHealth = 100
        self.charge = 0
        self.avatarPicture = picture
        self.avatarCanvas = canvas
        self.healthX1 = self.avatarX
        self.healthY1 = self.avatarY - 60
        self.healthX2 = self.avatarX + (self.avatarHealth * 2)
        self.healthY2 = self.avatarY - 40
        self.chargeX1 = self.avatarX
        self.chargeY1 = self.avatarY - 30
        self.chargeX2 = self.avatarX + (self.charge * 2)
        self.chargeY2 = self.avatarY - 10
        self.enemyX = -1
        self.end = False

        ## Creates the intial images for the avatar and HP/Charge bars
        canvas.create_image(self.avatarX, self.avatarY, anchor = NW, image = picture, tag = varTag)
        canvas.create_rectangle(self.healthX1, self.healthY1, self.healthX2, self.healthY2, \
                                fill = 'red', outline = 'black', tag = self.healthTag)
        canvas.create_rectangle(self.chargeX1, self.chargeY1, self.chargeX2, self.chargeY2, \
                                fill = 'blue', outline = 'black', tag = self.chargeTag)
        
    def move(self, event): ## All move functions for the avatar
        global root
        char = event.char

        if(self.cheats == True):
            if(char == "w"):
                self.jump()
                
            if(char == "s"):
                self.charge = 100
                self.avatarHealth = 100
                self.chargeBarUpdate()
                self.healthBarUpdate()
            
        if(char == "a"):
            if(self.avatarX == 0):
                self.avatarX = 50
            
            self.avatarCanvas.delete(self.tag)
            self.avatarX -= 50
            self.healthBarUpdate()
            self.chargeBarUpdate()
            self.avatarCanvas.create_image(self.avatarX, self.avatarY, anchor = NW, image = self.avatarPicture, tag = self.tag)
            
        elif(char == "d"):
            if(self.avatarX == canvasWidth - 200):
                self.avatarX = canvasWidth - 250
            
            self.avatarCanvas.delete(self.tag)
            self.avatarX += 50
            self.healthBarUpdate()
            self.chargeBarUpdate()
            self.avatarCanvas.create_image(self.avatarX, self.avatarY, anchor = NW, image = self.avatarPicture, tag = self.tag)

        elif(char == "q"):
            self.attack()
            
        elif(char == "e"):
            self.fire()

        elif(char == "r"):
            self.special()
                
        elif(char == "m"):
            self.end = True
            self.avatarY = 500
            self.projectileX = 1200
            enemy.mobX = 1200
            self.avatarCanvas.delete(ALL)
            root.destroy()

            settings()

        elif(char == "`"):
            self.end = True
            self.avatarY = 500
            self.projectileX = 1200
            enemy.mobX = 1200
            self.avatarCanvas.delete(ALL)
            root.destroy()

    def jump(self): ## Jump function, causes all other animations to stop when used
        orgAvatarY = self.avatarY

        def draw():
            self.avatarCanvas.delete(self.tag)
            self.avatarCanvas.create_image(self.avatarX, self.avatarY, anchor = NW, \
                                           image = self.avatarPicture, tag = self.tag)
            self.avatarCanvas.update()

        while(self.avatarY > 250):
            self.avatarY -= 50
            self.healthBarUpdate()
            self.chargeBarUpdate()
            self.avatarCanvas.after(50, draw())

        while(self.avatarY < orgAvatarY):
            self.avatarY += 50
            self.healthBarUpdate()
            self.chargeBarUpdate()
            self.avatarCanvas.after(50, draw())

        
    def attack(self): ## Basic attack for avatar
        if(self.avatarY == 450):
            punch = PhotoImage(file = 'effect_punch.gif')
            tempPunch = self.avatarCanvas.create_image(self.avatarX + 190, \
                                                       self.avatarY + 20, anchor = NW, image = punch)
            self.avatarCanvas.update()
            self.avatarCanvas.after(100, self.avatarCanvas.delete(tempPunch))
            self.attackHit()
            self.chargeBarUpdate()
                
            
    def attackHit(self):
        if(self.avatarX + 190 + 150 >= self.enemyX and self.enemyX > 0 ):
            self.charge += 2
            enemy.damage(5)
            self.avatarCanvas.delete(self.projectileTag)
            
            if(enemy.mobHealth <= 0):
                enemy.die()

    def fire(self): ## Fires a projectile from avatar
        if(self.avatarY == 450 and self.charge >= 40 and self.end == False):
            self.avatarHealth += 5
            self.charge -= 40
            self.chargeBarUpdate()

            self.originalY = self.avatarY
            self.projectileX = self.avatarX + 200
            self.projectileY = self.avatarY + 50

            def draw():
                self.avatarCanvas.delete(self.projectileTag)
                self.avatarCanvas.create_image(self.projectileX, self.projectileY, \
                                                     anchor = NW, image = projectile, tag = self.projectileTag)
                self.avatarCanvas.update()
    
            projectile = PhotoImage(file = 'effect_projectile.gif')
            
            while(self.projectileX < 1100):
                draw()
                self.projectileHit()
                self.projectileX += 1

    def projectileHit(self):
        if(self.projectileX + 100 >= self.enemyX and self.enemyX > 0):
            self.projectileX = 1100
            enemy.damage(80)
            
            self.avatarCanvas.delete(self.projectileTag)
            
            if(enemy.mobHealth <= 0):
                enemy.die()

    def special(self): ## Boom special for avatar
        if(self.avatarY == 450 and self.charge == 100):
            self.avatarHealth += 10
            self.charge = 0
            self.chargeBarUpdate()
            
            self.specialX = self.avatarX - 500
            self.specialY = self.avatarY - 450
    
            nuke = PhotoImage(file = 'effect_nuke.gif')
            tempNuke = self.avatarCanvas.create_image(self.specialX, self.specialY, \
                                                            anchor = NW, image = nuke)
            self.specialHit()
            self.avatarCanvas.update()
            self.avatarCanvas.after(700, self.avatarCanvas.delete(tempNuke))

            if(enemy.mobHealth <= 0):
                enemy.spawn()
                        
    def specialHit(self):
        if(self.specialX < self.enemyX and self.specialX + 1200 > self.enemyX):
            enemy.damage(500)
            
            if(enemy.mobHealth <= 0):
                enemy.mobX = 1200
                self.enemyX = -1
                self.avatarCanvas.delete(enemy.tag)
                self.avatarCanvas.delete(enemy.mobHealthTag)

    def healthBarUpdate(self):
        
        if(self.avatarHealth <= 0):
            self.gameOver()
            
        if(self.avatarHealth >= 100):
            self.avatarHealth = 100
        
        if(self.end == False):
            self.healthX1 = self.avatarX
            self.healthY1 = self.avatarY - 60
            self.healthX2 = self.avatarX + (self.avatarHealth * 2)
            self.healthY2 = self.avatarY - 40
            
            self.avatarCanvas.delete(self.healthTag)
            self.avatarCanvas.create_rectangle(self.healthX1, self.healthY1, self.healthX2, self.healthY2, \
                                                fill = 'red', outline = 'black', tag = self.healthTag) 

    def chargeBarUpdate(self):
        if(self.end == False):
            if(self.charge < 0):
                self.charge = 0
            elif(self.charge >= 100):
                self.charge = 100
                
            self.chargeX1 = self.avatarX
            self.chargeY1 = self.avatarY - 30
            self.chargeX2 = self.avatarX + (self.charge * 2)
            self.chargeY2 = self.avatarY - 10

            self.avatarCanvas.delete(self.chargeTag)
            self.avatarCanvas.create_rectangle(self.chargeX1, self.chargeY1, self.chargeX2, self.chargeY2, \
                                                fill = 'blue', outline = 'black', tag = self.chargeTag)

    def damage(self, amount):
        self.avatarHealth -= amount

    def gameOver(self):
        self.end = True
        self.avatarY = 500
        self.projectileX = 1200
        enemy.mobX = 1200
        self.avatarCanvas.delete(ALL)
        root.destroy()

        loseGame()

    def gameWin(self):
        self.end = True
        self.avatarY = 500
        self.projectileX = 1200
        enemy.mobX = 1200
        self.avatarCanvas.delete(ALL)
        root.destroy()

        winGame()
        
                
##-----------------------------------------------------------------------------------------------------------
        
class Mob(): ## Functions common to all mobs, inherited
    global enemy
    global mobIndex
    global mobSpawn
    global mainAvatar
        
    def damage(self, amount):
        if(self.mobHealth > 0):
            self.mobHealth -= amount

    def die(self):
        if(mainAvatar.end == False):
            self.mobX = 1200
            mainAvatar.enemyX = -1
            mainAvatar.avatarCanvas.delete(self.tag)
            mainAvatar.avatarCanvas.delete(self.mobHealthTag)

            self.spawn()

    def mobHealthUpdate(self):
        self.mobHealthX1 = self.mobX
        self.mobHealthY1 = self.mobY - 30
        self.mobHealthX2 = self.mobX + self.mobHealth
        self.mobHealthY2 = self.mobY - 10

        mainAvatar.avatarCanvas.delete(self.mobHealthTag)
        mainAvatar.avatarCanvas.create_rectangle(self.mobHealthX1, self.mobHealthY1, \
                                                 self.mobHealthX2, self.mobHealthY2, \
                                                 fill = 'red', outline = 'white', \
                                                 tag = self.mobHealthTag)

    def spawn(self): ## Spawns mobs
        global enemy
        global mobIndex
        global mobSpawn
        
        if(mobIndex < len(mobSpawn)):
            
            if(mobSpawn[mobIndex] == 0):
                mobIndex += 1
                enemy = smallEnemy()
                enemy.attack()
                
            elif(mobSpawn[mobIndex] == 1):
                mobIndex += 1
                enemy = mediumEnemy()
                enemy.attack()

            elif(mobSpawn[mobIndex] == 2):
                mobIndex += 1
                enemy = bigEnemy()
                enemy.attack()

            elif(mobSpawn[mobIndex] == 3):
                mobIndex += 1
                enemy = bossEnemy()
                enemy.attack()

        else:
            mainAvatar.gameWin() ## Win if all monsters are spawned
                

class smallEnemy(Mob):
    global mainAvatar
    global gameSpeed
    
    def __init__(self):
        self.mobHealth = 100
        self.mobX = 900
        self.mobY = 520
        self.mobHealthX1 = self.mobX
        self.mobHealthY1 = self.mobY - 30
        self.mobHealthX2 = self.mobX + self.mobHealth
        self.mobHealthY2 = self.mobY - 10
        self.tag = 'mob'
        self.mobHealthTag = 'mobHP'
        self.mobPicture = PhotoImage(file = "mob_small.gif")
        
        mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                             anchor = NW, image = self.mobPicture, tag = self.tag)
        mainAvatar.avatarCanvas.create_rectangle(self.mobHealthX1, self.mobHealthY1, self.mobHealthX2, self.mobHealthY2, \
                                            fill = 'red', outline = 'white', tag = self.mobHealthTag) 

    def attack(self):
        def draw():
            mainAvatar.enemyX = self.mobX
            mainAvatar.avatarCanvas.delete(self.tag)
            mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                                 anchor = NW, image = self.mobPicture, tag = self.tag)
            self.mobHealthUpdate()
            mainAvatar.avatarCanvas.update()
            
        while(self.mobX > 0 and self.mobX < 1100 and mainAvatar.end == False):
            mainAvatar.avatarCanvas.after(10, draw())
            self.hit()
            self.mobX -= 1


    def hit(self):
        if(mainAvatar.avatarX + 200 >= self.mobX and mainAvatar.end == False):
            self.damage(20)
            mainAvatar.damage(5)
            mainAvatar.healthBarUpdate()
            
        if(self.mobHealth <= 0):
            self.die()

class mediumEnemy(Mob):
    global mainAvatar
    global gameSpeed
    
    def __init__(self):
        self.mobHealth = 200
        self.mobX = 800
        self.mobY = 450
        self.mobHealthX1 = self.mobX
        self.mobHealthY1 = self.mobY - 30
        self.mobHealthX2 = self.mobX + self.mobHealth
        self.mobHealthY2 = self.mobY - 10
        self.tag = 'mob'
        self.mobHealthTag = 'mobHP'
        self.mobPicture = PhotoImage(file = "mob_medium.gif")
        
        mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                             anchor = NW, image = self.mobPicture, tag = self.tag)
        mainAvatar.avatarCanvas.create_rectangle(self.mobHealthX1, self.mobHealthY1, self.mobHealthX2, self.mobHealthY2, \
                                            fill = 'red', outline = 'white', tag = self.mobHealthTag) 

    def attack(self):
        def draw():
            mainAvatar.enemyX = self.mobX
            mainAvatar.avatarCanvas.delete(self.tag)
            mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                                 anchor = NW, image = self.mobPicture, tag = self.tag)
            self.mobHealthUpdate()
            mainAvatar.avatarCanvas.update()
            
        while(self.mobX > 0 and self.mobX < 1100 and mainAvatar.end == False):
            mainAvatar.avatarCanvas.after(gameSpeed - 40, draw())
            self.hit()
            self.mobX -= 1
            
        self.die()

    def hit(self):
        if(mainAvatar.avatarX + 200 >= self.mobX):
            self.damage(20)
            mainAvatar.damage(5)
            mainAvatar.healthBarUpdate()
            
        if(self.mobHealth <= 0):
            self.die()

class bigEnemy(Mob):
    global mainAvatar
    global gameSpeed
    
    def __init__(self):
        self.mobHealth = 200
        self.mobX = 750
        self.mobY = 250
        self.mobHealthX1 = self.mobX
        self.mobHealthY1 = self.mobY - 30
        self.mobHealthX2 = self.mobX + self.mobHealth
        self.mobHealthY2 = self.mobY - 10
        self.tag = 'mob'
        self.mobHealthTag = 'mobHP'
        mobSpawn = [0,1,0,1,0]
        self.mobPicture = PhotoImage(file = "mob_big.gif")
        
        mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                             anchor = NW, image = self.mobPicture, tag = self.tag)
        mainAvatar.avatarCanvas.create_rectangle(self.mobHealthX1, self.mobHealthY1, self.mobHealthX2, self.mobHealthY2, \
                                            fill = 'red', outline = 'white', tag = self.mobHealthTag) 

    def attack(self):
        def draw():
            mainAvatar.enemyX = self.mobX
            mainAvatar.avatarCanvas.delete(self.tag)
            mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                                 anchor = NW, image = self.mobPicture, tag = self.tag)
            self.mobHealthUpdate()
            mainAvatar.avatarCanvas.update()
            
        while(self.mobX > 0 and self.mobX < 1100 and mainAvatar.end == False):
            mainAvatar.avatarCanvas.after(gameSpeed - 30, draw())
            self.hit()
            self.mobX -= 1
            
        if(self.mobX == 1):
            self.die()


    def hit(self):
        if(mainAvatar.avatarX + 200 >= self.mobX):
            self.damage(20)
            mainAvatar.damage(20)
            mainAvatar.healthBarUpdate()
            
        if(self.mobHealth <= 0):
            self.die()

class bossEnemy(Mob):
    global mainAvatar
    global gameSpeed
    
    def __init__(self):
        self.mobHealth = 1200
        self.mobX = 700
        self.mobY = 50
        self.mobHealthX1 = self.mobX
        self.mobHealthY1 = self.mobY - 30
        self.mobHealthX2 = self.mobX + self.mobHealth/3
        self.mobHealthY2 = self.mobY - 10
        self.tag = 'mob'
        self.mobHealthTag = 'mobHP'
        mobSpawn = [0,1,0,1,0]
        self.mobPicture = PhotoImage(file = "mob_boss.gif")
        
        mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                             anchor = NW, image = self.mobPicture, tag = self.tag)
        mainAvatar.avatarCanvas.create_rectangle(self.mobHealthX1, self.mobHealthY1, self.mobHealthX2, self.mobHealthY2, \
                                            fill = 'red', outline = 'white', tag = self.mobHealthTag) 

    def attack(self):
        def draw():
            mainAvatar.enemyX = self.mobX
            mainAvatar.avatarCanvas.delete(self.tag)
            mainAvatar.avatarCanvas.create_image(self.mobX, self.mobY, \
                                                 anchor = NW, image = self.mobPicture, tag = self.tag)
            self.bossHealthUpdate()
            mainAvatar.avatarCanvas.update()
            
        while(self.mobX > 0 and self.mobX < 1100):
            mainAvatar.avatarCanvas.after(gameSpeed - 20, draw())
            self.hit()
            self.mobX -= 1
            
        if(self.mobX == 1):
            self.die()


    def hit(self):
        if(mainAvatar.avatarX + 200 >= self.mobX):
            self.damage(20)
            mainAvatar.damage(20)
            mainAvatar.healthBarUpdate()
            
        if(self.mobHealth <= 0):
            self.die()

    def bossHealthUpdate(self):
        self.mobHealthX1 = self.mobX
        self.mobHealthY1 = self.mobY - 30
        self.mobHealthX2 = self.mobX + self.mobHealth/3
        self.mobHealthY2 = self.mobY - 10

        mainAvatar.avatarCanvas.delete(self.mobHealthTag)
        mainAvatar.avatarCanvas.create_rectangle(self.mobHealthX1, self.mobHealthY1, self.mobHealthX2, self.mobHealthY2, \
                                            fill = 'red', outline = 'white', tag = self.mobHealthTag)

##----------------------------------------------------------------------------------------------------------------
def winFunctions(event):
    global endRoot
    endChar = event.char

    if(endChar == "r"): ## R and Q can restart or quit game
        endRoot.destroy()
        settings()

    if(endChar == "q"):
        endRoot.destroy()
        
def winGame():
    global endRoot
    global widgetDict
    
    endRoot = Tk()
    endCanvas = Canvas(endRoot, width = 800, height = 600)
    endCanvas.pack()

    winImage = PhotoImage(file = "end_win.gif")
    endCanvas.create_image(0,0, anchor = NW, image = winImage)

    widgetDict["restartText"] = Label(endRoot, text = "Restart - R")
    widgetDict["restartText"].place(x = 10, y = 560)
    widgetDict["quitText"] = Label(endRoot, text = "Quit - Q")
    widgetDict["quitText"].place(x = 730, y = 560)
    
    endRoot.bind('<Key>', winFunctions)

    endRoot.mainloop()
    
def loseFunctions(event):
    global endRoot
    endChar = event.char

    if(endChar == "r"):
        endRoot.destroy()
        settings()

    if(endChar == "q"):
        endRoot.destroy()
        
def loseGame():
    global endRoot
    global widgetDict
    
    endRoot = Tk()
    endCanvas = Canvas(endRoot, width = 800, height = 600)
    endCanvas.pack()

    loseImage = PhotoImage(file = "end_gameover.gif")
    endCanvas.create_image(0,0, anchor = NW, image = loseImage)

    widgetDict["restartText"] = Label(endRoot, text = "Restart - R")
    widgetDict["restartText"].place(x = 10, y = 560)
    widgetDict["quitText"] = Label(endRoot, text = "Quit - Q")
    widgetDict["quitText"].place(x = 730, y = 560)
    
    endRoot.bind('<Key>', loseFunctions)

    endRoot.mainloop()
    
    
def getSettings(event):
    global gameMap
    global gameAvatar
    global gameSpeed
    global gameCheats
    global mapVariable
    global avatarVariable
    global speedVariable
    global cheatsVariable
    
    gameMap = int(mapVariable.get()[0])
    gameAvatar = int(avatarVariable.get()[0])
    gameSpeed = int(speedVariable.get()[0])
    gameCheats = int(cheatsVariable.get()[0])
    
    settingsRoot.destroy()
    run()

    
def settings():
    global widgetDict
    global settingsRoot
    global mapVariable
    global avatarVariable
    global speedVariable
    global cheatsVariable
    
    widgetDict = {}
    settingsRoot = Tk()
    settingsRoot.title("Settings")

    mapVariable = StringVar(settingsRoot)
    mapVariable.set("1. Plains (default)")

    avatarVariable = StringVar(settingsRoot)
    avatarVariable.set("1. Pie (default)")

    speedVariable = StringVar(settingsRoot)
    speedVariable.set("1. Easy (default)")

    cheatsVariable = StringVar(settingsRoot)
    cheatsVariable.set("1. No (default)")
    
    widgetDict["settingsCanvas"] = Canvas(settingsRoot, width = settingsWidth, height = settingsHeight)
    widgetDict["settingsCanvas"].pack()

    widgetDict["welcomeText"] = Label(settingsRoot, \
                                         text = "Welcome to Button Mashing!\nPlease make your choices:")
    widgetDict["welcomeText"].place(x = 50, y = 30)
    
    widgetDict["mapText"] = Label(settingsRoot, text = "Choose map:")
    widgetDict["mapText"].place(x = 100, y = 90)
    
    widgetDict["mapMenu"] = OptionMenu(settingsRoot, mapVariable, \
                                       "1. Plains (default)", "2. Barren          ", "3. Beach           ")
    widgetDict["mapMenu"].place(x = 60, y = 120)

    widgetDict["avatarText"] = Label(settingsRoot, text = "Choose avatar:")
    widgetDict["avatarText"].place(x = 90, y = 170)
    
    widgetDict["avatarMenu"] = OptionMenu(settingsRoot, avatarVariable, \
                                       "1. Pie (default)  ", "2. Zombie Mushroom",\
                                          "3. JigglyPuff     ")
    widgetDict["avatarMenu"].place(x = 60, y = 200)

    widgetDict["speedText"] = Label(settingsRoot, text = "Choose speed/difficulty:")
    widgetDict["speedText"].place(x = 60, y = 260)
    
    widgetDict["speedMenu"] = OptionMenu(settingsRoot, speedVariable, \
                                       "1. Easy (default)", "2. Medium        ", "3. Hard          ")
    widgetDict["speedMenu"].place(x = 60, y = 290)

    widgetDict["cheatsText"] = Label(settingsRoot, text = "Cheats?:")
    widgetDict["cheatsText"].place(x = 100, y = 350)

    widgetDict["cheatsMenu"] = OptionMenu(settingsRoot, cheatsVariable, \
                                       "1. No (default)", "2. Yes        ")
    widgetDict["cheatsMenu"].place(x = 60, y = 380)

    widgetDict["inputButton"] = Button(settingsRoot, text = "Done")
    widgetDict["inputButton"].place(x = 115, y = 440)
    widgetDict["inputButton"].bind("<Button-1>", getSettings)

    settingsRoot.mainloop()
    
def run():
    global root
    global widgetDict
    global mainAvatar
    global gameAvatar
    global gameMap
    global gameCheats
    global gameSpeed
    global mobSpawn
    global mobIndex

    root = Tk()
    widgetDict["canvas"] = Canvas(root, width = canvasWidth, height = canvasHeight)
    widgetDict["canvas"].pack()

    cheats = False

    if(gameCheats == 1):
        cheats = False

    elif(gameCheats == 2):
        cheats = True
        
    ## Sets game map and game avatars
        
    if(gameMap == 1):
        plains = PhotoImage(file = "map_plains.gif")
        widgetDict["canvas"].create_image(0, 0, anchor = NW, image = plains)
        
    elif(gameMap == 2):
        barren = PhotoImage(file = "map_barren.gif")
        widgetDict["canvas"].create_image(0, 0, anchor = NW, image = barren)
        
    elif(gameMap == 3):
        beach = PhotoImage(file = "map_beach.gif")
        widgetDict["canvas"].create_image(0, 0, anchor = NW, image = beach)

    if(gameAvatar == 1):
        pie = PhotoImage(file = "avatar_pie.gif")
        mainAvatar = Avatar(widgetDict["canvas"], pie, cheats,'pie')

    elif(gameAvatar == 2):
        zombie = PhotoImage(file = "avatar_zombie.gif")
        mainAvatar = Avatar(widgetDict["canvas"], zombie, cheats,'zombie')

    elif(gameAvatar == 3):
        jigglypuff = PhotoImage(file = "avatar_jigglypuff.gif")
        mainAvatar = Avatar(widgetDict["canvas"], jigglypuff, cheats,'jigglypuff')


    if(gameSpeed == 1): ## Difficulty of game is dependent on game speed
        gameSpeed = 80

    elif(gameSpeed == 2):
        gameSpeed = 60

    elif(gameSpeed == 3):
        gameSpeed = 50
    
    root.bind('<Key>', mainAvatar.move)

    mobIndex = 0

    ## Decides a random set of spawns from set
    
    mobSpawnPossibilities = ([0,0,1,1,2,1,2,2,2,3],[0,1,0,2,2,1,1,2,2,3],[1,0,0,0,2,1,2,2,2,3])
    selectSpawn = randint(0,2)
    mobSpawn = mobSpawnPossibilities[selectSpawn]

    spawnStart = Mob()
    spawnStart.spawn()  ## Begins the spawn
    
    root.mainloop()

settings()
