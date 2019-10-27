import numpy as np


class TrainingSample:
    """
    This class dont know how to describe(

    __data: - training sample
    name: - name of training sample
    __intervals: - array values from min to max value data and divided to 2n+1 parts
    __max_data: (list of dictionary) - max values from intervals and zone where it located
    zones - list of zones
    """

    def __init__(self, t_data: np.ndarray, name: str, n: int, zones_names: list):
        """
        create training data
        :param x: training data
        :param name: name of data
        :param n: intervals number
        :param zones: name of intervals
        """
        self.data = np.array(t_data)
        self.name = name
        self.intervals = np.linspace(min(self.data), max(self.data), 2 * n + 1)
        self.zones_names = zones_names
        self.max_values = np.zeros(len(t_data))
        self.zones = np.zeros(len(t_data), dtype=str)
        self.create_data()

    def create_data(self):
        """
        adds maximum values and zones to the arrays of results
        """

        for i in range(len(self.data)):
            self.max_values[i], self.zones[i] = self.__find_max(self.data[i])

    def __find_max(self, x: float):
        """
        finds the maximum value among the intervals
        :param x: x from training sample
        :return: (dictionary)  max values from intervals and zone where it located
        """
        max_data = self.__get_x(x, self.intervals[0], self.intervals[1], self.intervals[3])
        odd_elems = self.intervals[1::2]
        n = len(odd_elems)
        i = 0
        zone = 0
        while i <= (n - 3):
            temp = self.__get_x(x, odd_elems[0], odd_elems[1], odd_elems[2])
            if temp > max_data:
                max_data = temp
                zone += 1
            i += 1
        temp = self.__get_x(x, odd_elems[-2], odd_elems[-1], self.intervals[-1])
        if temp > max_data:
            max_data = temp
            zone += 1
        return max_data, self.zones_names[zone]

    @staticmethod
    def __get_x(x: float, left: float, mid: float, right: float) -> float:
        """
        method for calculating x
        :param x: x from data
        :param left: start of interval
        :param mid: mid of interval
        :param right: end of interval
        :return result of function:
        """
        if x < mid:
            return (x - left) / (mid - left)
        else:
            return (x - right) / (mid - right)


class FuzzyModel:
    def __init__(self):

        self.__training_data = []
        self.__training_result = []
        self.values_left = None
        self.zones_left = None
        self.values_right = None
        self.zones_right = None

    def add_training_data(self, data: TrainingSample):
        self.__training_data.append(data)

    def add_training_result(self, data: TrainingSample):
        self.__training_result.append(data)

    def create_rules(self):
        self.values_left, self.zones_left = self.__create_left_side()
        self.values_right, self.zones_right = self.__create_right_side()

    def __create_left_side(self):
        data_zones = self.__training_data[0].zones
        data_values = self.__training_data[0].max_values
        if len(self.__training_data) < 1:
            return data_values.T, data_zones.T
        else:
            for i in range(1, len(self.__training_data)):
                data_zones = np.vstack((data_zones, self.__training_data[i].zones))
                data_values = np.vstack((data_values, self.__training_data[i].max_values))
        return data_values.T, data_zones.T

    def __create_right_side(self):
        data_zones = self.__training_result[0].zones
        data_values = self.__training_result[0].max_values
        if len(self.__training_result) < 1:
            return data_values.T, data_zones.T
        else:
            for i in range(1, len(self.__training_result)):
                data_zones = np.vstack((data_zones, self.__training_result[i].zones))
                data_values = np.vstack((data_values, self.__training_result[i].max_values))
        return data_values.T, data_zones.T

    def check_conflicts(self):
        conflict_indices = []
        for i in range(len(self.zones_left) - 1):
            for j in range(i + 1, len(self.zones_left)):
                if np.array_equal(self.zones_left[i], self.zones_left[j]):
                    conflict_indices.append(self.compare_rules(i, j))

        self.delete_conf_rules(conflict_indices)

    def compare_rules(self, i, j):
        sum_i = np.sum(self.values_left[i]) + np.sum(self.values_right[i])
        sum_j = np.sum(self.values_left[j]) + np.sum(self.values_right[j])
        if sum_i > sum_j:
            return i
        else:
            return j

    def delete_conf_rules(self, indices):
        for i in indices:
            self.values_left = np.delete(self.values_left, i, 0)
            self.zones_left = np.delete(self.zones_left, i, 0)
            self.values_right = np.delete(self.values_left, i, 0)
            self.zones_right = np.delete(self.zones_left, i, 0)

    def print_rules(self):
        for i in range(len(self.rules_left)):
            print("{} - IF {} THEN {}".format(i, self.rules_left[i], self.rules_right[i]))
