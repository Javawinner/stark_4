# a=[]
# b=[1,2,3]
#
# b.extend(a)
#
# print(b)


# class A(object):
# # #
# # #     def c(self):
# # #         patterns = [1, 2, 3]
# # #         patterns.extend(self.b())
# # #
# # #         return patterns
# # #
# # #     def b(self):
# # #         return []
# # #
# # #
# # # obj = A()
# # # print(obj.c())

class B(object):
    a=1

test=B()
print(getattr(test, 'b'))