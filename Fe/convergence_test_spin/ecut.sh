
        # -- NAME & LABEL --

SystemName      Fe_Convergence_tests
SystemLabel     Fe

        # -- MATERIAL --

NumberOfAtoms    1
NumberOfSpecies  1

%block ChemicalSpeciesLabel
    1    26  Fe
%endblock ChemicalSpeciesLabel

       # -- CELL & ATOMIC POSITIONS

LatticeConstant 1.0 Ang
%block LatticeParameters
2.863036 2.863036 2.863036 90.000000 90.000000 90.000000
%endblock LatticeParameters

AtomicCoordinatesFormat Fractional
%block AtomicCoordinatesAndAtomicSpecies
	0.000000000	  0.000000000	    0.000000000    1
       0.500000000     0.500000000     0.500000000    1
%endblock AtomicCoordinatesAndAtomicSpecies


       # --MONKHORST PACK --

%block kgrid_Monkhorst_Pack
12   0   0      0
0    12   0     0
0    0   12      0
%endblock kgrid_Monkhorst_Pack


       # --SELF CONSISTENT FIELD - -

MeshCutoff           220 Ry
PAO.BasisSize        DZP    # or DZP
PAO.BasisType        split
SolutionMethod       diagon
XC.authors           PBE       
XC.functional        GGA
MaxSCFIterations     200
DM.Tolerance         1.d-6    # 0.01 eV
DM.MixingWeight      0.05   
DM.NumberPulay       5  
Diag.ParallelOverK   T

		# -- SPIN --

SpinPolarized        T      #If spin polarized, use T
DM.InitSpin          0.0
DM.InitSpinAF        F      #gives the antiferromagnetic order if T, otherwise all spin up if F

		# --MOLECULAR DYNAMICS or CONJUGATE GRADIENT METHOD --       
                                                                                            
MD.TypeOfRun         cg     # cg: stuctural optimization
MD.NumCGsteps        0    # maximum number of cg minimization moves
MD.MaxCGDispl        0.05  Ang   
MD.MaxForceTol       0.02 eV/Ang
MD.VariableCell      T      # T: true, cell relaxation; otherwise: F
MD.ConstantVolume    F   

MD.UseSaveXV         T      # read the atomic positions stored in the SystemLabel.XV file
MD.UseSaveCG         F      # read the cg history information stored in the SystemLabel.CG file; used for continuation of the interrupted CG runs
WriteMDHistory       T      # store the atomic coordinates and energy,temperature, etc. in the SystemLabel.MD and SystemLabel.MDE

       # -- SAVING DENSITY MATRIX FOR POST RUN --

ON.UseSAVELWF        F
DM.UseSaveDM         F
UseSaveData          F
LongOutput           T



       # -- PROJECTED DOS & BAND STRUCTURE --

%block ProjectedDensityOfStates      #to write the Total DOS and PDOS on the basis orbitals, between two given energies
-15.00 15.00 0.1 500 eV              # energy window from -15 to 15 eV; with gaussian smearing of 0.1 eV; 500 points in the histogram.
%endblock ProjectedDensityOfStates

%block PDOS.kgrid_Monkhorst_Pack
    64   0   0      0
    0    64   0     0
    0    0   64      0
%endblock block PDOS.kgrid_Monkhorst_Pack

BandLinesScale       ReciprocalLatticeVectors
%block BandLines
1     0.000000  0.000000  0.000000    \Gamma
100   -0.5 0.5 0.5 H
100   0 0.5 0 N
100   0.000000  0.000000  0.000000    \Gamma
100   0.25 0.25 0.25 P
100   -0.5 0.5 0.5 H
100   0.25 0.25 0.25 P
100   0 0.5 0 N
%endblock BandLines



       # --Others--

WriteHirshfeldPop   T
WriteVoronoiPop     T
WriteMullikenPop    1


EOF
