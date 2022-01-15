## ui.R
# By "Krishna Shekhram(NetID:ks32), Eric Ellwanger(NetID:fre2) and Uttam Roy (NetID:uroy)"

library(shiny)
library(shinybusy)
library(shinydashboard)
library(recommenderlab)
library(data.table)
library(ShinyRatingInput)
library(shinyjs)
library(dplyr)

###########
# LOAD UI #
###########

shinyUI(fluidPage(
  
  # load page layout
  dashboardPage(
    
    dashboardHeader(title="Movie Recommender", titleWidth = 300),
    
    dashboardSidebar(width = 300,
                     sidebarMenu(
                       menuItem("By Genre", tabName = "Genres", icon = icon("film")),
                       menuItem("By Rating", tabName = "Recommender", icon = icon("star")),
                       HTML(paste0(
                         "<br><br><br><br><br><br><br><br><br>",
                         "<script>",
                         "var today = new Date();",
                         "var yyyy = today.getFullYear();",
                         "</script>"
                       ))
                     )
    ), # end dashboardSidebar
    
    dashboardBody(includeCSS("css/movies.css"),
                  tabItems(
                    tabItem(tabName = "Genres",
                            # Genre section
                            fluidRow(
                              box(width = 12, title = "Step 1: Choose a Genre to get Recommendations", status = "info", solidHeader = TRUE,
                                  br(),
                                  # includeMarkdown("www/tree.md"),
                                  column(3, uiOutput("genreSelectComboTree")),
                                  br(), br(), br(), br(), br(),
                                  tableOutput("genreResults")
                              )
                            ) 
                    ),
                    tabItem(tabName = "Recommender",
                            # Recommender section
                            fluidRow(
                              box(width = 12, title = "Step 1: Rate as many movies as possible for best reccomendations", status = "info", solidHeader = TRUE, collapsible = TRUE,
                                  div(class = "rateitems", uiOutput('ratings'))
                              )
                            ),
                            fluidRow(
                              useShinyjs(),
                              box(width = 12, status = "info", solidHeader = TRUE, title = "Step 2: Discover movies you might like",
                                  add_busy_spinner(spin = "fading-circle"),
                                  br(),
                                  actionButton("btn", "Click here to get your recommendations", class = "btn-warning"),
                                  br(), br(), br(),
                                  tableOutput("recomendResults")
                              )
                            )
                    )
                  )
    ) # end dashboardBody
    
  )# end dashboardPage
  
))