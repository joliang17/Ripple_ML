library(RSQLite)
library(dbplyr)
library(dplyr)
library(purrr)
library(ggplot2)
library(xts)
library(ggfortify)
library(ggthemes)
library(maps)
library(mapdata)
library(leaflet)

# Get the world map data
world_map <- map_data('world')
# 
"United States"     "Hong Kong"          "United Kingdom"     "Korea, Republic of"
country.name<-unique(world_map$region)
data.country<-dataset[which(!dataset$country %in% NA),]

data.country[data.country$country=='United States',]$country<-"USA"
data.country[data.country$country=='United Kingdom',]$country<-"UK"
data.country[data.country$country=='Hong Kong',]$country<-"China"
data.country[data.country$country=='Korea, Republic of',]$country<-"South Korea"
# Map the state abbreviations to state names so we can join with the map data
a<-NULL
for (i in 1:length(data.country))
{a<-append(a,country.name[grep(data.country[i], country.name)])}



colnames(world_map)[5]<-'country'

data.country %>% 
  select(country) %>%
  group_by(country) %>%
  summarize(n = n()) %>%
  right_join(world_map, by = 'country') %>%
  ggplot(aes(x = long, y = lat, group = group, fill = n)) + 
  geom_polygon() + 
  geom_path(color = 'white') + 
  scale_fill_continuous(low = "orange", 
                        high = "darkred",
                        name = 'Active level of country server') + 
  theme_map() + 
  coord_map('albers', lat0=30, lat1=40) + 
  ggtitle("world server") + 
  theme(plot.title = element_text(hjust = 0.5))



################################leafover
data.country %>%
  filter(country == "USA") %>%
  leaflet() %>% 
  setView(lat = -0.900653, lng = -78.467834, zoom = 7) %>% 
  addTiles() %>%
  addMarkers(
    ~LONGITUDE,
    ~LATITUDE,
    label = ~paste("Name:")
  )
##############################

