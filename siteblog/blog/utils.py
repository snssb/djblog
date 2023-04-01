class MyMixin(object):  # Может принимать object если надо
    mixin_prop = ''
    gslag = ''

    def get_prop(self):
        return self.mixin_prop.upper()  # Будем приводить строку к верх. регистру
