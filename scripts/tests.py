__author__ = 'lorenzo'



from factory import Communication

c = Communication()
for v in vars(c):
    print v

print c.slug
print c.name

print c.is_constraint(c.mass)  # True
print c.is_constraint(c.cost)  # True
print c.is_constraint(c.name)  # False
print c.is_constraint(c.slug)  # False






