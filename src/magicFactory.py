from __future__ import annotations  #This allows me to type-hint something as a MagicFactory in a param to a function in the class definition.
import math
from src.utils import calcLER, calcProbErr_X_Z, QuantumGate

class MagicFactory:
    gate:str            #gate being distilled (T, CCZ, ...)
    inputStateCnt:int   #number of states input into the factor to be distilled
    outputStateCnt:int  #number of magic states output by the factory
    outErrorRate:float   #error rate of the magic states produced by the factory
    distillationTime:float   #number of cycles to run a full distillation
    qubitFootprint:int       #number of physical qubits required for the factory
    codeDistance:int        #code distance used to implement this factory
    subFactory: MagicFactory|None #Subfactories used within this magic factory (e.g. CCZ factory uses multiple T factories to create magic state)

    def __init__(self, gate:QuantumGate, inputStateCnt:int, outputStateCnt:int, outErrorRate:float, distillationTime:float, qubitFootprint:int, codeDistance:int, subFactory:MagicFactory|None = None):
        self.gate = gate
        self.inputStateCnt = inputStateCnt
        self.outputStateCnt = outputStateCnt
        self.outErrorRate = outErrorRate
        self.distillationTime = distillationTime
        self.qubitFootprint = qubitFootprint
        self.codeDistance = codeDistance
        self.subFactory = subFactory


    """
        T factory from paper "Magic State Distillation: Not as Costly as You Think" by Daniel Litinski
            d_x: x code distance
            d_z: z code distance
            d_m: number of code cycles used in lattice surgery
            p_phys: error rate of the physical qubits
        NOTE: this factory takes in |+> qubits and outputs |T> magic states   TODO: double check this is the case
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
            gate = QuantumGate.T,
            inputStateCnt = 15,
            outputStateCnt = 1,
            outErrorRate = outErrorRate,
            distillationTime = distillationTime,
            qubitFootprint = qubitFootprint,
            codeDistance = d_x, #TODO: maybe adjust the class to take in more than just one code distance so we can also account for d_z
        )
    
    """
        15 to 1 T factory introduced in 'Low Overhead Quantum Computing with Lattice Surgery'. It is a little more space costly than the 15 to 1 factory
        from the 'Not as costly as you think' paper but provides better output fidelity (according to the equations).
            d: code distance used to encode logical qubits
            p_in: error rate of the states going into the distillation (this is the physical error rate if we are making a level 1 factory)
        NOTE: This factory takes in noisy |T> magic states and outputs cleaner |T> magic states
    """
    @classmethod
    def T_factory_15_to_1_Old(cls, d, p_in):
        
        qubitFootprint = (4*d) * (8*d)
        numCycles = 6.5*d  #I got this eq from the paper this factory is from under section X. Distillation
        outErrorRate = 35 * p_in**3 #assuming that the input of the factory is p_in TODO: this is probably distillation limited and doesnt relate to surface code size

        return cls(
            gate = QuantumGate.T,
            inputStateCnt = 15,
            outputStateCnt = 1,
            qubitFootprint = qubitFootprint,
            outErrorRate = outErrorRate,
            distillationTime = numCycles,
            codeDistance = d,
        )
    
    """
        CCZ factory based on the paper 'Efficient magic state factories with a catalyzed |CCZ> -> 2|T> transformation'
            T_Factory: The factory/protocol that is generating the T states to be used in the generation of the CCZ state
                NOTE: this must be a T factory. Also, the paper uses T factories that have half the code distance as the CCZ part of the factory
            d_CZZ is the code distance used for the CCZ distillation that distills the |T1> states into a CCZ state
    """
    @classmethod
    def CCZ_factory(cls, T_Factory: MagicFactory, d_CCZ: int):
        
        if T_Factory.gate != QuantumGate.T:  #CCZ factory works by using T gates distilled from T factories
            raise ValueError(f'CCZ_factory param T_Factory must be a T gate factory but was a {T_Factory.gate} gate factory')
        CCZ_NaiveDistCycleCnt = 4 + (T_Factory.codeDistance/d_CCZ)*3 + 1 + 2 #based on paper [4 stabelizer meas + Tdist/CCZdist*3 T injection + 1 X or Y basis meas + 2 detect err]
        CCZ_distillationTime = (4 + (T_Factory.codeDistance/d_CCZ)*3) * d_CCZ #we pipeline the factory by starting the production of the next CCZ state after finishing the T injection of the prior CCZ state so when running for a long time it only takes the time to do the injection and measurements.
        numT1Factories = math.ceil((8*T_Factory.distillationTime)/CCZ_distillationTime) #we need enough T1 factories to produce 8|T> states in the time it takes to make one CCZ state (5.5d_CCZ cycles)
        T1FactoryFootprint = T_Factory.qubitFootprint #The size of a level 1 T gate factory
        CCZFactoryFootprint = 3*6*d_CCZ #The size of just the CCZ distillation part of the CCZ factory
        qubitFootprint = numT1Factories*T1FactoryFootprint + CCZFactoryFootprint #Total space of CCZ distillation (1 CCZdistillation fed by numT1Factories Tgate factories)
        outErrorRate = 28* (T_Factory.outErrorRate)**2  #TODO: this is the out error rate if it is distillation limited (i.e. the code distance of the T and CCZ factories is high enough that it isn't the source of most error. However, it is possible that with low code distances, it does not get this good) Fix this to adjust error rate based on if the code distance is the bottleneck or if the distillation is the bottle neck.
        return cls(
            gate = QuantumGate.CCZ,
            inputStateCnt = 15,
            outputStateCnt = 1,
            outErrorRate = outErrorRate,
            distillationTime = CCZ_distillationTime,
            qubitFootprint = qubitFootprint,
            codeDistance = d_CCZ,
            subFactory = T_Factory,
        )
    
    """
        Catalyzed |CCZ> -> 2|T> factory based on paper 'Efficient magic state factories with a catalyzed |CCZ> -> 2|T> transformation'
        It takes in 15|T>, converts those to |CCZ>, then converts that to 2|T>
    """
    @classmethod
    def catalyzed_CCZ_to_2T_factory(cls, CCZ_factory: MagicFactory, d_T:int):
        distillationTime = 6.5 * d_T   #I got this from the figure in the paper, but it may assume no bottleneck in the L1 T or CCZ factories
        qubitFootprint = CCZ_factory.qubitFootprint + (4*d_T)**2
        outErrorRate = CCZ_factory.outErrorRate #I think the T states produced have the same error rate as the CCZ states of the CCZ factory (TODO: figure out how this relates to code distance of the factory)
        
        return cls(
            gate = QuantumGate.T,
            inputStateCnt = 15,
            outputStateCnt = 2,
            outErrorRate = outErrorRate,
            distillationTime = distillationTime,
            qubitFootprint = qubitFootprint,
            codeDistance = d_T,
            subFactory = CCZ_factory,
        )
    
    """This is the square root T factory based on the paper 'Efficient magic state factories with a catalyzed |CCZ> -> 2|T> transformation'"""
    """This uses 3 CCZ->2T factories which will produce 6 T-gates: 4 to implement logical AND, 1 to implement 2Theta (T) gate, and 1 to slowly build up another sqrt(T) state in case the catalyst gets poisoned"""
    def sqrtT_factory(cls, C2TFactory:MagicFactory, d:int):
        qubitFootprint = 3*d**2 + 3*C2TFactory.qubitFootprint #the 3d^2 term comes from the fact that the circuit itself is 3 logical qubits.
        distillationTime = C2TFactory.distillationTime #the bottleneck will likely be the CCZ factory outputs to be able to run the 3-qbit circuit
        #Somehow account for the time to distill the first catalyst state (depends on if you just use synthelization (many T gates) or magically distill it (look at other paper for this. will need to add it as a factory)
        return cls(
            gate = QuantumGate.sqrtT,
            inputStateCnt = 3 * C2TFactory.inputStateCnt, #this is ignoring the 2 input |+> states that will turn into sqrt T states because we can directly feed in the qubits we want to apply the sqrt T gate to
            outputStateCnt = 2,
            outErrorRate = C2TFactory.outErrorRate, #TODO: figure out if this is actually right. I think it will be a little worse than the CCZ output but it might be the same or something like 2x is since we apply one CCZ that has the error rate and then 1 additional T gate
            distillationTime = distillationTime,
            qubitFootprint = qubitFootprint,
            codeDistance = d,
            subFactory = C2TFactory,
        )
    
    """
        Factory to produce a series of arbitrarily small rotations. Uses the generalized C2T factory from 'Efficient magic state factories with a catalyzed |CCZ>->2|T> transformation'
        Starts with a C2T factory which produces 2T states, one is output and one is fed into the sqrt(T) factory (M_3). This factory produces 2 sqrt(T) gates, one is ouput the next
        is fed into the next factory M_4 and so on until M_k. the M_k factory outputs both its states.
        an M_k factory produces phases of e^ipi(1/2^k). Thus a M_0=Z, M_1=S, M_2=T, M_3=sqrt(T),...
        This factory outputs 1 of each state |M_n> for 2<=n<=k-1 and 2 |M_k> states
        
        Params:
            C2TFactory: the C2T factory used to produce the T states to run the M factories (and possibly also produce the initial catalyst)
            k: the finest grained rotation to produce (adding a phase of e^-ipi(1/2^k)
            d: the code distance used in the M part of the factories
    """
    @classmethod
    def catalyzed_Rz_factory(cls, C2TFactory:MagicFactory, k:int, d:int):
        #TODO: implement factory
        MfactoryFootprint = 3*d**2 #the M factories use 3 qubits each encoded at distance d^2
        numMfactories = k-2  #the first non C2T factory is a sqrt(T) factory (M_3) and then you have one M factory after for each k increase
        numC2TFactories = 1 + 2*numMfactories #each M factory needs 2 C2T factories to apply the logical and gate within them and the first C2T factory produces T states to go into the first M factory
        qubitFootprint = MfactoryFootprint * numMfactories + C2TFactory.qubitFootprint * numC2TFactories
        distillationTime = C2TFactory.distillationTime #I am assuming this will be the bottleneck, but there is also a startup period where we distill the catalysts we have to think about
        
        return cls(
            gate = None, #TODO: figure out how to represent this gate. its an Rz(1/2^k) gate
            inputStateCnt = numC2TFactories*5,
            outputStateCnt = k-1, #TODO: figure out how to represent the output since it outputs different types of states
            outErrorRate = C2TFactory.outErrorRate, #TODO: figure out if this is the out error rate. I think it moreso is going to depend on how you create the initial catalyst. if we do it by stringing to gether T gates we have to determine the fidelity of this catalyst. perhaps pass catalyst fidelity as param and we dont explain how catalyst is formed
            distillationTime = distillationTime,
            qubitFootprint = qubitFootprint,
            codeDistance = d, #TODO: this is just for the M factories so not a good indicator
            subFactory = C2TFactory
        )
    
    
    #TODO: implement factory based on the technique in the "Even more efficient magic state distillation by zero-level distillation"
    #TODO: other options include magic state cultivation: growing T states as cheap as CNOT gates paper (seems to be way better in space but a little worse in fidelity and time)
    






