##############################################################
#####Step Calculate global Social Segregation Index(SSI)######
##############################################################
library(dplyr)

######################################################
#####Load in SVI######################################
######################################################
Pathroot<-"/soge-home/users/cenv0925/"
City <- "StLouis"
########load us svi##########
SVI<-read.csv(paste(Pathroot,"SVI/Data/SVI2018_US.csv",sep=""))
SVI_SPL<-SVI %>% select(FIPS,SPL_THEME1,SPL_THEME2, SPL_THEME3, SPL_THEME4, SPL_THEMES)
print(paste(City," is loaded",sep=""))


######################################################
#####Build Subset SVI for The MSA#################
######################################################


newframe<-read.csv(paste(Pathroot,"SVI/Data/Step1_TotalOD/", City, "2019.csv",sep = ""),header = T)
names(newframe)[1] <- "O"
names(newframe)[2] <- "D"
#select unique census tracts from MSA 
Ovector<-unique(newframe$O)
Dvector<-unique(newframe$D)
TractID<-unique(c(Ovector,Dvector))
TractDF<-data.frame(TractID)
#join census tracts with SVI values 
TractDF<-TractDF %>% left_join(SVI_SPL, by=c('TractID'='FIPS'))
#remove census tracts withour svi values 
TractDF<-subset(TractDF, SPL_THEME1!=-999.000 & SPL_THEME4!=-999.0000)
####Rank based on  SVI##########
TractDF$Rank_THEME1<-rank(TractDF$SPL_THEME1)
TractDF$Rank_THEME2<-rank(TractDF$SPL_THEME2)
TractDF$Rank_THEME3<-rank(TractDF$SPL_THEME3)
TractDF$Rank_THEME4<-rank(TractDF$SPL_THEME4)
TractDF$Rank_THEMES<-rank(TractDF$SPL_THEMES)

######################################################
###############loop start############################
#####################################################
DF<-newframe[c('O','D','Total')]
SVI_RANK<-TractDF[c('TractID','Rank_THEME1','Rank_THEME2','Rank_THEME3','Rank_THEME4','Rank_THEMES')]
DF<- DF %>% left_join(SVI_RANK,by=c('O'='TractID'))
colnames(DF)[4]<-c('O_THEME1')
colnames(DF)[5]<-c('O_THEME2')
colnames(DF)[6]<-c('O_THEME3')
colnames(DF)[7]<-c('O_THEME4')
colnames(DF)[8]<-c('O_THEMES')
DF<- DF %>% left_join(SVI_RANK,by=c('D'='TractID'))
colnames(DF)[9]<-c('D_THEME1')
colnames(DF)[10]<-c('D_THEME2')
colnames(DF)[11]<-c('D_THEME3')
colnames(DF)[12]<-c('D_THEME4')
colnames(DF)[13]<-c('D_THEMES')


library(tidyr)
DF<-DF %>% drop_na()

DF$DIFF_THEME1<-abs(DF$O_THEME1-DF$D_THEME1)
DF$DIFF_THEME2<-abs(DF$O_THEME2-DF$D_THEME2)
DF$DIFF_THEME3<-abs(DF$O_THEME3-DF$D_THEME3)
DF$DIFF_THEME4<-abs(DF$O_THEME4-DF$D_THEME4)
DF$DIFF_THEMES<-abs(DF$O_THEMES-DF$D_THEMES)

#create two column to store distance and similarly(1-distance)
DF$DIS1<-0
DF$SSIM1<-0
DF$DIS2<-0
DF$SSIM2<-0
DF$DIS3<-0
DF$SSIM3<-0
DF$DIS4<-0
DF$SSIM4<-0
DF$DISS<-0
DF$SSIMS<-0
#remove items with na for O_&D_THEMES
#check for NA for a columne of a dataframe sum(is.na(Month$D_THEMES))
DF_clean<-subset(DF,(!is.na(DF$O_THEMES)) & (!is.na(DF$D_THEMES)))
#Rank based on SVI
Rank<-SVI_RANK$Rank_THEMES

###########################
######THEME1###############
###########################
for (n in 1:nrow(DF_clean)){
  DIFF_SET<-abs(Rank-DF_clean$O_THEME1[n])
  DIFF_Compare<-DF_clean$DIFF_THEME1[n]
  N<-length(DIFF_SET)#N denotes the number of census tracts
  A<-length(which(DIFF_SET<DIFF_Compare))#A denotes the number of tracts closer than the examined D_Tract
  count0<-length(which(DIFF_SET==0)) #count0 denotes the number of tracts with 0 social distance 
  if (count0>1){
    DF_clean$DIS1[n]<-(A+0.5)/(N-1)
    DF_clean$SSIM1[n]<-1-DF_clean$DIS1[n]
  }else{
    DF_clean$DIS1[n]<-(A)/(N-1)
    DF_clean$SSIM1[n]<-1-DF_clean$DIS1[n]
  }
}

print("Theme 1 is completed")

###########################
######THEME2###############
###########################

for (n in 1:nrow(DF_clean)){
  DIFF_SET<-abs(Rank-DF_clean$O_THEME2[n])
  DIFF_Compare<-DF_clean$DIFF_THEME2[n]
  N<-length(DIFF_SET)#N denotes the number of census tracts
  A<-length(which(DIFF_SET<DIFF_Compare))#A denotes the number of tracts closer than the examined D_Tract
  count0<-length(which(DIFF_SET==0)) #count0 denotes the number of tracts with 0 social distance 
  if (count0>1){
    DF_clean$DIS2[n]<-(A+0.5)/(N-1)
    DF_clean$SSIM2[n]<-1-DF_clean$DIS2[n]
  }else{
    DF_clean$DIS2[n]<-(A)/(N-1)
    DF_clean$SSIM2[n]<-1-DF_clean$DIS2[n]
  }
}

print("Theme 2 is completed")

###########################
######THEME3###############
###########################

for (n in 1:nrow(DF_clean)){
  DIFF_SET<-abs(Rank-DF_clean$O_THEME3[n])
  DIFF_Compare<-DF_clean$DIFF_THEME3[n]
  N<-length(DIFF_SET)#N denotes the number of census tracts
  A<-length(which(DIFF_SET<DIFF_Compare))#A denotes the number of tracts closer than the examined D_Tract
  count0<-length(which(DIFF_SET==0)) #count0 denotes the number of tracts with 0 social distance 
  if (count0>1){
    DF_clean$DIS3[n]<-(A+0.5)/(N-1)
    DF_clean$SSIM3[n]<-1-DF_clean$DIS3[n]
  }else{
    DF_clean$DIS3[n]<-(A)/(N-1)
    DF_clean$SSIM3[n]<-1-DF_clean$DIS3[n]
  }
}
print("Theme 3 is completed")

###########################
######THEME4###############
###########################

for (n in 1:nrow(DF_clean)){
  DIFF_SET<-abs(Rank-DF_clean$O_THEME4[n])
  DIFF_Compare<-DF_clean$DIFF_THEME4[n]
  N<-length(DIFF_SET)#N denotes the number of census tracts
  A<-length(which(DIFF_SET<DIFF_Compare))#A denotes the number of tracts closer than the examined D_Tract
  count0<-length(which(DIFF_SET==0)) #count0 denotes the number of tracts with 0 social distance 
  if (count0>1){
    DF_clean$DIS4[n]<-(A+0.5)/(N-1)
    DF_clean$SSIM4[n]<-1-DF_clean$DIS4[n]
  }else{
    DF_clean$DIS4[n]<-(A)/(N-1)
    DF_clean$SSIM4[n]<-1-DF_clean$DIS4[n]
  }
}

print("Theme 4 is completed")

###########################
######THEMES###############
###########################

for (n in 1:nrow(DF_clean)){
  DIFF_SET<-abs(Rank-DF_clean$O_THEMES[n])
  DIFF_Compare<-DF_clean$DIFF_THEMES[n]
  N<-length(DIFF_SET)#N denotes the number of census tracts
  A<-length(which(DIFF_SET<DIFF_Compare))#A denotes the number of tracts closer than the examined D_Tract
  count0<-length(which(DIFF_SET==0)) #count0 denotes the number of tracts with 0 social distance 
  if (count0>1){
    DF_clean$DISS[n]<-(A+0.5)/(N-1)
    DF_clean$SSIMS[n]<-1-DF_clean$DISS[n]
  }else{
    DF_clean$DISS[n]<-(A)/(N-1)
    DF_clean$SSIMS[n]<-1-DF_clean$DISS[n]
  }
}

print("Theme s is completed")

#########################################
#####OD Pair Social Dist and Sim##########
#########################################

write.csv(DF_clean,paste(Pathroot,"SVI/Result/OD_SS/",City,"_ODSS.csv",sep=""),row.names = FALSE)

print("OD Pair Social Distance and Similarity saved")


#########################################
#####Global SSI Calculation##############
#########################################

GlobalSSI <- data.frame(City = "StLouis",
                        TotalOD= sum(DF_clean$Total),
                        Theme1 = sum(DF_clean$SSIM1*DF_clean$Total)/sum(DF_clean$Total),
                        Theme2 = sum(DF_clean$SSIM2*DF_clean$Total)/sum(DF_clean$Total),
                        Theme3 = sum(DF_clean$SSIM3*DF_clean$Total)/sum(DF_clean$Total),
                        Theme4 = sum(DF_clean$SSIM4*DF_clean$Total)/sum(DF_clean$Total),
                        Themes = sum(DF_clean$SSIMS*DF_clean$Total)/sum(DF_clean$Total))


write.csv(GlobalSSI,paste(Pathroot,"SVI/Result/GlobalSSI/",City,"_GlobalSSI.csv",sep=""),row.names = FALSE)

print("GlobalSSI is calculated and saved")

#########################################
#####Local SSI Calculation###############
#########################################
TractDF$THEME1<-0
TractDF$THEME2<-0
TractDF$THEME3<-0
TractDF$THEME4<-0
TractDF$THEMES<-0


for (T_ID in 1:length(TractDF$TractID)){
  SSI_local<-subset(DF_clean,O==TractDF$TractID[T_ID])
  TractDF$THEME1[T_ID]<-sum(SSI_local$SSIM1*SSI_local$Total)/sum(SSI_local$Total)
  TractDF$THEME2[T_ID]<-sum(SSI_local$SSIM2*SSI_local$Total)/sum(SSI_local$Total)
  TractDF$THEME3[T_ID]<-sum(SSI_local$SSIM3*SSI_local$Total)/sum(SSI_local$Total)
  TractDF$THEME4[T_ID]<-sum(SSI_local$SSIM4*SSI_local$Total)/sum(SSI_local$Total)
  TractDF$THEMES[T_ID]<-sum(SSI_local$SSIMS*SSI_local$Total)/sum(SSI_local$Total)
}

write.csv(TractDF,paste(Pathroot,"SVI/Result/LocalSSI/",City,"_LocalSSI.csv",sep=""),row.names = FALSE)

print("LocalSSI is calculated and saved")


