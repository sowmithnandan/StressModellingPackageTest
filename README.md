# StressModellingPackageTest

A sustainable system is one which survives or persists.
                                      - R. Costanza, B.C. Patten~Ecological Economics 15 (1995) 193-196
                                      
In this work, we work on the premise that "Sustainability is not a goal achievement problem but rather a state maintenance problem". 
We represent Sustainability of a system as a set of its capabilities and argue that sustainable development basically means sustainable 
improvement of capabilities.

The fact that a system settles down in a stable state (or comfort zone), also limits the system to its set of capabilities in that stable state. 
Some forms of capability enhancement interventions may serve to perturb a system/sub-system strongly enough that it
settles down into a different stable state, with a correspondingly different set of capabilities. 

We also postulate that when systems/sub-systems need to co-exist, their interactions tend to minimize differentials in their respective 
capabilities. Hence, if a province witnesses sudden economic growth, the neighbouring provinces also eventually witness some economic growth as well, and/or we
will witness an influx of people from the neighbouring provinces,thus reducing the per-capita economic gains.

We build a system considering most probable factors that have an affect on target. Later we intervene at some nodes and observe its impact on target.
After which we note the change in target post intervention on its neighbouring regions and observe its stability over time steps.

<!--Below are 2 usecases that attempts the above stated hypothesis.-->

* Usecase 1 :  Stress Modelling while constructing a system using bayesian networks.
  *  [Agroclimatic Zones](https://colab.research.google.com/drive/1wS3M9gEIb1UbWPoiXqMtnyW35dOBO1Tx?usp=sharing)
  * [Taluks](https://colab.research.google.com/drive/1eG0Oom91g0HBFEEGiqIAZ-cAlgB5kGkq?usp=sharing)
* Usecase 2 :  Stress Modelling considering an existing SDG system with its capability vectors
  * [Sates](https://colab.research.google.com/drive/1QIsjVz-semReDFIbY8LkF5KGkqloggTY?usp=sharing)

# DOCUMENTATION 
1. ```StressModellingPackageTest.DownloadAdjList(option, filePath)```

* Description:  The package has a few pre-loaded graphs which can be used by the users to conduct their simulations. This function downloads the adjacency lists of these graphs. The user can run his simulations on an updated tweaked version of a pre-loaded graph by downloading its adjacency list, changing it and then using it with the Make Graph function. 

* Parameters: 
	* ```Option```: integer(1,2,3)
		1. Adjacency list for Agro-Climatic zones of Karnataka 
		2. Adjacency list for the States of India 
		3. Adjacency list for Taluks of Karnataka
	* ```filePath```: string 
	 	 The location where the adjacency list gets downloaded. 
    
 <hr>

 2. ``` GraphCreator.MakeGraph(AfterInterventionFolder, adjList, function='L2 Norm', PreComputed=0, col_select=[2, 3], cat_bins=[1, 3, 4]) ```


* Description: This function creates the graph object incorporating the data of all the nodes in the After Intervention Folder, and the adjacency relations between the nodes. It initializes all the dimensions of the capability vector after scalarization over the categories given by the user.

* Parameters:
	* ```AfterInterventionFolder```: string, required <br>
    Path to the folder containing the data of all nodes after the intervention. The structure for the folder and node files can be found [here](). Please name the files in this folder as “<Nodename> after.xlsx”
    * ```adjList```:string <br>
Path to adjacency list excel. The format for the adjacency list can be obtained through the function ```StressModellingPackageTest.DownloadAdjList(option, filePath)``` or seen [here](https://github.com/sowmithnandan/StressModellingPackageTest/tree/main/data/After).
If a precomputed graph is being used, an empty string can be passed.
	* ```function```: string (“L2 Norm”, “ATE”, “Sum”) OR custom function name <br>
Picks the chosen scalarization function from the ```Scalrization``` class, to convert the categorical probabilities into a single value. If a custom function is defined, please follow the given format …

			
			def new_scalrize(valIter):
			 finalVal =0
			 for i in range(len(valIter)):
			   finalVal += (valIter[i]**i)
			 return (finalVal/len(valIter))
			

	* ```PreComputed```: integer (0,1,2,3) <br>
		0. User Defined adjacency list. In this case ```adjList`` must point to an accurate Adjacency File
		1. Adjacency list for Agro-Climatic zones of Karnataka 
		2. Adjacency list for the States of India 
		3. Adjacency list for Taluks of Karnataka

	* ```col_select```: list , default = [2,3] <br>

	* ```cat_bins```: list , default = [1,3,4] <br>
Zero-indexed list of columns representing categories the user wants to choose from the NodeFile
	
* Returned Values:
	* ```GraphCreator()``` object. <br>
     Returns the initialised graph to use in further steps.
Zero-indexed list of row numbers that the user wants to choose from the NodeFile as dimensions of the capability vector. 

<hr>

3. ```classStressModellingPackageTest.ResultObject(NodeDict, MeanSDGs, MeanStress, numRounds)```
* Parameteres: <br>
    * ```MeanSDGs```:  A list which stores the Mean SDG value of the graph in each iteration of Stress Modeling. Mean SDG is calculated as the sum of the mean of all dimensions of the capability vector of the node over all nodes. 
    * ```MeanStress```: A list which stores the Mean Stress of the Graph in each iteration of Stress Modelling. The mean Stress of a given graph is the sum of stress encountered by each graph
For a given node in the graph, the amount of stress experienced by it would depend on the sum of the L1 distance to all the neighbouring nodes in the graph.  
    * ```NodesDict```: It is a dictionary that maps the nodes to lists which store the capability vector of the node over the iterations of stress modelling.
    * ```TransposedNodesDict```: dict <br>
Another representation for the result object data. 
    * ```Visualize(var_no, node_list)``` <br>
Gives a bare ```matplotlib``` visualization of the result object.
        * Parameters:
            * ```var_no```: int, (0,1,2….) <br>
The index of the dimension to visualize in the capability vector 
            * ```node_list```: list of strings <br>
The list of node names, as strings, whose behaviour you want to visualize , over the iterations of stress modelling. 
                     
<hr>

4. ``` Class StressModellingPackageTest.Scalarization ```                      
This class groups several scalarization functions aimed at getting a single scalar value from the categories in NodeFiles. The three predefined scalarization functions are: 

``` 
ATE(valIter): 
finalVal =0 
       	for i in range(len(valIter)):
            finalVal += (valIter[i]*(i+1))
        	return (finalVal/3)
```
```
L2_Norm(valIter):
 	finalVal =0 
        	for i in range(len(valIter)):
finalVal += (valIter[i]**2)
        	return (finalVal**(0.5))

```
```
Sum(valIter):
finalVal =0 
        	for i in range(len(valIter)):
            finalVal += valIter[i]
        	return finalVal

```

* Returned Values:
	* ```finalValue```:float <br>
Scalarized value for a given dimension.

<hr>

5. ```StressModellingPackageTest.ShapetoAdjFile(shapeFile, filePath, NodeColName)```

Converts .shp files to an adjacency list excel file. 

* Parameters:
    * ```shapeFile```: string <br>
Path to the <>.shp file. The folder must also contain: 
    * ```filePath``` : string <br>
Path to the folder where new excel must be downloaded.
    * ```NodeColName```: string <br>
Column name in the shape file, from which node names should be picked. 

* Return Values: <br>
No values are returned. But a new file is added as ```filePath+"/shapeToAdjFrame.xlsx"```

<hr>

6. ```StressModellingPackageTest.StressModelling(Graph_objOriginal, numRounds, EpsilonStress, SM_function='gradient_descent ```

* Description:  
After an intervention, the nodes interact; and they tend to minimize differentials in their respective capabilities. Differentials in capabilities lead to stress modelled as L1 or L2 distances between capability vectors.  Stress modelling iteratively tries to minimize the stress a node feels w.r.t to its neighbourhood. The iterations stop when the Graph stress falls below a threshold or it reaches maximum iterations. 

* Parameters:
    * ```Graph_objOriginal: GraphCreator``` object which is already initialised
    * ```numRounds```:  int
	MAX iterations threshold set by user
    * ```EpsilonStress```: Threshold of graph stress. If total graph stress is below EpsilonStress, the iterations stop
    * ```SM_function```: The method by which the model moves towards minimum stress state. 

* Return Values:
    * ```resultObject```: ResultObject, Object of this class
    * ``` Graph_obj```: GraphCreator, Object of the class. 	
		Gives the graph object with data after stress modelling. Can be used to continue further rounds. The original graph is not affected. 

<hr>


7. ``` StressModellingPackageTest.Validate(AfterFolder, AdjFile) ```

Validates if the number of nodes in Adjacency List and NodeFiles are the same. 

* Parameters:
    * ```AfterFolder```: string
Location to the folder containing the NodeFiles
    * ```AdjFile```: string
Location of the file containing the Adjacency List

* Return values:
    * ```validate```: bool
Returns True if its the same number of nodes, else returns False. 

<hr>

8. ```StressModellingPackageTest.ViewAdjList()```

* Description: <br>
The package has a few pre-loaded graphs which can be used by the users to conduct their simulations. This function shows the adjacency lists of these graphs.  

* Parameters: <br>
 Option:  integer(1,2,3)
	1. Adjacency list for Agro-Climatic zones of Karnataka 
	2. Adjacency list for the States of India 
	3. Adjacency list for Taluks of Karnataka

* Return Types: <br>
Does not return anything. Just prints the required information

<hr>
	
<details><summary>Code example</summary><p>
  ...
</p></details>
