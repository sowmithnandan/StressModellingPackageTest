
# Stress Modelling

***A sustainable system is one which survives or persists***.[[R. Costanza, B.C. Patten~Ecological Economics 15 (1995) 193-196]](https://www.elgaronline.com/view/book/9781035303427/book-part-9781035303427-15.xml)
                                      

"Sustainability is not a goal achievement problem but rather a state maintenance problem". [[The Theory of Being : Systems Science from a Traditional Indian Perspective.]](https://books.google.co.in/books/about/The_Theory_of_Being.html?id=wAywxwEACAAJ&redir_esc=y)
We represent Sustainability of a system as a set of its capabilities and argue that sustainable development basically means sustainable 
improvement of capabilities.

<!--The fact that a system settles down in a stable state (or comfort zone), also limits the system to its set of capabilities in that stable state. 
Some forms of capability enhancement interventions may serve to perturb a system/sub-system strongly enough that it
settles down into a different stable state, with a correspondingly different set of capabilities.

We postulate that when systems/sub-systems need to co-exist, their interactions tend to minimize differentials in their respective 
capabilities. Hence, if a province witnesses sudden economic growth, the neighbouring provinces also eventually witness some economic growth as well, and/or we
will witness an influx of people from the neighbouring provinces,thus reducing the per-capita economic gains.-->

 We consider a system (built using bayesian networks or any existing system) for any target (target forms the capability vector), intervene at one or more variables and capture the capability vector post intervention.
 Through this work, We simulate policy interventions to understand the impact of it over time and to determine whether it is sustainable or not. It is useful to compare and contrast the effects of interventions across neighboring regions to assess sustainability.


<!--We build a system considering most probable factors that have an affect on target. Later we intervene at some nodes and observe its impact on target.
After which we note the change in target, post intervention on its neighbouring regions and observe its stability over time steps.-->




## Installation

Install my-project with pip

```bash
 pip install StressModellingPackageTest
```
    
## Documentation


<details><summary>Preface</summary><p>
  Build a bayesian network for a Target using [Netica](https://www.norsys.com/netica.html) or [bnlearn](https://pypi.org/project/bnlearn/) understanding the dependent and independent variables affecting the Target.

 To understand why Bayesian Networks and how to build one ? Refer to the paper "[Network Learning on Open Data to aid Policy Making"](https://ceur-ws.org/Vol-3211/CR_098.pdf)

 The targets from your bayesian network form the capability vector. When intervened at one or more variables, there will be change in capability vector. [[Refer to "A Data-driven Approach for Supporting Policy Intervention in Sustainable Development"]](https://ic-sd.org/wp-content/uploads/2022/11/submission_357.pdf)

</p></details>
 
## Code details
Using the ***Stress Modelling Package***, we simulate the effects of the intervention over its neighbouring regions and  time  simultaneously to assess for Sustainability.

1. Initialize the graph by loading the Capability Vector post intervention (  the values can be continous values or categorical) and the Neighbourhood graph (upload the adjacency list or ) upon which you wish to see the simulation.

 ``` GraphCreator.MakeGraph(AfterInterventionFolder, adjList, function='L2 Norm', PreComputed=0, col_select=[2, 3], cat_bins=[1, 3, 4]) ```


   *Description*: This function creates the graph object incorporating the data of all the nodes in the After Intervention Folder, and the adjacency relations between the nodes. It initializes all the dimensions of the capability vector after scalarization over the categories given by the user.

*Parameters*:
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

2. Make sure the no. of regions you built your bayesian network is equal to the nodes in your neighbourhood graph using the below method.

``` StressModellingPackageTest.Validate(AfterFolder, AdjFile) ```

Validates if the number of nodes in Adjacency List and NodeFiles are the same. 

* Parameters:
    * ```AfterFolder```: string
Location to the folder containing the NodeFiles
    * ```AdjFile```: string
Location of the file containing the Adjacency List

* Return values:
    * ```validate```: bool
Returns True if its the same number of nodes, else returns False. 

3. Perform Stress Modelling

```classStressModellingPackageTest.ResultObject(NodeDict, MeanSDGs, MeanStress, numRounds)```
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


## Examples

Below are 2 case studies worked out as part of project.

1. For Goal 2, Target 2.4 we have build a bayesian model considering the dependent and independent variables for 
improving yield for rice and wheat crops.[Target 2.4 - Crop Yield Model](https://kdl.iiitb.ac.in/a3-1-crop-yield/)

We considered intervening at **NPK Consumption** variable and simulated the intervention across Agro-climatic zones of Karnataka 

For details regarding implementation and results, please refer to the Collab notebook --> [Open in Colab](https://colab.research.google.com/drive/1wS3M9gEIb1UbWPoiXqMtnyW35dOBO1Tx?usp=sharing)

2. Another case study we attempted stress modelling considering the existing SDG framework is to understand an interventions impact other Indian states capability vector (vector curated with the composite scores of all 17 SDG's).

For details regarding implementation and results, please refer to the Collab notebook -->[Open in Colab](https://colab.research.google.com/drive/1QIsjVz-semReDFIbY8LkF5KGkqloggTY?usp=sharing)


## Acknowledgements

This work features a component of our ongoing project "[Karnataka Data Lake](https://avalokana.karnataka.gov.in/DataLake/DataLake)" on designing a [Big data based Policy Support System for Sustainable development](https://link.springer.com/chapter/10.1007/978-3-030-96600-3_1) in collaboration 
with  [Department of Planning and Statistics, Government of Karnataka, India](https://planning.karnataka.gov.in/english).




## Demo

[Video link]()


## Support

#### How to download/add/edit the Adjacency list of the neighbourhood graph?

Please check the below method :
```StressModellingPackageTest.DownloadAdjList(option, filePath)```

* Description:  The package has a few pre-loaded graphs which can be used by the users to conduct their simulations. This function downloads the adjacency lists of these graphs. The user can run his simulations on an updated tweaked version of a pre-loaded graph by downloading its adjacency list, changing it and then using it with the Make Graph function. 

* Parameters: 
	* ```Option```: integer(1,2,3)
		1. Adjacency list for Agro-Climatic zones of Karnataka 
		2. Adjacency list for the States of India 
		3. Adjacency list for Taluks of Karnataka
	* ```filePath```: string 
	 	 The location where the adjacency list gets downloaded.

#### How to scalarize categorical values for a target?


``` Class StressModellingPackageTest.Scalarization ```                      
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

#### How to create an Adjacency file for neighbourhood graph?

Please try and find the shape file of the region and convert it into Adjacency list using the below method.

```StressModellingPackageTest.ShapetoAdjFile(shapeFile, filePath, NodeColName)```

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

#### How to view the pre-computed Adjacency lists?

```StressModellingPackageTest.ViewAdjList()```

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

#### How can I visualize my results?
```classStressModellingPackageTest.ResultObject(NodeDict, MeanSDGs, MeanStress, numRounds)```
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


## Authors

- Arpitha Malavalli, Sowmith Nandan, Niharika Sri Parasa, Srinath Srinivasa

In case of quieries, please contact 
sowmith.nandan@iiitb.ac.in, arpitha.malavalli@iiitb.ac.in, niharikasri.parasa@iiitb.ac.in
