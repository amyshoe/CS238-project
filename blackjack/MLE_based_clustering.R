##MAximum Likelihood Based Subsequence Clustering Algorithm

##required libraries
library(QUIC)
library(ggplot2)
library(MASS)

##---------Choosing the dataset
rm(list=ls())
setwd("~/Downloads/")
#setwd("~/Documents/")

#returns_data = read.table("SP500_10SpecialStocks.txt")
# returns_data = read.table("returns.txt")

##----------Get Data into proper format
##No Test and trainng Division currently
n= 10
list_n = 1:n
# train_dat = returns_data[,list_n]
# data1 = train_dat
# data2 = train_dat
# m1 = dim(data1)[1]
# data1 = data1[-c(m1),]
# data2 = data2[-c(1),]
# data_matrix = data.matrix(data.frame(data1,data2))
m = dim(data_matrix)[1]

##-----------Perform iterations of the MLE Clustering Algorithm
num_iter = 20
num_clusters = 2 # Number of clusters predefined
initial_clusters = sample(1:num_clusters,size = m, replace = TRUE)

##Get all the cluster points
cluster_points = list()
for(i in 1:num_clusters){
	cluster_points[[i]] = (initial_clusters == i)
} 
##Store the initial CLuster Covariance matrices
##Use the QUIC solver
lambda = 1e-6 #some value of lambda
covariance_matrices  = list()
for(i in 1:num_clusters){
	cat("i is:",i)
	temp_matrix = data_matrix[cluster_points[[i]],]
	n_i = dim(temp_matrix)[2]
	m_i = dim(temp_matrix)[1]
	##Get the rho matrix
	rho = mat.or.vec(n_i,n_i) + 0
	rho[1:n,(n+1):(2*n)] = lambda
	rho[(n+1):(2*n),(1:n)] = lambda
	
	cov_mat = 	t(temp_matrix)%*%(temp_matrix)/m_i
	##Use the quic solver
	out = QUIC(S = cov_mat, rho = rho)
	
	##This is the INVERSE COVARIANCE
	covariance_matrices[[i]] = out$X 	
}

##just a sanity check here to compare the values of the two terms
i=2
x_i = data_matrix[i,]
cat("log Det of inverse is:", log(det(covariance_matrices[[5]])), "while xt*sig*xt is:",x_i%*%covariance_matrices[[1]] %*%x_i )
temp_mt = covariance_matrices
temp_ass = assignments

















##-----------------MLE CLustering Alogrithm
##Iterate some number of times with the clustering algorithm
covariance_matrices = temp_mt
m = dim(data_matrix)[1]
lambda = 1e-6
num_iter = 50

for (iter in 1:num_iter){
	cat("ITERATION #", iter,"\n")
	
	##Get all the cluster points
	assignments = list()
	for (k in 1:num_clusters){
		#print("First step of listing")
		assignments[[k]] = list()
		
	}
	#cat("length of assignments is:",length(assignments))
	for( i in 1:m){
		best_cluster_num = -1
		best_cluster_score = -Inf
		x_i = data_matrix[i,]
		
		##For each point compute the score w.r.t a covariance matrix
		for(k in 1:num_clusters){
			score = 0
			const1 = (det(covariance_matrices[[k]])) ** (-0.5/n)
			const2 = (x_i)%*%covariance_matrices[[k]]%*%x_i
			score = const1*const2#((x_i)%*%covariance_matrices[[k]]%*%x_i) + log(det(covariance_matrices[[k]]))
			score = score[1,1]
			#cat("MAT",k,"logdet is:",const1,"x*E*x is",const2 ,"\n")
			if(score > best_cluster_score){
				best_cluster_score = score
				best_cluster_num = k
			}

		}
		#cat("Ressigning point ",i,"to:,",best_cluster_num,"\n")

		#cat("Best CLuster number is:",best_cluster_num)
		#print("Control is here!")
		##Assign the point to a cluster
		assignments[[best_cluster_num]] = c(assignments[[best_cluster_num]],c(i))
		
	}
	#cat("length of assignments is:",length(assignments),"\n")
	final_assignments = list()
	##Unlist each of the assignments before returning
	for(k in 1:num_clusters){
		#print("unlising")
		final_assignments[[k]] = unlist(assignments[[k]])
		#print("done unlisting")
		cat("Length of assignmet#",k,"---->",length(final_assignments[[k]]),"\n")
		#print(unlist(assignments[[k]]))
	}
	# assignments = MLE_cluster_assignment(covariance_matrices, data_matrix,num_clusters)
	#cat("LENGTH OF ASSIGNMENTS IS:",length(final_assignments))
	
	##given the assignments - Recompute Covariance matrices
	for(i in 1:num_clusters){
	
	temp_matrix = data_matrix[final_assignments[[i]],]
	n_i = dim(temp_matrix)[2]
	
	##Get the rho matrix
	rho = mat.or.vec(n_i,n_i) + 0
	rho[1:n,(n+1):(2*n)] = lambda
	rho[(n+1):(2*n)] = lambda
	m_i = dim(temp_matrix)[1]
	cov_mat = t(temp_matrix) %*% (temp_matrix)/m_i
	##Use the quic solver
	out = QUIC(S = cov_mat, rho = rho)
	
	##This is the INVERSE COVARIANCE
	covariance_matrices[[i]] = out$X 	
	}

}

##Framework for comparison - Greedy allocation algorithm
matchings = 1:num_clusters
matchings_dict2 = c()
for(iter in 1:num_clusters){
	min_val = Inf
	min_index = -1
	index = 1
	for(match in matchings){
		diff = norm(Sigs[[iter]] - covariance_matrices[[match]], type = c("F"))
		if(diff < min_val){
			min_index = index
			min_val = diff
		}
		index = index + 1
	}
	##mapped
	matchings_dict2[iter] = matchings[min_index]
	matchings = matchings[-min_index] 

}
list_diff = c()
for(i in 1:num_clusters){
	list_diff[i] = norm( Sigs[[i]] - covariance_matrices[[matchings_dict2[i]]], type = c("F"))/norm(Sigs[[iter]])

}


##Get a matrix of correct to incorrect predictions

preds = mat.or.vec(num_clusters, num_clusters) + 0

#length(intersect(final_assignments[[1]],1:2000))
for(i in 1:num_clusters){
	for(j in 1:num_clusters){
		print(j)
		preds[i,j] = length(intersect(final_assignments[[j]],((i-1)*2000+1):(i*2000)))
	}
}
preds = preds[1:num_clusters,matchings_dict2]
colnames(preds) = 1:num_clusters
colnames(preds) = paste("Predicted", colnames(preds), sep = "_")
row.names(preds) = 1:num_clusters
row.names(preds) = paste("True", row.names(preds), sep = "_")

