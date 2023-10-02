#install.packages("psych")
#install.packages("lme4")

library("ggplot2")
library("tidyverse")
library("psych")
library("lme4")

getwd()

rootDir <- paste(getwd(),"/Documents/data", sep="")
plotDir <- paste(getwd(),"/Documents/data/plots", sep="")
setwd(rootDir)

dx <- read_csv('subjects.csv')

df <- read_csv('24146_1_1_12072020_doors.csv')
head(df)

dist_data <- data.frame()
vas_data <- data.frame()
q_data <- data.frame()

dist_subj <- df[df$Section %in% c("TaskRun1","TaskRun2", "TaskRun3"), ]
vas_subj <- df[df$Section %in% c("VASpre","VAS1","VASmid", "VASpost", "VAS2", "VAS3"), ]
q_subj <- df[df$Section %in% c("Question"), ]

# Selecting specific columns for each df
dist_subj <- dist_subj %>% select(Subject,Section,Subtrial,DistanceFromDoor_SubTrial,
                                  Distance_lock,Door_anticipation_time,Door_opened,
                                  Door_outcome,Reward_magnitude,Punishment_magnitude,
                                  DoorAction_RT,ITI_duration)
vas_subj <- vas_subj %>% select(Subject, Section, VAS_type, VAS_score, VAS_RT)
q_subj <- q_subj %>% select(Subject, Section, Q_type, Q_score, Q_RT)

# Add N+1 column
# outcome
dist_subj$n1_outcome = lag(dist_subj$Door_outcome)
dist_subj$n2_outcome = lag(dist_subj$Door_outcome, 2)
dist_subj$n3_outcome = lag(dist_subj$Door_outcome, 3)

# door open
dist_subj$n1_door_open = lag(dist_subj$Door_opened)
dist_subj$n2_door_open = lag(dist_subj$Door_opened, 2)
dist_subj$n3_door_open = lag(dist_subj$Door_opened, 3)

# add column
dist_subj$nplus1 = ifelse(dist_subj$n1_outcome=="punishment" & dist_subj$n1_door_open=="opened", 
                          "1_lag_P",
                          ifelse(dist_subj$n1_outcome == "reward" & dist_subj$n1_door_open == "opened", 
                                 "1_lag_R",
                                 "1_lag_nofeedback"))
dist_subj$nplus2 = ifelse(dist_subj$n2_outcome=="punishment" & dist_subj$n2_door_open=="opened", 
                          "2_lag_P",
                          ifelse(dist_subj$n2_outcome == "reward" & dist_subj$n2_door_open == "opened", 
                                 "2_lag_R",
                                 "2_lag_nofeedback"))
dist_subj$nplus3 = ifelse(dist_subj$n3_outcome=="punishment" & dist_subj$n3_door_open=="opened", 
                          "3_lag_P",
                          ifelse(dist_subj$n3_outcome == "reward" & dist_subj$n3_door_open == "opened", 
                                 "3_lag_R",
                                 "3_lag_nofeedback"))

dist_data <- rbind(dist_data, dist_subj)
vas_data <- rbind(vas_data, vas_subj)
q_data <- rbind(q_data, q_subj)

# Add run number
dist_data$Section <- substr(dist_data$Section, 8,8)
names(dist_data)[names(dist_data) == "Section"] <- "RunNumber"
vas_data$Section <- substr(vas_data$Section, 4,4)

dist_data <- merge(dist_data, dx, by="Subject", all.x=TRUE)
vas_data <- merge(vas_data, dx, by="Subject", all.x=TRUE)
q_data <- merge(q_data, dx, by="Subject", all.x=TRUE)

rm(dist_subj, q_subj, vas_subj)

# Subject-level distance
subj_dist = data.frame()
subj <- unique(dist_data$Subject)


for (s in subj) {
  reward <- c(1:7) #old: 3,5,7
  p_data = data.frame()
  for (r in reward) {
    punishment <- c(1:7) #old: 0:9
    p_reward = data.frame()
    for (p in punishment) {
      z <- subset(dist_data, Subject == s)
      z <- subset(z, Reward_magnitude == r)
      z <- subset(z, Punishment_magnitude == p)
      z <- data.frame(psych::describe(z$DistanceFromDoor_SubTrial))
      z <- z[,c("mean","sd","se")]
      z$Reward <- r
      z$Punish <- p
      z$Subject <- s
      z <- data.frame(z)
      p_reward <- rbind(p_reward, z)
    }
    p_data <- rbind(p_data, p_reward)  
  }
  subj_dist <- rbind(subj_dist, p_data)
}

rm(p_reward, p_data, z, p, s, r)

# Subject-level reaction time data (log-transformed)
log_rt <- data.frame()
subj <- unique(dist_data$Subject)

for (s in subj) {
  zscore <- subset(dist_data, DoorAction_RT > 150) #150
  zscore <- subset(zscore, Subject == s)
  zscore$Zscore <- scale(zscore$DoorAction_RT)
  zscore <- subset(zscore, abs(Zscore) <=3)
  zscore$loge <- log(zscore$DoorAction_RT)
  log_rt <- rbind(log_rt, zscore)
}

subj_rt = data.frame()
subj <- unique(log_rt$Subject)


for (s in subj) {
  reward <- c(1:7) #old: 3,5,7
  p_data = data.frame()
  for (r in reward) {
    punishment <- c(1:7) #old: 0:9
    p_reward = data.frame()
    for (p in punishment) {
      z <- subset(log_rt, Subject == s)
      z <- subset(z, Reward_magnitude == r)
      z <- subset(z, Punishment_magnitude == p)
      z <- psych::describe(z$loge)
      z <- z[,c("mean","sd","se")]
      z$Reward <- r
      z$Punish <- p
      z$Subject <- s
      p_reward <- rbind(p_reward, z)
    }
    p_data <- rbind(p_data, p_reward)  
  }
  subj_rt <- rbind(subj_rt, p_data)
}

# Write function: average of each variable
avg_of_var <- function(df0) {
  avg_avg = data.frame()
  reward <- c(1:7) #old: 3,5,7
  for (r in reward) {
    avg_reward = data.frame()
    punishment <- c(1:7) #old: 0:9
    for (p in punishment) {
      q <- subset(df0, Reward == r)
      q <- subset(q, Punish == p)
      q <- psych::describe(q$mean)
      q <- q[,c("mean","sd","se")]
      q <- data.frame(q)
      q$Reward <- r
      q$Punish <- p
      avg_reward <- rbind(avg_reward, q)
    }
    avg_avg <- rbind(avg_avg, avg_reward)
  }
  avg_avg <<- avg_avg
}

# Calculate group averages: group_dist, group_rt, group_vas, group_q
group_dist <- avg_of_var(subj_dist)
names(group_dist)[1] <- "Distance"

group_rt <- avg_of_var(subj_rt)
names(group_rt)[1] <- "logRT"
rm(avg_avg)

group_vas = data.frame()
group <- c("ANX","HV")

for (g in group) {
  xx = data.frame()
  section <- unique(vas_data$Section)
  for (b in section){
    type <- unique(vas_data$VAS_type)
    x = data.frame()
    for (t in type) {
      x1 <- subset(vas_data, Group == g)
      x1 <- subset(x1, Section == b)
      x1 <- subset(x1, VAS_type == t)
      x1 <- psych::describe(x1$VAS_score)
      x1 <- x1[,c("mean","sd","se")]
      x1$Dx <- g
      x1$VAS_section <- b
      x1$VAS_type <- t
      x <- rbind(x, x1)
    }
    xx <- rbind(xx, x)
  }
  group_vas <- rbind(group_vas, xx)
}

group_q = data.frame()

for (g in group) {
  type <- unique(q_data$Q_type)
  x1 = data.frame()
  for (t in type) {
    x <- subset(q_data, Group == g)
    x <- subset(x, Q_type == t)
    x <- psych::describe(x$Q_score)
    x <- x[,c("mean","sd","se")]
    x$Dx <- g
    x$Q_type <- t
    x1 <- rbind(x1, x)
  }
  group_q <- rbind(group_q, x1)
}

rm(x,x1,xx,g,b,section,t,type)

# Set data types
dist_data <- dist_data %>%
  mutate(Subject = factor(Subject, levels=unique(dist_data$Subject)),
         RunNumber = factor(RunNumber, levels=unique(dist_data$RunNumber)))

group_vas <- group_vas %>%
  #TODO: Change after agreed!!!
  mutate(VAS_section = factor(VAS_section, levels=c(1,2,3,4),
                              labels = c("VAS1", "VAS2", "VAS3","vas_post")),
         VAS_type = factor(VAS_type, levels=c("Anxiety","Avoidance","Mood","Tired"),
                           labels = c("Anxiety","Want to continue",
                                      "Mood","Tired")))

group_q <- group_q %>%
  mutate(Q_type = factor(Q_type, levels=c("Won","Lost","Monster","Coins","Before","Performance"),
                         labels = c("Coins won","Coins lost",
                                    "Saw monster","Saw coins",
                                    "Anticipated winning","Rate performance")))

table(dist_data$Subject)


### Plotting ###
setwd(plotDir)

# Group average: Distance ~ RP curve
ggplot(group_dist, aes(x=Punish, y=Distance, 
                       group=factor(Reward), 
                       color=factor(Reward))) +
  geom_line(size=0.75) + geom_point() +
  geom_errorbar(size=0.75, width=0.2, aes(ymin = Distance-se, ymax = Distance+se)) +
  labs(x = "Punishment", y = "Distance from door", 
       color = "Reward", 
       title = "Distance ~ Reward x Punishment") +
  scale_x_continuous(breaks = c(0:10)) +
  theme_bw()

ggsave("dist_rp_group.png")

# Subj average: Distance ~ RP curve 
ggplot(subj_dist, aes(x=Punish, y=mean, 
                      group = factor(Reward), 
                      color=factor(Reward))) +
  geom_line() + geom_point() +
  geom_errorbar(width=0.2, aes(ymin = mean-se, ymax = mean+se)) +
  labs(x = "Punishment", y = "Distance from door", 
       color = "Reward", 
       title = "Distance ~ Reward x Punishment (subject)") +
  scale_x_continuous(breaks = c(0:10)) +
  facet_wrap(.~Subject) +
  theme_bw()

ggsave("dist_rp_subj.png")

# Group avg: RT ~ RP
ggplot(group_rt, aes(x=Punish, y=logRT, 
                     group=factor(Reward), 
                     color=factor(Reward))) +
  geom_line(size=0.75) + geom_point() +
  geom_errorbar(size=0.75, width=0.1, aes(ymin = logRT-se, ymax = logRT+se)) +
  labs(x = "Punishment", y = "log(Reaction Time)", 
       color = "Reward", 
       title = "RT ~ Reward x Punishment") +
  scale_x_continuous(breaks = c(0:10)) +
  theme_bw()
setwd(plotDir)

ggsave("rt_rp_group.png")


# Subj avg: RT ~ RP
ggplot(subj_rt, aes(x=Punish, y=mean, 
                    group = factor(Reward), 
                    color=factor(Reward))) +
  geom_line() + geom_point() +
  geom_errorbar(width=0.1, aes(ymin = mean-se, ymax = mean+se)) +
  labs(x = "Punishment", y = "log(Reaction Time)", 
       color = "Reward", 
       title = "RT ~ Reward x Punishment by subject") +
  scale_x_continuous(breaks = c(0:10)) +
  facet_wrap(.~Subject) +
  theme_bw()

ggsave("RT_rp_by_subj.png")


# Group avg: VAS
ggplot(group_vas, aes(x=VAS_section, y=mean, 
                      #group=factor(VAS_type), 
                      fill=factor(VAS_type))) +
  geom_bar(stat="identity", color="black",
           position=position_dodge()) +
  geom_errorbar(aes(ymin = mean-se, ymax = mean+se), width=.2, 
                position=position_dodge(0.9)) +
  labs(x = "VAS Section", y = "VAS Score", 
       fill = "Question", 
       title = "VAS") +
  facet_wrap(.~Dx) +
  theme_bw()
#sd and se for hv is all nas (so no error bars appear on plot)

ggsave("vas_group.png")

# Group avg: Questions
ggplot(group_q, aes(x=Q_type, y=mean,
                    fill=Dx, group=Dx)) +
  geom_bar(stat="identity", color="black", width=0.7,
           position=position_dodge()) +
  geom_errorbar(aes(ymin = mean-se, ymax = mean+se), width=.2, 
                position=position_dodge(0.7)) +
  labs(x = "", y = "Score", 
       title = "Post-task questions") +
  #facet_wrap(.~Dx) +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))

ggsave("q_group.png")


### Subject-level regression ###

# standardize data for betas
orig_dist_data <- dist_data
dist_data <- orig_dist_data
dist_data <- drop_na(dist_data, DistanceFromDoor_SubTrial, Reward_magnitude, Punishment_magnitude, DoorAction_RT)
dist_data$rp <- dist_data$Reward_magnitude*dist_data$Punishment_magnitude
dist_data <- dist_data %>% select(Subject,RunNumber,Subtrial,DistanceFromDoor_SubTrial,
                                  Reward_magnitude,Punishment_magnitude,rp,DoorAction_RT )
dist_data$RminusP <- dist_data$Reward_magnitude - dist_data$Punishment_magnitude
dist_data$EV <- (dist_data$Reward_magnitude*0.5) + (dist_data$Punishment_magnitude*0.5)
dist_data$conflict <- 6 - abs(dist_data$RminusP)
dist_data$DoorAction_RT <- log(dist_data$DoorAction_RT)
z_dist_data <- cbind(dist_data[,c(1:3)], scale(dist_data[,c(4:11)]))

# Distance regression: subject-level regression and betas

dist_lm_full <- lm(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + rp, data=z_dist_data)
summary(dist_lm_full)
dist_lm <- lmList(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + rp | Subject, data=z_dist_data)

##### experiment:
dist_lm_contRT <- lm(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + DoorAction_RT, data=z_dist_data)
summary(dist_lm_contRT)
#z_dist_data <- drop_na(z_dist_data, SCARED.AVG)
dist_lm <- lmList(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + DoorAction_RT | Subject, data=z_dist_data)

dist_lm_RminusP <- lm(DistanceFromDoor_SubTrial ~ RminusP, data=z_dist_data)
summary(dist_lm_RminusP)

dist_lm_EV <- lm(DistanceFromDoor_SubTrial ~ EV, data=z_dist_data)
summary(dist_lm_EV)

dist_lm_conflict <- lm(DistanceFromDoor_SubTrial ~ conflict, data=z_dist_data)
summary(dist_lm_conflict)

dist_lm_noRP_full <- lm(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude, data=z_dist_data)
summary(dist_lm_noRP_full)

dist_lm_noRP <- lmList(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude | Subject, data=z_dist_data)
RT_lm_noRP <- lmList(DoorAction_RT ~ Reward_magnitude + Punishment_magnitude  + rp | Subject, data=z_dist_data)

z_dist_data$DoorAction_RT <- log(z_dist_data$DoorAction_RT)
RT_lm_full <- lm(DoorAction_RT ~ Reward_magnitude + Punishment_magnitude, data=z_dist_data)
summary(RT_lm_full)
RT_lm <- lmList(DoorAction_RT ~ Reward_magnitude + Punishment_magnitude | Subject, data=z_dist_data)

#z_dist_data$DistanceFromDoor_SubTrial
#z_dist_data$Reward_magnitude
#z_dist_data$Punishment_magnitude
#z_dist_data$rp
#z_dist_data$Subject

#____________________>>>>>>>> current coefs from contRT
#------>>>> do regression for each run and average betas

# distance regression individual betas
dist_coeff <- coef(dist_lm)
names(dist_coeff)[1] <- "Intercept"
names(dist_coeff)[2] <- "Reward"
names(dist_coeff)[3] <- "Punishment"
names(dist_coeff)[4] <- "RP"
dist_coeff <- round(dist_coeff, digits=3)
dist_coeff$Subject <- rownames(dist_coeff)

# same regression, but no RP term
dist_coeff_noRP <- coef(dist_lm_noRP)
names(dist_coeff_noRP)[1] <- "Intercept"
names(dist_coeff_noRP)[2] <- "Reward"
names(dist_coeff_noRP)[3] <- "Punishment"
dist_coeff_noRP <- round(dist_coeff_noRP, digits=3)
dist_coeff_noRP$Subject <- rownames(dist_coeff_noRP)
# same regression, but no RP term

# RT regression individual betas
RT_coeff <- coef(RT_lm)
names(RT_coeff)[1] <- "Intercept"
names(RT_coeff)[2] <- "Reward"
names(RT_coeff)[3] <- "Punishment"
#names(RT_coeff)[4] <- "RP"
RT_coeff <- round(RT_coeff, digits=3)
RT_coeff$Subject <- rownames(RT_coeff)

# Save distance betas, p-vals
# problematic - subject 24476
dist_lm_pval <- as.data.frame(coef(summary(dist_lm, pool=F)))
dist_lm_pval$Subject <- rownames(dist_lm_pval)
#write.csv(dist_lm_pval, file="dist_lm_pvals.csv", quote=F, row.names=F)
#view regression analysis (distance)
summary(dist_lm)

RT_lm_pval <- as.data.frame(coef(summary(RT_lm, pool=F)))
RT_lm_pval$Subject <- rownames(RT_lm_pval)
#write.csv(dist_lm_pval, file="dist_lm_pvals.csv", quote=F, row.names=F)
#view regression analysis (distance)
summary(RT_lm)

#exporting subject-level beta values as .csv
#data.frame(unclass(summary(dist_lm)), check.names = FALSE, stringAsFactors = FALSE)

# Plot subject betas and group average
dist_coeff_long <- dist_coeff %>%
  pivot_longer(Intercept:RP,
               #dist_coeff_long <- dist_coeff_noRP %>%
               #  pivot_longer(Intercept:Punishment,
               names_to = "Variable",
               values_to = "value")

dist_coeff_long <- subset(dist_coeff_long, Variable != "Intercept")

# Add dx to subject betas
dist_coeff_long <- merge(dist_coeff_long, dx, by="Subject", all.x=FALSE)
#write.csv(dist_coeff_long, "dist_betas_subj.csv", quote=F, row.names = FALSE)

# group average
vars <- unique(dist_coeff_long$Variable)
group_dist_betas = data.frame()

for (v in vars) {
  betas_dx = data.frame()
  group <- c("ANX", "HV")
  for (g in group) {
    x <- subset(dist_coeff_long, Variable == v)
    x <- subset(x, Group == g)
    x1 <- psych::describe(x$value)
    x1 <- x1[,c("mean","sd","se")]
    x1$Variable <- v
    x1$dx <- g
    betas_dx <- rbind(betas_dx, x1)
  }
  group_dist_betas <- rbind(group_dist_betas, betas_dx)
}

sample_dist_betas = data.frame()

for (v in vars) {
  betas = data.frame()
  x <- subset(dist_coeff_long, Variable == v)
  x1 <- psych::describe(x$value)
  x1 <- x1[,c("mean","sd","se")]
  x1$Variable <- v
  betas <- rbind(betas, x1)
  sample_dist_betas <- rbind(sample_dist_betas, betas)
}


#independent-samples t tests (group distance betas)

RewardList <- subset(dist_coeff_long, Variable == "Reward")#REWARD
RewardBetasT <- t.test(value ~ Group, var.equal=TRUE, data = RewardList)
RewardBetasT$p.value #print p value only

PunishmentList <- subset(dist_coeff_long, Variable == "Punishment")#PUNISHMENT
PunishmentBetasT <- t.test(value ~ Group, var.equal=TRUE, data = PunishmentList)
PunishmentBetasT$p.value #print p value only

RPList <- subset(dist_coeff_long, Variable == "RP")#RP
RPBetaT <- t.test(value ~ Group, var.equal=TRUE, data = RPList)
RPBetaT$p.value #print p value only

# BOXPLOTS - group distance betas
if(!require(devtools))install.packages("devtools")
devtools::install_github("kassambara/ggpubr")

library("ggpubr")

ggboxplot(PunishmentList, x = "dx", y = "value",
          color = "dx", palette = c("red", "green"),
          main="Group-level Distance Betas, Punishment",
          ylab = "Beta Value", xlab = "DX")

setwd(plotDir)
ggsave("betas_punishment_boxplot.png")

ggboxplot(RewardList, x = "dx", y = "value",
          color = "dx", palette = c("red", "green"),
          main="Group-level Distance Betas, Reward",
          ylab = "Beta Value", xlab = "DX")

setwd(plotDir)
ggsave("betas_reward_boxplot.png")

ggboxplot(RPList, x = "dx", y = "value",
          color = "dx", palette = c("red", "green"),
          main="Group-level Distance Betas, RP",
          ylab = "Beta Value", xlab = "DX")

setwd(plotDir)
ggsave("betas_RP_boxplot.png")

# ANOVA with subject betas (Variable x Dx)
dist_coeff_long$Subject <- as.factor(dist_coeff_long$Subject)
options(contrasts=c("contr.sum","contr.poly"))
beta.aov = aov(value ~ (Variable*dx) + Error(Subject/Variable) + dx + Age + Sex + Version, data=dist_coeff_long)
summary(beta.aov)

dist_coeff_wide <- spread(dist_coeff_long,Variable,value)

dist_coeff_wide$SCARED.C <- scale(dist_coeff_wide$SCARED.C)
dist_coeff_wide$SCARED.P <- scale(dist_coeff_wide$SCARED.P)

beta_P.aov = aov(Punishment ~ dx + Age + Sex + Version + Error(Subject), data=dist_coeff_wide)
summary(beta_P.aov)

mod_P <- lm(Punishment ~ dx + Age + Sex + Version, data=dist_coeff_wide)
summary(mod_P)

mod_R = aov(Reward ~ dx + Age + Sex + Version, data=dist_coeff_wide)
summary(mod_R)

beta_RP.aov = aov(RP ~ dx + Age + Sex + Version, data=dist_coeff_wide)
summary(beta_RP.aov)

cor.test(dist_coeff_wide$Reward, dist_coeff_wide$Punishment)
plot(dist_coeff_wide$Reward,dist_coeff_wide$Punishment, ylim=c(-1,1), ylab="P")
abline(lm(Punishment ~ Reward, data=dist_coeff_wide))
text(dist_coeff_wide$Reward+0.05, dist_coeff_wide$Punishment-0.1,labels=dist_coeff_wide$Subject)
cor.test(dist_coeff_wide$SCARED.AVG, dist_coeff_wide$Reward)
plot(dist_coeff_wide$Reward,dist_coeff_wide$Punishment, ylim=c(-1,1), ylab="P")

cor.test(dist_coeff_wide$Punishment, dist_coeff_wide$Age)


#VIOLIN PLOTS- group distance betas
library(dplyr)
library(ggthemes)

ggplot(PunishmentList, aes(x=dx, y=value, color=dx)) +
  geom_violin(trim=FALSE) +
  # Add individual data points
  geom_jitter(position = position_jitterdodge(jitter.width=0.2), alpha=0.5) +
  # Add mean
  stat_summary(fun="mean", geom="crossbar",position=position_dodge(0.1), width=0.7) +
  #facet_wrap(.~Phase) +
  scale_color_manual(values=c("dark red", "dark green")) +
  theme_classic()+
  labs(x = "dx", y = "beta value", title = "Group-level Distance Betas, Punishment")+ 
  scale_y_continuous(limits = c(-1, 1), breaks = seq(-1,1,0.25)) +
  geom_hline(yintercept=0)

ggsave("group_betas_punishment_violinplot.png")

ggplot(RewardList, aes(x=dx, y=value, color=dx)) +
  geom_violin(trim=FALSE) +
  # Add individual data points
  geom_jitter(position = position_jitterdodge(jitter.width=0.2), alpha=0.5) +
  # Add mean
  stat_summary(fun="mean", geom="crossbar",position=position_dodge(0.1), width=0.7) +
  #facet_wrap(.~Phase) +
  scale_color_manual(values=c("dark red", "dark green")) +
  theme_classic()+
  labs(x = "dx", y = "beta value", title = "Group-Level Distance Betas, Reward")+ 
  scale_y_continuous(limits = c(-1, 1), breaks = seq(-1,1,0.25)) +
  geom_hline(yintercept=0)

ggsave("group_betas_reward_violinplot.png")

ggplot(RPList, aes(x=dx, y=value, color=dx)) +
  geom_violin(trim=FALSE) +
  # Add individual data points
  geom_jitter(position = position_jitterdodge(jitter.width=0.2), alpha=0.5) +
  # Add mean
  stat_summary(fun="mean", geom="crossbar",position=position_dodge(0.1), width=0.7) +
  #facet_wrap(.~Phase) +
  scale_color_manual(values=c("dark red", "dark green")) +
  theme_classic()+
  labs(x = "dx", y = "beta value", title = "Group-Level Distance Betas, RP")+ 
  scale_y_continuous(limits = c(-1, 1), breaks = seq(-1,1,0.25)) +
  geom_hline(yintercept=0)

ggsave("group_betas_rp_violinplot.png")

# plot R, P, RP betas across full sample
ggplot(dist_coeff_long, aes(x=Variable, y=value, color=Variable)) +
  geom_violin(trim=FALSE) +
  # Add individual data points
  geom_jitter(position = position_jitterdodge(jitter.width=0.2), alpha=0.5) +
  # Add mean
  stat_summary(fun="mean", geom="crossbar",position=position_dodge(0.1), width=0.7) +
  #facet_wrap(.~Phase) +
  scale_color_manual(values=c("red", "dark green", "blue")) +
  theme_classic()+
  labs(y = "Beta value", title = "Sample-Level Distance Betas") + 
  scale_y_continuous(limits = c(-1, 1), breaks = seq(-1,1,0.25)) +
  geom_hline(yintercept=0)

ggsave("sample_betas_violinplot.png")

#plot sex
ggplot(PunishmentList, aes(x=as.character(Sex), y=value, color=as.character(Sex))) +
  geom_violin(trim=FALSE) +
  # Add individual data points
  geom_jitter(position = position_jitterdodge(jitter.width=0.2), alpha=0.5) +
  # Add mean
  stat_summary(fun="mean", geom="crossbar",position=position_dodge(0.1), width=0.7) +
  #facet_wrap(.~Phase) +
  scale_color_manual(values=c("dark red", "dark green")) +
  theme_classic()+
  labs(x = "Sex (1=M; 2=F)", y = "beta value", title = "Distance Betas, Punishment")+ 
  scale_y_continuous(limits = c(-1, 1), breaks = seq(-1,1,0.25)) +
  geom_hline(yintercept=0)

ggplot(RewardList, aes(x=as.character(Sex), y=value, color=as.character(Sex))) +
  geom_violin(trim=FALSE) +
  # Add individual data points
  geom_jitter(position = position_jitterdodge(jitter.width=0.2), alpha=0.5) +
  # Add mean
  stat_summary(fun="mean", geom="crossbar",position=position_dodge(0.1), width=0.7) +
  #facet_wrap(.~Phase) +
  scale_color_manual(values=c("dark red", "dark green")) +
  theme_classic()+
  labs(x = "Sex (1=M; 2=F)", y = "beta value", title = "Distance Betas, Reward")+ 
  scale_y_continuous(limits = c(-1, 1), breaks = seq(-1,1,0.25)) +
  geom_hline(yintercept=0)

# independent-samples t tests (group rt betas)

# RewardRTList <- subset(dist_coeff_long, Variable == "Reward")#REWARD
# RewardRTBetasT <- t.test(value ~ dx, var.equal=TRUE, data = RewardList)
# RewardRTBetasT$p.value #print p value only
# 
# PunishmentRTList <- subset(dist_coeff_long, Variable == "Punishment")#PUNISHMENT
# PunishmentRTBetasT <- t.test(value ~ dx, var.equal=TRUE, data = PunishmentList)
# PunishmentRTBetasT$p.value #print p value only
# 
# RPRTList <- subset(dist_coeff_long, Variable == "RP")#RP
# RPRTBetaT <- t.test(value ~ dx, var.equal=TRUE, data = RPList)
# RPRTBetaT$p.value #print p value only

# Plot subject-level betas with group average
ggplot(dist_coeff_long, aes(x=Variable, y=value, #subj betas
                            color = Variable)) +
  geom_hline(yintercept=0, size=0.8) +
  scale_color_manual(values = c("red","green","blue")) +
  geom_point(position = position_dodge(width = 0.5), 
             alpha = 0.5, size = 1.5) +
  #group mean
  geom_point(data = sample_dist_betas, aes(x=Variable, y=mean),
             shape = "square", size=3,
             position = position_dodge(width = 0.75)) +
  geom_errorbar(data=group_dist_betas, 
                aes(x=Variable, ymin = mean-se, ymax = mean+se), 
                width=0.15, alpha=0.8, inherit.aes=FALSE) +
  labs(x = element_blank(), y = "Beta value", title = "Individual-level betas") +
  guides(fill = guide_legend(title="Variable")) +
  theme_bw()

setwd(plotDir)
ggsave("dist_betas_subj_group.png")

# Plot subject-level betas with group average
ggplot(dist_coeff_long, aes(x=Variable, y=value, #subj betas
                            color = Variable)) +
  geom_hline(yintercept=0, size=0.8) +
  scale_color_manual(values = c("red","green","blue")) +
  geom_point(position = position_dodge(width = 0.5), 
             alpha = 0.5, size = 1.5) +
  #group mean
  geom_point(data = group_dist_betas, aes(x=Variable, y=mean),
             shape = "square", size=3,
             position = position_dodge(width = 0.75)) +
  geom_errorbar(data=group_dist_betas, 
                aes(x=Variable, ymin = mean-se, ymax = mean+se), 
                width=0.15, alpha=0.8, inherit.aes=FALSE) +
  labs(x = element_blank(), y = "Beta value", title = "Individual-level betas") +
  guides(fill = guide_legend(title="Variable")) +
  facet_grid(.~dx) +
  theme_bw()

setwd(plotDir)
ggsave("dist_betas_subj_group.png")



#library(olsrr)
#ols_plot_cooksd_bar(mod_P)

# Subject beta distribution: kernel density
ggplot(dist_coeff_long, aes(x=value, fill=Variable)) +
  geom_density(alpha=0.5) +
  labs(x = "Beta value", y = "Density", 
       fill = "Type", title = "Kernel density of betas") +
  facet_wrap(.~dx) +
  theme_bw()
ggsave("beta_dist_by_group_kerneldensity.png")

ggplot(dist_coeff_long, aes(x=value, fill=dx)) +
  geom_density(alpha=0.5) +
  labs(x = "Beta value", y = "Density", 
       fill = "Type", title = "Kernel density of betas") +
  facet_wrap(.~Variable) +
  theme_bw()
ggsave("beta_dist_by_cond_kerneldensity.png")

### Distance StDev ###
subj_dist$rp <- subj_dist$Reward * subj_dist$Punish
z_dist_stdev_data <- as.data.frame(cbind(subj_dist$Subject, scale(subj_dist[,c(1:5,7)])))
names(z_dist_stdev_data)[1] <- "Subject"

# DistanceStDev regression: subject betas
# need to re move NAs

z_dist_stdev_data <- na.omit(z_dist_stdev_data)

dist_stdev_lm <- lmList(sd ~ Reward + Punish + rp | Subject, data=z_dist_stdev_data)


dist_stdev_coeff <- coef(dist_stdev_lm)
names(dist_stdev_coeff)[1] <- "Intercept"
names(dist_stdev_coeff)[2] <- "Reward"
names(dist_stdev_coeff)[3] <- "Punishment"
names(dist_stdev_coeff)[4] <- "RP"
dist_stdev_coeff <- round(dist_stdev_coeff, digits=3)
dist_stdev_coeff$Subject <- rownames(dist_stdev_coeff)

dist_stdev_coeff_long <- dist_stdev_coeff %>%
  pivot_longer(Intercept:RP,
               names_to = "Variable",
               values_to = "value")

dist_stdev_coeff_long <- subset(dist_stdev_coeff_long, Variable != "Intercept")
dist_stdev_coeff_long <- merge(dist_stdev_coeff_long, dx, by="Subject", all.x=FALSE)

ggplot(dist_stdev_coeff_long, aes(x=Variable, y=value, #subj betas
                                  color = Variable)) +
  geom_hline(yintercept=0, size=0.8) +
  scale_color_manual(values = c("red","green","blue")) +
  geom_point(position = position_dodge(width = 0.5), 
             alpha = 0.5, size = 1.5) +
  #group mean
  # geom_point(data = group_dist_betas, aes(x=Variable, y=mean),
  #             shape = "square", size=3,
  #             position = position_dodge(width = 0.75)) +
  #  geom_errorbar(data=group_dist_betas, 
  #                aes(x=Variable, ymin = mean-se, ymax = mean+se), 
  #                width=0.15, alpha=0.8, inherit.aes=FALSE) +
  labs(x = element_blank(), y = "Beta value", title = "Individual-level betas") +
  guides(fill = guide_legend(title="Variable")) +
  facet_grid(.~dx) +
  theme_bw()

# plot individual regressions
dist_data <- merge(dist_data, dx, by="Subject", all.x=TRUE)
ggplot(dist_data, aes(x=Reward_magnitude*Punishment_magnitude, y=DistanceFromDoor_SubTrial,
                      group = factor(Subject), color = factor(Subject))) +
  geom_point(size=1.3, alpha=0.5) + 
  stat_smooth(method=lm, alpha=0.3) +
  labs(x = "Reward x Punishment", y = "Distance", 
       fill = "Distance", color = "Subject",title = "Distance ~ Reward x Punishment") +
  facet_wrap(.~dx) +
  theme_bw()
ggsave("subj_dist_regression.png")

# where is the group distance data
exists("dist_lm_group")
ls()

# LME: group data
library(phia)
library(nlme)

dist_lme_group = lme(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + rp, random=~1|Subject, data=z_dist_data)
summary(dist_lme_group)
Anova(dist_lme_group, test.statistic="F", type=3)

### Split-half reliability###

library(dplyr) # need either magrittr or dplyr

dist_data <- dist_data %>%
  mutate(Subject = as.character(Subject), 
         RunNumber = as.numeric(as.character(RunNumber)))
summary(dist_data)

# Distance average: by run and subject
subj <- unique(dist_data$Subject)
subj_dist_r1r2 = data.frame()

for (s in subj) {
  runtype <- unique(dist_data$RunNumber)
  aa = data.frame()
  for(n in runtype) {
    reward <- c(1:7)
    aa1 = data.frame()
    for (r in reward) {
      punishment <- c(1:7)
      aa2 = data.frame()
      for (p in punishment) {
        x <- subset(dist_data, Subject == s)
        x <- subset(x, RunNumber == n)
        x <- subset(x, Reward_magnitude == r)
        x <- subset(x, Punishment_magnitude == p)
        y <- psych::describe(x$DistanceFromDoor_SubTrial)
        y <- y[,c("mean","sd","se")]
        y$Reward <- r
        y$Punish <- p
        y$RunNumber <- n
        y$Subject <- s
        aa2 <- rbind(aa2, y)
      }
      aa1 <- rbind(aa1, aa2)  
    }
    aa <- rbind(aa, aa1)
  }
  subj_dist_r1r2 <- rbind(subj_dist_r1r2, aa)
}

subj_dist_r1 <- subset(subj_dist_r1r2, RunNumber==1)
subj_dist_r2 <- subset(subj_dist_r1r2, RunNumber==2)
subj_dist_r3 <- subset(subj_dist_r1r2, RunNumber==3)

# Average distance of subjects by run
group_dist_r1 <- avg_of_var(subj_dist_r1)
names(group_dist_r1)[1] <- "Distance"
group_dist_r1$Run <- 1

group_dist_r2 <- avg_of_var(subj_dist_r2)
names(group_dist_r2)[1] <- "Distance"
group_dist_r2$Run <- 2

group_dist_r3 <- avg_of_var(subj_dist_r3)
names(group_dist_r3)[1] <- "Distance"
group_dist_r3$Run <- 3


# Combine runs
group_dist_r1r2r3 <- rbind(group_dist_r1, group_dist_r2, group_dist_r3)


### Regressions for Run 1 & Run 2

# Subset runs and scale data
z_r1 <- subset(z_dist_data, RunNumber == 1)
z_r2 <- subset(z_dist_data, RunNumber == 2)
z_r3 <- subset(z_dist_data, RunNumber == 3)

# Distance regression: Subject-level D ~ R + P betas
lm_r1 <- lmList(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + DoorAction_RT | Subject, data = z_r1)
coef_r1 <- coef(lm_r1)
names(coef_r1)[1] <- "Intercept"
names(coef_r1)[2] <- "Reward"
names(coef_r1)[3] <- "Punishment"
names(coef_r1)[4] <- "RT"
coef_r1 <- round(coef_r1, digits=3)
coef_r1$Subject <- rownames(coef_r1)
coef_r1$Run <- 1

summary(lm_r1)

lm_r2 <- lmList(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + DoorAction_RT | Subject, data = z_r2)
coef_r2 <- coef(lm_r2)
names(coef_r2)[1] <- "Intercept"
names(coef_r2)[2] <- "Reward"
names(coef_r2)[3] <- "Punishment"
names(coef_r2)[4] <- "RT"
coef_r2 <- round(coef_r2, digits=3)
coef_r2$Subject <- rownames(coef_r2)
coef_r2$Run <- 2

summary(lm_r2)

lm_r3 <- lmList(DistanceFromDoor_SubTrial ~ Reward_magnitude + Punishment_magnitude + DoorAction_RT | Subject, data = z_r3)
coef_r3 <- coef(lm_r3)
names(coef_r3)[1] <- "Intercept"
names(coef_r3)[2] <- "Reward"
names(coef_r3)[3] <- "Punishment"
names(coef_r3)[4] <- "RT"
coef_r3 <- round(coef_r2, digits=3)
coef_r3$Subject <- rownames(coef_r3)
coef_r3$Run <- 3

summary(lm_r3)

dist_coef_r1r2r3 <- rbind(coef_r1, coef_r2, coef_r3)

# Beta p-values by run
lm_r1_pval <- as.data.frame(coef(summary(lm_r1, pool=F)))
lm_r1_pval$Subject <- rownames(lm_r1_pval)
lm_r1_pval$Run <- 1

lm_r2_pval <- as.data.frame(coef(summary(lm_r2, pool=F)))
lm_r2_pval$Subject <- rownames(lm_r2_pval)
lm_r2_pval$Run <- 2

lm_r3_pval <- as.data.frame(coef(summary(lm_r3, pool=F)))
lm_r3_pval$Subject <- rownames(lm_r3_pval)
lm_r3_pval$Run <- 3

lm_r1r2r3_pval <- rbind(lm_r1_pval, lm_r2_pval, lm_r3_pval)
#write.csv(lm_r1r2_pval, file="lmdist_r1r2_pvals.csv", quote=F, row.names=F)

# Format data to plot r1-2 betas
dist_coef_r1r2r3 <- dist_coef_r1r2r3[,c(5,6,2:4)]
dist_coef_r1r2r3_long <- dist_coef_r1r2r3 %>% 
  pivot_longer(Reward:RT,
               values_to = "value",
               names_to = "Variable")
dist_coef_r1r2r3_plot <- dist_coef_r1r2r3_long %>%
  pivot_wider(id_cols = c(Subject, Variable),
              names_from = Run,
              names_prefix = "Run",
              values_from = value)

# Run 1 vs. Run 2 vs. Run 3 group average
dist_coef_r1r2r3_long <- merge(dist_coef_r1r2r3_long, dx, by="Subject", all.x=T)

r1_betas <- subset(dist_coef_r1r2r3_long, Run == 1)
r2_betas <- subset(dist_coef_r1r2r3_long, Run == 2)
r3_betas <- subset(dist_coef_r1r2r3_long, Run == 3)

r1_betas_wide <- spread(r1_betas,Variable,value)
r2_betas_wide <- spread(r2_betas,Variable,value)
r3_betas_wide <- spread(r3_betas,Variable,value)

r1_beta_P.aov = aov(Punishment ~ dx + Age + Sex + Version + Error(Subject), data=r1_betas_wide)
summary(r1_beta_P.aov)
r1_beta_R.aov = aov(Reward ~ dx + Age + Sex + Version + Error(Subject), data=r1_betas_wide)
summary(r1_beta_R.aov)

r2_beta_P.aov = aov(Punishment ~ dx + Age + Sex + Version + Error(Subject), data=r2_betas_wide)
summary(r2_beta_P.aov)
r2_beta_R.aov = aov(Reward ~ dx + Age + Sex + Version + Error(Subject), data=r2_betas_wide)
summary(r2_beta_R.aov)

r3_beta_P.aov = aov(Punishment ~ dx + Age + Sex + Version + Error(Subject), data=r3_betas_wide)
summary(r3_beta_P.aov)
r3_beta_R.aov = aov(Reward ~ dx + Age + Sex + Version + Error(Subject), data=r3_betas_wide)
summary(r3_beta_R.aov)

vars <- unique(dist_coef_r1r2r3_long$Variable)
group_dist_r1r2r3_betas = data.frame()

for (v in vars) {
  betas_dx = data.frame()
  group <- c("ANX", "HV")
  for (g in group) {
    x2 = data.frame()
    run <- 1:3
    for (n in run) {
      x <- subset(dist_coef_r1r2r3_long, Variable == v)
      x <- subset(x, dx == g)
      x <- subset(x, Run == n)
      x1 <- psych::describe(x$value)
      x1 <- x1[,c("mean","sd","se")]
      x1$Variable <- v
      x1$dx <- g
      x1$Run <- n
      x2 <- rbind(x2, x1)
    }
    betas_dx <- rbind(betas_dx, x2)
  }
  group_dist_r1r2r3_betas <- rbind(group_dist_r1r2r3_betas, betas_dx)
}


# Plot subject betas: by Run
ggplot(dist_coef_r1r2r3_long, aes(x=factor(Run), y=value, #subj betas
                                  color = Variable)) +
  geom_hline(yintercept=0, size=0.8) +
  scale_color_manual(values = c("red","green","blue")) +
  geom_point(position = position_dodge(width = 0.5), 
             alpha = 0.5, size = 1.5) +
  #group mean
  geom_point(data = group_dist_r1r2r3_betas, aes(x=factor(Run), y=mean),
             shape = "square", size=3,
             position = position_dodge(width = 0.75)) +
  geom_errorbar(data=group_dist_r1r2r3_betas, 
                aes(x=Run, ymin = mean-se, ymax = mean+se), 
                width=0.15, alpha=0.8, inherit.aes=FALSE) +
  labs(x = element_blank(), y = "Beta value", title = "Subject-level betas by run") +
  guides(fill = guide_legend(title="Variable")) +
  facet_grid(Variable~dx) +
  theme_bw()

setwd(plotDir)
ggsave("dist_betas_r1r2r3_subj_group.png")


# Plot subject betas Run 1-2
ggplot(dist_coef_r1r2r3_plot, aes(x=Run1, y=Run2, color=Variable)) +
  geom_point(size = 2.5, alpha=0.7) + 
  labs(x = "Run 1", y = "Run 2",
       color = "Variable", 
       title = "Run 1 and 2 subject betas") +
  scale_color_manual(values = c("red","green"," blue")) +
  # facet_wrap(.~Variable) + #, scales = "free_x") +
  stat_smooth(method=lm, alpha=0.15) +
  scale_x_continuous(breaks=seq(-1,1.25,.5), limits=c(-1.1,1.25)) +
  scale_y_continuous(breaks=seq(-1,1.25,.5), limits=c(-1.1,1.25)) +
  theme_bw()
ggsave("subj_betas_r1r2r.png")

# Plot subject betas Run 1-3
ggplot(dist_coef_r1r2r3_plot, aes(x=Run1, y=Run3, color=Variable)) +
  geom_point(size = 2.5, alpha=0.7) + 
  labs(x = "Run 1", y = "Run 3",
       color = "Variable", 
       title = "Run 1 and 3 subject betas") +
  scale_color_manual(values = c("red","green"," blue")) +
  # facet_wrap(.~Variable) + #, scales = "free_x") +
  stat_smooth(method=lm, alpha=0.15) +
  scale_x_continuous(breaks=seq(-1,1.25,.5), limits=c(-1.1,1.25)) +
  scale_y_continuous(breaks=seq(-1,1.25,.5), limits=c(-1.1,1.25)) +
  theme_bw()
ggsave("subj_betas_r1r3.png")

# Plot subject betas Run 2-3
ggplot(dist_coef_r1r2r3_plot, aes(x=Run2, y=Run3, color=Variable)) +
  geom_point(size = 2.5, alpha=0.7) + 
  labs(x = "Run 2", y = "Run 3",
       color = "Variable", 
       title = "Run 2 and 3 subject betas") +
  scale_color_manual(values = c("red","green"," blue")) +
  # facet_wrap(.~Variable) + #, scales = "free_x") +
  stat_smooth(method=lm, alpha=0.15) +
  scale_x_continuous(breaks=seq(-1,1.25,.5), limits=c(-1.1,1.25)) +
  scale_y_continuous(breaks=seq(-1,1.25,.5), limits=c(-1.1,1.25)) +
  theme_bw()
ggsave("subj_betas_r2r3.png")

# Plot group-level distance by run
ggplot(group_dist_r1r2r3, aes(x=Punish, y=Distance, 
                              color=factor(Reward), linetype = factor(Run), 
                              group = interaction(Reward,Run))) +
  geom_line(size=0.75) + geom_point() + 
  geom_errorbar(aes(ymin = Distance - se, ymax = Distance + se), 
                size=0.75, width=.1) +
  labs(x = "Punishment", y = "Distance", 
       color = "Reward",
       linetype = "Task Run",
       title = "Group-level Distance") +
  scale_x_continuous(breaks = c(0:10)) +
  theme_bw()
ggsave("group_dist_r1r2r3.png")

# Linear regression by run
ggplot(dist_data, aes(x=Reward_magnitude*Punishment_magnitude, y=DistanceFromDoor_SubTrial,
                      group = factor(Subject), color = factor(Subject))) +
  geom_point(alpha=0.3) +
  labs(x = "Reward*Punishment", y = "Distance", 
       fill = "Distance", 
       color = "Subject",
       title = "Subject-level Distance Regression (by run)") +
  stat_smooth(method=lm, alpha=0.2) +
  facet_grid(~RunNumber)+
  theme_bw() 
ggsave("r1r2r3_subj_regressionlines.png")


### Run 1 vs. Run 2 vs. Run 3 RT ###

# RT average: by run and subject
subj <- unique(log_rt$Subject)
subj_rt_r1r2r3 = data.frame()

for (s in subj) {
  runtype <- unique(log_rt$RunNumber)
  aa = data.frame()
  for(n in runtype) {
    reward <- c(1:7)
    aa1 = data.frame()
    for (r in reward) {
      punishment <- c(1:7)
      aa2 = data.frame()
      for (p in punishment) {
        x <- subset(log_rt, Subject == s)
        x <- subset(x, RunNumber == n)
        x <- subset(x, Reward_magnitude == r)
        x <- subset(x, Punishment_magnitude == p)
        y <- psych::describe(x$loge)
        y <- y[,c("mean","sd","se")]
        y$Reward <- r
        y$Punish <- p
        y$RunNumber <- n
        y$Subject <- s
        aa2 <- rbind(aa2, y)
      }
      aa1 <- rbind(aa1, aa2)  
    }
    aa <- rbind(aa, aa1)
  }
  subj_rt_r1r2r3 <- rbind(subj_rt_r1r2r3, aa)
}

subj_rt_r1 <- subset(subj_rt_r1r2r3, RunNumber==1)
subj_rt_r2 <- subset(subj_rt_r1r2r3, RunNumber==2)
subj_rt_r3 <- subset(subj_rt_r1r2r3, RunNumber==3)

# Average distance of subjects by run
group_rt_r1 <- avg_of_var(subj_rt_r1)
names(group_rt_r1)[1] <- "logRT"
group_rt_r1$Run <- 1

group_rt_r2 <- avg_of_var(subj_rt_r2)
names(group_rt_r2)[1] <- "logRT"
group_rt_r2$Run <- 2

group_rt_r3 <- avg_of_var(subj_rt_r3)
names(group_rt_r3)[1] <- "logRT"
group_rt_r3$Run <- 3

# Combine runs
group_rt_r1r2r3 <- rbind(group_rt_r1, group_rt_r2, group_rt_r3)

# Plot group-level RT by run
ggplot(group_rt_r1r2r3, aes(x=Punish, y=logRT, 
                            color=factor(Reward), linetype = factor(Run), 
                            group = interaction(Reward,Run))) +
  geom_line(size=0.75) + geom_point() + 
  geom_errorbar(aes(ymin = logRT - se, ymax = logRT + se), 
                size=0.75, width=.1) +
  labs(x = "Punishment", y = "log(Reaction Time)", 
       color = "Reward",
       linetype = "Task Run",
       title = "Group-level RT by run") +
  scale_x_continuous(breaks = c(0:10)) +
  facet_wrap(.~Reward) +
  theme_bw()
setwd(plotDir)
ggsave("group_rt_r1r2r3.png")

# Plot distance distribution by R/P
subj_dist_long <- subj_dist %>%
  pivot_longer(mean:se,
               names_to = "stat",
               values_to = "distance") %>%
  subset(stat == "mean") %>%
  pivot_longer(Reward:Punish,
               names_to = "name",
               values_to = "magnitude")

ggplot(subj_dist_long, aes(x=distance, fill=factor(magnitude))) +
  geom_density(alpha=0.3) +
  labs(x = "Distance", y = "Density", 
       fill = "Magnitude", title = "Distance Density") +
  facet_wrap(.~name) + #, scales="free_y") +
  theme_bw()
ggsave("PvsR_dist_kerneldensity.png")

# Plot RT distribution by run
ggplot(subj_rt_r1r2r3, aes(x=mean, fill=factor(RunNumber))) +
  geom_density(alpha=0.4) +
  labs(x = "log(Reaction Time)", y = "Density", 
       fill = "Run", title = "Subject-level RT density by run") +
  facet_wrap(.~Subject, scales = "free_y") +
  theme_bw()
ggsave("subj_r1r2r3_rt_kerneldensity.png")


########
# N+1
########





# Subj-level distance
subj_nplus1 = data.frame()
subj <- unique(dist_data$Subject)


for (s in subj) {
  trialtype <- c("1_lag_P", "1_lag_R", "1_lag_nofeedback")
  x = data.frame()
  for(t in trialtype) {
    reward <- c(1:7) #old: 3,5,7
    x1 = data.frame()
    for (r in reward) {
      punishment <- c(1:7) #old: 0:9
      x2 = data.frame()
      for (p in punishment) {
        z <- subset(dist_data, Subject == s)
        z <- subset(z, nplus1 == t)
        z <- subset(z, Reward_magnitude == r)
        z <- subset(z, Punishment_magnitude == p)
        z <- data.frame(psych::describe(z$DistanceFromDoor_SubTrial))
        z <- z[,c("mean","sd","se")]
        z$Reward_magnitude <- r
        z$Punishment_magnitude <- p
        z$Subject <- s
        z$nplus1 <- t
        z <- data.frame(z)
        names(z)[1] <- "DistanceFromDoor_SubTrial"
        x2 <- rbind(x2, z)
      }
      x1 <- rbind(x1, x2)  
    }
    x <- rbind(x, x1)
  }
  subj_nplus1 <- rbind(subj_nplus1, x)
}

# get data
trialtype <- c("1_lag_P", "1_lag_R", "1_lag_nofeedback")
nplus1 = data.frame()
for(t in trialtype) {
  reward <- c(1:7)
  x = data.frame()
  for (r in reward) {
    punishment <- c(1:7)
    x1 = data.frame()
    for (p in punishment) {
      x2 <- subset(subj_nplus1, nplus1 == t)
      x2 <- subset(x2, Reward_magnitude == r)
      x2 <- subset(x2, Punishment_magnitude == p)
      x3 <- psych::describe(x2$DistanceFromDoor_SubTrial)
      x3 <- x3[,c("mean","sd","se")]
      x3$Reward <- r
      x3$Punish <- p
      x3$nplus1 <- t
      x1 <- rbind(x1, x3)
    }
    x <- rbind(x, x1)  
  }
  nplus1 <- rbind(nplus1, x)
}

# plot N+1 by condition
ggplot(nplus1, aes(x=Punish, y=mean, color=factor(Reward)), 
       group = (Reward)) +
  geom_line() + geom_point() + 
  geom_errorbar(aes(ymin = mean-se, ymax = mean+se), width=.1) +
  labs(x = "Punishment", y = "Distance", color = "Reward", 
       title = "N+1") +
  scale_x_continuous(breaks = c(0:10)) +
  facet_grid(.~nplus1) +
  theme_classic()

### N+1 regression ###

dist_data <- dist_data %>%
  mutate(nplus1 = factor(nplus1, levels=c("1_lag_P","1_lag_R","1_lag_nofeedback")),
         nplus2 = factor(nplus2, levels=c("2_lag_P","2_lag_R","2_lag_nofeedback")),
         nplus3 = factor(nplus3, levels=c("3_lag_P","3_lag_R","3_lag_nofeedback"))
  )

lm_nplus1 <- lm(scale(DistanceFromDoor_SubTrial) ~ scale(Reward_magnitude) * scale(Punishment_magnitude) * factor(nplus1), 
                data=dist_data, na.action=na.exclude)
summary(lm_nplus1)
summary(lm_nplus1)$coef
contrasts(dist_data$nplus1)

Anova(lm_nplus1, test.statistic="F", type=3)

# plot N+1 regression
ggplot(drop_na(dist_data, nplus1), aes(x = Reward_magnitude*Punishment_magnitude, y = DistanceFromDoor_SubTrial,
                                       color=nplus1,
                                       group=nplus1)) + 
  geom_point(shape = 19, size = 1, alpha=0.5) +
  geom_smooth(method="lm", size=1, alpha=0.3) +
  labs(x = "Reward x Punishment", y = "Distance from door", title = "N+1 regression",
       color = "Previous outcome") +
  facet_wrap(.~dx) +
  theme_classic()


### old N+1
ind <- subset(lme_data, Subject==23986)
ind_lm <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.,
             data = ind)
summary(ind_lm)
anova(ind_lm)

ind_p <- subset(ind, boolean=="TRUE")
ind_r <- subset(ind, boolean=="FALSE")
p_lm <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.,
           data = ind_p)
r_lm <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.,
           data = ind_r)
summary(r_lm)

ind$boolean.f <- factor(ind$boolean)
is.factor(ind$boolean.f)
ind_rp <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.*boolean.f, data = ind)
summary(ind_rp)
coef_rp <- coef(ind_rp)
names(coef_rp)[2] <- "Reward"
names(coef_rp)[3] <- "Punishment"
names(coef_rp)[4] <- "R*P"

ggplot(ind, aes(x=RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial., y=DistanceFromDoor.SubTrial.,
                group = factor(boolean.f), color = factor(boolean.f))) +
  geom_point() +
  labs(x = "Reward*Punishment", y = "Distance", fill = "Distance", title = "D ~ R*P*(N+1)") +
  theme_light() +
  stat_smooth(method=lm, alpha=0.2)

# ANCOVA for N+1
rpn <- aov(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.*boolean.f, 
           data = ind)
summary(rpn)
install.packages("car")
library(car)
leveneTest(DistanceFromDoor.SubTrial.~boolean.f, ind)
Anova(rpn, type="III")

rp_ancova <- read.table(file = "clipboard",
                        sep = "\t", header=TRUE)

ind_coeff <- coeff[4,]

#####
# loge RT by RP plot
#####
# create histogram for RT distribution by subject
ggplot(logRT, aes(loge)) +
  geom_histogram(binwidth = 10, fill = "blue", alpha = 0.3) +
  facet_wrap(~ Subject, scales = 'free_x')


#check z-scored RT distribution
ggplot(zscores, aes(loge)) +
  geom_histogram(binwidth = 0.1, fill = "blue", alpha = 0.3)


# correlation logRT and Distance
scatter.smooth(logRT$DistanceFromDoor.SubTrial., logRT$DoorAction.RT.SubTrial.)
cor.test(logRT$DistanceFromDoor.SubTrial., logRT$DoorAction.RT.SubTrial., use="pairwise.complete.obs")

#Variance
ggplot(avg_avg_RT, aes(x=Punish, y=sd, 
                       group = factor(Reward), color=factor(Reward))) +
  geom_line() +
  geom_point() +
  labs(x = "Punishment", y = "Variability", fill = "sd") +
  scale_x_continuous(breaks = c(0:10)) +
  theme_classic()

scatter.smooth(x=p_lme_data$Distance, 
               y=stand_RT$logeReactionTime, main = "Dist ~ RT")
cor(p_lme_data$Distance, stand_RT$logeReactionTime)

scatter.smooth(x=stand_RT$logeReactionTime, 
               y=stand_RT$sd, main = "RT ~ variance")
cor(stand_RT$logeReactionTime, stand_RT$sd)

scatter.smooth(x=p_lme_data$Distance, 
               y=stand_RT$sd, main = "Dist ~ RT variance")
cor(p_lme_data$Distance, stand_RT$sd)


#####
# N+1 as beta for regression
#####

#check distance response distribution per subject
ggplot(lme_data, aes(DistanceFromDoor.SubTrial.)) +
  geom_histogram(binwidth = 20, fill = "red", alpha = 0.3) +
  facet_wrap(~ Subject, scales = 'free_x')

#dummy vars for win/loss/null
lme_data$Nplus1.f <- factor(lme_data$Nplus1)
contrasts(lme_data$Nplus1.f) = contr.treatment(3)
summary(lm(DistanceFromDoor.SubTrial.~Nplus1.f, data = lme_data))

lme_data <- within(lme_data, {
  Nplus1.ct <- C(Nplus1.f, treatment)
  print(attributes(Nplus1.ct))
})
summary(lm(DistanceFromDoor.SubTrial. ~ Nplus1.ct, data = lme_data))


lme_data <- lme_data[order(lme_data$Subject, lme_data$RunNumber, lme_data$SubTrial),]
lme_data$n1_pun = ifelse(lme_data$Outcome=="TRUE" & lme_data$Opened=="TRUE", 1, 0)
lme_data$n1_rew = ifelse(lme_data$Outcome == "FALSE" & lme_data$Opened == "TRUE", 1, 0)
lme_data$n1_na = ifelse(lme_data$Opened == "FALSE", 1, 0)

#convert to factor
lme_data$n1_pun = as.factor(lme_data$n1_pun)
lme_data$n1_rew = as.factor(lme_data$n1_rew)
lme_data$n1_na = as.factor(lme_data$n1_na)

#N-2 trial
for (i in 1:nrow(lme_data)+2) {
  if (lme_data[i-1,15] == 1){
    lme_data[i, "n2_pun"] = 1
  } else {
    lme_data[i, "n2_pun"] = 0
  }
}
for (i in 1:nrow(lme_data)+2) {
  if (lme_data[i-1,16] == 1){
    lme_data[i, "n2_rew"] = 1
  } else {
    lme_data[i, "n2_rew"] = 0
  }
}


#linear regression for N-1 betas
lm1 <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.*n1_na, 
          data = lme_data)

summary(lm1)

lm2 <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.*n1_pun, 
          data = lme_data)

summary(lm2)

lm3 <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial.*n1_rew, 
          data = lme_data)

summary(lm3)

#separate by N+1 trial
nplus1_r <- subset(lme_data, n1_rew == 1)
nplus1_p <- subset(lme_data, n1_pun == 1)
nplus1_na <- subset(lme_data, n1_na == 1)

lm_1 <- lmList(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial. | Nplus1, 
               data = lme_data, na.action = na.omit)

summary(lm_1)

lm_1.1 <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial., 
             data = nplus1_r, na.action = na.omit)
summary(lm_1.1)

lm_1.2 <- lm(DistanceFromDoor.SubTrial. ~ RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial., 
             data = nplus1_p, na.action = na.omit)
summary(lm_1.2)


lm_2 <- lm(DistanceFromDoor.SubTrial. ~ n1_rew*n1_pun*n1_na, 
           data = lme_data)

summary(lm_2)

plot(lm1)

#check response distribution N-1
ggplot(subset(lme_data, !is.na(lme_data[ ,14])), aes(DistanceFromDoor.SubTrial.)) +
  geom_histogram(binwidth = 10, fill = "red", alpha = 0.3) +
  facet_wrap(~ Nplus1, scales = 'free_x')

lme_data1 <- lme_data[complete.cases(lme_data),]

ggplot(lme_data1, aes(x=RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial., 
                      y=DistanceFromDoor.SubTrial.,
                      color = factor(Nplus1))) +
  geom_point() +
  labs(x = "Reward*Punishment", y = "Distance", 
       fill = "Distance", title = "D ~ R * P * previous trial") +
  theme_bw() +
  stat_smooth(method=lm, alpha=0.2)

ggplot(nplus1_na, aes(x=RewardMagnitude.SubTrial.*PunishmentMagnitude.SubTrial., 
                      y=DistanceFromDoor.SubTrial.)) +
  geom_point() +
  labs(x = "Reward*Punishment", y = "Distance", 
       fill = "Distance", title = "D ~ R * P * previous trial") +
  theme_bw() +
  stat_smooth(method=lm, alpha=0.2)
