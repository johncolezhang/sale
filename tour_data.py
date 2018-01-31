import pandas as pd
import numpy as np



if __name__ == "__main__":
    country_category_feature = ['country_distance', 'country_area', 'country_language', 'country_language_distance']
    country_feature = ['distance', 'area', 'language', 'language_distance']
    countries = pd.read_csv('data/countries.csv', dtype=str)
    countries.columns = ['country', 'lat', 'lng', 'distance', 'area', 'language', 'language_distance']

    #print(countries[countries['country'].isin(['AU'])])

    country_name = list(set(countries['country']))
    country_destination = []
    for name in country_name:
        for feature in country_feature:
            country_destination.append(name + "-" + feature)

    cd_info = []
    for cd in country_destination:
        [name, feature] = cd.split("-")
        cd_info.append(countries[feature][countries['country'] == name].values)

    # country_code = dict(zip(country_name, range(len(country_name))))
    # language = list(set(countries['language']))
    #
    # language_code = dict(zip(language, range(len(language))))


    age_gender = pd.read_csv('data/age_gender_bkts.csv', dtype=str)
    age_gender.columns = ['age_range', 'country', 'gender', 'population', 'year']

    #ag_feature = ['country', 'age_range', 'gender']
    age_range = []
    ag_name = []
    ag_value = []
    for value in age_gender.values:
        age_range.append(value[0])
        ag_name.append(value[0] + "_" + value[1] + "_" + value[2]) #range_nation_gender
        ag_value.append(value[3])
    age_range = list(set(age_range))

    ag_dict = dict(zip(ag_name, ag_value))

    # age_gender_list = age_gender.loc[:, ag_feature]
    # age_gender_list = list(set(map(tuple, age_gender_list.values.tolist())))
    #
    # ag_name = []
    # for ag in age_gender_list:
    #     ag_name.append(ag[0] + "_" + ag[1] + "_" + ag[2])
    #
    # for name in ag_name:
    #     print()

    train = pd.read_csv('data/train_users_2.csv', dtype=str)
    train.columns = ['id', 'date_created', 'time_first', 'first_booking', 'gender', 'age', 'signup_method',
                     'signup_flow', 'own_language', 'affiliate_channel', 'affiliate_provider', 'first_affiliate',
                     'signup_app', 'first_device', 'first_browser', 'country_destination']


    ######### deal with age range ############
    def deal_age_range(value):
        ar = []
        for age in value:
            if type(age) is str:
                age = int(float(age))
                if age < 5:
                    age = '0-4'
                    ar.append(age)
                    continue
                elif age < 10:
                    age = '5-9'
                    ar.append(age)
                    continue
                elif age >= 100:
                    age = '100+'
                    ar.append(age)
                    continue
                else:
                    age_10 = int(age / 10)
                    age_1 = int(age % 10)
                    if age_1 >= 5:
                        age = str(age_10) + str(5) + "-" + str(age_10) + str(9)
                    else:
                        age = str(age_10) + str(0) + "-" + str(age_10) + str(4)
                    ar.append(age)
            else:
                ar.append(str(age))
        return ar


    pd.DataFrame(np.array([[0, 0], [1, 1]])).to_csv("test.csv")

    train['age'] = pd.Series(deal_age_range(train['age'].values))

    print(set(train['signup_method'].values))
    print(set(train['signup_flow'].values))
    print(set(train['affiliate_channel'].values))
    print(set(train['affiliate_provider'].values))
    print(set(train['first_affiliate'].values))
    print(set(train['signup_app'].values))
    print(set(train['first_device'].values))
    print(set(train['first_browser'].values))

    age_gender_feature = list(map(lambda x: x + "age_gender", country_name))

    ages = train['age'].values
    genders = train['gender'].values
    age_set = list(set(ages))
    gender_set = list(set(genders))

    age_gender_value = []
    age_gender_name = []
    for age in age_set:
        for gender in gender_set:
            country_ag_info = []
            age_sex = age + "_" + gender
            age_gender_name.append(age_sex)
            for name in country_name:
                age_sex_name = age + "_" + name + "_" + gender.lower()
                if age_sex_name in ag_dict.keys():
                    country_ag_info.append(ag_dict[age_sex_name])
                else:
                    country_ag_info.extend([0] * len(country_name))
                    break
            age_gender_value.append(country_ag_info)

    age_gender_dict = dict(zip(age_gender_name, age_gender_value))

    first = True
    for i in range(len(ages)):
        if (i + 1) % 10000 == 0:
            print(round(i / len(ages) * 100, 2), "%")
        ag_dict_value = age_gender_dict[ages[i] + '_' + genders[i]]

        if first:
            country_infos = np.array(ag_dict_value)
            first = False
        else:
            country_infos = np.vstack((country_infos, np.array(ag_dict_value)))


    country_infos = np.vstack((age_gender_feature, country_infos))

    ag_frame = pd.DataFrame(country_infos)
    ag_frame.to_csv("data/ag_fram.csv")





    # for _ in ag_name:
    #     train[_] = pd.Series(np.zeros(len(train)))
    # for _ in country_category_feature:
    #     train[_] = pd.Series(np.zeros(len(train)))
    #
    # for country in country_name:
    #     country_info = countries[countries['country'].isin([country])]
    #     train.loc[train['country_destination'] == country, 'country_distance'] = \
    #         country_info['distance'].values
    #     train.loc[train['country_destination'] == country, 'country_area'] = \
    #         country_info['area'].values
    #     train.loc[train['country_destination'] == country, 'country_language'] = \
    #         country_info['language'].values
    #     train.loc[train['country_destination'] == country, 'country_language_distance'] = \
    #         country_info['language_distance'].values

    #print(train['country_language_distance'].head(50))



    # cp = train.loc[:, ['affiliate_channel', 'affiliate_provider']]
    #
    #
    # cp = list(map(tuple, cp.values.tolist()))

    # train_category_feature = ['signup_method', 'signup_flow', 'signup_app']

    test = pd.read_csv('data/test_users.csv', dtype=str)
    test.columns = ['id', 'date_created', 'time_first', 'first_booking', 'gender', 'age', 'signup_method',
                    'signup_flow', 'own_language', 'sub_channel', 'sub_provider', 'first_sub',
                    'signup_app', 'first_device', 'first_browser']

    sess = pd.read_csv('data/sessions.csv', dtype=str)
    sess.columns = ['id', 'action', 'action_type', 'action_detail', 'device_type', 'secs']

