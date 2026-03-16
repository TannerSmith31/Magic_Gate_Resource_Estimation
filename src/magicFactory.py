import qiskit
from utils import calcLER, calcProbErr_X_Z

class MagicFactory:
    gate:str            #gate being distilled (T, CCZ, ...)
    inputStateCnt:int   #number of states input into the factor to be distilled
    outputStateCnt:int  #number of magic states output by the factory
    outErrorRate:float   #error rate of the magic states produced by the factory
    distillationTime:float   #number of cycles to run a full distillation
    qubitFootprint:int       #number of qubits required for the factory

    def __init__(self, gate:str, inputStateCnt:int, outputStateCnt:int, outErrorRate:float, distillationTime:float, qubitFootprint:int, d_x:int, d_z:int):
        self.gate = gate
        self.inputStateCnt = inputStateCnt
        self.outputStateCnt = outputStateCnt
        self.outErrorRate = outErrorRate
        self.distillationTime = distillationTime
        self.qubitFootprint = qubitFootprint


    """
        T factory from paper "Magic State Distillation: Not as Costly as You Think by Daniel Litinski
            d_x: x code distance
            d_z: z code distance
            d_m: number of code cycles used in lattice surgery
            p_phys: error rate of the physical qubits
    """
    @classmethod
    def T_factory_15_to_1(cls, d_x:int, d_z:int, d_m:int, p_phys:float):

        qubitFootprint =  2*(d_x + 4*d_z) * 3*d_x + 4*d_m #This equation appears in section 3 of the 'not as costly' paper
        p_fail = None #This is the probability the protocol fails TODO figure this out (look at section 1 of the paper i guess)
        distillationTime = 6 * d_m / (1-p_fail)           #This equation appears in section 3 of the 'not as costly paper
        LER_X, LER_Z = calcProbErr_X_Z(p_phys=p_phys, d_x=d_x, d_z=d_z)
        outErrorRate = 10.3704 * p**3  #TODO: determine p. error calc based on paper assuming no incoherent errors (p is probability that qubit fails so i think we have to consider p_phys and the code distances)

        return cls(
            gate = "T",
            inputStateCnt = 15,
            ouputStateCnt = 1,
            outErrorRate = outErrorRate,
            distillationTime = distillationTime,
            qubitFootprint = qubitFootprint,
        )
    
    @classmethod
    def T_factory_20_to_4(cls, d_x, d_z, d_m, p_phys):
        #TODO calcluate variables
        #qubitFootprint =
        #cycles =
        #outErrorRate = 22 * p**2 #the error rate that the ouput |m>^4 state has an error is 22p^2, but since this will implement 4 T gates, the fail rate of each state is 5.5p^2

        return cls(
            gate = "T",
            inputStateCnt = 20,
            outputStateCnt = 4,

        )
    
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






