# coding=utf-8
import random


def main():
    ga = GeneticAlgorithm()
    ga.run_ga()


class GeneticAlgorithm():
    def __init__(self):
        self.population_size = 100
        self.number_of_genes = 30
        self.crossover_probability = 0.9
        self.mutation_probability = 1 / self.number_of_genes
        self.tournament_selection_parameter = 0.75  # выбрать лучшего из турнира с вероятностью p
        self.tournament_size = 3
        self.number_of_generations = 150
        self.number_of_best_individual_copies = 1
        self.fitness = [0 for x in range(self.population_size)]
        self.population = self.initialize_population(self.population_size, self.number_of_genes)

    # ГА
    def run_ga(self):
        for iGenerations in range(self.number_of_generations):
            maximum_fitness = 0.0
            x_best = [0, 0]
            best_individual = None

            # Декодирование хромосомы и оценка особи в популяции
            for i in range(self.population_size):
                chromosome = self.population[i]
                # Декодирование iой хромосомы
                x = self.decode_chromosome(chromosome)

                # оценка её приспособленности
                self.fitness[i] = self.evaluate_individual(x)
                if self.fitness[i] > maximum_fitness:  # особь - лучшая
                    maximum_fitness = self.fitness[i]
                    x_best = x
                    best_individual = chromosome

            temp_population = self.population  # Создание временной популяции

            # Турнир
            for i in range(round(self.population_size / 2)):
                j = i * 2
                # выбор двух лучших для кроссовера
                i1 = self.tournament_select(self.fitness, self.tournament_selection_parameter, self.tournament_size)
                i2 = self.tournament_select(self.fitness, self.tournament_selection_parameter, self.tournament_size)
                chromosome_1 = self.population[i1]
                chromosome_2 = self.population[i2]

                # кроссовер
                r = random.random()
                # если рандомное число меньше кроссовер вероятности, то кроссовер
                # и вставить обе особи из новой пары в популяцию
                if r < self.crossover_probability:
                    new_chromosome_pair = self.cross(chromosome_1, chromosome_2)
                    temp_population[j] = new_chromosome_pair[0]
                    temp_population[j + 1] = new_chromosome_pair[1]
                else:
                    temp_population[j] = chromosome_1
                    temp_population[j + 1] = chromosome_2

            # мутация
            for i in range(self.population_size):
                original_chromosome = temp_population[i]
                mutated_chromosome = self.mutate(original_chromosome, self.mutation_probability)
                # заменить на мутированную хромосому в популяции
                temp_population[i] = mutated_chromosome

            # добавить лучшего в популяцию, если найден
            if best_individual is not None:
                temp_population = self.insert_best_individual(temp_population, best_individual,
                                                              self.number_of_best_individual_copies)
            # замена популяции новой промежуточной популяцией
            population = temp_population
            print("фитнес", maximum_fitness, iGenerations, "x_ best", x_best)

        print("maximum_fitness: " + str(maximum_fitness))
        print("x-values (x_best): " + str(x_best))

    # Инициализация популяции
    def initialize_population(self, population_size, number_of_genes):
        population = [[0 for y in range(number_of_genes)] for x in range(
            population_size)]  # двумерный массив с нулями. x =  population_size, y= number_of_genes
        for i in range(population_size):
            for j in range(number_of_genes):
                if random.random() < 0.8:
                    population[i][j] = 1  # вставить единицы в случайные места
        return population

    # Декодирование хромомсомы
    def decode_chromosome(self, chromosome):
        n_genes = len(chromosome)  # 30
        x = [0.0 for x in range(1)]  # список из 0.0 до числа 1
        for i in range(1):
            for j in range(30, 0, -1):
                # x[i] = x[i] + chromosome[30 * (i - 1) + j] * 2 ** (-j)
                x[i] = x[i] + chromosome[30 - j] * 2 ** (-j)
                # print(x[i])
                # с конца умножить на 2^-j
            # x[i] = 2 - 2 * (-x[i]) / (-1 + 2 ** (-n_split))
            x[i] = (20 * (x[i])) - 10
            # print("x[i]", x[i])
        # print("x[i] j", x[i])
        return x

    # Оценка особи x
    def evaluate_individual(self, x):
        g = (6 * (x[0] - 1.5))
        fitness_value = 1 / g
        # чем меньше g, тем kexit
        # print("g: ", g, "fitness: ", fitness_value)
        return fitness_value

    # турнирный отбор для выбора лучшего as a parent для кроссовера
    def tournament_select(self, fitness, tournament_selection_parameter, tournament_size):
        i_tmp_vector = [0 for x in range(tournament_size)]
        fitness_vector = [0 for x in range(tournament_size)]
        i_selected = None
        for i in range(tournament_size):
            i_tmp_vector[i] = int(random.random() * self.population_size)  # выбор 3 Случайных особей
            fitness_vector[i] = fitness[i_tmp_vector[i]]  # оуенка их приспособленности

        no_chosen_index = True
        while no_chosen_index:
            idx_maximum = fitness_vector.index(max(fitness_vector))  # выбор максимальный фитнес
            # прогон трех особей до выбора одного лучшего:
            if len(fitness_vector) > 1:  # особей больше чем 1, то
                if random.random() < tournament_selection_parameter:  # случайно выбираем одну особь с максимум фитнесс
                    i_selected = i_tmp_vector[idx_maximum]
                    # print("i_selected ", i_tmp_vector, i_selected, fitness_vector)
                    no_chosen_index = False
                else:
                    fitness_vector.pop(idx_maximum)  # удалет из списка объект с индексом idx_maximum и возвращает его
                    i_tmp_vector.pop(idx_maximum)
                    # print("i_selected (else)", i_tmp_vector,fitness_vector)
                # 2
            else:
                i_selected = i_tmp_vector[0]
                no_chosen_index = False
                # print("i_selected (else) утв ", i_tmp_vector, i_selected)
            # 1
        # print("i_selected ==== ", i_tmp_vector, i_selected,fitness_vector)
        return i_selected

    # Кроссовер
    def cross(self, chromosome_1, chromosome_2):
        n_genes = len(chromosome_1)  # 30
        crossover_point = round(random.random() * (n_genes))  # точка скрещивания = рандомное число от 0 до 1 * 30
        # создание двух новых хромосом из нулей
        new_chromosome_pair = [[0 for y in range(n_genes)] for x in
                               range(2)]  # список до 2, заполненный списком из 0ей до 60
        for j in range(n_genes):
            if j < crossover_point:  # если j меньше точки скрещивания то
                new_chromosome_pair[0][j] = chromosome_1[j]
                new_chromosome_pair[1][j] = chromosome_2[j]

            else:
                new_chromosome_pair[0][j] = chromosome_2[j]
                new_chromosome_pair[1][j] = chromosome_1[j]
        # 00|00 и 00|00 ----> chromosome_1|chromosome_2 или chromosome_2|chromosome_1
        return new_chromosome_pair

    # мутация
    def mutate(self, chromosome, mutation_probability):
        mutated_chromosome = chromosome
        for j in range(self.number_of_genes):
            if random.random() < mutation_probability:
                mutated_chromosome[j] = 1 - chromosome[j]
        return mutated_chromosome

    # заменить на лучшего
    def insert_best_individual(self, population, best_individual, number_of_best_individual_copies):
        for i in range(number_of_best_individual_copies):
            population[i] = best_individual
        return population


if __name__ == "__main__":
    main()
