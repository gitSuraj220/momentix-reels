import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {ThreeCanvas} from '../kit/three-canvas';
import {Finish} from '../kit/finish';
import {Env, Floor, Coin} from './Studio';
import {fontCss} from '../fonts.css';
import CUES from '../cues.json';

export const FPS = 30;
type C = {id: string; who: string; w: string; s: number; e: number};
const CU = CUES as C[];
const S = (id: string) => CU.find((c) => c.id === id)!.s;
const E = (id: string) => CU.find((c) => c.id === id)!.e;
export const END = E('b6') + 1.6;
export const TOTAL = Math.round(END * FPS);

const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const inout = Easing.bezier(0.45, 0, 0.55, 1);
const pr = (t: number, a: number, d = 0.4, e = ease) => interpolate(t, [a, a + d], [0, 1], {...cl, easing: e});
const back = (k: number) => {k = Math.min(1, Math.max(0, k)); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2);};
const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
const inr = (n: number) => '₹' + Math.round(n).toLocaleString('en-IN');

// ---- timeline constants (seconds) ----
const T = {
  grow0: S('b2') + 0.4, grow1: E('b2') - 0.2, plus: S('b3'),
  freeze: S('ruko'), laser: S('m1'), tax: S('m2') + 0.3, slice: S('m3') - 0.1,
  fee: S('m5'), real: S('m6'), shatter: S('m7'), slam: S('m8'),
  cal: S('m9'), ltcg: S('m10') + 0.5, shield: S('m11'), open: S('m13') + 0.4, zero: S('m14'),
  plinth: S('b4') + 0.2, tip: S('b6') + 0.3,
};
const BASE = 24, EXTRA = 12, SLICE = 3;
const CH = 0.078; // coin pitch

// ---- materials ----
const STEEL = new THREE.MeshPhysicalMaterial({color: '#7d8796', metalness: 1, roughness: 0.38, clearcoat: 0.3});
const STEEL_DARK = new THREE.MeshPhysicalMaterial({color: '#262b34', metalness: 1, roughness: 0.42});
const MARBLE = new THREE.MeshPhysicalMaterial({color: '#151922', metalness: 0.2, roughness: 0.3, clearcoat: 1});

const coinWobble = (i: number) => ({dx: (random(`x${i}`) - 0.5) * 0.06, dz: (random(`z${i}`) - 0.5) * 0.06, ry: random(`r${i}`) * 6.28, tl: (random(`t${i}`) - 0.5) * 0.03});

// The hero tower: base coins + profit coins that drop in, then the top SLICE fly to the vault and one fee coin flicks away.
const Tower: React.FC<{t: number; vaultX: number}> = ({t, vaultX}) => {
  const els: React.ReactNode[] = [];
  for (let i = 0; i < BASE + EXTRA; i++) {
    const w = coinWobble(i);
    let y = 0.0375 + i * CH, x = w.dx, z = w.dz, rx = w.tl, rz = w.tl, ry = w.ry, show = true;
    if (i >= BASE) {
      const k = i - BASE, td = lerp(T.grow0, T.grow1, k / EXTRA);
      const f = pr(t, td, 0.32, Easing.in(Easing.quad));
      if (t < td) show = false;
      y += (1 - f) * 2.5;
      const bounce = Math.max(0, Math.sin((t - td - 0.32) * 18)) * Math.exp(-(t - td - 0.32) * 10) * 0.05;
      if (f >= 1) y += bounce;
      const sliceIdx = i - (BASE + EXTRA - SLICE); // top SLICE coins
      if (sliceIdx >= 0) {
        const ts = T.slice + sliceIdx * 0.09, k2 = pr(t, ts, 0.75, inout);
        if (k2 > 0) {
          const sx = x, sy = y, ex = vaultX, ey = 1.75;
          x = lerp(sx, ex, k2); z = lerp(z, 0.2, k2);
          y = lerp(sy, ey, k2) + Math.sin(k2 * Math.PI) * 0.9;
          rx += k2 * 7 + sliceIdx; rz += k2 * 4; if (k2 >= 1) show = false;
        }
      }
      if (i === BASE + EXTRA - SLICE - 1) { // fee coin: flicks away at T.fee
        const k3 = pr(t, T.fee + 0.25, 0.7, Easing.out(Easing.quad));
        if (k3 > 0) { x -= k3 * 3.0; y += Math.sin(k3 * Math.PI) * 0.8 - k3 * 1.0; z -= k3 * 2.5; rx += k3 * 9; if (k3 >= 1) show = false; }
      }
    }
    if (show) els.push(<Coin key={i} p={[x, y, z]} r={[rx, ry, rz]} />);
  }
  return <group>{els}</group>;
};

const Vault: React.FC<{x: number; open: number}> = ({x, open}) => (
  <group position={[x, 0, 0.2]} rotation={[0, -0.35, 0]} scale={0.8}>
    <mesh material={STEEL_DARK} position={[0, 1.1, 0]} castShadow receiveShadow><boxGeometry args={[2.3, 2.2, 1.6]} /></mesh>
    <mesh position={[0, 1.15, 0.79]}><cylinderGeometry args={[0.8, 0.8, 0.02, 64]} /><meshBasicMaterial color="#020203" /></mesh>
    <group position={[-0.85, 1.15, 0.82]} rotation={[0, -open * 1.9, 0]}>
      <group position={[0.85, 0, 0]}>
        <mesh material={STEEL} rotation={[Math.PI / 2, 0, 0]} castShadow><cylinderGeometry args={[0.85, 0.85, 0.12, 64]} /></mesh>
        <mesh material={STEEL_DARK} position={[0, 0, 0.08]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.18, 0.18, 0.1, 32]} /></mesh>
        {[0, 1, 2].map((k) => <mesh key={k} material={STEEL} position={[0, 0, 0.13]} rotation={[0, 0, (k * Math.PI) / 3 + open * 3]}><boxGeometry args={[1.0, 0.07, 0.07]} /></mesh>)}
      </group>
    </group>
    <mesh position={[0, 2.21, 0]}><boxGeometry args={[1.2, 0.02, 0.18]} /><meshBasicMaterial color="#000" /></mesh>
  </group>
);

const Laser: React.FC<{y: number; k: number; x: number}> = ({y, k, x}) => k <= 0 ? null : (
  <group position={[x, y, 0]} scale={[k, 1, 1]}>
    <mesh><boxGeometry args={[5, 0.012, 0.012]} /><meshBasicMaterial color="#ffffff" toneMapped={false} /></mesh>
    <mesh><boxGeometry args={[5, 0.05, 0.05]} /><meshBasicMaterial color="#ff2030" toneMapped={false} transparent opacity={0.55} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
    <mesh><boxGeometry args={[5, 0.18, 0.18]} /><meshBasicMaterial color="#ff2030" toneMapped={false} transparent opacity={0.14} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
  </group>
);

const Shield: React.FC<{k: number; h: number}> = ({k, h}) => k <= 0 ? null : (
  <group position={[0, 0, 0]} scale={[k, k, k]}>
    <mesh position={[0, h / 2, 0]}><cylinderGeometry args={[0.95, 0.95, h, 64, 1, true]} /><meshBasicMaterial color="#ffcf5a" transparent opacity={0.13} blending={THREE.AdditiveBlending} side={THREE.DoubleSide} depthWrite={false} toneMapped={false} /></mesh>
    {[0.05, h * 0.5, h].map((y, i) => <mesh key={i} position={[0, y, 0]} rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[0.95, 0.015, 8, 96]} /><meshBasicMaterial color="#ffe08a" toneMapped={false} /></mesh>)}
  </group>
);

const Plinth: React.FC<{t: number}> = ({t}) => {
  const roll = pr(t, T.plinth + 0.6, 1.6, inout);           // rolls across on its edge
  const fall = pr(t, T.tip, 0.55, Easing.in(Easing.quad));  // then tips over flat
  const bounce = Math.max(0, Math.sin((t - T.tip - 0.55) * 22)) * Math.exp(-(t - T.tip - 0.55) * 9) * 0.06;
  const x = lerp(-0.5, 0.15, roll) + fall * 0.25;
  const y = 1.16 + lerp(0.5, 0.04, fall) + (fall >= 1 ? bounce : 0);
  return (
    <group position={[-4.2, 0, 0.4]}>
      <mesh material={MARBLE} position={[0, 0.55, 0]} castShadow receiveShadow><cylinderGeometry args={[0.75, 0.85, 1.1, 64]} /></mesh>
      <mesh material={MARBLE} position={[0, 1.13, 0]}><cylinderGeometry args={[0.85, 0.85, 0.06, 64]} /></mesh>
      <group position={[x, y, 0.1]} rotation={[0, 0.25, 0]}>
        <group rotation={[0, 0, (1 - fall) * (Math.PI / 2)]}>
          <Coin p={[0, 0, 0]} r={[0, -roll * 6, 0]} />
        </group>
      </group>
    </group>
  );
};

const PlinthLight: React.FC<{i: number}> = ({i}) => {
  const tgt = useMemo(() => new THREE.Object3D(), []);
  return (<>
    <primitive object={tgt} position={[-4.2, 1.1, 0.4]} />
    <spotLight position={[-3.2, 5, 4]} target={tgt} angle={0.35} penumbra={0.7} intensity={i} color="#fff1d6" castShadow />
  </>);
};

// ---- camera keyframes ----
type K = [number, [number, number, number], [number, number, number]];
const CAMK = (): K[] => [
  [0, [0.2, 4.2, 12], [0, 2.2, 0]],
  [S('hook2'), [0.3, 2.5, 7.6], [0, 2.0, 0]],
  [S('b2'), [-0.3, 2.5, 7.6], [0, 2.0, 0]],
  [E('b3'), [-0.6, 2.8, 8.2], [0, 2.2, 0]],
  [T.laser, [0.5, 2.8, 9.0], [0.8, 2.1, 0]],
  [T.slice + 0.9, [1.0, 2.7, 9.4], [1.0, 2.0, 0]],
  [T.real, [0.2, 2.7, 7.8], [0.1, 2.1, 0]],
  [T.cal, [0.6, 2.7, 8.6], [0.6, 2.0, 0]],
  [T.open, [1.0, 2.5, 9.4], [1.0, 1.9, 0]],
  [T.plinth, [1.0, 2.5, 9.4], [1.0, 1.9, 0]],
  [T.plinth + 0.9, [-3.6, 2.7, 8.6], [-4.7, 1.55, 0]],
  [END, [-3.8, 2.5, 8.0], [-4.8, 1.5, 0]],
];
const camAt = (t: number) => {
  const ks = CAMK();
  let i = 0; while (i < ks.length - 2 && t > ks[i + 1][0]) i++;
  const [t0, p0, l0] = ks[i], [t1, p1, l1] = ks[i + 1];
  const k = inout(Math.min(1, Math.max(0, (t - t0) / Math.max(0.001, t1 - t0))));
  return {p: p0.map((v, j) => lerp(v, p1[j], k)), l: l0.map((v, j) => lerp(v, l1[j], k))};
};

const Cam: React.FC<{t: number}> = ({t}) => {
  const {camera} = useThree();
  const c = camAt(t);
  // impact shake
  const sh = [T.slice + 0.75, T.slam, T.zero].reduce((a, s) => a + Math.exp(-Math.pow((t - s) / 0.08, 2)), 0);
  camera.position.set(c.p[0] + Math.sin(t * 61) * 0.05 * sh, c.p[1] + Math.cos(t * 53) * 0.05 * sh, c.p[2]);
  camera.lookAt(c.l[0], c.l[1], c.l[2]);
  camera.updateProjectionMatrix();
  return null;
};

const Scene: React.FC<{t: number}> = ({t}) => {
  const {scene} = useThree();
  useMemo(() => { scene.fog = new THREE.Fog('#05070c', 13, 30); }, [scene]);
  const vaultX = interpolate(t, [T.laser - 0.2, T.laser + 0.7], [7, 2.5], {...cl, easing: ease});
  const red = Math.max(0, Math.sin(t * 7)) * (1 - pr(t, S('b1'), 0.4)) + 0.8 * Math.exp(-Math.pow((t - T.slice) / 0.6, 2));
  const growH = (BASE + EXTRA - SLICE) * CH;
  return (
    <>
      <Cam t={t} />
      <spotLight position={[3, 9, 5]} angle={0.45} penumbra={0.8} intensity={280} color="#ffe2b0" castShadow shadow-mapSize={[1024, 1024]} shadow-bias={-0.0004} />
      <spotLight position={[-6, 5, -4]} angle={0.55} penumbra={1} intensity={160} color="#5d7cff" />
      <pointLight position={[0, 1.6, 3]} intensity={5} color="#ffd38a" />
      <PlinthLight i={interpolate(t, [T.plinth, T.plinth + 0.8], [0, 260], cl)} />
      <spotLight position={[-3, 7, 3]} angle={0.4} penumbra={0.6} intensity={320 * red} color="#ff2a2a" />
      <Floor />
      <Tower t={t} vaultX={vaultX - 0.15} />
      {[[-2.4, -2.8, 16], [2.8, -3.6, 24], [-3.6, -6, 30]].map(([x, z, n], j) => (
        <group key={j} position={[x, 0, z]}>{Array.from({length: n}, (_, i) => { const w = coinWobble(i + 100 * j + 300); return <Coin key={i} p={[w.dx, 0.0375 + i * CH, w.dz]} r={[w.tl, w.ry, w.tl]} />; })}</group>
      ))}
      <Laser y={(BASE + EXTRA - SLICE) * CH + 0.02} x={0.6} k={pr(t, T.laser, 0.35) * (1 - pr(t, T.slice + 0.6, 0.3))} />
      <Vault x={vaultX} open={pr(t, T.open, 0.9, inout)} />
      <Shield k={back(pr(t, T.shield, 0.5)) * (1 - pr(t, T.plinth + 0.3, 0.4))} h={growH + 0.15} />
      <Plinth t={t} />
    </>
  );
};

// ---- HTML overlays ----
const F: React.CSSProperties = {fontFamily: 'P', fontWeight: 800, position: 'absolute', left: 0, right: 0, textAlign: 'center'};
const gold: React.CSSProperties = {background: 'linear-gradient(180deg,#fff6d8,#f2c14e 55%,#b07a1c)', WebkitBackgroundClip: 'text', color: 'transparent'};
const win = (t: number, a: number, b: number, fi = 0.25, fo = 0.25) => Math.min(pr(t, a, fi), 1 - pr(t, b - fo, fo));
const pop = (t: number, a: number) => back(pr(t, a, 0.35));

const Overlays: React.FC<{t: number}> = ({t}) => {
  // counter: 1,00,000 -> 1,50,000 while coins drop; then profit view
  const val = 100000 + 50000 * pr(t, T.grow0, T.grow1 - T.grow0, inout);
  const head1 = win(t, 0.05, T.freeze + 0.1);
  const profit = (() => {
    if (t < T.real) return 50000;
    return interpolate(t, [T.real + 0.4, T.real + 1.6], [50000, 39430], {...cl, easing: inout});
  })();
  const shardK = pr(t, T.shatter + 0.35, 0.6);
  return (
    <AbsoluteFill>
      {/* Beat A/B: shares + counter */}
      <div style={{...F, top: 270, opacity: head1}}>
        <span style={{background: t < S('b1') ? 'rgba(255,40,50,.92)' : 'rgba(30,180,90,.92)', color: '#fff', fontSize: 40, padding: '10px 28px', borderRadius: 40, letterSpacing: 3}}>{t < S('b1') ? '⚠ JIO SHARES' : '📈 LISTING +50%'}</span>
      </div>
      <div style={{...F, top: 345, fontSize: 150, ...gold, opacity: head1, filter: 'drop-shadow(0 8px 24px rgba(0,0,0,.7))', transform: `scale(${t < T.grow0 ? pop(t, 0.2) : 1 + 0.04 * Math.sin(t * 30) * (t < T.grow1 ? 1 : 0)})`}}>{inr(val)}</div>
      <div style={{...F, top: 545, fontSize: 96, color: '#3dff8f', textShadow: '0 0 30px rgba(61,255,143,.5)', opacity: win(t, T.plus, T.freeze + 0.1), transform: `translateY(${(1 - pr(t, T.plus, 0.4)) * 40}px) scale(${pop(t, T.plus)})`}}>+₹50,000</div>

      {/* Beat C: tax */}
      <div style={{...F, top: 280, fontSize: 64, color: '#fff', opacity: win(t, T.tax, T.real - 0.1)}}>STCG 20% <span style={{color: '#ff4a55'}}>+ 4% cess</span></div>
      <div style={{...F, top: 370, fontSize: 150, color: '#ff4a55', textShadow: '0 8px 30px rgba(255,40,50,.5)', opacity: win(t, T.slice + 0.6, T.fee - 0.05), transform: `scale(${pop(t, T.slice + 0.6)})`}}>−₹10,400</div>
      <div style={{...F, top: 380, fontSize: 120, color: '#ff8a55', opacity: win(t, T.fee + 0.2, T.real - 0.05), transform: `scale(${pop(t, T.fee + 0.2)})`}}>−₹170</div>
      <div style={{...F, top: 540, fontSize: 40, color: '#c8cdd6', opacity: win(t, T.fee + 0.2, T.real - 0.05), letterSpacing: 2}}>STT + CHARGES</div>

      {/* Beat E: real profit */}
      <div style={{...F, top: 260, fontSize: 48, color: '#c8cdd6', letterSpacing: 3, opacity: win(t, T.real, T.cal)}}>ASLI PROFIT</div>
      <div style={{...F, top: 320, fontSize: 150, ...gold, opacity: win(t, T.real, T.cal), filter: 'drop-shadow(0 8px 24px rgba(0,0,0,.7))'}}>{inr(profit)}</div>
      <div style={{...F, top: 520, height: 170, opacity: win(t, T.shatter, T.cal)}}>
        {/* 50% shatters into 4 shards */}
        {[0, 1, 2, 3].map((q) => (
          <div key={q} style={{position: 'absolute', left: 0, right: 0, fontSize: 150, color: '#ff4a55', clipPath: ['polygon(0 0,52% 0,45% 100%,0 100%)', 'polygon(52% 0,100% 0,100% 48%,47% 55%)', 'polygon(47% 55%,100% 48%,100% 100%,45% 100%)', 'polygon(0 0,0 0,0 0,0 0)'][q],
            transform: `translate(${(q === 0 ? -1 : 1) * shardK * 220 - 260}px, ${shardK * shardK * (300 + q * 120)}px) rotate(${(q - 1) * shardK * 40}deg)`, opacity: 1 - shardK}}>50%<span style={{position: 'absolute', left: '28%', right: '28%', top: '48%', height: 10, background: '#fff', opacity: pr(t, T.shatter, 0.2)}} /></div>
        ))}
        <div style={{position: 'absolute', left: 0, right: 0, fontSize: 170, color: '#ffd43b', textShadow: '0 0 40px rgba(255,212,59,.5)', transform: `translateX(220px) scale(${pr(t, T.slam, 0.01) * (2.2 - 1.2 * pr(t, T.slam, 0.18, Easing.in(Easing.quad)))})`, opacity: pr(t, T.slam, 0.05)}}>39%</div>
      </div>

      {/* Beat F: calendar, STCG vs LTCG, shield, zero */}
      {(() => {
        const o = win(t, T.cal, T.ltcg + 0.2);
        const page = Math.min(12, Math.floor(1 + pr(t, T.cal + 0.15, 1.1, Easing.in(Easing.quad)) * 12));
        return (
          <div style={{position: 'absolute', left: 340, top: 250, width: 400, height: 330, opacity: o, perspective: 900}}>
            <div style={{position: 'absolute', inset: 0, background: '#f4efe4', borderRadius: 26, boxShadow: '0 20px 60px rgba(0,0,0,.6)', overflow: 'hidden'}}>
              <div style={{height: 86, background: '#e33', color: '#fff', fontFamily: 'P', fontWeight: 800, fontSize: 44, textAlign: 'center', lineHeight: '86px', letterSpacing: 4}}>MAHINE</div>
              <div style={{fontFamily: 'P', fontWeight: 800, fontSize: 190, color: '#14161c', textAlign: 'center', lineHeight: '230px'}}>{page}{page === 12 ? '+' : ''}</div>
            </div>
          </div>
        );
      })()}
      <div style={{...F, top: 280, opacity: win(t, T.ltcg, T.shield + 0.1), display: 'flex', justifyContent: 'center', gap: 36}}>
        <div style={{fontSize: 70, color: '#ff4a55', position: 'relative', padding: '18px 34px', border: '5px solid #ff4a55', borderRadius: 26, opacity: 1 - 0.5 * pr(t, T.ltcg + 0.5, 0.3)}}>20%
          <div style={{position: 'absolute', left: 10, right: 10, top: '50%', height: 9, background: '#fff', transformOrigin: 'left', transform: `scaleX(${pr(t, T.ltcg + 0.4, 0.25)}) rotate(-12deg)`}} /></div>
        <div style={{fontSize: 70, color: '#3dff8f', padding: '18px 34px', border: '5px solid #3dff8f', borderRadius: 26, transform: `scale(${pop(t, T.ltcg + 0.6)})`}}>12.5%</div>
      </div>
      <div style={{...F, top: 430, fontSize: 40, color: '#c8cdd6', letterSpacing: 2, opacity: win(t, T.ltcg, T.shield + 0.1)}}>1 SAAL KE BAAD: LTCG</div>
      <div style={{...F, top: 270, fontSize: 56, ...gold, opacity: win(t, T.shield + 0.2, T.plinth), transform: `scale(${pop(t, T.shield + 0.2)})`}}>🛡 ₹1.25 LAKH / SAAL</div>
      <div style={{...F, top: 350, fontSize: 64, color: '#fff', opacity: win(t, T.shield + 0.2, T.plinth)}}>TAX-FREE</div>
      <div style={{...F, top: 440, fontSize: 170, color: '#3dff8f', textShadow: '0 0 40px rgba(61,255,143,.55)', opacity: win(t, T.zero - 0.05, T.plinth), transform: `scale(${pop(t, T.zero - 0.05)})`}}>TAX ₹0</div>
      <div style={{...F, top: 650, fontSize: 30, color: '#9aa1ad', opacity: win(t, T.zero, T.plinth)}}>price same rahe toh · example</div>

      {/* Beat G: not allotted */}
      <div style={{...F, top: 330, opacity: win(t, T.plinth + 0.9, END + 1)}}>
        <span style={{display: 'inline-block', fontSize: 74, color: '#ff4a55', border: '8px solid #ff4a55', borderRadius: 18, padding: '6px 30px', transform: `rotate(-8deg) scale(${lerp(2.4, 1, pr(t, S('b6') - 0.1, 0.16, Easing.in(Easing.quad)))})`, opacity: pr(t, S('b6') - 0.1, 0.05), background: 'rgba(5,7,12,.6)'}}>NOT ALLOTTED</span>
      </div>
      <div style={{...F, top: 500, fontSize: 120, color: '#3dff8f', opacity: win(t, S('b5') + 0.5, END + 1), transform: `scale(${pop(t, S('b5') + 0.5)})`}}>TAX ₹0 😅</div>
    </AbsoluteFill>
  );
};

// ---- captions: phrase at a time, bottom safe area ----
const HI = /(₹[\d,.]+(?: lakh)?|\d+(?:\.\d+)?%|zero!?|loss|tax-free|Jio)/gi;
const HI1 = /^(₹[\d,.]+(?: lakh)?|\d+(?:\.\d+)?%|zero!?|loss|tax-free|Jio)$/i;
const Caption: React.FC<{t: number}> = ({t}) => {
  const c = CU.find((x) => t >= x.s - 0.05 && t < x.e + 0.18);
  if (!c) return null;
  const k = pr(t, c.s - 0.05, 0.14);
  const parts = c.w.split(HI).filter((p) => p !== undefined && p !== '');
  return (
    <div style={{position: 'absolute', left: 60, right: 60, top: 1330, textAlign: 'center', transform: `scale(${0.86 + 0.14 * back(k)})`, opacity: k}}>
      <span style={{display: 'inline-block', background: c.who === 'bunty' ? 'rgba(20,90,60,.88)' : 'rgba(12,14,20,.88)', borderRadius: 28, padding: '14px 30px', fontFamily: 'P', fontWeight: 800, fontSize: 56, lineHeight: 1.25, color: '#fff', boxShadow: '0 10px 30px rgba(0,0,0,.5)'}}>
        {parts.map((p, i) => <span key={i} style={{color: HI1.test(p) ? '#FFD43B' : '#fff'}}>{p}</span>)}
      </span>
      <div style={{fontFamily: 'P', fontWeight: 700, fontSize: 26, color: c.who === 'bunty' ? '#7dffb4' : '#9fb4ff', marginTop: 10, letterSpacing: 3}}>{c.who === 'bunty' ? 'BUNTY' : 'MOMO'}</div>
    </div>
  );
};

export const Film: React.FC<{captions?: boolean; audio?: boolean}> = ({captions = true, audio = true}) => {
  const fr = useCurrentFrame();
  const t = fr / FPS;
  const flash = Math.exp(-Math.pow((t - (T.slice + 0.75)) / 0.06, 2)) * 0.35 + Math.exp(-Math.pow((t - T.slam) / 0.05, 2)) * 0.25;
  return (
    <AbsoluteFill style={{background: '#05070c'}}>
      <style>{fontCss}</style>
      <Finish fr={fr} bloom={0.55}>
        <ThreeCanvas width={1080} height={1920} shadows camera={{fov: 34, position: [0, 3, 12], near: 0.1, far: 60}}>
          <Env />
          <Scene t={t} />
        </ThreeCanvas>
      </Finish>
      <Overlays t={t} />
      {captions && <Caption t={t} />}
      <AbsoluteFill style={{background: '#fff', opacity: flash, pointerEvents: 'none'}} />
      <div style={{position: 'absolute', right: 46, top: 70, fontFamily: 'P', fontWeight: 700, fontSize: 28, color: 'rgba(255,255,255,.75)', letterSpacing: 2}}>MOMENTIX</div>
      {audio && <Audio src={staticFile('mix.wav')} />}
    </AbsoluteFill>
  );
};
