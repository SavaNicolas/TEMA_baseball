from database.DAO import DAO
from model.model import Model

mymodel= Model()
mymodel.getTeamsOfYear(2015)
mymodel.buildGraph(2015)
print(mymodel.getGraphDetails())



