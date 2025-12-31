class WebregEvent:
    def __init__(self, data):
        self.__data = data

        def __getattr__(self, name):
            return self.__data.get(name)
