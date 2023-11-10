

import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm
from matplotlib.animation import FuncAnimation
def colorFader(c1,c2,c3,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    c3 = np.array(mpl.colors.to_rgb(c3))
    if mix < 0.9:
        return mpl.colors.to_hex((1-mix)*c1 + mix*c2)
    else:
        return mpl.colors.to_hex((1 - mix) * c2 + mix * c3)

c1='#F8BBD0'
c2='#1976D2'
c3 = '#F44336'

phases = 5
d = {}

# elérés


for i in np.arange(phases)+1:
    DREAM_data = h5py.File(
        'C:\\Users\Csalad\Documents\Gabor\Kutatas\\futasok\\2023_10\\0.5MA_1keV\output\output_Phase' + str(i) + '.h5',
        'r')

    d['Eqsys' + str(i)] = DREAM_data.get('eqsys')
    d['Other'+ str(i)]= DREAM_data.get('other')
    d['Fluid'+ str(i)]= d['Other'+str(i)].get('fluid')
    d['Eeff' + str(i)]= d['Fluid'+str(i)].get('Eceff')
    d['Temp'+str(i)]=d['Eqsys' + str(i)].get('T_cold')
    d['Efield'+str(i)]=d['Eqsys' + str(i)].get('E_field')
    d['j'+str(i)]=d['Eqsys' + str(i)].get('j_tot')
    d['j_re'+ str(i)]= d['Eqsys' + str(i)].get('j_re')
    d['I_p'+str(i)]= d['Eqsys' + str(i)].get('I_p')
    d['grid'+str(i)]=DREAM_data.get('grid')
    d['time'+str(i)]=d['grid'+str(i)].get('t')
    d['radius'+str(i)]=d['grid'+str(i)].get('r')



locals().update(d)

##print(Eqsys1.get('T_cold'))

#idő állítás

temp = 0
time_total = []
for i in np.arange(phases )+1:


    if i > 1:
        d['time' + str(i)] = d['time' + str(i)] + temp

    temp = d['time' + str(i)][-1]

    time_total = np.append(time_total, np.reshape(d['time' + str(i)], len(d['time' + str(i)])))

    if i != phases:
        time_total = time_total[:-1]



#array vegi ismetlodest kszurjuk:
#time_total = np.array(list(dict.fromkeys(time)))
time_total= time_total * 1e3
print(time_total)



# hogyan tegyük egybe az arrayeket
# Adjust temperature arrays
# Hőmérséklet:

Temp_total = np.delete(d['Temp'+'1'], -1, axis=0)
for i in np.arange(phases-1)+2:
    # egybe tenni a darabokat
    Temp_total = np.vstack((Temp_total, d['Temp'+str(i)]))
    # ha következőt teszünk egybe akkor ez levágja az azonos részt
    #d['Temp' + str(i)] = np.delete(d['Temp' + str(i)], -1, axis=0)
    if i != phases:
        Temp_total = Temp_total[:-1]


# Adjust electric field arrays
Efield_total = np.delete(d['Efield'+'1'], -1, axis=0)
for i in np.arange(phases-1)+2:
    # egybe tenni a darabokat
    Efield_total = np.vstack((Efield_total, d['Efield'+str(i)]))
    # ha következőt teszünk egybe akkor ez levágja az azonos részt
    #d['Efield' + str(i)] = np.delete(d['Efield' + str(i)], -1, axis=0)

    if i != phases:
        Efield_total = Efield_total[:-1]

# Adjust effektív electric field arrays
Eeff_total = np.delete(d['Eeff'+'1'], -1, axis=0)
for i in np.arange(phases-1)+2:
    # egybe tenni a darabokat
    Eeff_total = np.vstack((Eeff_total, d['Eeff'+str(i)]))
    # ha következőt teszünk egybe akkor ez levágja az azonos részt
    #d['Eeff' + str(i)] = np.delete(d['Eeff' + str(i)], -1, axis=0)

    if i != phases:
        Eeff_total = Eeff_total[:-1]


# Adjust plasma current arrays

I_p_total = np.delete(I_p1, -1)

for i in np.arange(phases-1)+2:
    
    # egybe tenni a darabokat
    I_p_total = np.append(I_p_total, np.reshape(d['I_p' + str(i)],len(d['I_p' + str(i)])))
    # ha következőt teszünk egybe akkor ez levágja az azonos részt
    #d['I_p' + str(i)] = np.delete(d['I_p' + str(i)], -1)

    if i != phases:
        I_p_total = I_p_total[:-1]

I_p_total = I_p_total*1e-6


# Adjust áramsűrűség

j_total = np.delete(d['j'+'1'], -1, axis=0)
for i in np.arange(phases-1)+2:
    # egybe tenni a darabokat
    j_total = np.vstack((j_total, d['j'+str(i)]))
    # ha következőt teszünk egybe akkor ez levágja az azonos részt
    d['j' + str(i)] = np.delete(d['j' + str(i)], -1, axis=0)


# elfutó eletron áramsűrűség
j_re = np.delete(d['j_re'+'1'], -1, axis=0)
for i in np.arange(phases-1)+2:
    # egybe tenni a darabokat
    j_re = np.vstack((j_re, d['j_re'+str(i)]))
    # ha következőt teszünk egybe akkor ez levágja az azonos részt
    d['j_re' + str(i)] = np.delete(d['j_re' + str(i)], -1, axis=0)



#print(np.reshape(d['I_p2'],len(I_p2)))

#ez = np.append(I_p_total, np.reshape(d['I_p2'],len(d['I_p2'])))
#print(len(ez))

times = [1,20, 30,50,75,100,150,400,450,500,550,600,700,1000,1796] # a hőmérséklet eséshez

times = [1,20, 30,50,75,100,150,400,450,500,550,600,700,1000,1796,2100] # a hőmérséklet eséshez

colors = ('#000000', '#00008B', '#000080', '#4B0082', '#800080', '#800000', '#FF0000', '#FF4500', '#FFA500',
          '#FFD700', '#d24dff',"#FF00FF","#00FF00","#00FFFF","#0000FF") #homerseklet eséshez




radius0=radius1
norm_radius=radius0/radius0[-1]

FONTSIZE = 20


radius = (0, 0.2, 0.4, 0.6, 0.8, 1)

#print(len(time_total))
#print(len(I_p_total))
print(len(Eeff_total[:,19]))

ezez= np.array([0,1,2,3])

print(ezez[-1])
#áramerősság plot
plt.figure()
plt.plot(time_total, I_p_total,label='Plazmaáram' ,color='#000000', linewidth=5)
plt.legend(loc="upper right", fontsize=FONTSIZE+10)
plt.ylabel("Plazmaáram [MA]", size=FONTSIZE+10)
plt.yticks(size=FONTSIZE)
plt.xlabel("Idő [ms]", size=FONTSIZE+10)
plt.xticks(size=FONTSIZE)
plt.xlim(time_total[0]*0.8, time_total[-1])
plt.ylim(I_p_total.min()*0.9, I_p_total.max()*1.03)
plt.title("Plazmaáram az idő függvényében", fontsize=FONTSIZE+20)


#plt.axvline(x=time1_adj[999]*1e3, label="Argon belövés leállítása", color="red", linewidth=2, linestyle="--")
##plt.axvline(x=time2_adj[0]*1e3, label="Start of exponential temperature decay", color="orange", linewidth=4, linestyle="--")
#plt.axvline(x=time3_adj[0]*1e3, label="Start of the self consistent temperature phase", color="blue", linewidth=4, linestyle="--")
#plt.axvline(x=time4_adj[0]*1e3, label="Start of the runaway plateau phase", color="green", linewidth=4, linestyle="--")

plt.legend(loc="upper right", fontsize=25)

#hömerseklet plot

plt.figure()
for i in range(0, len(times)):
    plt.plot(norm_radius, Temp_total[times[i], :], label="Idő %5.2f ms" % (time_total[times[i]]), color=colorFader(c1,c2,c3,i/len(times)), linewidth=5)

#plt.legend(loc="upper right", fontsize=30)

plt.yticks(size=FONTSIZE)
plt.xlabel("Normált kissugár", size=FONTSIZE+10)
plt.xticks(size=FONTSIZE)

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=FONTSIZE+10)


plt.autoscale(enable=True, axis='x', tight=True)
plt.title("Hőmérséklet a kissugár függvényében", fontsize=FONTSIZE+20)
plt.ylabel('Hőmérséklet [eV]', size=FONTSIZE+10)
plt.yscale('log')
#plt.tick_params(axis='x', labelsize=FONTSIZE)
#plt.tick_params(axis='y', labelsize=FONTSIZE)


#elfutó elektron áramsűrűség
plt.figure()
for i in range(0, len(times)):
    plt.plot(norm_radius, j_re[times[i], :], label="Idő %5.2f ms" % (time_total[times[i]]), color=colorFader(c1,c2,c3,i/len(times)), linewidth=5)
plt.autoscale(enable=True, axis='x', tight=True)
plt.title("Elfutó elektron áramsűrűség a normált kissugár függvényében", fontsize=FONTSIZE+20)
plt.ylabel('Áramsűrűség j_re [MA/m2]', size=FONTSIZE+10)
plt.xlabel("Normált kissugár", size=FONTSIZE+10)
plt.tick_params(axis='x', labelsize=FONTSIZE)
plt.tick_params(axis='y', labelsize=FONTSIZE)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=FONTSIZE+10)

#totális áramsűrűség
plt.figure()
for i in range(0, len(times)):
    plt.plot(norm_radius, j_total[times[i], :], label="Idő %5.2f ms" % (time_total[times[i]]), color=colorFader(c1,c2,c3,i/len(times)), linewidth=5)
plt.autoscale(enable=True, axis='x', tight=True)
plt.title("Totális áramsűrűség a normált kissugár függvényében", fontsize=FONTSIZE+20)
plt.ylabel('Áramsűrűség j_tot [MA/m2]', size=FONTSIZE+10)
plt.xlabel("Normált kissugár", size=FONTSIZE+10)
plt.tick_params(axis='x', labelsize=FONTSIZE)
plt.tick_params(axis='y', labelsize=FONTSIZE)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=FONTSIZE+10)

#elektromos tér
plt.figure()
for i in range(0, len(times)):
    plt.plot(norm_radius, Efield_total[times[i], :]/Eeff_total[times[i], :], label="Idő %5.2f ms" % (time_total[times[i]]), color=colorFader(c1,c2,c3,i/len(times)), linewidth=5)
plt.autoscale(enable=True, axis='x', tight=True)
plt.title("Normált elektromos térerősség a normált kissugár függvényében", fontsize=FONTSIZE+20)
plt.ylabel('Normál elektromos térerősség', size=FONTSIZE+10)
plt.xlabel("Normált kissugár", size=FONTSIZE+10)
plt.tick_params(axis='x', labelsize=FONTSIZE)
plt.tick_params(axis='y', labelsize=FONTSIZE)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=FONTSIZE+10)

plt.show()




'''

plt.figure()
for i in range(0, len(times)):
    plt.plot(norm_radius, Temp_total[times[i], :], label="Idő %5.2f ms" % (time_total[times[i]]), color=str(colors[i]), linewidth=5)

    #giff keszites:
    plt.yticks(size=FONTSIZE)
    plt.xlabel("Normált kissugár", size=FONTSIZE + 10)
    plt.xticks(size=FONTSIZE)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=FONTSIZE + 10)
    plt.title("Hőmérséklet a kissugár függvényében", fontsize=FONTSIZE + 20)
    plt.ylabel('Hőmérséklet [eV]', size=FONTSIZE + 10)
    #plt.yscale('log')
    #plt.ylim((0, 1010))
    #plt.savefig(f'gifek/{i:004}', dpi =100 , facecolor = 'white')
    if i != 0:
        plt.pause((time_total[times[i+1]]-time_total[times[i]])*2)
    else:
        plt.pause(time_total[times[1]]*2)
    plt.clf()

#plt.legend(loc="upper right", fontsize=30)

plt.yticks(size=FONTSIZE)
plt.xlabel("Normált kissugár", size=FONTSIZE+10)
plt.xticks(size=FONTSIZE)

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=FONTSIZE+10)


plt.autoscale(enable=True, axis='x', tight=True)
plt.title("Hőmérséklet a kissugár függvényében", fontsize=FONTSIZE+20)
plt.ylabel('Hőmérséklet [eV]', size=FONTSIZE+10)
plt.yscale('log')

plt.show()
#plt.tick_params(axis='x', labelsize=FONTSIZE)
#plt.tick_params(axis='y', labelsize=FONTSIZE)

'''


'''
def animate(i):
    plt.plot(norm_radius, Temp_total[times[i], :], label="Idő %5.2f ms" % (time_total[times[i]]), color=str(colors[i]), linewidth=5)

    #giff keszites:
    plt.yticks(size=FONTSIZE)
    plt.xlabel("Normált kissugár", size=FONTSIZE + 10)
    plt.xticks(size=FONTSIZE)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=FONTSIZE + 10)
    plt.title("Hőmérséklet a kissugár függvényében", fontsize=FONTSIZE + 20)
    plt.ylabel('Hőmérséklet [eV]', size=FONTSIZE + 10)
    #plt.yscale('log')
    plt.ylim((0, 1010))
    #plt.savefig(f'gifek/{i:004}', dpi =100 , facecolor = 'white')
    if i != 0:
        plt.pause((time_total[times[i+1]]-time_total[times[i]])*2)
    else:
        plt.pause(time_total[times[1]]*2)
    plt.cla()

#plt.legend(loc="upper right", fontsize=30)

fig= plt.figure()

ani = FuncAnimation(fig=fig, func=animate, interval=100)
ani.save('C:\\Users\Csalad\Documents\Gabor\Kutatas\\futasok\\2023_10\\0.5MA_1keV/tmp/animation.gif', writer='imagemagick')
plt.show()

'''