// Scene setup
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050505, 0.002);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 2000);
camera.position.z = 1000;

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('canvas-container').appendChild(renderer.domElement);

// Particles setup
const geometry = new THREE.BufferGeometry();
const particleCount = 2000; // Number of particles

const positions = new Float32Array(particleCount * 3);
const scales = new Float32Array(particleCount);

let i = 0, j = 0;

for (let ix = 0; ix < particleCount; ix++) {
    const x = (Math.random() * 2 - 1) * 800;
    const y = (Math.random() * 2 - 1) * 800;
    const z = (Math.random() * 2 - 1) * 800;

    positions[i] = x;
    positions[i + 1] = y;
    positions[i + 2] = z;

    scales[j] = 1;

    i += 3;
    j++;
}

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('scale', new THREE.BufferAttribute(scales, 1));

// Create a custom shader material for glowy particles
const material = new THREE.PointsMaterial({
    color: 0x00aaff,
    size: 4,
    sizeAttenuation: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
});

const particles = new THREE.Points(geometry, material);
scene.add(particles);

// Mouse interaction
let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;

const windowHalfX = window.innerWidth / 2;
const windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', onDocumentMouseMove);
window.addEventListener('resize', onWindowResize);

function onDocumentMouseMove(event) {
    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    render();
}

function render() {
    targetX = mouseX * 0.001;
    targetY = mouseY * 0.001;

    particles.rotation.y += 0.002;
    particles.rotation.x += 0.001;

    // Interactive movement based on mouse
    particles.rotation.y += 0.05 * (targetX - particles.rotation.y);
    particles.rotation.x += 0.05 * (targetY - particles.rotation.x);

    // Wave effect
    const positions = particles.geometry.attributes.position.array;
    const time = Date.now() * 0.0005;

    for (let i = 0; i < particleCount; i++) {
        // Simple wave motion on Y axis
        // positions[i * 3 + 1] += Math.sin((i + time) * 0.5) * 0.5;
        
        // Let's make it breathe/pulse
        // scales[i] = (Math.sin((i + time) * 0.3) + 1) * 2 + 1;
    }
    
    // Color cycling
    const h = (360 * (1.0 + time) % 360) / 360;
    material.color.setHSL(h, 0.5, 0.5);

    particles.geometry.attributes.position.needsUpdate = true;
    
    renderer.render(scene, camera);
}

animate();