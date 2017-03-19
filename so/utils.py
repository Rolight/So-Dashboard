class _const:

    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError(
                "Cannot change value for constant: {name}".format(name=name))

        if not name.isupper():
            raise self.ConstCaseError(
                "Constant {name} should be in upper case".format(name=name))

        self.__dict__[name] = value
