# Oscar Alberto Santos Muñoz
# Example 5-4 from Diseño en Ingeniería Mecánica de Shigley 9a Edición
# In this code I will iterate over Table A-8 from the appendix of the book to
# prove that the 42x5 mm pipe is the solution that meets the requirements of the problem.
# Packages
import pandas as pd
import sympy as sp
import os
# Data
# Aliminium 2014
syt = 276000000 # Pa
nd = 4
F = 1750    # N
P = 9000    # N
T = 72      # Nm
L = 0.120   # m
# Print data
lst = [syt,nd,F,P,T,L]
lst_str = ['syt','nd','F','P','T','L']
for i in range(len(lst)):
    print(f'{lst_str[i]} = {lst[i]}')

print()
# Symbolic variables
M, c, r, do, A, I, J = sp.symbols('M c r do A I J')

# Strings
sigma = chr(963)
tau = chr(964)

# Ec 1
sx = P/A + (M*c)/I
print('Normal stress across the x-axis by tensile and bending stresses')
print(f'{sigma}x = {sx}')
sx = sx.subs({M:F*L, c:do/2})
print('Substituting M as F*L and c as do/2')
print(f'{sigma}x = {sx}  ...(1)')
print()

print('Shear stress across zx-plane due to torsion')
tzx = (T*r)/J
print(f'{tau}zx = {tzx}')
print('Substituting r as do/2')
tzx = tzx.subs(r,do/2)
print(f'{tau}zx = {tzx}  ...(2)')
print()
print(f"{sigma}' = ({sigma}\N{SUPERSCRIPT TWO} + 3*{tau}zx\N{SUPERSCRIPT TWO})^(1/2)  ...(3)")
print('Knowing that the design factor must be:')
print(f"{sigma}' <= Sy/nd = (276 X 10\N{SUPERSCRIPT SIX})/4 = 69 MPa")
print()
# Load data from the csv
df = pd.read_csv('TablaA8.csv')

d_col = df['Diameter']
A_col = df['A']
I_col = df['I']
J_col = df['J']

sx_lst = []
tzx_lst = []
EcVonMises_lst = []
n_lst = []

print('Despite I show the units in mm, cm\N{SUPERSCRIPT TWO} and cm\N{SUPERSCRIPT FOUR} all were translated in the csv file to m, m\N{SUPERSCRIPT TWO} and m\N{SUPERSCRIPT FOUR} for the calculations')
print('Here I will iterate over each row from the csv with each value of d, A, I and J')
for i in range(12):
    sx_lst.append(sx.subs({do:d_col[i], I:I_col[i], A:A_col[i]}))
    tzx_lst.append(tzx.subs({do:d_col[i], J:J_col[i]}))
    # print(f'Row: {i} with d={d_col[i]},I={I_col[i]},A={A_col[i]},J={J_col[i]}')
    print('Row: {} with d={:.2f} mm, I={:.2f} cm\N{SUPERSCRIPT FOUR}, A={:.2f} cm\N{SUPERSCRIPT TWO}, J={:.2f} cm\N{SUPERSCRIPT FOUR}'.format(i, d_col[i]*1000, I_col[i]*100000000, A_col[i]*10000, J_col[i]*100000000))
    EcVonMises_lst.append((sx_lst[i]**2 + 3*tzx_lst[i]**2)**(1/2))
    print(f"{sigma}' = {EcVonMises_lst[i]}")
    n_lst.append(syt/EcVonMises_lst[i])
    print(f'n = {n_lst[i]}')

print(f"Therefore the pipe with the smallest diameter that meets the condition {sigma}' <= Sy/nd = 69 MPa is 42x5mm from Table A8")

# Export results to csv
results = {
            'sigmax':sx_lst,
            'tauzx':tzx_lst,
            'sigma\'':EcVonMises_lst,
            'n':n_lst
            }

df_results = pd.DataFrame(results, columns= ['sigmax', 'tauzx','sigma\'','n'])
df_save = pd.concat([df, df_results], axis=1)
#print(df_save)
path = os.getcwd()
# Join paths
file_name = os.path.join(path,'results.csv')
df_save.to_csv(file_name, index = False, header=True)
if os.path.exists(file_name):
    print('Results were exported correctly')
else:
    print('Something went wrong while exporting')