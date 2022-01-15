#Load required libraries
library(xgboost)
library(glmnet)
library(caret)

########################
#  Read in Train Data  #
########################
train = read.csv("train.csv") 

#Train data without "PID" and "Sale_Price"
train.x = train[, 2:(ncol(train)-1)]

#log transformed "Sale_Price" - Train Labels
train.y = log(train[, "Sale_Price"])        

##########################
# PRE-PROCESS TRAIN DATA #
##########################
#replace missing values in Garage_Yr_Blt column with 0's
train.x$Garage_Yr_Blt[is.na(train.x$Garage_Yr_Blt)] = 0


###################### 
#  XGBOOST TRAINING  #
######################
categorical.varsX <- colnames(train.x)[which(sapply(train.x, function(x) mode(x)=="character"))]
train.matrixX <- train.x[, !colnames(train.x) %in% categorical.varsX, drop=FALSE]

DummyVarsX = data.frame(varName = NULL, mLevels=NULL)
n.trainX <- nrow(train.matrixX)

#Add columns for categorical variables
for(var in categorical.varsX){
        mylevelsX <- sort(unique(train.x[, var]))
        mX <- length(mylevelsX)
        mX <- ifelse(mX>2, mX, 1)
        tmp.trainX <- matrix(0, n.trainX, mX)
        col.namesX <- NULL
        for(j in 1:mX){
                tmp.trainX[train.x[, var]==mylevelsX[j], j] <- 1
                col.namesX = c(col.namesX, paste(var, '_', mylevelsX[j], sep=''))
        }
        colnames(tmp.trainX) <- col.namesX
        DummyVarsX = rbind(DummyVarsX, data.frame(varName = var, mLevels = mylevelsX))
        train.matrixX <- cbind(train.matrixX, tmp.trainX)
}

set.seed(6590)
dtrain = xgb.DMatrix(data = as.matrix(train.matrixX), label= train.y)

param1 = list(eta=0.05,
              gamma=0,
              max_depth=6, 
              subsample=.5)

#xgboost model training
xgb_mod <- xgb.train(data = dtrain,  params=param1, nrounds = 700)


#############################
#   glmnet model training   #
#############################
remove.var <- c('Street', 'Utilities',  'Condition_2', 'Roof_Matl', 'Heating', 'Pool_QC', 'Misc_Feature', 'Low_Qual_Fin_SF', 'Pool_Area', 'Longitude', 'Latitude')
train.xG = train.x[,!colnames(train.x) %in% remove.var, drop=FALSE]

#Apply winsorization to a few variables to account for extreme values
winsor.vars <- c("Lot_Frontage", "Lot_Area", "Mas_Vnr_Area", "BsmtFin_SF_2", "Bsmt_Unf_SF", "Total_Bsmt_SF", "Second_Flr_SF", 'First_Flr_SF', "Gr_Liv_Area", "Garage_Area", "Wood_Deck_SF", "Open_Porch_SF", "Enclosed_Porch", "Three_season_porch", "Screen_Porch", "Misc_Val")

varWins = data.frame(varName = NULL, myQuan = NULL)
quan.value <- 0.95
for(var in winsor.vars){
        tmp = train.xG[, var]
        myquan = quantile(tmp, probs = quan.value, na.rm = TRUE)
        tmp[tmp > myquan] = myquan
        train.xG[, var] = tmp
        varWins = rbind(varWins, data.frame(varName = var, myQuan = myquan))
}

categorical.varsG = colnames(train.xG)[which(sapply(train.xG, function(x) mode(x)=="character"))]
train.matrixG <- train.xG[, !colnames(train.xG) %in% categorical.varsG, drop=FALSE]

DummyVarsG = data.frame(varName = NULL, mLevels=NULL)
n.trainG <- nrow(train.matrixG)
for(var in categorical.varsG){
        mylevelsG <- sort(unique(train.xG[, var]))
        mG <- length(mylevelsG)
        mG <- ifelse(mG>2, mG, 1)
        tmp.trainG <- matrix(0, n.trainG, mG)
        col.namesG <- NULL
        for(j in 1:mG){
                tmp.trainG[train.xG[, var]==mylevelsG[j], j] <- 1
                col.namesG = c(col.namesG, paste(var, '_', mylevelsG[j], sep=''))
        }
        colnames(tmp.trainG) <- col.namesG
        DummyVarsG = rbind(DummyVarsG, data.frame(varName = var, mLevels = mylevelsG))
        train.matrixG <- cbind(train.matrixG, tmp.trainG)
}

set.seed(6590)
GLM.out = cv.glmnet(as.matrix(train.matrixG), train.y, 
                    lambda = c(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1), alpha = 0.2)


########################
#  Read in Test Data   #
########################
test = read.csv("test.csv")

#Test data without "PID" and "Sale_Price" ("Sale_Price" shouldn't be in the file)
test.x = test[, 2:ncol(test)]

#########################
# PRE-PROCESS TEST DATA #
#########################
#replace missing values in Garage_Yr_Blt column with 0's
test.x$Garage_Yr_Blt[is.na(test.x$Garage_Yr_Blt)] = 0

###########################
#    XGBoost Prediction   #
###########################
test.matrixX <- test.x[, !colnames(test.x) %in% categorical.varsX, drop=FALSE]

n.testX <- nrow(test.matrixX)
for(var in categorical.varsX){
        mylevels = sort(unique(DummyVarsX[DummyVarsX[, 'varName'] == var, 'mLevels']))
        m <- length(mylevels)
        m <- ifelse(m>2, m, 1)
        tmp.test <- matrix(0, n.testX, m)
        col.names <- NULL
        for(j in 1:m){
                tmp.test[test.x[, var]==mylevels[j], j] <- 1
                col.names <- c(col.names, paste(var, '_', mylevels[j], sep=''))
        }
        colnames(tmp.test) <- col.names
        test.matrixX <- cbind(test.matrixX, tmp.test)
}

XGB.pred <- predict(xgb_mod, newdata = as.matrix(test.matrixX))
XGB.data = data.frame(PID = test[,1], Sale_Price = exp(XGB.pred))
colnames(XGB.data) = c('PID', 'Sale_Price')

###########################
#   Write Data to File    #
###########################
write.csv(XGB.data, "mysubmission1.txt", quote=FALSE, row.names=FALSE)


###########################
#    glmnet Prediction    #
###########################
test.xG = test.x[,!colnames(test.x) %in% remove.var, drop=FALSE]

for(var in varWins$varName) {
        tmp = test.xG[, var]
        myquan = varWins[varWins[, 'varName'] == var, 'myQuan']
        tmp[tmp > myquan] = myquan
        test.xG[, var] = tmp
}

test.matrixG <- test.xG[, !colnames(test.xG) %in% categorical.varsG, drop=FALSE]
n.test <- nrow(test.matrixG)
for(var in categorical.varsG){
        mylevels = sort(unique(DummyVarsG[DummyVarsG[, 'varName'] == var, 'mLevels']))
        m <- length(mylevels)
        m <- ifelse(m>2, m, 1)
        tmp.test <- matrix(0, n.test, m)
        col.names <- NULL
        for(j in 1:m){
                tmp.test[test.xG[, var]==mylevels[j], j] <- 1
                col.names <- c(col.names, paste(var, '_', mylevels[j], sep=''))
        }
        colnames(tmp.test) <- col.names
        test.matrixG <- cbind(test.matrixG, tmp.test)
}

GLM.pred <-predict(GLM.out, s = GLM.out$lambda.min, newx = as.matrix(test.matrixG))
GLM.data = data.frame(PID = test[,1], Sale_Price = exp(GLM.pred))
colnames(GLM.data) = c('PID', 'Sale_Price')

###########################
#   Write Data to File    #
###########################
write.csv(GLM.data, "mysubmission2.txt", quote=FALSE, row.names=FALSE)
