## Mettre dans le meme dossier que le rapport final


########################### Couleur ############################################################
colors1<-c( "#1D28E0","#C71000FF")
choix_pal <- "futurama"
col_ind <- "#008EA0FF"
col_var <- "#C71000FF"
col_bar <- "#8A419888"
logodark <- "#5A9599EE"
corail <- "#FF6348FF"
orange <- "#FF6F00FF"


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


############### Nettoyage de données ##########################################################
clean <- function(mon_df = mon_df){
  i = 1 # on initie i
  mon_vec <- c() # on crée le vecteur qui va récupérer les lignes a supprimer
  age <- select(mon_df, "age") # on choisit la variable age du df
  failures <- select(mon_df, "failures") # on choisit la variable failures du df
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


################## contribution des variables ##############################################
var_contrib <- function(acm = acm, axes = c(1,2), col.var = var, gradient.cols = NULL, ...){
  fviz_mca_var(acm, choice = "var.cat", axes = axes,
               invisible = "quali.sup", col.var = col.var, 
               repel = TRUE, labelsize = 3, ylim = c(-1,2),
               ggtheme = theme_minimal(), 
               gradient.cols = gradient.cols, ...)
}


################# Nuage de points des individus ###########################################
habillage <- function(x, n, axes = c(1,2)){
  fviz_mca_ind(x, geom="point", palette=choix_pal,
               axes= axes,
               habillage = n, alpha = 0.4,
               ggtheme = theme_minimal())
}


########### liste des graphiques du nuage de points des individus #########################
boucle_habillage <- function(acm = acm, n = n, axes = c(1, 2)){
  mon_vec <- list() ## creation liste
  for(i in 1:length(n)){
    graph_hab <- list(habillage(acm, n[i], axes = axes)) ## cree le graphique et le met en liste
    mon_vec <- append(mon_vec, graph_hab) ## ajoute graphique a la liste des graphiques
  }
  return(mon_vec) ## retourne la liste des graphiques
}


############ Pourcentage des valeurs propres et de la variance par dimension #############
pourcent_var_val_prop <- function(acm = acm, choix = "variance", sup = 10, ncp = 20){
  fviz_screeplot(acm, choice = choix, ncp = ncp,
                 main = paste("Percentage of explained", choix),
                 addlabels = TRUE, ylim = c(0, sup), ylab=" ",
                 barfill = col_bar, barcol="white")
}


################### Graphique des contributions ##########################################
contrib <- function(acm = acm, choix = "ind", axes = axes, ncol = NULL, nrow = NULL, taille = 8, top = Inf){
  if(length(axes) > 1){ ## si on donne un graphique de plusieurs axes
    i = 1 ## initialise 1
    mon_vec = list() ## initialise liste
    for(i in 1:length(axes)){
      cc <- fviz_contrib(acm, choice = choix, axes = axes[i], fill = col_ind,
                         color = col_ind, ggtheme = theme_classic(), top = top) +
        theme(axis.text.x = element_text(size = taille), title = element_text(size=9))
      cc <- list(cc) ## on cree le graphique et on le met sous forme de liste
      mon_vec <- append(mon_vec, cc) ## ajoute le graphique a la liste totale
      i = i + 1
    }
    ggarrange(plotlist = mon_vec, nrow = nrow, ncol = ncol) ## sort tous les graphiques
  }else{ ## si 1 seul graphique demande
    fviz_contrib(acm, choice = choix, axes = axes[1], fill = col_bar, color = col_bar,
                 ggtheme = theme_classic(), top = top) + 
      theme(axis.text.x = element_text(size = taille), title = element_text(size=9))
  }
}


############### Tableau du test du khi-deux pour AFC ##################################
test_khi_deux <- function(mon_df = mon_df, vec = vec, val_grade = val_grade, title = ""){
  ma_liste <- list() ## initialise liste
  for(i in 1:length(vec)){
    note <- mon_df$gradetot ## recupere moyenne
    contingence <- table(note, mon_df[, vec[i]]) ## cree tableau de contingence
    ma_liste <- append(ma_liste, suppressWarnings(chisq.test(contingence))$p.value)
    ## ajoute p-value du khi-deux a la liste
  }
  ma_liste <- unlist(ma_liste)
  col <- colnames(mon_df[, -val_grade]) ## definit nom des variables
  tab <- as.table(t(matrix(ma_liste)), nrow = 2) ## transforme liste en tableau
  colnames(tab) <- col
  rownames(tab) <- "p-value"
  tab_fun(tab, title = title) ## sort le tableau
}


############## tests avec p-values ###################################################
mod_classe <- function(CAH = CAH, nbr_classe = nbr_classe, sup = sup){
  i <- 1
  for(i in nbr_classe){
    classe<-as.data.frame(CAH$desc.var$category[i])[,-4]
    classe<-round(classe,2)
    colnames(classe) <- c("Cla/Mod", "Mod/Cla", "Global", "v.test")
    p.value <- as.data.frame(CAH$desc.var$category[i])[1:sup, 4]
    p.value<- format(p.value,scientific=T,digits = 4)
    sapply(i, function(x) assign(sprintf("classe_%1d", x),
                                 tab_fun(cbind(classe[1:sup,], p.value),  title = paste("Cluster", i)),
                                 envir = globalenv()))
  }
}