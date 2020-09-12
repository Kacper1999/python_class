import math
from editdistance import eval as ed  # https://pypi.org/project/editdistance/0.3.1/

# from project.edit_dist import edit_dist as ed

max_ed = 0.25  # max edit distance


def collection_ed(text: str, collection):
    lowest_ed = math.inf
    for t in collection:
        curr_ed = ed(t, text)
        if curr_ed < lowest_ed:
            lowest_ed = curr_ed
    return lowest_ed


def collection_ed_to_len_ratio(text: str, collection):
    return collection_ed(text, collection) / len(text)


class KWGroups:
    def __init__(self, kw_group, cmd_id):
        self.cmd_id = cmd_id
        self.kw_group = kw_group

    def __contains__(self, word: str):
        return math.ceil(len(word) * max_ed) >= self.ed(word)

    def ed(self, word: str):
        return collection_ed(word, self.kw_group)

    def ed_to_len_ratio(self, word):
        return collection_ed_to_len_ratio(word, self.kw_group)


class Object:
    def __init__(self, name: str, obj_id: str):
        self.id = obj_id
        self.name = name

    def __str__(self):
        return f"NAME: {self.name}\tID: {self.id}"


class House:
    def __init__(self):
        self.objects = dict()
        self.curr_obj_id = "A"

    def __getitem__(self, text: str):
        if not self.__contains__(text):
            raise ValueError
        return self.objects[self.get_name_with_lowest_ed(text)]

    def __contains__(self, text: str):
        return math.ceil(len(text) * max_ed) >= self.ed(text)

    def __str__(self):
        output = ""
        for obj in self.objects.values():
            output += obj.__str__() + "\n"
        return output

    def ed(self, word: str):
        return collection_ed(word, self.objects.keys())

    def ed_to_len_ratio(self, word: str):
        return collection_ed_to_len_ratio(word, self.objects.keys())

    def get_name_with_lowest_ed(self, text: str):
        lowest_ed = math.inf
        name = None
        for obj_name in self.objects.keys():
            curr_ed = ed(obj_name, text)
            if curr_ed < lowest_ed:
                name = obj_name
                lowest_ed = curr_ed
        return name

    def next_obj_id(self):
        for c in self.curr_obj_id:
            if c != "Z":
                return self.curr_obj_id[:-1] + chr(ord(c) + 1)
        return self.curr_obj_id + "A"

    def add_obj(self, name, obj_id=None):  # passing obj_id should be only used when we want several names
        if obj_id is None:
            obj_id = self.curr_obj_id
            self.curr_obj_id = self.next_obj_id()
        if name in self.objects:
            print("Object name already taken")
            return
        self.objects[name] = Object(name, obj_id)


def main():
    h = House()
    for i in range(27):
        obj_name = "light " + str(i)
        h.add_obj(obj_name)
    print(h)
    print("light 3" in h)

    house = House()
    house.add_obj("światło w duży m pokoju")
    house.add_obj("światło w kuchni")
    house.add_obj("światło", "A")
    house.add_obj("budzik")
    print(house)


if __name__ == '__main__':
    main()
