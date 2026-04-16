# Alcubierre Metric — Complete Linearization Calculation

## Author: Brian Sheppard + Claude
## Date: 2026-04-15
## Purpose: Explicit derivation of the linearized field equations, stress-energy,
##          Poisson structure, and image-method entry point

---

## 1. The Alcubierre Metric

The warp drive metric (Alcubierre 1994):

$$ds^2 = -dt^2 + \bigl(dx - v_s f(r_s)\,dt\bigr)^2 + dy^2 + dz^2$$

where:
- $v_s = dx_s/dt$ is the bubble velocity (the "ship" trajectory is $x_s(t) = v_s t$ for constant velocity)
- $r_s = \sqrt{(x - x_s(t))^2 + y^2 + z^2}$ is the distance from the bubble center
- $f(r_s)$ is a **shape function** satisfying $f(0) = 1$ (at the ship) and $f \to 0$ as $r_s \to \infty$

A standard choice is:

$$f(r_s) = \frac{\tanh\bigl(\sigma(r_s + R)\bigr) - \tanh\bigl(\sigma(r_s - R)\bigr)}{2\tanh(\sigma R)}$$

where $R$ is the bubble radius and $\sigma$ controls wall thickness ($\Delta \sim 1/\sigma$).

Expanding the squared term:

$$ds^2 = -(1 - v_s^2 f^2)\,dt^2 - 2v_s f\,dx\,dt + dx^2 + dy^2 + dz^2$$

---

## 2. ADM Decomposition (Exact)

The Alcubierre metric is already in ADM form:

$$ds^2 = -(\alpha^2 - \beta_i \beta^i)\,dt^2 + 2\beta_i\,dx^i\,dt + \gamma_{ij}\,dx^i\,dx^j$$

Reading off the components:

| Quantity | Value |
|----------|-------|
| Lapse | $\alpha = 1$ |
| Shift vector | $\beta^x = -v_s f(r_s),\quad \beta^y = \beta^z = 0$ |
| 3-metric | $\gamma_{ij} = \delta_{ij}$ (flat Euclidean) |

**This is the crucial structural observation: the spatial slices are exactly flat.** All of the warp drive's content lives in the shift vector — the way spatial slices are threaded together in time. There is no spatial curvature; no tidal deformation of the spatial geometry. The "warping" is purely in how the time direction threads through space.

Verification: $-\alpha^2 + \beta_i\beta^i = -1 + v_s^2 f^2 = -(1 - v_s^2 f^2)$. ✓

Since $\gamma_{ij} = \delta_{ij}$, all spatial covariant derivatives reduce to partial derivatives: $D_i = \partial_i$, and the spatial Ricci tensor vanishes: ${}^{(3)}R_{ij} = 0$.

---

## 3. Extrinsic Curvature

The extrinsic curvature of the spatial slices embedded in the 4-geometry:

$$K_{ij} = \frac{1}{2\alpha}\bigl(-\partial_t \gamma_{ij} + D_i \beta_j + D_j \beta_i\bigr)$$

Since $\partial_t \gamma_{ij} = 0$ and $\alpha = 1$:

$$K_{ij} = \frac{1}{2}\bigl(\partial_i \beta_j + \partial_j \beta_i\bigr)$$

With $\beta_x = \gamma_{xj}\beta^j = -v_s f$ and $\beta_y = \beta_z = 0$:

$$\boxed{K_{xx} = -v_s\,\partial_x f, \qquad K_{xy} = -\frac{v_s}{2}\,\partial_y f, \qquad K_{xz} = -\frac{v_s}{2}\,\partial_z f}$$

$$K_{yy} = K_{zz} = K_{yz} = 0$$

### 3.1 The Trace (Expansion Scalar)

$$K = \delta^{ij}K_{ij} = K_{xx} + K_{yy} + K_{zz} = -v_s\,\partial_x f$$

Equivalently, $K = \nabla \cdot \boldsymbol{\beta} = \partial_x \beta^x = -v_s\,\partial_x f$.

The **volume expansion** of the Eulerian observers is $\theta = -K = v_s\,\partial_x f$. Since $f$ decreases from 1 to 0 (so $f'(r_s) < 0$) and $\partial_x f = f'(r_s)\cdot(x - x_s)/r_s$:

- **In front** of the ship ($x > x_s$): $(x - x_s) > 0$, $f' < 0$ → $\theta < 0$ → **contraction** ✓
- **Behind** the ship ($x < x_s$): $(x - x_s) < 0$, $f' < 0$ → $\theta > 0$ → **expansion** ✓

This is the warp effect: space contracts ahead and expands behind, carrying the ship forward.

### 3.2 $K_{ij}K^{ij}$

$$K_{ij}K^{ij} = K_{xx}^2 + 2K_{xy}^2 + 2K_{xz}^2$$

$$= v_s^2(\partial_x f)^2 + \frac{v_s^2}{2}(\partial_y f)^2 + \frac{v_s^2}{2}(\partial_z f)^2$$

---

## 4. Stress-Energy Tensor (Exact Results from ADM Constraints)

Because $\gamma_{ij} = \delta_{ij}$ and ${}^{(3)}R_{ij} = 0$, the ADM constraint equations give us **exact** (not linearized) components of $T_{\mu\nu}$. This is a special feature of the Alcubierre metric.

### 4.1 Energy Density — Hamiltonian Constraint

$${}^{(3)}R + K^2 - K_{ij}K^{ij} = 16\pi G\,\rho$$

With ${}^{(3)}R = 0$:

$$\rho = \frac{1}{16\pi G}\bigl(K^2 - K_{ij}K^{ij}\bigr)$$

$$K^2 - K_{ij}K^{ij} = v_s^2(\partial_x f)^2 - v_s^2(\partial_x f)^2 - \frac{v_s^2}{2}\bigl[(\partial_y f)^2 + (\partial_z f)^2\bigr]$$

$$= -\frac{v_s^2}{2}\bigl[(\partial_y f)^2 + (\partial_z f)^2\bigr]$$

Therefore:

$$\boxed{\rho = \frac{-v_s^2}{32\pi G}\bigl[(\partial_y f)^2 + (\partial_z f)^2\bigr]}$$

**This is the famous Alcubierre result.** The energy density is everywhere $\leq 0$, and strictly negative off the axis of motion. The weak energy condition (WEC) is violated everywhere the shape function has a transverse gradient — i.e., at the bubble wall.

Using $f = f(r_s)$ with $\partial_y f = f'\,y/r_s$ and $\partial_z f = f'\,z/r_s$:

$$\boxed{\rho = \frac{-v_s^2}{32\pi G}\,(f')^2\,\frac{y^2 + z^2}{r_s^2}}$$

Note the angular dependence: $\rho = 0$ on the axis of motion ($y = z = 0$) and maximal in the equatorial plane ($y^2 + z^2 = r_s^2$, i.e., $x = x_s$). The exotic matter forms a **torus-like distribution** centered on the bubble wall.

### 4.2 Momentum Density — Momentum Constraint

$$D_j\bigl(K^{ij} - \delta^{ij}K\bigr) = 8\pi G\,j^i$$

**$x$-component:**

$$8\pi G\,j^x = \partial_x\underbrace{(K_{xx} - K)}_{= 0} + \partial_y K_{xy} + \partial_z K_{xz}$$

Since $K_{xx} = K = -v_s\,\partial_x f$, the first term vanishes identically.

$$j^x = \frac{1}{8\pi G}\Bigl(-\frac{v_s}{2}\,\partial_y^2 f - \frac{v_s}{2}\,\partial_z^2 f\Bigr) = \frac{-v_s}{16\pi G}\,\nabla_\perp^2 f$$

where $\nabla_\perp^2 \equiv \partial_y^2 + \partial_z^2$ is the **transverse Laplacian**.

$$\boxed{j^x = \frac{-v_s}{16\pi G}\,\nabla_\perp^2 f}$$

**$y$-component:**

$$8\pi G\,j^y = \partial_x K_{xy} + \partial_y(K_{yy} - K) + \partial_z K_{yz}$$

$$= -\frac{v_s}{2}\,\partial_x\partial_y f + v_s\,\partial_y\partial_x f = \frac{v_s}{2}\,\partial_x\partial_y f$$

$$\boxed{j^y = \frac{v_s}{16\pi G}\,\partial_x\partial_y f}$$

**$z$-component** (by symmetry):

$$\boxed{j^z = \frac{v_s}{16\pi G}\,\partial_x\partial_z f}$$

**Key observation:** The momentum density $j^i$ is **linear** in $v_s$ (first-order), while the energy density $\rho$ is **quadratic** in $v_s$ (second-order). In the linearization regime $v_s \ll c$, the momentum density dominates.

### 4.3 Total Energy

Integrating the energy density over all space (switching to spherical coordinates $r_s, \theta, \phi$ centered on the bubble):

$$E = \int \rho\,d^3x = \frac{-v_s^2}{32\pi G}\int_0^\infty\!\int_0^\pi\!\int_0^{2\pi} (f')^2\,\sin^2\!\theta\;\cdot r_s^2\sin\theta\;d\phi\,d\theta\,dr_s$$

$$= \frac{-v_s^2}{32\pi G}\cdot 2\pi \cdot \frac{4}{3}\cdot\int_0^\infty (f')^2\,r_s^2\,dr_s$$

$$\boxed{E = \frac{-v_s^2}{12\,G}\int_0^\infty (f')^2\,r_s^2\,dr_s}$$

For a top-hat bubble (radius $R$, wall thickness $\Delta \sim 1/\sigma$): $f' \sim -\sigma$ in the wall, so $(f')^2 \sim \sigma^2$ over a radial interval $\sim 1/\sigma$, at radius $\sim R$:

$$E \sim \frac{-v_s^2}{12\,G}\,\sigma^2 \cdot R^2 \cdot \frac{1}{\sigma} = \frac{-v_s^2\,\sigma\,R^2}{12\,G} = \frac{-v_s^2\,R^2}{12\,G\,\Delta}$$

**The thinner the wall, the more negative energy is required** — this is the Pfenning–Ford constraint. For $R \sim 100\,\text{m}$ and $\Delta \sim 1\,\text{m}$:

$$|E| \sim \frac{v_s^2\,(100)^2}{12\,G\cdot 1} \sim \frac{v_s^2\cdot 10^4}{12\cdot 6.67\times 10^{-11}} \sim v_s^2 \times 10^{13}\;\text{kg}$$

Even at $v_s = 0.01c \approx 3 \times 10^6\;\text{m/s}$, this gives $|E| \sim 10^{26}\;\text{kg}\cdot c^2$ — planetary-mass scale. The energy requirement is severe but scales as $v_s^2$ and $R^2/\Delta$.

---

## 5. The Linearization Regime

### 5.1 Metric Perturbation

Writing $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$:

$$h_{tt} = v_s^2 f^2, \qquad h_{tx} = h_{xt} = -v_s f, \qquad \text{all others} = 0$$

Linearization requires $|h_{\mu\nu}| \ll 1$:
- $|h_{tx}| = v_s |f| \leq v_s \ll 1$ → requires **$v_s \ll c$** (subluminal)
- $|h_{tt}| = v_s^2 f^2 \leq v_s^2 \ll v_s \ll 1$ → automatically satisfied

So the linearization is valid for subluminal bubble velocities.

### 5.2 Order Counting

| Quantity | Order in $v_s/c$ | Physical role |
|----------|-------------------|---------------|
| $h_{tx} = -v_s f$ | $O(v_s)$ | Gravitomagnetic potential |
| $h_{tt} = v_s^2 f^2$ | $O(v_s^2)$ | Post-Newtonian correction |
| $K_{ij}$ | $O(v_s)$ | Extrinsic curvature |
| $j^i$ (momentum density) | $O(v_s)$ | First-order source |
| $\rho$ (energy density) | $O(v_s^2)$ | Second-order source |
| $\theta$ (expansion) | $O(v_s)$ | The warp effect itself |

**The warp effect ($\theta$) and the momentum density ($j^i$) are both first-order in $v_s$.** The exotic energy density is second-order. This means:

> At leading order in the subluminal regime, the Alcubierre drive is a **gravitomagnetic** phenomenon — a frame-dragging effect, not a Newtonian-potential effect. The "exotic matter" signature appears only at the next order.

### 5.3 Gauge Analysis

The trace-reversed perturbation $\bar{h}_{\mu\nu} = h_{\mu\nu} - \frac{1}{2}\eta_{\mu\nu}h$ where $h = \eta^{\mu\nu}h_{\mu\nu}$:

$$h = \eta^{tt}h_{tt} = (-1)(v_s^2 f^2) = -v_s^2 f^2$$

$$\bar{h}_{tt} = v_s^2 f^2 - \frac{1}{2}(-1)(-v_s^2 f^2) = \frac{1}{2}v_s^2 f^2$$

$$\bar{h}_{tx} = -v_s f$$

$$\bar{h}_{xx} = \bar{h}_{yy} = \bar{h}_{zz} = \frac{1}{2}v_s^2 f^2$$

The harmonic (de Donder / Lorenz) gauge condition is $\partial_\mu \bar{h}^{\mu\nu} = 0$. Raising indices with $\eta^{\mu\nu}$:

$$\bar{h}^{tt} = \frac{1}{2}v_s^2 f^2, \quad \bar{h}^{tx} = v_s f, \quad \bar{h}^{xx} = \bar{h}^{yy} = \bar{h}^{zz} = \frac{1}{2}v_s^2 f^2$$

Check the $\nu = t$ condition:

$$\partial_\mu \bar{h}^{\mu t} = \partial_t\bigl(\tfrac{1}{2}v_s^2 f^2\bigr) + \partial_x(v_s f)$$

Using $\partial_t f = -v_s\,\partial_x f$ (since $f$ depends on $t$ only through $x - v_s t$):

$$= v_s^2 f(-v_s\,\partial_x f) + v_s\,\partial_x f = v_s\,\partial_x f\bigl(1 - v_s^2 f\bigr)$$

**This is not zero.** The Alcubierre metric in its natural coordinates is **not in harmonic gauge**.

At leading order ($O(v_s)$), the gauge violation is $v_s\,\partial_x f$, which is first-order and non-negligible. A gauge transformation would be required to put the metric in harmonic form. However, there is a better approach.

### 5.4 Why ADM Is the Natural Framework

The gauge issue is an artifact of trying to force the problem into the harmonic-gauge wave equation $\Box\bar{h}_{\mu\nu} = -16\pi G\,T_{\mu\nu}$. The ADM approach avoids this entirely:

1. The constraint equations (Sections 4.1–4.2) are **exact** for this metric, not linearized
2. They directly yield the physically meaningful quantities ($\rho$, $j^i$)
3. The flat spatial geometry means the constraint equations involve only flat-space differential operators
4. The Poisson equation structure emerges naturally from the shift vector, without gauge transformation

**Conclusion: For the image method, work in ADM form, not in harmonic gauge.**

---

## 6. The Poisson Equation Structure

This is where the method of images becomes applicable. We need to identify equations of the form $\nabla^2 \phi = -4\pi\sigma$ that govern the warp drive fields.

### 6.1 Shift Vector as Gravitomagnetic Potential

The shift vector satisfies:

$$\nabla^2 \beta^x = -v_s\,\nabla^2 f$$

This is a Poisson equation with source $\sigma = \frac{v_s}{4\pi}\nabla^2 f$. The source is **localized at the bubble wall** — wherever $f$ has nonzero second derivatives.

Decomposing the Laplacian into longitudinal and transverse parts:

$$\nabla^2 f = \partial_x^2 f + \nabla_\perp^2 f$$

From Section 4.2, we know $\nabla_\perp^2 f = -\frac{16\pi G}{v_s}j^x$, so:

$$\nabla^2 \beta^x = -v_s\,\partial_x^2 f + 16\pi G\,j^x$$

The transverse Laplacian connects directly to the momentum density — the physical source.

### 6.2 Spherical Shape Function

For the spherically symmetric $f(r_s)$:

$$\nabla^2 f = f'' + \frac{2}{r_s}\,f' = \frac{1}{r_s^2}\frac{d}{dr_s}\bigl(r_s^2\,f'\bigr)$$

This source profile has the following properties:
- **Interior** ($r_s \ll R$): $f \approx 1$, $f' \approx 0$ → $\nabla^2 f \approx 0$
- **Exterior** ($r_s \gg R$): $f \approx 0$, $f' \approx 0$ → $\nabla^2 f \approx 0$
- **Wall** ($r_s \approx R$): $f$ transitions rapidly → $\nabla^2 f$ is large and localized

The source is a **spherical shell** centered on the bubble. This is exactly the geometry amenable to the method of images.

### 6.3 Thin-Wall Limit

In the thin-wall limit ($\sigma \to \infty$, $\Delta \to 0$), the shape function approaches a step function:

$$f(r_s) \to \Theta(R - r_s)$$

The Laplacian becomes distributional:

$$f' \to -\delta(r_s - R)$$

$$\nabla^2 f \to -\delta'(r_s - R) - \frac{2}{R}\,\delta(r_s - R)$$

This is a **surface distribution** with both monopole ($\delta$) and dipole ($\delta'$) layers at $r_s = R$. In the language of potential theory, the bubble wall becomes a **double layer** — exactly the structure that the method of images represents with image charges and image dipoles placed behind a conducting surface.

### 6.4 Expansion Scalar and Poisson Equation

The expansion scalar $\theta = v_s\,\partial_x f$ also satisfies a Poisson-like relation. Taking the divergence:

$$\nabla^2\theta = v_s\,\partial_x(\nabla^2 f)$$

This is not itself a Poisson equation (the right side involves $\partial_x$ of a source, not the source itself), but it shows that $\theta$ inherits its structure from $\nabla^2 f$. The expansion field is the $x$-derivative of the potential generated by the wall source — a **dipole field** pattern.

### 6.5 The Two Poisson Problems

Summarizing, the image method has **two natural entry points**, at different orders in $v_s$:

**First order ($O(v_s)$) — The Gravitomagnetic Problem:**

$$\nabla^2 \beta^x = -v_s\,\nabla^2 f \equiv -4\pi\sigma_\beta$$

Source: $\sigma_\beta = \frac{v_s}{4\pi}\nabla^2 f$, localized at the bubble wall. This governs the shift vector, the expansion scalar, and the momentum density.

**Second order ($O(v_s^2)$) — The Energy Problem:**

The energy density $\rho$ is quadratic in $\partial f$, not linear. It does NOT directly satisfy a Poisson equation. However, it can be written as:

$$\rho = \frac{-v_s^2}{32\pi G}\,|\nabla_\perp f|^2 = \frac{-1}{32\pi G}\,\bigl[(\partial_y\beta^x)^2 + (\partial_z\beta^x)^2\bigr]$$

This is a **nonlinear functional** of the shift-vector solution. The image method would proceed by:
1. Solving the linear Poisson equation for $\beta^x$ (with images)
2. Computing $\rho$ from the solution

The linearity needed for the image method lives at first order. The exotic energy density is a derived second-order consequence.

**Self-consistency note:** In linearized GR, the metric perturbation $h_{\mu\nu}$ lives on a fixed Minkowski background, and the stress-energy $T_{\mu\nu}$ is treated as a given source. But in full GR, $T_{\mu\nu}$ sources the geometry and the geometry determines the motion of matter — the problem is self-consistent. The linearized approach is valid at $O(v_s)$ for the gravitomagnetic problem, but the energy density $\rho$ at $O(v_s^2)$ sits at the boundary of what first-order linearization can self-consistently capture. The ADM constraint equations give $\rho$ *exactly* (because the spatial geometry is flat), so the energy density itself is not approximate — but interpreting it through a linearized boundary-value framework introduces a second-order-on-first-order tension. This is a known feature of linearized GR, not a flaw in this calculation, but it means the mode decomposition in Phase 2 should verify consistency by checking that the second-order energy density derived from first-order modes matches the exact ADM result.

---

## 7. Entry Point for the Method of Images

### 7.1 The Boundary-Value Problem

The method of images solves Poisson equations by replacing boundary conditions with fictitious sources ("images") placed outside the physical domain. For the Alcubierre metric, the structure is:

**Physical domain:** All of space, divided into interior ($r_s < R$) and exterior ($r_s > R$) by the bubble wall.

**The field:** $\beta^x(r_s, \theta, \phi) = -v_s f(r_s)$

**The source:** $\nabla^2 f$, localized at $r_s \approx R$

**Boundary conditions at the wall ($r_s = R$):**
- $f$ continuous (metric must be continuous)
- $\partial_{r_s} f$ continuous (metric must be $C^1$, or else distributional sources at the wall)

**Boundary conditions at infinity:** $f \to 0$, $\beta^x \to 0$ (asymptotic flatness)

**Boundary condition at origin:** $f(0) = 1$ (ship location), $f'(0) = 0$ (regularity)

### 7.2 Interior/Exterior Decomposition

Consider the following decomposition. In the **exterior** ($r_s > R$), the field $\beta^x$ is sourced by what appears to be a point-like object at the origin (the ship) — but modified by the presence of the wall. In classical potential theory, this is solved by placing the real source at the origin plus an image source at some interior point that accounts for the wall.

In the **interior** ($r_s < R$), the field is $\beta^x = -v_s$ (uniform, since $f = 1$). This corresponds to a uniform frame-dragging — the entire interior of the bubble is being carried along.

The image-method reformulation asks: **Can the bubble-wall source ($\nabla^2 f$ at $r_s \approx R$) be decomposed into contributions from:**

1. **A real source** (the ship at the origin, with positive mass-energy)
2. **An "image" of the ship** reflected through the bubble wall
3. **Possibly an "image" of the distant universe** reflected inward

If so, the exotic matter is not an independent source — it is the field pattern created by ordinary sources in the presence of the wall boundary.

### 7.3 Comparison with Electrostatic Image Problem

The closest classical analog is a **conducting sphere** of radius $R$ with a point charge $q$ at the center:

| Electrostatics | Alcubierre (proposed) |
|---------------|----------------------|
| Point charge $q$ at origin | Ship with mass-energy at origin |
| Conducting sphere at $r = R$ | Bubble wall at $r_s = R$ |
| Boundary condition: $\Phi = \text{const}$ on sphere | Boundary condition: matching of $f$, $f'$ at wall |
| Interior field: Coulomb + image charge | Interior field: $\beta^x = -v_s$ (uniform drag) |
| Image charge outside sphere | Image source outside bubble? |

The key difference: in electrostatics, the interior of a conducting sphere is shielded. In the Alcubierre case, the interior has a **uniform** shift (not zero). This is more analogous to a **dielectric sphere** problem, where the interior field is uniform but nonzero — a well-known result in Jackson Ch. 4.

### 7.4 The Casimir Connection

The energy density $\rho$ is negative and localized at the boundary. In QFT, the Casimir effect produces negative energy density between conducting plates because the boundary conditions restrict the allowed vacuum modes, creating a standing-wave structure with lower zero-point energy than free space.

The proposed analog:

| Casimir Effect | Alcubierre Image Method |
|---------------|------------------------|
| EM vacuum modes | Gravitational (metric perturbation) modes |
| Conducting plates at separation $d$ | Bubble wall at radius $R$ |
| Boundary conditions restrict modes | Wall boundary conditions restrict $\beta^x$ solutions |
| Standing waves between plates | Standing wave pattern in $f(r_s)$ |
| Net negative energy density in gap | Net negative $\rho$ at wall |
| Energy $\propto -1/d^4$ (plate separation) | Energy $\propto -v_s^2 R^2/\Delta$ (wall thickness) |

Both effects share the structure: **boundary conditions on a field → restricted mode spectrum → negative energy density localized at the boundary**.

The Casimir energy scales as $1/d^4$ (distance between plates); the Alcubierre exotic energy scales as $1/\Delta$ (wall thickness). Both diverge as the boundary becomes sharp — the Pfenning–Ford constraint is the gravitational analog of the Casimir divergence for infinitesimally close plates.

---

## 8. What This Calculation Establishes

### 8.1 Results

1. **The ADM framework gives exact stress-energy** for the Alcubierre metric without linearization, because the spatial slices are flat. The linearization question is about the *source interpretation*, not the field equations themselves.

2. **The warp drive is gravitomagnetic at leading order.** The shift vector $\beta^x = -v_s f$ plays the role of a vector potential; the expansion/contraction is the associated "field"; the exotic energy density is a second-order energy stored in this field.

3. **The shift vector satisfies a Poisson equation** $\nabla^2\beta^x = -v_s\nabla^2 f$ with source localized at the bubble wall. This is the natural entry point for the method of images.

4. **In the thin-wall limit**, the source becomes a surface distribution (monopole + dipole layers) at $r_s = R$ — precisely the structure that image methods handle.

5. **The energy density is a nonlinear functional** of the Poisson solution. The image method operates at the linear (first-order) level; the exotic energy emerges as a second-order consequence.

6. **The Alcubierre metric is not in harmonic gauge**, so the standard $\Box\bar{h}_{\mu\nu} = -16\pi G\,T_{\mu\nu}$ formulation requires a gauge transformation. The ADM approach avoids this entirely and is the natural framework.

### 8.2 What Remains for Phase 1

**Immediate next calculations:**

| # | Task | Depends on |
|---|------|------------|
| A | Solve $\nabla^2\beta^x = -v_s\nabla^2 f$ via Green's function on a spherical domain. Decompose into interior/exterior problems with matching at $r_s = R$. | This document |
| B | Identify the image configuration: what image sources, placed where, reproduce the correct $\beta^x$ in each region? | Task A |
| C | Compute $\rho$ from the image-method $\beta^x$ and verify it matches Section 4.1. | Tasks A, B |
| D | Compare with Lobo & Visser 2004 (gr-qc/0406083, gr-qc/0412065) — they did linearized Alcubierre analysis. What did they find? Does it overlap? | Literature |
| E | Compare with Fuchs et al. 2024 (2405.02709) — their matter-shell + shift-vector warp drive is the closest known result to what the image method predicts. | Literature |

**The critical question for Task B** was investigated in the 2026-04-15 session (see Section 9 below). The answer is **(b)** — a continuous surface distribution — with significant implications for how the image method should be reframed.

---

## 9. Green's Function Analysis: What the Image Decomposition Actually Gives

*(Added 2026-04-15, following explicit investigation of Tasks A–B)*

### 9.1 The Obstacle: Constant Interior Field

The Alcubierre interior field $\beta^x = -v_s$ (constant) cannot be produced by any finite collection of point image sources. A superposition of $1/|\mathbf{r} - \mathbf{r}_i|$ terms from point sources is constant only in the trivial case of no sources. This rules out the simple "ship + one image" picture.

### 9.2 Electromagnetic Analog: Uniformly Magnetized Sphere

The closest classical analog is a **uniformly magnetized sphere** ($\mathbf{M} = M\hat{x}$):

| Property | Magnetized sphere | Alcubierre bubble |
|----------|------------------|-------------------|
| Interior field | $\mathbf{B} = \frac{2\mu_0}{3}\mathbf{M}$ (uniform) | $\beta^x = -v_s$ (uniform) |
| Exterior field | Pure dipole $\sim 1/r^3$ | Suppressed (faster than power law for sharp walls) |
| Source | Surface current $\mathbf{K} = \mathbf{M}\times\hat{n}$ | Double layer $\delta(r-R) + \delta'(r-R)$ on wall |

The Alcubierre bubble is more extreme: the exterior field is **more suppressed** than a simple dipole, meaning the wall sources specifically cancel the exterior multipoles.

### 9.3 Image Representation

In the thin-wall limit, the source $\nabla^2 f \to -\delta'(r-R) - \frac{2}{R}\delta(r-R)$ decomposes as:

- **Monopole layer** $\delta(r-R)$: Equivalent (by Gauss's theorem) to a point source at the origin for the exterior. Image representation is a single point image — standard Kelvin inversion.
- **Dipole layer** $\delta'(r-R)$: Produces the discontinuity structure. Its image representation requires a **continuous distribution along the radial direction**, analogous to the dielectric sphere problem (Jackson Ch. 4).

**Conclusion:** The image method works, but the "images" are continuous distributions on (or near) the wall surface, not point sources.

### 9.4 The Three-Body Picture

The seed document's three-body proposal (ship + distant source + image) faces a specific problem: the ship's gravitomagnetic contribution $\beta^x_{\text{ship}} \sim -4GMv_s/r$ is singular at the origin and nowhere constant. Converting this to the required uniform interior field demands fine-tuned cancellation from other sources at *every* radius — not a natural feature of point-source superpositions.

### 9.5 Revised Interpretation: Mode/Standing-Wave Picture

The analysis suggests the image method is better understood through the **Casimir/mode picture** rather than the point-image picture:

1. The bubble wall imposes boundary conditions on gravitomagnetic field modes
2. The allowed mode spectrum inside the bubble is restricted (analogous to Casimir plates restricting EM vacuum modes)
3. The lowest-energy configuration consistent with these boundary conditions is the uniform $\beta^x = -v_s$ interior
4. The negative energy density at the wall is the second-order energy stored in this boundary-constrained configuration

This preserves the core insight of the image-method proposal — exotic matter as boundary effect, not independent source — while shifting from a point-source to a mode-based mathematical framework.

### 9.6 What This Means for the Project

| Original claim | Status after analysis |
|----------------|----------------------|
| Exotic matter is a boundary effect | **Supported** — the math confirms all source structure lives at the wall |
| Point-image decomposition (ship + image) | **Not viable** — constant interior field incompatible with point images |
| Three-body reformulation | **Problematic** — requires fine-tuned cancellation |
| Casimir analog | **Strengthened** — mode/boundary picture is the natural framework |
| Poisson equation as entry point | **Confirmed** — the equation is well-posed; the interpretation shifts |

The project should pivot from "method of images" (point sources) to **"boundary-mode decomposition"** (standing waves constrained by the wall). The mathematical tools change from Green's functions with image charges to **spectral decomposition on spherical domains** — spherical Bessel functions, Helmholtz eigenmodes, and their gravitational analogs.

## 10. Limits of This Calculation

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Subluminal only ($v_s \ll c$) | Cannot directly address superluminal warp | Establish the framework subluminally first; superluminal extension is a separate problem |
| Linearization drops $O(v_s^2)$ terms in field equations | Energy density IS $O(v_s^2)$ — it's at the edge of what linearization captures | The ADM results are exact; linearization affects only the image-method interpretation |
| Spherical shape function only | Real warp bubbles may be oblate/prolate | Spherical case first; deformations are perturbative corrections |
| Spin-2 vs spin-1 | Some image-method intuitions from EM will fail for gravity | Must verify each step; Costa & Natário 2014 catalogs the differences |
| Gauge dependence | Image decomposition may be gauge-artifact | Working in ADM avoids gauge issues for the constraints; evolution equations still need care |
| Static/constant-$v_s$ only | Real trajectories accelerate | Constant-velocity case is the natural starting point; acceleration introduces radiation |

---

## Appendix A: Notation and Conventions

- Signature: $(-,+,+,+)$
- Units: $c = 1$ except where explicitly restored
- Greek indices $\mu,\nu,\ldots$: spacetime (0,1,2,3)
- Latin indices $i,j,\ldots$: spatial (1,2,3)
- $G$: Newton's gravitational constant
- $\eta_{\mu\nu} = \text{diag}(-1,1,1,1)$: Minkowski metric
- ADM sign convention: $K_{ij} = \frac{1}{2\alpha}(-\partial_t\gamma_{ij} + D_i\beta_j + D_j\beta_i)$, so positive $K$ means spatial contraction

## Appendix B: Explicit Derivatives for $f(r_s)$

For reference, the partial derivatives of $f(r_s)$ in Cartesian coordinates:

$$\partial_x f = f'\,\frac{x - x_s}{r_s}, \qquad \partial_y f = f'\,\frac{y}{r_s}, \qquad \partial_z f = f'\,\frac{z}{r_s}$$

$$\partial_i\partial_j f = \frac{f''}{r_s^2}(x^i - x_s^i)(x^j - x_s^j) + \frac{f'}{r_s}\Bigl(\delta_{ij} - \frac{(x^i - x_s^i)(x^j - x_s^j)}{r_s^2}\Bigr)$$

where $x_s^i = (x_s, 0, 0)$.

The Laplacian:

$$\nabla^2 f = f'' + \frac{2}{r_s}\,f' = \frac{1}{r_s^2}\frac{d}{dr_s}\bigl(r_s^2 f'\bigr)$$

The transverse Laplacian:

$$\nabla_\perp^2 f = \nabla^2 f - \partial_x^2 f = \frac{f'}{r_s}\Bigl(2 - \frac{(x-x_s)^2}{r_s^2}\Bigr) + f''\Bigl(1 - \frac{(x-x_s)^2}{r_s^2}\Bigr) - \frac{f'}{r_s}$$

In spherical coordinates about the bubble center ($\cos\chi = (x - x_s)/r_s$):

$$\nabla_\perp^2 f = f''(1 - \cos^2\!\chi) + \frac{f'}{r_s}(1 - \cos^2\!\chi + 1) = f''\sin^2\!\chi + \frac{f'}{r_s}(1 + \sin^2\!\chi)$$

Hmm — the transverse Laplacian is **not** spherically symmetric even though $f$ is. This reflects the fact that the Alcubierre metric breaks spherical symmetry down to axial symmetry (the axis of motion is preferred).

## Appendix C: Energy Condition Summary

For the Alcubierre stress-energy:

| Condition | Statement | Status |
|-----------|-----------|--------|
| Weak (WEC) | $\rho \geq 0$ | **Violated** ($\rho \leq 0$ everywhere) |
| Null (NEC) | $T_{\mu\nu}k^\mu k^\nu \geq 0$ for null $k^\mu$ | **Violated** (follows from WEC violation) |
| Strong (SEC) | $(T_{\mu\nu} - \frac{1}{2}g_{\mu\nu}T)\,u^\mu u^\nu \geq 0$ | **Violated** |
| Dominant (DEC) | $\rho \geq 0$ and $T^{\mu\nu}$ future-causal | **Violated** |

All four classical energy conditions are violated. The image method's claim is that this violation is a **boundary effect** (analogous to Casimir), not an independent exotic source.
