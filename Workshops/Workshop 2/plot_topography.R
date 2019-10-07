library(tidyverse)
library(akima)
library(scales)
library(mgcv)
library(gridExtra)
library(png)
library(grid)

#####
electrodeLocs <- read_delim("https://raw.githubusercontent.com/craddm/ExploringERPs/master/biosemi70elecs.loc",
                            "\t",
                            escape_double = FALSE,
                            col_names = c("chanNo","theta","radius","electrode"),
                            trim_ws = TRUE)

electrodeLocs$radianTheta <- pi/180*electrodeLocs$theta

electrodeLocs <- electrodeLocs %>%
  mutate(x = .$radius*sin(.$radianTheta),
         y = .$radius*cos(.$radianTheta))

polar <- ggplot(electrodeLocs,
                aes(radianTheta, radius, label = electrode)) +
  geom_text()+
  theme_bw()+
  coord_fixed(ratio = 6.75)

cartesian <- ggplot(electrodeLocs,
                    aes(x, y, label = electrode))+
  geom_text()+
  theme_bw()+
  coord_equal()

theme_topo <- function(base_size = 12)
{
  theme_bw(base_size = base_size) %+replace%
    theme(
      rect             = element_blank(),
      line             = element_blank(),
      axis.text = element_blank(),
      axis.title = element_blank()
    )
}

circleFun <- function(center = c(0,0),diameter = 1, npoints = 100) {
  r = diameter / 2
  tt <- seq(0,2*pi,length.out = npoints)
  xx <- center[1] + r * cos(tt)
  yy <- center[2] + r * sin(tt)
  return(data.frame(x = xx, y = yy))
}

headShape <- circleFun(c(0, 0), round(max(electrodeLocs$x)), npoints = 100) # 0
nose <- data.frame(x = c(-0.075,0,.075),y=c(.495,.575,.495))

#Define Matlab-style Jet colourmap
jet.colors <- colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan", "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))

######

electrodeLocs$electrode <- toupper(electrodeLocs$electrode)

S2_nm_sample_df <- read.csv("data_sample/S2_nm_sample.csv")
S2_nm_sample_df$sensor.position <- toupper(S2_nm_sample_df$sensor.position)

create_eeg_images <- function(folder, group) {
  i <- 0
  j <- 0
  MIN_VAL <- min(S2_nm_sample_df$sensor.value)
  MAX_VAL <- max(S2_nm_sample_df$sensor.value)
  for(i in seq(0, 250, by=10)) {
    ######
    
    sample_df <- S2_nm_sample_df %>% 
      select(-c(name, channel, trial.number)) %>% 
      dplyr::filter((subject.identifier == group) & (sample.num == i))
    
    sample_df <- left_join(electrodeLocs, sample_df, by = c("electrode" = "sensor.position"))
    sample_df <- sample_df %>% rename(amplitude = `sensor.value`)
    sample_df <- dplyr::filter(sample_df, !is.na(amplitude))
    
    ######
    gridRes <- 100 # Specify the number of points for each grid dimension i.e. the resolution/smoothness of the interpolation
    
    tmpTopo <- with(sample_df,
                    interp(x = x, y = y, z = amplitude,
                           xo = seq(min(x)*2,
                                    max(x)*2,
                                    length = gridRes),
                           yo = seq(min(y)*2,
                                    max(y)*2,
                                    length = gridRes),
                           linear = FALSE,
                           extrap = TRUE)
    ) 
    
    interpTopo <- data.frame(x = tmpTopo$x, tmpTopo$z)
    
    names(interpTopo)[1:length(tmpTopo$y)+1] <- tmpTopo$y
    
    interpTopo <- gather(interpTopo,
                         key = y,
                         value = amplitude,
                         -x,
                         convert = TRUE)
    
    interpTopo$incircle <- sqrt(interpTopo$x^2 + interpTopo$y^2) < .7 # mark grid elements that are outside of the plotting circle
    
    interpTopo <- interpTopo[interpTopo$incircle,] #remove the elements outside the circle
    
    maskRing <- circleFun(diameter = 1.42) #create a circle round the outside of the plotting area to mask the jagged edges of the interpolation
    
    splineSmooth <- gam(amplitude ~ s(x, y, bs = 'ts'),
                        data = sample_df)
    
    GAMtopo <- data.frame(expand.grid(x = seq(min(sample_df$x)*2,
                                              max(sample_df$x)*2,
                                              length = gridRes),
                                      y = seq(min(sample_df$y)*2,
                                              max(sample_df$y)*2,
                                              length = gridRes)))
    
    GAMtopo$amplitude <-  predict(splineSmooth,
                                  GAMtopo,
                                  type = "response")
    
    GAMtopo$incircle <- (GAMtopo$x)^2 + (GAMtopo$y)^2 < .7^2 # mark
    
    GAMplot <- ggplot(GAMtopo[GAMtopo$incircle,],
                      aes(x, y, fill = amplitude)) +
      geom_raster()+
      stat_contour(aes(z = amplitude),
                   binwidth = 0.5)+
      theme_topo()+
      scale_fill_gradientn(colours = jet.colors(10),
                           limits = c(MIN_VAL, MAX_VAL),
                           guide = "colourbar",
                           oob = squish)+
      geom_path(data = maskRing,
                aes(x, y, z = NULL, fill =NULL),
                colour = "white",
                size = 6)+
      geom_point(data = sample_df,
                 aes(x,y,fill = NULL))+
      geom_path(data = nose,
                aes(x, y, z = NULL, fill = NULL),
                size = 1.5)+
      geom_path(data = headShape,
                aes(x,y,z = NULL,fill = NULL),
                size = 1.5)+
      coord_quickmap() +
      labs(title=paste0(sample_df$time[sample_df$sample.num == i][1], " second")) +
      ggsave(paste0("/home/ruslan/Projects/EEG/data_sample/", folder, "/topography_", i, ".jpg"))
  }
}

create_eeg_images(folder = "a_topo", group = "a")
create_eeg_images(folder = "c_topo", group = "c")
