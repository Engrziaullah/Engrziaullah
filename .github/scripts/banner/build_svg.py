"""Stage 5: assemble the full animated dark.svg / light.svg."""
import os
import html
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "..", "assets"))

W, H = 1180, 610
GRID_W, GRID_H = 300, 340
RASTER_RES = 260
N_INTRO_GROUPS = 60
N_BANDS = 94

FRAME_X, FRAME_Y, FRAME_W, FRAME_H = 36, 84, 448, 492
GAP = 34
INFO_X = FRAME_X + FRAME_W + GAP           # 518
INFO_RIGHT = 1125
ROW_TEXTLEN = INFO_RIGHT - INFO_X          # 607
ROW_TOTAL_CHARS = 74

DOT_S = 1.6          # portrait dot square size (svg units)
TRAV_S = 3.4          # traveler dot square size

# --- timeline (seconds) ---
T_INTRO_FADE = 2.0
T_INTRO_TOTAL = 3.2
T_HOLD0 = 3.0     # portrait hold at loop-local t=0..3.0
T_T1_END = 4.3    # transition into python
T_HOLD1_END = 6.3
T_T2_END = 7.6
T_HOLD2_END = 9.6
T_T3_END = 10.9
T_HOLD3_END = 12.9
T_CYCLE = 14.2    # T4 end == full cycle length
LOOP_BEGIN = 3.2  # loop anchors start exactly when intro hands off

ROWS = [
    ("Subject", "Zia Ullah"),
    ("Role", "AI/ML Engineer"),
    ("Origin", "Malakand, Pakistan"),
    ("Education", "BS Software Engineering, 6th Sem"),
    ("Status", "Building + Researching + Shipping"),
    ("ToolChain", "VS Code, Git, GitHub, Jupyter"),
    ("__gap__", None),
    ("Core.Lang", "Python, SQL, C++"),
    ("Core.GenAI", "LangChain, LangGraph, LangSmith"),
    ("Core.Vision", "OpenCV, MediaPipe"),
    ("Core.ML", "TensorFlow, Keras, scikit-learn"),
    ("Core.Infra", "FastAPI, Flask, Streamlit, AWS"),
    ("__gap__", None),
    ("Grid.Mail", "ziaullahbj9@gmail.com"),
    ("Grid.Kaggle", "ziaullah299"),
    ("Grid.LinkedIn", "engr-ziaullah-innovation"),
    ("Grid.GitHub", "@Engrziaullah"),
    ("Grid.IEEE", "President, Univ. of Malakand"),
]

THEMES = {
    "dark": dict(
        bg="#0B0F19", panel_bar="#0B1222", panel="#0C1426", win_bg="#070B16",
        portrait="#818CF8", chrome="#22D3EE", accent="#10B981",
        text="#F8FAFC", muted="#94A3B8", dim="#475569", dots="rgba(148,163,184,0.35)",
        pill_bg="#312E81", pill_text="#EEF2FF", live="#F87171", border_line="rgba(255,255,255,0.10)",
    ),
    "light": dict(
        bg="#FFFFFF", panel_bar="#F1F5F9", panel="#F8FAFC", win_bg="#FFFFFF",
        portrait="#4F46E5", chrome="#0891B2", accent="#10B981",
        text="#0F172A", muted="#475569", dim="#94A3B8", dots="rgba(15,23,42,0.25)",
        pill_bg="#EEF2FF", pill_text="#4338CA", live="#DC2626", border_line="rgba(15,23,42,0.10)",
    ),
}


def esc(s):
    return html.escape(str(s), quote=True)


def portrait_to_svg(row, col, scale, ox, oy):
    return ox + col * scale, oy + row * scale


def logo_to_svg(x, y, scale, ox, oy):
    return ox + x * scale, oy + y * scale


def make_portrait_transform():
    scale = FRAME_H / GRID_H
    disp_w = GRID_W * scale
    ox = FRAME_X + (FRAME_W - disp_w) / 2
    oy = FRAME_Y
    return scale, ox, oy


def make_logo_transform():
    scale = (FRAME_H * 0.80) / RASTER_RES
    disp = RASTER_RES * scale
    ox = FRAME_X + (FRAME_W - disp) / 2
    oy = FRAME_Y + (FRAME_H - disp) / 2
    return scale, ox, oy


def dot_run_path(points_xy, size=DOT_S):
    s = size
    parts = []
    for x, y in points_xy:
        xi, yi = int(round(x)), int(round(y))
        parts.append(f"M{xi} {yi}h{s:g}v{s:g}h-{s:g}z")
    return "".join(parts)


def build_intro_layer(dot_rc, group_ids, scale, ox, oy, color):
    e = []
    a = e.append
    a(f'<g id="introLayer" opacity="1">')
    a(f'<animate attributeName="opacity" from="1" to="0" begin="{LOOP_BEGIN}s" dur="1.3s" fill="freeze"/>')
    n = N_INTRO_GROUPS
    for g in range(n):
        m = group_ids == g
        if not np.any(m):
            continue
        pts = [portrait_to_svg(r, c, scale, ox, oy) for r, c in dot_rc[m]]
        d = dot_run_path(pts)
        begin = 0.02 * g  # staggered across ~1.18s so fades (0.8s each) finish by ~2.0s
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
          f'dur="0.8s" fill="freeze"/><path d="{d}" fill="{color}" shape-rendering="crispEdges"/></g>')
    a("</g>")
    return "".join(e)


def build_loop_portrait_layer(dot_rc, band_grid, band_centroids, scale, ox, oy, color, python_centroid_svg):
    band_ids = band_grid[dot_rc[:, 0], dot_rc[:, 1]]
    e = []
    a = e.append
    a('<g id="loopPortrait">')
    key_times = f"0;{T_HOLD0/T_CYCLE:.4f};{T_T1_END/T_CYCLE:.4f};{T_HOLD3_END/T_CYCLE:.4f};1"
    for b in range(N_BANDS):
        m = band_ids == b
        if not np.any(m):
            continue
        pts = [portrait_to_svg(r, c, scale, ox, oy) for r, c in dot_rc[m]]
        d = dot_run_path(pts)
        cy, cx = band_centroids[b]
        bx, by = portrait_to_svg(cy, cx, scale, ox, oy)
        dx = (python_centroid_svg[0] - bx) * 0.42
        dy = (python_centroid_svg[1] - by) * 0.42
        op_vals = "1;1;0;0;1"
        tr_vals = f"0,0;0,0;{dx:.1f},{dy:.1f};{dx:.1f},{dy:.1f};0,0"
        a(f'<g opacity="0"><path d="{d}" fill="{color}" shape-rendering="crispEdges"/>'
          f'<animate attributeName="opacity" values="{op_vals}" keyTimes="{key_times}" '
          f'begin="{LOOP_BEGIN}s" dur="{T_CYCLE}s" repeatCount="indefinite"/>'
          f'<animateTransform attributeName="transform" type="translate" values="{tr_vals}" '
          f'keyTimes="{key_times}" begin="{LOOP_BEGIN}s" dur="{T_CYCLE}s" repeatCount="indefinite"/></g>')
    a("</g>")
    return "".join(e)


def build_travelers_layer(py, pt, cv, scale, ox, oy, color):
    e = []
    a = e.append
    op_key = f"0;{T_HOLD0/T_CYCLE:.4f};{T_T1_END/T_CYCLE:.4f};{T_HOLD3_END/T_CYCLE:.4f};1"
    a(f'<g id="travelers" opacity="0">')
    a(f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{op_key}" '
      f'begin="{LOOP_BEGIN}s" dur="{T_CYCLE}s" repeatCount="indefinite"/>')
    pos_key = (f"0;{T_HOLD1_END/T_CYCLE:.4f};{T_T2_END/T_CYCLE:.4f};"
               f"{T_HOLD2_END/T_CYCLE:.4f};{T_T3_END/T_CYCLE:.4f};1")
    for i in range(len(py)):
        p1 = logo_to_svg(py[i, 0], py[i, 1], scale, ox, oy)
        p2 = logo_to_svg(pt[i, 0], pt[i, 1], scale, ox, oy)
        p3 = logo_to_svg(cv[i, 0], cv[i, 1], scale, ox, oy)
        vals = (f"{p1[0]:.0f},{p1[1]:.0f};{p1[0]:.0f},{p1[1]:.0f};{p2[0]:.0f},{p2[1]:.0f};"
                f"{p2[0]:.0f},{p2[1]:.0f};{p3[0]:.0f},{p3[1]:.0f};{p3[0]:.0f},{p3[1]:.0f}")
        a(f'<rect width="{TRAV_S:g}" height="{TRAV_S:g}" fill="{color}" shape-rendering="crispEdges">'
          f'<animateTransform attributeName="transform" type="translate" values="{vals}" '
          f'keyTimes="{pos_key}" begin="{LOOP_BEGIN}s" dur="{T_CYCLE}s" repeatCount="indefinite"/></rect>')
    a("</g>")
    return "".join(e)


def dotted_leader(n):
    return "." * max(3, n)


def build_info_rows(t):
    e = []
    a = e.append
    y = 162
    delay = 0.90
    for label, value in ROWS:
        if label == "__gap__":
            y += 31
            continue
        dots_n = ROW_TOTAL_CHARS - len(label) - len(value) - 2
        d = dotted_leader(dots_n)
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>'
          f'<text x="{INFO_X}" y="{y}" font-size="14" textLength="{ROW_TEXTLEN}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
          f'<tspan fill="{t["chrome"]}">{esc(label)} </tspan>'
          f'<tspan fill="{t["dots"]}">{d}</tspan>'
          f'<tspan fill="{t["text"]}" font-weight="600"> {esc(value)}</tspan></text></g>')
        y += 23
        delay += 0.12
    return "".join(e), y


def build_svg(theme_name, dots_bool, intro_rc, intro_gid, band_grid, band_centroids,
              trav_py, trav_pt, trav_cv):
    t = THEMES[theme_name]
    p_scale, p_ox, p_oy = make_portrait_transform()
    l_scale, l_ox, l_oy = make_logo_transform()

    first_logo_centroid_local = trav_py.mean(axis=0)  # (x,y) in raster space; "first logo" = LangChain
    first_logo_centroid_svg = (l_ox + first_logo_centroid_local[0] * l_scale,
                                l_oy + first_logo_centroid_local[1] * l_scale)

    intro_svg = build_intro_layer(intro_rc, intro_gid, p_scale, p_ox, p_oy, t["portrait"])
    loop_svg = build_loop_portrait_layer(np.column_stack(np.nonzero(dots_bool)), band_grid, band_centroids,
                                          p_scale, p_ox, p_oy, t["portrait"], first_logo_centroid_svg)
    trav_svg = build_travelers_layer(trav_py, trav_pt, trav_cv, l_scale, l_ox, l_oy, t["chrome"])

    info_rows_svg, _ = build_info_rows(t)

    parts = []
    a = parts.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,\'Liberation Mono\',monospace" '
      f'role="img" aria-label="Zia Ullah — profile.sh --live">')
    a("<defs>")
    a(f'<clipPath id="frameClip{theme_name}"><rect x="{FRAME_X}" y="{FRAME_Y}" width="{FRAME_W}" height="{FRAME_H}" rx="10"/></clipPath>')
    a(f'<clipPath id="winClip{theme_name}"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="18"/></clipPath>')
    a(f'<linearGradient id="accent{theme_name}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{t["portrait"]}"><animate attributeName="stop-color" '
      f'values="{t["portrait"]};{t["chrome"]};{t["accent"]};{t["portrait"]}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="0.5" stop-color="{t["chrome"]}"><animate attributeName="stop-color" '
      f'values="{t["chrome"]};{t["accent"]};{t["portrait"]};{t["chrome"]}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{t["accent"]}"><animate attributeName="stop-color" '
      f'values="{t["accent"]};{t["portrait"]};{t["chrome"]};{t["accent"]}" dur="10s" repeatCount="indefinite"/></stop>'
      f'</linearGradient>')
    a("</defs>")

    a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="18" fill="{t["win_bg"]}"/>')
    a(f'<g clip-path="url(#winClip{theme_name})">')
    a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="{t["panel"]}"/>')
    a(f'<rect x="2" y="2" width="{W-4}" height="46" fill="{t["panel_bar"]}"/>')
    a(f'<line x1="2" y1="48" x2="{W-2}" y2="48" stroke="{t["border_line"]}"/>')
    a('<circle cx="30" cy="25" r="5.5" fill="#ff5f56"/><circle cx="50" cy="25" r="5.5" fill="#ffbd2e"/>'
      '<circle cx="70" cy="25" r="5.5" fill="#27c93f"/>')
    a(f'<text x="590" y="29" text-anchor="middle" font-size="12" fill="{t["muted"]}">'
      f'ziaullahbj9@gmail.com - % ./profile.sh --live</text>')

    a(f'<text x="{FRAME_X+2}" y="74" font-size="10" letter-spacing="3" fill="{t["dim"]}">VISUAL.MAP</text>')
    a(f'<rect x="{FRAME_X}" y="{FRAME_Y}" width="{FRAME_W}" height="{FRAME_H}" rx="10" fill="none" '
      f'stroke="{t["portrait"]}" stroke-width="2" opacity="0.45"/>')
    a(f'<rect x="{FRAME_X}" y="{FRAME_Y}" width="{FRAME_W}" height="{FRAME_H}" rx="10" fill="{t["win_bg"]}" '
      f'stroke="{t["portrait"]}" stroke-opacity="0.35"/>')
    a(f'<g clip-path="url(#frameClip{theme_name})">')
    a(loop_svg)
    a(trav_svg)
    a(intro_svg)
    a("</g>")

    a(f'<text x="{INFO_X}" y="106" font-size="13" letter-spacing="2" fill="{t["chrome"]}">SYSTEM.INFO</text>')
    a(f'<line x1="{INFO_X+96}" y1="102" x2="{INFO_RIGHT}" y2="102" stroke="{t["border_line"]}"/>')
    a(f'<text x="{INFO_RIGHT}" y="106" text-anchor="end" font-size="12" fill="{t["live"]}" font-weight="700">'
      f'<tspan>&#9679;</tspan> LIVE<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></text>')
    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.6s" fill="freeze"/>'
      f'<rect x="{INFO_X}" y="122" width="245" height="20" rx="4" fill="{t["pill_bg"]}"/>'
      f'<text x="{INFO_X+9}" y="136" font-size="14" font-weight="700" fill="{t["pill_text"]}">@Engrziaullah</text></g>')

    a(info_rows_svg)

    a("</g>")
    a(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="17" fill="none" stroke="url(#accent{theme_name})" '
      f'stroke-width="1.6"/>')
    a("</svg>")
    return "".join(parts)


def main():
    dots_dark = np.load(os.path.join(HERE, "dots_dark.npy"))
    dots_light = np.load(os.path.join(HERE, "dots_light.npy"))
    intro_rc_dark = np.load(os.path.join(HERE, "intro_rc_dark.npy"))
    intro_gid_dark = np.load(os.path.join(HERE, "intro_gid_dark.npy"))
    intro_rc_light = np.load(os.path.join(HERE, "intro_rc_light.npy"))
    intro_gid_light = np.load(os.path.join(HERE, "intro_gid_light.npy"))
    band_grid = np.load(os.path.join(HERE, "band_grid.npy"))
    band_centroids = np.load(os.path.join(HERE, "band_centroids.npy"))
    trav_py = np.load(os.path.join(HERE, "traveler_langchain.npy"))
    trav_pt = np.load(os.path.join(HERE, "traveler_langgraph.npy"))
    trav_cv = np.load(os.path.join(HERE, "traveler_langsmith.npy"))

    os.makedirs(OUT_DIR, exist_ok=True)

    dark_svg = build_svg("dark", dots_dark, intro_rc_dark, intro_gid_dark, band_grid, band_centroids,
                          trav_py, trav_pt, trav_cv)
    light_svg = build_svg("light", dots_light, intro_rc_light, intro_gid_light, band_grid, band_centroids,
                           trav_py, trav_pt, trav_cv)

    dark_path = os.path.join(OUT_DIR, "dark.svg")
    light_path = os.path.join(OUT_DIR, "light.svg")
    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(light_svg)

    print(f"dark.svg  : {os.path.getsize(dark_path)/1024:.1f} KB")
    print(f"light.svg : {os.path.getsize(light_path)/1024:.1f} KB")


if __name__ == "__main__":
    main()
