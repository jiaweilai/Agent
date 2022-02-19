import os
from re import U, X

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate

# get settings and functions from utilities module
from utilities import utils

# define colors
colors = ['tab:blue', 'tab:red', 'tab:orange', 'tab:purple', 'tab:green']

def get_process_file_dir(filename,sepnote):
    # Main input data dir
    main_folder = utils.INPUT_DIR
    file = os.path.join(main_folder,filename)
    data = pd.read_csv(file, sep=sepnote, header=None, engine='python')
    return data

def get_mpi_dump(dumpid,lxsize,nxsize,xproc,nspec):

    main_folder = utils.INPUT_DIR
    deltax = lxsize/(nxsize-1)

    lx = []
    drun = []
    urun = []
    vrun = []
    wrun = []
    erun = []
    rrte = []
    trun = []
    prun = []
    yrun = np.zeros((nxsize,nspec))
    rrte = np.zeros((nxsize,nspec))
    for iproc in range(0,xproc):
        filename = 'OptDump'+str(dumpid).zfill(3)+'Proc'+str(iproc).zfill(4)+'.dat'
        file = os.path.join(main_folder,filename)
        

        f = open(file, 'r')
        data = []
        for line in f:
            line = line.strip()
            columns = line.split()
            data.append(columns)
        f.close()

        for nx in range(0,int(nxsize/xproc)):
            lx.append(float(nx+iproc*int(nxsize/xproc))*deltax)
            drun.append(data[nx][0])
            urun.append(data[nx][1])
            vrun.append(data[nx][2])
            wrun.append(data[nx][3])
            erun.append(data[nx][4])
            trun.append(data[nx][5+nspec+0])
            prun.append(data[nx][5+nspec+1])
            for ispec in range(0,nspec):
                yrun[nx+iproc*int(nxsize/xproc),ispec] = data[nx][ispec+5]
                rrte[nx+iproc*int(nxsize/xproc),ispec] = data[nx][5+nspec+2+ispec]

    lout = pd.to_numeric(pd.Series(lx))
    dout = pd.to_numeric(pd.Series(drun))
    uout = pd.to_numeric(pd.Series(urun))
    vout = pd.to_numeric(pd.Series(vrun))
    wout = pd.to_numeric(pd.Series(wrun))
    eout = pd.to_numeric(pd.Series(erun))
    tout = pd.to_numeric(pd.Series(trun))
    pout = pd.to_numeric(pd.Series(prun))
 
    return lout,dout,uout,vout,wout,eout,tout,pout,yrun,rrte

def get_sl_delta_th_loc(t,dx,rr,x,yrin):

    # Thermal flame thickness
    dtdx = np.diff(t)/dx
    dtdxmax = np.amax(dtdx)
    tmax = np.amax(trun)
    deltath = (tmax-300.0)/dtdxmax

    # Laminar flame speed
    rr_int = np.trapz(rr, x)
    SL = -1.0 * rr_int/yrin
    print('delta_th = {:.5f} m'.format(deltath))
    
    print('S_L = {:.5f} m/s'.format(SL))
    return

if __name__ == '__main__':

    # create figure
    # set global plotting parameters
    plt.rcParams['font.size'] = 18

    dumpno = 20
    lx = 0.01
    nxsize = 1000

    deltax = lx/(nxsize-1)
    lx,drun,urun,vrun,wrun,erun,trun,prun,yrun,rrte = get_mpi_dump(dumpno,lx,nxsize,8,9)

    get_sl_delta_th_loc(trun,deltax,rrte[:,0],lx,yrun[0,0])

    f, ax = plt.subplots(3, 1, figsize=(8, 8))

    ax[0].plot(lx,trun, '-', color=colors[0], lw=1.0)
    ax[1].plot(lx,urun/drun, '-', color=colors[0], lw=1.0)
    ax[2].plot(lx,yrun[:,1]/drun, '-', color=colors[0], lw=1.0)
    ax[0].set_title('Dump no: '+str(dumpno))
    ax[0].set_ylabel('T (K)')
    ax[1].set_ylabel('u (m/s)')
    ax[2].set_ylabel('Y (-)')
    ax[2].set_xlabel('lx [m]')
    plt.tight_layout()

    # Process laminar flame results
    laminar_flame_data = get_process_file_dir('laminar_flame.csv',',')

    timestep = laminar_flame_data[0]
    timevalue = laminar_flame_data[1]
    tmax = laminar_flame_data[2]
    sl = laminar_flame_data[3]
    deltath = laminar_flame_data[4]

    plotx = timestep

    f, ax = plt.subplots(3, 1, sharex=True, figsize=(8, 8))
    ax[0].plot(plotx, sl, '-', color=colors[0], ms=2.0, lw=1.0)
    ax[1].plot(plotx, deltath, '-', color=colors[0], ms=2.0, lw=1.0)
    ax[2].plot(plotx, tmax, '-', color=colors[0], ms=2.0, lw=1.0)

    ax[0].set_ylabel('S_L (m/s)')
    ax[1].set_ylabel('delta_th (mm)')
    ax[2].set_ylabel('Tmax (K)')
    ax[2].set_xlabel('time [s]')

    plt.tight_layout()
    #plt.savefig(r"FileName.svg", format="svg")
    plt.show()

