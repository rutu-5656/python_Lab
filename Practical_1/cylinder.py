
radius  = int(input("Enter the radius of the cylinder: "))
height = int(input("Enter the height of the cylinder: "))

volume = 3.14 * radius * radius * height
surface_area = 2 * 3.14 * radius * (radius + height)

print("Volume of the cylinder is:", volume)
print("Surface area of the cylinder is:", surface_area)
