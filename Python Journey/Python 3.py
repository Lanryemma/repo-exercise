import math
#Mathematical Operators
friends = 5
#friends = friends + 3 
friends += 3#this will also give us 8
friend1 = 13
#friend1 =friend1 - 7 #this will give us 6
friend1 -= 7 #this willl also give us 6
print(friends)
print(friend1)

#To multiply we use A*B or A*=B
#To divide we use A/B or A/=B
#TO raise to power we use A**B or A**=B
#To find he module we use A % B or A %= B(this will give use the remainder after division)

#built in functions
x = 3.5
y= -4
z = 5.2
result = round(x)
result1 = abs(y)#it finds the absolute value
result2 = pow(4, 3)#This means 4^3 = 64
result3 = max(x, y, z)
result4 = min(x, y, z)
print(result, result1, result2, result3, result4)

#Now we use the math function
result5 = math.ceil(z)
result6 = math.floor(x)
result7 = math.sqrt(64)
print(math.pi)
print(result5, result6, result7)

#now we calculate the circumference of a circle
# circumference o a circle is (2*pi*radius)
radius = float(input("Enter the radius of the circle: "))
circumference = 2 * math.pi * radius
print(f"The circumference of a {radius}cm radius circle is {round(circumference, 2)}cm")
#the round function will round it to two decimal place

#Now we calculate the area of a circle
# formula is (pi * radius^2)
radius1 = float(input("Enter the radius of the circle: "))
Area = math.pi * radius1 ** 2
print(f"The Area of a {radius1}cm radius circle is {round(Area, 2)}cm^2")

#Now we calculate the hypotenuse of a triangle
# formula = (hypotenuse =math.sqrt(opposite^2 + Adjacent^2) )
Opp = float(input("Enter the opposite length of the Triangle: "))
Adj = float(input("Enter the Adjacent length of the Triangle: "))
Hyp = math.sqrt(pow(Opp, 2) + pow(Adj, 2))
#Hyp = math.sqrt(Opp**2 + Adj**2)
print(f"The Hypotenuse of the Triangle is {round(Hyp, 2)}cm")

