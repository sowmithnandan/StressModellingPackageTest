import pandas as pd
import pkg_resources
import copy
import math
# !pip install networkx[default]
# !pip install matplotlib==3.1.3
import networkx as nx
import numpy as np
np.random.seed(1000)
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import os 
import geopandas as gpd

DATA_PATH = pkg_resources.resource_filename('StressModellingPackageTest', 'data/')
# print("DATA_PATH within the package to the data is :",DATA_PATH)

class Scalarization:
    def __init__(self):
        pass
    
    def L2_Norm(self,valIter):
        finalVal =0 
        for i in range(len(valIter)):
            finalVal += (valIter[i]**2)
        return (finalVal**(0.5))
        # return (val1**2+val2**2+val3**3)**(0.5)

    def ATE(self,valIter):
        finalVal =0 
        for i in range(len(valIter)):
            finalVal += (valIter[i]*(i+1))
        return (finalVal/3)
        
    def Sum(self,valIter): # returns same val for single item
        finalVal =0 
        for i in range(len(valIter)):
            finalVal += valIter[i]
        return finalVal


    def getFunction(self,selection="L2 Norm"):
        if selection=="L2 Norm":
            return self.L2_Norm
        elif selection == "ATE":
            return self.ATE
        elif selection == "Sum":
            return self.Sum
        return selection

#add more here

class GraphCreator:
    AfterInterventionFile = "" 
    adjList = ""
    PreComputed = 0
    def getMeanSDGGraph2(self,label):
        meanSDG = 0
        for n in self.G.nodes():
            meanSDG += np.mean(np.array(self.G.nodes[n][label]))
        return meanSDG / self.values.no_attri

    def getGraphStress2(self,label):
        for n in self.G.nodes():
            nodeStress = 0
            neigList = list(self.G.neighbors(n))
            for nei in neigList:
                a = np.array(self.G.nodes[n][label])
                b = np.array(self.G.nodes[nei][label])
                nodeStress += np.linalg.norm((a - b), ord=1)
            self.G.nodes[n]["nodesStress"] = nodeStress
            
        stress = 0
        for n in self.G.nodes():
            stress += self.G.nodes[n]["nodesStress"]
        return stress

    def __init__(self):
        pass

    def MakeGraph(self,AfterInterventionFolder,adjList,function ="L2 Norm",PreComputed=0,col_select =[2,3],cat_bins=[1,3,4]):
        self.PreComputed = PreComputed
        if(self.PreComputed==1):
            self.adjList = DATA_PATH+"PreComputedGraphs/Adjacent list ac zones.xlsx"
        elif(self.PreComputed==2):
            self.adjList = DATA_PATH+"PreComputedGraphs/States_Neighbors.xlsx" 
        elif(self.PreComputed==3):
            self.adjList = DATA_PATH+"PreComputedGraphs/TalukAdjacencyFrame.xlsx"
        else:
            self.adjList =adjList
        self.AfterInterventionFile = AfterInterventionFolder
        self.col_select = col_select
        self.cat_bins = cat_bins
        self.function = function
        self.scalrization_func=Scalarization().getFunction(function)
        self.values=Values(self.AfterInterventionFile,self.adjList,self.col_select,self.cat_bins,self.scalrization_func)
        if(self.values.flag==False):
            return False
        self.G= nx.Graph()
        self.init_graph_attr1()
        return self

    def updateValues(self,Graph):
        for node_no in range(Graph.values.no_nodes):
            self.values.node_attri_dict[self.values.node_list[node_no]]= Graph.G.nodes[node_no]["sdgvec"]
    
    def init_graph_attr1(self): 
        nodeAttr = {}
        self.init_graph1()
        for i in range(self.values.no_nodes):
            temp = {}
            # temp['OldDeltaVector'] = np.zeros(2)
            temp["DeltaVectornodesStress"] = 0 
            # temp['NewDeltaVector'] = np.zeros(2)
            temp["sdgvec"] = self.values.node_attri_dict[self.values.node_list[i]]
            temp["tempsdgvec"] = self.values.node_attri_dict[self.values.node_list[i]]
            temp["oldsdgvec"] = self.values.node_attri_dict[self.values.node_list[i]]
            temp["nodesStress"] = 0
            temp["meansdg"] = np.mean(self.values.node_attri_dict[self.values.node_list[i]])
            temp["name"] = self.values.node_list[i]
            nodeAttr[i] = temp
        print(nodeAttr)
        nx.set_node_attributes(self.G, nodeAttr)

    def init_graph1(self): #states is a dataframe
        self.G.add_nodes_from([i for i in range(0,self.values.no_nodes)])
        labels = {}
        labels = self.values.node_adj_frame.columns
        print(labels)
        print(self.values.node_adj_frame)
        for i in range(self.values.no_nodes):
            snode=  self.values.node_adj_frame[labels[0]][i]-1
            temp = self.values.node_adj_frame[labels[2]][i]
            if ',' in str(temp):
                sedge_arr=temp.split(',')
                for i in range(0,len(sedge_arr)):
                    self.G.add_edge(snode,int(sedge_arr[i])-1)  
            elif temp==np.nan:
                print("ERROR:None found in th adjacency excel sheet")
            else :
                self.G.add_edge(snode,int(temp)-1)
        return
     
class Values:
    def __init__(self, AfterFolder, AdjFile,col_select,cat_bins,sclarisation_func):
        self.AfterFolder = AfterFolder
        self.AdjFile=AdjFile
        self.col_select=col_select
        self.cat_bins=cat_bins
        self.sclarisation_func=sclarisation_func
        self.node_list=[]
        self.attr_list =[]
        self.node_attri_dict=[]
        self.node_adj_frame = None
        self.no_nodes =None
        self.no_attri = None
        self.flag=self.populate_after()
        

    def preprocess(self,Folder): # col_select =[2,3]
        df = pd.DataFrame()
        attribute_dict={}
        for filename in os.listdir(Folder):
            cntr=0
            self.node_list.append(filename.split(" ")[0])
            tempExcel = pd.read_excel(Folder+"/"+filename)
            if cntr==0:
                for i in self.col_select:
                    attribute_dict[tempExcel.iloc[i][0]]=[]
                self.attr_list=attribute_dict.keys()
                cntr+=1
        self.no_nodes=len(self.node_list)
        self.no_attri=len(self.attr_list)
        for filename in os.listdir(Folder):
            tempExcel = pd.read_excel(Folder+"/"+filename)
            for j in self.col_select: 
                CategoryProbabilitesList = []
                for k in self.cat_bins:
                    CategoryProbabilitesList.append(float(tempExcel.iloc[j][k]))
                scalarvalue = self.sclarisation_func(CategoryProbabilitesList)
                attribute_dict[tempExcel.iloc[j][0]].append(scalarvalue)
        df["Nodes"] = self.node_list
        for attribute in self.attr_list:
            df[attribute] = attribute_dict[attribute]  
        return df

    def populate_after(self):
        #df = pd.read_excel(BeforeATEFile)
        df= self.preprocess(self.AfterFolder)
        df['sdgvec'] = df[self.attr_list].values.tolist()
        self.node_attri_dict = dict(zip(df["Nodes"], df.sdgvec))
        # df2['sdgvec'] = df2[attribute_list].values.tolist()
        self.node_adj_frame=pd.read_excel(self.AdjFile)
        if(Validate(self.AfterFolder,self.AdjFile)==False):
                print("No of Nodes do not Match")
                return False
        else:
            return True


def StressModelling(Graph_objOriginal,numRounds,EpsilonStress,SM_function ="gradient_descent"):
        # BeforeInterventionFolder,AfterInterventionFolder,adjList,function ="L2 Norm",PreComputed=0,col_select =[2,3]
        graphCreatorObj = GraphCreator()
        Graph_obj = graphCreatorObj.MakeGraph(Graph_objOriginal.AfterInterventionFile,
                                            Graph_objOriginal.adjList,
                                            Graph_objOriginal.function,
                                            Graph_objOriginal.PreComputed,
                                            Graph_objOriginal.col_select,
                                            Graph_objOriginal.cat_bins)
        NodesDict = {}
        for i in Graph_obj.values.node_list:
            NodesDict[i] = []
        MeanSDGs = []
        MeanStress = [] 
        for i in range(numRounds):
            temp1 = Graph_obj.getMeanSDGGraph2("sdgvec")
            temp2 = Graph_obj.getGraphStress2("sdgvec")
            MeanSDGs.append(temp1)
            MeanStress.append(temp2)
            for n in Graph_obj.G.nodes():
                NodesDict[Graph_obj.G.nodes[n]["name"]].append(Graph_obj.G.nodes[n]["sdgvec"])
            if temp2>=EpsilonStress:
                func1=StressReduction().getFunction(SM_function)
                func1(Graph_obj.G,"sdgvec" ,"tempsdgvec",Graph_obj.values.no_attri)
            else:
                print(i,"stress less than epsilon")
                break
        for n in Graph_obj.G.nodes(): 
            NodesDict[Graph_obj.G.nodes[n]["name"]].append(Graph_obj.G.nodes[n]["sdgvec"])
        Graph_obj.updateValues(Graph_obj)
        resultObject = ResultObject(NodesDict,MeanSDGs,MeanStress,numRounds)
        return resultObject,Graph_obj

class ResultObject:
    NodesDict = None
    MeanSDGs = None
    MeanStress = None
    TransposedFlag = False
    TransposedNodesDict =None
    nodesList = None 
    def __init__(self, NodeDict,MeanSDGs,MeanStress,numRounds):
        self.NodesDict = NodeDict
        self.MeanSDGs = MeanSDGs
        self.MeanStress = MeanStress
        self.numRounds = numRounds

    def returnTranspose(self):
        if(self.TransposedFlag):
            return self.TransposedNodesDict
        self.nodesList = list(self.NodesDict.keys())
        self.TransposedFlag = True
        numberOfItr = len(self.NodesDict[self.nodesList[0]])
        self.TransposedNodesDict = { }
        for i in range(numberOfItr):
            self.TransposedNodesDict[str(i)] = {}
            for j in range(1,len(self.NodesDict[self.nodesList[0]][0])+1):
                self.TransposedNodesDict[str(i)]["var"+str(j)] = [] 
        for keys in self.NodesDict:
            for i in range(len(self.NodesDict[keys])):
                for j in range(len(self.NodesDict[keys][i])):
                    self.TransposedNodesDict[str(i)]["var"+str(j+1)].append(self.NodesDict[keys][i][j])
        return self.TransposedNodesDict

    def Visualize(self,var_no,node_list):
        for node in self.NodesDict.keys():
            if node in node_list:
                temp_list=[]
                for l in self.NodesDict[node]:
                    if var_no > len(l):
                        print ("ERROR:Attribute number is inaccurate")
                        return
                    temp_list.append(l[var_no-1])
                plt.plot(range(self.numRounds+1),temp_list,label=str(node))
        plt.xlabel("Time Steps")
        plt.ylabel("Attribute value over timesteps")
        plt.legend()
        plt.show()
                

class StressReduction:
    def __init__(self) -> None:
        pass

    def Gradient_Descent(self,G,label1,label2,numSDG):
        for n in G.nodes():
            nodeStress = 0
            neigList = list(G.neighbors(n))
            a = np.zeros(numSDG)
            for nei in neigList:
                a = np. add(a,np.array(G.nodes[nei][label1]))
            if len(neigList)!=0:
                a = a/len(neigList)
                G.nodes[n][label2] = np.add(G.nodes[n][label2],np.add(a,-1*np.array(G.nodes[n][label1]))).tolist()
        for n in G.nodes():
            G.nodes[n][label1] = G.nodes[n][label2].copy()
        return 
    
    def getFunction(self,SM_function):
        if SM_function=="gradient_descent":
            return self.Gradient_Descent
        return SM_function

def CreateGraph(AfterInterventionFolder,adjList,function,PreComputed):
    Graph_obj =  GraphCreator().MakeGraph(AfterInterventionFolder=AfterInterventionFolder,adjList=adjList,function=function,PreComputed=PreComputed)
    return Graph_obj

# Test CODE
def Validate(AfterFolder,AdjFile):
    a,c=0,0
    print("No of Nodes in AdjFile")
    df=pd.read_excel(AdjFile)
    a=df.shape[0]
    print(a)
    print("No of Nodes in After Intervention Folder")
    c=len(os.listdir(AfterFolder))
    print(c)
    return a==c

def ATEFunction1(a):
  return sum(a)
  
def ViewAdjList():
    print("Option PreComputed=1, Agroclimatic zone in Karnataka")
    adjList = DATA_PATH+"PreComputedGraphs/Adjacent list ac zones.xlsx"
    df=pd.read_excel(adjList)
    print(df)
    print("-------------------------------------------")
    print("Option PreComputed=2, States Neighbours for SDG in India")
    adjList = DATA_PATH+"PreComputedGraphs/States_Neighbors.xlsx"
    df=pd.read_excel(adjList)
    print(df)
    print("-------------------------------------------")
    print("Option PreComputed=3, Taluk adjacency list")
    adjList = DATA_PATH+"PreComputedGraphs/TalukAdjacencyFrame.xlsx"
    df=pd.read_excel(adjList)
    print(df)
    print("-------------------------------------------")


def DownloadAdjList(option,filePath):
    if(option==1):
        adjList = DATA_PATH+"PreComputedGraphs/Adjacent list ac zones.xlsx"
    elif(option==2):
        adjList = DATA_PATH+"PreComputedGraphs/States_Neighbors.xlsx"
    elif(option==3):
        adjList = DATA_PATH+"PreComputedGraphs/TalukAdjacencyFrame.xlsx"
    else: 
        print("Option entered is not valid")
        return 0
    df=pd.read_excel(adjList)
    df.to_excel(filePath)
    return 1

#Standalone to generate shape file and download
def ShapetoAdjFile(shapeFile,filePath,NodeColName):
    gdf = gpd.read_file(shapeFile)
    gdf["NEIGHBORS"] = None  

    for index, country in gdf.iterrows():   

        # get 'not disjoint' countries
        neighbors = gdf[~gdf.geometry.disjoint(country.geometry)][NodeColName].tolist()

        # remove own name of the country from the list
        neighbors = [ name for name in neighbors if country[NodeColName] != name ]

        # add names of neighbors as NEIGHBORS value
        gdf.at[index, "NEIGHBORS"] = ", ".join(neighbors)
    taluk_index_dict={}
    for i in range(len(gdf[NodeColName])):
        print(gdf[NodeColName][i])
        taluk_index_dict[gdf[NodeColName][i]]=i+1

    print(taluk_index_dict)
    final_L =[]
    for i in range(len(gdf["NEIGHBORS"])):
        l_temp= gdf["NEIGHBORS"][i].split(", ")
        l=list(map(lambda x: str(taluk_index_dict[x]),l_temp))
        print(l)
        final_L.append(",".join(l))
    gdf["NEIGHBORS_new"] = final_L
    df_new =pd.DataFrame()
    df_new=gdf.filter([NodeColName,'NEIGHBORS_new'], axis=1)
    df_new["S.NO"]=[_ for _ in range(1,len(taluk_index_dict)+1)]
    df_new=df_new[["S.NO",NodeColName,'NEIGHBORS_new']]
    # save GeoDataFrame as a new file
    print(df_new)
    df_new.to_excel(filePath+"/shapeToAdjFrame.xlsx",index=False)


# Test CODE 

# Graph_obj1= CreateGraph(BeforeInterventionFolder=r"./data/Before",AfterInterventionFolder=r"./data/After",adjList=r"./data/Adjacent list ac zones.xlsx",function="L2 Norm",PreComputed=1)

# print(Graph_obj1.values.node_attri_dict)
# print(Graph_obj1.G.nodes[0])
# print(graphUpdated1.values.node_attri_dict)
# print(graphUpdated1.G.nodes[0])












