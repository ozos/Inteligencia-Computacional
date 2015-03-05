import random
from math import sqrt
import webbrowser
import sys
from PIL import Image, ImageDraw, ImageFont

coords = []
matc = []
Tam=20

def cds_random(cds, xmax=800, ymax=600):
    coords = []
    for i in xrange(cds):
        x = random.randint(0, xmax)
        y = random.randint(0, ymax)
        coords.append((''.join([chr(i+97)+chr(i+97)]),(float(x), float(y))))
    return coords


def dist_matriz(coords):
    matriz = {}
    for i,(nom,(x1, y1)) in enumerate(coords):
        for j, (nom,(x2, y2)) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            matriz[i, j] = dist
    return matriz


def ruta_largo(matriz, ruta):

    total = 0
    num_cds = len(ruta)
    for i in range(num_cds):
        j = (i + 1) % num_cds
        cd_i = ruta[i]
        cd_j = ruta[j]
        total += matriz[cd_i, cd_j]
    return total


def eval_func(cromosoma):
   #evaluacion
    global matc
    return ruta_largo(matc, cromosoma)

#individuos
class individuo:

    distancia = 0
    largo = Tam
    seperator = ' '

    def __init__(self, cromosoma=None, largo=Tam):
        self.cromosoma = cromosoma or self._hacercromosoma()
        self.largo = largo
        self.distancia = 0

    def _hacercromosoma(self):
        cromosoma = []
        lst = [i for i in xrange(self.largo)]
        for i in xrange(self.largo):
            seleccion = random.choice(lst)
            lst.remove(seleccion)
            cromosoma.append(seleccion)
        return cromosoma

    def evaluar(self, optimum=None):
        self.distancia = eval_func(self.cromosoma)

    def cruza(self, otro):
        izq, der = self._puntos_cruza()
        p1 = individuo()
        p2 = individuo()
        c1 = [c for c in self.cromosoma if c not in otro.cromosoma[izq:der + 1]]
        p1.cromosoma = c1[:izq] + otro.cromosoma[izq:der + 1] + c1[izq:]
        c2 = [c for c in otro.cromosoma if c not in self.cromosoma[izq:der + 1]]
        p2.cromosoma = c2[:izq] + self.cromosoma[izq:der + 1] + c2[izq:]
        return p1, p2

    def mutacion(self):
        izq, der = self._puntos_cruza()
        temp = self.cromosoma[izq]
        self.cromosoma[izq] = self.cromosoma[der]
        self.cromosoma[der] = temp

    def _puntos_cruza(self):
        izq = random.randint(0, self.largo - 2)
        #der = random.randint(izq, self.largo - 1)
        der=self.largo - 1
        return izq, der

    def __repr__(self):
        #representacion en cadena
        return '<%s cromosoma="%s" distancia=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str, self.cromosoma)), self.distancia)

    def copy(self):
        twin = self.__class__(self.cromosoma[:])
        twin.distancia = self.distancia
        return twin

    def __cmp__(self, otro):
        return cmp(self.distancia, otro.distancia)


class poblacion:
    size = 0

    def __init__(self, poblacion=None, size=100, maxGen=1000, \
                 tasanvoindividuo=0.6, tasacruza=0.90, \
                 tasa_mutacion=0.1):
        self.size = size
        self.poblacion = self._hacerpoblacion()
        self.maxGen = maxGen
        self.tasanvoindividuo = tasanvoindividuo
        self.tasacruza = tasacruza
        self.tasa_mutacion = tasa_mutacion
        for individuo in self.poblacion:
            individuo.evaluar()
        self.Generacion = 0
        self.mindistancia = sys.maxint
        self.minindividuo = None
        #self._printpoblacion()
        gen_img(coords, self.poblacion[0].cromosoma, "Inicial.png")


    def _hacerpoblacion(self):
        return [individuo() for i in range(0, self.size)]

    def run(self):
        for i in range(1, self.maxGen + 1):
            print "Generacion no:" + str(i)
            for j in range(0, self.size):
                self.poblacion[j].evaluar()
                distanciactual = self.poblacion[j].distancia
                if distanciactual < self.mindistancia:
                    self.mindistancia = distanciactual
                    self.minindividuo = self.poblacion[j]

            print "mejor individuo:", self.minindividuo
            if random.random() < self.tasacruza:
                hijos = []
                nvoindividuo = int(self.tasanvoindividuo * self.size / 2)
                for i in range(0, nvoindividuo):
                    seleccionado1 = self._selrank()
                    seleccionado2 = self._selrank()
                    padre1 = self.poblacion[seleccionado1]
                    padre2 = self.poblacion[seleccionado2]
                    hijo1, hijo2 = padre1.cruza(padre2)
                    hijo1.evaluar()
                    hijo2.evaluar()
                    hijos.append(hijo1)
                    hijos.append(hijo2)
                for i in range(0, nvoindividuo):
                    totaldistancia = 0
                    for k in range(0, self.size):
                        totaldistancia += self.poblacion[k].distancia
                    randdistancia = random.random()
                    sumadistancia = 0
                    for j in range(0, self.size):
                        sumadistancia += (self.poblacion[j].distancia / totaldistancia)
                        if sumadistancia >= randdistancia:
                            self.poblacion[j] = hijos[i]
                            break
            if random.random() < self.tasa_mutacion:
                seleccionado = self._seleccion()
                self.poblacion[seleccionado].mutacion()
        for i in range(0, self.size):
            self.poblacion[i].evaluar()
            distanciactual = self.poblacion[i].distancia
            if distanciactual < self.mindistancia:
                self.mindistancia = distanciactual
                self.minindividuo = self.poblacion[i]
        print "..................Result........................."
        print self.minindividuo
        #self._printpoblacion()

    def _seleccion(self):
        totaldistancia = 0
        for i in range(0, self.size):
            totaldistancia += self.poblacion[i].distancia
        randdistancia = random.random() * (self.size - 1)
        sumadistancia = 0
        seleccionado = 0
        for i in range(0, self.size):
            sumadistancia += (1 - self.poblacion[i].distancia / totaldistancia)
            if sumadistancia >= randdistancia:
                seleccionado = i
                break
        return seleccionado

    def _selrank(self, seleccionarmejor=0.9):
        self.poblacion.sort()
        if random.random() < seleccionarmejor:
            return random.randint(0, self.size * self.tasanvoindividuo)
        else:
            return random.randint(self.size * self.tasanvoindividuo, \
                                  self.size - 1)

    def _printpoblacion(self):
        for i in range(0, self.size):
            print "individuo ", i, self.poblacion[i]


def gen_img(coords, ruta, img_file):
    espacio = 20
    coordxy=coords
    coordxy = [(x + espacio, 600- y + espacio) for(nom ,(x, y)) in coordxy]
    maxx, maxy = 0, 0
    for x, y in coordxy:
        maxx = max(x, maxx)
        maxy = max(y, maxy)
    maxx += espacio
    maxy += espacio
    img = Image.new("RGB", (int(maxx), int(maxy)), color="white")
    fuente = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    num_cds = len(ruta)
    for i in range(num_cds):
        j = (i + 1) % num_cds
        cd_i = ruta[i]
        cd_j = ruta[j]
        x1, y1 = coordxy[cd_i]
        x2, y2 = coordxy[cd_j]
        d.line((int(x1), int(y1), int(x2), int(y2)), fill="black")
        d.text((int(x1) + 7, int(y1) - 5), str(i), font=fuente, fill=(32, 32, 32))
        d.text((int(x1) + 7, int(y1) - 17), str(coords[ruta[i]][0]), font=fuente, fill="red")

    for x, y in coordxy:
        x, y = int(x), int(y)
        d.ellipse((x - 5, y - 5, x + 5, y + 5), outline="black", fill="gray")
    del d
    img.save(img_file, "PNG")
    webbrowser.open(img_file)


def main():
    global matc, coords, Tam
    coords = cds_random(Tam)
    print("Ciudades: ")
    for i in range(len(coords)):
        print(str(i)+ " " + str(coords[i]))
    matc = dist_matriz(coords)
    pob = poblacion()
    pob.run()
    for i in range(len(coords)):
        print(str(i)+ " " + str(coords[pob.minindividuo.cromosoma[i]]))
    gen_img(coords, pob.minindividuo.cromosoma, "Resultado.png")


main()
