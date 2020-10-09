# Portfolio---Python
Python codes created by Hugo Rodrigues.
- Verificationapp.py
- reportgen.py

  These codes were created for the Verification and Validation of testing results of a Landing Gear Control System. The purpose of the verification and validation of the physical testing results on a Landing Gear Control System designed by our team is to assure the reliability of a CPLD* / FPGA** integrated circuit on a state machine for the Main Landing Gear of an airplane, model CRJ-200. 
  The Printed Circuit Board (PCB) was tested, using LabView, in 68 different cases where each of them spends several hours. The results were generated in several (+60000) .csv file which contains more than 4000 rows considering all possible cases for a perfect functionality and failure mode in a Landing Gear State Machine. 
Each case was simulated on a dedicated software (ModelSim - Intel) for a CPLD / FPGA integrated circuit, which contains all possible results (active mode and failure mode). A total of 68 .csv files were generated from the simulation, as well as a waveform diagram for time analysis. Those .csv results contain digital information of each sensor, solenoid valves, and the elapsed time for each specific state.

How does the Python code works?
1)	Allows the user to choose between verifying one test at a time or several tests of the same case;
2)	Allows the user to indicate the tolerance range of error between the elapsed time, in milliseconds, between the simulation and the physical testing;
3)	Loads all the information of the Testbench simulation (ModelSim) and stores into an array;
4)	Loads all the information of the Physical Testing (LabView) and stores into an array;
5)	Compares row by row of the physical testing results with the testbench simulation results;
6)	Stores the information of the tests that were NOT APPROVED, such as file name, number of mismatched rows, mismatched rows ranges, and elapsed time that exceeded the tolerance;
7)	Creates an HTML code with the percentage of results approved and disapproved represented in a pie graph and all the information mention on (6);
8)	Opens a web browser with the results;

* CPLD - Complex Programmable Logic Device
** FPGA - Field Programmable Gate Array

