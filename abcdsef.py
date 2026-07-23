"""so lets formulate the plan ....we have done till chunking right? now we have 2 major milestones to cover 1.  Generation of Evolution tree 2. Generation of Knowledge package for every node in the evolution tree.....lets see how we will appoach now:


1. for the tree generation  we have 2 major hurdles. 1. what will be the candidate concepts and how will we choose between thousands of concepts what are really node worthy and what are just noise or supporting concepts 2. how will we decide parent child relationships between the nodes ...

       so here is my plan  we will make the chunks then We will pass the chunks to the LLM which will extract all terminologies to become a candidate node , parallelly we will  do HDBSCAN vector space semantic clustering of the chunks and find every cluster's' centroid and the concept around the centroid becomes a node then we will do a betweenness computuation of every chunk also"""
