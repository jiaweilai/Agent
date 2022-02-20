
def printout(phi,yf,yo2,yn2):
    print('==== Equivalence ratio {} ===='.format(phi))
    print('Check total mass fraction is {}'.format(yf + yo2 + yn2))
    print('Stochiometric YH2 = {:.8e}, YO2 = {:.8e}, YN2 = {:.8e}'.format(yf,yo2,yn2))

if __name__ == '__main__':
    molar_mass_h2 = 2
    molar_mass_O2 = 32
    molar_mass_h2o = 18
    molar_mass_N2 = 28

    air = molar_mass_O2 + 3.76 * molar_mass_N2
    fuel = 2 * molar_mass_h2
    print(fuel)
    far_st = fuel/air

    total_mass = air + fuel
    y_h2 = fuel/total_mass
    y_o2 = molar_mass_O2 / total_mass
    y_n2 = 3.76 * molar_mass_N2 / total_mass
    printout(1.0,y_h2,y_o2,y_n2)

    phi = 1.2
    far = phi * far_st
    fuel = air * far
    total_mass = air + fuel
    y_h2 = fuel/total_mass
    y_o2 = molar_mass_O2 / total_mass
    y_n2 = 3.76 * molar_mass_N2 / total_mass
    printout(phi,y_h2,y_o2,y_n2)