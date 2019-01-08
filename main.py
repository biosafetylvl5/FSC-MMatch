import networkx as nx
import metis as ms
import random as r
from math import ceil

randomNames = ["Bernarda Hundt","Luis Loth  ","Jaqueline Ziglar  ","Olevia Gorton  ","Paris Fluker  ","Nova Shand  ","Marine Kensey  ","Sara Buczek  ","Tenesha Clegg  ","Candace Kwong  ","Jama Shetler  ","Nell Fennessey  ","Thalia Leedy  ","Carla Maki  ","Eugenio Paynter  ","Leigh Nazario  ","Robert Mallet  ","Leonora Turner  ","Norene Lyford  ","Boyce Lorentz  ","Lowell Stockman  ","Siu Henegar  ","Darcel Kierstead  ","Theo Decosta  ","Stanton Babich  ","Julieta Jun  ","Shea Brink  ","Xuan Fandel  ","Diedra Gorley  ","Penny Winnie  ","Tobi Kono  ","Lasandra Fesler  ","Evelyne Uselton  ","Mikaela Gupta  ","Sharlene Mingle  ","Hilaria Chagolla  ","Percy Cowans  ","Clarita Gentner  ","Junko Valentin  ","Mamie Sthilaire  ","Fausto Garlow  ","Hyman Bosch  ","Yan Fendley  ","Kandace Norberg  ","Florance Spier  ","Larue Morado  ","Laurence Truett  ","Neda Boos  ","Diann Felker  ","Theresia Nicholes","Barry Harms  ","Cythia Verdi  ","Racquel Baptista  ","Sharlene Sisemore  ","Mercedes Bashaw  ","Kenia Whalley  ","Victorina Traverso  ","Lottie Carlucci  ","Jaymie Labarge  ","Eleonora Heffelfinger  ","Ada Nack  ","Yen Lute  ","Andrea Marroquin  ","Joaquina Ingles  ","Raisa Muntz  ","Janel Niday  ","Yetta Troop  ","Alex Stock  ","Demetrius Rothchild  ","Tawny Michalek  ","Genie Ryant  ","Georgiann Vorpahl  ","Dexter Bilbrey  ","Mica Christain  ","Tashina Hollman  ","Carina Whitworth  ","Laveta Mcfarland  ","Toney Driver  ","Classie Kissel  ","Rey Sievert  ","Forest Hollabaugh  ","Marcell Buntin  ","Miyoko Besaw  ","Cassey Margulies  ","Nikia Barnhouse  ","Guy Hambright  ","Arnulfo Linhart  ","Jeane Stratman  ","Shakita Rydberg  ","Mellisa Tinder  ","Corina Ader  ","Sheila Hempel  ","Trey Wimbish  ","Camila Decuir  ","Kimiko Battey  ","Ione Manley  ","Cyndy Trivett  ","Kaleigh Leaf  ","Gertrud Berens  ","Krissy Pilkington"]

A = "All"
M = "Male"
F = "Female"
O = "Other"

goptions = [M,F,A]
genders = [M,F,O]

def genRandomPrefs(names, genders, goptions):
    prefs = {}
    for name in names:
       prefs[name] = [genders[r.randint(0,2)], goptions[r.randint(0,2)], r.sample(names, r.randint(0,10)), r.sample(names,r.randint(0,1))]
    return prefs

# Need to move peeps from all to only to fill rooms
# Weights (tuple): (unidirectional like, bidirectional like, maybe nope)
def createWeightedGraph(peoplePrefs, weights):
    graph = nx.Graph()
    for choosingPerson in peoplePrefs:
        graph.add_node(choosingPerson)
    for choosingPerson in peoplePrefs:
        for chosenPerson in peoplePrefs[choosingPerson][2]:
            if (choosingPerson, chosenPerson) in graph.edges():
                graph[choosingPerson][chosenPerson]["weight"] = weights[1]
            else:
                graph.add_edge(choosingPerson, chosenPerson, weight=weights[0])
        for noPerson in peoplePrefs[choosingPerson][3]:
            if (choosingPerson, noPerson) in graph.edges():
                graph[choosingPerson][noPerson]["weight"] = weights[2]
            else:
                graph.add_edge(choosingPerson, noPerson, weight=weights[2])
    return graph

def partGraphIntoRooms(graph, roomSize):
    if graph.number_of_nodes() == 0: return ()
    partitions = ceil(graph.number_of_nodes()/roomSize)
    graph.graph['edge_weight_attr'] = 'weight'
    (edgecuts, parts) = ms.part_graph(graph, partitions, recursive=True)
    print(edgecuts)
    print("Divided into", len(set(parts)), "parts. Goal:", partitions, "partitions.")
    return parts

#peoplePrefsRaw (dict): {Chooser:[Female, Male, Other/Prefer Not To Say,  Male, Male Only(M)/Female, Female Only(F), All okay(A), [People want to room with], [Ohp, maybe not people]]}
peoplePrefsRaw = genRandomPrefs(randomNames, genders, goptions)
# Easy Example:
#peoplePrefsRaw = {"J":[F,A,["L"],[]],"L":[M,A,["J"],[]],"K":[F,A,["M"],[]],"M":[M,A,["K"],[]],"H":[F,A,["J"],[]],"N":[M,A,["M"],[]]}
subGroups = {}
for genderPref in goptions:
    subGroups[genderPref] = {k:v for (k,v) in peoplePrefsRaw.items() if genderPref == v[1]}

# Balancing of people (removal of peeps from the "All" category and insertion into the M/F categories will be done by hand (it's quicker than writing code for it!))
peoplePerRoom = 4
for genderPref in goptions:
    peoplePrefs = subGroups[genderPref]
    graph = createWeightedGraph(subGroups[genderPref], (500,1000,0))
    rawParts = partGraphIntoRooms(graph, peoplePerRoom)
    print(rawParts)
    assign = {}
    print(graph.nodes())
    print(list(graph.nodes()))
    nodes = list(graph.nodes())
    for i, p in enumerate(rawParts):
        if p in assign:
            assign[p].append(nodes[i])
        else:
            assign[p] = [nodes[i]]
    print("\"", genderPref, "\" Room Assignments: ", assign)
