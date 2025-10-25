from sympy import symbols, diff
#The derivative of a function describes how the output of a 
# function changes when there is a small change in an input variable.
#Let's give a 'small change' a name epsilon or  𝜖
# 𝜖 can be any value 0.001, 0.0000001 or whatever 

J = (3)**2
J_epsilon = (3 + 0.001)**2
k = (J_epsilon - J)/0.001    # difference divided by epsilon
print(f"J = {J}, J_epsilon = {J_epsilon}, dJ_dw ~= k = {k:0.6f} ")

#J = 9, J_epsilon = 9.006001, dJ_dw ~= k = 6.001000



#Finding symbolic derivatives
#In backprop it is useful to know the derivative of simple functions at any input value
#Define the python variables and their symbolic names.

J, w = symbols('J, w')
J=w**2
print(J)

#Use SymPy's diff to differentiate the expression for  𝐽
#with respect to  𝑤
dJ_dw = diff(J,w)
print(dJ_dw)
# 2𝑤

#Evaluate the derivative at a few points by 'substituting' numeric 
# values for the symbolic values. In the first example,  𝑤 is replaced by  2
dJ_dw.subs([(w,2)])    # derivative at the point w = 2

dJ_dw.subs([(w,3)])    # derivative at the point w = 3

dJ_dw.subs([(w,-3)])    # derivative at the point w = -3