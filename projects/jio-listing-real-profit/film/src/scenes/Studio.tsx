import React, {useMemo} from 'react';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {random} from 'remotion';

export const GOLD = new THREE.MeshPhysicalMaterial({color: '#f2c14e', metalness: 1, roughness: 0.2, clearcoat: 0.6, clearcoatRoughness: 0.15});
export const GOLD_EDGE = new THREE.MeshPhysicalMaterial({color: '#c8902a', metalness: 1, roughness: 0.32});
const COIN_GEO = new THREE.CylinderGeometry(0.5, 0.5, 0.075, 64, 1);
// Reeded edge look: slightly smaller ridged ring
const RIM_GEO = new THREE.TorusGeometry(0.47, 0.012, 8, 64);

export const Env: React.FC = () => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.background = new THREE.Color('#05070c');
    (scene as any).environmentIntensity = 0.55;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = 1.05;
  }, [gl, scene]);
  return null;
};

export const Coin: React.FC<{p: [number, number, number]; r?: [number, number, number]}> = ({p, r = [0, 0, 0]}) => (
  <group position={p} rotation={r}>
    <mesh geometry={COIN_GEO} material={GOLD} castShadow receiveShadow />
    <mesh geometry={RIM_GEO} material={GOLD_EDGE} rotation={[Math.PI / 2, 0, 0]} position={[0, 0.039, 0]} />
  </group>
);

// A tower of n coins with seeded wobble. `base` = y of first coin.
export const Tower: React.FC<{n: number; x?: number; z?: number; seed: string; from?: number}> = ({n, x = 0, z = 0, seed, from = 0}) => {
  const coins = useMemo(() => Array.from({length: n}, (_, i) => ({
    dx: (random(`${seed}x${i}`) - 0.5) * 0.06, dz: (random(`${seed}z${i}`) - 0.5) * 0.06,
    ry: random(`${seed}r${i}`) * 6.28, tilt: (random(`${seed}t${i}`) - 0.5) * 0.03,
  })), [n, seed]);
  return <group>{coins.slice(from).map((c, k) => { const i = k + from; return <Coin key={i} p={[x + c.dx, 0.0375 + i * 0.078, z + c.dz]} r={[c.tilt, c.ry, c.tilt]} />; })}</group>;
};

export const Floor: React.FC = () => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
    <circleGeometry args={[14, 96]} />
    <meshPhysicalMaterial color="#080a10" metalness={0.1} roughness={0.32} clearcoat={0.8} clearcoatRoughness={0.2} specularIntensity={0.4} />
  </mesh>
);

export const Lights: React.FC<{red?: number}> = ({red = 0}) => (
  <>
    <spotLight position={[3, 8, 4]} angle={0.42} penumbra={0.8} intensity={260} color="#ffe2b0" castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0004} />
    <spotLight position={[-5, 4, -4]} angle={0.5} penumbra={1} intensity={140} color="#5d7cff" />
    <pointLight position={[0, 1.5, 3]} intensity={6} color="#ffd38a" />
    {red > 0 && <spotLight position={[-3, 6, 3]} angle={0.35} penumbra={0.6} intensity={300 * red} color="#ff2a2a" />}
  </>
);
