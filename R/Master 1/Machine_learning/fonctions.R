############### Nettoyage de données ##########################################################
clean <- function(mon_df = mon_df){
  i = 1 # on initie i
  mon_vec <- c() # on crée le vecteur qui va récupérer les lignes a supprimer
  age <- dplyr::select(mon_df, "age") # on choisit la variable age du df
  failures <- dplyr::select(mon_df, "failures") # on choisit la variable failures du df
  for (i in 1:nrow(mon_df)) { # boucle pour recuperer les lignes du df a supprimer
    if (age[i,] - failures[i, ] < 15) {
      mon_vec <- append(mon_vec, i)
    }
    if (age[i,] - failures[i, ] > 20) {
      mon_vec <- append(mon_vec, i)
    }  
  }
  mon_df[-mon_vec,] # on supprime les lignes du df
}


########################## Tableau ############################################################
# si above = TRUE on a un header_above
tab_fun <- function(tab, above = FALSE, title = title, font_size = 10, header = NULL){
  if(above){
    tab %>% kable(caption = title) %>%
      kable_styling(font_size = font_size, full_width=FALSE, stripe_color = "lightgray", stripe_index = 0,
                    latex_options = c("HOLD_position", "striped"), position = "center") %>%
      add_header_above(header = header, bold=TRUE, color="red")%>%
      column_spec(1, bold=T) %>%
      row_spec(0, bold=T)
  } else {
    tab %>% kable(caption = title) %>%
      kable_styling(font_size = font_size, full_width=FALSE, stripe_color = "lightgray", stripe_index = 0,
                    latex_options = c("HOLD_position", "striped"), position = "center") %>%
      column_spec(1, bold=T) %>%
      row_spec(0, bold=T)
  }
}

################# Matrice de Cramer pour corrplot ############################################
cv <- function(x, y) {
  t <- table(x, y)
  chi <- suppressWarnings(chisq.test(t))$statistic
  cramer <- sqrt(chi / (length(x) * (min(dim(t)) - 1)))
  cramer
}

cramer.matrix<-function(y, fill = TRUE){
  col.y<-ncol(y)
  V<-matrix(ncol=col.y,nrow=col.y)
  for(i in 1:(col.y - 1)){
    for(j in (i + 1):col.y){
      V[i,j]<-cv(pull(y,i),pull(y,j))
    }
  }
  diag(V) <- 1 
  if (fill) {
    for (i in 1:ncol(V)) {
      V[, i] <- V[i, ]
    }
  }
  colnames(V)<-names(y)
  rownames(V)<-names(y)
  V
}

