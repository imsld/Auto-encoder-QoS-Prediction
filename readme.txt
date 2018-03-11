****************************************************************************
* README file for Prediction of Web Service QoS 
* Last updated: 2018/02/11
****************************************************************************

This gite contains a simple neural network (an autoencoder) by exploiting
cross-validation on a well-known dataset
The initial dataset is available for downloading at: 
http://wsdream.github.io/dataset/wsdream_dataset2.html

****************************************************************************
Important notes
****************************************************************************

1)After downloading the project, you need to unzip the following files:

dataset1.rar  		- located on /dataset/dataset1/
rtdata_updated.part001.rar  - located on /dataset/dataset2/slots/rtdata/
tpdata_updated.part001.rar  - located on /dataset/dataset2/slots/tpdata/
rtdata_max-density.part001.rar  - located on /dataset/dataset2/slots/rtdata/
tpdata_max-density.part001.rar  - located on /dataset/dataset2/slots/tpdata/


2)Customize the execution configuration, by updating the contents of params 
variable located in "/validation/cross_validation.py" file. Especially we 
have to change the following values :  	 

dataDensity	-takes two values possible : 76/74
		 	76 for selecting the max density slots in training/testing 
		 	the auto encoder. The density of data set is 76%.
		 	74 for selecting the updated slots in training/testing 
		 	the auto encoder. The density of data set is 74%. 
		 	the max density slots are located in :
		 	/dataset/dataset2/slot/yydata/yyMatrix_max_density_slot_xx.txt		 	 
		 	the updated slots are located in :
		 	/dataset/dataset2/slot/yydata/yyMatrix_updated_slot_xx.txt
		 	yy : rt/tp
		 	xx : 0/1/.../63     

qosMetric	-takes two values possible :
			 	0 for selecting only the response time QoS
			 	1 for selecting only the throughput QoS

layer_sizes	-it is a array that specifies the number of neurons in hidden layer   

****************************************************************************
List of contents of the Project
****************************************************************************

ICWS18		- Folder containing the source article for ICWS conference 
              
results		- Folder containing the results of execution

dataset		- Folder containing the updated data set

readme.txt  - descriptions of the project