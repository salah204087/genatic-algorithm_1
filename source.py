import random
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt

Chromosome=[[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,1],[0,1,1,0,0],[0,1,1,0,1],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,1],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,1],[0,1,1,0,1],[0,1,1,0,0],[0,1,1,0,0],[0,1,1,0,1]]
def fitness(Chromosome):
    fit=[]
    fit=list(map(sum,Chromosome))
    return fit


def Selection(relative):
    relative_fitness=[]
    for i in range (len(relative)):
        relative_fitness.append(relative[i]/sum(relative))
    return relative_fitness

def cumulative(prob,relative):
    total_sum=0.0
    cumulative_probabilities=[]
    for i in range (len(prob)):
        total_sum+=prob[i]
        cumulative_probabilities.append(total_sum)
    return cumulative_probabilities


def one_point_crossover(cum,Chromosome,pcross,len_chromosome):
    gene=[]
    for i in range(10):
        parent1_cum=0.0
        parent2_cum=0.0
        index_parent1=0
        index_parent2=0
        child1=[]
        child2=[]     
        cut=0.0
        for i in range (len(cum)):
            if random.random()<cum[i]:
                parent1_cum=cum[i-1]
                index_parent1=cum.index(parent1_cum)
                break
            else:
                continue
        for i in range (len(cum)):
            if random.random()<cum[i]:
                parent2_cum=cum[i-1]
                index_parent2=cum.index(parent2_cum)
                break
            else:
                continue
        cut=pcross*len_chromosome
        parent1=Chromosome[index_parent1]
        parent2=Chromosome[index_parent2]
        for i in range (int(cut)):
            child1.append(parent1[i])
        for i in range (int(cut),len_chromosome-int(cut)-1,-1):
            child1.append(parent2[i])
        for i in range (int(cut)):
            child2.append(parent2[i])
        for i in range (int(cut),len_chromosome-int(cut)-1,-1):
            child2.append(parent1[i])
        gene.append(child1)
        gene.append(child2)
    return gene

def mutation(gen,pmut,len_chromosome):
    nextgene=[]
    for i in range(len(gen)):
        genen=[]
        for j in range(len_chromosome):
            if random.random() < pmut:
                genen.append(int(not gen[i][j]))
            else:
                genen.append(gen[i][j])
        nextgene.append(genen)
    return nextgene


def generation(population,number_of_generation,len_chromosome,pcross,pmut):
    highest_fitness=[]
    average_fitness=[]
    all_population=[]
    gen=Chromosome
    for i in range (int(number_of_generation/population)):
        all_population.append(mutation(one_point_crossover(cumulative(Selection(fitness(gen)), fitness(gen)),gen,0.6,5),0.05,5))
        highest_fitness.append(max(fitness(gen)))
        average_fitness.append(mean(fitness(gen)))
        gen=mutation(one_point_crossover(cumulative(Selection(fitness(gen)), fitness(gen)),gen,0.6,5),0.05,5)
    print("The final population:")
    print(all_population[int(number_of_generation/population)-1])
    for i in range(int(number_of_generation/population)):
        print("The highest fitness in "+ str(i+1) +" generation:"+str(highest_fitness[i]))
        print("The average fitness in "+ str(i+1) +" generation:"+str(average_fitness[i]))
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x=np.array(highest_fitness)
    y=np.array(average_fitness)
    plt.plot(x,color="blue")
    plt.title("fitness acurracy without elitism")
    plt.plot(y, color="red")
    plt.show()

generation(20,100 ,5, 0.6, 0.05)

def elitism(size_of_elitism,population,number_of_generation,len_chromosome,pcross,pmut):
    highest_fitness=[]
    average_fitness=[]
    all_population=[]
    gen=Chromosome
    copy_of_gene=[]
    for i in range (int(number_of_generation/population)):     
        all_population.append(gen)
        highest_fitness.append(max(fitness(gen)))
        average_fitness.append(mean(fitness(gen)))
        gen=mutation(one_point_crossover(cumulative(Selection(fitness(gen)), fitness(gen)),gen,0.6,5),0.05,5)
        copy_of_gene=gen.copy()
        for i in range(size_of_elitism): 
            index=fitness(copy_of_gene).index(max(fitness(copy_of_gene)))
            fitness(copy_of_gene)[index]=0
            gen[i]=mutation(one_point_crossover(cumulative(Selection(fitness(gen)), fitness(gen)),gen,0.6,5),0.05,5)[index]
    print("The final population with elitism:")
    print(all_population[int(number_of_generation/population)-1])
    for i in range(int(number_of_generation/population)):
        print("The highest fitness in "+ str(i+1) +" generation with elitism:"+str(highest_fitness[i]))
        print("The average fitness in "+ str(i+1) +" generation with elitism:"+str(average_fitness[i]))
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x=np.array(highest_fitness)
    y=np.array(average_fitness)
    plt.plot(x,color="blue")
    plt.title("fitness acurracy with elitism")
    plt.plot(y, color="red")
    plt.show()
        
elitism(2,20,100 ,5, 0.6, 0.05)