################ Import ###########################
source("fonctions.R")
data_mat <- read.csv("student-mat.csv", sep= ";")
data_por <- read.csv("student-por.csv", sep= ";")

############## creation moyenne ###################
data_mat$moyenne = (data_mat$G1 + data_mat$G2 + data_mat$G3)/3
data_por$moyenne = (data_por$G1 + data_por$G2 + data_por$G3)/3

############## creation matiere ###################
data <- rbind(data_mat, data_por)
data$matiere <- "math"
data$matiere[c(396:1044)] <- "portugais"

############# nettoyage variable age ##############
data_mat <- clean(data_mat)
data_por <- clean(data_por)
data <- clean(data)

############ variable traveltime #################
data$traveltime[data$traveltime==1] <- "trav < 15"
data$traveltime[data$traveltime==2] <- "trav 15-30"
data$traveltime[data$traveltime==3] <- "trav 30-1h"
data$traveltime[data$traveltime==4] <- "trav > 1h"

############ variable studytime ##################
data$studytime[data$studytime==1] <- "stud < 2h"
data$studytime[data$studytime==2] <- "stud 2-5h"
data$studytime[data$studytime==3] <- "stud 5-10h"
data$studytime[data$studytime==4] <- "stud > 10h"

############ variable Medu #######################
data$Medu[data$Medu == "0"] <- "niveau 0"
data$Medu[data$Medu == "1"] <- "niveau 1"
data$Medu[data$Medu == "2"] <- "niveau 2"
data$Medu[data$Medu == "3"] <- "niveau 3"
data$Medu[data$Medu == "4"] <- "niveau 4"

########### variable Fedu ########################
data$Fedu[data$Fedu == "0"] <- "niveau 0"
data$Fedu[data$Fedu == "1"] <- "niveau 1"
data$Fedu[data$Fedu == "2"] <- "niveau 2"
data$Fedu[data$Fedu == "3"] <- "niveau 3"
data$Fedu[data$Fedu == "4"] <- "niveau 4"

########### variable famrel #####################
data$famrel[data$famrel == "1"] <- "Très mauvaise"
data$famrel[data$famrel == "2"] <- "Mauvaise"
data$famrel[data$famrel == "3"] <- "Moyenne"
data$famrel[data$famrel == "4"] <- "Bonne"
data$famrel[data$famrel == "5"] <- "Très bonne"


########### variable classe #####################
for (i in 1:nrow(data)){
  if(data$age[i] - data$failures[i] == 15){data$classe[i] <- "10eme"}
  else if(data$age[i] - data$failures[i] == 16){data$classe[i] <- "11eme"}
  else if(data$age[i] - data$failures[i] %in% c(17, 18)){data$classe[i] <- "12eme"}
}

########### variable absence ####################
data$absences <- as.factor(cut(
  data$absences, c(0, 5, 10, 75), 
  labels = c("abs [0,5]", "abs ]5,10]", "abs ]10,75]"),
  include.lowest = TRUE)
  )

######### variable failures #####################
data$failures[data$failures==2] <- "2 ou 3"
data$failures[data$failures==3] <- "2 ou 3"

######## variable moyenne ###############
data$moyenne_facteur <- cut(
  data$moyenne, c(0, 5, 10, 15, 20),
  labels=c("moy [0,05]", "moy ]05,10]", "moy ]10,15]", "moy ]15,20]")
  )

######### creation df que l'on va utiliser #####################
data_nettoye <- data[, -c(3, 31:34)]
for (i in 1:31){data_nettoye[, i] <- as.factor(data_nettoye[, i])}
