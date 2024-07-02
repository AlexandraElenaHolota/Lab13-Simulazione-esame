from model.model import Model

mymodel = Model()

mymodel.buildGrafo(2010, "circle")

mymodel.printGraph()

list = mymodel.printGrafo()
for l in list:
    print(l)

mymodel.percorsoMassimo()

print(f"Peso cammino massimo: {str(mymodel.bestDistance)}")

for ii in mymodel.edgesPath:
            print(f"{ii[0]} --> {ii[1]}: weight {ii[2]} distance {str(mymodel.distanza(ii))}")

