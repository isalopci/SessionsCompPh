for i in `seq -w 1 1 20`; do   # use 40 60 80 100...360 380 400 as the cutoff energy for testing

for j in `seq -w 100 40 400`; do
mkdir "${i}-${j}"; cp *.psf "${i}-${j}"        
cd "${i}-${j}"
echo "Running for ${i} k points with mesh cutoff ${j} Ry..."
cat >ecut.fdf<<EOF


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
$i   0   0      0
0    $i   0     0
0    0   $i      0
%endblock kgrid_Monkhorst_Pack


       # --SELF CONSISTENT FIELD - -

MeshCutoff           $j Ry
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

SpinPolarized        F      #If spin polarized, use T
DM.InitSpinAF        F      #gives the antiferromagnetic order if T, otherwise all spin up if F

EOF

mpirun -np 8 siesta ecut.fdf > ecut.fdf.sout
E=`grep "siesta:         Total =" ecut.fdf.sout | tail -1| awk '{printf "%12.6f \n", $4}'`    # read the total energy of the system
echo $i $j $E >> ../Energy_ecut.dat
cd ../
done
done