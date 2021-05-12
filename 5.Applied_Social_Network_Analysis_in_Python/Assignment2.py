
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 2 - Network Connectivity
# 
# In this assignment you will go through the process of importing and analyzing an internal email communication network between employees of a mid-sized manufacturing company. 
# Each node represents an employee and each directed edge between two nodes represents an individual email. The left node represents the sender and the right node represents the recipient.

# In[2]:


import networkx as nx

# This line must be commented out when submitting to the autograder
# !head email_network.txt


# ### Question 1
# 
# Using networkx, load up the directed multigraph from `email_network.txt`. Make sure the node names are strings.
# 
# *This function should return a directed multigraph networkx graph.*

# ### Question 2
# 
# How many employees and emails are represented in the graph from Question 1?
# 
# *This function should return a tuple (#employees, #emails).*

# In[3]:


import pandas as pd


def answer_one():
    df = pd.read_csv('email_network.txt', sep='\t', header=0)
    df.rename(columns={'#Sender': 'Sender'}, inplace=True)
    df['Sender'] = df['Sender'].apply(str)
    df['Recipient'] = df['Recipient'].apply(str)
    records = df[['Sender', 'Recipient']].to_records(index=False)
    result = list(records)
    G = nx.MultiDiGraph()
    G.add_edges_from(result)

    return G
    
G = answer_one()
# G.edges()
# G.degree("1")



# In[4]:


def answer_two():
        
    G = answer_one()
    edgeNum = len(G.edges())
    nodeNum = len(G.nodes())

    return (nodeNum, edgeNum)

answer_two()


# ### Question 3
# 
# * Part 1. Assume that information in this company can only be exchanged through email.
# 
#     When an employee sends an email to another employee, a communication channel has been created, allowing the sender to provide information to the receiver, but not vice versa. 
# 
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
# 
# 
# * Part 2. Now assume that a communication channel established by an email allows information to be exchanged both ways. 
# 
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
# 
# 
# *This function should return a tuple of bools (part1, part2).*

# In[5]:


def answer_three():
    G = answer_one()
    part1 = nx.is_strongly_connected(G)
    part2 = nx.is_weakly_connected(G)
    
    return (part1, part2)

answer_three()


# ### Question 4
# 
# How many nodes are in the largest (in terms of nodes) weakly connected component?
# 
# *This function should return an int.*

# In[6]:


def answer_four():
    G = answer_one()
    num =len(max(nx.weakly_connected_components(G)))
    
    return num

answer_four()


# ### Question 5
# 
# How many nodes are in the largest (in terms of nodes) strongly connected component?
# 
# *This function should return an int*

# In[7]:


def answer_five():
        
    G = answer_one()
    num = len(max(nx.strongly_connected_components(G), key=len))
    
    return num

answer_five()



# ### Question 6
# 
# Using the NetworkX function strongly_connected_component_subgraphs, find the subgraph of nodes in a largest strongly connected component. 
# Call this graph G_sc.
# 
# *This function should return a networkx MultiDiGraph named G_sc.*

# In[8]:


def answer_six():
        
    G = answer_one()
    G_sc = max(nx.strongly_connected_component_subgraphs(G), key=len)
    
    return G_sc


answer_six()


# ### Question 7
# 
# What is the average distance between nodes in G_sc?
# 
# *This function should return a float.*

# In[9]:


def answer_seven():
        
    G_sc = answer_six()
    averageDistance = nx.average_shortest_path_length(G_sc)
    
    return averageDistance

answer_seven()


# ### Question 8
# 
# What is the largest possible distance between two employees in G_sc?
# 
# *This function should return an int.*

# In[10]:


def answer_eight():
        
    G_sc = answer_six()
    diameter = nx.diameter(G_sc)
    
    return diameter

answer_eight()


# ### Question 9
# 
# What is the set of nodes in G_sc with eccentricity equal to the diameter?
# 
# *This function should return a set of the node(s).*

# In[11]:


def answer_nine():
    G_sc = answer_six()
    diameter = answer_eight()
    eccentricity = nx.eccentricity(G_sc)
    
    nodes = set()
    for key in eccentricity:
        if eccentricity[key] == diameter:
            nodes.add(key)

    return nodes


answer_nine()


# ### Question 10
# 
# What is the set of node(s) in G_sc with eccentricity equal to the radius?
# 
# *This function should return a set of the node(s).*

# In[12]:


def answer_ten():
    G_sc = answer_six()
    radius = nx.radius(G_sc)
    eccentricity = nx.eccentricity(G_sc)
    
    nodes = set()
    for key in eccentricity:
        if eccentricity[key] == radius:
            nodes.add(key)

    return nodes


answer_ten()


# ### Question 11
# 
# Which node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter of G_sc?
# 
# How many nodes are connected to this node?
# 
# 
# *This function should return a tuple (name of node, number of satisfied connected nodes).*

# In[17]:


def answer_eleven():    
    G_sc = answer_six()
    diameter = nx.diameter(G_sc)
    nodes = answer_nine()
    
    maxCount = 0
    name = '0'
    for u in G_sc.nodes():
        count = 0
        shortestPath = nx.shortest_path(G_sc, source=u)
        for v in shortestPath:
            if len(shortestPath[v]) == diameter + 1:
                count += 1
        if maxCount < count:
            maxCount = count
            name = u
    
    return (name, maxCount)

answer_eleven()





# In[51]:


def answer_twelve():
        
    # Your Code Here
    
    return # Your Answer Here

G = nx.DiGraph()

G.add_edge(1,2); G.add_edge(1,4)
G.add_edge(3,1); G.add_edge(3,2)
G.add_edge(3,4); G.add_edge(2,3)
G.add_edge(4,3)

print("periphery:", nx.periphery(G))
print("diameter:", nx.diameter(G))
print("all shortest paths starting at 1:",
      nx.shortest_path(G, 1))



# ### Question 13
# 
# Construct an undirected graph G_un using G_sc (you can ignore the attributes).
# 
# *This function should return a networkx Graph.*

# In[14]:


def answer_thirteen():
    G_sc = answer_six()
    G_un = nx.Graph()
    for u, v in G_sc.edges():
        G_un.add_edge(u, v)
    
    return G_un

G = answer_thirteen()
# len(G.edges())


# ### Question 14
# 
# What is the transitivity and average clustering coefficient of graph G_un?
# 
# *This function should return a tuple (transitivity, avg clustering).*

# In[15]:


def answer_fourteen():
        
    G_un = answer_thirteen()
    avgClustering = nx.average_clustering(G_un)
    transitivity = nx.transitivity(G_un)
    
    
    return (transitivity, avgClustering)

answer_fourteen()


# In[ ]:




