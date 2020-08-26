from complex import Complex

znumber = Complex(3, 4)
fig = znumber.plot()
znumber2 = Complex(2.5, 4.5)
fig = znumber2.plot(fig)
fig.show()
