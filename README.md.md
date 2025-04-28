### Description:
---
The goal with the problem is solving the amount of slices it would take to cut a circle from radius $260$ until the radius is $100$ if each cut is made along the tangent line stepped in $2.1$ towards the center.

---
<br/><br/>


**Number of Cutting Layers:**

${260-100 \over 2.1} \approx 76.2 \approx 76$
<br/><br/>


**Removed Area:**

$(260^2 - 100^2) * \pi \approx 181 \, 000$
<br/><br/>


**Static Optimal Angle:**

$2\cdot\arccos\left(\frac{260-2.1}{260}\right) \approx 14.58 \degree$ 
<br/><br/>


**First Layer Optimal Cuts:**

$\frac{360}{14.58} \approx 24.7$
<br/><br/>


**First Layer Actual Cuts:** 

$24.7 \approx 25$
<br/><br/>


**Static Actual Angle:**
${360 \over 25} = 14.4 \degree$
<br/><br/>


**First Layer Cut Length for Static Angle:**

$\sin(14.4) \cdot 260 \approx 65.42$
<br/><br/>


**Last Layer Cut Length for Static Angle:**

$\sin(14.4) \cdot 102.5 \approx 25.79$
<br/><br/>


Using a static angle for each layer then leads to the final layer
<br/><br/>


**Last Layer Optimal Angle:**

$2\cdot\arccos\left(\frac{260-76 \cdot2.1}{260-75 \cdot2.1}\right) = 2\cdot\arccos\left(\frac{100.4}{102.5}\right) \approx 23.24 \degree$
<br/><br/>


**Last Layer Optimal Cuts:**

$\frac{360}{23.24} \approx 15.49$
<br/><br/>


**Last Layer Actual Cuts:**

$15.49 \approx 16$
<br/><br/>


**Last Layer Actual Angle:**

${360 \over 16} = 22.5 \degree$
<br/><br/>


**Last Layer Optimal Angle:**

$2\cdot\arccos\left(\frac{260-76 \cdot2.1}{260-75 \cdot2.1}\right) = 2\cdot\arccos\left(\frac{100.4}{102.5}\right) \approx 23.24 \degree$
<br/><br/>


**Last Layer Optimal Cuts:**

$\frac{360}{23.24} \approx 15.49$
<br/><br/>


**Last Layer Actual Cuts:**

$15.49 \approx 16$
<br/><br/>


**Last Layer Actual Angle:**

${360 \over 16} = 22.5 \degree$
<br/><br/>


**Approximate Cuts:**
Upper Limit:



---

#### Method 1 - Static Slice
- Approximate Area: 180 000
- Cuts: 1900


#### Method 2 - Semi-Static Slice
- Approximate Area: 

**One Angle Change**
- Cuts: 1735

**Two Angle Changes**
- Cuts: 1675


#### Method 3 - Modular Slice
- Approximate Area: 
- Cuts: 3425
