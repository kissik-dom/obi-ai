# ENGINEERING_SPEC.md - GHIDRA SRE, Parametric CAD/CAE, OpenBOM & Propulsion Research

## 1. End-to-End Reverse-Engineering & Manufacturing Pipeline

The **Engineering GHIDRA Anti-Gravity Tab** (`Tab 12`, `/api/engineering/*`) unifies binary reverse engineering, parametric 3D mechanical CAD, multilayer high-voltage PCB design, multiphysics CFD/FEA, screw-level Bill of Materials sourcing, and advanced propulsion physics simulation into a single reproducible sandbox pipeline:

1. **Binary & Firmware Analysis**:
   - `GHIDRA 11.2` (NSA Apache 2.0) headless analyzer (`analyzeHeadless` + `Ghidrathon` + `ghidra_bridge`) producing C/C++ decompilation and P-code control-flow graphs.
   - `Binary Ninja Cloud` (LLIL/MLIL/HLIL), `Radare2 + Cutter` (`r2pipe`), and `angr 9.2` symbolic execution for vulnerability and protocol recovery.

2. **Parametric 3D CAD & Generative Geometry**:
   - `FreeCAD 0.22` (PartDesign, Assembly4, Fasteners, FEM, TechDraw) + `OpenCascade 7.7 / CadQuery 2.4` Python BREP generation (`.step`, `.brep`, `.stl`).
   - `OpenSCAD 2024` (`BOSL2` precision threads/gears) and `Blender 4.0` Geometry Nodes.
   - `IfcOpenShell 0.7` OpenBIM integration with Tab 11 (`City / Urban Planning`).

3. **Electronics & High-Voltage Power Design**:
   - `KiCad 8` schematic, high-voltage creepage/clearance DRC, RF microstrip calculator, `KiKit` panelization, and `LTspice XVII` transient simulation.

4. **Multiphysics Simulation (CFD / FEA / EM)**:
   - `OpenFOAM 12` & `SU2` computational fluid dynamics, `CalculiX 2.20` structural/thermal FEA, `Elmer FEM 9` coupled electromagnetics, `Gmsh 4.12` meshing, and `OpenMDAO 3.33` multidisciplinary optimization.
   - Breakthrough Propulsion Physics (`NASA BPP`) research notebooks: Woodward Mach-Effect thruster mass-fluctuation modeling, Biefeld-Brown electrohydrodynamic lifter electrostatic FEM, asymmetric RF resonant cavity Maxwell eigenmode analysis, and Casimir QVF numerical sweeps.

5. **Every-Screw BOM, Tooling & Patent Documentation**:
   - `OpenBOM` + `InvenTree` + `Octopart` sourcing manifest enumerating every fastener (`M3x10`, `M4x16` ISO 4762 socket head cap screws), required hex/Allen key (`2.5mm`, `3.0mm`), calibrated torque specification (`1.2 Nm`, `2.9 Nm`), and `PrusaSlicer 2.8` G-code print settings.
   - `DocAssemble` + `LaTeX` automated patent-style technical specification & assembly manual exported in one finished batch (`s3://kingdom-finished/{sandbox_id}/`).
