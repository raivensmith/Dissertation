import numpy as np
import matplotlib.pyplot as plt


d65 = np.loadtxt('d65.txt')
d65_lambda = []
d65_flux = []

for i in range(0, len(d65)):
    d65_lambda.append(d65[i][0])
    d65_flux.append(d65[i][1])

plt.figure(dpi=300)
plt.plot(d65_lambda, d65_flux, 'k')
plt.title('D65 Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized Flux (Watts/nm)')
plt.xlim((350, 850))
plt.xticks(np.linspace(350, 850, 11))
plt.ylim(((0, 1)))
plt.grid()

cie = np.loadtxt('cie1931xyz.txt')
cie_lambda = []
cie_x = []
cie_y = []
cie_z = []

for j in range(0, len(cie)):
    cie_lambda.append(cie[j][0])
    cie_x.append(cie[j][1])
    cie_y.append(cie[j][2])
    cie_z.append(cie[j][3])

plt.figure(dpi=300)
plt.plot(cie_lambda, cie_x, 'r')
plt.plot(cie_lambda, cie_y, 'g')
plt.plot(cie_lambda, cie_z, 'b')
plt.title('CIE XYZ Tristimulus Curves')
plt.xlabel('Wavelength (nm)')
plt.legend(['X', 'Y', 'Z'])

# D65 Range Correction
d65_flux_start_from360 = d65_flux.copy()

for k in d65_flux[0:10]:
    d65_flux_start_from360.remove(k)

for l in d65_flux[411::]:
    d65_flux_start_from360.remove(l)

# CIE Range Correction
cie_lambda_start_from360nm = cie_lambda.copy()

for n in cie_lambda_start_from360nm[401::]:
    cie_lambda_start_from360nm.remove(n)

X = []
Y = []
Z = []

x = []
y = []

for m in range(0,len(d65_flux_start_from360)):
    X.append(cie_x[m] * d65_flux_start_from360[m])
    Y.append(cie_y[m] * d65_flux_start_from360[m])
    Z.append(cie_z[m] * d65_flux_start_from360[m])
    x.append(4 * X[m] / (X[m] + 15 * Y[m] + 3 * Z[m]))
    y.append(9 * Y[m] / (X[m] + 15 * Y[m] + 3 * Z[m]))

sum_X = sum(X)
sum_Y = sum(Y)
sum_Z = sum(Z)
sum_all = sum_X + sum_Y + sum_Z

norm_X = sum_X / sum_Y
norm_Y = sum_Y / sum_Y
norm_Z = sum_Z / sum_Y
norm_sum = norm_X + norm_Y + norm_Z

X_coord = 4 * norm_X / (norm_X + 15 * norm_Y + 3 * norm_Z)
Y_coord = 9 * norm_Y / (norm_X + 15 * norm_Y + 3 * norm_Z)

red = [2.473562011839831, 1.0, 0.00020110704560175643]
green = [0.4862204717395029, 1.0, 0.020843550427069965]
blue = [5.6282116190086615, 1.0, 30.56178762666784]

X_red = 4 * red[0] / (red[0] + 15 * red[1] + 3 * red[2])
X_green = 4 * green[0] / (green[0] + 15 * green[1] + 3 * green[2])
X_blue = 4 * blue[0] / (blue[0] + 15 * blue[1] + 3 * blue[2])
Y_red = 9 * red[1] / (red[0] + 15 * red[1] + 3 * red[2])
Y_green = 9 * green[1] / (green[0] + 15 * green[1] + 3 * green[2])
Y_blue = 9 * blue[1] / (blue[0] + 15 * blue[1] + 3 * blue[2])

plt.figure(figsize=(5, 5), dpi = 300)
plt.plot(x, y, 'k-', alpha=0.5)
plt.plot(X_coord, Y_coord, 'ko-')
plt.plot([X_red, X_green],[Y_red, Y_green],'ko-')
plt.plot([X_green, X_blue], [Y_green, Y_blue],'ko-')
plt.plot([X_blue, X_red], [Y_blue, Y_red],'ko-')

white_point_loc = 'D65 White Point (' + '{:.2f}'.format(X_coord) + ', ' + '{:.2f}'.format(Y_coord) + ')'

plt.annotate(white_point_loc, (X_coord, Y_coord), (X_coord - 0.02, Y_coord + 0.025))
plt.title('1976 Universal Chromaticity Scale (UCS)')
plt.xlabel('u\'')
plt.ylabel('v\'')
plt.grid()