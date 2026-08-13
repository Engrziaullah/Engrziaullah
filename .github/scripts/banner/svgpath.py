"""Minimal, correct SVG path 'd' parser -> list of flattened polygon subpaths (numpy Nx2 arrays).
Handles M/m L/l H/h V/v C/c S/s Q/q T/t A/a Z/z, including packed-flag arc args
("00-1.327" = flag 0, flag 0, x -1.327) and juxtaposed-number notation (".41.41", "-.23-.08")
that trip up regex-only tokenizers.
"""
import re
import numpy as np

_NUM_RE = re.compile(r"[-+]?(\d+\.\d+|\.\d+|\d+)(?:[eE][-+]?\d+)?")
_FLAG_RE = re.compile(r"[01]")


class _Scanner:
    def __init__(self, d):
        self.s = d
        self.i = 0
        self.n = len(d)

    def skip_ws(self):
        while self.i < self.n and (self.s[self.i].isspace() or self.s[self.i] == ","):
            self.i += 1

    def peek_cmd(self):
        self.skip_ws()
        if self.i < self.n and self.s[self.i].isalpha():
            return self.s[self.i]
        return None

    def take_cmd(self):
        c = self.peek_cmd()
        if c is not None:
            self.i += 1
        return c

    def more_args(self):
        self.skip_ws()
        return self.i < self.n and (self.s[self.i].isdigit() or self.s[self.i] in "-+.")

    def num(self):
        self.skip_ws()
        m = _NUM_RE.match(self.s, self.i)
        if not m:
            raise ValueError(f"expected number at {self.i}: ...{self.s[self.i:self.i+20]!r}")
        self.i = m.end()
        return float(m.group(0))

    def flag(self):
        self.skip_ws()
        m = _FLAG_RE.match(self.s, self.i)
        if not m:
            raise ValueError(f"expected flag(0/1) at {self.i}: ...{self.s[self.i:self.i+20]!r}")
        self.i = m.end()
        return m.group(0) == "1"


def parse_path_d(d):
    """Returns list of subpaths; each is an (N,2) float ndarray of flattened points."""
    sc = _Scanner(d)
    subpaths = []
    cur = []
    cur_pos = complex(0, 0)
    start_pos = complex(0, 0)
    last_ctrl = None
    cmd = None

    def flush_subpath():
        nonlocal cur
        if cur:
            subpaths.append(cur)
        cur = []

    def cubic(base, c1, c2, end):
        ts = np.linspace(0, 1, 20)[1:]
        for t in ts:
            pt = (1 - t) ** 3 * base + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t**2 * c2 + t**3 * end
            cur.append(pt)

    def quad(base, c1, end):
        ts = np.linspace(0, 1, 16)[1:]
        for t in ts:
            pt = (1 - t) ** 2 * base + 2 * (1 - t) * t * c1 + t**2 * end
            cur.append(pt)

    def arc(base, rx, ry, rot_deg, large, sweep, end):
        if rx == 0 or ry == 0 or base == end:
            cur.append(end)
            return
        phi = np.radians(rot_deg)
        x1, y1 = base.real, base.imag
        x2, y2 = end.real, end.imag
        dx2, dy2 = (x1 - x2) / 2, (y1 - y2) / 2
        x1p = np.cos(phi) * dx2 + np.sin(phi) * dy2
        y1p = -np.sin(phi) * dx2 + np.cos(phi) * dy2
        rxa, rya = abs(rx), abs(ry)
        lam = (x1p**2) / (rxa**2) + (y1p**2) / (rya**2)
        if lam > 1:
            s = np.sqrt(lam)
            rxa, rya = rxa * s, rya * s
        sign = -1 if large == sweep else 1
        num = rxa**2 * rya**2 - rxa**2 * y1p**2 - rya**2 * x1p**2
        den = rxa**2 * y1p**2 + rya**2 * x1p**2
        co = sign * np.sqrt(max(num, 0) / den) if den > 0 else 0
        cxp = co * rxa * y1p / rya
        cyp = -co * rya * x1p / rxa
        cx = np.cos(phi) * cxp - np.sin(phi) * cyp + (x1 + x2) / 2
        cy = np.sin(phi) * cxp + np.cos(phi) * cyp + (y1 + y2) / 2

        def ang(ux, uy, vx, vy):
            dot = ux * vx + uy * vy
            length = np.sqrt(ux**2 + uy**2) * np.sqrt(vx**2 + vy**2)
            a = np.arccos(np.clip(dot / length, -1, 1))
            return -a if (ux * vy - uy * vx) < 0 else a

        theta1 = ang(1, 0, (x1p - cxp) / rxa, (y1p - cyp) / rya)
        dtheta = ang((x1p - cxp) / rxa, (y1p - cyp) / rya, (-x1p - cxp) / rxa, (-y1p - cyp) / rya)
        if not sweep and dtheta > 0:
            dtheta -= 2 * np.pi
        elif sweep and dtheta < 0:
            dtheta += 2 * np.pi
        ts = np.linspace(0, 1, 24)[1:]
        for t in ts:
            th = theta1 + t * dtheta
            x = cx + rxa * np.cos(phi) * np.cos(th) - rya * np.sin(phi) * np.sin(th)
            y = cy + rxa * np.sin(phi) * np.cos(th) + rya * np.cos(phi) * np.sin(th)
            cur.append(complex(x, y))

    while True:
        c = sc.peek_cmd()
        if c is not None:
            sc.take_cmd()
            cmd = c
        elif not sc.more_args():
            break
        if cmd is None:
            break
        cl = cmd.lower()
        relative = cmd.islower()

        if cl == "m":
            x, y = sc.num(), sc.num()
            pt = (cur_pos + complex(x, y)) if relative else complex(x, y)
            flush_subpath()
            cur.append(pt)
            cur_pos = pt
            start_pos = pt
            last_ctrl = None
            cmd = "l" if relative else "L"
        elif cl == "l":
            x, y = sc.num(), sc.num()
            pt = (cur_pos + complex(x, y)) if relative else complex(x, y)
            cur.append(pt)
            cur_pos = pt
            last_ctrl = None
        elif cl == "h":
            x = sc.num()
            pt = complex(cur_pos.real + x, cur_pos.imag) if relative else complex(x, cur_pos.imag)
            cur.append(pt)
            cur_pos = pt
            last_ctrl = None
        elif cl == "v":
            y = sc.num()
            pt = complex(cur_pos.real, cur_pos.imag + y) if relative else complex(cur_pos.real, y)
            cur.append(pt)
            cur_pos = pt
            last_ctrl = None
        elif cl == "c":
            x1, y1, x2, y2, x, y = (sc.num() for _ in range(6))
            base = cur_pos
            C1 = base + complex(x1, y1) if relative else complex(x1, y1)
            C2 = base + complex(x2, y2) if relative else complex(x2, y2)
            E = base + complex(x, y) if relative else complex(x, y)
            cubic(base, C1, C2, E)
            cur_pos = E
            last_ctrl = C2
        elif cl == "s":
            x2, y2, x, y = (sc.num() for _ in range(4))
            base = cur_pos
            C1 = (2 * base - last_ctrl) if last_ctrl is not None else base
            C2 = base + complex(x2, y2) if relative else complex(x2, y2)
            E = base + complex(x, y) if relative else complex(x, y)
            cubic(base, C1, C2, E)
            cur_pos = E
            last_ctrl = C2
        elif cl == "q":
            x1, y1, x, y = (sc.num() for _ in range(4))
            base = cur_pos
            C1 = base + complex(x1, y1) if relative else complex(x1, y1)
            E = base + complex(x, y) if relative else complex(x, y)
            quad(base, C1, E)
            cur_pos = E
            last_ctrl = C1
        elif cl == "t":
            x, y = sc.num(), sc.num()
            base = cur_pos
            C1 = (2 * base - last_ctrl) if last_ctrl is not None else base
            E = base + complex(x, y) if relative else complex(x, y)
            quad(base, C1, E)
            cur_pos = E
            last_ctrl = C1
        elif cl == "a":
            rx, ry, rot = sc.num(), sc.num(), sc.num()
            large, sweep = sc.flag(), sc.flag()
            x, y = sc.num(), sc.num()
            base = cur_pos
            E = base + complex(x, y) if relative else complex(x, y)
            arc(base, rx, ry, rot, large, sweep, E)
            cur_pos = E
            last_ctrl = None
        elif cl == "z":
            cur.append(start_pos)
            cur_pos = start_pos
            last_ctrl = None
            # after Z, an immediately-following number belongs to no implicit command; stop implicit repeat
            cmd = None
        else:
            raise ValueError(f"unsupported path command {cmd!r}")

    flush_subpath()
    return [np.array([(p.real, p.imag) for p in sp]) for sp in subpaths]


if __name__ == "__main__":
    polys = parse_path_d("M10 10 L20 10 L20 20 Z")
    print(len(polys), polys[0])
