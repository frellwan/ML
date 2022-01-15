## server.R
# By "Krishna Shekhram(NetID:ks32), Eric Ellwanger(NetID:fre2) and Uttam Roy (NetID:uroy)"

#define constants
TOP_N = 10
GENRES =  c("Action",
            "Adventure",
            "Animation",
            "Children's",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film-Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "War",
            "Western")

# define functions
get_user_ratings = function(value_list) {
  dat = data.table(MovieID = sapply(strsplit(names(value_list), "_"), 
                                    function(x) ifelse(length(x) > 1, x[[2]], NA)),
                   Rating = unlist(as.character(value_list)))
  dat = dat[!is.null(Rating) & !is.na(MovieID)]
  dat[Rating == " ", Rating := 0]
  dat[, ':=' (MovieID = as.numeric(MovieID), Rating = as.numeric(Rating))]
  dat = dat[Rating > 0]
  dat
}

# read in data
myurl = "https://liangfgithub.github.io/MovieData/"

ratings = read.csv(paste0(myurl, 'ratings.dat?raw=true'), 
                   sep = ':',
                   colClasses = c('integer', 'NULL'), 
                   header = FALSE)
colnames(ratings) = c('UserID', 'MovieID', 'Rating', 'Timestamp')
ratings$Timestamp = NULL

movies = readLines(paste0(myurl, 'movies.dat?raw=true'))
movies = strsplit(movies, split = "::", fixed = TRUE, useBytes = TRUE)
movies = matrix(unlist(movies), ncol = 3, byrow = TRUE)
movies = data.frame(movies, stringsAsFactors = FALSE)
colnames(movies) = c('MovieID', 'Title', 'Genres')
movies$MovieID = as.integer(movies$MovieID)
movies$Title = iconv(movies$Title, "latin1", "UTF-8")
movies$Year = as.numeric(unlist(lapply(movies$Title, 
                                       function(x) substr(x, nchar(x)-4, nchar(x)-1))))

small_image_url = "https://liangfgithub.github.io/MovieImages/"
movies$image_url = sapply(movies$MovieID, 
                          function(x) paste0(small_image_url, x, '.jpg?raw=true'))

#total <- merge(movies,ratings,by="MovieID")

tempratings = ratings %>%
  group_by(MovieID) %>%
  summarize(ratings_per_movie = n(), ave_ratings = mean(Rating)) %>%
  inner_join(movies, by='MovieID')

m = quantile(tempratings$ratings_per_movie, 3/4)
C = mean(tempratings$ave_ratings)

toprated = tempratings %>% 
  mutate(weighted.rating = (ratings_per_movie/(ratings_per_movie + m))*ave_ratings + (m/(ratings_per_movie+m))*C) %>%
  arrange(desc(weighted.rating))

# tmp = ratings %>% 
#         group_by(MovieID) %>% 
#         summarize(ratings_per_movie = n(), ave_ratings = mean(Rating)) %>%
#         inner_join(movies, by = 'MovieID') %>%
#         mutate(weighted.rating = (ratings_per_movie/(ratings_per_movie+350))*ave_ratings + (350/(ratings_per_movie+350))*3.239) %>%
#         arrange(desc(weighted.rating))

################
# SERVER LOGIC #
################
shinyServer(function(input, output, session) {
  
  # collapsible tree
  output$genreSelectComboTree <- renderUI({
    selectInput("selectedGenre","Select a genre:", GENRES)
  })
  
  genreMovies <- reactive(toprated[grep(input$selectedGenre, toprated$Genres), ])
  
  
  output$genreResults <- renderUI({
    num_movies_in_genre = nrow(genreMovies())
    num_rec_movies = min(num_movies_in_genre, TOP_N)
    num_cols <- 5
    num_rows <- ceiling(num_rec_movies/num_cols)
    
    lapply(1:num_rows, function(i) {
      list(fluidRow(lapply(1:num_cols, function(j) {
        movie_idx = (i - 1) * num_cols + j
        list(box(width = 2,
                 div(style = "text-align:center", img(src = genreMovies()$image_url[movie_idx], height = 150)),
                 #div(style = "text-align:center; color: #999999; font-size: 80%", books$authors[movie_idx]),
                 div(style = "text-align:center", strong(genreMovies()$Title[movie_idx]))
              )
           )
      })))
    })
  })
  
  
  # show the movies to be rated
  output$ratings <- renderUI({
    num_rows <- 20
    num_cols <- 6 # movies per row
    
    lapply(1:num_rows, function(i) {
      list(fluidRow(lapply(1:num_cols, function(j) {
        movie_idx = (i - 1) * num_cols + j
        list(box(width = 2,
                 div(style = "text-align:center", img(src = movies$image_url[movie_idx], height = 150)),
                 #div(style = "text-align:center; color: #999999; font-size: 80%", books$authors[movie_idx]),
                 div(style = "text-align:center", strong(movies$Title[movie_idx])),
                 div(style = "text-align:center; font-size: 150%; color: #f0ad4e;", 
                     ratingInput(paste0("select_", movies$MovieID[movie_idx]), label = "", dataStop = 5)))) #00c0ef
      })))
    })
  })
  
  # Calculate recommendations when the submit button is clicked
  df <- eventReactive(input$btn, {
      # hide the rating container
      useShinyjs()
      jsCode <- "document.querySelector('[data-widget=collapse]').click();"
      runjs(jsCode)
      
      # get the user's rating data
      gc()
      value_list <- reactiveValuesToList(input)
      user_ratings <- get_user_ratings(value_list)
      print(user_ratings)
      
      # add user's ratings as last rows of rating matrix
      new_rows = cbind(cbind(rep(9999, nrow(user_ratings))), user_ratings)
      colnames(new_rows) = c('UserID', 'MovieID', 'Rating')
      new_ratings = rbind(ratings, new_rows)
      
      i = paste0('u', new_ratings$UserID)
      j = paste0('m', new_ratings$MovieID)
      x = new_ratings$Rating
      DF = data.frame(i, j, x, stringsAsFactors = T)
      Rmat = sparseMatrix(as.integer(DF$i), as.integer(DF$j), x = DF$x)
      rownames(Rmat) = levels(DF$i)
      colnames(Rmat) = levels(DF$j)
      Rmat = new('realRatingMatrix', data = Rmat)
      rec_UBCF = Recommender(Rmat[-nrow(Rmat)], method = 'UBCF',
                             parameter = list(normalize = 'Z-score', 
                                              method = 'Cosine', 
                                              nn = 25))
      
      rm(DF)
      gc()
      #res <- predict(rec_UBCF, Rmat[nrow(Rmat)], type = 'topNList', n=5)
      res <- predict(rec_UBCF, Rmat[nrow(Rmat)], n=TOP_N)
      
      # sort, organize, and return the results
      user_results <- as(res, 'list')
      user_predicted_ids <- as.integer(sub('.', '', user_results[[1]]))
      
      recom_results <- data.table()
      for (i in 1:length(user_predicted_ids)){
              newdata = data.table(Rank = i, 
                                   MovieID = user_predicted_ids[i], 
                                   Title = movies$Title[movies$MovieID == user_predicted_ids[i]])
              recom_results = rbind(recom_results, newdata)
              gc()
     }
     gc()
     recom_results
      
    }) # still busy
    
  
  # display the recommendations
  output$recomendResults <- renderUI({
    recom_result <- df()
    num_cols <- 5
    num_rows <- ceiling(min(nrow(recom_result), TOP_N)/num_cols)

    lapply(1:num_rows, function(i) {
            list(fluidRow(lapply(1:num_cols, function(j) {
                    movie_idx = (i - 1) * num_cols + j
                    rec_movie_id = recom_result$MovieID[movie_idx]
                    
                    box(width = 2, status = "success", solidHeader = TRUE, title = paste0("Rank ", movie_idx),
                        div(style = "text-align:center", 
                            a(img(src = movies$image_url[movies$MovieID == rec_movie_id], height = 150))
                        ),
                        div(style="text-align:center; font-size: 100%", 
                            strong(movies$Title[movies$MovieID == rec_movie_id])
                        )
                    ) #box       
      }))) # columns
    }) # rows
    
  }) # renderUI function
  
}) # server function