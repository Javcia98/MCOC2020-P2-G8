# -*- coding: utf-8 -*-
import numpy as np
from numpy import  float64
g = 9.81 #kg*m/s^2


class Barra(object):

    """Constructor para una barra"""
    def __init__(self, ni, nj, R, t, E, ρ, σy):
        super(Barra, self).__init__()
        self.ni = ni
        self.nj = nj
        self.R = R
        self.t = t
        self.E = E
        self.ρ = ρ
        self.σy = σy

    def obtener_conectividad(self):
        return [self.ni, self.nj]

    def calcular_area(self):
        A = np.pi*(self.R**2) - np.pi*((self.R-self.t)**2)
        return A

    def calcular_largo(self, reticulado):
        """Devuelve el largo de la barra. 
        ret: instancia de objeto tipo reticulado
        """
        xi = reticulado.obtener_coordenada_nodal(self.ni)
        xj = reticulado.obtener_coordenada_nodal(self.nj)
        dij = xi-xj
        return np.sqrt(np.dot(dij,dij))

    def calcular_peso(self, reticulado):
        """Devuelve el largo de la barra. 
        ret: instancia de objeto tipo reticulado
        """
        L = self.calcular_largo(reticulado)
        A = self.calcular_area()
        peso = self.ρ * A * L * g
        
        return peso 


    def obtener_rigidez(self, ret):
        """Devuelve la rigidez ke del elemento. Arreglo numpy de (4x4)
        ret: instancia de objeto tipo reticulado
        """
        L = self.calcular_largo(ret)
        A = self.calcular_area()
        K = self.E*A/L
        
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.nj)
        dij =(xi-xj)
        cos = dij[0]/L
        sen = dij[1]/L
        T0 = np.array([[-cos], [-sen], [cos], [sen]])
        
        ke = (T0 @ T0.T) * K

        return ke

    def obtener_vector_de_cargas(self, ret):
        """Devuelve el vector de cargas nodales fe del elemento. Vector numpy de (4x1)
        ret: instancia de objeto tipo reticulado
        """
        W = self.calcular_peso(ret)
        vec = np.array([0, -1, 0, -1])
        fe = vec.T * W/2
    
        return fe


    def obtener_fuerza(self, ret):
        """Devuelve la fuerza se que debe resistir la barra. Un escalar tipo double. 
        ret: instancia de objeto tipo reticulado
        """
        L = self.calcular_largo(ret)
        A = self.calcular_area()
        K = self.E*A/L
        
        n1 = self.ni
        n2 = self.nj
        
        di = ret.obtener_coordenada_nodal(self.ni)
        dj = ret.obtener_coordenada_nodal(self.nj)
        dij =(di-dj)
        cos = dij[0]/L
        sen = dij[1]/L
        T0 = np.array([[-cos], [-sen], [cos], [sen]])
        
        Kreal = T0.T * K
        
       
        ue =np.array([ret.u[2*n1], ret.u[2*n1 + 1], ret.u[2*n2], ret.u[2*n2 + 1]])
        
        se = Kreal@ue
        np.float64(se)
        return -se
     
    
    
    
    
    
    
    
    
    
    