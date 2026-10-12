from __future__ import division
from vpython import *
from math import *
import numpy as np
import os
import platform

# ---------------------------------------------------------
# Ekranı temizleme fonksiyonu (Windows / Linux / Mac uyumlu)
# ---------------------------------------------------------
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# ---------------------------------------------------------
# Başlık (banner) yazdırma fonksiyonu
# ---------------------------------------------------------
def print_banner():
    print("========================================")
    print("             VECTOR PRODUCT             ")
    print("========================================\n")

def main():
    # Önce ekranı temizle ve başlığı yaz
    clear_screen()
    print_banner()

    # ----------------------------------------------------------------------
    # -----Kullanıcıdan Vektör Girişi Alma----------------------------------
    print("--- Enter the Vector Components ---\n")

    # Vektör A (v1)
    v1x = float(input("Enter  X component of vector A: "))
    v1y = float(input("Enter  Y component of vector A: "))
    v1z = float(input("Enter  z component of vector A: "))

    # Vektör B (v2)
    v2x = float(input("Enter  X component of vector B: "))
    v2y = float(input("Enter  Y component of vector B: "))
    v2z = float(input("Enter  Z component of vector B: "))

    # ----------------------------------------------------------------------
    # Canvas ayarları ve Başlık
    scene = canvas(width=600, height=600, background=color.white, title='VECTOR PRODUCT')

    # ----------------------------------------------------------------------
    # -----Vektör Tanımı ve Çapraz Çarpım Hesaplaması-------------------------
    a = vector(v1x, v1y, v1z)
    b = vector(v2x, v2y, v2z)
    crossp = cross(a, b)

    # Çapraz çarpımın normuna göre kontrol
    if mag(crossp) < 1e-6:
        norm = vector(0, 0, 0)
    else:
        norm2 = 0.01 * crossp / mag(crossp)
        norm = vector(norm2.x, norm2.y, norm2.z)

    # ---------Vektörler Arası Düzlemi Oluşturma (QUAD)----------------------
    d_color = color.cyan

    v0_vert = vertex(pos=vector(0, 0, 0), color=d_color)
    v1_vert = vertex(pos=a,             color=d_color)
    v2_vert = vertex(pos=a + b,         color=d_color)
    v3_vert = vertex(pos=b,             color=d_color)

    triangle = quad(v0=v0_vert, v1=v1_vert, v2=v2_vert, v3=v3_vert, opacity=0.7)

    # ----------------------------------------------------------------------
    # -----------Eksenler ve Etiketler----------------------------------------
    arrow(pos=vector(-10, 0, 0), axis=vector(20, 0, 0), shaftwidth=0.1, color=color.black)  # x axis
    arrow(pos=vector(0, -10, 0), axis=vector(0, 20, 0), shaftwidth=0.1, color=color.black)  # y axis
    arrow(pos=vector(0, 0, -10), axis=vector(0, 0, 20), shaftwidth=0.1, color=color.black)  # z axis

    label(pos=vector(10, 0, 0), text='x', height=16, color=color.white,
          background=color.black, box=True, border=4, font='monospace')
    label(pos=vector(0, 10, 0), text='y', height=16, color=color.white,
          background=color.black, box=True, border=4, font='monospace')
    label(pos=vector(0, 0, 10), text='z', height=16, color=color.white,
          background=color.black, box=True, border=4, font='monospace')

    # ------------Vektörlerin Gösterimi------------------------------------
    vec1 = arrow(pos=vector(0, 0, 0), axis=a,       shaftwidth=0.2, color=color.red)    # Vektör A
    vec2 = arrow(pos=vector(0, 0, 0), axis=b,       shaftwidth=0.2, color=color.green)  # Vektör B
    vc   = arrow(pos=vector(0, 0, 0), axis=crossp,  shaftwidth=0.2, color=color.blue)   # A x B

    # ----------------------------------------------------------------------
    # ------------------Dönme Matrisi Tanımı--------------------------------

    # Açı ve dönme ekseni hesaplanabilir mi?
    if mag(a) < 1e-6 or mag(b) < 1e-6:
        print("\nUYARI: Vektörlerden biri sıfır. Açı ve animasyon hesaplanmayacak.")
        ang = 0
        rotaks = vector(1, 0, 0)  # dummy eksen
    elif mag(crossp) < 1e-6:
        print("\nUYARI: Vektörler paralel veya anti-paralel. Animasyon yapılmayacak.")
        ang = 0
        rotaks = vector(1, 0, 0)  # dummy eksen
    else:
        # Her şey normal, açı ve dönme ekseni hesaplanabilir
        ang = a.diff_angle(b)   # radyan cinsinden açı
        rotaks = crossp / mag(crossp)

    ux = rotaks.x
    uy = rotaks.y
    uz = rotaks.z

    def Rot(x):
        return np.array([
            [ux*ux*(1-cos(x)) + cos(x),      ux*uy*(1-cos(x)) - uz*sin(x), ux*uz*(1-cos(x)) + uy*sin(x)],
            [ux*uy*(1-cos(x)) + uz*sin(x),   uy*uy*(1-cos(x)) + cos(x),    uy*uz*(1-cos(x)) - ux*sin(x)],
            [ux*uz*(1-cos(x)) - uy*sin(x),   uy*uz*(1-cos(x)) + ux*sin(x), uz*uz*(1-cos(x)) + cos(x)]
        ])

    # ----------------------------------------------------------------------
    # ---------------------Simülasyon---------------------------------------
    teta = 0
    w = 2 * pi / 180   # açısal hız (rad/s)
    dt = 0.05          # zaman adımı

    # a vektörünü NumPy array'e çevir
    a_np = np.array([a.x, a.y, a.z])

    # İlk döndürülmüş vektör
    xrot_np = Rot(teta).dot(a_np)
    xrot = vector(xrot_np[0], xrot_np[1], xrot_np[2])

    vecrot = arrow(pos=vector(0, 0, 0), axis=xrot, shaftwidth=0.2, color=color.red)

    # Animasyon başlamadan önce sahnede tıklama bekle
    scene.waitfor('click')

    # Eğer ang = 0 ise döngüye hiç girmeyecek, sadece sahne açık kalacak
    while teta < ang:
        rate(30)
        teta = teta + w * dt
        xrot_np = Rot(teta).dot(a_np)
        vecrot.axis = vector(xrot_np[0], xrot_np[1], xrot_np[2])

    # Programın hemen kapanmaması için:
    input("\nSimülasyon bitti. Pencereyi kapatmak için ENTER'a basın... ")

# ---------------------------------------------------------
# Ana çalıştırma bloğu (hata yakalama ile)
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n*** BİR HATA OLUŞTU ***")
        print(e)
        input("\nHata mesajını gördüyseniz ENTER'a basın (konsol kapanmasın diye)... ")
