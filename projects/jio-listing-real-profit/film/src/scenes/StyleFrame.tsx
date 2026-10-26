import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import * as THREE from 'three';
import {ThreeCanvas} from '../kit/three-canvas';
import {Finish} from '../kit/finish';
import {Env, Floor, Lights, Tower, Coin} from './Studio';
import {fontCss} from '../fonts.css';

const STEEL = new THREE.MeshPhysicalMaterial({color: '#7d8796', metalness: 1, roughness: 0.38, clearcoat: 0.3});
const STEEL_DARK = new THREE.MeshPhysicalMaterial({color: '#3a414d', metalness: 1, roughness: 0.45});

const Vault: React.FC<{p: [number, number, number]}> = ({p}) => (
  <group position={p} rotation={[0, -0.45, 0]}>
    <mesh material={STEEL_DARK} position={[0, 1.1, 0]} castShadow receiveShadow><boxGeometry args={[2.3, 2.2, 1.6]} /></mesh>
    <mesh material={STEEL} position={[0, 1.15, 0.82]} rotation={[Math.PI / 2, 0, 0]} castShadow><cylinderGeometry args={[0.85, 0.85, 0.12, 64]} /></mesh>
    <mesh material={STEEL_DARK} position={[0, 1.15, 0.9]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.18, 0.18, 0.1, 32]} /></mesh>
    {[0, 1, 2].map((k) => (
      <mesh key={k} material={STEEL} position={[0, 1.15, 0.95]} rotation={[0, 0, (k * Math.PI) / 3]}><boxGeometry args={[1.0, 0.07, 0.07]} /></mesh>
    ))}
    {/* open slot on top for coins */}
    <mesh position={[0, 2.21, 0]}><boxGeometry args={[1.2, 0.02, 0.18]} /><meshBasicMaterial color="#000" /></mesh>
  </group>
);

const Laser: React.FC<{y: number}> = ({y}) => (
  <group position={[0, y, 0]}>
    <mesh><boxGeometry args={[5, 0.012, 0.012]} /><meshBasicMaterial color="#ffffff" toneMapped={false} /></mesh>
    <mesh><boxGeometry args={[5, 0.05, 0.05]} /><meshBasicMaterial color="#ff2030" toneMapped={false} transparent opacity={0.55} blending={THREE.AdditiveBlending} /></mesh>
    <mesh><boxGeometry args={[5, 0.16, 0.16]} /><meshBasicMaterial color="#ff2030" toneMapped={false} transparent opacity={0.15} blending={THREE.AdditiveBlending} /></mesh>
  </group>
);

const label: React.CSSProperties = {fontFamily: 'P', fontWeight: 800, textAlign: 'center', position: 'absolute', left: 0, right: 0};

export const StyleFrame: React.FC<{beat: number}> = ({beat}) => {
  const fr = useCurrentFrame();
  const camPos: [number, number, number] = beat === 1 ? [0.5, 2.2, 10] : [0.9, 2.4, 11];
  return (
    <AbsoluteFill style={{background: '#05070c'}}>
      <style>{fontCss}</style>
      <Finish fr={fr} bloom={0.6}>
        <ThreeCanvas width={1080} height={1920} shadows camera={{fov: 34, position: camPos}} onCreated={({camera}) => camera.lookAt(beat === 1 ? 0 : 0.4, 2.0, 0)}>
          <Env />
          <Lights red={beat === 1 ? 0.8 : 0} />
          <Floor />
          {beat === 1 && <>
            <Tower n={38} seed="hero" />
            <group position={[-2.2, 0, -2.5]}><Tower n={18} seed="b1" /></group>
            <group position={[2.4, 0, -3.2]}><Tower n={26} seed="b2" /></group>
            <Coin p={[1.0, 0.04, 1.0]} r={[0, 0.4, 0]} />
          </>}
          {beat === 2 && <>
            <group position={[-1, 0, 0]}><Tower n={30} seed="hero" /></group>
            <group position={[-1, 0, 0]} rotation={[0, 0, -0.08]}>
              {Array.from({length: 8}, (_, i) => <Coin key={i} p={[0.55 + i * 0.22, 2.55 + i * 0.05 - i * i * 0.012, (i % 3) * 0.08]} r={[0.3 + i * 0.25, i, 0.5 + i * 0.3]} />)}
            </group>
            <Laser y={2.38} />
            <group scale={0.75}><Vault p={[2.6, 0, 0.2]} /></group>
          </>}
        </ThreeCanvas>
      </Finish>
      {beat === 1 && <>
        <div style={{...label, top: 300}}><span style={{background: 'rgba(255,40,50,.92)', color: '#fff', fontSize: 40, padding: '10px 28px', borderRadius: 40, letterSpacing: 3}}>⚠ JIO SHARES</span></div>
        <div style={{...label, top: 380, fontSize: 150, background: 'linear-gradient(180deg,#fff6d8,#f2c14e 55%,#b07a1c)', WebkitBackgroundClip: 'text', color: 'transparent', filter: 'drop-shadow(0 8px 24px rgba(0,0,0,.7))'}}>₹1,00,000</div>
      </>}
      {beat === 2 && <>
        <div style={{...label, top: 300, fontSize: 64, color: '#fff'}}>STCG 20% <span style={{color: '#ff4a55'}}>+ 4% cess</span></div>
        <div style={{...label, top: 390, fontSize: 150, color: '#ff4a55', textShadow: '0 8px 30px rgba(255,40,50,.5)'}}>−₹10,400</div>
        <div style={{position: 'absolute', left: 700, top: 1230, fontFamily: 'P', fontWeight: 800, fontSize: 70, color: '#e8edf5', letterSpacing: 8, textShadow: '0 4px 16px #000'}}>TAX</div>
      </>}
    </AbsoluteFill>
  );
};
