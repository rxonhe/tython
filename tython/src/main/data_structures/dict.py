class Dict(dict):
    def __hash__(self):
        return super

    def __eq__(self, other):
        return super


def dict_of(**kwargs):
    return Dict(**kwargs)
