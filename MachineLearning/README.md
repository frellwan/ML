## Applications of Machine Learning
This course teaches how to use machine learning techniques to solve a wide variety of problems. This course will give you a strong grasp of the general principles of machine learning, including familiarity with
common approaches, assumptions, and methodologies. You should be able to assess the strengths, weaknesses,
and use cases of ML algorithms, and to select and apply the right tools for custom classification, regression, and
analysis problems. 

### Week 1
Demonstrate the vectorized math of numpy

### Week 2
Write a Naive Bayes classifier from scratch for the UC IRvine Diabetes dataset and compare to the sklearn implementation. Use SVMlight to see if a support vector machine performs better than a Naive Bayes classifier.

### Week 3
Compare multiple models (Naive Bayes Classifier with Gaussian or Bernoulli distributions and a Decision Forest) for the MNIST dataset. This compares pereprocessing the images vs. no preprocessing as well.

### Week 4
Using the UC Irvine banknote dataset, train a support vector machine using stochastic gradient decent from scratch comparing ridge, and lasso regularization (using several values of the regularization coefficient lambda) using hinge loss.

### Week 5
Use Principle Coordinate Analysis and principle component analysis to visualize the 2D difference between classes in the CIFAR10 dataset.

### Week 6
Use agglomorative clustering using single linkage, complete linkage, and group average linkage to analyze the European employment in 1979 dataset. Also look at K-means clustering and analyze the number of groups using the elbow plot and the silhouiette score.

### Week 7
Use a Random Forest claassification model for the activities of daily life dataset from the UC Irvine that has a series of acceleration readings for x, y, and z axis for 14 differnet actvities by quantizing the activity data and developoing features using k-means clustering. Use hyperparameter tuning to improve the model performance.

### Week 8
Use several data sets to demonstrate various regression models including linear regression, polynomial regression, and the effect ridge and lasso regularization methods. 

### Week 9
Compare lasso, ridge, and elastic net regularization for both linear and logistic regression models. Also investigate the effect of box-cox transformation on the effect on a non normal distributed dataset.

### Week 10
Find topics and frequently used words in a vocabulary dataset using expectation maximization based on a multinomial distribution (here we will use 30 topics). 

### Week 11
Use expectation maximization on a guassian mixture model for image segmentation based on several different numbers for segments.

### Week 12
Use a boltzman mean field approximation to classify MNIST images with noise added to them. Look at various hyperparameter values to improve the classification performance.

### Week 13
Develop a pytorch model using convulutional nueral network (CNN) layers to build a classifier for the CIFAR data set.

### Week 14
Design a denoising autoencoder using pytorch for the MNIST dataset that will use the first 5 principal components to to classify images. The variational autoencoder will learn the mean and standard deviation of the categories to generate images for each category.
