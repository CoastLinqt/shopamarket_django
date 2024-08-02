def categories_get(object_name):
    list_data = []

    for categories in object_name:

        dict_data = dict()
        list_sub = []

        dict_data['id'] = categories.pk
        dict_data['title'] = categories.title
        dict_data['image'] = {"src": categories.src.url, "alt": categories.alt}

        for sub_cat in categories.all():

            dict_subcategories = dict()

            dict_subcategories['id'] = sub_cat.pk
            dict_subcategories['title'] = sub_cat.title
            dict_subcategories['image'] = {"src": sub_cat.src.url, "alt": sub_cat.alt}

            list_sub.append(dict_subcategories)

            dict_data['subcategories'] = list_sub
        list_data.append(dict_data)
    print(list_data)

    return list_data


