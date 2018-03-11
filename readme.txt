****************************************************************************
* README file for Prediction of Web Service QoS 
* Last updated: 2018/02/11
****************************************************************************

This gite describes a simple neural network (an autoencoder) by exploiting
cross-validation on a well-known dataset
The initial dataset is available for downloading at: 
http://wsdream.github.io/dataset/wsdream_dataset2.html

****************************************************************************
Important notes
****************************************************************************

1)After downloading the project, you need to unzip the following files:

dataset1.rar  				- located on /dataset/dataset1/
rtdata_updated.part000.rar  - located on /dataset/dataset2/slots/rtdata/
tpdata_updated.part000.rar  - located on /dataset/dataset2/slots/tpdata/

2)Customize the execution configuration, by updating the contents of params variable  	 

****************************************************************************
List of contents of the Project
****************************************************************************

rtdata.txt  - response-time values of 4,500 Web services when invoked by 142 
              service users over 64 time slices. Data format:
              User ID | Service ID | Time Slice ID | Response Time (sec)
              e.g.: 98    4352    33    0.311
tpdata.txt  - throughput values of 4,500 Web services when invoked by 142 
              service users in 64 time slices. Data format:
              User ID | Service ID | Time Slice ID | Throughput (kbps)
              e.g.: 91    1196    62    32.88
readme.txt  - descriptions of the dataset


1) Il faut decompresser les fichier :
									"./dataset/dataset1/dataset1.rar"
									"./dataset/dataset2/slots/rtdata/rtdata_max_density.partxxx.rar"
									"./dataset/dataset2/slots/rtdata/rtdata_update.partxxx.rar"
									"./dataset/dataset2/slots/tpdata/tpdata_max_density.partxxx.rar"
									"./dataset/dataset2/slots/tpdata/tpdata_update.partxxx.rar"

2) Executer le fichier validation.cross_validation.py (avec les paramètres adequats, voir ci-dessous)

validation.cross_validation.py	 --->Avant de lancer l'execution il faut verifier la variable "params" (au debut de ficchier)
									'dataDensity' = 76 ==> le deroulement se fera sur le data set yyMatrix_max_density_slot_xx.txt (valeurs nan remplacees si c'est possible) 
												  = 74 ==> le deroulement se fera sur le data set yyMatrix_updated_slot_xx.txt (les valeurs nan non pas etaient remplacees)
									'qosMetric'   = 0  ==> le deroulement s'effectura que pour la QoS response time
									   			  =	1  ==> le deroulement s'effectura que pour la QoS throughput
									'layer_sizes' =[120] ==> tableau pour specifier le nombre de neurones de la couche cachee (ici 120)
									   			  =[120,100,xx] ==> le deroulement se fait pour un autoencodeur avec 120 neurones cachees puis 100
									   			  					puis xx neurones sur la couche cachee	

autoencoders.auotencoder.py 	 --->create()			   --->Creation de lâ€™auto encodeur en specifiant le matrice dâ€™entee et
							   		 				 		   le nombre de neurones sur la couche cachee.
							   		  
						    	 --->get_rmse_mae_Vlaues() --->Calculs des RMSE et MAE relatifs aux meilleur modÃ¨le trouve dans
										  		 			   la phase dâ€™apprentissage
														  
														  
pretreatments.io_operations.py	 --->Actions relatives aux I/O operations sur le data set.
							   		  
pretreatments.neighborhooding.py --->Actions relatives aux operations sur le voisinage

pretreatments.treatments.py		 --->set_dataMatrixBySlot() 	--->Decomposition du data set par slot: rtdata_slot_xx.txt, tpdata_slot_xx.txt
																	Representation matricielle pour chaque slot: rtMatrix_slot_xx.txt, tpMatrix_slot_xx.txt

									 set_new_dataMatrixBySlot() --->Unification des matrices 142 X 4500 (ajout des utilisateurs et services manquants):
									 								rtMatrix_updated_slot_xx.txt, tpMatrix_updated_slot_xx.txt
									 
									 set_max_density_dataMatrixBySlot() -->Modification des nan valeurs : pour le slot XX on remplace la valeur
									 									   manquante par la moyenne de cette valeur sur tous les slots qui precèdent 
									 									   le slot actuel
									 									   rtMatrix_max_density_slot_xx.txt, tpMatrix_max_density_slot_xx.txt
									 									   
	    
						    

