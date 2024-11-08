library(httr)
library(jsonlite)
library(dplyr)

api_url <- 'https://api.football-data.org/v4/competitions/matches/'
headers <- add_headers('X-Auth-Token' = '7ee3394168a140f98a511dd870124818')

response <- GET(api_url, headers)
if (status_code(response) == 200) {
  data <- content(response, as = "text")
  data <- fromJSON(data)
  df <- data$matches
  print(head(df))
}
