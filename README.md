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
 
