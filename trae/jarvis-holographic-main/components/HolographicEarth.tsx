import React, { useRef, useMemo, useState, useEffect } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { TextureLoader, Mesh, AdditiveBlending, DoubleSide, Group, BufferAttribute, Vector3, PlaneGeometry } from 'three';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import { Points, PointMaterial, Text } from '@react-three/drei';
import * as random from 'maath/random/dist/maath-random.esm';
import { HandTrackingState, RegionName } from '../types';
import { SoundService } from '../services/soundService';

interface HolographicEarthProps {
  handTrackingRef: React.MutableRefObject<HandTrackingState>;
  setRegion: (region: RegionName) => void;
}

// --- Tactical Terrain Component (Iron Man HUD Style) ---
const TerrainModel: React.FC<{ 
    expansionRef: React.MutableRefObject<number>;
    handTrackingRef: React.MutableRefObject<HandTrackingState>;
}> = ({ expansionRef, handTrackingRef }) => {
    const groupRef = useRef<Group>(null);
    const tiltRef = useRef<Group>(null);
    const spinRef = useRef<Group>(null);
    const meshRef = useRef<Mesh>(null);
    const fillMeshRef = useRef<Mesh>(null);
    const markersRef = useRef<Group>(null);
    const ringRef = useRef<Mesh>(null);

    const [terrainData, setTerrainData] = useState<{
        geometry: PlaneGeometry;
        maxHeights: Float32Array;
    } | null>(null);

    // 1. Generate Height Map Data (REAL WORLD DATA - Mount Fuji)
    useEffect(() => {
        const width = 12;
        const depth = 12;
        const segments = 128; // Higher resolution for real terrain
        
        const geom = new PlaneGeometry(width, depth, segments, segments);
        
        // Safety check for attributes
        if (!geom.attributes.position) {
            console.error("PlaneGeometry attributes missing");
            return;
        }

        const count = geom.attributes.position.count;
        const posArray = geom.attributes.position.array;
        const maxHeights = new Float32Array(count);
        const colorArray = new Float32Array(count * 3);

        // Fallback Generator (Procedural)
        const generateProcedural = () => {
             console.warn("Generating Procedural Terrain (Fallback)");
             
             // Simple FBM-like noise function for terrain shape
            const getElevation = (x: number, y: number) => {
                let z = Math.sin(x * 0.4) * Math.cos(y * 0.4) * 1.5; 
                z += Math.sin(x * 1.5 + y * 0.8) * 0.5;
                z += Math.cos(x * 2.0) * 0.2;
                return Math.max(-0.5, z); 
            };

            for (let i = 0; i < count; i++) {
                const x = posArray[i * 3];
                const y = posArray[i * 3 + 1]; 
                
                const h = getElevation(x, y);
                maxHeights[i] = h > 0 ? h : h * 0.2; 

                const intensity = 0.2 + (h + 1) / 3;
                colorArray[i*3] = 0;   
                colorArray[i*3+1] = intensity * 0.8; 
                colorArray[i*3+2] = intensity * 1.0; 
            }
            
            geom.setAttribute('color', new BufferAttribute(colorArray, 3));
            setTerrainData({ geometry: geom, maxHeights });
        };

        // Mount Fuji Tile Coordinates (Zoom 11)
        // Lat: 35.3606, Lon: 138.7274
        // x=1813, y=809 (Approximate for Z11)
        // Using AWS Terrain Tiles (Terrarium Format)
        // Format: (R * 256 + G + B / 256) - 32768
        const tileUrl = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/11/1813/809.png';

        // Load Image and Process
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.src = tileUrl;

        // Add timeout protection
        const timeoutId = setTimeout(() => {
            console.warn("Terrain image load timed out");
            img.src = ""; // Cancel load
            generateProcedural();
        }, 3000); // 3 seconds timeout

        img.onload = () => {
            clearTimeout(timeoutId);
            try {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                if (!ctx) {
                    generateProcedural();
                    return;
                }

                ctx.drawImage(img, 0, 0);
                const imgData = ctx.getImageData(0, 0, img.width, img.height);
                const pixels = imgData.data;

                // Map image pixels to geometry vertices
                // The plane geometry UVs map 0..1 to the image
                // We need to loop through vertices and sample the image
                
                // PlaneGeometry vertices are ordered row by row
                // (segments + 1) vertices per row
                const gridX = segments + 1;
                const gridY = segments + 1;

                let minH = Infinity;
                let maxH = -Infinity;

                for (let i = 0; i < count; i++) {
                    // Calculate UV coordinates for this vertex
                    const col = i % gridX;
                    const row = Math.floor(i / gridX);
                    
                    // UVs (0 to 1)
                    const u = col / segments;
                    const v = 1 - (row / segments); // Flip Y because canvas 0,0 is top-left

                    // Sample pixel
                    const px = Math.floor(u * (img.width - 1));
                    const py = Math.floor(v * (img.height - 1));
                    const idx = (py * img.width + px) * 4;

                    const r = pixels[idx];
                    const g = pixels[idx + 1];
                    const b = pixels[idx + 2];

                    // Decode Height (Terrarium format) in meters
                    const elevation = (r * 256 + g + b / 256) - 32768;

                    // Scale down for 3D scene (e.g., 1000m -> 1 unit)
                    // Mount Fuji is ~3776m
                    // We want it to be maybe 2-3 units high in our scene
                    const sceneHeight = elevation * 0.0005; // Scaling factor
                    
                    maxHeights[i] = sceneHeight;

                    if (sceneHeight < minH) minH = sceneHeight;
                    if (sceneHeight > maxH) maxH = sceneHeight;
                }

                // Normalize heights relative to base (so it's not floating too high/low)
                // And Apply Colors
                for (let i = 0; i < count; i++) {
                    // Adjust height to be relative to the lowest point in the tile
                    // But keep some "base" thickness
                    const relativeH = maxHeights[i] - minH;
                    maxHeights[i] = relativeH;

                    // Color Logic based on Real Height
                    // Peaks (High) -> White/Cyan (Snow/Tech)
                    // Mid -> Blue/Green
                    // Low -> Dark Blue
                    const normalizedH = (relativeH) / (maxH - minH); // 0 to 1
                    
                    if (normalizedH > 0.8) {
                        // Peak (Snow/Ice)
                        colorArray[i*3] = 0.8;
                        colorArray[i*3+1] = 1.0;
                        colorArray[i*3+2] = 1.0;
                    } else if (normalizedH > 0.4) {
                        // Mid (Mountain body)
                        colorArray[i*3] = 0;
                        colorArray[i*3+1] = 0.5 + normalizedH * 0.5;
                        colorArray[i*3+2] = 0.8;
                    } else {
                        // Base
                        colorArray[i*3] = 0;
                        colorArray[i*3+1] = 0.2;
                        colorArray[i*3+2] = 0.4;
                    }
                }

                geom.setAttribute('color', new BufferAttribute(colorArray, 3));
                setTerrainData({ geometry: geom, maxHeights });
            } catch (e) {
                console.error("Error processing terrain image:", e);
                generateProcedural();
            }
        };

        img.onerror = () => {
            clearTimeout(timeoutId);
            console.error("Failed to load terrain image, falling back to procedural");
            generateProcedural();
        };
        
        return () => {
            clearTimeout(timeoutId);
            geom.dispose();
        };
    }, []);

    // 2. Target Markers (Floating points above peaks)
    const markers = useMemo(() => {
        const items = [];
        // Real locations near Fuji (approximate relative positions)
        // These are just illustrative labels for the "Fuji" context
        const placeNames = ["SUMMIT STATION", "BASE CAMP 1", "GOTEMBA TRAIL", "LAKE KAWAGUCHI", "AOKIGAHARA", "SHRINE POINT", "DATA LINK", "SAT UPLINK"];
        
        for(let i=0; i<8; i++) { 
            const x = (Math.random() - 0.5) * 8.0;
            const z = (Math.random() - 0.5) * 8.0;
            items.push({ 
                position: new Vector3(x, 0, z), 
                label: `TGT-${i}`,
                name: placeNames[i] || `SECTOR ${i}`
            });
        }
        return items;
    }, []);

    useFrame((state) => {
        if (!groupRef.current || !meshRef.current || !fillMeshRef.current || !terrainData) return;
        
        const exp = expansionRef.current;
        const { maxHeights } = terrainData;
        
        // --- TRANSITION LOGIC ---
        // CHANGED: Terrain starts appearing at 0.5 (50%), Fully formed at 1.0
        let progress = (exp - 0.5) / 0.5;
        progress = Math.max(0, Math.min(1, progress));
        
        // Snap to avoid jitter at max
        if (progress > 0.99) progress = 1.0;

        groupRef.current.visible = progress > 0.01;
        if (!groupRef.current.visible) return;

        // --- INTERACTION LOGIC (RIGHT HAND) ---
        const rightHand = handTrackingRef.current.rightHand;
        let speedZ = 0.002; // Default slow spin
        let speedX = 0;

        if (rightHand) {
            const { x, y } = rightHand.rotationControl;
            // X-Axis input -> Spin (Z-axis rotation for plane)
            // FINE TUNING: Threshold 0.02 (responsive), Speed 0.02 (very slow)
            if (Math.abs(x) > 0.02) {
                speedZ = x * 0.02; 
            }
            // Y-Axis input -> Tilt (X-axis rotation for group)
            if (Math.abs(y) > 0.02) {
                speedX = y * 0.015;
            }
        }

        if (spinRef.current) {
            spinRef.current.rotation.z -= speedZ;
        }
        
        if (tiltRef.current) {
            // Clamp tilt to avoid flipping completely
            // Base is -Math.PI / 2.5 (~ -72 deg)
            // Allow +/- 30 degrees range
            tiltRef.current.rotation.x += speedX;
        }

        // --- ANIMATE GEOMETRY ---
        if (meshRef.current.geometry && meshRef.current.geometry.attributes.position) {
            const positionAttribute = meshRef.current.geometry.attributes.position;
            const positions = positionAttribute.array as Float32Array;
            
            for (let i = 0; i < positions.length / 3; i++) {
                // CHANGED: Reduced height multiplier from 2.0 to 0.8 for flatter look
                const targetH = maxHeights[i] * 0.8 * progress; 
                
                const x = positions[i*3];
                const wave = Math.sin(x * 2 + state.clock.elapsedTime * 2) * 0.1 * progress;
                
                const finalH = targetH + wave;

                positions[i*3 + 2] = finalH;
            }
            positionAttribute.needsUpdate = true;
        }

        // --- ANIMATE MARKERS ---
        if (markersRef.current) {
             markersRef.current.children.forEach((child, idx) => {
                 const m = markers[idx];
                 if (!m) return;
                 
                 const currentHeight = 0.5 + progress * 1.5;
                 
                 child.position.set(m.position.x, m.position.z, currentHeight);
                 
                 const head = child.children[1] as Group;
                 if (head) {
                     head.lookAt(state.camera.position);
                     const outerRing = head.children[0]; 
                     if (outerRing) {
                         outerRing.rotation.z -= 0.02;
                     }
                     const centerDot = head.children[2];
                     if (centerDot) {
                         const scale = 1 + Math.sin(state.clock.elapsedTime * 8 + idx) * 0.2;
                         centerDot.scale.setScalar(scale);
                     }
                 }
             });
        }

        // Radar Ring Animation
        if (ringRef.current) {
            ringRef.current.scale.setScalar(1 + (state.clock.elapsedTime % 2) * 0.5);
            (ringRef.current.material as any).opacity = 0.5 * (1 - (state.clock.elapsedTime % 2) / 2);
        }
    });

    if (!terrainData) return null;

    return (
        <group ref={groupRef} visible={false}>
             {/* Slanted Tactical View */}
             <group ref={tiltRef} rotation={[-Math.PI / 2.5, 0, 0]} position={[0, -1, 0]}> 
                
                <group ref={spinRef}>
                    {/* Base Grid (Static floor) */}
                    <gridHelper 
                        args={[30, 30, 0x001133, 0x000510]} 
                        position={[0, 0, 0.1]} 
                        rotation={[Math.PI/2, 0, 0]}
                    />

                    {/* Wireframe Terrain */}
                    <mesh ref={meshRef} geometry={terrainData.geometry}>
                        <meshBasicMaterial 
                            vertexColors
                            wireframe
                            transparent 
                            opacity={0.6} 
                            blending={AdditiveBlending}
                        />
                    </mesh>

                    {/* Fill Terrain */}
                    <mesh ref={fillMeshRef} geometry={terrainData.geometry}>
                        <meshBasicMaterial 
                            color="#000000" 
                            transparent 
                            opacity={0.8}
                            side={DoubleSide}
                        />
                    </mesh>

                    {/* Floating Targets */}
                    <group ref={markersRef}>
                        {markers.map((m, i) => (
                            <group key={i} position={[m.position.x, m.position.z, 0]}>
                                {/* Tether */}
                                <mesh position={[0, 0, -1.5]} rotation={[Math.PI/2, 0, 0]}>
                                    <cylinderGeometry args={[0.005, 0.02, 3, 4]} /> 
                                    <meshBasicMaterial 
                                        color="#00F0FF" 
                                        transparent 
                                        opacity={0.3} 
                                        blending={AdditiveBlending} 
                                        depthWrite={false} 
                                    />
                                </mesh>

                                {/* Head */}
                                <group>
                                    <mesh rotation={[0,0, Math.random() * Math.PI]}>
                                        <ringGeometry args={[0.15, 0.16, 32, 1, 0, Math.PI * 1.5]} />
                                        <meshBasicMaterial color="#00F0FF" transparent opacity={0.6} blending={AdditiveBlending} side={DoubleSide} depthWrite={false} />
                                    </mesh>
                                    
                                    <mesh rotation={[0,0,Math.PI/4]}>
                                        <ringGeometry args={[0.08, 0.09, 4]} />
                                        <meshBasicMaterial color="#00F0FF" transparent opacity={0.8} blending={AdditiveBlending} side={DoubleSide} depthWrite={false} />
                                    </mesh>

                                    <mesh>
                                        <circleGeometry args={[0.03, 16]} />
                                        <meshBasicMaterial color="#FF2A2A" transparent opacity={0.9} blending={AdditiveBlending} depthWrite={false} />
                                    </mesh>

                                    <group position={[0.25, 0.05, 0]}>
                                        <mesh position={[-0.1, -0.05, 0]} rotation={[0,0,Math.PI/4]}>
                                            <planeGeometry args={[0.1, 0.01]} />
                                            <meshBasicMaterial color="#00F0FF" opacity={0.5} transparent blending={AdditiveBlending} />
                                        </mesh>
                                        
                                        <mesh position={[0.3, 0, 0]}>
                                            <planeGeometry args={[0.8, 0.16]} />
                                            <meshBasicMaterial color="#000510" transparent opacity={0.8} />
                                        </mesh>
                                        
                                        <Text
                                            position={[0.3, 0, 0.01]}
                                            fontSize={0.08}
                                            color="#00F0FF"
                                            anchorX="center"
                                            anchorY="middle"
                                        >
                                            {m.name}
                                        </Text>
                                    </group>
                                </group>
                            </group>
                        ))}
                    </group>

                    {/* Radar Ring */}
                    <mesh ref={ringRef} position={[0,0,0.2]}>
                        <ringGeometry args={[1.5, 1.55, 64]} />
                        <meshBasicMaterial color="#00F0FF" transparent opacity={0.5} blending={AdditiveBlending} side={DoubleSide} />
                    </mesh>
                </group>
             </group>
        </group>
    );
};


const HolographicEarth: React.FC<HolographicEarthProps> = ({ handTrackingRef, setRegion }) => {
  const earthGroupRef = useRef<Group>(null); 
  const earthRef = useRef<Mesh>(null);
  const cloudsRef = useRef<Mesh>(null);
  const wireframeRef = useRef<Mesh>(null);
  const ringRef = useRef<Mesh>(null);
  const particlesRef = useRef<any>(null);
  
  const smoothExpansionRef = useRef(0);
  const wasTerrainModeRef = useRef(false);

  // Load Color, Normal, and Specular maps for realistic texture
  const [colorMap, normalMap, specularMap] = useLoader(TextureLoader, [
    '/textures/earth_atmos_2048.jpg',
    '/textures/earth_normal_2048.jpg',
    '/textures/earth_specular_2048.jpg'
  ]);
  
  const satelliteData = useMemo(() => {
     try {
         return random.inSphere(new Float32Array(1500), { radius: 2.2 }) as Float32Array;
     } catch (e) {
         return new Float32Array(1500);
     }
  }, []);

  useFrame((state, delta) => {
    if (!earthRef.current || !earthGroupRef.current) return;

    const leftHand = handTrackingRef.current.leftHand;
    const rightHand = handTrackingRef.current.rightHand;
    let targetExpansion = 0;

    // 1. 360 Rotation & Scrolling Control (Right Hand)
    let currentSpeedX = 0.0005; // Default ambient spin
    let currentSpeedY = 0;
    
    if (rightHand) {
        const { x, y } = rightHand.rotationControl;
        
        // X-Axis Control (Spinning Left/Right)
        // FINE TUNING: Threshold 0.02 (responsive), Speed 0.02 (very slow)
        if (Math.abs(x) > 0.02) {
            currentSpeedX = -x * 0.02;
        }
        
        // Y-Axis Control (Tilting/Scrolling Up/Down)
        // We apply this to the entire group for a tumbling effect
        if (Math.abs(y) > 0.02) {
            currentSpeedY = y * 0.02;
        }
    }
    
    // Apply Spin (Y-axis) to individual components to maintain opposing wireframe rotation
    earthRef.current.rotation.y += currentSpeedX;
    if (cloudsRef.current) cloudsRef.current.rotation.y += currentSpeedX * 1.1;
    // Wireframe rotates counter to earth for tech effect
    if (wireframeRef.current) wireframeRef.current.rotation.y -= (currentSpeedX * 0.5);
    
    // Apply Tilt (X-axis) to the container group
    earthGroupRef.current.rotation.x += currentSpeedY;


    // 2. Expansion/Zoom Control (Left Hand)
    if (leftHand) {
      targetExpansion = leftHand.expansionFactor;

      const movementDelta = Math.abs(targetExpansion - smoothExpansionRef.current);
      if (movementDelta > 0.002) {
          SoundService.playServo(movementDelta);
      }
    }

    smoothExpansionRef.current += (targetExpansion - smoothExpansionRef.current) * 0.08;
    const exp = smoothExpansionRef.current;

    // --- VISIBILITY & TRANSITION CONTROL ---
    
    // CHANGED: Earth starts fading earlier (0.4) to separate from Terrain (0.5+)
    // Fade out range: 0.4 to 0.6
    let earthOpacity = 1;
    if (exp > 0.4) {
        earthOpacity = 1 - ((exp - 0.4) / 0.2); 
        earthOpacity = Math.max(0, Math.min(1, earthOpacity));
    }
    
    earthGroupRef.current.visible = earthOpacity > 0.01;

    if (earthGroupRef.current.visible) {
        if (earthRef.current.material) (earthRef.current.material as any).opacity = 0.9 * earthOpacity;
        if (cloudsRef.current?.material) (cloudsRef.current.material as any).opacity = 0.15 * earthOpacity;
        if (wireframeRef.current?.material) (wireframeRef.current.material as any).opacity = 0.2 * earthOpacity;
        if (ringRef.current?.material) (ringRef.current.material as any).opacity = 0.1 * earthOpacity;
        if (particlesRef.current) particlesRef.current.visible = earthOpacity > 0.5;
    }

    // CHANGED: Adjusted sound trigger to match new 50% threshold
    if (exp > 0.55) {
        if (!wasTerrainModeRef.current) {
            SoundService.playMapSwitch();
            wasTerrainModeRef.current = true;
        }
    } else {
        wasTerrainModeRef.current = false;
    }

    // --- Earth Animations (Only if visible) ---
    if (earthGroupRef.current.visible) {
        const baseScale = 1.5;
        const coreScale = baseScale * (1 - Math.max(0, exp - 0.3) * 0.5); 
        earthRef.current.scale.set(coreScale, coreScale, coreScale);

        const cloudScale = baseScale * 1.02 + (exp * 1.0); 
        if (cloudsRef.current) {
            cloudsRef.current.scale.set(cloudScale, cloudScale, cloudScale);
            // Cloud rotation handled above in shared block
            cloudsRef.current.rotation.y += (exp * 0.01);
        }

        const wireScale = baseScale * 1.2 + (exp * 2.0);
        if (wireframeRef.current) {
            wireframeRef.current.scale.set(wireScale, wireScale, wireScale);
             // Wireframe rotation handled above in shared block
             wireframeRef.current.rotation.y -= (exp * 0.02);
        }

        if (ringRef.current) {
            ringRef.current.scale.set(1 + exp, 1 + exp, 1 + exp);
            ringRef.current.rotation.z -= currentSpeedX * 1.5;
            ringRef.current.rotation.x = (Math.PI / 2) + (Math.sin(state.clock.elapsedTime * 0.2) * 0.1) + (exp * 0.5);
        }

        if (particlesRef.current) {
            particlesRef.current.rotation.y += 0.001;
            particlesRef.current.scale.set(1 + exp * 1.5, 1 + exp * 1.5, 1 + exp * 1.5);
        }

        const rotationY = earthRef.current.rotation.y % (Math.PI * 2);
        const normalizedRotation = rotationY < 0 ? rotationY + Math.PI * 2 : rotationY;
        const degrees = (normalizedRotation * 180) / Math.PI;
        
        if (degrees > 30 && degrees < 100) setRegion(RegionName.AMERICAS);
        else if (degrees >= 100 && degrees < 190) setRegion(RegionName.PACIFIC);
        else if (degrees >= 190 && degrees < 280) setRegion(RegionName.ASIA);
        else if (degrees >= 280 && degrees < 330) setRegion(RegionName.AFRICA);
        else setRegion(RegionName.EUROPE);
    }
  });

  return (
    <group position={[0, 0, 0]}>
        <EffectComposer enableNormalPass={false}>
           <Bloom luminanceThreshold={0.2} mipmapBlur intensity={1.5} radius={0.6} />
        </EffectComposer>

        {/* EARTH GROUP */}
        <group ref={earthGroupRef}>
            <mesh ref={earthRef}>
                <sphereGeometry args={[1, 64, 64]} />
                <meshPhongMaterial 
                    map={colorMap} 
                    normalMap={normalMap}
                    specularMap={specularMap}
                    color="#0066ff"
                    emissive="#001133"
                    emissiveMap={colorMap} // Continents will glow
                    emissiveIntensity={0.5}
                    specular="#111111"
                    shininess={15}
                    transparent={true}
                    opacity={0.95}
                    blending={AdditiveBlending}
                />
            </mesh>

            <mesh ref={cloudsRef}>
                <sphereGeometry args={[1.01, 64, 64]} />
                <meshBasicMaterial 
                    map={colorMap}
                    color="#00F0FF"
                    transparent
                    opacity={0.2}
                    blending={AdditiveBlending}
                />
            </mesh>

            <mesh ref={wireframeRef}>
                <icosahedronGeometry args={[1, 2]} />
                <meshBasicMaterial 
                    color="#002FA7" 
                    wireframe 
                    transparent 
                    opacity={0.2} 
                    blending={AdditiveBlending}
                />
            </mesh>

            <group ref={particlesRef} rotation={[0,0,Math.PI/4]}>
                <Points positions={satelliteData} stride={3} frustumCulled={false}>
                    <PointMaterial
                        transparent
                        color="#00F0FF"
                        size={0.015}
                        sizeAttenuation={true}
                        depthWrite={false}
                        blending={AdditiveBlending}
                    />
                </Points>
            </group>

            <mesh ref={ringRef} rotation={[Math.PI / 2.3, 0, 0]}>
                <ringGeometry args={[2.0, 2.4, 128]} />
                <meshBasicMaterial 
                    color="#00F0FF" 
                    side={DoubleSide} 
                    transparent 
                    opacity={0.1} 
                    blending={AdditiveBlending}
                />
            </mesh>
        </group>
        
        {/* TERRAIN MODEL OVERLAY */}
        <TerrainModel expansionRef={smoothExpansionRef} handTrackingRef={handTrackingRef} />
        
        <ambientLight intensity={0.2} color="#002FA7" />
        <pointLight position={[10, 10, 10]} intensity={2} color="#00F0FF" />
        <pointLight position={[-10, -10, -5]} intensity={1} color="#FF00FF" />
    </group>
  );
};

export default HolographicEarth;