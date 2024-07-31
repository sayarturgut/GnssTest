import customtkinter,threading,serial.tools.list_ports,serial,subprocess,tkintermapview,math,sys,os,serial,socket,queue,random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tkinter import filedialog
from matplotlib.path import Path
from numpy import cos,sin,arccos
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Cursor
from scipy.special import binom
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from shapely.geometry.polygon import LinearRing, Polygon
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from time import sleep
from tkinter import ttk
from pylab import *
import tkinter as tk
import numpy as np
from tkinter import *
global degis,degis1
kes,enlem1,boylam1,enlem,boylam,portver,dongu,degis,x,y,coordx,coordy,linedon,roverx,roverymax,roverymin,arcxdata,arcydata,sirali_konum=0,[],[],[],[],[],0,0,[],[],[],[],0,[],[],[],[],[],[]
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    portver.append(port.device)
    dongu=dongu+1
def comrefresh():
    dongu=0
    portver=[]
    ports = serial.tools.list_ports.comports(include_links=False)
    for port in ports :
        portver.append(port.device)
        dongu=dongu+1
    droportana.configure(values=portver)
    droportana1.configure(values=portver)
class MyToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, parent):
        self.toolitems = (
            ('Home', 'Home', 'home', 'home'),
            ('Back', 'Back', 'back', 'back'),
            ('Forward', 'Forward', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan', 'move', 'pan'),
            ('Zoom', 'Zoom', 'zoom_to_rect', 'zoom'),              
            (None, None, None, None),
            ('Subplots', 'Subplots', 'subplots', 'configure_subplots'),
            ('Save', 'Save', 'filesave', 'save_figure'),   
        )
        super().__init__(canvas, parent)
def resolution():
    text = screen_size.get()
    text = text.split("x")
    app_width = int(text[0])
    app_height= int(text[1])
    Cerceve.geometry(f'{app_width}x{app_height}+{int(screen_width)}+{int(screen_height)}')
    sekme.configure(width=app_width,height=app_height,
                               fg_color="#242424",
                               segmented_button_fg_color="#033b54",
                               segmented_button_selected_color="#033b54",)
def ntripworkers():
    if __name__ == '__main__':
        workerntrip = threading.Thread(target = ntripf,daemon=True)
        workerntrip.start()
def ntripf():
     i=0
     while True:
        from datetime import datetime
        zaman=datetime.now()
        baudrate=dropana.get()
        timeout=1
        serial_portgiden=droportana.get()
        serial_portgelen=droportana1.get()
        serrtk = serial.Serial(serial_portgiden, baudrate, timeout=timeout)
        ntrip_mountpoint = mountpgirtxt.get("1.0", "end-1c")
        ntrip_username = idgirtxt.get("1.0", "end-1c")
        ntrip_password = sifregirtxt.get("1.0", "end-1c")
        sunc=servergirtxt.get("1.0", "end-1c")
        portsunc=int(portgirtxt.get("1.0", "end-1c"))
        ntrip_server = (sunc, portsunc)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ntrip_server)
        ntrip_request = f'GET /{ntrip_mountpoint} HTTP/1.1\r\n'
        ntrip_request += f'User-Agent: NTRIP nTripClient/1.0\r\n'
        ntrip_request += f'Authorization: Basic {ntrip_username}:{ntrip_password}\r\n'
        ntrip_request += f'Connection: close\r\n\r\n'
        client.send(ntrip_request.encode())
        gnss_data = b''
        while True:
            response = client.recv(4096)
            if not response:
                break
            gnss_data += response
            serrtk.write(response)
            gnss_response = serrtk.readline()
        client.close()
        kaynakciktxt.delete("1.0",END)
        kaynakciktxt.insert(END,gnss_data)
        i=i+1
        veri_decoded=gnss_response.decode().strip()
        if(veri_decoded[0:6]=="$GNGGA"):
            veri_decoded=veri_decoded.replace("$GNGGA","$GPGGA")
        print(veri_decoded)
        global boylam1,enlem1
        if(len(veri_decoded)>=74 and veri_decoded[0:1]=="$"):
            RTKbaglan.configure(text="Bağlantı Sağlandı")
            N=veri_decoded.find("N")
            E=veri_decoded.find("E")
            S=veri_decoded.find(",")
            latitude=veri_decoded[16:N-1]
            longitude=veri_decoded[N+2:E-1]
            saat=veri_decoded[S+1:S+10]
            altitude.configure(text="Rakım:"+veri_decoded[E+12:E+17]+" "+veri_decoded[E+18:E+19]+"etre")
            veribilgi.configure(text="Saat:"+saat[0:2]+":"+saat[3:5]+":"+saat[5:])
            uydusayi.configure(text="Kullanılan uydu: "+veri_decoded[E+4:E+6])
            if(int(veri_decoded[E+2:E+3])==0):
                fixing.configure(text="GNSS konumlandırma durumu:"+"Sabitlenen uydu yok'0'",text_color="red")
            if(int(veri_decoded[E+2:E+3])==1):
                fixing.configure(text="GNSS konumlandırma durumu:"+"RTK düzeltmesi yok'1'",text_color="red")
            if(int(veri_decoded[E+2:E+3])==2):
                fixing.configure(text="GNSS konumlandırma durumu:"+"DGPS'2'",text_color="yellow")
            if(int(veri_decoded[E+2:E+3])==4):
                fixing.configure(text="GNSS konumlandırma durumu:"+"Maksimum düzeltme'4'",text_color="green")
            if(int(veri_decoded[E+2:E+3])==5):
                fixing.configure(text="GNSS konumlandırma durumu:"+"Float'5'",color="green")
            latitude=float(latitude)
            longitude=float(longitude)
            latDeg=latitude / 100
            latDeg=int(latDeg)
            latMin=latitude - (latDeg * 100)
            latMin= latMin/60
            lonDeg=longitude/100
            lonDeg=int(lonDeg)
            lonMin=longitude-(lonDeg * 100)
            lonMin=lonMin/60
            longitudeson=lonDeg+lonMin
            latitudeson=latDeg+latMin
            enlem.append(latitudeson)
            boylam.append(longitudeson)
            u=0
            for x in enlem:
                u=u+1
            if u > 1:
                enlem.pop(1)
                boylam.pop(1)
            ilkenlem=enlem[0]*11100000
            ilkboylam=boylam[0]
            enlemcm=(latitudeson*11100000)-ilkenlem
            yboylamcm=math.cos(latitudeson)*11100000
            boylamcm=(yboylamcm*longitudeson)-(yboylamcm*ilkboylam)
            enlem1=enlemcm
            boylam1=boylamcm
            if(kes==1):
                port.close()
            ax1.plot(boylam1,enlem1, color="red",linestyle="dashed",marker="o"), ax1.grid(True)
            ax1.set_xlabel('$x(cm)$'),ax1.set_ylabel('$y(cm)$')
            ax1.set_title('$GPS DATA$')
            line1.draw()
            hesap0=str(zaman)
            zaman1=datetime.now()
            hesap=str(zaman1)
            sonuc=str(int(abs(float(hesap[18:19]+hesap[20:27])-float(hesap0[18:19]+hesap0[20:27]))))
            veriaktarim.configure(text="Veri aktarım süresi: "+
                                    sonuc[0:3]+"."+
                                    sonuc[3:]+
                                    " Milisaniye")
        else:
            fixing.configure(text="GNSS konumlandırma durumu:"+"GNSS ALICISI BAĞLANTISI YOK",text_color="red")
        serrtk.close()
def köşe_ekle_worker():
        workerel = threading.Thread(target = köşe_ekle,daemon=True)
        workerel.start() 
def köşe_ekle():
    global degis,degis1
    örnekalan=int(diklinemesafe.get("1.0","end-1c"))
    if örnekalan==0:
        döndön=0  
        #ab=[39.7567933,39.7560015,39.7548220,39.7544261,39.7551685,39.7567933]
        #ba=[30.4983882,30.4967253,30.4972188,30.4983668,30.4980342,30.4983882]
        ab=[39.7525993,39.7526076,39.7525477,39.7525379,39.7525993]
        ba=[30.6336177,30.6338607,30.6338700,30.6336259,30.6336177]
        sayi=len(ab)
        global degis1,degis
        while(sayi!=0):
            latitudeson=ab[döndön]
            longitudeson=ba[döndön]
            döndön=döndön+1
            sayi=sayi-1
            enlem.append(latitudeson)
            boylam.append(longitudeson)
            ilkenlem=enlem[0]*11100000
            ilkboylam=boylam[0]
            enlemcm=(latitudeson*11100000)-ilkenlem
            yboylamcm=math.cos(latitudeson)*11100000
            boylamcm=(yboylamcm*longitudeson)-(yboylamcm*ilkboylam)
            enlem1=enlemcm
            boylam1=boylamcm
            degis1=str(degis+1)
            makepolyel.configure(text=degis1+". Nokta işaretlendi!")
            x.append(enlem1)
            y.append(boylam1)
            degis=degis+1
            latitudemap=str(latitudeson)
            longitudemap=str(longitudeson)
            polygon_1.add_position(latitudeson,longitudeson)
    else:
        latitudeson=float(makepolyinputenlem.get("1.0", "end-1c"))
        longitudeson=float(makepolyinputboylam.get("1.0", "end-1c"))
        enlem.append(latitudeson)
        boylam.append(longitudeson)
        ilkenlem=enlem[0]*11100000
        ilkboylam=boylam[0]
        enlemcm=(latitudeson*11100000)-ilkenlem
        yboylamcm=math.cos(latitudeson)*11100000
        boylamcm=(yboylamcm*longitudeson)-(yboylamcm*ilkboylam)
        enlem1=enlemcm
        boylam1=boylamcm
        degis1=str(degis+1)
        makepolyel.configure(text=degis1+". Nokta işaretlendi!")
        x.append(enlem1)
        y.append(boylam1)
        degis=degis+1
        latitudemap=str(latitudeson)
        longitudemap=str(longitudeson)
        polygon_1.add_position(latitudeson,longitudeson)
    map_widget.set_address(latitudemap+","+longitudemap)
    map_widget.canvas.itemconfig(polygon_1.canvas_polygon, fill="yellow")
def iki_nokta_cizgi(event):
    global linedon
    if onclickac.get()==1:
        linedon=linedon+1
        yay_çizgi_bilgi_label.configure(text="Çizgi için "+str(linedon)+".Nokta Seçildi")
        coordx.append(event.xdata)
        coordy.append(event.ydata)
        x = event.xdata
        y = event.ydata
        figure1.canvas.draw()
        if linedon>=2:
            yay_çizgi_bilgi_label.configure(text="Çizgi tamamlandı")
            linex=np.array([coordx[0],coordx[1]])
            liney=np.array([coordy[0],coordy[1]])
            sirali_konum.append((coordx[0],coordy[0]))
            sirali_konum.append((coordx[1],coordy[1]))
            #print(sirali_konum)
            ax1.plot(linex,liney,color="red")
            roverx.append(coordx)
            if coordy[0]>=coordy[1]:
                roverymax.append(coordy[0])
                roverymin.append(coordy[1])
                bilgi_frame.insert(END,
                    f'EKLENEN(ÇİZGİ)      ({int(coordx[0])},{int(coordy[1])})                 ({int(coordx[1])},{int(coordy[0])})')
                bilgi_frame.itemconfig(END,{'fg':'white'})
            else:
                roverymax.append(coordy[1])
                roverymin.append(coordy[0])
                bilgi_frame.insert(END,
    f'EKLENEN(ÇİZGİ)      ({int(coordx[0])},{int(coordy[0])})                 ({int(coordx[1])},{int(coordy[1])})')
                bilgi_frame.itemconfig(END,{'fg':'white'})           
            figure1.canvas.draw()
            coordx.clear()
            coordy.clear()
            linedon=0
    if arc_çiz.get() == 1:
        arcxdata.append(event.xdata)
        arcydata.append(event.ydata)
        linedon+=1
        yay_çizgi_bilgi_label.configure(text="Yay için "+str(linedon)+".Nokta Seçildi")
        if linedon>=3:
            bernstein = lambda n, k, t: binom(n,k)* t**k * (1.-t)**(n-k)
            def bezier(points, num):
                N = len(points)
                t = np.linspace(0, 1, num=num)
                curve = np.zeros((num, 2))
                for i in range(N):
                    curve += np.outer(bernstein(N - 1, i, t), points[i])
                return curve

            start_point = (arcxdata[0], arcydata[0])
            end_point = (arcxdata[1], arcydata[1])
            mid_point = (arcxdata[2], arcydata[2])

            nodes1 = np.array([start_point, mid_point, end_point])
            curve1 = bezier(nodes1, num=int(nokta_sayi_input.get("1.0","end-1c")))
            bilgi_frame.insert(END,
    f'EKLENEN(YAY)       ({int(start_point[0])},{int(start_point[1])})                 ({int(end_point[0])},{int(end_point[1])})')
            bilgi_frame.itemconfig(END,{'fg':'white'})
            ax1.plot(curve1[:,0], curve1[:,1], color="red", ls="", marker="o", ms=3)
            sirala=0
            for döndur in curve1:
                sirali_konum.append((curve1[:,0][sirala],curve1[:,1][sirala]))
                sirala+=1
            #print(sirali_konum)
            line1.draw()
            linedon=0
            yay_çizgi_bilgi_label.configure(text="Yay tamamlandı")
            arcxdata.clear()
            arcydata.clear()
def temizle():
    global degis1,degis
    ax1.clear()
    line1.draw()
    bilgi_frame.delete(0,END)
    x.clear()
    y.clear()
    degis=0
def rotate_poligon():
    global x,y
    alfa=rotating_angle.get()
    x_dönmüş=x.copy()
    y_dönmüş=y.copy()
    for rotate in range(0,len(x[1:-1])):
        x_dönmüş[rotate+1]=(x[rotate+1]*np.cos(np.deg2rad(alfa)))-(y[rotate+1]*np.sin(np.deg2rad(alfa)))
        y_dönmüş[rotate+1]=(x[rotate+1]*np.sin(np.deg2rad(alfa)))+(y[rotate+1]*np.cos(np.deg2rad(alfa)))
    x=[]
    y=[]
    x=x_dönmüş.copy()
    y=y_dönmüş.copy()
    ax1.clear()
    ax1.plot(x,y,color="black")
    ax1.grid(True)
    ax1.set_xlabel('$x(cm)$'),ax1.set_ylabel('$y(cm)$')
    ax1.set_title('$GPS DATA$')
    makepolyel.configure(text="Poligon çizildi.")
    line1.draw()
def veri_sil():
    kacinciveri=str(bilgi_frame.curselection())
    kacinciveri=kacinciveri.replace(",","")
    kacinciveri=kacinciveri.replace(")","")
    kacinciveri=kacinciveri.replace("(","")
    a=ax1.lines[int(kacinciveri)+1]
    a.remove()
    line1.draw()
    bilgi_frame.delete(int(kacinciveri))
def set_angle(alfa):
    poligon_döndür.configure(text="Açı Değiştir:"+str(int(alfa)))
def poligon_bitir():
        global roverymin,roverymax,roverx,sirali_konum
        map_widget.set_zoom(16)
        ax1.clear()
        ax1.plot(x,y,color="black")
        ax1.grid(True)
        ax1.set_xlabel('$x(cm)$'),ax1.set_ylabel('$y(cm)$')
        ax1.set_title('$GPS DATA$')
        makepolyel.configure(text="Poligon çizildi.")
        line1.draw()
def çizgi_bitir_worker():
    workerçizgi = threading.Thread(target = çizgi_bitir,daemon=True)
    workerçizgi.start() 
def çizgi_bitir():
    #-------çizgi hesap
    global roverymin,roverymax,roverx,sirali_konum
    myinterval =float(diklineadet.get("1.0", "end-1c"))
    xvals = np.arange(min(x), max(x), myinterval)
    def generate_equation(x, y):
        # y = mx + b
        # b = y - mx
        left = []
        right = []
        M = []
        B = []
        for i in range(len(x)-1):
            m = ((y[i+1] - y[i]) / (x[i+1] - x[i]))
            b = y[i+1] - m*x[i+1]
            M.append(m)
            B.append(b)
            left.append(min(x[i], x[i+1]))
            right.append(max(x[i], x[i+1]))
        return M, B, left, right
    M, B, left, right = generate_equation(np.array(x), np.array(y))
    roverx,roverymax,roverymin,linesay,sirali_konum=[],[],[],0,[]
    for i in range(len(xvals)):
        ylim = []
        for j in range(len(M)):
            if xvals[i] >= left[j] and xvals[i] <= right[j]:
                Y = M[j] * xvals[i] + B[j]
                ylim.append(Y)
        linex=np.array([xvals[i],xvals[i]])
        liney=np.array([min(ylim),max(ylim)])
        ax1.plot(linex,liney,color="red")
        ax1.scatter(linex,liney,color="red")
        linesay=linesay+1
        line1.draw()
        roverx.append(xvals[i])
        roverymin.append(min(ylim))
        roverymax.append(max(ylim))
        sirali_konum.append((roverx[i],roverymin[i]))
        sirali_konum.append((roverx[i],roverymax[i]))
    for cizgidegis in range(0,linesay):
        bilgi_frame.insert(END,
                            f'{cizgidegis+1}.Çizgi                    ({int(roverx[cizgidegis])},{int(roverymin[cizgidegis])})                 ({int(roverx[cizgidegis])},{int(roverymax[cizgidegis])})')
        bilgi_frame.itemconfig(cizgidegis,{'fg':'white'})
    bilgi_frame.itemconfig(linesay-1,{'fg':'white'})
    line1.draw()
    #print(sirali_konum)
def noktakayittxt():
    dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(dosya_yolu, "w") as dosya:
        for veri in sirali_konum:
            dosya.write(str(veri)+"\n")
#----Çerçeve ekran boyut,tema,başlık,font------
Cerceve = customtkinter.CTk()
app_width=1600
app_height=900
screen_width=Cerceve.winfo_screenwidth()
screen_height=Cerceve.winfo_screenheight()
screen_width= (screen_width/2)-(app_width / 2)
screen_height= (screen_height/2)-(app_height / 2)
Cerceve.geometry(f'{app_width}x{app_height}+{int(screen_width)}+{int(screen_height)}')
myfont=customtkinter.CTkFont(family="Font",size=11,slant="italic")
Cerceve.title("GPS Verisi Ölçekleme Sistemi")
customtkinter.set_appearance_mode("dark")
#------sekmeler-----
sekme=customtkinter.CTkTabview(Cerceve,width=1600,height=900,
                               fg_color="#242424",
                               segmented_button_fg_color="#242424",
                               segmented_button_selected_color="#033b54",)
sekme.place(relx=0,rely=0)
ayarlartab=sekme.add("Ayarlar")
veritakiptab=sekme.add("Veri Takip")
sekme.set("Veri Takip")
#---çerçeve kullanım kolaylığı için sağ-sol böl sağ=ax-----------
left_frame = customtkinter.CTkFrame(veritakiptab,fg_color="#242424")
left_frame.place(relx=0.01, rely=0.05, relwidth=0.32, relheight=0.9)
right_frame = customtkinter.CTkCanvas(veritakiptab, bg='#C0C0C0', bd=1.5)
right_frame.place(relx=0.34, rely=0.05, relwidth=0.65, relheight=0.9)
#---Sağ kısımdaki grafik----
plt.style.use('ggplot')
figure1 = plt.Figure(figsize=(5,6), dpi=100)
ax1 = figure1.add_subplot(111)
ax1.grid(True),ax1.set_xlabel('$x(cm)$'),ax1.set_ylabel('$y(cm)$')
right_frame = customtkinter.CTkCanvas(veritakiptab, bg='#C0C0C0', bd=1.5)
right_frame.place(relx=0.34, rely=0.05, relwidth=0.65, relheight=0.9)
line1 = FigureCanvasTkAgg(figure1, right_frame)
line1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH,expand=1)
toolbar = MyToolbar(line1, right_frame)
toolbar.place(rely=0,relx=0,anchor=NW)
#----butonlar cart curt---
axtemizle=customtkinter.CTkButton(veritakiptab,text="Grafiği temizle",fg_color="#363636",hover_color="#033b54",command=temizle)
axtemizle.place(relx=0.918,rely=0)
#-------tarla kayıt--------
poligon_döndür=customtkinter.CTkButton(veritakiptab,text="Açı Değiştir",fg_color="#363636",hover_color="#033b54",command=rotate_poligon)
poligon_döndür.place(relx=0.202,rely=0.03,relwidth=0.07)
noktalari_kaydet=customtkinter.CTkButton(veritakiptab,text="Noktaları Kaydet",fg_color="#363636",hover_color="#033b54",command=noktakayittxt)
noktalari_kaydet.place(relx=0.25,rely=0.1,relwidth=0.07)
#----------veritakip saat, uydu sayısı, rakım, konumlandırma,süre bilgi.
veribilgi=customtkinter.CTkLabel(veritakiptab,text="Saat:",justify = LEFT,font=("",18))
veribilgi.place(rely=0.34,relx=0.01)
uydusayi=customtkinter.CTkLabel(veritakiptab,text="Kullanılan uydu:",font=("",18))
uydusayi.place(rely=0.4,relx=0.01)
altitude=customtkinter.CTkLabel(veritakiptab,text="Rakım:",font=("",18))
altitude.place(rely=0.37,relx=0.01)
fixing=customtkinter.CTkLabel(veritakiptab,text="GNSS konumlandırma durumu:",font=("",18))
fixing.place(rely=0.46,relx=0.01)
veriaktarim=customtkinter.CTkLabel(veritakiptab,text="Veri aktarım süresi:",font=("",18))
veriaktarim.place(rely=0.43,relx=0.01)
yay_çizgi_bilgi_label=customtkinter.CTkLabel(veritakiptab,text="Yay için 3 nokta işaretleyiniz.")
yay_çizgi_bilgi_label.place(rely=0.067,relx=0.205)
nokta_sayi_input=customtkinter.CTkTextbox(veritakiptab)
nokta_sayi_input.place(rely=0.1,relx=0.205,relwidth=0.04,relheight=0.037)
nokta_sayi_input.insert(END,"6")
#-------bilgi frame-----
bilgi_frame=Listbox(veritakiptab,bg="#363636",bd=0,activestyle="dotbox")
bilgi_frame.place(relx=0,rely=0.033,relwidth=0.2)
bilgi_scrollbar=customtkinter.CTkScrollbar(bilgi_frame)
bilgi_scrollbar.pack(side=RIGHT,fill=BOTH)
listbox_title=customtkinter.CTkLabel(veritakiptab,text="Çizgi Sayısı                Başlangıç XY                Bitiş XY")
listbox_title.place(relx=0,rely=0)
bilgi_frame.config(yscrollcommand = bilgi_scrollbar.set)
bilgi_scrollbar.configure(command=bilgi_frame.yview)
bilgi_denemebuton=customtkinter.CTkButton(veritakiptab,fg_color="#363636",text="Sil",command=veri_sil)
bilgi_denemebuton.place(relx=0,rely=0.275)
#--------mouse click------
onclickac=customtkinter.CTkSwitch(veritakiptab,text="Çizgi")
onclickac.place(relx=0.855,rely=0.002)
cursor = Cursor(ax1, horizOn=True, vertOn=True, useblit=True,
                color = 'r', linewidth = 1)
annot = ax1.annotate("", xy=(0,0), xytext=(-40,40),textcoords="offset points",
                    bbox=dict(boxstyle='round4', fc='linen',ec='k',lw=1),
                    arrowprops=dict(arrowstyle='-|>'))
annot.set_visible(True)
figure1.canvas.mpl_connect('button_press_event', iki_nokta_cizgi)
#---------yay çiz---------
arc_çiz=customtkinter.CTkSwitch(veritakiptab,text="Yay")
arc_çiz.place(relx=0.28,rely=0.032,relwidth=0.05)
#------poligon oluştur çizgi doldur----
makepolyinputenlem=customtkinter.CTkTextbox(veritakiptab)
makepolyinputenlem.place(rely=0,relx=0.34,relwidth=0.09,relheight=0.037)
makepolyinputenlem.insert(END,"'Enlem'")
makepolyinputboylam=customtkinter.CTkTextbox(veritakiptab)
makepolyinputboylam.place(rely=0,relx=0.43,relwidth=0.09,relheight=0.037)
makepolyinputboylam.insert(END,"'Boylam'")
makepolyel=customtkinter.CTkButton(veritakiptab,text="Köşe Belirle",fg_color="#363636",hover_color="#033b54",command=köşe_ekle_worker)
makepolyel.place(rely=0.002,relx=0.582)
poligon_bitir_buton=customtkinter.CTkButton(veritakiptab,text="Poligon Çiz",fg_color="#363636",hover_color="#033b54",command=poligon_bitir)
poligon_bitir_buton.place(rely=0.002,relx=0.672)
çizgi_bitir_buton=customtkinter.CTkButton(veritakiptab,text="Çizgi Doldur",fg_color="#363636",hover_color="#033b54",command=çizgi_bitir_worker)
çizgi_bitir_buton.place(rely=0.002,relx=0.762)
diklinemesafe=customtkinter.CTkTextbox(veritakiptab)
diklinemesafe.place(rely=0,relx=0.55,relwidth=0.03,relheight=0.037)
diklinemesafe.insert(END,"10")
diklineadet=customtkinter.CTkTextbox(veritakiptab)
diklineadet.place(rely=0,relx=0.52,relwidth=0.03,relheight=0.037)
diklineadet.insert(END,"100")
#------poligon çevir-----
rotating_angle=customtkinter.CTkSlider(veritakiptab,from_=0,to=360,command=set_angle,orientation=HORIZONTAL)
rotating_angle.place(relx=0.2,rely=0)
rotating_angle.set(0)
#--------Ayarlar sekmesi ntrip client konfigürasyonu--
optionscom = portver.copy()
droport = customtkinter.CTkOptionMenu(master=veritakiptab ,
                                    values=optionscom,
                                    button_color="#363636",
                                    fg_color="#363636",
                                    dropdown_hover_color="#033b54",
                                    )
droport.set("PORTS")
options = [
    "9600",
    "19200",
    "31250",
    "38400",
    "57600",
    "74880",
    "115200"
]
düzenleme=customtkinter.CTkLabel(ayarlartab,text="NTRIP Client Configuration",font=myfont)
düzenleme.place(relx=0,rely=0.08)
servergir=customtkinter.CTkLabel(ayarlartab,text="Sunucu:")
servergir.place(relx=0,rely=0.11)
servergirtxt=customtkinter.CTkTextbox(ayarlartab)
servergirtxt.place(relx=0.05,rely=0.11,relwidth=0.09,relheight=0.037)
servergirtxt.insert(END,"212.156.70.42")
portgir=customtkinter.CTkLabel(ayarlartab,text="Port:")
portgir.place(relx=0,rely=0.15)
portgirtxt=customtkinter.CTkTextbox(ayarlartab)
portgirtxt.place(relx=0.05,rely=0.15,relwidth=0.09,relheight=0.037)
portgirtxt.insert(END,"2101")
mountpgir=customtkinter.CTkLabel(ayarlartab,text="Mountpoint:")
mountpgir.place(relx=0,rely=0.19)
mountpgirtxt=customtkinter.CTkTextbox(ayarlartab)
mountpgirtxt.place(relx=0.05,rely=0.19,relwidth=0.09,relheight=0.037)
mountpgirtxt.insert(END,"RTCM3Net")
kaynakcik=customtkinter.CTkLabel(ayarlartab,text="Kaynak tablosu;")
kaynakcik.place(relx=0.144,rely=0.09)
kaynakciktxt=customtkinter.CTkTextbox(ayarlartab)
kaynakciktxt.place(relx=0.14,rely=0.12,relwidth=0.155,relheight=0.13)
idgir=customtkinter.CTkLabel(ayarlartab,text="Kullanıcı:")
idgir.place(relx=0,rely=0.23)
idgirtxt=customtkinter.CTkTextbox(ayarlartab)
idgirtxt.place(relx=0.05,rely=0.23,relwidth=0.09,relheight=0.037)
idgirtxt.insert(END,"K0726018801")
sifregir=customtkinter.CTkLabel(ayarlartab,text="Şifre:")
sifregir.place(relx=0,rely=0.27)
sifregirtxt=customtkinter.CTkTextbox(ayarlartab)
sifregirtxt.place(relx=0.05,rely=0.27,relwidth=0.09,relheight=0.037)
sifregirtxt.insert(END,"BSG6sS")
gidenportgir=customtkinter.CTkLabel(ayarlartab,text="GNSS COM:")
gidenportgir.place(relx=0,rely=0.31)
droportana = customtkinter.CTkOptionMenu(master=ayarlartab ,
                                    values=optionscom,
                                    button_color="#363636",
                                    fg_color="#363636",
                                    dropdown_hover_color="#033b54",
                                    )
droportana.set("Giden")
droportana.place(rely=0.31,relx=0.05)
droportana1 = customtkinter.CTkOptionMenu(master=ayarlartab ,
                                    values=optionscom,
                                    button_color="#363636",
                                    fg_color="#363636",
                                    dropdown_hover_color="#033b54",
                                    )
droportana1.set("Gelen")
droportana1.place(rely=0.31,relx=0.145)
RTKbaglan=customtkinter.CTkButton(ayarlartab,text="RTK Bağlan",command=ntripworkers)
RTKbaglan.place(relx=0.05,rely=0.35)
RTKbaglan=customtkinter.CTkButton(ayarlartab,text="Bağlantı Yenile",command=comrefresh)
RTKbaglan.place(relx=0.145,rely=0.35)
dropana = customtkinter.CTkOptionMenu(master=ayarlartab ,
                                    values=options,
                                    button_color="#363636",
                                    fg_color="#363636",
                                    dropdown_hover_color="#033b54",)
dropana.set("BaudRate")
dropana.place(rely=0.26,relx=0.145)
#-------Ekran boyut----------
screensize = [
    "640x360",
    "800x600",
    "1280x720",
    "1600x900",
    "1900x1000",
    "2560x1440"
]
screen_size=customtkinter.CTkOptionMenu(master=Cerceve ,
                                    values=screensize,
                                    button_color="#363636",
                                    fg_color="#363636",
                                    dropdown_hover_color="#033b54",)
screen_size.place(rely=0,relx=0.876,relwidth=0.07)
screen_size.set("Ekran Boyutu")
dropbut=customtkinter.CTkButton(Cerceve,text="Değiştir"
                                ,fg_color="#363636",
                                hover_color="#033b54",
                                command=resolution)
dropbut.place(rely=0,relx=0.947,relwidth=0.05)
#-------harita ve ana döngü
map_widget = tkintermapview.TkinterMapView(left_frame)
map_widget.place(rely=0.5,relheight=0.5, relwidth=1)
map_widget.set_tile_server("http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}", max_zoom=22)
map_widget.set_address("Eskisehir Osmangazi Üniversitesi,Eskisehir,Turkey")
polygon_1 = map_widget.set_polygon([(0,0)],outline_color="red",fill_color="Blue")
polygon_1.remove_position(0,0)
Cerceve.iconbitmap("icon1.ico")
Cerceve.mainloop()
