list_1 = ["a", "b", "c"]
list_2 = list_1
del list_2[0]
print list_1
list_3 = ["x", "y", "z"]
list_4 = list_3[:] #copies the whole list into a new memory location
del list_4[0]
print list_3



list_1 = ["a", "b", "c", "d", "e", "f", "g"]
list_2 = list_1[-4:] # empty space on right side of colon means goes through the end

#dictionaries are mutable

my_dictionary = {1:'Clark University', 2:'WPI', 3:'Holy Cross'}

items = my_dictionary.items()

# items are tuples
    #tuples in the list are immutable, but can modify the list items in it




