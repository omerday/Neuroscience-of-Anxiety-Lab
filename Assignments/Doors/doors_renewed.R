install.packages("psych")
install.packages("lme4")

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
vas_subj <- df[df$Section %in% c("VASpre","VAS1","VASmid", "VASpost"), ]
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