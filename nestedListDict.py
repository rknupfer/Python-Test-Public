


mylist = [
    {u'id': 5650,
     u'children': [
         {u'id': 4635},
         {u'id': 5648}
     ]},
    {u'id': 67,
     u'children': [
         {u'id': 77}
     ]}
]

def extract_id_values(mylist):
    ids_to_return_dict = {}

    for element in mylist:
        for key, value in element.items():
            if 'id' == key:
                ids_to_return_dict['id'] = value
            if 'children' == key:
                for children_elem in value:
                    if 'id' in children_elem:
                        
                        # Either one of the three following statements works to do the same thing - 
                        # assign the new nested value of 'children' to the new dictionary:
                        # ids_to_return_dict['id'] = value
                        ids_to_return_dict = {'children':[{'id':value}]}
                        # ids_to_return_dict = dict(id=value)
                        
                        # Not yet working:
                        ids_to_return_dict.update(['children'][{'id':value}])
                        ids_to_return_dict.update(children = value)

                        
    return ids_to_return_dict


# print(extract_id_values(mylist))
extract_id_values(mylist)
for element in mylist:
    print (element)


