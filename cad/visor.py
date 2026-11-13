"""Visor 3D en el navegador para revisar el diseño antes de exportar STL.

Uso:
  .venv\\Scripts\\python.exe -m cad.visor [S150-A12.5]              ensamble de una configuración
  .venv\\Scripts\\python.exe -m cad.visor taller.separador_ender3   piezas de una carpeta de taller

Escribe un solo archivo HTML (salidas/<código>/visor.html o taller/<pieza>/salidas/visor.html)
con la geometría dentro: se abre con doble clic. Girar, acercar, vistas estándar, ocultar
piezas, corte por un plano y medir entre dos puntos en mm. three.js se carga de jsDelivr,
así que la primera vez hace falta internet.
"""
import base64
import html
import importlib
import json
import math
import sys
import tempfile
import time
from pathlib import Path

from build123d import Color, Compound, Location, export_gltf

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ("#2459B8", "#C2570F", "#2E7D4F", "#7A3FB0", "#B8932A", "#2E3338")


def _glb(shape, name, color):
    """glTF binario de una pieza. Pasa por una carpeta temporal por la «ñ» de la ruta.

    export_gltf gira la raíz a Y arriba con `location *= giro`, que no gira la traslación
    de una pieza colocada con Location: se envuelve en un Compound de raíz neutra."""
    shape = shape.moved(Location())   # copia: no cambia la etiqueta ni el color del original
    shape.label = name
    shape.color = Color(color)
    root = Compound(children=[shape], label=name)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "pieza.glb"
        if not export_gltf(root, str(path), binary=True, linear_deflection=0.02, angular_deflection=0.15):
            raise RuntimeError(f"No se pudo exportar {name} a glTF")
        return path.read_bytes()


def write(parts, dest, title, notes=(), lines=(), points=(), panel=True, subtitle="", share=None):
    """parts: [(nombre, grupo, color, shape)]; lines: [((x,y,z), (x,y,z), color)];
    points: [((x,y,z), color, etiqueta)]. Todo en mm, marco del modelo (Z arriba).
    panel=False: solo el modelo a pantalla completa, con el título encima (para compartir).
    share: ruta opcional de una copia sin <html>/<head>/<body> para publicarla como página."""
    data = []
    for name, group, color, shape in parts:
        bb = shape.bounding_box()
        data.append({"name": name, "group": group, "color": color,
                     "size": [bb.size.X, bb.size.Y, bb.size.Z],
                     "glb": base64.b64encode(_glb(shape, name, color)).decode("ascii")})
    payload = {"title": title, "notes": list(notes), "parts": data,
               "lines": [[list(a), list(b), c] for a, b, c in lines],
               "points": [[list(p), c, t] for p, c, t in points],
               "stamp": time.strftime("%Y-%m-%d %H:%M")}
    page = (TEMPLATE.replace("__TITLE__", html.escape(title)).replace("__SUBTITLE__", html.escape(subtitle))
            .replace("__MODE__", "" if panel else "solo").replace("__ASIDE__", "" if panel else "hidden")
            .replace("__NAME__", "hidden" if panel else "")
            .replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    if share:
        body = page
        for tag in ("<!doctype html>\n", '<html lang="es"><head>', "</head><body>", "</body></html>"):
            body = body.replace(tag, "", 1)
        Path(share).parent.mkdir(parents=True, exist_ok=True)
        Path(share).write_text(body, encoding="utf-8")
    return dest


def config_parts(code=None):
    from cad import ensamble
    from cad import params as P
    from cad.exportar import COLORS, parse
    sep, ang = parse(code) if code else P.PRESENTATION_CONFIG
    code = ensamble.config_code(sep, ang)
    items = ensamble.build(sep, ang)
    parts = [(it.name, it.role, COLORS[it.role], it.part) for it in items]
    axes = ensamble.camera_axes(sep, ang)
    cross, _ = ensamble.axes_crossing(sep, ang)
    lines = [(tuple(p), tuple(p + u * (p.Z / -u.Z)), COLORS[f"cámara {k + 1}"]) for k, (p, u) in enumerate(axes)]
    (p1, _), (p2, _) = axes
    notes = [f"Carros en las marcas ±{sep / 2:.1f} mm",
             f"Separación entre centros de lente: {p2.X - p1.X:.2f} mm",
             f"Cuña por cámara: {ang:.1f}° (convergencia {2 * ang:.1f}°)",
             f"Lentes a {p1.Z:.1f} mm sobre Marker0"]
    points = []
    if cross is not None:
        notes.append(f"Cruce de ejes a {cross.Z:.1f} mm sobre Marker0")
        points.append((tuple(cross), "#B4361C", "cruce de ejes"))
    dest = ROOT / "salidas" / code / "visor.html"
    return parts, dest, f"Barra estéreo — {code}", notes, lines, points


def taller_parts(module):
    modelo = importlib.import_module(f"{module}.modelo")
    shapes = modelo.variants()
    parts, x = [], 0.0
    for k, s in enumerate(shapes):
        bb = s.bounding_box()
        placed = Location((x - bb.min.X, -bb.center().Y, -bb.min.Z)) * s
        x += bb.size.X + max(6.0, 0.3 * bb.size.X)
        parts.append((s.label, "pieza", PALETTE[k % len(PALETTE)], placed))
    notes = [f"{s.label}: {s.bounding_box().size.X:.2f} × {s.bounding_box().size.Y:.2f} × "
             f"{s.bounding_box().size.Z:.2f} mm (caja envolvente X × Y × Z)" for s in shapes]
    dest = ROOT.joinpath(*module.split(".")) / "salidas" / "visor.html"
    return parts, dest, module.split(".")[-1], notes, (), ()


def main(arg=None):
    t0 = time.time()
    spec = taller_parts(arg) if arg and arg.startswith("taller.") else config_parts(arg)
    parts, dest, title, notes, lines, points = spec
    write(parts, dest, title, notes, lines, points)
    print(f"{len(parts)} piezas en {time.time() - t0:.1f} s -> {dest}")
    return dest


TEMPLATE = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#F4F3EF;--panel:#FFFFFF;--ink:#15202A;--mute:#5B6670;--line:#D9D6CE;--acc:#B4361C;--edge:#1A1F24}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#16191C;--panel:#1F2327;--ink:#E7E9EB;--mute:#9AA4AD;--line:#343A40;--acc:#F07A5A;--edge:#0B0D0F;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#16191C;--panel:#1F2327;--ink:#E7E9EB;--mute:#9AA4AD;--line:#343A40;--acc:#F07A5A;--edge:#0B0D0F;color-scheme:dark}
[hidden]{display:none!important}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font:13px/1.4 system-ui,Segoe UI,sans-serif}
#app{display:grid;grid-template-columns:300px 1fr;height:100%}
aside{background:var(--panel);border-right:1px solid var(--line);overflow:auto;padding:14px}
h1{font-size:15px;margin:0 0 4px}small{color:var(--mute)}
h2{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);margin:16px 0 6px}
ul{list-style:none;margin:0;padding:0}li{display:flex;align-items:center;gap:6px;padding:2px 0;cursor:default}
li .sw{width:10px;height:10px;border-radius:2px;flex:none}li label{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
li button{font-size:10px;padding:0 5px}
.notes li{display:block;color:var(--ink)}
button,select{background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:3px 8px;font:inherit;cursor:pointer}
button.on{border-color:var(--acc);color:var(--acc)}
.row{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}
#view{position:relative;overflow:hidden}canvas{display:block}
#hud{position:absolute;left:12px;bottom:12px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:6px 10px;min-height:20px;max-width:70%;white-space:pre}
#tip{position:absolute;pointer-events:none;background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:2px 6px;display:none}
input[type=range]{width:100%}
@media (max-width:760px){#app{grid-template-columns:1fr;grid-template-rows:40% 60%}aside{border-right:0;border-bottom:1px solid var(--line)}}
#app.solo{grid-template-columns:1fr;grid-template-rows:1fr}
#name{position:absolute;top:calc(14px + env(safe-area-inset-top,0px));left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));pointer-events:none;display:flex;flex-direction:column;gap:2px}
#name b{font-size:17px;letter-spacing:.01em;text-wrap:balance}#name span{color:var(--mute);font-variant-numeric:tabular-nums}
#app.solo #hud{left:max(12px,env(safe-area-inset-left,0px));bottom:calc(12px + env(safe-area-inset-bottom,0px));color:var(--mute);font-size:12px;white-space:normal}
</style></head><body><div id="app" class="__MODE__">
<aside __ASIDE__>
<h1 id="ttl"></h1><small id="stamp"></small>
<h2>Datos del modelo</h2><ul class="notes" id="notes"></ul>
<h2>Vista</h2>
<div class="row"><button data-v="iso">Iso</button><button data-v="front">Frente (−Y)</button><button data-v="top">Arriba</button><button data-v="side">Lado (+X)</button></div>
<div class="row"><button id="ortho">Ortogonal</button><button id="edges" class="on">Aristas</button><button id="axes">Ejes XYZ</button></div>
<h2>Medir</h2>
<div class="row"><button id="measure">Medir 2 puntos</button><button id="clear">Borrar medidas</button></div>
<h2>Corte</h2>
<div class="row"><select id="cutAxis"><option value="">Sin corte</option><option>X</option><option>Y</option><option>Z</option></select><button id="flip">Invertir</button></div>
<input type="range" id="cut" min="0" max="1000" value="500" disabled>
<h2>Piezas</h2><div class="row"><button id="all">Todas</button></div><ul id="parts"></ul>
</aside>
<div id="view"><div id="name" __NAME__><b>__TITLE__</b><span>__SUBTITLE__</span></div><div id="hud">Arrastra para girar · rueda para acercar · botón derecho para mover · pasa el ratón sobre una pieza para ver su nombre</div><div id="tip"></div></div>
</div>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
const D = JSON.parse(document.getElementById('data').textContent);
const $ = s => document.querySelector(s);
$('#ttl').textContent = D.title; $('#stamp').textContent = 'Generado ' + D.stamp;
for (const n of D.notes) { const li = document.createElement('li'); li.textContent = n; $('#notes').append(li); }
if (!D.notes.length) $('#notes').innerHTML = '<li>—</li>';

const view = $('#view');
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setPixelRatio(devicePixelRatio); renderer.localClippingEnabled = true;
view.prepend(renderer.domElement);
const css = getComputedStyle(document.documentElement), tok = n => css.getPropertyValue(n).trim();
const scene = new THREE.Scene(); scene.background = new THREE.Color(tok('--bg') || '#F4F3EF');
scene.add(new THREE.HemisphereLight(0xffffff, 0x666666, 1.6));
const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(1, -2, 3); scene.add(sun);
const world = new THREE.Group(); scene.add(world);   // marco del modelo: mm, Z arriba
const persp = new THREE.PerspectiveCamera(35, 1, 0.1, 1e5), ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, -1e5, 1e5);
for (const c of [persp, ortho]) c.up.set(0, 0, 1);
let cam = persp; const controls = new OrbitControls(cam, renderer.domElement);
const clip = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0); let clipOn = false, clipSign = 1;

const loader = new GLTFLoader(), entries = [];
function b64(s) { const b = atob(s), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u.buffer; }
const edgeMat = new THREE.LineBasicMaterial({color: tok('--edge') || '#1A1F24', transparent: true, opacity: .55, clippingPlanes: [clip]});
for (const p of D.parts) {
  const gltf = await loader.parseAsync(b64(p.glb), '');
  const g = gltf.scene; g.rotation.x = Math.PI / 2;     // glTF es Y arriba; el modelo, Z arriba
  const holder = new THREE.Group(); holder.add(g); world.add(holder); holder.updateMatrixWorld(true);
  const bb = new THREE.Box3().setFromObject(holder), s = new THREE.Vector3(); bb.getSize(s);
  const k = p.size[0] > 1e-6 && s.x > 1e-9 ? p.size[0] / s.x : (p.size[2] / Math.max(s.z, 1e-9));
  holder.scale.setScalar(isFinite(k) && k > 0 ? k : 1);   // el glTF viene en metros: se vuelve a mm
  const isBox = p.group === 'caja';
  g.traverse(o => { if (o.isMesh) {
    o.material = new THREE.MeshStandardMaterial({color: p.color, roughness: .6, metalness: p.group === 'aluminio' ? .4 : 0,
      transparent: isBox, opacity: isBox ? .18 : 1, depthWrite: !isBox, side: THREE.DoubleSide, clippingPlanes: [clip]});
    o.userData.part = p.name;
    if (!isBox) o.add(new THREE.LineSegments(new THREE.EdgesGeometry(o.geometry, 25), edgeMat));
  }});
  entries.push({p, holder});
}
const lineMat = c => new THREE.LineBasicMaterial({color: c});
for (const [a, b, c] of D.lines) world.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...a), new THREE.Vector3(...b)]), lineMat(c)));
for (const [p, c] of D.points) { const m = new THREE.Mesh(new THREE.SphereGeometry(4), new THREE.MeshBasicMaterial({color: c})); m.position.set(...p); world.add(m); }

const box = new THREE.Box3().setFromObject(world), center = box.getCenter(new THREE.Vector3()), size = box.getSize(new THREE.Vector3());
const R = Math.max(size.x, size.y, size.z) || 10;
const axesHelper = new THREE.AxesHelper(R * .25); axesHelper.visible = false; world.add(axesHelper);
const dirs = {iso: [1, -1.2, .9], front: [0, -1, 0.0001], top: [0, -0.0001, 1], side: [1, 0, 0.0001]};
function setView(v) {
  const d = new THREE.Vector3(...dirs[v]).normalize();
  for (const c of [persp, ortho]) { c.position.copy(center).addScaledVector(d, R * 2.2); c.lookAt(center); }
  ortho.zoom = 1; ortho.updateProjectionMatrix(); controls.target.copy(center); controls.update();
}
function resize() {
  const w = view.clientWidth, h = view.clientHeight, a = w / h; renderer.setSize(w, h);
  persp.aspect = a; persp.updateProjectionMatrix();
  const hh = R * .75; Object.assign(ortho, {left: -hh * a, right: hh * a, top: hh, bottom: -hh}); ortho.updateProjectionMatrix();
}
addEventListener('resize', resize); resize(); setView('iso');
document.querySelectorAll('[data-v]').forEach(b => b.onclick = () => setView(b.dataset.v));
$('#ortho').onclick = e => {
  const next = cam === persp ? ortho : persp; next.position.copy(cam.position); next.quaternion.copy(cam.quaternion);
  cam = next; controls.object = cam; controls.update(); e.target.classList.toggle('on', cam === ortho);
};
$('#edges').onclick = e => { edgeMat.visible = !edgeMat.visible; e.target.classList.toggle('on', edgeMat.visible); };
$('#axes').onclick = e => { axesHelper.visible = !axesHelper.visible; e.target.classList.toggle('on', axesHelper.visible); };

// piezas
const groups = {};
for (const e of entries) (groups[e.p.group] ??= []).push(e);
for (const [g, list] of Object.entries(groups)) {
  const h = document.createElement('li'); h.innerHTML = `<b>${g}</b>`; $('#parts').append(h);
  for (const e of list) {
    const li = document.createElement('li');
    li.innerHTML = `<input type="checkbox" checked><span class="sw" style="background:${e.p.color}"></span><label title="${e.p.name}">${e.p.name}</label><button>solo</button>`;
    const cb = li.querySelector('input'); e.cb = cb;
    cb.onchange = () => e.holder.visible = cb.checked;
    li.querySelector('button').onclick = () => { for (const o of entries) { o.holder.visible = o === e; o.cb.checked = o === e; } };
    $('#parts').append(li);
  }
}
$('#all').onclick = () => { for (const o of entries) { o.holder.visible = true; o.cb.checked = true; } };

// corte
function updateClip() {
  const ax = $('#cutAxis').value; clipOn = !!ax; $('#cut').disabled = !clipOn;
  if (!clipOn) { clip.normal.set(0, 0, 0); clip.constant = 1; return; }
  const i = 'XYZ'.indexOf(ax), lo = box.min.getComponent(i), hi = box.max.getComponent(i);
  const v = lo + (hi - lo) * $('#cut').value / 1000, n = new THREE.Vector3(); n.setComponent(i, -clipSign);
  clip.normal.copy(n); clip.constant = clipSign * v;
  $('#hud').textContent = `Corte en ${ax} = ${v.toFixed(2)} mm`;
}
$('#cutAxis').onchange = updateClip; $('#cut').oninput = updateClip; $('#flip').onclick = () => { clipSign *= -1; updateClip(); };
updateClip();

// medir y nombre bajo el ratón
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2(), marks = new THREE.Group(); world.add(marks);
let measuring = false, first = null;
function pick(ev) {
  const r = renderer.domElement.getBoundingClientRect();
  mouse.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(mouse, cam);
  const vis = entries.filter(e => e.holder.visible && e.p.group !== 'caja').map(e => e.holder);
  return ray.intersectObjects(vis, true).find(h => h.object.isMesh && (!clipOn || clip.distanceToPoint(h.point) >= 0));
}
renderer.domElement.addEventListener('pointermove', ev => {
  const h = pick(ev), tip = $('#tip');
  if (!h) { tip.style.display = 'none'; return; }
  let o = h.object; while (o && !o.userData.part) o = o.parent;
  const r = view.getBoundingClientRect(), p = h.point;
  tip.textContent = `${o ? o.userData.part : ''}  (${p.x.toFixed(1)}, ${p.y.toFixed(1)}, ${p.z.toFixed(1)})`;
  Object.assign(tip.style, {display: 'block', left: ev.clientX - r.left + 14 + 'px', top: ev.clientY - r.top + 10 + 'px'});
});
let down = null;
renderer.domElement.addEventListener('pointerdown', ev => down = [ev.clientX, ev.clientY]);
renderer.domElement.addEventListener('pointerup', ev => {
  if (!measuring || !down || Math.hypot(ev.clientX - down[0], ev.clientY - down[1]) > 4) return;
  const h = pick(ev); if (!h) return;
  const dot = new THREE.Mesh(new THREE.SphereGeometry(R * .006), new THREE.MeshBasicMaterial({color: 0xB4361C, depthTest: false}));
  dot.position.copy(h.point); dot.renderOrder = 9; marks.add(dot);
  if (!first) { first = h.point.clone(); $('#hud').textContent = 'Punto 1 fijado; haz clic en el punto 2'; return; }
  const a = first, b = h.point, d = b.clone().sub(a);
  const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints([a, b]), new THREE.LineBasicMaterial({color: 0xB4361C, depthTest: false}));
  l.renderOrder = 9; marks.add(l);
  $('#hud').textContent = `Distancia ${d.length().toFixed(2)} mm\nΔX ${d.x.toFixed(2)}   ΔY ${d.y.toFixed(2)}   ΔZ ${d.z.toFixed(2)} mm`;
  first = null;
});
$('#measure').onclick = e => { measuring = !measuring; first = null; e.target.classList.toggle('on', measuring);
  $('#hud').textContent = measuring ? 'Medir: clic en el punto 1 (la medida es sobre la malla, ± la tolerancia de teselado 0.02 mm)' : ''; };
$('#clear').onclick = () => { marks.clear(); first = null; $('#hud').textContent = ''; };

renderer.setAnimationLoop(() => renderer.render(scene, cam));
</script>
<script type="application/json" id="data">__DATA__</script>
</body></html>
"""

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
