"""
An implementation of random noise functions.
"""
from . import Math


class Noise:
    """
    The general noise class.

    Attributes:
        seed (int): The seed for the random noise.
        type (str): The type of noise to generate. Can be "perlin", "simplex". Defaults to "simplex".
    """
    seed: int = 0
    type: str = "simplex"

    @classmethod
    def noise(cls, x: float) -> float:
        """Generates a 1D noise value."""
        if cls.type == "simplex":
            return OpenSimplex2.noise(cls.seed, x)
        elif cls.type == "perlin":
            return 0.0
        return 0.0

    @classmethod
    def noise2(cls, x: float, y: float) -> float:
        """Generates a 2D noise value."""
        if cls.type == "simpex":
            return OpenSimplex2.noise2(cls.seed, x, y)
        elif cls.type == "perlin":
            return 0.0
        return 0.0

    @classmethod
    def noise3(cls, x: float, y: float, z: float) -> float:
        """Generates a 3D noise value."""
        if cls.type == "simpex":
            return OpenSimplex2.noise3(cls.seed, x, y, z)
        elif cls.type == "perlin":
            return 0.0
        return 0.0

    @classmethod
    def noise4(cls, x: float, y: float, z: float, w: float) -> float:
        """Generates a 4D noise value."""
        if cls.type == "simpex":
            return OpenSimplex2.noise4(cls.seed, x, y, z, w)
        elif cls.type == "perlin":
            return 0.0
        return 0.0


class OpenSimplex2:
    """A Python translation of parts of the OpenSimplex2F algorithm."""
    PRIME_X = 0x5205402B9270C86F
    PRIME_Y = 0x598CD327003817B5
    PRIME_Z = 0x5BCC226E9FA0BACB
    PRIME_W = 0x56CC5227E58F554B
    HASH_MULTIPLIER = 0x53A3F72DEEC546F5
    SEED_FLIP_3D = -0x52D547B2E96ED629
    SEED_OFFSET_4D = 0xE83DC3E0DA7164D

    ROOT2OVER2 = 0.7071067811865476
    SKEW_2D = 0.366025403784439
    UNSKEW_2D = -0.21132486540518713

    ROOT3OVER3 = 0.577350269189626
    FALLBACK_ROTATE_3D = 2.0 / 3.0
    ROTATE_3D_ORTHOGONALIZER = UNSKEW_2D

    SKEW_4D = -0.138196601125011
    UNSKEW_4D = 0.309016994374947
    LATTICE_STEP_4D = 0.2

    N_GRADS_2D_EXPONENT = 7
    N_GRADS_3D_EXPONENT = 8
    N_GRADS_4D_EXPONENT = 9
    N_GRADS_2D = 1 << N_GRADS_2D_EXPONENT
    N_GRADS_3D = 1 << N_GRADS_3D_EXPONENT
    N_GRADS_4D = 1 << N_GRADS_4D_EXPONENT

    NORMALIZER_2D = 0.01001634121365712
    NORMALIZER_3D = 0.07969837668935331
    NORMALIZER_4D = 0.0220065933241897

    RSQUARED_2D = 0.5
    RSQUARED_3D = 0.6
    RSQUARED_4D = 0.6

    GRADIENTS_2D = []
    GRADIENTS_3D = []
    GRADIENTS_4D = []

    @classmethod
    def noise(cls, seed: int, x: float) -> float:
        return cls.noise2(seed, x, 0)

    @classmethod
    def noise2(cls, seed: int, x: float, y: float) -> float:
        s = cls.SKEW_2D * (x + y)
        xs = x + s
        ys = y + s

        return cls.noise2_base(seed, xs, ys)

    @classmethod
    def noise2_base(cls, seed: int, xs: float, ys: float) -> float:
        xsb = Math.floor(xs)
        ysb = Math.floor(ys)
        xi = xs - xsb
        yi = ys - ysb

        xsbp = xsb * cls.PRIME_X
        ysbp = ysb * cls.PRIME_Y

        t = (xi + yi) * cls.UNSKEW_2D
        dx0 = xi + t
        dy0 = yi + t

        value = 0
        a0 = cls.RSQUARED_2D - dx0 * dx0 - dy0 * dy0
        if a0 > 0:
            value = (a0 * a0) * (a0 * a0) * cls.grad2(seed, xsbp, ysbp, dx0, dy0)

        a1 = (2 * (1 + 2 * cls.UNSKEW_2D) *
              (1 / cls.UNSKEW_2D + 2)) * t + ((-2 * (1 + 2 * cls.UNSKEW_2D) * (1 + 2 * cls.UNSKEW_2D)) + a0)
        if a1 > 0:
            dx1 = dx0 - (1 + 2 * cls.UNSKEW_2D)
            dy1 = dy0 - (1 + 2 * cls.UNSKEW_2D)
            value += (a1 * a1) * (a1 * a1) * cls.grad2(seed, xsbp + cls.PRIME_X, ysbp + cls.PRIME_Y, dx1, dy1)

        if dy0 > dx0:
            dx2 = dx0 - cls.UNSKEW_2D
            dy2 = dy0 - (cls.UNSKEW_2D + 1)
            a2 = cls.RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (a2 * a2) * (a2 * a2) * cls.grad2(seed, xsbp, ysbp + cls.PRIME_Y, dx2, dy2)
        else:
            dx2 = dx0 - (cls.UNSKEW_2D + 1)
            dy2 = dy0 - cls.UNSKEW_2D
            a2 = cls.RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (a2 * a2) * (a2 * a2) * cls.grad2(seed, xsbp + cls.PRIME_X, ysbp, dx2, dy2)

        return value

    @classmethod
    def grad2(cls, seed: int, xsvp: int, ysvp: int, dx: float, dy: float) -> float:
        hash_val = seed ^ xsvp ^ ysvp
        hash_val *= cls.HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls.N_GRADS_2D_EXPONENT + 1)
        gi = int(hash_val) & ((cls.N_GRADS_2D - 1) << 1)
        return cls.GRADIENTS_2D[gi | 0] * dx + cls.GRADIENTS_2D[gi | 1] * dy

    @classmethod
    def noise3(cls, seed: int, x: float, y: float, z: float) -> float:
        r = cls.FALLBACK_ROTATE_3D * (x + y + z)
        xr = r - x
        yr = r - y
        zr = r - z

        return cls.noise3_base(seed, xr, yr, zr)

    @classmethod
    def noise3_base(cls, seed: int, xr: float, yr: float, zr: float) -> float:
        xrb = Math.round(xr)
        yrb = Math.round(yr)
        zrb = Math.round(zr)
        xri = xr - xrb
        yri = yr - yrb
        zri = zr - zrb

        x_n_sign = int(-1.0 - xri) | 1
        y_n_sign = int(-1.0 - yri) | 1
        z_n_sign = int(-1.0 - zri) | 1

        ax0 = x_n_sign * -xri
        ay0 = y_n_sign * -yri
        az0 = z_n_sign * -zri

        xrbp = xrb * cls.PRIME_X
        yrbp = yrb * cls.PRIME_Y
        zrbp = zrb * cls.PRIME_Z

        value = 0
        a = (cls.RSQUARED_3D - xri * xri) - (yri * yri + zri * zri)
        l = 0
        while True:
            if a > 0:
                value += (a * a) * (a * a) * cls.grad3(seed, xrbp, yrbp, zrbp, xri, yri, zri)

            if ax0 >= ay0 and ax0 >= az0:
                b = a + ax0 + ax0
                if b > 1:
                    b -= 1
                    value += (b * b) * (b * b) * cls.grad3(
                        seed, xrbp - x_n_sign * cls.PRIME_X, yrbp, zrbp, xri + x_n_sign, yri, zri
                    )
            elif ay0 > ax0 and ay0 >= az0:
                b = a + ay0 + ay0
                if b > 1:
                    b -= 1
                    value += (b * b) * (b * b) * cls.grad3(
                        seed, xrbp, yrbp - y_n_sign * cls.PRIME_Y, zrbp, xri, yri + y_n_sign, zri
                    )
            else:
                b = a + az0 + az0
                if b > 1:
                    b -= 1
                    value += (b * b) * (b * b) * cls.grad3(
                        seed, xrbp, yrbp, zrbp - z_n_sign * cls.PRIME_Z, xri, yri, zri + z_n_sign
                    )

            if l == 1:
                break

            ax0 = 0.5 - ax0
            ay0 = 0.5 - ay0
            az0 = 0.5 - az0

            xri = x_n_sign * ax0
            yri = y_n_sign * ay0
            zri = z_n_sign * az0

            a += (0.75 - ax0) - (ay0 + az0)

            xrbp += (x_n_sign >> 1) & cls.PRIME_X
            yrbp += (y_n_sign >> 1) & cls.PRIME_Y
            zrbp += (z_n_sign >> 1) & cls.PRIME_Z

            x_n_sign = -x_n_sign
            y_n_sign = -y_n_sign
            z_n_sign = -z_n_sign

            seed ^= cls.SEED_FLIP_3D

            l += 1

        return value

    @classmethod
    def grad3(cls, seed: int, xrvp: int, yrvp: int, zrvp: int, dx: float, dy: float, dz: float) -> float:
        hash_val = (seed ^ xrvp) ^ (yrvp ^ zrvp)
        hash_val *= cls.HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls.N_GRADS_3D_EXPONENT + 2)
        gi = int(hash_val) & ((cls.N_GRADS_3D - 1) << 2)
        return cls.GRADIENTS_3D[gi | 0] * dx + cls.GRADIENTS_3D[gi | 1] * dy + cls.GRADIENTS_3D[gi | 2] * dz

    @classmethod
    def noise4(cls, seed: int, x: float, y: float, z: float, w: float) -> float:
        s = cls.SKEW_4D * (x + y + z + w)
        xs = x + s
        ys = y + s
        zs = z + s
        ws = w + s

        return cls.noise4_base(seed, xs, ys, zs, ws)

    @classmethod
    def noise4_base(cls, seed: int, xs: float, ys: float, zs: float, ws: float) -> float:
        xsb = Math.floor(xs)
        ysb = Math.floor(ys)
        zsb = Math.floor(zs)
        wsb = Math.floor(ws)
        xsi = xs - xsb
        ysi = ys - ysb
        zsi = zs - zsb
        wsi = ws - wsb

        si_sum = (xsi + ysi) + (zsi + wsi)
        starting_lattice = int(si_sum * 1.25)

        seed += starting_lattice * cls.SEED_OFFSET_4D

        starting_lattice_offset = starting_lattice * -cls.LATTICE_STEP_4D
        xsi += starting_lattice_offset
        ysi += starting_lattice_offset
        zsi += starting_lattice_offset
        wsi += starting_lattice_offset

        ssi = (si_sum + starting_lattice_offset * 4) * cls.UNSKEW_4D

        xsvp = xsb * cls.PRIME_X
        ysvp = ysb * cls.PRIME_Y
        zsvp = zsb * cls.PRIME_Z
        wsvp = wsb * cls.PRIME_W

        value = 0
        i = 0
        while True:
            score0 = 1.0 + ssi * (-1.0 / cls.UNSKEW_4D)
            if (xsi >= ysi and xsi >= zsi and xsi >= wsi and xsi >= score0):
                xsvp += cls.PRIME_X
                xsi -= 1
                ssi -= cls.UNSKEW_4D
            elif (ysi > xsi and ysi >= zsi and ysi >= wsi and ysi >= score0):
                ysvp += cls.PRIME_Y
                ysi -= 1
                ssi -= cls.UNSKEW_4D
            elif (zsi > xsi and zsi > ysi and zsi >= wsi and zsi >= score0):
                zsvp += cls.PRIME_Z
                zsi -= 1
                ssi -= cls.UNSKEW_4D
            elif (wsi > xsi and wsi > ysi and wsi > zsi and wsi >= score0):
                wsvp += cls.PRIME_W
                wsi -= 1
                ssi -= cls.UNSKEW_4D

            dx = xsi + ssi
            dy = ysi + ssi
            dz = zsi + ssi
            dw = wsi + ssi
            a = (dx * dx + dy * dy) + (dz * dz + dw * dw)
            if a < cls.RSQUARED_4D:
                a -= cls.RSQUARED_4D
                a *= a
                value += a * a * cls.grad4(seed, xsvp, ysvp, zsvp, wsvp, dx, dy, dz, dw)

            if i == 4:
                break

            xsi += cls.LATTICE_STEP_4D
            ysi += cls.LATTICE_STEP_4D
            zsi += cls.LATTICE_STEP_4D
            wsi += cls.LATTICE_STEP_4D
            ssi += cls.LATTICE_STEP_4D * 4 * cls.UNSKEW_4D
            seed -= cls.SEED_OFFSET_4D

            if i == starting_lattice:
                xsvp -= cls.PRIME_X
                ysvp -= cls.PRIME_Y
                zsvp -= cls.PRIME_Z
                wsvp -= cls.PRIME_W
                seed += cls.SEED_OFFSET_4D * 5

            i += 1

        return value

    @classmethod
    def grad4(
        cls, seed: int, xsvp: int, ysvp: int, zsvp: int, wsvp: int, dx: float, dy: float, dz: float, dw: float
    ) -> float:
        hash_val = seed ^ (xsvp ^ ysvp) ^ (zsvp ^ wsvp)
        hash_val *= cls.HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls.N_GRADS_4D_EXPONENT + 2)
        gi = int(hash_val) & ((cls.N_GRADS_4D - 1) << 2)
        return (cls.GRADIENTS_4D[gi | 0] * dx +
                cls.GRADIENTS_4D[gi | 1] * dy) + (cls.GRADIENTS_4D[gi | 2] * dz + cls.GRADIENTS_4D[gi | 3] * dw)


# below is the generator code for the gradients

grad2 = [
    0.38268343236509,
    0.923879532511287,
    0.923879532511287,
    0.38268343236509,
    0.923879532511287,
    -0.38268343236509,
    0.38268343236509,
    -0.923879532511287,
    -0.38268343236509,
    -0.923879532511287,
    -0.923879532511287,
    -0.38268343236509,
    -0.923879532511287,
    0.38268343236509,
    -0.38268343236509,
    0.923879532511287,
    0.130526192220052,
    0.99144486137381,
    0.608761429008721,
    0.793353340291235,
    0.793353340291235,
    0.608761429008721,
    0.99144486137381,
    0.130526192220051,
    0.99144486137381,
    -0.130526192220051,
    0.793353340291235,
    -0.60876142900872,
    0.608761429008721,
    -0.793353340291235,
    0.130526192220052,
    -0.99144486137381,
    -0.130526192220052,
    -0.99144486137381,
    -0.608761429008721,
    -0.793353340291235,
    -0.793353340291235,
    -0.608761429008721,
    -0.99144486137381,
    -0.130526192220052,
    -0.99144486137381,
    0.130526192220051,
    -0.793353340291235,
    0.608761429008721,
    -0.608761429008721,
    0.793353340291235,
    -0.130526192220052,
    0.99144486137381,
]

for grad_i in range(len(grad2)):
    grad2[grad_i] = grad2[grad_i] / OpenSimplex2.NORMALIZER_2D

grad_j = 0
for grad_i in range(OpenSimplex2.N_GRADS_2D * 2):
    if grad_j == len(grad2):
        grad_j = 0
    OpenSimplex2.GRADIENTS_2D.append(grad2[grad_j])
    grad_j += 1

grad3 = [
    2.22474487139,
    2.22474487139,
    -1.0,
    0.0,
    2.22474487139,
    2.22474487139,
    1.0,
    0.0,
    3.0862664687972017,
    1.1721513422464978,
    0.0,
    0.0,
    1.1721513422464978,
    3.0862664687972017,
    0.0,
    0.0,
    -2.22474487139,
    2.22474487139,
    -1.0,
    0.0,
    -2.22474487139,
    2.22474487139,
    1.0,
    0.0,
    -1.1721513422464978,
    3.0862664687972017,
    0.0,
    0.0,
    -3.0862664687972017,
    1.1721513422464978,
    0.0,
    0.0,
    -1.0,
    -2.22474487139,
    -2.22474487139,
    0.0,
    1.0,
    -2.22474487139,
    -2.22474487139,
    0.0,
    0.0,
    -3.0862664687972017,
    -1.1721513422464978,
    0.0,
    0.0,
    -1.1721513422464978,
    -3.0862664687972017,
    0.0,
    -1.0,
    -2.22474487139,
    2.22474487139,
    0.0,
    1.0,
    -2.22474487139,
    2.22474487139,
    0.0,
    0.0,
    -1.1721513422464978,
    3.0862664687972017,
    0.0,
    0.0,
    -3.0862664687972017,
    1.1721513422464978,
    0.0,
    -2.22474487139,
    -2.22474487139,
    -1.0,
    0.0,
    -2.22474487139,
    -2.22474487139,
    1.0,
    0.0,
    -3.0862664687972017,
    -1.1721513422464978,
    0.0,
    0.0,
    -1.1721513422464978,
    -3.0862664687972017,
    0.0,
    0.0,
    -2.22474487139,
    -1.0,
    -2.22474487139,
    0.0,
    -2.22474487139,
    1.0,
    -2.22474487139,
    0.0,
    -1.1721513422464978,
    0.0,
    -3.0862664687972017,
    0.0,
    -3.0862664687972017,
    0.0,
    -1.1721513422464978,
    0.0,
    -2.22474487139,
    -1.0,
    2.22474487139,
    0.0,
    -2.22474487139,
    1.0,
    2.22474487139,
    0.0,
    -3.0862664687972017,
    0.0,
    1.1721513422464978,
    0.0,
    -1.1721513422464978,
    0.0,
    3.0862664687972017,
    0.0,
    -1.0,
    2.22474487139,
    -2.22474487139,
    0.0,
    1.0,
    2.22474487139,
    -2.22474487139,
    0.0,
    0.0,
    1.1721513422464978,
    -3.0862664687972017,
    0.0,
    0.0,
    3.0862664687972017,
    -1.1721513422464978,
    0.0,
    -1.0,
    2.22474487139,
    2.22474487139,
    0.0,
    1.0,
    2.22474487139,
    2.22474487139,
    0.0,
    0.0,
    3.0862664687972017,
    1.1721513422464978,
    0.0,
    0.0,
    1.1721513422464978,
    3.0862664687972017,
    0.0,
    2.22474487139,
    -2.22474487139,
    -1.0,
    0.0,
    2.22474487139,
    -2.22474487139,
    1.0,
    0.0,
    1.1721513422464978,
    -3.0862664687972017,
    0.0,
    0.0,
    3.0862664687972017,
    -1.1721513422464978,
    0.0,
    0.0,
    2.22474487139,
    -1.0,
    -2.22474487139,
    0.0,
    2.22474487139,
    1.0,
    -2.22474487139,
    0.0,
    3.0862664687972017,
    0.0,
    -1.1721513422464978,
    0.0,
    1.1721513422464978,
    0.0,
    -3.0862664687972017,
    0.0,
    2.22474487139,
    -1.0,
    2.22474487139,
    0.0,
    2.22474487139,
    1.0,
    2.22474487139,
    0.0,
    1.1721513422464978,
    0.0,
    3.0862664687972017,
    0.0,
    3.0862664687972017,
    0.0,
    1.1721513422464978,
    0.0,
]

for grad_i in range(len(grad3)):
    grad3[grad_i] = grad3[grad_i] / OpenSimplex2.NORMALIZER_3D

grad_j = 0
for grad_i in range(OpenSimplex2.N_GRADS_3D * 2):
    if grad_j == len(grad3):
        grad_j = 0
    OpenSimplex2.GRADIENTS_3D.append(grad3[grad_j])
    grad_j += 1

grad4 = [
    -0.6740059517812944,
    -0.3239847771997537,
    -0.3239847771997537,
    0.5794684678643381,
    -0.7504883828755602,
    -0.4004672082940195,
    0.15296486218853164,
    0.5029860367700724,
    -0.7504883828755602,
    0.15296486218853164,
    -0.4004672082940195,
    0.5029860367700724,
    -0.8828161875373585,
    0.08164729285680945,
    0.08164729285680945,
    0.4553054119602712,
    -0.4553054119602712,
    -0.08164729285680945,
    -0.08164729285680945,
    0.8828161875373585,
    -0.5029860367700724,
    -0.15296486218853164,
    0.4004672082940195,
    0.7504883828755602,
    -0.5029860367700724,
    0.4004672082940195,
    -0.15296486218853164,
    0.7504883828755602,
    -0.5794684678643381,
    0.3239847771997537,
    0.3239847771997537,
    0.6740059517812944,
    -0.6740059517812944,
    -0.3239847771997537,
    0.5794684678643381,
    -0.3239847771997537,
    -0.7504883828755602,
    -0.4004672082940195,
    0.5029860367700724,
    0.15296486218853164,
    -0.7504883828755602,
    0.15296486218853164,
    0.5029860367700724,
    -0.4004672082940195,
    -0.8828161875373585,
    0.08164729285680945,
    0.4553054119602712,
    0.08164729285680945,
    -0.4553054119602712,
    -0.08164729285680945,
    0.8828161875373585,
    -0.08164729285680945,
    -0.5029860367700724,
    -0.15296486218853164,
    0.7504883828755602,
    0.4004672082940195,
    -0.5029860367700724,
    0.4004672082940195,
    0.7504883828755602,
    -0.15296486218853164,
    -0.5794684678643381,
    0.3239847771997537,
    0.6740059517812944,
    0.3239847771997537,
    -0.6740059517812944,
    0.5794684678643381,
    -0.3239847771997537,
    -0.3239847771997537,
    -0.7504883828755602,
    0.5029860367700724,
    -0.4004672082940195,
    0.15296486218853164,
    -0.7504883828755602,
    0.5029860367700724,
    0.15296486218853164,
    -0.4004672082940195,
    -0.8828161875373585,
    0.4553054119602712,
    0.08164729285680945,
    0.08164729285680945,
    -0.4553054119602712,
    0.8828161875373585,
    -0.08164729285680945,
    -0.08164729285680945,
    -0.5029860367700724,
    0.7504883828755602,
    -0.15296486218853164,
    0.4004672082940195,
    -0.5029860367700724,
    0.7504883828755602,
    0.4004672082940195,
    -0.15296486218853164,
    -0.5794684678643381,
    0.6740059517812944,
    0.3239847771997537,
    0.3239847771997537,
    0.5794684678643381,
    -0.6740059517812944,
    -0.3239847771997537,
    -0.3239847771997537,
    0.5029860367700724,
    -0.7504883828755602,
    -0.4004672082940195,
    0.15296486218853164,
    0.5029860367700724,
    -0.7504883828755602,
    0.15296486218853164,
    -0.4004672082940195,
    0.4553054119602712,
    -0.8828161875373585,
    0.08164729285680945,
    0.08164729285680945,
    0.8828161875373585,
    -0.4553054119602712,
    -0.08164729285680945,
    -0.08164729285680945,
    0.7504883828755602,
    -0.5029860367700724,
    -0.15296486218853164,
    0.4004672082940195,
    0.7504883828755602,
    -0.5029860367700724,
    0.4004672082940195,
    -0.15296486218853164,
    0.6740059517812944,
    -0.5794684678643381,
    0.3239847771997537,
    0.3239847771997537,
    -0.753341017856078,
    -0.37968289875261624,
    -0.37968289875261624,
    -0.37968289875261624,
    -0.7821684431180708,
    -0.4321472685365301,
    -0.4321472685365301,
    0.12128480194602098,
    -0.7821684431180708,
    -0.4321472685365301,
    0.12128480194602098,
    -0.4321472685365301,
    -0.7821684431180708,
    0.12128480194602098,
    -0.4321472685365301,
    -0.4321472685365301,
    -0.8586508742123365,
    -0.508629699630796,
    0.044802370851755174,
    0.044802370851755174,
    -0.8586508742123365,
    0.044802370851755174,
    -0.508629699630796,
    0.044802370851755174,
    -0.8586508742123365,
    0.044802370851755174,
    0.044802370851755174,
    -0.508629699630796,
    -0.9982828964265062,
    -0.03381941603233842,
    -0.03381941603233842,
    -0.03381941603233842,
    -0.37968289875261624,
    -0.753341017856078,
    -0.37968289875261624,
    -0.37968289875261624,
    -0.4321472685365301,
    -0.7821684431180708,
    -0.4321472685365301,
    0.12128480194602098,
    -0.4321472685365301,
    -0.7821684431180708,
    0.12128480194602098,
    -0.4321472685365301,
    0.12128480194602098,
    -0.7821684431180708,
    -0.4321472685365301,
    -0.4321472685365301,
    -0.508629699630796,
    -0.8586508742123365,
    0.044802370851755174,
    0.044802370851755174,
    0.044802370851755174,
    -0.8586508742123365,
    -0.508629699630796,
    0.044802370851755174,
    0.044802370851755174,
    -0.8586508742123365,
    0.044802370851755174,
    -0.508629699630796,
    -0.03381941603233842,
    -0.9982828964265062,
    -0.03381941603233842,
    -0.03381941603233842,
    -0.37968289875261624,
    -0.37968289875261624,
    -0.753341017856078,
    -0.37968289875261624,
    -0.4321472685365301,
    -0.4321472685365301,
    -0.7821684431180708,
    0.12128480194602098,
    -0.4321472685365301,
    0.12128480194602098,
    -0.7821684431180708,
    -0.4321472685365301,
    0.12128480194602098,
    -0.4321472685365301,
    -0.7821684431180708,
    -0.4321472685365301,
    -0.508629699630796,
    0.044802370851755174,
    -0.8586508742123365,
    0.044802370851755174,
    0.044802370851755174,
    -0.508629699630796,
    -0.8586508742123365,
    0.044802370851755174,
    0.044802370851755174,
    0.044802370851755174,
    -0.8586508742123365,
    -0.508629699630796,
    -0.03381941603233842,
    -0.03381941603233842,
    -0.9982828964265062,
    -0.03381941603233842,
    -0.37968289875261624,
    -0.37968289875261624,
    -0.37968289875261624,
    -0.753341017856078,
    -0.4321472685365301,
    -0.4321472685365301,
    0.12128480194602098,
    -0.7821684431180708,
    -0.4321472685365301,
    0.12128480194602098,
    -0.4321472685365301,
    -0.7821684431180708,
    0.12128480194602098,
    -0.4321472685365301,
    -0.4321472685365301,
    -0.7821684431180708,
    -0.508629699630796,
    0.044802370851755174,
    0.044802370851755174,
    -0.8586508742123365,
    0.044802370851755174,
    -0.508629699630796,
    0.044802370851755174,
    -0.8586508742123365,
    0.044802370851755174,
    0.044802370851755174,
    -0.508629699630796,
    -0.8586508742123365,
    -0.03381941603233842,
    -0.03381941603233842,
    -0.03381941603233842,
    -0.9982828964265062,
    -0.3239847771997537,
    -0.6740059517812944,
    -0.3239847771997537,
    0.5794684678643381,
    -0.4004672082940195,
    -0.7504883828755602,
    0.15296486218853164,
    0.5029860367700724,
    0.15296486218853164,
    -0.7504883828755602,
    -0.4004672082940195,
    0.5029860367700724,
    0.08164729285680945,
    -0.8828161875373585,
    0.08164729285680945,
    0.4553054119602712,
    -0.08164729285680945,
    -0.4553054119602712,
    -0.08164729285680945,
    0.8828161875373585,
    -0.15296486218853164,
    -0.5029860367700724,
    0.4004672082940195,
    0.7504883828755602,
    0.4004672082940195,
    -0.5029860367700724,
    -0.15296486218853164,
    0.7504883828755602,
    0.3239847771997537,
    -0.5794684678643381,
    0.3239847771997537,
    0.6740059517812944,
    -0.3239847771997537,
    -0.3239847771997537,
    -0.6740059517812944,
    0.5794684678643381,
    -0.4004672082940195,
    0.15296486218853164,
    -0.7504883828755602,
    0.5029860367700724,
    0.15296486218853164,
    -0.4004672082940195,
    -0.7504883828755602,
    0.5029860367700724,
    0.08164729285680945,
    0.08164729285680945,
    -0.8828161875373585,
    0.4553054119602712,
    -0.08164729285680945,
    -0.08164729285680945,
    -0.4553054119602712,
    0.8828161875373585,
    -0.15296486218853164,
    0.4004672082940195,
    -0.5029860367700724,
    0.7504883828755602,
    0.4004672082940195,
    -0.15296486218853164,
    -0.5029860367700724,
    0.7504883828755602,
    0.3239847771997537,
    0.3239847771997537,
    -0.5794684678643381,
    0.6740059517812944,
    -0.3239847771997537,
    -0.6740059517812944,
    0.5794684678643381,
    -0.3239847771997537,
    -0.4004672082940195,
    -0.7504883828755602,
    0.5029860367700724,
    0.15296486218853164,
    0.15296486218853164,
    -0.7504883828755602,
    0.5029860367700724,
    -0.4004672082940195,
    0.08164729285680945,
    -0.8828161875373585,
    0.4553054119602712,
    0.08164729285680945,
    -0.08164729285680945,
    -0.4553054119602712,
    0.8828161875373585,
    -0.08164729285680945,
    -0.15296486218853164,
    -0.5029860367700724,
    0.7504883828755602,
    0.4004672082940195,
    0.4004672082940195,
    -0.5029860367700724,
    0.7504883828755602,
    -0.15296486218853164,
    0.3239847771997537,
    -0.5794684678643381,
    0.6740059517812944,
    0.3239847771997537,
    -0.3239847771997537,
    -0.3239847771997537,
    0.5794684678643381,
    -0.6740059517812944,
    -0.4004672082940195,
    0.15296486218853164,
    0.5029860367700724,
    -0.7504883828755602,
    0.15296486218853164,
    -0.4004672082940195,
    0.5029860367700724,
    -0.7504883828755602,
    0.08164729285680945,
    0.08164729285680945,
    0.4553054119602712,
    -0.8828161875373585,
    -0.08164729285680945,
    -0.08164729285680945,
    0.8828161875373585,
    -0.4553054119602712,
    -0.15296486218853164,
    0.4004672082940195,
    0.7504883828755602,
    -0.5029860367700724,
    0.4004672082940195,
    -0.15296486218853164,
    0.7504883828755602,
    -0.5029860367700724,
    0.3239847771997537,
    0.3239847771997537,
    0.6740059517812944,
    -0.5794684678643381,
    -0.3239847771997537,
    0.5794684678643381,
    -0.6740059517812944,
    -0.3239847771997537,
    -0.4004672082940195,
    0.5029860367700724,
    -0.7504883828755602,
    0.15296486218853164,
    0.15296486218853164,
    0.5029860367700724,
    -0.7504883828755602,
    -0.4004672082940195,
    0.08164729285680945,
    0.4553054119602712,
    -0.8828161875373585,
    0.08164729285680945,
    -0.08164729285680945,
    0.8828161875373585,
    -0.4553054119602712,
    -0.08164729285680945,
    -0.15296486218853164,
    0.7504883828755602,
    -0.5029860367700724,
    0.4004672082940195,
    0.4004672082940195,
    0.7504883828755602,
    -0.5029860367700724,
    -0.15296486218853164,
    0.3239847771997537,
    0.6740059517812944,
    -0.5794684678643381,
    0.3239847771997537,
    -0.3239847771997537,
    0.5794684678643381,
    -0.3239847771997537,
    -0.6740059517812944,
    -0.4004672082940195,
    0.5029860367700724,
    0.15296486218853164,
    -0.7504883828755602,
    0.15296486218853164,
    0.5029860367700724,
    -0.4004672082940195,
    -0.7504883828755602,
    0.08164729285680945,
    0.4553054119602712,
    0.08164729285680945,
    -0.8828161875373585,
    -0.08164729285680945,
    0.8828161875373585,
    -0.08164729285680945,
    -0.4553054119602712,
    -0.15296486218853164,
    0.7504883828755602,
    0.4004672082940195,
    -0.5029860367700724,
    0.4004672082940195,
    0.7504883828755602,
    -0.15296486218853164,
    -0.5029860367700724,
    0.3239847771997537,
    0.6740059517812944,
    0.3239847771997537,
    -0.5794684678643381,
    0.5794684678643381,
    -0.3239847771997537,
    -0.6740059517812944,
    -0.3239847771997537,
    0.5029860367700724,
    -0.4004672082940195,
    -0.7504883828755602,
    0.15296486218853164,
    0.5029860367700724,
    0.15296486218853164,
    -0.7504883828755602,
    -0.4004672082940195,
    0.4553054119602712,
    0.08164729285680945,
    -0.8828161875373585,
    0.08164729285680945,
    0.8828161875373585,
    -0.08164729285680945,
    -0.4553054119602712,
    -0.08164729285680945,
    0.7504883828755602,
    -0.15296486218853164,
    -0.5029860367700724,
    0.4004672082940195,
    0.7504883828755602,
    0.4004672082940195,
    -0.5029860367700724,
    -0.15296486218853164,
    0.6740059517812944,
    0.3239847771997537,
    -0.5794684678643381,
    0.3239847771997537,
    0.5794684678643381,
    -0.3239847771997537,
    -0.3239847771997537,
    -0.6740059517812944,
    0.5029860367700724,
    -0.4004672082940195,
    0.15296486218853164,
    -0.7504883828755602,
    0.5029860367700724,
    0.15296486218853164,
    -0.4004672082940195,
    -0.7504883828755602,
    0.4553054119602712,
    0.08164729285680945,
    0.08164729285680945,
    -0.8828161875373585,
    0.8828161875373585,
    -0.08164729285680945,
    -0.08164729285680945,
    -0.4553054119602712,
    0.7504883828755602,
    -0.15296486218853164,
    0.4004672082940195,
    -0.5029860367700724,
    0.7504883828755602,
    0.4004672082940195,
    -0.15296486218853164,
    -0.5029860367700724,
    0.6740059517812944,
    0.3239847771997537,
    0.3239847771997537,
    -0.5794684678643381,
    0.03381941603233842,
    0.03381941603233842,
    0.03381941603233842,
    0.9982828964265062,
    -0.044802370851755174,
    -0.044802370851755174,
    0.508629699630796,
    0.8586508742123365,
    -0.044802370851755174,
    0.508629699630796,
    -0.044802370851755174,
    0.8586508742123365,
    -0.12128480194602098,
    0.4321472685365301,
    0.4321472685365301,
    0.7821684431180708,
    0.508629699630796,
    -0.044802370851755174,
    -0.044802370851755174,
    0.8586508742123365,
    0.4321472685365301,
    -0.12128480194602098,
    0.4321472685365301,
    0.7821684431180708,
    0.4321472685365301,
    0.4321472685365301,
    -0.12128480194602098,
    0.7821684431180708,
    0.37968289875261624,
    0.37968289875261624,
    0.37968289875261624,
    0.753341017856078,
    0.03381941603233842,
    0.03381941603233842,
    0.9982828964265062,
    0.03381941603233842,
    -0.044802370851755174,
    0.044802370851755174,
    0.8586508742123365,
    0.508629699630796,
    -0.044802370851755174,
    0.508629699630796,
    0.8586508742123365,
    -0.044802370851755174,
    -0.12128480194602098,
    0.4321472685365301,
    0.7821684431180708,
    0.4321472685365301,
    0.508629699630796,
    -0.044802370851755174,
    0.8586508742123365,
    -0.044802370851755174,
    0.4321472685365301,
    -0.12128480194602098,
    0.7821684431180708,
    0.4321472685365301,
    0.4321472685365301,
    0.4321472685365301,
    0.7821684431180708,
    -0.12128480194602098,
    0.37968289875261624,
    0.37968289875261624,
    0.753341017856078,
    0.37968289875261624,
    0.03381941603233842,
    0.9982828964265062,
    0.03381941603233842,
    0.03381941603233842,
    -0.044802370851755174,
    0.8586508742123365,
    -0.044802370851755174,
    0.508629699630796,
    -0.044802370851755174,
    0.8586508742123365,
    0.508629699630796,
    -0.044802370851755174,
    -0.12128480194602098,
    0.7821684431180708,
    0.4321472685365301,
    0.4321472685365301,
    0.508629699630796,
    0.8586508742123365,
    -0.044802370851755174,
    -0.044802370851755174,
    0.4321472685365301,
    0.7821684431180708,
    -0.12128480194602098,
    0.4321472685365301,
    0.4321472685365301,
    0.7821684431180708,
    0.4321472685365301,
    -0.12128480194602098,
    0.37968289875261624,
    0.753341017856078,
    0.37968289875261624,
    0.37968289875261624,
    0.9982828964265062,
    0.03381941603233842,
    0.03381941603233842,
    0.03381941603233842,
    0.8586508742123365,
    -0.044802370851755174,
    -0.044802370851755174,
    0.508629699630796,
    0.8586508742123365,
    -0.044802370851755174,
    0.508629699630796,
    -0.044802370851755174,
    0.7821684431180708,
    -0.12128480194602098,
    0.4321472685365301,
    0.4321472685365301,
    0.8586508742123365,
    0.508629699630796,
    -0.044802370851755174,
    -0.044802370851755174,
    0.7821684431180708,
    0.4321472685365301,
    -0.12128480194602098,
    0.4321472685365301,
    0.7821684431180708,
    0.4321472685365301,
    0.4321472685365301,
    -0.12128480194602098,
    0.753341017856078,
    0.37968289875261624,
    0.37968289875261624,
    0.37968289875261624,
]

for grad_i in range(len(grad4)):
    grad4[grad_i] = grad4[grad_i] / OpenSimplex2.NORMALIZER_4D

grad_j = 0
for grad_i in range(OpenSimplex2.N_GRADS_4D * 2):
    if grad_j == len(grad4):
        grad_j = 0
    OpenSimplex2.GRADIENTS_4D.append(grad4[grad_j])
    grad_j += 1
