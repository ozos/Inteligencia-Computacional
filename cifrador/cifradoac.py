import getopt,sys
from random import randint


def img_gen(data,data2,height,w,rule,k,tam,ci,m,n):
    from PIL import Image, ImageDraw
    img = Image.new("RGB",(w,height),(255,255,255))
    fname=str(rule)+".png"
    draw = ImageDraw.Draw(img)
    width=w-w/k

    for x in range(0,1):
        for y in range(tam):
            draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="yellow",outline="black")
            draw.text((w/2 -40,5),"Encriptado: ",fill="black")
            
    for x in range(1,k+1):
        for y in range(tam):
            if data[x-1][y]:
                if x==1 :
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="pink",outline="blue")
                elif x <= ci:
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="green",outline="yellow")
                elif x > m:
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="orange",outline="purple")
                
                else:
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="red",outline="black")
                    
            else: draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="white",outline="black")
            
    for x in range(k+1,k+2):
        for y in range(tam):
            draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="yellow",outline="black")

    for x in range(k+2,2*k+2):
        for y in range(tam):
            if data2[x-k-2][y]:
                if x<k+2+n:
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="orange",outline="blue")
               
                elif x == 2*k+1:
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="pink",outline="purple")
                
                else:
                    draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="red",outline="black")
                    
            else: draw.polygon([(y * height/tam,x*width/2/k), ((y+1) * height/tam,x*width/2/k), ((y+1) * height/tam,(x+1)*width/2/k), (y * height/tam, (x+1)*width/2/k)], fill="white",outline="black")
                    

    draw.text((w/2 -40,height/2),"Desencriptado: ",fill="black")
    img.format = "PNG"
    img.save(fname,"PNG")
    import webbrowser
    webbrowser.open(fname)
    return

  
def ca_gen(k,tam,s,ci,m,n,rulesnum,opc,ca):
    ats=[]
    rules=[]
    for j in range (len(rulesnum)):          
          rule = [(rulesnum[j]/pow(2,i)) % 2 for i in range(8)]
          rules.append(rule)
        
    if opc ==0:
        ats.append(s)
        for i in range (ci-1):
            atr= [randint(0,1) for i in range(tam)]
            ats.append(atr)

        for i in range(ci,k):
        
            suma=[0]*tam
       
            for l in range (ci):
                data = ats[-l-1]
            
                if l< len(rules):
                    atr = [rules[l][4*data[(j-1)%tam]+2*data[j]+data[(j+1)%tam]]
                       for j in range(tam)]
                else:
                    atr=data
                suma= [(suma[p] + atr[p]) %2 for p in range(tam)]  
            ats.append(suma)
        
    else:
        for i in range(n):
            ats.append(ca[k-1-i])

        for i in range(ci,k):
        
            suma=[0]*tam
       
            for l in range (ci):
                data = ats[-l-1]
            
                if l< len(rules):
                    atr = [rules[len(rules)-l-1][4*data[(j-1)%tam]+2*data[j]+data[(j+1)%tam]]
                       for j in range(tam)]
                else:
                    atr=data
                suma= [(suma[p] + atr[p]) %2 for p in range(tam)]  
            ats.append(suma)
            
            
  
    
    return ats


def abits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def atexto(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def main():
   
    h = 900
    w = 900

    m=10
    n=5
    ci=5
    k=m+n
    rulesnum =(30,45,105,45)
    #rulesnum =(1,1)
    opc=0 #0 encripta 1 desencripta
    
    #s= [randint(0,1) for i in range(5)]
    #s=[1, 0, 1, 0, 0]
    print ("Escribe el mensaje: ")
    s1=raw_input()
    s= abits(s1)

    tam = len(s)
    ca=[]
    ca = ca_gen(k,tam,s,ci,m,n,rulesnum,opc,ca)
    
    print ("Texto a encriptar: " + s1 + " = " + str (s))
   
    for i in range(n):
        print ("Clave " + str(i) +": " +str (atexto(ca[k-1-i]))+ " = " + str(ca[k-1-i]))
    
    dca= ca_gen(k,tam,s,ci,m,n,rulesnum,1,ca)
    print ("Texto desencriptado: " + str (atexto(dca[k-1])) + " = " + str (dca[k-1]))
    
    img_gen(ca,dca,h,w,rulesnum,k,tam,ci,m,n)
    
    return

main()
