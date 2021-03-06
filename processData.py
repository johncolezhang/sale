import pandas as pd
from sklearn import linear_model
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


def readfile(path):
    """
    data = pd.DataFrame(columns=['sale_date', 'class_id', 'sale_quantity', 'brand_id', 'compartment', 'type_id',
                                 'level_id', 'department_id', 'TR', 'gearbox_type', 'displacement', 'if_charging',
                                 'price_level', 'driven_type_id', 'fuel_type_id', 'newenergy_type_id',
                                 'emission_standards_id', 'if_MPV_id', 'if_luxurious_id', 'power', 'cylinder_number',
                                 'engine_torque', 'car_length', 'car_width', 'car_height', 'total_quality',
                                 'equipment_quality', 'rated_passenger', 'wheelbase', 'front_track', 'rear_track'])
    """
    csv_data = pd.read_csv(path, dtype=str)
    csv_data.columns = ['sale_date', 'class_id', 'sale_quantity', 'brand_id', 'compartment', 'type_id',
                        'level_id', 'department_id', 'TR', 'gearbox_type', 'displacement', 'if_charging',
                        'price_level', 'price', 'driven_type_id', 'fuel_type_id', 'newenergy_type_id',
                        'emission_standards_id', 'if_MPV_id', 'if_luxurious_id', 'power', 'cylinder_number',
                        'engine_torque', 'car_length', 'car_width', 'car_height', 'total_quality',
                        'equipment_quality', 'rated_passenger', 'wheelbase', 'front_track', 'rear_track']
    return csv_data


def classByDate(data, date):
    train_data = data[data.sale_date < date]
    test_data = data[data.sale_date >= date]

    def classByClass(t_data):
        t_dict = {}
        for row in t_data.iterrows():
            if row[1].values[1] not in t_dict.keys():
                t_dict[row[1].values[1]] = list()
            t_dict[row[1].values[1]].append(row[1])
        return t_dict

    train_data = classByClass(train_data)
    test_data = classByClass(test_data)
    return train_data, test_data



def timestamp(train_data, class_id):
    id_dict = {}
    for id in class_id:
        data = train_data[id]
        sale_list = []
        for row in data:
            sale_list.append((row['sale_date'], row['sale_quantity']))
        sort_list = sorted(sale_list, key=lambda tu: tu[0])  #sort by time
        id_dict[id] = sort_list
    return id_dict



def chooseStrategy(id_dict, strategy):
    dict_time = {}
    dict_sales = {}
    for id, tup in id_dict.items():
        time = []
        sales = []
        if strategy is 'average':
            count_sales = 0
            count = 0
            current = int(tup[0][0])
            for tu in tup:
                if current != int(tu[0]):
                    time.append(current)
                    current = int(tu[0])
                    sales.append(count_sales / count)
                    count_sales = 0
                    count = 0
                count += 1
                count_sales += int(tu[1])
            time.append(current)
            sales.append(count_sales / count)
        elif strategy is 'max':
            max_sales = 0
            current = int(tup[0][0])
            for tu in tup:
                if current != int(tu[0]):
                    time.append(current)
                    sales.append(max_sales)
                    current = int(tu[0])
                    max_sales = 0
                if int(tu[1]) > max_sales:
                    max_sales = int(tu[1])
            time.append(current)
            sales.append(max_sales)
        dict_time[id] = time
        dict_sales[id] = sales
    return dict_time, dict_sales


def linearRegression(dict_time, dict_sales):
    for id in dict_time.keys():
        time = dict_time[id]
        sales = dict_sales[id]
        reg = linear_model.LinearRegression()
        poly = PolynomialFeatures(degree=2)
        start = time[0]
        time = list(map(lambda x: subMonth(start, x), time))
        time = np.array(time).reshape(-1, 1)
        sales = np.array(sales).reshape(-1, 1)
        poly_time = poly.fit_transform(time)
        poly_sales = poly.fit_transform(sales)
        reg.fit(time, sales)
        test = np.array([subMonth(start, 201711)]).reshape(-1, 1)
        poly_test = poly.fit_transform(test)
        pre_sale = reg.predict(test)
        print(pre_sale)


def subMonth(start, time):
    start_year = int(start / 100)
    time_year = int(time / 100)
    start_month = int(start % 100)
    time_month = int(time % 100)
    return ((time_year - start_year) * 12 + (time_month - start_month) * 1) + 1



if __name__ == "__main__":
    data = readfile('data/train.csv')
    class_id = list(set(data['class_id'].values))

    date = '201710'
    train_data, test_data = classByDate(data, date)

    id_dict = timestamp(train_data, class_id)

    strategy = 'average'
    #strategy = 'max'
    dict_time, dict_sales = chooseStrategy(id_dict, strategy)
    linearRegression(dict_time, dict_sales)

