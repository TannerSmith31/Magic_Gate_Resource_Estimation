import qiskit
from utils import calcLER, calcProbErr_X_Z

class MagicFactory:
    gate:str            #gate being distilled (T, CCZ, ...)
    inputStateCnt:int   #number of states input into the factor to be distilled
    outputStateCnt:int  #number of magic states output by the factory
    outErrorRate:float   #error rate of the magic states produced by the factory
    distillationTime:float   #number of cycles to run a full distillation
    qubitFootprint:int       #number of physical qubits required for the factory

    def __init__(self, gate:str, inputStateCnt:int, outputStateCnt:int, outErrorRate:float, distillationTime:float, qubitFootprint:int):
        self.gate = gate
        self.inputStateCnt = inputStateCnt
        self.outputStateCnt = outputStateCnt
        self.outErrorRate = outErrorRate
        self.distillationTime = distillationTime
        self.qubitFootprint = qubitFootprint


    """
        T factory from paper "Magic State Distillation: Not as Costly as You Think" by Daniel Litinski
            d_x: x code distance
            d_z: z code distance
            d_m: number of code cycles used in lattice surgery
            p_phys: error rate of the physical qubits
    """
    @classmethod
    def T_factory_15_to_1(cls, d_x:int, d_z:int, d_m:int, p_phys:float):

        #TODO: FIGURE OUT HOW THEY CALCULATE outErrorRate and p_fail SO I DONT HAVE TO HARD CODE THE EXAMPLES HERE
        p_fail = 0   #the probability the distilation protocol fails
        outErrorRate = 0    #error rate of the produced magic state causing a faulty rotation
        if (d_x==7 and d_z == 3 and d_m ==3 and p_phys == 10**(-4)):
            p_fail = 0.005524
            outErrorRate = 10**(-8)
        elif (d_x==9 and d_z==3 and d_z ==3 and p_phys == 10**(-4)):
            p_fail = 0.005524
            outErrorRate = 9.3*10**(-10)
        elif (d_x==11 and d_z==5 and d_z == 5 and p_phys == 10**(-4)):
            p_fail = 0
            outErrorRate = 1.9 * 10**(-11)
        else:
            print("WARNING: unknown d_x, d_z, d_m, p_phys combo for 15 to 1 factory")
            print("setting p_fail to 10^-3 and outErrorRate = p_phys^((d_x+1)/4)")
            p_fail = 10**(-3)
            outErrorRate = p_phys**((d_x+1)/4) # This seems to approximate the error rates given in the 'Not as Costly' paper fairly well
        
        qubitFootprint =  2*(d_x + 4*d_z) * 3*d_x + 4*d_m #This equation appears in section 3 of the 'not as costly' paper
        distillationTime = 6 * d_m / (1-p_fail)           #This equation appears in section 3 of the 'not as costly paper

        return cls(
            gate = "T",
            inputStateCnt = 15,
            outputStateCnt = 1,
            outErrorRate = outErrorRate,
            distillationTime = distillationTime,
            qubitFootprint = qubitFootprint,
        )
    
    # @classmethod
    # def T_factory_20_to_4(cls, d_x, d_z, d_m, p_phys):
    #     #TODO calcluate variables
    #     #qubitFootprint =
    #     #cycles =
    #     #outErrorRate = 22 * p**2 #the error rate that the ouput |m>^4 state has an error is 22p^2, but since this will implement 4 T gates, the fail rate of each state is 5.5p^2

    #     return cls(
    #         gate = "T",
    #         inputStateCnt = 20,
    #         outputStateCnt = 4,

    #     )
    
    @classmethod
    def CCZ_factory(cls):
        #TODO: implement factory
        return
    
    @classmethod
    def sqrtT_factory(cls):
        #TODO: implement factory
        return
    
    @classmethod
    def synthillation_factory(cls):
        #TODO: implement factory
        return
    

MagicFactory.T_factory_15_to_1(d_x=7, d_z=3, d_m=3, p_phys=0.0001)







