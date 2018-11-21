# Problem Formulation: Light Quality 

## Derivation

Let the total luminous flux radiated from a point source, for example, an omnidirectional isotropic radiator, be phi.

$$\phi = I* 2\pi[1-cos(\frac{A}{2})]$$

where I is the luminous intensity and A is the beam angle. If we solve this equation for I at A = 2pi, the luminous intensity can be expressed as the following.

$$I=\frac{\phi}{4\pi}$$

The luminous flux is itself related to the electrical power supplied to the light source through an efficiency factor. The power that is not converted to light is lost as heat, which in a real-life scenario will depend on the type of light source used.

$$P = \frac{\phi} {\eta } $$

At a distance d from the light source the illuminance in Lumens per m^2 (Lux) is:

$$E(d) = \frac{I}{d^2}\ = \frac{\phi }{4\pi d^2} = \frac{\eta P}{4\pi d^2}$$

Where P is electrical Power in Watts, phi is luminous flux in lumens and eta is the efficiency of the light source. 

The following section will now focus on relating the above equation to a three-dimensional Cartesian coordinate system that illustrates a room. The distance of any point (x,y,z) in a 3D room to the isotropic radiator at position (x_1,y_1,z_1) can be written as:

$$d = \sqrt{(x-x_1)^2+(y-y_1)^2+(z-z_1)^2}$$

The intensity at any point within this 3D room is therefore:

$$E(x,y,z) = \frac{\eta P}{4\pi((x-x_0)^2+(y-y_0)^2+(z-z_0)^2)}$$

Since illuminance is an additive entity, having several light sources indicates that the illuminance at a point is merely the summation of the individual components caused by individual light sources. The illuminance (in Lux) at any point in the room with n light sources is therefore the following, assuming their efficiencies are equal.

$$E(x,y,z)= \sum_{i=1}^{n} \frac{\eta P_n}{4\pi((x-x_n)^2+(y-y_n)^2+(z-z_n)^2)}$$

## Objective Function

In a first step, we try to maximise the illuminance in a certain zone in the room where illuminance should be greatest such as a work area. The problem was reduced to the two dimensions in a first step to reduce complexity.

$$minimise\ -\overline{E}[x_1, y_1, x_2, y_2, x_3, y_3] = \frac{\sum{E_{ROI}}}{n_{ROI}}$$

$$where\ E_{ROI}[x,y]= \sum_{i=1}^{3} \frac{\eta P_n}{4\pi((x-x_n)^2+(y-y_n)^2)}$$

The objective is to maximise the mean light intensity in the ROI (region of interest). This entails calculating the light intensity at every point in the ROI and then finding the arithmetic mean. Minimising the negative of the mean is equivalent to maximising the mean and is used to be compliant with the negative null form.

## Parameters

These are fixed values in the optimisation problem.

$$Room\ Size\ $$

$$(x_{min}, y_{min})^T = (0,0)^Tm$$

$$(x_{max}, y_{max})^T = (10,7)^Tm$$

$$Number\ of\ lamps$$

$$Lamp\ power$$

$$Lamp\ Radii$$

$$Lamp\ Efficiency$$

$$ROI\ First\ Point$$

$$ROI\ Second\ Point$$

$$n = 3$$

$$P_{1,3}=50W, P_{2} = 120W$$

$$r_{1,3} = 0.15m, r_2 = 0.3m$$

$$\eta = 0.8$$

$$P_1 = (3,3)^Tm$$

$$P_2 = (9,5)^Tm$$

**Future**

$$Albedo$$

$$a =\ ?$$

## Design Variables

These are the variables whose optimum values will be determined through the optimisation the objective function. In this case, the design variables are the positions of the lamp in the two-dimensional room.

$$\overline{E}[x_1, y_1, x_2, y_2, x_3, y_3] = \frac{\sum{E_{ROI}}}{n_{ROI}}$$

## Constraints

Conditions the design variables need to meet, in order for the design to be considered suitable. This is for instance that the lamp centre needs to be at least one radius away from the room walls, as the lamp cannot be located in the wall. This is reflected in the first two equations.  

$$\mid{\frac{x_{max}}{2}-x_n}\mid- \frac{x_{max}}{2}+r_n ≤ 0$$

$$\mid{\frac{y_{max}}{2}-y_n}\mid- \frac{y_{max}}{2}+r_n ≤ 0$$

The following equation states that the lamps need to be located at least one radius from one another, as they would be overlapping otherwise.

$$1-\frac{\sqrt{(x_n-x_{n-1})^2+(y_n-y_{n-1})^2}}{r_n +r_{n-1}}≤ 0$$

The final constraint states that the illuminance shall only be calculated at a distance more than a radius from the light source. This is important to bound the problem, as at the illuminance becomes infinity at zero distances. Since there are three lamps, this will lead to 3x4 = 12 constraints.

$$r_n-\sqrt{(x-x_n)^2+(y-y_n)^2} ≤ 0$$

## Problem Formulation

The problem can be formalised in the negative null form as follows: 

$$minimise$$

$$where$$

$$-\overline{E}[x_1, y_1, x_2, y_2, x_3, y_3] = -\frac{\sum{E_{ROI}}}{n_{ROI}}$$

$$E_{ROI}[x,y]= \sum_{i=1}^{3} \frac{\eta P_n}{4\pi((x-x_n)^2+(y-y_n)^2)}$$

$$subject\ to:$$

$$g_1:\ \mid 5 -x_1\mid - 4.85 ≤0$$

$$g_2:\ \mid 3.5 -y_1\mid - 3.35 ≤0$$

$$g_2:\ \mid 5 -x_2\mid - 4.7 ≤0$$

$$g_4:\ \mid 3.5 -y_2\mid - 3.2 ≤0$$

$$g_5:\ \mid 5 -x_3\mid - 4.85 ≤0$$

$$g_6:\ \mid 3.5 -y_3\mid - 3.35 ≤0$$

$$g_7: 1-\frac{\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}}{0.45}≤ 0$$

$$g_8: 1-\frac{\sqrt{(x_3-x_2)^2+(y_3-y_2)^2}}{0.45}≤ 0$$

$$g_9: 1-\frac{\sqrt{(x_3-x_1)^2+(y_3-y_1)^2}}{0.3}≤ 0$$

$$g_{10}: 0.15-\sqrt{(x-x_1)^2+(y-y_1)^2} ≤ 0$$

$$g_{11}: 0.3-\sqrt{(x-x_2)^2+(y-y_2)^2} ≤ 0$$

$$g_{12}: 0.15-\sqrt{(x-x_3)^2+(y-y_3)^2} ≤ 0$$

## Further Resources

- Old Stuff

    $$I(r) = \frac{P}{A} = \frac{P }{4\pi r^2} (Watts\ per\ m^2)$$

- Websites

    [https://www.noao.edu/education/QLTkit/ACTIVITY_Documents/Safety/LightLevels_outdoor+indoor.pdf](https://www.noao.edu/education/QLTkit/ACTIVITY_Documents/Safety/LightLevels_outdoor+indoor.pdf)

    [http://hyperphysics.phy-astr.gsu.edu/hbase/vision/Areance.html](http://hyperphysics.phy-astr.gsu.edu/hbase/vision/Areance.html)

    [https://en.wikipedia.org/wiki/Candela](https://en.wikipedia.org/wiki/Candela) (last paragraph is good)

    [http://www.charlstonlights.com/led-light-requirement-calculator](http://www.charlstonlights.com/led-light-requirement-calculator)

    [https://www.suprabeam.com/uk/light](https://www.suprabeam.com/uk/light)

- More Info on Units
    - Lumens relation

        ![](Screenshot2018-10-28at15-7d0282e7-5e10-4649-951e-7d08aaaa1381.26.41.jpg)

    *Minimum intensity for a room to be well light

    - Ideal activity lux(amount of luminance that hits a surface)

        ![](Screenshot2018-10-28at15-dcc64aaa-371e-45d1-ab6a-e4f26be2ab5b.14.59.png)

    - Power in watts and lumens

        ![](Screenshot2018-10-28at15-319487bd-d327-4667-b900-d69cdc831fce.24.11.png)

    Potential issue: At r=0, I becomes infinity. 

    Potential issue: Not all power gets transferred to light energy, depending on the lightbulb (incandescent vs. halogen vs. LED). Ask Nan how to reflect that

- More Info on Power Derivation

    We want to maximise the minimum of the following function to achieve the most balanced light distribution across the room. Merely maximising average light intensity would not guarantee that the light distribution is smooth. The equation below calculates the intensity at every single point. The total power needed to illuminate the room is:

    $$P_{tot} = \sum_{i=1}^{n} {P_n}$$

    In order to achieve a certain illuminance at a distance r from a singular ideal light source, the following electrical power is required.

    $$P(\eta,x,y,z,E) = \frac{4\pi E}{\eta}((x-x_0)^2+(y-y_0)^2+(z-z_0)^2)$$

    If we have multiple light sources, the total power required to achieve a total illuminance of E at a point (x,y,z) is the following. 

    $$P_{tot}(\eta,x,y,z,E) = \sum_{i=1}^{n}\frac{4\pi E_n}{\eta_n}((x-x_n)^2+(y-y_n)^2+(z-z_n)^2)$$

    We can take out the factor of this equation, giving the following expression. We also assume all the light sources have the same efficiency.

    $$P_{tot}(\eta,x,y,z,E_{tot}) = \frac{4\pi E_{tot}}{\eta_{tot}}\sum_{i=1}^{n}((x-x_n)^2+(y-y_n)^2+(z-z_n)^2)$$

    We want to minimise the maximum total power required at any point within the room to achieve a minimum illuminance.w

- Nan Feedback

    You can calculate the value of your minimum.

    That equation becomes the objective function to be maximised

    Maximise f(x)

    s.t. partial f(x) to x is 0 (stationary point)

    another constraint is your hessian is greater than 0

    Use integration between z1 and z2 divided by (z2-z1) to find average

    Energy consumption is bette

    interested in the minimum energy needed to give power

    assume same lights, same properties —> becomes a linear programming problem. if you have more than one type of light

    it doens’t look like two subsytems

    Fix the power of light sources and then find how many lights you need to find illumincance
