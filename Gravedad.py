import turtle
import math
class Fn:
    def Modulo(ListaXY):
        return (ListaXY[0]**2+ListaXY[1]**2)**0.5
    def Distancia(Objeto1,Objeto2):
        return [Objeto1.getPos()[0]-Objeto2.getPos()[0],Objeto1.getPos()[1]-Objeto2.getPos()[1]]
    def SumaM(Lista1,Lista2):
        Resultado=[]
        for i in range(len(Lista1)):
            Resultado.append(Lista1[i]+Lista2[i])
        return Resultado
    def MultiM(Lista,K):
        Resultado=[]
        for i in range(len(Lista)):
            Resultado.append(Lista[i]*K)
        return Resultado
class Espacio:
    def __init__(self,ListaPlanetas,ListaNaves,ListaPlanetasTurtle,ListaNavesTurtle,stepTiempo,CiclosSoloCalcula,Zoom):
        self.ListaPlanetas=ListaPlanetas
        self.ListaNaves=ListaNaves
        self.ListaPlanetasTurtle=ListaPlanetasTurtle
        self.ListaNavesTurtle=ListaNavesTurtle
        self.ListaObjetos=ListaPlanetas+ListaNaves
        self.ListaObjetosTurtle=ListaPlanetasTurtle+ListaNavesTurtle
        self.stepTiempo=stepTiempo
        self.CiclosSoloCalcula=CiclosSoloCalcula
        self.Zoom=Zoom
        self.G = 6.67408*10**-11

    def ObjetosPenUp(self):
        for ObjetoT in self.ListaObjetosTurtle:
            ObjetoT.penup()
    def ObjetosPenDown(self):
        for ObjetoT in self.ListaObjetosTurtle:
            ObjetoT.pendown()
    def ZoomIn(self):
        self.ObjetosPenUp()
        self.Zoom=self.Zoom*1.1
        for i,PlanetaT in enumerate(self.ListaPlanetasTurtle):
            PlanetaT.turtlesize(self.ListaPlanetas[i].getRadio()*self.Zoom/10)
        self.ColocaObjetos()
        self.ObjetosPenDown()
    def ZoomOut(self):
        self.ObjetosPenUp()
        self.Zoom=self.Zoom/1.1
        for i,PlanetaT in enumerate(self.ListaPlanetasTurtle):
            PlanetaT.turtlesize(self.ListaPlanetas[i].getRadio()*self.Zoom/10)
        self.ColocaObjetos()
        self.ObjetosPenDown()
    def VTiempoUp(self):
        self.stepTiempo=self.stepTiempo*1.5
        self.CiclosSoloCalcula=self.CiclosSoloCalcula/1.5
    def VTiempoDown(self):
        self.stepTiempo=self.stepTiempo/1.5
        self.CiclosSoloCalcula=self.CiclosSoloCalcula*1.5
    def PrintDatos(self):
        #print("hola")
        pass
    def Inicio(self):
        self.ObjetosPenUp()
        for i,PlanetaT in enumerate(self.ListaPlanetasTurtle):
            PlanetaT.pensize(0.1)
            PlanetaT.speed(0)
            PlanetaT.shape("circle")
            PlanetaT.turtlesize(self.ListaPlanetas[i].getRadio()*self.Zoom/10)#ni idea de por qué ese /10, pero funciona xD
            PlanetaT.pencolor("blue")
        for NaveT in self.ListaNavesTurtle:
            NaveT.speed(0)
            NaveT.pencolor("red")
        self.ColocaObjetos()
        self.ObjetosPenDown()
    def ColocaObjetos(self):
        for i,ObjetoT in enumerate(self.ListaObjetosTurtle):
            PosTurtle=self.ListaObjetos[i].CalculaPosTurtle()
            ObjetoT.goto(PosTurtle[0],PosTurtle[1])
    def Bucle(self):
        for i in range(round(self.CiclosSoloCalcula)):
            for Objeto in (self.ListaObjetos):
                Objeto.Integra()
        self.ColocaObjetos()
        self.PrintDatos()
        screen.ontimer(self.Bucle,0)
class Movil:
    def __init__(self,Nombre,Pos,Vel,Ace,Masa):
        self.Nombre=Nombre
        self.Pos=Pos
        self.Vel=Vel
        self.Ace=Ace
        self.Masa=Masa
        self.PosTurtle=[0,0]
    #get set
    def getPos(self):
        return self.Pos
    def getVel(self):
        return self.Vel
    def getAce(self):
        return self.Ace
    def getMasa(self):
        return self.Masa
    def getPosTurtle(self):
        return self.PosTurtle
    def getNombre(self):
        return self.Nombre

    def setPos(self,Pos):
        self.Pos=[Pos[0],Pos[1]]
    def setVel(self,Vel):
        self.Vel=[Vel[0],Vel[1]]
    def setAce(self,Ace):
        self.Ace=[Ace[0],Ace[1]]
    def setPosTurtle(self,PosTurtle):
        self.PosTurtle=[PosTurtle[0],PosTurtle[1]]

    def CalculaPosTurtle(self):#multiplica la posición por el zoom
        self.PosTurtle=Fn.MultiM(self.getPos(),Espacio.Zoom)
        return self.PosTurtle
    def CalculaG(self):
        GravedadFinalXY=[0,0]
        for Planeta in Espacio.ListaPlanetas:
            if Planeta==self:
                continue#no calcules g para sí mismo
            #unitarios,gravedad*unitarios
            DisPlaneta=Fn.Distancia(self,Planeta)
            ModDisPlaneta=Fn.Modulo(DisPlaneta)
            UniXY=Fn.MultiM(DisPlaneta,1/ModDisPlaneta)
            GravedadXY=Fn.MultiM(UniXY,-Planeta.getMasa()*Espacio.G/ModDisPlaneta**2)
            #accum
            GravedadFinalXY=Fn.SumaM(GravedadFinalXY,GravedadXY)
        return GravedadFinalXY
    def Integra(self):
        self.Ace=self.CalculaAce()
        self.Vel=Fn.SumaM(self.Vel,(Fn.MultiM(self.Ace,Espacio.stepTiempo)))
        self.Pos=Fn.SumaM(self.Pos,(Fn.MultiM(self.Vel,Espacio.stepTiempo)))
        return self.Pos
class Planeta(Movil):
    def __init__(self,Nombre,Pos,Vel,Ace,Masa,Radio):
        Movil.__init__(self,Nombre,Pos,Vel,Ace,Masa)
        self.Radio=Radio
    #get set
    def getRadio (self):
        return self.Radio
    def CalculaAce(self):
        return self.CalculaG()
class Nave(Movil):
    def __init__(self,Turtle,Nombre,Pos,Vel,Ace,Masa,FMotor,Combustible):
        Movil.__init__(self,Nombre,Pos,Vel,Ace,Masa)
        self.Turtle=Turtle
        self.Throttle=0
        self.FMotor=FMotor
        self.Combustible=Combustible
        self.UniXYMotor=[math.cos(Turtle.heading()*2*3.1415/360),math.sin(Turtle.heading()*2*3.1415/360)]
    def ThrottleUp(self):
        if self.Throttle<1:
            self.Throttle=self.Throttle+0.1
    def ThrottleDown(self):
        if self.Throttle>0:
            self.Throttle=self.Throttle-0.1
    def ThrottleCut(self):
        self.Throttle=0
    def CalculaAceMotor(self):
        AceMotor=0
        if self.Combustible>0:
            AceMotor=self.FMotor*self.Throttle/self.Masa
        return Fn.MultiM(self.UniXYMotor,AceMotor)
    def CalculaAce(self):
        if self.TocandoSuelo()==False:
            return Fn.SumaM(self.CalculaG(),self.CalculaAceMotor())
        else:
            return [0,0]
    def TocandoSuelo(self):
        for Planeta in Espacio.ListaPlanetas:
            if Fn.Modulo(Fn.Distancia(self,Planeta))<= Planeta.getRadio():
                DistanciaPlaneta=Fn.Distancia(self,Planeta)
                ModDistanciaPlaneta=Fn.Modulo(DistanciaPlaneta)
                UniXY=[DistanciaPlaneta[0]/ModDistanciaPlaneta,DistanciaPlaneta[1]/ModDistanciaPlaneta]
                DistanciaSuelo=Planeta.getRadio()-ModDistanciaPlaneta
                Movimiento=[-UniXY[0]*DistanciaSuelo,-UniXY[1]*DistanciaSuelo]
                self.Vel=[0,0]
                self.Pos=[self.getPos()[0]+Movimiento[0],self.getPos()[1]+Movimiento[1]]
                return True
            else:
                return False

NaveT=turtle.Turtle()
Nave=Nave(NaveT,"Nave",[0,64010000],[3200,0],[0,0],100,1,1000)#3203
Tierra=Planeta("Tierra",[0,0],[-12,0],[0,0],5.972*10**24,6371000)
TierraT=turtle.Turtle()
Luna=Planeta("Luna",[0,384400000],[1020,0],[0,0],7.349*10**22,1737000)
LunaT=turtle.Turtle()
Espacio=Espacio([Tierra,Luna],[Nave],[TierraT,LunaT],[NaveT],100,100,0.000008)
#Pantalla y teclas
screen = turtle.Screen()#debe llamarse screen (o cambiar Espacio.Bucle())
screen.setup(width=1.0, height=1.0)
screen.onkey(screen.bye, "q")
screen.onkey(Espacio.ZoomIn,"plus")
screen.onkey(Espacio.ZoomOut,"minus")
screen.onkey(Espacio.VTiempoUp,"period")
screen.onkey(Espacio.VTiempoDown,"comma")
screen.onkey(Nave.ThrottleUp,"a")
screen.onkey(Nave.ThrottleDown,"z")
screen.onkey(Nave.ThrottleCut,"x")


screen.listen()
#Arranca el programa
Espacio.Inicio()
screen.ontimer(Espacio.Bucle,0)
screen.mainloop()
