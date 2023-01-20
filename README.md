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

Below are 2 usecases that attempts the above stated hypothesis.

* Usecase 1 :  Stress Modelling while constructing a system using bayesian networks.
  *  [Agroclimatic Zones](https://colab.research.google.com/drive/1wS3M9gEIb1UbWPoiXqMtnyW35dOBO1Tx?usp=sharing)
  * [Taluks](https://colab.research.google.com/drive/1eG0Oom91g0HBFEEGiqIAZ-cAlgB5kGkq?usp=sharing)
* Usecase 2 :  Stress Modelling considering an existing SDG system with its capability vectors
  * [Sates](https://colab.research.google.com/drive/1QIsjVz-semReDFIbY8LkF5KGkqloggTY?usp=sharing)

# DOCUMENTATION 
*
```
StressModellingPackageTest.DownloadAdjList(option, filePath)
```

	* Description:  The package has a few pre-loaded graphs which can be used by the users to conduct their simulations. This function downloads the adjacency lists of these graphs. The user can run his simulations on an updated tweaked version of a pre-loaded graph by downloading its adjacency list, changing it and then using it with the Make Graph function. 

	* Parameters: 
		* ```Option```: integer(1,2,3)
			1. Adjacency list for Agro-Climatic zones of Karnataka 
			2. Adjacency list for the States of India 
			3. Adjacency list for Taluks of Karnataka
		* ```filePath```: string 
	 	 The location where the adjacency list gets downloaded. 
    
 <hr>
 *
```
GraphCreator.MakeGraph(AfterInterventionFolder, adjList, function='L2 Norm', PreComputed=0, col_select=[2, 3], cat_bins=[1, 3, 4])[source]
```

	* Description: This function creates the graph object incorporating the data of all the nodes in the After Intervention Folder, and the adjacency relations between the nodes. It initializes all the dimensions of the capability vector after scalarization over the categories given by the user.

	* Parameters:
		* ```AfterInterventionFolder```: string, required
Path to the folder containing the data of all nodes after the intervention. The structure for the folder and node files can be found [here](). Please name the files in this folder as “<Nodename> after.xlsx”
		* ```adjList```:string
Path to adjacency list excel. The format for the adjacency list can be obtained through the function 
		*```StressModellingPackageTest.DownloadAdjList(option, filePath)``` or seen [here](https://github.com/sowmithnandan/StressModellingPackageTest/tree/main/data/After).
If a precomputed graph is being used, an empty string can be passed.
		* ```Function````:string (“L2 Norm”, “ATE”, “Sum”) OR custom function name
Picks the chosen scalarization function from the ```Scalrization``` class, to convert the categorical probabilities into a single value. If a custom function is defined, please follow the given format …

			```
			def new_scalrize(valIter):
			 finalVal =0
			 for i in range(len(valIter)):
			   finalVal += (valIter[i]**i)
			 return (finalVal/len(valIter))
			```

		* ```PreComputed```: integer (0,1,2,3)
			0. User Defined adjacency list. In this case ```adjList`` must point to an accurate Adjacency File
			1. Adjacency list for Agro-Climatic zones of Karnataka 
			2. Adjacency list for the States of India 
			3. Adjacency list for Taluks of Karnataka

		* ```col_select```: list , default = [2,3]

		* ```cat_bins```: list , default = [1,3,4]
Zero-indexed list of columns representing categories the user wants to choose from the NodeFile
	
* Returned Values:
		* ```GraphCreator()``` object. Returns the initialised graph to use in further steps.
Zero-indexed list of row numbers that the user wants to choose from the NodeFile as dimensions of the capability vector. 

<hr>
